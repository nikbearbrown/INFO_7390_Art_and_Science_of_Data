import openai

def get_embedding(text, embedding_model="text-embedding-ada-002"):
    """
    Generate an embedding for a given text using OpenAI's embedding model.
    """
    try:
        response = openai.Embedding.create(
            input=[text],
            engine=embedding_model
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
