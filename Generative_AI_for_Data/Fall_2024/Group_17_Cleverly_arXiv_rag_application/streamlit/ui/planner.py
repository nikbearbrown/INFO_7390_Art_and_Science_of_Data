import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Get the FastAPI URL from environment variables
DEPLOY_URL = os.getenv("DEPLOY_URL", "http://127.0.0.1:8000")

def main():

    # List of session state keys to reset
    keys_to_reset = [
        "chat_history",
        "current_plan",
        "current_summary",
        "general_response",
        "save_status"
    ]

    if st.button("Start a new chat"):
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Session state has been reset.")

    st.title("Planner")

    # Ensure token and username are available in session state
    if "access_token" not in st.session_state or "username" not in st.session_state:
        st.error("You are not logged in. Please log in to create or view plans.")
        return

    access_token = st.session_state["access_token"]
    username = st.session_state["username"]

    # Initialize chat history, current plan, save status, and fallback response if not present
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "current_plan" not in st.session_state:
        st.session_state["current_plan"] = None
    if "current_summary" not in st.session_state:
        st.session_state["current_summary"] = "No summary provided yet."  # To retain the summary for the current plan
    if "general_response" not in st.session_state:
        st.session_state["general_response"] = "No general response yet."
    if "save_status" not in st.session_state:
        st.session_state["save_status"] = None  # Track save status for the plan

    # Chat input for user query
    user_query = st.chat_input("What do you want to learn today?")

    if user_query:
        # Add user query to chat history
        st.session_state["chat_history"].append({"role": "user", "content": user_query})

        # Make a request to the backend for processing
        try:
            response = requests.post(
                f"{DEPLOY_URL}/query",
                json={
                    "user_query": user_query,
                    "current_plan": st.session_state.get("current_plan"),
                    "current_summary": st.session_state.get("current_summary"),  # Pass current summary
                },
                headers={"Authorization": f"Bearer {st.session_state['access_token']}"},  # Include token
            )

            if response.status_code == 200:
                data = response.json()

                # Handle learning plan if it exists
                if data.get("plan"):
                    st.session_state["current_plan"] = data["plan"]
                    summary = data.get("summary", st.session_state["current_summary"])  # Retain the previous summary if not updated
                    st.session_state["current_summary"] = summary  # Update or retain the summary
                    st.session_state["chat_history"].append({"role": "assistant", "content": summary})

                    # Update general response for a generated plan
                    st.session_state["general_response"] = data.get(
                        "response", "I've generated a plan for you based on your query."
                    )

                    # Display plan metadata and details
                    if st.session_state["current_plan"]:
                        # Display the Plan Title
                        plan_title = st.session_state["current_plan"].get("Title", "Untitled Plan")
                        st.markdown(f"## {plan_title}")

                        with st.expander("Outcomes"):
                            expected_outcome = st.session_state["current_plan"].get("ExpectedOutcome", "N/A")
                            st.markdown(f"**Expected Outcome:** {expected_outcome}")

                            key_topics = st.session_state["current_plan"].get("KeyTopics", [])
                            if key_topics:
                                st.markdown("**Key Topics:**")
                                for topic in key_topics:
                                    st.write(f"- {topic}")

                        # Display Summary
                        st.markdown("### Summary")
                        st.text(summary)

                        # Display Module Tabs
                        modules = st.session_state["current_plan"].get("Modules", [])
                        if modules:
                            module_tabs = [f"Module {module['module']}" for module in modules]
                            tab_containers = st.tabs(module_tabs)

                            for i, tab in enumerate(tab_containers):
                                with tab:
                                    module = modules[i]
                                    st.markdown(f"#### {module['title']}")
                                    st.write(module['description'])

                # Handle fallback response if no plan is available
                elif data.get("response"):
                    st.session_state["general_response"] = data["response"]
                    st.session_state["chat_history"].append({"role": "assistant", "content": data["response"]})

                else:
                    # Handle the case where no response or plan is provided
                    st.session_state["general_response"] = "Failed to fetch the learning plan details."
                    st.error("Failed to fetch the learning plan details.")
            else:
                # Handle error responses from the backend
                st.session_state["general_response"] = "Failed to process the query. Please try again later."
                st.error("Failed to process the query. Please try again later.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Add Save Plan to Database functionality
    if st.session_state["current_plan"]:
        if st.button("Save Plan to Database", key="save_plan_button"):
            try:
                save_response = requests.post(
                    f"{DEPLOY_URL}/save_plan",
                    json={
                        "plan": st.session_state["current_plan"],
                        "summary": st.session_state["current_summary"],
                    },
                    headers={"Authorization": f"Bearer {st.session_state['access_token']}"},  # Include token
                )

                if save_response.status_code == 200:
                    st.session_state["save_status"] = f"Plan saved successfully. Plan ID: {save_response.json().get('plan_id')}"
                else:
                    st.session_state["save_status"] = f"Failed to save plan: {save_response.json().get('detail', 'Unknown error')}"

            except Exception as e:
                st.session_state["save_status"] = f"An error occurred while saving the plan: {e}"

        # Display save status without refreshing
        if st.session_state["save_status"]:
            st.success(st.session_state["save_status"])

    # Navigate to the Saved Plans page
    if st.button("View Saved Plans"):
        st.session_state["page"] = "plans"  # Update current page to "plans"
        st.rerun()  # Trigger rerun to load the new page

    # Display the general response in another text area
    st.text_area(
        "Learning Assistant Response",
        value=st.session_state.get("general_response", "No general response yet."),
        height=200,
        key="general_response_text"
    )

if __name__ == "__main__":
    main()