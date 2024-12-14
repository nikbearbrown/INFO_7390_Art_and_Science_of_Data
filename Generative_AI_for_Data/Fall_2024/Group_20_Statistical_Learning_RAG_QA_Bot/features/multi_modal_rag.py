import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

def multi_modal_rag():
    # Initialize session state variables
    if 'chat_with_pdf' not in st.session_state:
        st.session_state.chat_with_pdf = False
    if 'history' not in st.session_state:
        st.session_state.history = None
    if 'selected_document' not in st.session_state:
        st.session_state.selected_document = None

    st.title('MultiAgent System - Langgraph')

    # Simple dropdown with just one document option
    document_options = ["Select a document", "Intro to Statistical Learning"]
    selected_title = st.selectbox("**Select a Document**:", document_options)

    if selected_title != "Select a document":
        st.session_state.selected_document = selected_title
        
        # Display document information
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Placeholder for document image
            st.image("https://d2sofvawe08yqg.cloudfront.net/ISLR/s_hero2x?1620436274", width=150)
            
        with col2:
            st.subheader(selected_title)
            st.write("**Summary**: An Introduction to Statistical Learning provides a broad and less technical treatment of key topics in statistical learning. The book is intended for anyone who wishes to use cutting-edge statistical learning techniques to analyze their data.")

        if st.button("**Chat With PDF**"):
            st.session_state.chat_with_pdf = True
            st.session_state.history = []
            st.rerun()