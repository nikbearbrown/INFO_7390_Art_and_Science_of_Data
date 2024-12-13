import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def pinecone_connection():
    """
    Establish a connection to Pinecone by retrieving API key and index name from environment variables.
    """
    try:
        # Retrieve Pinecone credentials
        pinecone_api_key = os.environ.get('PINECONE_API_KEY')
        index_name = os.environ.get('INDEX')
        
        # Validate credentials
        if not pinecone_api_key or not index_name:
            raise ValueError("Pinecone API key or index name is missing.")
        
        return pinecone_api_key, index_name
    except Exception as e:
        print(f"Exception in pinecone_connection function: {e}")
        return None, None

def openai_connection():
    """
    Establish a connection to OpenAI by retrieving the API key from environment variables.
    """
    try:
        # Retrieve OpenAI API key
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        
        # Validate API key
        if not openai_api_key:
            raise ValueError("OpenAI API key is missing.")
        
        return openai_api_key
    except Exception as e:
        print(f"Exception in openai_connection function: {e}")
        return None
