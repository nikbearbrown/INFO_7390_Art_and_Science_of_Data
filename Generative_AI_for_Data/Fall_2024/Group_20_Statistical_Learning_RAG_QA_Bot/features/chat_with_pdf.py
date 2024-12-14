import streamlit as st
import requests
import os
from fast_api.services.google_codelabs import start_codelab_server
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
@st.fragment
def download_fragment(file_content: bytes, file_name: str) -> None:
    st.download_button('**Download File**', data=file_content, file_name=file_name, key="download_file_button")

def chat_pdf():
    st.title(f"Chat with Textbook")
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = None
    if 'response' not in st.session_state:
        st.session_state.response = None

    user_input = st.chat_input("Enter your query:")

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state['history']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if user_input:
        st.session_state.user_input = user_input
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state['history'].append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            params = {
                "input_query": user_input,
                "index_name": "advdatascience"
            }
            response = requests.get(
                f"{os.getenv("FAST_API_URL")}/langraph/get-langraph-response/",
                params=params
            )

            if response.status_code == 200:
                # Parse the JSON response
                response_data = response.json()

                st.session_state.response = response_data
            
                message_placeholder.markdown(response_data)
                st.session_state['history'].append({"role": "assistant", "content": response_data})

    # Add a clear button
    if st.button("Clear Chat"):
        st.session_state['history'] = []
        st.rerun()
    
    if st.button("Extract Into PDF"):
        params = {
            "md_text": st.session_state.response
        }
        response = requests.get(
            f"{os.getenv("FAST_API_URL")}/download/download-pdf/",
            params=params
        )

        if response.status_code == 200:

            download_fragment(response.content, f"advds_report.pdf")
        else:
            st.error("Error generating PDF")
    # if st.button("Extract Report Into Codelabs"):
    
    #     content = st.session_state.response
    #     # Define the payload to match the expected JSON format
    #     payload = {
    #         "content": content
    #     }
        
    #     try:
    #         response = requests.get(
    #             f"{os.getenv('FAST_API_URL')}/google-codelabs/create-codelab",
    #             json=payload
    #         )
    #         if response.status_code == 200:
    #             start_codelab_server()
    #         else:
    #             st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    #     except requests.RequestException as e:
    #         st.error(f"Request failed: {e}")