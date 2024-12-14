import streamlit as st
import requests
from fpdf import FPDF
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

# Function to make POST request to FastAPI
def call_fastapi_endpoint(endpoint, payload):
    url = f"{FASTAPI_URL}{endpoint}"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to call {endpoint}: {e}")
        return None

def create_pdf_with_unicode(content):
    """
    Generate a PDF with Unicode support using a TrueType font.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add a TrueType font for Unicode support
        font_path = "noto-sans-v27-latin-regular.ttf"  # Update with the correct font path
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file '{font_path}' not found. Please ensure it exists.")

        pdf.add_font("NotoSans", style="", fname=font_path, uni=True)
        pdf.set_font("NotoSans", size=16)
        pdf.cell(0, 10, "Your Travel Itinerary", ln=True, align="C")
        pdf.ln(10)  # Add a line break

        # Add the content
        pdf.set_font("NotoSans", size=12)
        paragraphs = content.split("\n\n")
        for paragraph in paragraphs:
            pdf.multi_cell(0, 10, paragraph)
            pdf.ln(5)  # Add spacing between paragraphs

        # Save the PDF to a file
        pdf_file = "travel_itinerary.pdf"
        pdf.output(pdf_file)
        return pdf_file
    except Exception as e:
        raise RuntimeError(f"Failed to create PDF: {e}")



# Main Streamlit App
def chat():
    st.title("🌍 Travel Itinerary & Vlogs")

    # Query input
    query = st.text_area("✍️ Enter your travel-related query:", placeholder="e.g., 'Plan a 5-day itinerary for Paris'")

    if st.button("Generate Full Travel Suggestions"):
        if query.strip():
            st.write(f"🤔 **Your Query:** {query}")
            
            # Step 1: Validate query and generate OpenAI response
            st.info("💡 **Generating your personalized travel itinerary...**")
            response_payload = {"query": query, "top_k": 5, "threshold": 0.75}
            itinerary_response = call_fastapi_endpoint("/generate-openai-response", response_payload)
            st.session_state.itinerary_response = itinerary_response["response"]


            if itinerary_response and "response" in itinerary_response:
                st.markdown(itinerary_response["response"])
            else:
                st.warning("⚠️ Could not generate a proper itinerary. Please try refining your query.")

            # Step 2: Fetch web search results
            st.info("🔍 **Fetching additional web suggestions...**")
            search_payload = {"query": f"Create a detailed travel itinerary: {query}", "max_results": 1}
            search_results = call_fastapi_endpoint("/search", search_payload)

            if search_results and "results" in search_results:
                st.markdown("### Here is more information if you would like to read more and explore more about the places:")
                for idx, item in enumerate(search_results["results"], start=1):
                    st.write(f"{item.get('title', 'No Title')}")
                    st.write(f"📍 Description: {item.get('content', 'No description available.')}")
                    st.write(f"🌐 **Learn More:** [Link]({item.get('url', '#')})")
                    st.markdown("---")
            else:
                st.warning("⚠️ No proper web suggestions found. Please try refining your query.")

            # Step 3: Fetch related YouTube videos
            st.info("🎥 **Fetching related YouTube videos...**")
            youtube_payload = {"query": f"Best travel vlogs for {query}", "max_results": 1}
            youtube_results = call_fastapi_endpoint("/youtube-search", youtube_payload)

            if youtube_results and "results" in youtube_results and len(youtube_results["results"]) > 0:
                st.markdown("### 🎥 watch thease youtube videos and see what places you find good:")
                for idx, video in enumerate(youtube_results["results"], start=1):
                    st.write(f"{video.get('title', 'No Title')}")
                    st.video(video.get("url", "#"))
                    st.markdown("---")
            else:
                st.warning("🔍 No related YouTube video found for your itinerary.")

            # Step 4: PDF Download Button
            if itinerary_response and "response" in itinerary_response:
                st.info("💾 **Download Your Itinerary as a PDF and save the itenary. Happy Travels!!!**")

                try:
                    # Generate the PDF file
                    pdf_file = create_pdf_with_unicode(itinerary_response["response"])

                    # Allow the user to download the generated PDF
                    with open(pdf_file, "rb") as file:
                        st.download_button(
                            label="📥 Download PDF",
                            data=file,
                            file_name="travel_itinerary.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"⚠️ Failed to generate the PDF. Error: {e}")

    # Add navigation button to Budget Planner
    if st.button("Go to Budget Planner"):
        if "itinerary_response" in st.session_state and st.session_state.itinerary_response:
            st.session_state.page = "Budget Planner"  # Set the target page
            st.rerun()  # Force re-run to apply navigation
        else:
            st.warning("⚠️ Please generate a travel itinerary first before accessing the Budget Planner.")

if __name__ == "__main__":
    chat()
