import streamlit as st
import requests

# Function to load the external CSS file
def load_css(file_name):
    """Loads a CSS file into the Streamlit app."""
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css("wishlist_style.css")  # Replace with the actual path to your style.css file

# Function to fetch wishlisted recipes
def fetch_wishlisted_recipes(username):
    response = requests.get(f"http://backend:8000/wishlist/{username}")
    if response.status_code == 200:
        return response.json().get("recipes", [])
    else:
        st.error("Failed to fetch wishlisted recipes. Please try again.")
        return []

def display_wishlisted_recipes():
    st.header("Your Wishlisted Recipes ❤️ ")

    # Ensure user is logged in
    if st.session_state.get("username") is None:
        st.warning("Please log in to view your wishlisted recipes.")
        return

    # Fetch wishlisted recipes for the current user
    recipes = fetch_wishlisted_recipes(st.session_state["username"])

    if not recipes:
        st.write("No recipes in your wishlist yet.")
        return

    # Iterate through each recipe
    for recipe in recipes:
        # Build the recipe card with images directly inside
        card_content = f"""
        <div class="recipe-card">
            <div class="recipe-header">
                <h2 class="recipe-title">{recipe['Name']}</h2>
            </div>
            <div class="recipe-info"><strong>Preparation Time:</strong> {recipe['PrepTime']}</div>
            <div class="recipe-info"><strong>Cook Time:</strong> {recipe['CookTime']}</div>
            <div class="recipe-info"><strong>Total Time:</strong> {recipe['TotalTime']}</div>
            <div class="recipe-info"><strong>Description:</strong> {recipe['Description']}</div>
        """

        # Add images directly inside the card
        if recipe.get('Images'):
            card_content += "<div class='scrolling-wrapper'>"
            for img_url in recipe['Images']:
                card_content += f"<img class='scroll-img' src='{img_url}' alt='Recipe Image'>"
            card_content += "</div>"

        card_content += "</div>"  # Close recipe card
        st.markdown(card_content, unsafe_allow_html=True)

        # Add "Remove from Wishlist" button
        if st.button(f"Remove from Wishlist: {recipe['Name']}", key=f"remove_{recipe['Name']}"):
            remove_from_wishlist(recipe['Name'])

        # Expander for additional details
        with st.expander(f"Read More: {recipe['Name']}"):
            # Ingredients
            quantities = recipe.get('RecipeIngredientQuantities', [])
            parts = recipe.get('RecipeIngredientParts', [])
            if quantities and parts:
                combined_ingredients = ", ".join([f"{quantity} {part}" for quantity, part in zip(quantities, parts)])
                st.markdown(f"<div class='ingredients'><strong>Ingredients:</strong> {combined_ingredients}</div>", unsafe_allow_html=True)

            # Instructions
            instructions = recipe.get('RecipeInstructions', [])
            if instructions:
                combined_instructions = "<br>".join([f"- {step}" for step in instructions])
                st.markdown(f"<div class='instructions'><strong>Instructions:</strong><br>{combined_instructions}</div>", unsafe_allow_html=True)

            # Nutrition analysis
            nutrition_analysis = f"""
            <div class='nutrition-analysis'>
                <strong>Nutrition Analysis:</strong><br>
                <strong>Calories:</strong> {recipe.get('Calories', 'N/A')}<br>
            </div>
            """
            st.markdown(nutrition_analysis, unsafe_allow_html=True)


# Function to remove a recipe from the wishlist
def remove_from_wishlist(recipe_name):
    payload = {
        "username": st.session_state["username"],
        "recipe_name": recipe_name
    }
    response = requests.delete(f"http://backend:8000/wishlist", json=payload)
    if response.status_code == 200:
        st.success(f"{recipe_name} has been removed from your wishlist.")
        # Refresh the wishlist
        st.session_state["wishlist"] = fetch_wishlisted_recipes(st.session_state["username"])
    else:
        st.error("Failed to remove recipe from wishlist. Please try again.")
