import os
from dotenv import load_dotenv
import openai
import pinecone
import logging
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_log = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
openai.api_key = os.getenv("OPENAI_API_KEY")

youtube_index_name = "youtube-index"
DIMENSION = 1536  
METRIC = "cosine"

if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT or not YOUTUBE_API_KEY:
    logging.error("API keys missing in environment variables.")
    exit(1)

pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

if youtube_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=youtube_index_name,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    logging.info(f"Index '{youtube_index_name}' created successfully.")
else:
    logging.info(f"Index '{youtube_index_name}' already exists.")

youtube_index = pc.Index(youtube_index_name)

nltk.download("punkt")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_ada_embedding(text):
    """
    This model is used to generate embeddings of dimension 1536.
    """
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        _log.error(f"Error generating ADA embedding for text: {e}")
        return None

def combined_short_transcripts(transcript, min_length=300):
    consolidated_transcript = []
    current_text = ""
    current_start = None

    for record in transcript:
        if current_start is None:
            current_start = record['start']

        current_text += " " + record['text']

        if len(current_text.strip()) >= min_length:
            consolidated_transcript.append({
                "text": current_text.strip(),
                "start": current_start
            })
            current_text = ""
            current_start = None
    if current_text.strip() and len(current_text.strip()) >= min_length:
        consolidated_transcript.append({
            "text": current_text.strip(),
            "start": current_start
        })

    return consolidated_transcript

def get_channel_videos(channel_username):
    """
    Fetch all video IDs from the given channel username.
    """
    try:
        channel_response = youtube.channels().list(
            part="snippet,contentDetails",
            forUsername=channel_username
        ).execute()

        if "items" not in channel_response or not channel_response["items"]:
            logging.error("Channel not found.")
            return []

        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        videos = []

        next_page_token = None
        while True:
            playlist_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            videos.extend([
                {
                    "videoId": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"]
                } for item in playlist_response["items"]
            ])

            next_page_token = playlist_response.get("nextPageToken")
            if not next_page_token:
                break

        return videos
    except Exception as e:
        logging.error(f"Error fetching channel videos: {e}")
        return []

def get_transcript(video_id, language="en"):
    """
    Fetch YouTube video transcript using the Transcript API.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except Exception as e:
        logging.error(f"Error fetching transcript for video {video_id}: {str(e)}")
        return []

def store_transcript_in_pinecone(transcript, video_id, video_title):
    """
    Store the transcript into Pinecone with timestamp data.
    """
    consolidated_transcript = combined_short_transcripts(transcript)

    for record in consolidated_transcript:
        text = record["text"]
        embedding = get_ada_embedding(text)

        if embedding is None:
            continue

        vector_data = {
            "id": f"{video_id}-{record['start']}",
            "values": embedding,
            "metadata": {
                "video_id": video_id,
                "timestamp": record["start"],
                "text": text,
                "title": video_title
            },
        }

        try:
            youtube_index.upsert([(vector_data["id"], vector_data["values"], vector_data["metadata"])])
            logging.info(f"Transcript entry at {record['start']}s stored successfully.")
        except Exception as e:
            logging.error(f"Failed to store transcript entry at {record['start']}s: {e}")

if __name__ == "__main__":
    channel_username = "AllanSu"
    videos = get_channel_videos(channel_username)

    if not videos:
        logging.info("No videos found for the channel. Please try again.")
        exit(1)

    logging.info(f"Found {len(videos)} videos for the channel '{channel_username}'")

    for video in videos:
        video_id = video["videoId"]
        video_title = video["title"]
        logging.info(f"Fetching transcript for video ID: {video_id}")
        transcript = get_transcript(video_id)

        if transcript:
            logging.info(f"Storing transcript for video ID: {video_id}")
            store_transcript_in_pinecone(transcript, video_id, video_title)
            logging.info(f"Transcript for video ID: {video_id} stored successfully.")
        else:
            logging.info(f"Transcript not available for video ID: {video_id}")
