"""
Test script to verify OpenAI integration.
"""
from openai_helper import OpenAIHelper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_models():
    """Test OpenAI models."""
    print("Testing OpenAI models...")
    try:
        # Initialize OpenAI helper
        helper = OpenAIHelper()
        
        # Get embedding model
        embeddings = helper.get_embeddings()
        
        # Get LLM
        llm = helper.get_llm()
        
        # Test embeddings
        test_text = "This is a test of the OpenAI embedding model."
        embedding = embeddings.embed_query(test_text)
        
        print(f"✅ Successfully generated embedding with {len(embedding)} dimensions")
        
        # Test LLM
        response = llm.invoke("What is metastatic disease?")
        
        print(f"✅ Successfully generated response from LLM:")
        print(f"\nResponse: {response.content}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing OpenAI models: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=== OPENAI INTEGRATION TESTS ===\n")
    
    # Test OpenAI models
    test_openai_models()
    
    print("\n=== ALL TESTS COMPLETED ===")

if __name__ == "__main__":
    main()
