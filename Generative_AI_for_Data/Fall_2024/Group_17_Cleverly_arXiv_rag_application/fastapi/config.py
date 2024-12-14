import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from pinecone import Pinecone, ServerlessSpec
from queue import Queue
import snowflake.connector

load_dotenv()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# -------- Initialize the environment variables --------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")
YOUTUBE_INDEX = os.getenv("YOUTUBE_INDEX")
DIMENSION = os.getenv("DIMENSION")
METRIC = os.getenv("METRIC")
CLOUD_PROVIDER = os.getenv("CLOUD_PROVIDER")
REGION = os.getenv("REGION")
IMAGE_INDEX= os.getenv("IMG_INDEX_NAME")
IMAGE_DIM= os.getenv("IMAGE_DIMENSIONS")

# Initialize OpenAI
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Check if the Pinecone index exists
existing_indexes = [idx["name"] for idx in pc.list_indexes()]
if INDEX_NAME not in existing_indexes:
    # Create the index if it doesn't exist
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(cloud=CLOUD_PROVIDER, region=REGION),
    )

# Connect to the index
index = pc.Index(INDEX_NAME)

if YOUTUBE_INDEX not in existing_indexes:
    # Create the YouTube index if it doesn't exist
    pc.create_index(
        name=YOUTUBE_INDEX,
        dimension=DIMENSION,  # Same dimension as embeddings
        metric=METRIC,
        spec=ServerlessSpec(cloud=CLOUD_PROVIDER, region=REGION),
    )

youtube_index = pc.Index(YOUTUBE_INDEX)

if IMAGE_INDEX not in existing_indexes:
    # Create the YouTube index if it doesn't exist
    pc.create_index(
        name=IMAGE_INDEX,
        dimension=IMAGE_DIM,  # Same dimension as embeddings
        metric=METRIC,
        spec=ServerlessSpec(cloud=CLOUD_PROVIDER, region=REGION),
    )

image_index = pc.Index(IMAGE_INDEX)

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA')
}

# JWT and security configurations
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 160