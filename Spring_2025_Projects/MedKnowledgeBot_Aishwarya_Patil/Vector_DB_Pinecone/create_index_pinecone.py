import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import openai
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Get API keys from environment
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
openai.api_key = openai_api_key

# Embedding model details
embedding_model = "text-embedding-ada-002"
embedding_dimension = 1536  # fixed for ada-002

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Define index name
index_name = "mediqbot-index"

# Check if index exists and create it if it doesn't
index_list = pc.list_indexes()

if index_name not in [index.name for index in index_list]:
    # Create a new serverless index
    pc.create_index(
        name=index_name,
        dimension=embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  # choose your closest region
        )
    )
    logger.info(f"Created new index: {index_name}")
else:
    logger.info(f"Index {index_name} already exists")

print(f"Pinecone index '{index_name}' is ready with dimension {embedding_dimension}")
