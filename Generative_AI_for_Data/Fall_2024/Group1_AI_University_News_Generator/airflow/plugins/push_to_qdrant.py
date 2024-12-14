import os
import json
import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embeddings(text: str) -> list:
    """
    Generate embeddings for the input text using OpenAI GPT API.

    Parameters:
        text (str): The input text to generate embeddings for.

    Returns:
        list: A list representing the generated embeddings.
    """
    try:
        logger.info("Generating embeddings for text.")
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=[text]  # Input must be a list
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise

def push_to_qdrant():
    """
    Push news articles to Qdrant with generated embeddings.
    """
    # Qdrant connection details from environment variables
    API_URL = os.getenv("QDRANT_API_URL")
    API_KEY = os.getenv("QDRANT_API_KEY")

    if not API_URL or not API_KEY:
        raise ValueError("Qdrant API URL or API Key is not set in the environment variables.")

    # Initialize Qdrant client
    client = QdrantClient(API_URL, api_key=API_KEY)

    # Collection name and vector size
    COLLECTION_NAME = "news_collection"
    VECTOR_SIZE = 1536  # Vector size for "text-embedding-ada-002"

    # Define vector configuration
    vector_config = VectorParams(size=VECTOR_SIZE, distance="Cosine")

    # Create or recreate the collection
    try:
        logger.info(f"Creating or updating the collection: {COLLECTION_NAME}.")
        if client.get_collection(COLLECTION_NAME):
            logger.info(f"Collection '{COLLECTION_NAME}' exists. Deleting it for recreation.")
            client.delete_collection(COLLECTION_NAME)
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=vector_config
        )
        logger.info(f"Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating collection in Qdrant: {e}")
        raise RuntimeError(f"Error creating collection in Qdrant: {e}")

    # Path to the JSON file
    json_file_path = "/opt/airflow/logs/news_output.json"  # Update path as per your setup

    # Load the JSON data
    if not os.path.exists(json_file_path):
        logger.error(f"JSON file not found at {json_file_path}.")
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    try:
        with open(json_file_path, "r") as f:
            articles = json.load(f)
            logger.info(f"Loaded {len(articles)} articles from {json_file_path}.")
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        raise

    # Prepare points for insertion into Qdrant
    points = []
    for idx, article in enumerate(articles):
        # Combine title and description for embedding generation
        content = (article.get("title", "") + " " + article.get("description", "")).strip()

        # Skip if there is no meaningful content
        if not content:
            logger.warning(f"Article {idx + 1} skipped due to missing content.")
            continue

        # Generate embeddings using OpenAI GPT
        try:
            vector = generate_embeddings(content)
        except Exception as e:
            logger.error(f"Failed to generate embeddings for article {idx + 1}: {e}")
            continue

        # Create a point with article details as payload
        points.append(
            PointStruct(
                id=idx + 1,
                vector=vector,
                payload={
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "source": article.get("source"),
                }
            )
        )

    # Insert data into Qdrant
    if points:
        try:
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            logger.info(f"Data pushed to Qdrant successfully with {len(points)} articles!")
        except Exception as e:
            logger.error(f"Error pushing data to Qdrant: {e}")
            raise RuntimeError(f"Error pushing data to Qdrant: {e}")
    else:
        logger.warning("No valid articles found to push to Qdrant.")

# Call the function for testing or integration
if __name__ == "__main__":
    push_to_qdrant()
