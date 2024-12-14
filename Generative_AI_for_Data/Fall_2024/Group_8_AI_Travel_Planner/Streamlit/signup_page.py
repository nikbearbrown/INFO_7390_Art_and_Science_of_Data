import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")


def sign_up():
    st.title("📝 Sign Up")
    username = st.text_input("👤 Username", placeholder="Enter a unique username")
    password = st.text_input("🔒 Password", placeholder="Choose a strong password", type="password")

    if st.button("Sign Up"):
        if username and password:
            try:
                # Make a request to the FastAPI signup endpoint
                response = requests.post(f"{FASTAPI_URL}/signup", params={"username": username, "password": password})

                if response.status_code == 200:
                    st.success("🎉 Sign-up successful! You can now log in.")
                elif response.status_code == 400:
                    st.error("🚨 Username already exists. Try another one.")
                else:
                    st.error(f"⚠️ Error: {response.json().get('detail', 'Something went wrong.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Unable to connect to the server. Error: {e}")
        else:
            st.error("⚠️ Please fill in both fields.")
