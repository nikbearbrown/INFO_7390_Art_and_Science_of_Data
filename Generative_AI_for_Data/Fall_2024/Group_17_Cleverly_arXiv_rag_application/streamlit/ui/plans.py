import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the FastAPI URL from environment variables
DEPLOY_URL = os.getenv("DEPLOY_URL", "http://127.0.0.1:8000")

def main():
    st.title("Saved Plans")

    # Ensure username and access_token are available in session state
    if "username" not in st.session_state or "access_token" not in st.session_state:
        st.error("You are not logged in. Please log in to view your plans.")
        return

    username = st.session_state["username"]
    access_token = st.session_state["access_token"]

    # Button to navigate back to the Planner
    if st.button("Make a new Plan"):
        st.session_state["page"] = "planner"
        st.rerun()

    # Fetch all saved plans for the logged-in user from the backend
    try:
        response = requests.get(
            f"{DEPLOY_URL}/get_plans",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code == 200:
            plans = response.json()  # Backend filters plans based on logged-in user
            if isinstance(plans, dict) and "message" in plans:
                st.warning(plans["message"])  # Display a message if no plans are found
                plans = []
        else:
            st.error("Failed to fetch plans.")
            plans = []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        plans = []

    if not plans:
        st.info("No saved plans available.")
        return

    # Searchable Dropdown
    search_term = st.text_input("Search Plans", placeholder="Type to search plans")
    filtered_plans = [plan for plan in plans if search_term.lower() in plan["title"].lower()]

    if not filtered_plans:
        st.warning("No plans match your search.")
        return

    plan_options = {plan["plan_id"]: plan["title"] for plan in filtered_plans}
    # Add a limit to the dropdown by controlling the display items
    max_display_items = 100  # Customize as per UI preference
    selected_plan_id = st.selectbox(
        "Select a Plan",
        options=list(plan_options.keys())[:max_display_items],  # Limit to max_display_items
        format_func=lambda x: plan_options[x] if x in plan_options else "Unknown Plan",
    )

    # Display selected plan details
    if selected_plan_id:
        selected_plan = next((plan for plan in plans if plan["plan_id"] == selected_plan_id), None)

        if not selected_plan:
            st.error("Selected plan could not be found.")
            return

        st.markdown(f"### Plan Title")
        st.write(selected_plan["title"])

        st.markdown(f"### Plan Summary")
        st.write(selected_plan["summary"])

        st.markdown(f"### Key Topics")
        key_topics = selected_plan.get("key_topics", [])
        if isinstance(key_topics, list):
            st.write(", ".join(key_topics) if key_topics else "No key topics available.")
        else:
            st.write("Invalid key topics format.")

        st.markdown(f"### Outcomes")
        st.write(selected_plan.get("learning_outcomes", "No outcomes provided."))

        # Fetch modules for the selected plan
        try:
            modules_response = requests.get(
                f"{DEPLOY_URL}/get_modules/{selected_plan_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if modules_response.status_code == 200:
                modules = modules_response.json()  # Backend returns modules for the selected plan
                if isinstance(modules, dict) and "message" in modules:
                    st.warning(modules["message"])  # Display a message if no modules are found
                    modules = []
            else:
                st.error("Failed to fetch modules for the selected plan.")
                modules = []
        except Exception as e:
            st.error(f"An error occurred while fetching modules: {e}")
            modules = []

        if modules:
            st.markdown("## Plan Modules")
            for module in modules:
                st.markdown(f"#### Module {module['module']}: {module['title']}")
                st.write(module.get("description", "No description available."))

                # Add a button to navigate to the "lesson" page for each module
                if st.button(f"Go to Lesson for Module {module['module']}", key=f"lesson_{module['module_id']}"):
                    st.session_state["selected_module_id"] = module["module_id"]
                    st.session_state["page"] = "lesson"
                    st.rerun()

if __name__ == "__main__":
    main()
