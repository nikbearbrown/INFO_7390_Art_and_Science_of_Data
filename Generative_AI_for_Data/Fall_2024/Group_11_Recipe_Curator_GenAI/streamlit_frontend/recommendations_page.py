import streamlit as st
import requests

FASTAPI_ENDPOINT = "http://backend:8000"

# Function to convert ISO 8601 duration format to minutes/hours
def convert_iso8601_to_time(duration):
    if not duration:  # Check if the duration is None or empty
        return "N/A"  

    import re
    pattern = re.compile(r'P(T?)(\d+H)?(\d+M)?')
    match = pattern.match(duration)

    if not match:
        return "N/A"  # Return "N/A" if the format doesn't match

    time_str = ""
    hours = match.group(2)
    minutes = match.group(3)

    if hours:
        time_str += f"{int(hours[:-1])} hr "
    if minutes:
        time_str += f"{int(minutes[:-1])} min"

    return time_str.strip()

# Function to load the external CSS file
def load_css(file_name):
    """Loads a CSS file into the Streamlit app."""
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def recommendations_page():
    st.header("Recommended Recipes 🍽️")

    # Load custom CSS for recommendations
    load_css("recommendations_style.css")  # Path to your recommendations CSS

    if "username" not in st.session_state or st.session_state["username"] is None:
        st.warning("Please log in to see recommendations.")
        return

    username = st.session_state["username"]

    # Fetch user details to get favorite categories
    user_response = requests.get(f"{FASTAPI_ENDPOINT}/user/{username}")
    if user_response.status_code == 200:
        user_data = user_response.json()
        favorite_categories = user_data.get("favorite_categories", [])
    else:
        st.error("Failed to fetch user information.")
        return

    # Display favorite categories as badges
    if favorite_categories:
        st.markdown("### Your Favorite Categories 🍱 🌮")
        badge_style = (
            "display: inline-block; padding: 6px 12px; background-color: #ff9aa2; "
            "border-radius: 15px; margin: 5px; color: #333; font-size: 14px;"
        )
        badges_html = " ".join([
            f"<span style='{badge_style}'>{category}</span>"
            for category in favorite_categories
        ])
        box_style = (
            "border: 1px solid #ddd; padding: 10px; border-radius: 10px; "
            "background-color: #f9f9f9; text-align: center; margin-bottom: 20px;"
        )
        st.markdown(f"<div style='{box_style}'>{badges_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown("### No favorite categories found.")

    # Fetch recommendations from the backend
    response = requests.get(f"{FASTAPI_ENDPOINT}/recommendations/{username}")
    st.markdown("### Top 3 Recipes are Recommended based on your favourite categories and recipe search 🍟 🍔")
    if response.status_code == 200:
        recommended_recipes = response.json().get("recipes", [])
        if recommended_recipes:
            # Group recipes by category
            recipes_by_category = {}
            for recipe in recommended_recipes:
                category = recipe.get('RecipeCategory', 'Others')
                if category not in recipes_by_category:
                    recipes_by_category[category] = []
                recipes_by_category[category].append(recipe)

            # Render recommendations grouped by category
            for category, recipes in recipes_by_category.items():
                # Render the category as a subheading
                category_style = (
                    "text-align: center; background-color: #e6e6fa; color: #4a4a4a; "
                    "padding: 8px; border-radius: 15px; margin: 20px 0; font-size: 18px; font-weight: bold;"
                )
                st.markdown(f"<div style='{category_style}'>{category}</div>", unsafe_allow_html=True)

                # Render the recipes for this category
                for recipe in recipes:
                    name = recipe.get('Name', 'N/A')
                    description = recipe.get('Description', 'N/A')
                    prep_time = convert_iso8601_to_time(recipe.get('PrepTime', 'N/A'))
                    cook_time = convert_iso8601_to_time(recipe.get('CookTime', 'N/A'))
                    total_time = convert_iso8601_to_time(recipe.get('TotalTime', 'N/A'))
                    images = recipe.get('Images', [])

                    # Build the recipe card with images directly inside
                    card_content = f"""
                    <div class="recipe-card">
                        <div class="recipe-header">
                            <h2 class="recipe-title">{name}</h2>
                        </div>
                        <div class="recipe-info"><strong>Preparation Time:</strong> {prep_time}</div>
                        <div class="recipe-info"><strong>Cook Time:</strong> {cook_time}</div>
                        <div class="recipe-info"><strong>Total Time:</strong> {total_time}</div>
                        <div class="recipe-info"><strong>Description:</strong> {description}</div>
                    """

                    # Add images directly inside the card
                    if images:
                        card_content += "<div class='scrolling-wrapper'>"
                        for img_url in images[:3]:  # Display up to 3 images
                            card_content += f"<img class='scroll-img' src='{img_url}' alt='Recipe Image'>"
                        card_content += "</div>"

                    card_content += "</div>"  # Close recipe card
                    st.markdown(card_content, unsafe_allow_html=True)

                    # Expander for additional details
                    with st.expander(f"Read More: {name}"):
                        # Ingredients
                        if recipe.get('RecipeIngredientQuantities') and recipe.get('RecipeIngredientParts'):
                            combined_ingredients = ", ".join([
                                f"{quantity} {part}"
                                for quantity, part in zip(recipe['RecipeIngredientQuantities'], recipe['RecipeIngredientParts'])
                            ])
                            st.markdown(f"<div class='ingredients'><strong>Ingredients:</strong> {combined_ingredients}</div>", unsafe_allow_html=True)

                        # Instructions
                        if recipe.get('RecipeInstructions'):
                            combined_instructions = "<br>".join([f"- {step}" for step in recipe['RecipeInstructions']])
                            st.markdown(f"<div class='instructions'><strong>Instructions:</strong><br>{combined_instructions}</div>", unsafe_allow_html=True)

                        # Nutrition analysis
                        nutrition_analysis = f"""
                        <div class='nutrition-analysis'>
                            <strong>Nutrition Analysis:</strong><br>
                            <strong>Calories:</strong> {recipe.get('Calories', 'N/A')}<br>
                        </div>
                        """
                        st.markdown(nutrition_analysis, unsafe_allow_html=True)

        else:
            st.write("No recommendations found for your favorite categories.")
    else:
        st.error("Failed to fetch recommendations.")
