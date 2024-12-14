import os
import sys
import streamlit as st
import requests
import snowflake.connector
from dotenv import load_dotenv
import base64

# Add the root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

# FastAPI endpoint URLs
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")
REGISTER_URL = f"{FASTAPI_URL}/auth/register"
LOGIN_URL = f"{FASTAPI_URL}/auth/login"

# Set up Streamlit page configuration
st.set_page_config(page_title="F1 Wikipedia", layout="centered")

def add_custom_styles(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    custom_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .stMarkdown {{
        background: transparent !important;
    }}
    .login-container {{
        max-width: 400px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }}
    .stTextInput > div > div > input {{
        background-color: white;
        color: #333;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 8px 12px;
    }}
    button[aria-label="Toggle password visibility"] {{
        display: none !important;
    }}
    .stSelectbox > div > div {{
        background: transparent !important;
    }}
    .stButton > button {{
        width: 100%;
        background-color: #333333;  
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }}
    .stButton > button:hover {{
        background-color: #1a1a1a;
    }}
    input[type="password"]::-ms-reveal,
    input[type="password"]::-ms-clear {{
        display: none;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Apply custom styles
add_custom_styles("Images/Paddockpal.png")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

def create_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None

def logout():
    st.session_state['logged_in'] = False
    st.session_state['access_token'] = None

def login_page():
    st.title("Login / Signup")
    option = st.selectbox("Select Login or Signup", ("Login", "Signup"))

    with st.container():
        if option == "Login":
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                login(username, password)

        elif option == "Signup":
            st.subheader("Signup")
            username = st.text_input("Username", key="signup_username")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            if st.button("Signup"):
                signup(username, email, password)

def signup(username, email, password):
    response = requests.post(REGISTER_URL, json={
        "username": username,
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        st.success("Account created successfully! Please login.")
    else:
        st.error(f"Signup failed: {response.json().get('detail', 'Unknown error occurred')}")

def login(username, password):
    response = requests.post(LOGIN_URL, json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token_data = response.json()
        st.session_state['access_token'] = token_data['access_token']
        st.session_state['logged_in'] = True
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error("Invalid username or password. Please try again.")

# Main Interface
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        import landing
        landing.run()