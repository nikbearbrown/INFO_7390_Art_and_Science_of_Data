import streamlit as st
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Claude Chat",
    page_icon="🤖",
    layout="wide"
)

# Initialize Anthropic client with API key from .env
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Set up session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page header
st.title("Chat with Claude 3.5 Sonnet")
st.markdown("简单的Claude AI聊天界面")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("输入您的问题...")

# Handle user input
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display Claude's thinking indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("思考中...")
        
        # Send request to Claude
        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=st.session_state.messages
        )
        
        # Extract and display Claude's response
        assistant_response = response.content[0].text
        message_placeholder.markdown(assistant_response)
    
    # Add Claude's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Add a sidebar with information
with st.sidebar:
    st.header("关于")
    st.markdown("这是一个简单的Streamlit应用，使用Claude 3.5 Sonnet模型。")
    st.markdown("确保您的.env文件中包含ANTHROPIC_API_KEY。")
    
    if st.button("清除对话历史"):
        st.session_state.messages = []
        st.rerun()
