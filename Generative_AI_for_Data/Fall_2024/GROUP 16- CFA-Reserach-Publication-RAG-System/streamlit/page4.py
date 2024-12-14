import streamlit as st
import requests
import logging
from datetime import datetime
from typing import Dict, List
import json
import os
import re

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi-app:8000")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_page_state():
    """Initialize session state variables for the page"""
    if 'selected_document' not in st.session_state:
        st.session_state.selected_document = None
    if 'selected_note' not in st.session_state:
        st.session_state.selected_note = None
    if 'current_notes' not in st.session_state:
        st.session_state.current_notes = []
    if 'sort_order' not in st.session_state:
        st.session_state.sort_order = "Newest First"
    if 'question' not in st.session_state:
        st.session_state.question = ""

def fetch_folders():
    """Fetch only folder titles without loading PDFs"""
    try:
        response = requests.get(f"{FASTAPI_URL}/folders/list")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to load folder list: {str(e)}")
        return []

def fetch_document_notes(folder_name: str) -> List[Dict]:
    """Fetch research notes for a specific document"""
    try:
        with st.spinner("Loading notes..."):
            response = requests.get(
                f"{FASTAPI_URL}/pdfs/{folder_name}/notes"
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    notes = result.get("notes", [])
                    logger.info(f"Retrieved {len(notes)} notes for document {folder_name}")
                    return notes
            logger.error(f"Failed to fetch notes: Status code {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching notes: {str(e)}")
        return []

def save_as_notes(report_data: Dict) -> bool:
    """Save the current report as a research note"""
    try:
        # Extract and clean text content
        text_blocks = []
        image_paths = []
        
        # Process each block in the report
        for block in report_data["report"]["blocks"]:
            if "text" in block:
                cleaned_text = clean_text_content(block["text"])
                if cleaned_text:
                    text_blocks.append(cleaned_text)
            elif "file_path" in block:
                if block["file_path"]:
                    image_paths.append(block["file_path"])
        
        if not text_blocks:
            st.error("Error: No text content to save")
            return False
        
        # Prepare note data
        note_data = {
            "timestamp": datetime.now().isoformat(),
            "query": report_data["metadata"]["query"],
            "text_blocks": text_blocks,
            "image_paths": image_paths
        }
        
        # Log the API endpoint and data being sent
        api_endpoint = f"{FASTAPI_URL}/pdfs/{report_data['metadata']['folder_name']}/save-note"
        logger.info(f"Sending request to: {api_endpoint}")
        logger.info(f"Note data: {json.dumps(note_data, indent=2)}")
        
        # Make the API request
        response = requests.post(
            api_endpoint,
            json=note_data,
            timeout=30
        )
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                st.success(f"""
                Research note saved successfully!
                - Query: {note_data['query']}
                - Text blocks: {len(text_blocks)}
                - Images: {len(image_paths)}
                """)
                return True
            else:
                error_msg = result.get("detail", "Unknown error occurred")
                st.error(f"Failed to save note: {error_msg}")
                return False
        else:
            error_msg = f"Server error: {response.status_code}"
            try:
                error_detail = response.json().get("detail", "No detail provided")
                error_msg = f"{error_msg} - {error_detail}"
            except:
                pass
            st.error(f"Failed to save note: {error_msg}")
            return False
                
    except requests.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        st.error(f"Failed to save note: {error_msg}")
        return False
        
    except Exception as e:
        logger.error(f"Error saving notes: {str(e)}")
        st.error(f"Error saving notes: {str(e)}")
        return False

def clean_text_content(text: str) -> str:
    """Clean and format text content from the report."""
    try:
        # Remove code block markers
        text = re.sub(r'```[a-zA-Z]*\n|```', '', text)
        
        # Remove specific markers
        text = re.sub(r'\[TEXT\]|\[/TEXT\]|\[IMAGE\]|\[/IMAGE\]', '', text)
        
        # Remove chunk references
        text = re.sub(r'\(Chunk \d+\)', '', text)
        
        # Clean up multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return text

def format_timestamp(timestamp: str) -> str:
    """Format timestamp to readable date/time with fallback"""
    if not timestamp:
        return "No date available"
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y %I:%M %p")
    except ValueError:
        try:
            if timestamp.isdigit():
                dt = datetime.fromtimestamp(int(timestamp))
                return dt.strftime("%B %d, %Y %I:%M %p")
        except:
            pass
        return str(timestamp)

def render_image(image_path: str):
    """Render an image with consistent styling"""
    try:
        image_url = f"{FASTAPI_URL}{image_path}"
        response = requests.get(image_url)
        if response.status_code == 200:
            st.image(
                response.content,
                use_column_width=True,
                caption="Document Image",
                output_format="PNG"
            )
    except Exception as e:
        logger.error(f"Error rendering image: {str(e)}")
        st.warning("Failed to load image")

def render_note_card(note: Dict):
    """Render a note card for selected notes section"""
    try:
        with st.container():
            st.markdown(f"""
                <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 4px; margin-bottom: 1rem;">
                    <div style="margin-bottom: 0.5rem;">
                        <strong>Note ID:</strong> {note.get('note_id', 'Unknown')}<br>
                        <strong>Created:</strong> {format_timestamp(note.get('timestamp', ''))}<br>
                        <strong>Query:</strong> {note.get('query', 'No query available')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Note content in collapsed state by default
            with st.expander("View Note Content", expanded=False):
                if note.get('content'):
                    st.markdown(note['content'])
                else:
                    st.info("No text content available")
                
                if note.get('image_paths'):
                    for image_path in note['image_paths']:
                        if image_path.strip():
                            render_image(image_path)
    except Exception as e:
        logger.error(f"Error rendering note card: {str(e)}")
        st.error("Error displaying note")

def sort_notes(notes: List[Dict], sort_order: str) -> List[Dict]:
    """Sort notes by timestamp"""
    try:
        def get_sort_key(note):
            timestamp = note.get('timestamp', '')
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                try:
                    if str(timestamp).isdigit():
                        return datetime.fromtimestamp(int(timestamp))
                except:
                    pass
                return datetime.min
        
        return sorted(
            notes,
            key=get_sort_key,
            reverse=(sort_order == "Newest First")
        )
    except Exception as e:
        logger.error(f"Error sorting notes: {str(e)}")
        return notes
def render_search_result(note: Dict):
    """Render a search result with different styles for exact and semantic matches"""
    try:
        match_type = note.get('match_type', 'exact')
        
        # Different styling for exact vs semantic matches
        if match_type == 'exact':
            border_color = "#28a745"  # Green for exact matches
            match_label = "Exact Match"
        else:
            border_color = "#17a2b8"  # Blue for semantic matches
            match_label = "Semantic Match"
        
        st.markdown(f"""
            <style>
            .search-result-{match_type} {{
                border-left: 4px solid {border_color};
                padding: 1rem;
                margin: 1rem 0;
                background-color: #f8f9fa;
                border-radius: 4px;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="search-result-{match_type}">
                <div style="margin-bottom: 0.5rem;">
                    <strong>{match_label}</strong><br>
                    <strong>Your Question:</strong> {note.get('query', 'No query available')}
                    {f'<br><strong>Original Note Query:</strong> {note.get("original_query", "")}' if match_type == 'semantic' else ''}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Show search results in expanded state by default
        with st.expander("View Content", expanded=True):
            if note.get('content'):
                st.markdown(note['content'])
            else:
                st.info("No text content available")
            
            if note.get('image_paths'):
                st.markdown("### Supporting Images")
                for image_path in note['image_paths']:
                    if image_path.strip():
                        render_image(image_path)
        
        st.markdown("---")
                
    except Exception as e:
        logger.error(f"Error rendering search result: {str(e)}")
        st.error("Error displaying search result")

def show():
    """Main function to display the research notes page"""
    try:
        st.title("Research Notes")
        
        # Initialize page state
        init_page_state()
        
        # Create three columns for document selection and sort order
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # Document selector
            folders = fetch_folders()
            if folders:
                options = ["Select a document"] + [folder['title'] for folder in folders]
                selected_folder = st.selectbox(
                    "Select a document",
                    options=options,
                    index=0,
                    key="notes_folder_selector"
                )
                
                if selected_folder != "Select a document":
                    st.session_state.selected_document = selected_folder
                else:
                    st.session_state.selected_document = None
                    st.session_state.selected_note = None
            else:
                st.warning("No documents available")
                return
        
        # Only show content if a document is selected
        if st.session_state.selected_document:
            # Fetch notes for the selected document
            notes = fetch_document_notes(st.session_state.selected_document)
            
            if notes:
                with col2:
                    # Note selector dropdown
                    note_options = ["Select a note", "ALL"] + [
                        f"Note {note.get('note_id', idx)}"
                        for idx, note in enumerate(notes, 1)
                    ]
                    selected_note = st.selectbox(
                        "Select research note",
                        options=note_options,
                        key="note_selector"
                    )
                    if selected_note != "Select a note":
                        st.session_state.selected_note = selected_note
                    else:
                        st.session_state.selected_note = None
                
                with col3:
                    # Sort order selector
                    sort_order = st.selectbox(
                        "Sort by",
                        ["Newest First", "Oldest First"],
                        key="notes_sort_order"
                    )
            
            # Display selected notes section first
            if st.session_state.selected_note:
                st.markdown("### Selected Research Notes")
                sorted_notes = sort_notes(notes, sort_order)
                
                if st.session_state.selected_note == "ALL":
                    for note in sorted_notes:
                        render_note_card(note)
                else:
                    note_id = st.session_state.selected_note.split("Note ")[-1]
                    selected_note_data = next(
                        (note for note in sorted_notes if str(note.get('note_id')) == note_id),
                        None
                    )
                    if selected_note_data:
                        render_note_card(selected_note_data)
                        
                        # Add save button for individual notes
                        if st.button("Save as Note", key=f"save_note_{note_id}", use_container_width=True):
                            # Prepare report data structure similar to page3
                            report_data = {
                                "report": {
                                    "blocks": [{"text": selected_note_data.get('content', '')}]
                                },
                                "metadata": {
                                    "query": selected_note_data.get('query', ''),
                                    "folder_name": st.session_state.selected_document,
                                    "processing_timestamp": datetime.now().isoformat()
                                }
                            }
                            
                            # Add images if present
                            if selected_note_data.get('image_paths'):
                                for image_path in selected_note_data['image_paths']:
                                    report_data["report"]["blocks"].append({"file_path": image_path})
                            
                            if save_as_notes(report_data):
                                st.success("Research note saved successfully!")
                                st.rerun()
            
            # Search section - fixed position
            st.markdown("### Search Notes")
            search_col1, search_col2 = st.columns([4, 1])
            
            with search_col1:
                question = st.text_input(
                    "Search by question:",
                    key="question",
                    placeholder="Enter your question to find matching research notes..."
                )
            
            with search_col2:
                st.markdown("<br>", unsafe_allow_html=True)
                search_clicked = st.button("Search", type="primary", use_container_width=True)
            
            # Container for search results
            search_results_container = st.container()
            
            # Handle search
            if search_clicked and question.strip():
                with search_results_container:
                    with st.spinner("Searching for relevant information..."):
                        try:
                            response = requests.post(
                                f"{FASTAPI_URL}/pdfs/{st.session_state.selected_document}/search-notes",
                                json={
                                    "query": question,
                                    "top_k": 5,
                                    "pdf_id": st.session_state.selected_document
                                }
                            )
                            
                            if response.status_code == 200:
                                results = response.json()
                                matches = results.get("matches", [])
                                match_type = results.get("match_type", "none")
                                
                                if matches:
                                    st.markdown("### Search Results")
                                    for match in matches:
                                        render_search_result(match)
                                else:
                                    st.info("No relevant information found in the research notes.")
                            else:
                                st.error(f"Failed to search notes. Status code: {response.status_code}")
                                
                        except Exception as e:
                            logger.error(f"Search error: {str(e)}")
                            st.error("An error occurred while processing your search.")
            
            if not notes:
                st.info(f"No research notes found for {st.session_state.selected_document}")
                
    except Exception as e:
        logger.error(f"Error in research notes page: {str(e)}")
        st.error("An error occurred while loading the page")
        if os.getenv("DEBUG"):
            st.error(f"Debug info: {str(e)}")

if __name__ == "__main__":
    show()