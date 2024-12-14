import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()

# Set your API keys
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
PINECONE_API_KEY = ""

def load_and_split_pdf(pdf_path):
    """
    Load PDF and split it into chunks
    """
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    # Split pages into chunks
    chunks = text_splitter.split_documents(pages)
    return chunks

def create_embeddings_and_store(chunks, index_name):
    """
    Create embeddings and store them in Pinecone
    """
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create or get Pinecone index
    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            metric='cosine',
            dimension=1536, # OpenAI embeddings dimension
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    # Create vector store and upload documents
    vector_store = PineconeVectorStore.from_documents(
        chunks,
        index_name=index_name,
        embedding=embeddings,
        pinecone_api_key=PINECONE_API_KEY
    )
    
    return vector_store

def process_pdf_to_pinecone(pdf_path, index_name):
    """
    Main function to process PDF and store embeddings
    """
    try:
        # Initialize Pinecone
        
        # Load and split PDF
        print("Loading and splitting PDF...")
        chunks = load_and_split_pdf(pdf_path)
        print(f"Created {len(chunks)} chunks from PDF")
        
        # Create embeddings and store in Pinecone
        print("Creating embeddings and storing in Pinecone...")
        vector_store = create_embeddings_and_store(chunks, index_name)
        print("Successfully stored embeddings in Pinecone")
        
        return vector_store
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    pdf_path = "islpwebsite.pdf"
    index_name = "advdatascience"
    
    vector_store = process_pdf_to_pinecone(pdf_path, index_name)