import streamlit as st

def navigate_back():
    st.session_state.chat_with_pdf = False
    st.rerun()