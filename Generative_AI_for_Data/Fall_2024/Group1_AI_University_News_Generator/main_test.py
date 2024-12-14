import streamlit as st
from PIL import Image  # For logo and other static images
from dotenv import load_dotenv
import os
import sys
import requests
import json
import time
import openai
# Add the plugins path for custom imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'airflow/plugins'))
from news_fetcher import fetch_news  # Import the fetch_news function from your news_fetcher script

# Load environment variables
load_dotenv()

# Access environment variables
api_key = os.getenv("NEWSAPI_KEY")
airflow_base_url = os.getenv("AIRFLOW_BASE_URL", "http://localhost:8080/api/v1")
airflow_username = os.getenv("AIRFLOW_USERNAME", "airflow")
airflow_password = os.getenv("AIRFLOW_PASSWORD", "airflow")

# Check if API key is loaded
if not api_key:
    st.error("API key for NewsAPI is missing. Please check your .env file.")

# Global configuration
st.set_page_config(page_title="AI University News Generator", layout="wide")

# Sidebar Navigation
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "News Generator","Q&A Bot", "About"])
    return page

# Home Page

def home_page():
    # Page Styles
    st.markdown(
        """
        <style>
        body {
            background-color: #f4f4f4;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            font-size: 80px;
            color: #2c3e50;
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
            animation: bounceIn 2s ease-in-out;
            transition: transform 0.3s ease, font-size 0.3s ease;
        }
        .main-title:hover {
            transform: scale(1.1);
            font-size: 90px;
            animation: none;
        }
        .subtitle {
            font-size: 24px;
            color: #1abc9c;
            text-align: center;
            margin-bottom: 30px;
            animation: fadeIn 2s;
        }
        .description {
            text-align: center;
            color: #7f8c8d;
            font-size: 20px;
            margin-bottom: 40px;
            animation: fadeIn 2.5s;
        }
        .buttons-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #95a5a6;
            margin-top: 30px;
        }
        .contact-box {
            border: 1px solid #dcdcdc;
            border-radius: 10px;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: slideUp 1.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        @keyframes bounceIn {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-30px);
            }
            60% {
                transform: translateY(-15px);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main Title with Animation
    st.markdown("<h1 class='main-title'>AI University News Hub</h1>", unsafe_allow_html=True)

    # Subtitle
    st.markdown(
        "<h3 class='subtitle'>Your personalized gateway to campus news, safety, and opportunities!</h3>",
        unsafe_allow_html=True,
    )

    # Description
    st.markdown(
        "<p class='description'>Stay informed with curated updates tailored to your interests. Empower your academic journey with real-time insights and opportunities.</p>",
        unsafe_allow_html=True,
    )

    # Divider
    st.markdown("---")

    # Interactive Buttons
    st.markdown(
        """
        <div class='buttons-container'>
            <button style='font-size: 18px; padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;'>📚 Academic News</button>
            <button style='font-size: 18px; padding: 10px 20px; background-color: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;'>🚨 Safety Alerts</button>
            <button style='font-size: 18px; padding: 10px 20px; background-color: #1abc9c; color: white; border: none; border-radius: 5px; cursor: pointer;'>🎓 Career Opportunities</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown(
            "<div class='contact-box'>", unsafe_allow_html=True
        )
        st.markdown("### About This App")
        st.write(
            """
            Welcome to the AI University News Hub! Our mission is to keep you informed and prepared 
            with the latest news, safety updates, and career opportunities for university communities.
            """
        )
        st.markdown("### Contact Us")
        st.write("For inquiries, email us at [contact@aiuniversity.com](mailto:contact@aiuniversity.com)")
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div class='footer'>
        <p>Built with ❤️ by the AI University Team | © 2024</p>
        </div>
        """,
        unsafe_allow_html=True,
    )





# Check Airflow Connectivity
def check_airflow_connection():
    try:
        response = requests.get(f"{airflow_base_url}/dags", auth=(airflow_username, airflow_password))
        response.raise_for_status()
        st.success("Connected to Airflow API!")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to Airflow API: {e}")
        return False

# Trigger Airflow DAG
def trigger_airflow_dag(dag_id, query, country):
    url = f"{airflow_base_url}/dags/{dag_id}/dagRuns"
    payload = {"conf": {"query": query, "country": country}}
    try:
        response = requests.post(url, auth=(airflow_username, airflow_password), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Check DAG Run Status
def check_dag_run_status(dag_id, dag_run_id):
    url = f"{airflow_base_url}/dags/{dag_id}/dagRuns/{dag_run_id}"
    try:
        response = requests.get(url, auth=(airflow_username, airflow_password))
        response.raise_for_status()
        return response.json().get("state")
    except Exception as e:
        st.error(f"Error checking DAG run status: {e}")
        return None

# Display Results
def display_results():
    st.title("News Results")

    # Allow users to select the type of news they want to review
    news_type = st.selectbox(
        "Select the type of news to display", 
        ["Academic News", "Safety News", "Career Articles"]
    )

    st.write(f"Showing previously fetched {news_type.lower()}...")

    # Example placeholder for fetched articles
    articles = [
        {"title": "Scholarship Opportunities", "source": "University Times", "description": "Find the best scholarships available this year.", "url": "#"},
        {"title": "Campus Safety Tips", "source": "Campus Security", "description": "How to stay safe on campus.", "url": "#"},
        {"title": "Top Career Fairs", "source": "Career Center", "description": "Upcoming career fairs you shouldn't miss.", "url": "#"},
    ]

    # Filter articles by selected news type
    filtered_articles = [a for a in articles if news_type.lower() in a["description"].lower()]

    # Display articles
    for idx, article in enumerate(filtered_articles, start=1):
        st.markdown(f"### {idx}. [{article['title']}]({article['url']})")
        st.write(f"**Source**: {article['source']}")
        st.write(article['description'])
        st.write("---")


# News Generator Page
def news_generator():
    st.title("Personalized News Generator")

    # Allow users to select the type of news they want
    news_type = st.selectbox(
        "Select the type of news you want to generate", 
        ["Academic News", "Safety News", "Career Articles"]
    )

    # Input for search query and country selection
    query = st.text_input("Search News", placeholder=f"Type a keyword for {news_type.lower()} (e.g., Scholarships)")
    country = st.selectbox("Country", ["us", "in", "gb", "ca", "au"], index=0)

    if st.button("Generate News"):
        with st.spinner("Fetching news..."):
            if query:
                # Simulate news fetching logic based on the selected type
                st.success(f"Here are the latest {news_type.lower()}!")
                # Add a placeholder for displaying news articles
                st.write(f"Displaying results for '{query}' in {news_type.lower()} for {country.upper()}...")
            else:
                st.warning("Please enter a query before generating news.")


def conversational_qna_bot():
    st.title("Conversational Chatbot (Q&A Style)")

    news_output_path = "airflow/logs/news_output.json"

    # Load articles
    if os.path.exists(news_output_path):
        with open(news_output_path) as f:
            saved_articles = json.load(f)
        
        # Let the user select an article
        titles = [article["title"] for article in saved_articles]
        selected_article = st.selectbox("Select an Article", titles)

        # Fetch the context for the selected article
        article_context = next(
            (article["description"] for article in saved_articles if article["title"] == selected_article),
            None
        )

        # Initialize session state for article and chat history
        if "selected_article" not in st.session_state:
            st.session_state.selected_article = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        

        # Reset chat history if a new article is selected
        if st.session_state.selected_article != selected_article:
            st.session_state.selected_article = selected_article
            st.session_state.chat_history = [
                {"role": "system", "content": f"You're an assistant answering questions about this article: {article_context}"}
            ]

        # Display context and chat history
        if article_context:
            st.markdown(f"**Context for Selected Article:** {selected_article}")
            st.write(article_context)

            st.markdown("### Chat History")
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                elif message["role"] == "assistant":
                    st.markdown(f"**Bot:** {message['content']}")

            # User Input
            user_input = st.text_input("Your message", key="user_input")
            

            

            if st.button("Send"):
                if user_input:
                    with st.spinner("Thinking..."):
                        # Add user message to history
                        st.session_state.chat_history.append({"role": "user", "content": user_input})

                        # Call OpenAI API
                        try:
                            openai.api_key = os.getenv("OPENAI_API_KEY")
                            response = openai.ChatCompletion.create(
                                model="gpt-4",
                                messages=st.session_state.chat_history,
                            )
                            bot_message = response['choices'][0]['message']['content'].strip()

                            # Add bot response to history
                            st.session_state.chat_history.append({"role": "assistant", "content": bot_message})
                        except Exception as e:
                            bot_message = f"Error generating response: {e}"
                            st.session_state.chat_history.append({"role": "assistant", "content": bot_message})
                    
                    
                else:
                    st.warning("Please enter a message.")
        else:
            st.error("Could not fetch the context for the selected article.")
    else:
        st.error(f"News output file not found at {news_output_path}.")





# About Page
def about_page():
    st.title("About This Project")
    st.write("""
    The AI University News Generator provides personalized updates about campus life using cutting-edge AI and NLP.
    """)

# Main Application
def main():
    page = sidebar()

    if page == "Home":
        home_page()
    elif page == "News Generator":
        news_generator()
    elif page == "Q&A Bot":
        conversational_qna_bot()
    elif page == "About":
        about_page()

if __name__ == "__main__":
    main()