import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

def load_css():
    st.markdown("""
        <style>
            .summary-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .summary-content {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 4px;
                margin: 1rem 0;
            }
            
            .summary-title {
                text-align: center;
                margin-bottom: 1.5rem;
            }
            
            .nav-buttons {
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin: 1rem 0;
            }

            .key-point {
                padding: 0.5rem 0;
                margin: 0.25rem 0;
            }

            .main-topic {
                padding: 0.5rem 0;
                margin: 0.25rem 0;
            }

            .summary-text {
                line-height: 1.6;
                margin: 1rem 0;
            }
        </style>
    """, unsafe_allow_html=True)

def fetch_folders():
    """Fetch only folder titles without loading PDFs"""
    try:
        response = requests.get(f"{FASTAPI_URL}/folders/list")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to load folder list: {str(e)}")
        return []

def show():
    load_css()
    
    # Folder selection section
    st.markdown("<div class='doc-selector'>", unsafe_allow_html=True)
    folders = fetch_folders()
    if not folders:
        st.warning("No folders available")
        return
    
    selected_folder = st.selectbox(
        "Select a document",
        options=[""] + [folder['title'] for folder in folders],
        index=0,
        key="folder_selector"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if selected_folder:
        st.session_state.pdf_for_summary = selected_folder
    
    pdf_title = st.session_state.get('pdf_for_summary')
    
    if not pdf_title:
        st.info("Please select a PDF from the dropdown above")
        return
    
    try:
        st.markdown(f"<h1 class='summary-title'>Summary: {pdf_title}</h1>", unsafe_allow_html=True)
        
        # Navigation buttons at the top
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("← Back to PDF View", use_container_width=True):
                    st.session_state['current_page'] = "PDF Selection"
                    st.rerun()
        
        # Summary content
        with st.container():
            st.markdown("<div class='summary-content'>", unsafe_allow_html=True)
            
            # Add a loading spinner while generating summary
            with st.spinner("Generating summary..."):
                try:
                    response = requests.get(
                        f"{FASTAPI_URL}/pdfs/{pdf_title}/process",
                        timeout=120  # Increased timeout
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display extracted text in expandable section
                        with st.expander("📄 View Extracted Text"):
                            st.text(result['extracted_text'])
                        
                        # Display summary
                        st.subheader("📋 Document Summary")
                        summary_data = result['summary']
                        
                        # Display Key Points
                        if summary_data.get('key_points'):
                            st.subheader("Key Points")
                            for point in summary_data['key_points']:
                                st.markdown(f"• {point}")
                        
                        # Display Main Topics
                        if summary_data.get('main_topics'):
                            st.subheader("Main Topics")
                            for topic in summary_data['main_topics']:
                                st.markdown(f"• {topic}")
                        
                        # Display Summary
                        if summary_data.get('summary'):
                            st.subheader("Detailed Summary")
                            st.write(summary_data['summary'])
                        
                        # Check if we have any content
                        if not any([
                            summary_data.get('key_points'),
                            summary_data.get('main_topics'),
                            summary_data.get('summary')
                        ]):
                            st.warning("No summary content was generated. The model might need adjustments.")
                            
                            # Display raw response for debugging
                            with st.expander("Show Raw Response"):
                                st.json(result)
                    else:
                        st.error(f"Failed to generate summary. Status code: {response.status_code}")
                        with st.expander("Show Error Details"):
                            st.json(response.json())
                            
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The summary generation is taking longer than expected. Please try again.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Bottom navigation
        with st.container():
            if st.button("← Back to PDF View", key="bottom_back", use_container_width=True):
                st.session_state['current_page'] = "PDF Selection"
                st.rerun()
                    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("← Back to PDF Selection"):
            st.session_state['current_page'] = "PDF Selection"
            st.rerun()

if __name__ == "__main__":
    show()