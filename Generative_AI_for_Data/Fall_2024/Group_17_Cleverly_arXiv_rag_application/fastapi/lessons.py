import logging
from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from pydantic import BaseModel
from typing import Optional, List
import logging
from pinecone import Pinecone, ServerlessSpec
# from transformers import CLIPProcessor, CLIPModel
# import torch
import time
from syllabus import get_embedding
from config import (
    client,
    youtube,
    index,
    youtube_index,
    image_index
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retrieve_detailed_explanation(title: str, description: str, top_k: int = 50) -> str:
    """
    Retrieve detailed explanations for the given title and description by querying Pinecone dynamically.
    """
    try:
        logging.info("Starting retrieval of detailed explanations.")
        logging.info(f"Title: {title}")
        logging.info(f"Description: {description}")
        logging.info(f"Top_k parameter: {top_k}")

        # Dynamically create a query based on the title and description
        query_text = f"Find detailed explanations relevant to the following context:\nTitle: {title}\nDescription: {description}"
        logging.info("Generated query text for embedding.")
        
        query_embedding = get_embedding(query_text)
        if not query_embedding:
            logging.error("Failed to generate embedding. Query embedding is empty.")
            raise ValueError("Query embedding is empty.")
        logging.info("Successfully generated query embedding.")

        # Query Pinecone
        logging.info("Querying Pinecone with generated embedding.")
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Process results
        if results and results.get("matches"):
            logging.info(f"Received {len(results['matches'])} matches from Pinecone.")
            chunks = []
            for match in results["matches"]:
                score = match["score"]
                chunk_id = match["metadata"].get("chunk_id", "N/A")
                text = match["metadata"].get("text", "").strip()

                logging.info(f"Processing match with score: {score}, Chunk ID: {chunk_id}")
                if score >= 0.85:  # Threshold for relevance
                    if text:
                        logging.info(f"Adding chunk with score {score} and Chunk ID {chunk_id}.")
                        chunks.append(f"Chunk ID: {chunk_id}. {text}")

            if chunks:
                logging.info("Successfully processed and filtered relevant chunks.")
                return "\n\n".join(chunks)
            else:
                logging.warning("No relevant chunks found after filtering.")
                return "No relevant explanation found."

        logging.warning("No matches received from Pinecone.")
        return "No relevant explanation found."

    except Exception as e:
        logging.error(f"Error occurred during explanation retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving explanation: {str(e)}")

# Function for summarizing text
def summarize_text(text: str, max_length: int = 100) -> str:
    try:
        logger.info("Summarizing input text")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model if you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize this text in {max_length} characters: {text}"}
            ],
            max_tokens=max_length,
        )

        # Access the content of the response correctly
        summary = response.choices[0].message.content.strip()
        logger.info(f"Summarized text: {summary}")
        return summary

    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")


# Function for chunking text
def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Fetching relevant YouTube videos
def fetch_youtube_videos(query: str, max_results: int = 3) -> List[dict]:
    try:
        logger.info("Fetching YouTube videos for query: %s", query)
        search_response = youtube.search().list(
            q=query, part="snippet", type="video", maxResults=max_results
        ).execute()
        videos = [
            {
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
            }
            for item in search_response.get("items", [])
        ]
        return videos
    except Exception as e:
        logger.error(f"Error fetching YouTube videos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching YouTube videos: {str(e)}")

# Fetch video transcript
def fetch_video_transcript(video_id: str) -> Optional[str]:
    try:
        logger.info("Fetching transcript for video ID: %s", video_id)
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript_data])
    except Exception as e:
        # Check if the error is due to transcripts being disabled
        if "TranscriptsDisabled" in str(e):
            logger.warning(f"Transcript disabled for video ID: {video_id}")
            return None
        logger.error(f"Error fetching transcript for video {video_id}: {str(e)}")
        return None


# Generate embeddings for text
def generate_embedding(text: str) -> List[float]:
    try:
        logger.info("Generating embeddings for text")
        response = client.embeddings.create(model="text-embedding-ada-002", input=text)
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")

# Upsert video data to Pinecone
def upsert_to_pinecone(video_id: str, title: str, description: str, transcript_chunks: List[str]) -> None:
    try:
        logger.info("Upserting data to Pinecone for video ID: %s", video_id)
        for idx, chunk in enumerate(transcript_chunks):
            embedding = generate_embedding(chunk)
            youtube_index.upsert([
                {
                    "id": f"{video_id}_chunk_{idx}",
                    "values": embedding,
                    "metadata": {
                        "title": title,
                        "description": description,
                        "transcript_chunk": chunk,
                        "video_id": video_id,
                    },
                }
            ])
    except Exception as e:
        logger.error(f"Error upserting to Pinecone for video {video_id}: {str(e)}")

def summarize_text_arxiv(text: str) -> str:
    """
    Summarizes the text using OpenAI's GPT API with the preferred method.
    
    Args:
        text (str): The full summary text.
    
    Returns:
        str: A summarized version of the text.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the following text to 40-80 words:\n{text}"}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in summarize_text: {str(e)}")
        return "Summary not available due to an error."

# #---------image logic -------
# # Generate embedding for the query text using CLIP
# def generate_text_embedding(query_text: str, model: CLIPModel, processor: CLIPProcessor):
#     """
#     Generate embeddings for the query text using the CLIP model.
#     """
#     inputs = processor(text=query_text, return_tensors="pt")
#     with torch.no_grad():
#         embedding = model.get_text_features(**inputs).numpy().flatten()
#     return embedding

# # Query Pinecone and retrieve metadata
# def retrieve_from_image_index(query_text: str):
#     """
#     Query the Pinecone image index and retrieve metadata based on the text embedding.
#     """
#     try:
#         # Load CLIP model and processor
#         model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#         processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

#         # Generate query embedding
#         query_embedding = generate_text_embedding(query_text, model, processor)

#         # Query the Pinecone image index
#         results = image_index.query(
#             vector=query_embedding.tolist(),
#             top_k=5,
#             include_metadata=True
#         )

#         # Extract URLs from the results
#         image_urls = [result['metadata']['url'] for result in results['matches'] if 'url' in result['metadata']]

#         return image_urls
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error querying image index: {str(e)}")
    
# def summarize_image_with_openai(image_url: str, module_title: str) -> str:
#     """
#     Summarize the content of an image using OpenAI's GPT-4, incorporating the module title.
 
#     Args:
#         image_url (str): The URL of the image to summarize.
#         module_title (str): The title of the module associated with the image.
 
#     Returns:
#         str: The summary of the image content or an error message if it fails.
#     """ 
#     for attempt in range(3):  # Retry up to 3 times for transient errors
#         try:
#             # Log the start of the API call
#             logging.info(f"Attempting OpenAI API call. Attempt {attempt + 1} for URL: {image_url}")
 
#             # OpenAI ChatCompletion request
#             response = client.ChatCompletion.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "You are an assistant that summarizes images using their URLs and module titles. Keep the summary concise."},
#                     {"role": "user", "content": f"Summarize this image: {image_url} with the module title: {module_title}."}
#                 ]
#             )
 
#             # Extract the summary
#             summary = response["choices"][0]["message"]["content"]
#             logging.info(f"Summary generated successfully for URL: {image_url}")
#             return summary
 
#         except client.error.RateLimitError as rate_err:
#             # Handle rate limit errors by retrying after a short delay
#             logging.warning(f"Rate limit error: {rate_err}. Retrying in 2 seconds...")
#             time.sleep(2)  # Wait before retrying
 
#         except client.error.APIConnectionError as conn_err:
#             # Handle network or connection errors
#             logging.error(f"Connection error: {conn_err}. Retrying in 2 seconds...")
#             time.sleep(2)
 
#         except client.error.InvalidRequestError as invalid_err:
#             # Log invalid requests and break (no retry)
#             logging.error(f"Invalid request: {invalid_err}")
#             return "Error: Invalid request. Please check the inputs."
 
#         except client.error.AuthenticationError as auth_err:
#             # Log authentication errors and return immediately
#             logging.error(f"Authentication error: {auth_err}")
#             return "Error: Authentication failed. Please check the OpenAI API key."
 
#         except client.error.OpenAIError as openai_err:
#             # Handle other OpenAI-specific errors
#             logging.error(f"OpenAI error: {openai_err}")
#             return "Error: An issue occurred with the OpenAI API."
 
#         except Exception as e:
#             # Handle unexpected errors
#             logging.error(f"Unexpected error: {e}", exc_info=True)
#             return "Error generating summary. Please try again later."
 
#     # If all retries fail
#     logging.error(f"All retry attempts failed for URL: {image_url}")
#     return "Error: Unable to generate summary after multiple attempts." 
 

# def generate_image_summaries(image_urls: List[str]) -> List[dict]:
#     """
#     Helper function to summarize a list of image URLs.
 
#     Args:
#         image_urls (List[str]): A list of image URLs to summarize.
 
#     Returns:
#         List[dict]: A list of dictionaries with the image URL and its summary.
#     """
#     summaries = []
#     for url in image_urls:
#         try:
#             summary = summarize_image_with_openai(url)
#         except Exception as e:
#             logging.error(f"Error summarizing image {url}: {e}")
#             summary = "Unable to summarize image."
#         summaries.append({"url": url, "summary": summary})
#     return summaries