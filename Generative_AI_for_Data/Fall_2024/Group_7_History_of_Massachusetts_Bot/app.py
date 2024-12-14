import streamlit as st
import time
from RAGChat import RAGChat

st.set_page_config(
    page_title="Mass History RAG Bot",  # Title of the tab
    page_icon="📖", 
)

# Initialize RAGChat once and store it in session state
if "rag_chat" not in st.session_state:
    st.session_state.rag_chat = RAGChat(markdown_directory="./")

rag_chat = st.session_state.rag_chat

st.image("logo.png", width=150)
st.title("History of Massachusetts Q&A Bot")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []
    st.session_state.first_response = True

if st.session_state.first_response:
    initial_message = "How can I help you today?"
    st.session_state.conversation.append({"sender": "assistant", "text": initial_message})
    st.session_state.first_response = False

# Display conversation history
for msg in st.session_state.conversation:
    with st.chat_message(msg["sender"]):
        st.markdown(msg["text"])

# User input
if user_input := st.chat_input("What's on your mind?"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.conversation.append({"sender": "user", "text": user_input})

    # Generate response using RAGChat
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_text = ""
        try:
            # Get the answer from RAGChat
            response_text = rag_chat.get_answer(user_input)
            response_placeholder.markdown(response_text)
        except Exception as e:
            response_text = f"Error: {str(e)}"
            response_placeholder.markdown(response_text)

        st.session_state.conversation.append({"sender": "assistant", "text": response_text})

