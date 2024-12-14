import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Use a default value if FASTAPI_URL is not set
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

def login():
    st.title("🔑 Login")
    username = st.text_input("👤 Username", placeholder="Enter your username")
    password = st.text_input("🔒 Password", placeholder="Enter your password", type="password")

    if st.button("Login"):
        if username and password:
            # Make a request to the FastAPI login endpoint
            try:
                response = requests.post(f"{FASTAPI_URL}/login", params={"username": username, "password": password})

                if response.status_code == 200:
                    st.success("✅ Login successful! Redirecting to Chat...")
                    st.session_state.logged_in = True
                elif response.status_code == 401:
                    st.error("🚫 Invalid username or password. Please try again.")
                else:
                    st.error(f"⚠️ Error: {response.json().get('detail', 'Something went wrong.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Unable to connect to the server. Error: {e}")
        else:
            st.error("⚠️ Please enter both username and password.")
