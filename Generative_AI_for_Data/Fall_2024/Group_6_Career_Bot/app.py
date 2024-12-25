import os
os.system('pip install openai')
os.system('pip install pinecone-client')
os.system('pip install python-dotenv')

import streamlit as st
import openai
from pinecone import Pinecone

from dotenv import load_dotenv
load_dotenv()


openai.api_key = st.secrets["OPENAI_API_KEY"]
api_key = st.secrets["PINECONE_API_KEY"]
host = st.secrets["PINECONE_HOST"]
pc = Pinecone(api_key=api_key)

index_name = "career-guidance"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Adjust dimension to your embedding size
        metric="cosine"
    )

index = pc.Index(name=index_name, host=host)

st.title("PRAJNA- The Career Guidance Bot")
st.markdown(
    """
    Welcome to **PRAJNA**, your personal career guidance assistant!  
    🔍 Ask questions about career growth, skills, opportunities, and more.  
    🤖 Powered by OpenAI and Pinecone for intelligent responses.
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def trim_chat_history():
    if len(st.session_state.messages) > 6:  # Keep only 3 user-bot pairs (6 messages)
        st.session_state.messages = st.session_state.messages[-6:]


def handle_query():
    query = st.session_state.query
    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response['data'][0]['embedding']

        query_result = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        context = "\n\n".join([match['metadata']['text'] for match in query_result['matches']])


        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages + [
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            max_tokens=300,
            temperature=0.5
        )

        bot_response = gpt_response['choices'][0]['message']['content'].strip()

        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        trim_chat_history()

        st.session_state.query = ""  # Reset the input field
    else:
        st.warning("Please enter a query!")

st.write("### Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**User:** {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"**Prajna:** {message['content']}")

st.text_input(
    "Enter your query:",
    key="query",  # Store the input in session_state
    on_change=handle_query,  # Call handle_query when "Enter" is pressed
    placeholder="Type your question and press Enter..."
)
