import streamlit as st
import requests
import openai
import os
import numpy as np
import faiss
import pickle

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# File paths - Update these paths to relative paths or ENV variables for production
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.index")
ID_MAPPING_PATH = os.getenv("ID_MAPPING_PATH", "id_mapping.pkl")
CONTENT_DICT_PATH = os.getenv("CONTENT_DICT_PATH", "content_dict.pkl")

# Load FAISS index, ID mapping, and content dictionary
try:
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)
    id_mapping = pickle.load(open(ID_MAPPING_PATH, "rb"))
    content_dict = pickle.load(open(CONTENT_DICT_PATH, "rb"))
except Exception as e:
    raise RuntimeError(f"Error loading FAISS index or data files: {e}")

def rag_api(user_query: str, top_k: int = 5) -> dict:
    """
    Retrieval-Augmented Generation (RAG) pipeline: Retrieve context from FAISS index,
    then generate a response using OpenAI.
    """
    try:
        # Step 1: Generate embedding for the user query
        query_embedding = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=user_query
        )["data"][0]["embedding"]

        query_embedding = np.array(query_embedding, dtype=np.float32)

        # Step 2: Perform semantic search
        distances, indices = faiss_index.search(query_embedding.reshape(1, -1), top_k)
        results = []
        context = ""

        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(id_mapping):
                result_id = id_mapping[idx] if isinstance(id_mapping, list) else id_mapping.get(idx)
                if result_id:
                    for item in content_dict:
                        if "id" in item and item["id"] == result_id:
                            file_name_chunk_no = item.get("text_chunk", "No file_name_chunk_no available")
                            results.append({"file_name_chunk_no": file_name_chunk_no, "distance": float(dist)})
                            context += f"{file_name_chunk_no}\n\n"
                            break

        # Step 3: Generate a response using RAG
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions using the provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_query}"}
            ]
        )

        generated_response = response["choices"][0]["message"]["content"]

        return {
            "query": user_query,
            "results": results,
            "response": generated_response
        }

    except Exception as e:
        return {"error": str(e)}




# Set up the page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a sidebar for prompt selection
st.sidebar.header("Conversation Settings")
st.sidebar.subheader("About This App")
st.sidebar.write(
    """
    Welcome to the Arizona Legal Case Assistant! 🚀
    
    This bot is powered by a rich database containing over 100 detailed legal case documents specific to the state of Arizona. 
    Explore precedent cases, understand legal nuances, or gather insights for research right at your fingertips.
    
    Use the input box below to ask your legal questions or search for case-specific information, and let the wealth of Arizona's legal history assist you!
    """
)


# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to chat about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response from RAG Flask API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call Flask RAG API
            response_data = rag_api(prompt, top_k=5)

            if "response" in response_data:
                full_response = response_data["response"]
                message_placeholder.markdown(full_response)
            else:
                st.error(f"Error from API: {response_data.get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
