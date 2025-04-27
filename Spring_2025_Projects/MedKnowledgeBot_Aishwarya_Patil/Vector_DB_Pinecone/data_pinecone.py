import json
import os
import boto3
import openai
from pinecone import Pinecone
from dotenv import load_dotenv
from tqdm import tqdm
import logging
import time

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pinecone_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize S3 client
def initialize_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        return s3_client
    except Exception as e:
        logger.error(f"Error initializing S3 client: {e}")
        return None

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with overlap"""
    if not text or len(text) == 0:
        return []
        
    words = text.split()
    chunks = []
    
    # If text is shorter than chunk_size, return it as is
    if len(words) <= chunk_size:
        return [text]
    
    # Create chunks with overlap
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

def get_openai_embedding(text):
    """Get embeddings from OpenAI API"""
    try:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        logger.error(f"Error getting OpenAI embedding: {e}")
        return None

def load_documents_from_s3(bucket_name, s3_key):
    """Load documents from a JSON file in S3"""
    try:
        # Initialize S3 client
        s3_client = initialize_s3_client()
        if not s3_client:
            return []
        
        # Download JSON file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
        documents = json.loads(content)
        
        logger.info(f"Loaded {len(documents)} documents from s3://{bucket_name}/{s3_key}")
        return documents
    except Exception as e:
        logger.error(f"Error loading documents from S3: {e}")
        return []

def process_and_upload_to_pinecone(documents, index_name, batch_size=50):
    """Create embeddings for document chunks and upload to Pinecone"""
    try:
        # Initialize Pinecone
        api_key = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=api_key)
        
        # Connect to index
        index = pc.Index(index_name)
        
        # Variables to track progress
        total_vectors = 0
        batch_vectors = []
        
        # Process each document
        for doc_idx, doc in tqdm(enumerate(documents), total=len(documents), desc="Processing documents"):
            doc_id = doc.get('id', f"doc_{doc_idx}")
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            # Skip documents with no text
            if not text or len(text) == 0:
                logger.warning(f"Document {doc_id} has no text, skipping")
                continue
            
            # Create chunks from text
            chunks = chunk_text(text)
            logger.info(f"Document {doc_id} chunked into {len(chunks)} pieces")
            
            # Process each chunk
            for chunk_idx, chunk in enumerate(chunks):
                try:
                    # Create a unique vector ID
                    vector_id = f"{doc_id}_chunk_{chunk_idx}"
                    
                    # Generate embedding using OpenAI
                    embedding = get_openai_embedding(chunk)
                    
                    if embedding:
                        # Prepare vector record with metadata
                        record = {
                            'id': vector_id,
                            'values': embedding,
                            'metadata': {
                                **metadata,  # Include all original metadata
                                'chunk_idx': chunk_idx,
                                'chunk_text': chunk[:100] + "..." if len(chunk) > 100 else chunk,  # Include snippet of text
                                'doc_id': doc_id
                            }
                        }
                        
                        # Add to batch
                        batch_vectors.append(record)
                        
                        # Upload when batch is full
                        if len(batch_vectors) >= batch_size:
                            index.upsert(vectors=batch_vectors)
                            total_vectors += len(batch_vectors)
                            logger.info(f"Uploaded batch of {len(batch_vectors)} vectors. Total: {total_vectors}")
                            batch_vectors = []
                            time.sleep(1)  # Sleep to avoid rate limiting
                    else:
                        logger.warning(f"Failed to get embedding for chunk {chunk_idx} of document {doc_id}")
                        
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_idx} of document {doc_id}: {e}")
            
        # Upload any remaining vectors
        if batch_vectors:
            index.upsert(vectors=batch_vectors)
            total_vectors += len(batch_vectors)
            logger.info(f"Uploaded final batch of {len(batch_vectors)} vectors. Total: {total_vectors}")
        
        logger.info(f"Successfully uploaded {total_vectors} vectors to Pinecone index '{index_name}'")
        return total_vectors
    
    except Exception as e:
        logger.error(f"Error in process_and_upload_to_pinecone: {e}")
        return 0

if __name__ == "__main__":
    # Configuration
    BUCKET_NAME = "mediqbot-data"  # Your S3 bucket name
    S3_KEY = "processed/all_documents_combined.json"  # Path to your combined JSON file in S3
    INDEX_NAME = "mediqbot-index"  # Pinecone index name
    BATCH_SIZE = 50  # Number of vectors to upload in each batch
    
    # Load documents from S3
    documents = load_documents_from_s3(BUCKET_NAME, S3_KEY)
    
    if documents:
        # Process and upload to Pinecone
        total_vectors = process_and_upload_to_pinecone(documents, INDEX_NAME, BATCH_SIZE)
        print(f"Uploaded a total of {total_vectors} vectors to Pinecone")
    else:
        print("No documents to process or error loading documents from S3")