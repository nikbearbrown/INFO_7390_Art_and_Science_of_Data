import os
import logging
import openai
import boto3
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from typing import List
from botocore.config import Config
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
boto_config = Config(retries={'max_attempts': 10, 'mode': 'standard'}, max_pool_connections=50)

# Initialize API keys and clients
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Pinecone
pinecone_client = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Configure S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id_rag=os.getenv('AWS_ACCESS_KEY_ID_RAG'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_RAG'),
    config=boto_config
)

# Configuration
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Define Pinecone index map
INDEX_MAP = {
    'sporting': "sporting-regulations-embeddings",
    'financial': "financial-regulations-embeddings",
    'technical': "technical-regulations-embeddings"
}

# Ensure Pinecone indexes exist
def ensure_index_exists(index_name: str, dimension: int = 1536):
    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=dimension,
            metric="euclidean",
            spec=ServerlessSpec(cloud="aws", region=os.getenv('PINECONE_REGION'))
        )
        logging.info(f"Created Pinecone index: {index_name}")
    else:
        logging.info(f"Pinecone index already exists: {index_name}")

# Ensure all necessary indexes are created
def initialize_indexes():
    for index_name in INDEX_MAP.values():
        ensure_index_exists(index_name)

# PDF Loader using Docling
class DoclingPDFLoader(BaseLoader):
    def __init__(self, file_path: str | List[str]):
        self._file_paths = file_path if isinstance(file_path, list) else [file_path]
        self._converter = DocumentConverter()

    def lazy_load(self) -> LCDocument:
        for source in self._file_paths:
            dl_doc = self._converter.convert(source).document
            text = dl_doc.export_to_markdown()
            yield LCDocument(page_content=text)

# Extract text from PDF
def extract_text_from_pdf(file_path: str) -> List[LCDocument]:
    loader = DoclingPDFLoader(file_path=file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(docs)

# Fetch documents from specific folders in S3
def fetch_documents(folders: List[str], years: List[str]) -> List[dict]:
    documents = []
    for folder in folders:
        logging.info(f"Fetching documents from folder: {folder}")
        try:
            response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=folder)
            if 'Contents' in response:
                filtered_documents = [
                    {'id': obj['Key'], 's3_key': obj['Key'], 'category': folder.rstrip('/')}
                    for obj in response['Contents']
                    if any(year in obj['Key'] for year in years) and obj['Key'].endswith('.pdf')
                ]
                documents.extend(filtered_documents)
                logging.info(f"Found {len(filtered_documents)} documents in {folder}.")
            else:
                logging.warning(f"No documents found in folder: {folder}")
        except Exception as e:
            logging.error(f"Error fetching documents from folder {folder}: {e}")
    return documents

# Generate embeddings using OpenAI
def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    try:
        logging.info("Generating embedding for text...")
        response = openai.Embedding.create(input=text, model=model)
        embedding = response['data'][0]['embedding']
        logging.info("Embedding generated successfully.")
        return embedding
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        return []

# Upsert embedding into Pinecone
def upsert_to_pinecone(index_name: str, vector_id: str, embedding: List[float], metadata: dict):
    try:
        logging.info(f"Upserting embedding to Pinecone index {index_name}...")
        index = pinecone_client.Index(index_name)
        index.upsert(vectors=[(vector_id, embedding, metadata)])
        logging.info("Embedding upserted successfully.")
    except Exception as e:
        logging.error(f"Error upserting to Pinecone: {e}")

# Process a single document
def process_document(document: dict):
    try:
        regulation_id = document.get('id')
        s3_key = document.get('s3_key')
        category = document.get('category')

        if not regulation_id or not s3_key or not category:
            logging.error(f"Invalid document structure: {document}")
            return

        local_file_path = f"/tmp/{os.path.basename(s3_key)}"
        s3_client.download_file(AWS_BUCKET_NAME, s3_key, local_file_path)

        # Extract text chunks from the document
        chunks = extract_text_from_pdf(local_file_path)
        if not chunks:
            logging.warning(f"No text chunks extracted for {regulation_id}. Skipping...")
            return

        for i, chunk in enumerate(chunks):
            vector_id = f"{regulation_id}_chunk_{i+1}"
            embedding = generate_embedding(chunk.page_content)
            if not embedding:
                logging.warning(f"Embedding generation failed for chunk {i} of {regulation_id}. Skipping...")
                continue

            # Add the full text of the chunk to the metadata
            metadata = {
                "s3_key": s3_key,
                "chunk": i + 1,
                "category": category,
                "text": chunk.page_content
            }
            upsert_to_pinecone(INDEX_MAP[category], vector_id, embedding, metadata)

    except Exception as e:
        logging.error(f"Error processing document {document}: {e}")

# Process documents from folders with specific year filters
def process_documents():
    folders = ['sporting/', 'financial/', 'technical/']
    years = ['2024', '2026']
    initialize_indexes()
    documents = fetch_documents(folders, years)

    if not documents:
        logging.warning("No documents found containing specified years.")
        return

    for document in documents:
        process_document(document)

if __name__ == "__main__":
    logging.info("Starting document processing...")
    process_documents()