import os
from dotenv import load_dotenv
import logging
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
from nltk.tokenize import sent_tokenize
import openai
import pinecone
from pinecone import Pinecone, ServerlessSpec
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_log = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
openai.api_key = os.getenv("OPENAI_API_KEY")

youtube_index_name = "youtube-query-index"
DIMENSION = 1536
METRIC = "cosine"

if not YOUTUBE_API_KEY or not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
    logging.error("API keys missing in environment variables.")
    exit(1)

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

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

def combined_short_transcripts(transcript, min_length=700):
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

def get_ada_embedding(text):
    """
    Generate embeddings using the ADA model.
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

def search_youtube_videos(query, max_results=2):
    """
    Search YouTube for videos related to the given query.
    """
    try:
        response = youtube.search().list(
            q=query + ' itinerary',
            part="snippet",
            type="video",
            maxResults=max_results
        ).execute()

        videos = [
            {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            } for item in response["items"]
        ]
        return videos
    except Exception as e:
        logging.error(f"Error searching YouTube videos: {e}")
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
    Store the transcript into Pinecone with metadata.
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
    search_queries = [
        "Paris",
        "Lisbon",
        "Hungary",
        "Barcelona",
        "Rome",
        "Switzerland",
        "Vienna",
        "Athens",
        "Europe",
        "Bali",
        "New Orleans",
        "Kerry, Ireland",
        "Marrakesh, Morocco",
        "Sydney",
        "The Maldives",
        "Cape Town, South Africa",
        "Dubai, U.A.E",
        "Bora Bora, French Polynesia",
        "New York",
        "Dubrovnik, Croatia",
        "Edinburgh, Scotland",
        "Paro Valley, Bhutan",
        "Jaipur, India",
        "Waikato, New Zealand",
        "Havana, Cuba",
        "Tokyo, Japan",
        "Antarctica",
        "Vancouver, Canada",
        "Los Angeles",
        "Kruger National Park, South Africa",
        "Santorini, Greece",
        "Moscow, Russia",
        "Singapore",
        "London, England",
        "Rio de Janeiro, Brazil",
        "Petra, Jordan",
        "Hong Kong",
        "Barbados",
        "Amsterdam",
        "Santiago, Chile",
        "Cairo, Egypt",
        "Seoul, Korea",
        "Laucala Island Resort, Fiji",
        "Providencia, Colombia",
        "Machu Picchu, Peru",
        "Virunga National Park, Democratic Republic of Congo",
        "Lisbon, Portugal",
        "Hanoi, Vietnam",
        "Hawaii",
        "Beijing, China",
        "Budapest, Hungary",
        "Cinque Terre, Italy",
        "Buenos Aires, Argentina",
        "Las Vegas",
        "Banff and Jasper National Parks, Canada",
        "Torres del Paine National Park, Chile",
        "Glacier National Park, USA",
        "Mount Kilimanjaro, Tanzania",
        "Banjaran Hotsprings, Malaysia",
        "Aoraki/Mount Cook National Park, New Zealand",
        "Tasmania, Australia",
        "Redwood National Park, USA",
        "Ilulissat Icefjord, Greenland",
        "Gobi Desert, Mongolia",
        "Luang Prabang, Laos",
        "Yogyakarta, Indonesia",
        "Oaxaca, Mexico",
        "Fez, Morocco",
        "Tbilisi, Georgia",
        "Samarkand, Uzbekistan",
        "Tallinn, Estonia",
        "Vilnius, Lithuania",
        "Ronda, Spain",
        "Medellín, Colombia",
        "Valencia, Spain",
        "San Miguel de Allende, Mexico",
        "Kuala Lumpur, Malaysia",
        "Reykjavik, Iceland",
        "Porto, Portugal",
        "Krakow, Poland",
        "Manila, Philippines",
        "Chiang Mai, Thailand",
        "Andaman and Nicobar Islands, India",
        "Seychelles Outer Islands",
        "Raja Ampat Islands, Indonesia",
        "The Whitsundays, Australia",
        "Tahiti, French Polynesia",
        "Exuma Cays, Bahamas",
        "Madagascar Beaches",
        "Koh Samui, Thailand",
        "Salar de Uyuni, Bolivia",
        "Trans-Siberian Railway, Russia",
        "Bhutanese Himalayas",
        "Silk Road, Central Asia",
        "Churchill, Canada",
        "Uluru, Australia",
        "Lake Baikal, Russia",
        "Bagan, Myanmar",
        "Bumthang Valley, Bhutan",
        "Lake Louise, Canada"
    ]
    
    for search_query in search_queries:
        logging.info(f"Processing query: {search_query}")
        videos = search_youtube_videos(search_query)

        if not videos:
            logging.info(f"No videos found for the query '{search_query}'. Please try again.")
            continue

        logging.info(f"Found {len(videos)} videos for the query '{search_query}'")

        for video in videos:
            video_id = video["videoId"]
            video_title = video["title"]
            logging.info(f"Fetching transcript for video ID: {video_id}")
            transcript = get_transcript(video_id)

            if transcript:
                store_transcript_in_pinecone(transcript, video_id, video_title)
            else:
                logging.info(f"Transcript not available for video ID: {video_id}")
        
        time.sleep(5)  # Pause between queries to avoid rate limiting
