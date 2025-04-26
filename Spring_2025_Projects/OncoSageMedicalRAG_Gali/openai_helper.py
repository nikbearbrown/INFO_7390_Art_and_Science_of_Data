"""
Helper module for OpenAI model integration.
"""
import os
import logging
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIHelper:
    """Helper class for OpenAI model operations."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        embedding_model: str = "text-embedding-ada-002",
        chat_model: str = "gpt-3.5-turbo",
        temperature: float = 0.1
    ):
        """
        Initialize OpenAI helper.
        
        Args:
            api_key: OpenAI API key (default: read from environment variable)
            embedding_model: OpenAI embedding model name
            chat_model: OpenAI chat model name
            temperature: Temperature for generation (higher = more creative)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.temperature = temperature
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it as an argument or OPENAI_API_KEY environment variable.")
        
        # Initialize models
        self._init_models()
    
    def _init_models(self) -> None:
        """Initialize OpenAI models."""
        try:
            logger.info(f"Initializing OpenAI embedding model: {self.embedding_model}")
            self.embeddings = OpenAIEmbeddings(
                model=self.embedding_model,
                openai_api_key=self.api_key
            )
            
            logger.info(f"Initializing OpenAI chat model: {self.chat_model}")
            self.llm = ChatOpenAI(
                model_name=self.chat_model,
                temperature=self.temperature,
                openai_api_key=self.api_key
            )
            
            logger.info("Successfully initialized OpenAI models")
        except Exception as e:
            logger.error(f"Error initializing OpenAI models: {str(e)}")
            raise
    
    def get_embeddings(self) -> OpenAIEmbeddings:
        """
        Get OpenAI embeddings model.
        
        Returns:
            OpenAIEmbeddings: LangChain OpenAI embeddings model
        """
        return self.embeddings
    
    def get_llm(self) -> ChatOpenAI:
        """
        Get OpenAI LLM model.
        
        Returns:
            ChatOpenAI: LangChain OpenAI chat model
        """
        return self.llm
