import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import streamlit as st

# Load environment variables
load_dotenv()

# Pinecone setup
PINECONE_API_KEY_f1 = os.getenv("PINECONE_API_KEY_f1")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENV")

# Validate environment variables
if not PINECONE_API_KEY_f1:
    raise ValueError("API key for Pinecone is missing.")

# Initialize Pinecone client
pinecone_client = Pinecone(api_key=PINECONE_API_KEY_f1)

# Check and create indexes if necessary
INDEX_NAMES = [
    "sporting-regulations-embeddings",
    "technical-regulations-embeddings",
    "financial-regulations-embeddings",
]

for index_name in INDEX_NAMES:
    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=384,  # Update this dimension based on the embeddings model used
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT),
        )

# Sentence Transformer model
MODEL_NAME = "all-MiniLM-L6-v2"  # Change the model name if needed
sentence_transformer_model = SentenceTransformer(MODEL_NAME)


def generate_embeddings_transformer(text):
    """
    Generate embeddings for the given text using Sentence Transformers.
    """
    try:
        embeddings = sentence_transformer_model.encode(text)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error generating embeddings with Sentence Transformers: {e}")
        return None


def query_pinecone(index_name, query_embedding, keywords, top_k=5):
    """
    Perform a hybrid search combining semantic search and keyword-based filtering.
    """
    try:
        # Access the specified index
        index = pinecone_client.index(index_name)  # Correctly access the index
        response = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        matches = response.get("matches", [])

        # Keyword-based filtering
        keyword_matches = [
            match for match in matches
            if any(keyword.lower() in match["metadata"].get("text", "").lower() for keyword in keywords)
        ]

        # Combine results with priority for keyword matches
        combined_results = keyword_matches + [m for m in matches if m not in keyword_matches]
        return combined_results[:top_k]
    except Exception as e:
        print(f"Error querying index {index_name}: {e}")
        return []
    



def fetch_relevant_documents(query):
    print("Generating embedding for the query using Sentence Transformers...")
    query_embedding = generate_embeddings_transformer(query)
    if not query_embedding:
        print("Failed to generate query embeddings.")
        return []

    all_results = []
    for index_name in INDEX_NAMES:
        print(f"Searching index: {index_name}...")
        # Pass an empty list for keywords if none are being used
        results = query_pinecone(index_name, query_embedding, keywords=[], top_k=10)
        for match in results:
            print(f"Match: {match['metadata'].get('text', '')[:100]}... (Score: {match.get('score', 0)})")
        all_results.extend(results)

    # Sort results by score in descending order
    sorted_results = sorted(all_results, key=lambda x: x.get("score", 0), reverse=True)
    return sorted_results[:5]


def get_combined_context(matches):
    """
    Combine text metadata from the top matches into a single context,
    while filtering duplicates.
    """
    seen_texts = set()
    contexts = []
    for match in matches:
        text = match["metadata"].get("text", "")
        if text and text not in seen_texts:
            seen_texts.add(text)
            contexts.append(text)
    return "\n\n".join(contexts[:3])  # Combine top 3 unique matches


def generate_answer_with_sentence_transformers(context, query):
    """
    Generate an answer based on the given context (using Sentence Transformers).
    This function is left as a placeholder and can be customized further.
    """
    if not context:
        return "No relevant information found in the database."

    # Placeholder for answer generation (you can integrate other logic or models)
    return f"Based on the context provided, here is the response for your query:\n\n{context}"


def main():
    """
    Main entry point for the F1 Regulations Assistant.
    """
    print("\n=== F1 Regulations Assistant ===")
    while True:
        query = input("\nEnter your question (type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting F1 Regulations Assistant. Goodbye!")
            break

        print("\nProcessing query...")
        matches = fetch_relevant_documents(query)
        context = get_combined_context(matches)
        answer = generate_answer_with_sentence_transformers(context, query)

        print("This is the context from the embeddings:")
        print(context)
        print("\nThis is the Answer:")
        print(answer)
        print("\n" + "="*50)


def show_paddockpal():

    # Input section for user queries
    query = st.text_input("Enter your question:", key="user_query")
    if st.button("Submit"):
        if not query.strip():
            st.warning("Please enter a valid question.")
        else:
            st.write("Processing your query...")
            matches = fetch_relevant_documents(query)
            context = get_combined_context(matches)

            st.subheader("Context from Database:")
            if context:
                st.text_area("Context:", value=context, height=200, disabled=True)
            else:
                st.write("No relevant context found.")

            st.subheader("Generated Answer:")
            answer = generate_answer_with_sentence_transformers(context, query)
            st.write(answer)

if __name__ == "__main__":
    main()