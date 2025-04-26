"""
Helper module for Pinecone vector database operations.
Uses HuggingFace embeddings locally and OpenAI embeddings in cloud environments.
"""
import os
import logging
import socket
from typing import List, Dict, Any, Optional

from pinecone import Pinecone, ServerlessSpec
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PineconeHelper:
    """Helper class for Pinecone operations."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        index_name: Optional[str] = None,
        force_embedding: Optional[str] = None  # Can be 'huggingface' or 'openai' to force
    ):
        """
        Initialize Pinecone helper.
        
        Args:
            api_key: Pinecone API key (default: read from environment variable)
            openai_api_key: OpenAI API key (default: read from environment variable)
            index_name: Name of the Pinecone index (default: read from environment variable)
            force_embedding: Force a specific embedding model ('huggingface' or 'openai')
        """
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.index_name = index_name or os.getenv("PINECONE_INDEX_NAME", "medical-knowledge")
        
        if not self.api_key:
            raise ValueError("Pinecone API key is required. Set it as an argument or PINECONE_API_KEY environment variable.")
        
        # Determine if running on EC2 or locally
        is_ec2 = self._is_running_on_ec2() if force_embedding is None else (force_embedding.lower() == 'openai')
        
        # Initialize embeddings based on environment
        if is_ec2:
            # Running on EC2 - use OpenAI embeddings
            if not self.openai_api_key:
                raise ValueError("OpenAI API key is required for cloud deployment. Set it as OPENAI_API_KEY environment variable.")
            
            self._init_openai_embeddings()
        else:
            # Running locally - use HuggingFace embeddings
            self._init_huggingface_embeddings()
        
        # Initialize Pinecone
        self._init_pinecone()
    
    def _is_running_on_ec2(self) -> bool:
        """
        Determine if code is running on EC2 by checking system metadata
        or hostname patterns common to EC2 instances.
        """
        try:
            # Try to access EC2 metadata service with a short timeout
            import requests
            response = requests.get(
                "http://169.254.169.254/latest/meta-data/instance-id", 
                timeout=0.1
            )
            return response.status_code == 200
        except Exception:
            # If metadata service is not available, check hostname
            hostname = socket.gethostname()
            return hostname.startswith("ip-") or "ec2" in hostname
        
    def _init_huggingface_embeddings(self):
        """Initialize HuggingFace embeddings."""
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            embedding_model_name = "NeuML/pubmedbert-base-embeddings"
            logger.info(f"Initializing HuggingFace embedding model: {embedding_model_name}")
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
            self.dimension = 768  # PubMedBERT has 768 dimensions
            logger.info("Successfully initialized HuggingFace embeddings")
        except Exception as e:
            logger.error(f"Error initializing HuggingFace embeddings: {str(e)}")
            raise
    
    def _init_openai_embeddings(self):
        """Initialize OpenAI embeddings."""
        try:
            from langchain_openai import OpenAIEmbeddings
            embedding_model = "text-embedding-3-large"
            logger.info(f"Initializing OpenAI embedding model: {embedding_model}")
            self.embeddings = OpenAIEmbeddings(
                model=embedding_model,
                openai_api_key=self.openai_api_key,
                dimensions=1536
            )
            self.dimension = 1536  # OpenAI embedding dimension
            logger.info("Successfully initialized OpenAI embeddings")
        except Exception as e:
            logger.error(f"Error initializing OpenAI embeddings: {str(e)}")
            raise
    
    def _init_pinecone(self) -> None:
        """Initialize Pinecone and ensure index exists."""
        try:
            logger.info(f"Initializing Pinecone with index: {self.index_name}")
            
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=self.api_key)
            
            # List all indexes
            try:
                indexes = self.pc.list_indexes()
                index_names = [idx.name for idx in indexes]
                logger.info(f"Available indexes: {index_names}")
                
                if self.index_name not in index_names:
                    logger.info(f"Creating new Pinecone index: {self.index_name}")
                    
                    # Create serverless index
                    index_config = self.pc.create_index(
                        name=self.index_name,
                        dimension=self.dimension,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                    # Get the host from the created index
                    self.host = index_config.host
                    logger.info(f"Created new index with host: {self.host}")
                else:
                    # Get the existing index description
                    index_description = self.pc.describe_index(name=self.index_name)
                    self.host = index_description.host
                    logger.info(f"Using existing index with host: {self.host}")
            except Exception as e:
                logger.error(f"Error checking/creating index: {str(e)}")
                raise
            
            # Get the index
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Successfully connected to Pinecone index: {self.index_name}")
            
            # Get index stats to verify connection
            try:
                stats = self.index.describe_index_stats()
                logger.info(f"Index stats: {stats}")
            except Exception as e:
                logger.warning(f"Could not get index stats: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise
    
    def get_langchain_vectorstore(self) -> "PineconeVectorStore":
        """
        Get LangChain Pinecone vector store.
        
        Returns:
            PineconeVectorStore: LangChain Pinecone vector store
        """
        from langchain_pinecone import PineconeVectorStore
        return PineconeVectorStore(
            index=self.index,
            embedding=self.embeddings,
            text_key="text"
        )
    
    def create_from_documents(self, documents: List[Document]) -> "PineconeVectorStore":
        """
        Create vector store from documents.
        
        Args:
            documents: List of documents to store
            
        Returns:
            PineconeVectorStore: LangChain Pinecone vector store
        """
        try:
            logger.info(f"Creating vector store with {len(documents)} documents")
            from langchain_pinecone import PineconeVectorStore
            vector_store = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                text_key="text"
            )
            vector_store.add_documents(documents)
            return vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a retriever for the vector store.
        
        Args:
            search_kwargs: Search parameters (default: {"k": 3})
            
        Returns:
            Retriever: LangChain retriever
        """
        if search_kwargs is None:
            search_kwargs = {"k": 3}
        
        try:
            vector_store = self.get_langchain_vectorstore()
            return vector_store.as_retriever(search_kwargs=search_kwargs)
        except Exception as e:
            logger.error(f"Error creating retriever: {str(e)}")
            raise
    
    def similarity_search(self, query: str, k: int = 3):
        """
        Perform similarity search.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of documents and their scores
        """
        try:
            vector_store = self.get_langchain_vectorstore()
            return vector_store.similarity_search_with_score(query=query, k=k)
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise
