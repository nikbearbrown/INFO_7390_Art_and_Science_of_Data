import streamlit as st
import Streamlit.informationpage as informationpage
import Streamlit.paddockpal1 as paddockpal1
import Streamlit.tracks_drivers as tracks_drivers  # Import the new page
import os

# Define available pages
PAGES = {
    "informationpage": {
        "module": "informationpage",
        "title": "Welcome to Paddock Pal",
        "icon": "🏠",
    },
    "paddockpal1": {
        "module": "paddockpal1",
        "title": "Paddock Pal Bot",
        "icon": "🤖",
    },
    "tracks_drivers": {
        "module": "tracks_drivers",
        "title": "Drivers and Tracks",
        "icon": "🏎️",
    },
}

# Add custom CSS for Ferrari red navigation and white buttons with black text
def add_custom_styles():
    st.markdown(
        """
        <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #FF2800; /* Ferrari red */
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] .css-1xarl3l {
            color: white !important; /* Make text white */
        }

        /* Sidebar title styling */
        [data-testid="stSidebar"] .css-1aumxhk {
            color: white !important; /* Sidebar title in white */
        }

        /* Sidebar button styles */
        .stButton button {
            background-color: white !important; /* White buttons */
            color: black !important; /* Black text inside buttons */
            border: 1px solid #FF2800; /* Ferrari red border */
            border-radius: 5px;
        }

        .stButton button:hover {
            background-color: #FF2800 !important; /* Ferrari red on hover */
            color: white !important; /* White text on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def run():
    # Apply custom styles
    add_custom_styles()

    # Add the application logo at the top of the navigation bar
    logo_path = "Images/logo.png"  # Update path if necessary
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    else:
        st.sidebar.warning("Logo not found. Please ensure the logo file is in the 'Images' folder.")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    for page_key, page_data in PAGES.items():
        if st.sidebar.button(f"{page_data['icon']} {page_data['title']}"):
            st.session_state['current_page'] = page_key

    # Initialize session state to track the current page
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'informationpage'

    # Load the selected page
    current_page = st.session_state['current_page']
    st.title(PAGES[current_page]["title"])

    # Render the selected page
    if current_page == "informationpage":
        informationpage.show_info()
    elif current_page == "paddockpal1":
        paddockpal1.show_paddockpal()
    elif current_page == "tracks_drivers":
        tracks_drivers.show_drivers_tracks()

if __name__ == "__main__":
    run()
