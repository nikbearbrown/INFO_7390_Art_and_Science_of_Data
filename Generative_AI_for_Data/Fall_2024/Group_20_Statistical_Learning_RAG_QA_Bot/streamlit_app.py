import streamlit as st
from features.multi_modal_rag import multi_modal_rag
from features.chat_with_pdf import chat_pdf
from navigation.back import navigate_back

if "chat_with_pdf" not in st.session_state:
    st.session_state.chat_with_pdf = False

# Set up the page configuration
rag_page = st.Page(multi_modal_rag, title="Agentic RAG with Langgraph", icon=":material/book:")
back_page = st.Page(navigate_back, title="Back", icon=":material/logout:")

chat_pdf_page = st.Page(chat_pdf, title="Chat With the PDF", icon=":material/chat:")


# Define Navigation
if st.session_state.chat_with_pdf:
    pg = st.navigation(
        {
            "Features": [chat_pdf_page],
            "Account": [back_page]
        }
    )
else:
    pg = st.navigation([rag_page])

# Set Configurations
st.set_page_config(page_title="My Application", page_icon=":material/lock:")

# Run the selected page
pg.run()


