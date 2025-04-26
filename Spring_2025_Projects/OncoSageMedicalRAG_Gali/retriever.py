"""
Module for retrieving documents from Pinecone vector database.
"""
from pinecone_helper import PineconeHelper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Demo function for Pinecone retrieval."""
    # Initialize Pinecone helper
    pinecone_helper = PineconeHelper()
    
    # Example query
    query = "What is Metastatic disease?"
    print(f"Query: {query}")
    
    # Perform similarity search
    docs = pinecone_helper.similarity_search(query=query, k=2)
    
    # Display results
    for i, (doc, score) in enumerate(docs):
        print(f"\nResult {i+1} (score: {score}):")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    main()
