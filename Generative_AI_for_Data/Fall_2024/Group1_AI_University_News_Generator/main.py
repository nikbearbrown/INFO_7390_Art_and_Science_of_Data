import streamlit as st
from PIL import Image  # For logo and other static images
from dotenv import load_dotenv
import os
import sys
import requests
import json
import time
import openai
from streamlit_option_menu import option_menu
# Add the plugins path for custom imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'airflow/plugins'))
from news_fetcher import fetch_news  # Import the fetch_news function from your news_fetcher script
import streamlit.web.bootstrap as bootstrap
from streamlit.web import cli as stcli


# Load environment variables
load_dotenv()

# Access environment variables
api_key = os.getenv("NEWSAPI_KEY")
airflow_base_url = os.getenv("AIRFLOW_BASE_URL", "http://airflow-webserver:8090/api/v1")
airflow_username = os.getenv("AIRFLOW_USERNAME", "airflow")
airflow_password = os.getenv("AIRFLOW_PASSWORD", "airflow")

# Check if API key is loaded
if not api_key:
    st.error("API key for NewsAPI is missing. Please check your .env file.")

# Global configuration
st.set_page_config(page_title="AI University News Generator", layout="wide")

# Sidebar Navigation
import streamlit as st
from streamlit_option_menu import option_menu

def sidebar():
    # Add custom styles for sidebar
    st.markdown(
        """
        <style>
        /* General sidebar container */
        .css-1lcbmhc.e1fqkh3o3 {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }

        /* Menu item customization */
        .nav-link {
            font-size: 18px !important;
            font-weight: bold;
            color: #444 !important;
        }

        /* Hover effect for navigation items */
        .nav-link:hover {
            background-color: #d9edf7 !important;
            color: #0c5460 !important;
            border-radius: 5px;
        }

        /* Selected navigation item */
        .nav-link-selected {
            background-color: #02ab21 !important;
            color: white !important;
            font-weight: bold;
        }

        /* Sidebar title styling */
        .css-fg4pbf {
            font-size: 20px !important;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        selected_page = option_menu(
            menu_title="Navigation",  # Required
            options=["Home", "News Generator", "Q&A Bot", "About"],  # Menu options
            icons=["house", "newspaper", "robot", "info-circle"],  # Corresponding icons from Bootstrap
            menu_icon="cast",  # Menu icon
            default_index=0,  # Default selected index
        )

    return selected_page


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
        
       
        st.markdown("### Contact Us")
        st.write("For inquiries, email us at [inamdar.chaitanya6398@gmail.com](mailto:inamdar.chaitanya6398@gmail.com)")
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
        #st.success("Connected to Airflow API!")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to Airflow API: {e}")
        return False

def trigger_airflow_dag(dag_id, category, university):
    """
    Trigger the Airflow DAG with dynamic inputs for category and university.
    """
    url = f"{airflow_base_url}/dags/{dag_id}/dagRuns"
    payload = {"conf": {"category": category, "university": university}}
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

def display_results(news_type, university):
    st.subheader(f"Displaying Results for {news_type} at {university}")
    gpt_response_path = "airflow/logs/gpt_response.json"
    
    try:
        # Check for GPT response if required
        if os.path.exists(gpt_response_path):
            with open(gpt_response_path) as f:
                gpt_data = json.load(f)
                st.write(gpt_data.get("response", "No response found."))
        else:
            st.error(f"GPT response file not found at {gpt_response_path}.")
    except Exception as e:
        st.error(f"Error reading GPT response: {e}")

    # Load saved articles
    news_output_path = "airflow/logs/news_output.json"
    try:
        if os.path.exists(news_output_path):
            with open(news_output_path) as f:
                saved_articles = json.load(f)
                
                # Filter articles by selected category and university
                matching_articles = [
                    article for article in saved_articles
                    if news_type.lower() in article.get("category", "").lower()
                    and university.lower() == article.get("source", "").lower()
                ]
                
                # Display articles
                if matching_articles:
                    for idx, article in enumerate(matching_articles, start=1):
                        st.markdown(f"### {idx}. [{article['title']}]({article['url']})")
                        st.write(f"**Source**: {article['source']}")
                        st.write(article.get('description', 'No description available.'))
                        st.write("---")
                #else:
                #    st.info(f"No {news_type.lower()} found for {university}.")
        else:
            st.error(f"News output file not found at {news_output_path}.")
    except Exception as e:
        st.error(f"Error reading news output: {e}")




def news_generator():

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
            font-size: 50px;
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
    st.markdown("<h1 class='main-title'>Personalized News Generator</h1>", unsafe_allow_html=True)

    if not check_airflow_connection():
        return

    # Select the type of news
    news_type = st.selectbox(
        "Select the type of news to generate",
        ["Academic News", "Safety News", "Career Articles"]
    )

    # Select the university
    university = st.selectbox(
        "Select University",
        [
            "Northeastern University",
            "Arizona State University",
            "UCLA",
            "University of Illinois Urbana-Champaign",
            "University of Michigan",
            "University of Texas at Austin"
        ]
    )

    if st.button("Generate News"):
        with st.spinner("Please wait while we fetch the news!"):
            # Trigger the Airflow DAG with dynamic inputs
            response = trigger_airflow_dag(
                dag_id="news_fetcher_pipeline",
                category=news_type,
                university=university
            )
            if response:
                dag_run_id = response.get("dag_run_id")
                status = "queued"

                # Poll for status
                while status in ["queued", "running"]:
                    time.sleep(5)
                    status = check_dag_run_status("news_fetcher_pipeline", dag_run_id)

                if status == "success":
                    st.success(f"Latest {news_type.lower()} from {university}!")
                    display_results(news_type, university)
                else:
                    st.error(f"DAG execution failed or did not complete. Status: {status}")
            else:
                st.error("Failed to trigger Airflow DAG.")



def conversational_qna_bot():

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
            font-size: 50px;
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
    st.markdown("<h1 class='main-title'>AI Conversational Chatbot</h1>", unsafe_allow_html=True)    

    # Center the image using CSS styling
    st.write(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    #st.image("images/chatbot.png", caption="Conversational Chatbot", width=100)

    

 
    #st.image("images/chatbot.png", caption="Conversational Chatbot", use_column_width=True)
    #st.title("Conversational Chatbot (Q&A Style)")

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
     st.markdown("### About This App")
     st.write(
            """
            Welcome to the AI University News Hub! Our mission is to keep you informed and prepared 
            with the latest news, safety updates, and career opportunities for university communities.
            """
        )

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