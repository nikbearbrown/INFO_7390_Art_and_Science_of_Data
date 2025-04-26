"""
Test script to verify Pinecone connection and functionality.
"""
from langchain.schema import Document
from dotenv import load_dotenv
from pinecone_helper import PineconeHelper

# Load environment variables
load_dotenv()

def test_pinecone_connection():
    """Test basic Pinecone connection."""
    print("Testing Pinecone connection...")
    try:
        helper = PineconeHelper()
        print("✅ Connection successful!")
        return helper
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return None

def test_document_insertion(helper):
    """Test document insertion."""
    print("\nTesting document insertion...")
    try:
        # Create sample documents
        documents = [
            Document(
                page_content="Metastatic disease is a term used to describe cancer that has spread from the primary site to other parts of the body.",
                metadata={"source": "test_doc_1.pdf"}
            ),
            Document(
                page_content="Common treatments for metastatic disease include chemotherapy, radiation therapy, surgery, and targeted therapies.",
                metadata={"source": "test_doc_2.pdf"}
            )
        ]
        
        # Insert documents
        vector_store = helper.create_from_documents(documents)
        print(f"✅ Successfully inserted {len(documents)} documents!")
        return True
    except Exception as e:
        print(f"❌ Document insertion failed: {str(e)}")
        return False

def test_similarity_search(helper):
    """Test similarity search."""
    print("\nTesting similarity search...")
    try:
        # Query
        query = "What is metastatic disease?"
        results = helper.similarity_search(query, k=1)
        
        # Display results
        for i, (doc, score) in enumerate(results):
            print(f"\nResult {i+1} (score: {score}):")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
        
        print("✅ Similarity search successful!")
        return True
    except Exception as e:
        print(f"❌ Similarity search failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=== PINECONE VERIFICATION TESTS ===\n")
    
    # Test connection
    helper = test_pinecone_connection()
    if not helper:
        return
    
    # Test document insertion
    insertion_success = test_document_insertion(helper)
    if not insertion_success:
        return
    
    # Test similarity search
    test_similarity_search(helper)
    
    print("\n=== ALL TESTS COMPLETED ===")

if __name__ == "__main__":
    main()
