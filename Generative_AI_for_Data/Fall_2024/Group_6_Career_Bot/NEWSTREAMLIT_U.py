import streamlit as st
import openai
from pinecone import Pinecone

# Initialize OpenAI API
openai.api_key = "your_api"

# Initialize Pinecone
api_key = "pcsk_EB1ry_N9StDcXxKY6MEaxKkBRuZzczM3pYn9MUNC15jUC4p2XALtwpo7eocAcsGYpV3c5"
host = "https://career-guidance-index-rxt2r7i.svc.aped-4627-b74a.pinecone.io"  # Replace with your Pinecone host
pc = Pinecone(api_key=api_key)
index_name = "career-guidance"

# Check if index exists and create it if necessary
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Adjust dimension to your embedding size
        metric="cosine"
    )

# Connect to the index
index = pc.Index(name=index_name, host=host)

# Streamlit App
st.title("PRAJNA- The Career Guidance Bot")
st.markdown(
    """
    Welcome to **PRAJNA**, your personal career guidance assistant!  
    🔍 Ask questions about career growth, skills, opportunities, and more.  
    🤖 Powered by OpenAI and Pinecone for intelligent responses.
    """
)

# Initialize session state to maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to retain only the last 3 chat pairs
def trim_chat_history():
    if len(st.session_state.messages) > 6:  # Keep only 3 user-bot pairs (6 messages)
        st.session_state.messages = st.session_state.messages[-6:]

# Function to handle query submission
def handle_query():
    query = st.session_state.query  # Access the query from session state
    if query:
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Generate embedding for the query
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_embedding = response['data'][0]['embedding']

        # Query Pinecone for relevant context
        query_result = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )

        # Combine contexts
        context = "\n\n".join([match['metadata']['text'] for match in query_result['matches']])

        # Generate GPT-4 response
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages + [
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            max_tokens=300,
            temperature=0.5
        )

        # Extract the response message
        bot_response = gpt_response['choices'][0]['message']['content'].strip()

        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Retain only the last 3 user-bot chat pairs
        trim_chat_history()

        # Clear the query input field
        st.session_state.query = ""  # Reset the input field
    else:
        st.warning("Please enter a query!")

# Display chat history
st.write("### Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**User:** {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"**Prajna:** {message['content']}")

# Input for user query with "Enter" key support
st.text_input(
    "Enter your query:",
    key="query",  # Store the input in session_state
    on_change=handle_query,  # Call handle_query when "Enter" is pressed
    placeholder="Type your question and press Enter..."
)