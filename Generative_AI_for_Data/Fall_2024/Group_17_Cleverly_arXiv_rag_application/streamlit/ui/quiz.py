import streamlit as st
import requests
import os
from dotenv import load_dotenv
 
# Load environment variables
load_dotenv()
 
DEPLOY_URL = os.getenv("DEPLOY_URL", "http://127.0.0.1:8000")
 
def main():
    st.title("Quiz Page")
 
    # Ensure necessary session state variables
    if "selected_module_id" not in st.session_state:
        st.error("No module selected. Please go back to the lesson page.")
        return
 
    # Initialize session state variables if not already initialized
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
 
    selected_module_id = st.session_state["selected_module_id"]
 
    # Fetch or generate the quiz
    try:
        if not st.session_state.quiz_generated:
            with st.spinner("Generating quiz..."):
                quiz_response = requests.get(f"{DEPLOY_URL}/generate_quiz/{selected_module_id}")
            
            if quiz_response.status_code == 200:
                quiz_data = quiz_response.json()
                st.session_state.quiz_questions = quiz_data.get("quiz", [])
                st.session_state.quiz_generated = True
            else:
                st.error("Failed to generate quiz.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
 
    # Display the quiz
    if st.session_state.quiz_questions:
        st.subheader("Quiz")
        for i, question_item in enumerate(st.session_state.quiz_questions):
            question = question_item.get("question", "No question provided.")
            options = question_item.get("options", [])
            st.markdown(f"### Q{i + 1}: {question}")
            selected_option = st.radio(
                label=f"Options for Q{i + 1}",
                options=options,
                key=f"quiz_q{i}"
            )
            # Store user's selected option
            if len(st.session_state.user_answers) <= i:
                st.session_state.user_answers.append({
                    "question": question,
                    "selected_option": selected_option
                })
            else:
                st.session_state.user_answers[i]["selected_option"] = selected_option
 
    # Submit button to validate answers
    if st.button("Submit Quiz"):
        st.subheader("Quiz Results")
        correct_answers_count = 0
 
        # Validate answers
        for i, user_answer in enumerate(st.session_state.user_answers):
            correct_answer = st.session_state.quiz_questions[i].get("correct_answer", "")
            selected_option = user_answer["selected_option"]
 
            if selected_option == correct_answer:
                correct_answers_count += 1
                st.markdown(f"✅ **Q{i + 1}: Correct!**")
            else:
                st.markdown(f"❌ **Q{i + 1}: Incorrect!**")
                st.markdown(f"**Correct Answer:** {correct_answer}")
 
        total_questions = len(st.session_state.quiz_questions)
        st.markdown(f"### You got {correct_answers_count} out of {total_questions} questions correct.")
        st.markdown(f"### Your Score: {correct_answers_count / total_questions * 100:.2f}%")
 
 