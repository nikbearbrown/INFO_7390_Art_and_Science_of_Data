import os
import json
from openai import OpenAI
from qdrant_client import QdrantClient


def query_qdrant_and_generate_response(query_text, limit=5):
    """
    Query Qdrant for relevant articles and generate a GPT response.
    Save the GPT response to a JSON file for further use.

    Parameters:
        query_text (str): The user query or input to search in Qdrant.
        limit (int): The number of top results to fetch from Qdrant.

    Returns:
        str: The GPT-generated response.
    """
    # Validate environment variables
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_api_url = os.getenv("QDRANT_API_URL")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([qdrant_api_key, qdrant_api_url, openai_api_key]):
        raise ValueError("Missing one or more required environment variables: QDRANT_API_KEY, QDRANT_API_URL, OPENAI_API_KEY")

    # Initialize Qdrant client
    qdrant_client = QdrantClient(api_key=qdrant_api_key, url=qdrant_api_url)
    collection_name = "news_collection"

    # Ensure Qdrant collection exists
    try:
        qdrant_client.get_collection(collection_name)
    except Exception as e:
        raise ValueError(f"Collection '{collection_name}' does not exist in Qdrant: {e}")

    # TODO: Replace with actual query vector generation logic
    # Use an embedding model to generate the vector for `query_text`
    query_vector = [0] * 1536  # Placeholder vector

    # Search Qdrant for relevant embeddings
    try:
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
        )
    except Exception as e:
        raise RuntimeError(f"Error querying Qdrant: {e}")

    # Combine retrieved articles into a single input string for GPT
    retrieved_articles = [
        f"Title: {point.payload.get('title', 'N/A')}\nDescription: {point.payload.get('description', 'N/A')}"
        for point in search_results
    ]
    input_text = "\n\n".join(retrieved_articles)

    if not input_text:
        return "No relevant articles found in Qdrant for the given query."

    # Initialize OpenAI GPT client
    gpt_client = OpenAI(api_key=openai_api_key)

    # Generate response using GPT
    try:
        response = gpt_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant summarizing news."},
                {"role": "user", "content": f"Please summarize the following articles:\n\n{input_text}"},
            ],
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error generating response with GPT: {e}")

    # Save GPT response to a file
    output_path = "/opt/airflow/logs/gpt_response.json"
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump({"response": gpt_response}, f, indent=4)
        print(f"GPT response saved to {output_path}")
    except Exception as e:
        raise RuntimeError(f"Error saving GPT response to file: {e}")

    # Return GPT response
    return gpt_response
