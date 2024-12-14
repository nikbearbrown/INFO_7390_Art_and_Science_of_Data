import os
import streamlit as st
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from ui import planner, lesson, quiz, plans

# Set page configuration
st.set_page_config(layout="wide")

# Load environment variables
load_dotenv()

# FastAPI URL from environment variables
DEPLOY_URL = os.getenv("DEPLOY_URL", "http://127.0.0.1:8000")

def user_signup(username, password):
    """
    Function to register a new user, sending a post request to the FastAPI backend
    """
    response = requests.post(f"{DEPLOY_URL}/signup", params={"username": username, "password": password})
    return response.json()

def user_login(username, password):
    """
    Function to login an existing user, verifying the user credentials through FastAPI
    """
    response = requests.post(f"{DEPLOY_URL}/login", params={"username": username, "password": password})
    return response.json()

def signup():
    st.subheader("Signup Page")

    username = st.text_input("Create a valid username")
    password = st.text_input("Create a valid password", type="password")
    confirm_password = st.text_input("Confirm your password", type="password")

    if st.button("Signup"):
        if password == confirm_password:
            result = user_signup(username, password)
            if result.get("message"):
                st.success(result["message"])
            else:
                st.error(result.get("detail", "Signup failed"))
        else:
            st.error("Passwords do not match. Please retry.")

def login():
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = user_login(username, password)
        if "access_token" in result:
            st.session_state["access_token"] = result["access_token"]
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.session_state["page"] = "plans"
            st.rerun()
        else:
            st.error(result.get("detail", "Login failed"))

def user_logout():
    """Logs out the user and resets session state."""
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

def sidebar_navigation():
    """Sidebar for navigation between pages when logged in."""
    with st.sidebar:
        st.write(f"Logged in as: {st.session_state.get('username', 'User')}")
        st.button("Planner", on_click=lambda: change_page("planner"))
        st.button("Lessons", on_click=lambda: change_page("lesson"))
        st.button("Saved Plans", on_click=lambda: change_page("plans"))
        st.button("Quiz", on_click=lambda: change_page("quiz"))
        user_logout()

def change_page(page_name):
    """Changes the current page and triggers a rerun."""
    st.session_state["page"] = page_name
    st.rerun()

def main():
    """Main entry point for the Streamlit app."""
    st.title("Personalized AI Learning Assistant")

    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    # Page navigation logic
    if st.session_state["logged_in"]:
        sidebar_navigation()

        if st.session_state["page"] == "planner":
            planner.main()
        elif st.session_state["page"] == "lesson":
            lesson.main()
        elif st.session_state["page"] == "plans":
            plans.main()
        elif st.session_state["page"] == "quiz":
            quiz.main()
        else:
            st.error("404 - Page Not Found")
    else:
        choice = st.radio("Choose an option:", ("Login", "Signup"))
        if choice == "Signup":
            signup()
        else:
            login()

if __name__ == "__main__":
    main()
