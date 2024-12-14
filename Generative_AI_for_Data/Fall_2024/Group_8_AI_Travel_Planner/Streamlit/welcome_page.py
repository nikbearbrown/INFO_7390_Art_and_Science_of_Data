import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")


def welcome_page():
    # Render the welcome page content with st.markdown
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #4CAF50;">🤖 Welcome to WanderWise: Your Friendly AI Travel Planner</h1>
            <p style="font-size: 18px;">Plan smarter, chat better, and stay productive!</p>
            <p style="font-size: 16px;">
                AI Planner helps you with:<br>
                🗺️ Finding relevant searches for your travel plans<br>
                📋 Creating detailed itineraries tailored just for you<br>
                🎥 Suggesting YouTube videos to explore destinations<br>
                🌐 Providing website links for easy access to bookings<br>
                🖨️ Allowing you to take a printout of your itinerary for a hassle-free trip<br>
            </p>
            <p style="font-size: 16px; font-weight: bold;">
                Your one-stop solution to smarter, easier, and more personalized travel planning!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
