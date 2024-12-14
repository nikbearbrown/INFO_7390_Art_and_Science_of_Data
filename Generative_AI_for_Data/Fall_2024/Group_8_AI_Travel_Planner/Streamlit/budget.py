import streamlit as st
import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()
FASTAPI_URL = os.getenv("FASTAPI_URL")

def call_budget_endpoint(itinerary, modification_query=None):
    try:
        payload = {"itinerary": itinerary, "modification_query": modification_query}
        response = requests.post(f"{FASTAPI_URL}/generate-budget", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to connect to the budget endpoint: {e}")
        return None

def budget_page(itinerary_response):
    st.title("💰 Travel Budget Planner")

    if not itinerary_response:
        st.error("No itinerary context found. Please go back and generate an itinerary first.")
        if st.button("Go Back to Chat"):
            st.session_state.page = "Chat"
            st.experimental_rerun()
        return

    # Step 1: Display the initial budget
    st.info("Generating your personalized budget...")
    raw_data = call_budget_endpoint(itinerary_response)

    if raw_data and "budget" in raw_data:
        budget_data = raw_data["budget"]
        
        # Extracting title, objective, key categories, and expected total
        title = budget_data.get("Title", "Title unavailable.")
        objective = budget_data.get("Objective", "Objective not provided.")
        key_categories = budget_data.get("KeyCategories", [])
        expected_total = budget_data.get("ExpectedTotal", "N/A")

        # Display title, objective, and key categories as subtext
        st.subheader(title)
        st.markdown(f"**Objective:** {objective}")
        if key_categories:
            st.markdown("**Key Categories:**")
            for category in key_categories:
                st.markdown(f"- {category}")
        else:
            st.markdown("**Key Categories:** None provided.")

        st.markdown(f"**Expected Total Cost:** ${expected_total}")

        # Flatten JSON Breakdown into a tabular format
        breakdown = budget_data.get("Breakdown", [])
        if breakdown:
            flat_budget = [
                {"Category": item["Category"], "Item": item["Item"], "Cost": item["Cost"]}
                for item in breakdown
            ]
            df = pd.DataFrame(flat_budget)
            st.markdown("### Detailed Breakdown")
            st.table(df)  # Display the table
        else:
            st.warning("No breakdown data available.")

        # Step 2: Allow user to modify the budget
        modification_query = st.text_input("Refine Your Budget:", placeholder="e.g., Increase dining by 10%")
        if st.button("Update Budget"):
            updated_raw_data = call_budget_endpoint(itinerary_response, modification_query)
            if updated_raw_data and "budget" in updated_raw_data:
                refined_budget = updated_raw_data["budget"]
                st.success("Budget updated successfully! 🎉")

                # Extract updated breakdown
                updated_breakdown = refined_budget.get("Breakdown", [])
                if updated_breakdown:
                    flat_updated_budget = [
                        {"Category": item["Category"], "Item": item["Item"], "Cost": item["Cost"]}
                        for item in updated_breakdown
                    ]

                    # Convert to DataFrame for updated breakdown
                    df_updated = pd.DataFrame(flat_updated_budget)
                    st.markdown("### Updated Breakdown")
                    st.table(df_updated)  # Display the updated table
                else:
                    st.warning("No updated breakdown data available.")

                # Update and display the new expected total cost
                updated_total = refined_budget.get("ExpectedTotal", "N/A")
                st.markdown(f"**Updated Total Cost:** ${updated_total}")
            else:
                st.error("Failed to update the budget. Please try again.")
    else:
        st.error("Failed to generate budget. Please try again.")

    # Navigation back to Chat Page
    if st.button("Go Back to Chat"):
        st.session_state.page = "Chat"
        st.rerun()
