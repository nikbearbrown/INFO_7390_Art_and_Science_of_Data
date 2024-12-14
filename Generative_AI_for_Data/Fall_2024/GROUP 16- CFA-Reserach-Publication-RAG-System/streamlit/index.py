import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pathlib
import page1
import page2
import page3
import page4

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        /* Center the main content */
        .block-container {
            padding-top: 2rem;
            max-width: 700px;
        }
        
        /* Style the authentication container */
        .auth-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Style buttons */
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            height: 2.5rem;
            margin-top: 1rem;
        }
        
        /* Style sidebar */
        .css-1d391kg {
            padding-top: 2rem;
        }
        
        /* Style input fields */
        .stTextInput > div > div > input {
            border-radius: 5px;
        }
        
        /* Custom title styling */
        .custom-title {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #0E1117;
        }
        
        /* Center the login/register options */
        .auth-options {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        /* Style navigation buttons */
        .nav-button {
            background-color: transparent;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        /* Success message styling */
        .success-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #d4edda;
            color: #155724;
            text-align: center;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

def show_navigation():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation links
        selected_page = None
        
        if st.sidebar.button("Dashboard", key="nav_home", use_container_width=True):
            selected_page = "Home"
            
        if st.sidebar.button("PDF Selection", key="nav_page1", use_container_width=True):
            selected_page = "PDF Selection"
            
        if st.sidebar.button("Summary", key="nav_page2", use_container_width=True):
            selected_page = "Summary"
        
        if st.sidebar.button("Document Q&A System", key="nav_page3", use_container_width=True):
            selected_page = "Document Q&A System"
        
        if st.sidebar.button("Research Notes", key="nav_page4", use_container_width=True):
            selected_page = "Research Notes"

        # Add a separator before logout
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Logout button with different styling
        if st.sidebar.button("🚪  Logout", key="nav_logout", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if selected_page:
            st.session_state.current_page = selected_page
            st.rerun()
            
        return st.session_state.get('current_page', "Home")
    

env_path = pathlib.Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

FASTAPI_URL = os.getenv("FASTAPI_URL")  # Adjust based on where FastAPI is running

def display_registration_instructions():
    st.subheader("Registration Instructions")
    st.write("Please provide the following information to register:")
    st.write("- **Username**: Your desired username.")
    st.write("- **Email**: A valid email address.")
    st.write("- **Password**: A password that is at least 8 characters long and contains at least one uppercase letter and one lowercase letter.")
    st.write("- **Confirm Password**: Re-enter your password to confirm it.")
    st.write("After filling in all the fields, click the 'Submit Registration' button to complete the registration process.")

def register_user(username, email, password, confirm_password):
    url = f"{FASTAPI_URL}/register"
    data = {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        st.success("User registered successfully!")
    else:
        error_details = response.json().get('detail')
        if isinstance(error_details, list):
            error_message = '\n'.join([error['msg'] for error in error_details])
        else:
            error_message = error_details
        st.error(f"Registration failed: {error_message}")

def login_user(email, password):
    url = f"{FASTAPI_URL}/token"
    data = {
        "username": email,
        "password": password
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        st.error(response.json().get('detail'))
        return None

def get_current_user(token):
    url = f"{FASTAPI_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch current user details.")
        return None

def main():
    # if 'token' not in st.session_state:
    #     # Center the title
    #     st.markdown("<h1 class='custom-title'>Welcome to Document Q/A System</h1>", unsafe_allow_html=True)
        
    #     # Create centered container for auth options
    #     col1, col2, col3 = st.columns([1, 2, 1])
    #     with col2:
    #         # st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            
    #         # Login/Register toggle buttons
    #         col_login, col_register = st.columns(2)
    #         with col_login:
    #             if st.button("Login", use_container_width=True):
    #                 st.session_state.show_login = True
    #                 st.session_state.show_register = False
    #         with col_register:
    #             if st.button("Register", use_container_width=True):
    #                 st.session_state.show_register = True
    #                 st.session_state.show_login = False

    #         if 'show_login' not in st.session_state:
    #             st.session_state.show_login = True
    #         if 'show_register' not in st.session_state:
    #             st.session_state.show_register = False

    #         if st.session_state.show_login:
    #             st.markdown("<h3 style='text-align: center; margin-top: 1rem;'>Login</h3>", unsafe_allow_html=True)
    #             login_email = st.text_input("Email", key="login_email")
    #             login_password = st.text_input("Password", type="password", key="login_password")
    #             if st.button("Sign In", type="primary", use_container_width=True):
    #                 if login_email and login_password:
    #                     token = login_user(login_email, login_password)
    #                     if token:
    #                         st.session_state['token'] = token
    #                         st.markdown("<div class='success-message'>Login successful!</div>", unsafe_allow_html=True)
    #                         st.rerun()
    #                 else:
    #                     st.error("Please enter both email and password")

    #         if st.session_state.show_register:
    #             st.markdown("<h3 style='text-align: center; margin-top: 1rem;'>Create Account</h3>", unsafe_allow_html=True)
    #             register_username = st.text_input("Username", key="register_username")
    #             register_email = st.text_input("Email", key="register_email")
    #             register_password = st.text_input("Password", type="password", key="register_password")
    #             confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")
    #             if st.button("Sign Up", type="primary", use_container_width=True):
    #                 if register_username and register_email and register_password and confirm_password:
    #                     register_user(register_username, register_email, register_password, confirm_password)
    #                 else:
    #                     st.error("Please fill in all fields")
            
    #         st.markdown("</div>", unsafe_allow_html=True)

    # else:  # User is logged in
    #     user_info = get_current_user(st.session_state['token'])
    #     if user_info:
    selected_page = show_navigation()
            
    # Display user info in sidebar
    with st.sidebar:
        st.markdown("---")
        # st.markdown(f"<div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 5px;'>"
        #             f"<p>👤 <strong>{user_info['email']}</strong></p>"
        #             f"</div>", unsafe_allow_html=True)
    
    # Show selected page content
    if selected_page == "Home":
        st.markdown("<h1 style='text-align: center;'>Welcome to Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Select a page from the sidebar to get started.</p>", unsafe_allow_html=True)
    elif selected_page == "PDF Selection":
        page1.show()
    elif selected_page == "Summary":
        page2.show()
    elif selected_page == "Document Q&A System":
        page3.show()
    elif selected_page == "Research Notes":
        page4.show()

if __name__ == "__main__":
    main()