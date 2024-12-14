import streamlit as st
import requests
import fitz
from PIL import Image
import io
from dotenv import load_dotenv
import os
import math
from typing import List

# Load environment variables
load_dotenv()

# Configuration
FASTAPI_URL = os.getenv("FASTAPI_URL")
PDFS_PER_PAGE = 6
GRID_COLUMNS = 3

def handle_summary_click():
    # Store current PDF info in session state for page2.py
    if st.session_state.current_pdf:
        st.session_state.pdf_for_summary = st.session_state.current_pdf
        # Change the current page to Summary in session state
        st.session_state['current_page'] = "Summary"
        st.rerun()

def load_css():
    st.markdown("""
        <style>
            /* Container styles */
            .main-container {
                padding: 1rem;
                background-color: #ffffff;
            }
            
            /* Quick select styles */
            .quick-select {
                margin-bottom: 1rem;
                padding: 0.5rem;
                background-color: #f8f9fa;
                border-radius: 4px;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            
            /* Style for the selectbox container */
            .stSelectbox {
                max-width: 600px !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            
            /* Grid styles */
            .pdf-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                padding: 0.5rem;
            }
            
            /* PDF viewer container */
            .pdf-viewer-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* PDF page container */
            .pdf-page {
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            /* Navigation buttons container */
            .nav-buttons {
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin: 1rem 0;
            }
            
            /* Action buttons container */
            .action-buttons {
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin: 1rem 0;
                padding: 1rem;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if 'grid_page' not in st.session_state:
        st.session_state.grid_page = 1
    if 'current_pdf' not in st.session_state:
        st.session_state.current_pdf = None

def get_paginated_pdfs(pdfs: List[dict], page: int, per_page: int) -> List[dict]:
    start_idx = (int(page) - 1) * int(per_page)
    end_idx = start_idx + int(per_page)
    return pdfs[start_idx:end_idx]

def scroll_to_bottom():
    js = '''
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    '''
    st.markdown(js, unsafe_allow_html=True)

def display_pdf_viewer(pdf_title: str):
    try:
        with st.spinner("Loading PDF..."):
            response = requests.get(f"{FASTAPI_URL}/pdfs/{pdf_title}/document")
            
            if response.status_code == 200:
                doc = fitz.open(stream=response.content, filetype="pdf")
                total_pages = doc.page_count
                
                # Top navigation buttons
                with st.container():
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("← Back to Library", use_container_width=True):
                            st.session_state.current_pdf = None
                            st.rerun()
                    # with col2:
                    #     if st.button("Last Page", key="top_last", use_container_width=True):
                    #         st.session_state.scroll_to_bottom = True
                    #         st.rerun()
                    with col3:
                        if st.button("Generate Summary", key="top_summary", use_container_width=True):
                            handle_summary_click()
                
                # Display PDF title and total pages
                st.markdown(f"<h2 style='text-align: center;'>{pdf_title}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>Total Pages: {total_pages}</p>", unsafe_allow_html=True)
                
                # Container for all PDF pages
                with st.container():
                    # Render all pages
                    for page_num in range(total_pages):
                        page = doc[page_num]
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        # Display page number and content
                        st.markdown(f"<div class='pdf-page'>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center; color: #666;'>Page {page_num + 1}</p>", 
                                  unsafe_allow_html=True)
                        st.image(img, use_column_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                
                doc.close()
                
                # Bottom navigation buttons
                with st.container():
                    st.markdown("<div id='last-page'></div>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("← Back to Library", key="bottom_back", use_container_width=True):
                            st.session_state.current_pdf = None
                            st.rerun()
                    # with col2:
                    #     if st.button("Last Page", key="bottom_last", use_container_width=True):
                    #         st.session_state.scroll_to_bottom = True
                    #         st.rerun()
                    with col3:
                        if st.button("Generate Summary", key="bottom_summary", use_container_width=True):
                            handle_summary_click()

                
    except Exception as e:
        st.error("Error loading PDF. Please try again.")
        if st.button("← Back to Library"):
            st.session_state.current_pdf = None
            st.rerun()

# Rest of the code remains the same...
def display_grid_view(pdfs: List[dict]):
    total_pages = math.ceil(len(pdfs) / PDFS_PER_PAGE)
    current_pdfs = get_paginated_pdfs(pdfs, st.session_state.grid_page, PDFS_PER_PAGE)
    
    # Quick select dropdown with constrained width
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pdf_titles = [pdf['title'] for pdf in pdfs]
            selected_pdf = st.selectbox(
                "Quick Select PDF",
                [""] + pdf_titles,
                index=0,
                label_visibility="collapsed"
            )
            
            if selected_pdf:
                st.session_state.current_pdf = selected_pdf
                st.rerun()
    
    # Grid navigation
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("←", use_container_width=True,
                        disabled=st.session_state.grid_page <= 1):
                st.session_state.grid_page = int(st.session_state.grid_page) - 1
                st.rerun()
        
        with col2:
            st.markdown(f"<p style='text-align: center; margin: 0;'>{st.session_state.grid_page} / {total_pages}</p>",
                      unsafe_allow_html=True)
        
        with col3:
            if st.button("→", use_container_width=True,
                        disabled=int(st.session_state.grid_page) >= total_pages):
                st.session_state.grid_page = int(st.session_state.grid_page) + 1
                st.rerun()
    
    # Display grid
    cols = st.columns(GRID_COLUMNS)
    for idx, pdf in enumerate(current_pdfs):
        with cols[idx % GRID_COLUMNS]:
            with st.container():
                try:
                    # Cover image
                    cover_response = requests.get(f"{FASTAPI_URL}/pdfs/{pdf['title']}/cover")
                    if cover_response.status_code == 200:
                        cover_image = Image.open(io.BytesIO(cover_response.content))
                        st.image(cover_image, use_column_width=True)
                except Exception:
                    st.markdown("📚")
                
                # Title and button
                st.markdown(f"<p style='text-align: center; margin: 5px 0;'>{pdf['title']}</p>",
                          unsafe_allow_html=True)
                if st.button("View", key=f"btn_{pdf['title']}", use_container_width=True):
                    st.session_state.current_pdf = pdf['title']
                    st.rerun()

def show():
    """Main function to display the PDF viewer page"""
    # Initialize session state and load CSS
    init_session_state()
    load_css()
    
    try:
        # Fetch PDFs from API
        response = requests.get(f"{FASTAPI_URL}/pdfs/all")
        if response.status_code != 200:
            st.error("Unable to load PDF library")
            return
        
        pdfs = response.json()
        
        # Display appropriate view
        if st.session_state.current_pdf:
            display_pdf_viewer(st.session_state.current_pdf)
        else:
            display_grid_view(pdfs)
            
    except Exception as e:
        st.error("Unable to connect to server")

if __name__ == "__main__":
    show()