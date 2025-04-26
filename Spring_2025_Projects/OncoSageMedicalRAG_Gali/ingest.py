"""
Document ingestion module for Medical RAG QA system.
Processes documents and stores them in Pinecone vector database.
"""
import os
import logging
from pathlib import Path
from typing import List

# Updated imports for current LangChain version
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader

from pinecone_helper import PineconeHelper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_documents(data_dir: str = 'data/',
                     glob_pattern: str = "**/*.pdf",
                     chunk_size: int = 1000,
                     chunk_overlap: int = 100,
                     embedding_model: str = "text-embedding-3-large"):
    """
    Ingest documents into Pinecone vector database.
    
    Args:
        data_dir: Directory containing documents
        glob_pattern: Pattern to match files
        chunk_size: Size of document chunks
        chunk_overlap: Overlap between chunks
        embedding_model: Name of the OpenAI embedding model
    """
    try:
        logger.info(f"Starting document ingestion from {data_dir}")
        
        # Initialize Pinecone helper with OpenAI embeddings
        pinecone_helper = PineconeHelper(embedding_model=embedding_model)
        
        # Load documents
        loader = DirectoryLoader(data_dir, glob=glob_pattern, show_progress=True, loader_cls=PyPDFLoader)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents")
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(texts)} chunks")
        
        # Store in Pinecone
        pinecone_helper.create_from_documents(texts)
        logger.info("Documents successfully ingested into Pinecone")
        
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise

if __name__ == "__main__":
    ingest_documents()
