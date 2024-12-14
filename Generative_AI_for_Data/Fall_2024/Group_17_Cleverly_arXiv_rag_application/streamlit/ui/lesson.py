import streamlit as st
import requests
import os
from dotenv import load_dotenv
 
# Load environment variables
load_dotenv()
 
# Get the FastAPI URL from environment variables
DEPLOY_URL = os.getenv("DEPLOY_URL", "http://127.0.0.1:8000")

def main():
    st.title("Lesson Details")
 
    # Ensure username, access_token, and selected_module_id are available in session state
    if (
        "username" not in st.session_state
        or "access_token" not in st.session_state
        or "selected_module_id" not in st.session_state
    ):
        st.error("You are not logged in or no module was selected. Please go back and select a module.")
        return
 
    access_token = st.session_state["access_token"]
    selected_module_id = st.session_state["selected_module_id"]

    # Fetch details for the selected module from the backend
    try:
        response = requests.get(
            f"{DEPLOY_URL}/get_module_details/{selected_module_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code == 200:
            module_details = response.json()
            if isinstance(module_details, dict) and "message" in module_details:
                st.warning(module_details["message"])
                return
        else:
            st.error("Failed to fetch module details.")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
 
    # Display the module details
    st.markdown(f"## Module {module_details.get('module')}: {module_details.get('title')}")
    st.write(module_details.get("description", "No description available."))

    # Add a back button to navigate back to the plan page
    if st.button("Back to Plans"):
        del st.session_state["selected_module_id"]
        st.session_state["page"] = "plans"
        st.rerun()

    if st.button("Take Quiz"):
        st.session_state["page"] = "quiz"  # Switch to Quiz page
        st.rerun()
 
    # Display detailed explanation as an article
    detailed_explanation = module_details.get("detailed_explanation", "No detailed explanation available.")
    st.markdown("### Detailed Explanation")
    paragraphs = detailed_explanation.split("\n\n")  # Split into paragraphs by double line breaks
    for paragraph in paragraphs:
        st.markdown(paragraph.strip())  # Render each paragraph as Markdown with proper spacing
 
    # Fetch and display related images
    # try:
    #     st.markdown("### Related Images with Summaries")
    #     image_response = requests.get(
    #         f"{DEPLOY_URL}/get_image_urls_with_summaries/{selected_module_id}",
    #         headers={"Authorization": f"Bearer {access_token}"}
    #     )
    #     if image_response.status_code == 200:
    #         image_data = image_response.json()
    #         if "images" in image_data:
    #             images = image_data["images"]
    #             if images:
    #                 for item in images:
    #                     url = item.get("url")
    #                     summary = item.get("summary")
    #                     if url:
    #                         # Display the image with a caption for the summary
    #                         st.image(url, caption=summary or "No summary available", use_container_width=True)
    #                     else:
    #                         st.warning("Invalid image URL.")
    #             else:
    #                 st.info("No related images found for this module.")
    #         else:
    #             st.error("Unexpected response format for image data.")
    #     else:
    #         st.error(f"Failed to retrieve images for this module. Status Code: {image_response.status_code}")
    # except Exception as e:
    #     st.error(f"An error occurred while fetching images: {e}")
 
    # Fetch and display the most relevant YouTube video
    try:
        with st.spinner("Fetching the most relevant YouTube video..."):
            video_response = requests.get(
                f"{DEPLOY_URL}/get_relevant_youtube_video/{selected_module_id}"
            )
        if video_response.status_code == 200:
            video_data = video_response.json()
            if video_data["video_url"]:
                st.markdown("### Most Relevant YouTube Video")
                st.write(f"**Relevance Score:** {video_data['relevance_score']:.2f}")
                st.video(video_data["video_url"])
            else:
                st.warning("No relevant YouTube video found for this module.")
        else:
            st.error("Failed to fetch relevant YouTube video.")
    except Exception as e:
        st.error(f"An error occurred while fetching the YouTube video: {e}")

    try:
        with st.spinner("Fetching relevant Arxiv papers..."):
            # Make a request to your FastAPI endpoint
            arxiv_response = requests.get(
                f"{DEPLOY_URL}/get_relevant_arxiv_paper/{selected_module_id}"
            )

        if arxiv_response.status_code == 200:
            arxiv_data = arxiv_response.json()
            if arxiv_data:
                st.markdown("### Relevant Arxiv Papers")
                for paper in arxiv_data:
                    st.markdown(f"**Title:** {paper['title']}")
                    st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
                    st.markdown(f"**Published Date:** {paper['published']}")
                    st.markdown(f"**Summary:** {paper['summary']}")
                    st.markdown(f"[Read More]({paper['link']})")
                    if paper.get("pdf_url"):
                        st.markdown(f"[Download PDF]({paper['pdf_url']})")
                    st.markdown("---")
            else:
                st.warning("No relevant papers found for this module.")
        else:
            st.error("Failed to fetch relevant Arxiv papers.")

    except Exception as e:
        st.error(f"An error occurred while fetching Arxiv papers: {e}")
 

    if video_response.status_code == 200 and video_data.get("video_url"):
        try:
            with st.spinner("Generating flashcards..."):
                flashcards_response = requests.get(f"{DEPLOY_URL}/generate_flashcards/{selected_module_id}")
            if flashcards_response.status_code == 200:
                # Parse the JSON response
                flashcards_data = flashcards_response.json()  # Expecting a nested JSON structure
                flashcards = flashcards_data.get("flashcards", [])  # Extract the list of flashcards
                if flashcards:
                    st.subheader("Flashcards")
                    for i, flashcard in enumerate(flashcards):
                        question = flashcard.get("question", "Question not available.")
                        answer = flashcard.get("answer", "Answer not available.")
                        
                        # Use st.container for the box layout
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="
                                    border: 2px solid #ddd; 
                                    border-radius: 10px; 
                                    padding: 15px; 
                                    background-color: #f9f9f9; 
                                    color: #333; 
                                    font-family: Arial, sans-serif;
                                    margin-bottom: 10px;">
                                    <p><strong>Flashcard {i+1}</strong></p>
                                    <p><strong>Q:</strong> {question}</p>
                                    <p><strong>A:</strong> {answer}</p>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                else:
                    st.warning("No flashcards generated. Please try again.")
            else:
                st.error("Failed to generate flashcards. Please check the module ID or try again later.")
        except Exception as e:
            st.error(f"An error occurred while generating flashcards: {e}")

if __name__ == "__main__":
    main()
 