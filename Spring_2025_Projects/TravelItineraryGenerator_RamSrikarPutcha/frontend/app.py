import streamlit as st
import requests
from datetime import date, timedelta
import io
import base64

BACKEND_URL = "http://localhost:8000"
st.set_page_config(page_title="Smart Travel Itinerary", layout="wide", page_icon="✈️")

# CSS for WhatsApp-style chat
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.user-msg, .bot-msg {
    padding: 10px 15px;
    border-radius: 12px;
    max-width: 70%;
    word-wrap: break-word;
}
.user-msg {
    background-color: #d1e7dd;
    align-self: flex-end;
    text-align: right;
}
.bot-msg {
    background-color: #f0f0f0;
    align-self: flex-start;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Reset button
if st.sidebar.button("🔄 Reset App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Helper for styled download button
def create_download_link(pdf_bytes, filename):
    try:
        b64 = base64.b64encode(pdf_bytes.read()).decode()
        href = f'''
        <a href="data:application/pdf;base64,{b64}" download="{filename}" 
           style="display: inline-block; padding: 12px 20px; 
                  background-color: #3b82f6; color: white; 
                  text-decoration: none; border-radius: 8px; 
                  font-weight: 600; text-align: center;">
            ⬇️ Download PDF Itinerary
        </a>
        '''
        return href
    except Exception:
        st.error("Error creating download link.")
        return ""

with st.sidebar:
    st.title("Plan Your Trip")
    with st.form("travel_form"):
        city = st.selectbox("Destination City", ["New York", "San Francisco", "Chicago", "Seattle", "Las Vegas", "Los Angeles"])
        today = date.today()
        start_date = st.date_input("Start Date", today + timedelta(days=1), min_value=today)
        end_date = st.date_input("End Date", today + timedelta(days=2), min_value=start_date)
        preference = st.selectbox("Package", [
            "Suggest an itinerary with Tours, Accommodation, Things to do",
            "Suggest an itinerary with Accommodation, Things to do",
            "Suggest an itinerary with Things to do"
        ])
        budget = st.select_slider("Budget", options=["low", "medium", "high"], value="medium")
        submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    st.session_state.clear()
    st.session_state.submitted = True
    st.session_state.city = city
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date
    st.session_state.preference = preference
    st.session_state.budget = budget
    st.session_state.loading = True
    st.session_state.chat_history = []
    st.rerun()

# ------------------ Generate Itinerary ------------------
if st.session_state.get("loading", False):
    st.info("⏳ Generating itinerary, please wait...")
    with st.spinner("Working on it..."):
        payload = {
            "city": st.session_state.city,
            "start_date": str(st.session_state.start_date),
            "end_date": str(st.session_state.end_date),
            "preference": st.session_state.preference,
            "travel_type": "Solo",
            "adults": 1,
            "kids": 0,
            "budget": st.session_state.budget,
            "include_tours": "Tours" in st.session_state.preference,
            "include_accommodation": "Accommodation" in st.session_state.preference,
            "include_things": "Things to do" in st.session_state.preference
        }

        try:
            res = requests.post(f"{BACKEND_URL}/generate-itinerary", json=payload, timeout=180)
            res.raise_for_status()
            data = res.json()
            st.session_state.itinerary_html = data["data"]["itinerary_html"]
            st.session_state.itinerary_text = data["data"]["itinerary_text"]
            st.session_state.generated_itinerary = data["data"]["itinerary_text"]

            pdf_response = requests.post(
                f"{BACKEND_URL}/generate-pdf",
                json={
                    "city": payload["city"],
                    "itinerary": st.session_state.itinerary_text,
                    "start_date": str(st.session_state.start_date)
                },

                timeout=60
            )
            pdf_response.raise_for_status()
            st.session_state.pdf_bytes = io.BytesIO(pdf_response.content)

            st.session_state.loading = False
            st.rerun()

        except Exception as e:
            st.session_state.loading = False
            st.error(f"❌ Failed to generate itinerary: {e}")
            st.stop()

# ------------------ Display Itinerary ------------------
if st.session_state.get("itinerary_html"):
    st.success("✅ Your personalized itinerary is ready!")

    tabs = st.tabs(["📋 Itinerary", "📄 PDF Download", "💬 Ask About Your Itinerary"])

    with tabs[0]:
        html_wrapper = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Itinerary</title></head>
        <body>{st.session_state.itinerary_html}</body>
        </html>
        """
        st.components.v1.html(html_wrapper, height=800, scrolling=True)

    with tabs[1]:
        if "pdf_bytes" in st.session_state:
            st.markdown(create_download_link(st.session_state.pdf_bytes, f"{st.session_state.city}_Itinerary.pdf"), unsafe_allow_html=True)
        else:
            st.warning("PDF not available.")

    with tabs[2]:
        st.markdown("<h3 style='margin-bottom: 0.5rem;'>💬 Ask About Your Itinerary</h3>", unsafe_allow_html=True)

        # Input field
        question_key = f"question_input_{len(st.session_state.get('chat_history', []))}"
        question = st.text_input(
            "❓ What would you like to know about your trip?",
            key=question_key,
            placeholder="E.g., Where's the best place for dinner?",
            label_visibility="collapsed"
        )

        if st.button("Ask Question"):
            if question.strip():
                with st.spinner("Finding answers for you..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/ask",
                            json={"itinerary": st.session_state.generated_itinerary, "question": question},
                            timeout=60
                        )
                        res.raise_for_status()
                        answer = res.json().get("answer")
                        st.session_state.chat_history.append((question, answer))
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("Please enter a question.")

        # Chat display with styling
        if st.session_state.get("chat_history"):
            st.markdown("""
            <style>
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
                margin-top: 20px;
            }
            .chat-row {
                display: flex;
                align-items: flex-end;
                gap: 10px;
            }
            .chat-user {
                background-color: #d1fae5;
                color: #0f5132;
                padding: 10px 14px;
                border-radius: 16px;
                max-width: 100%;
                margin-left: auto;
                margin-right: 0; 
                display: block;
                text-align: left; 
            }
            .chat-bot {
                background-color: #f0f0f0;
                color: #111827;
                padding: 10px 14px;
                border-radius: 16px;
                max-width: 100%;
                margin-right: auto;
            }
            .label {
                font-size: 13px;
                margin-bottom: 2px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for q, a in st.session_state.chat_history[::-1]:
                st.markdown(f"""
                <div class='chat-row'>
                    <div style='text-align: right;'>
                        <div class='label'>You</div>
                        <div class='chat-user'>{q}</div>
                    </div>
                </div><br>
                <div class='chat-row'>
                    <div>
                        <div class='label'>Response</div>
                        <div class='chat-bot'>{a}</div>
                    </div>
                </div><br>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)



# ------------------ Welcome ------------------
elif not st.session_state.get("submitted"):
    st.markdown("## 👋 Welcome to Smart Travel Itinerary")
    st.markdown("Use the sidebar to generate your personalized travel plan with tours, stays, and hidden gems.")