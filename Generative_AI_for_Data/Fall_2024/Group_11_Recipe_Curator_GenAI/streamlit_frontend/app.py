import streamlit as st
import requests
import json
import re
from wishlist_page import display_wishlisted_recipes
from recommendations_page import recommendations_page

# Store API endpoint
FASTAPI_ENDPOINT = "http://backend:8000"
# Title with emojis
st.title("Recipe Curator: The Smart Way to Discover Recipes You'll Love 👩🏻‍🍳 🌮")

# Initialize Streamlit session states
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "logged_out"  # Track the current page state (logged_out or logged_in)
if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = set()  # Initialize wishlist as a set to track wishlisted recipes

# Load the external CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS styles from the file
load_css("style.css")

# Function to convert ISO 8601 duration format to minutes/hours
def convert_iso8601_to_time(duration):
    if not duration:  # Check if the duration is None or empty
        return "N/A"  # Return "N/A" or any default value if duration is missing
    
    pattern = re.compile(r'P(T?)(\d+H)?(\d+M)?')
    match = pattern.match(duration)
    
    if not match:
        return duration  # Return as-is if no match

    time_str = ""
    hours = match.group(2)
    minutes = match.group(3)
    
    if hours:
        time_str += f"{int(hours[:-1])} hr "
    if minutes:
        time_str += f"{int(minutes[:-1])} min"
    
    return time_str.strip()

def sidebar():
    st.sidebar.image("images/recipe_logo.png", use_container_width=True)  # Add your logo file here

    # Check if the user is logged in
    if st.session_state["session_id"] is not None:
        st.sidebar.write(f"Welcome, {st.session_state['username']}!")
        st.sidebar.write("Get ready to find delicious recipes!")
        
        # Provide navigation
        selection = st.sidebar.radio(
            "Choose an option", 
            ["Recipe Search", "Wishlisted Recipes", "Recommendations"]
        )

        # Handle navigation
        if selection == "Recipe Search":
            st.session_state["page"] = "logged_in"
        elif selection == "Wishlisted Recipes":
            st.session_state["page"] = "wishlisted_recipes"
        elif selection == "Recommendations":
            st.session_state["page"] = "recommendations"

        # Logout button
        if st.sidebar.button("Logout"):
            logout()
    else:
        st.sidebar.write("Hello! You are about to discover the best dishes globally!! Turn in Now.")
# Function to handle about page
def about_page():
    st.header("About This App")
    st.write("🍽️ Welcome to the Conversational Recipe Finder!")
    st.write("This app helps you find recipes based on your ingredients, and you can also have conversational interactions to refine your search.")
    st.write("Simply start by providing a few ingredients, and the system will guide you to find relevant recipes. You can continue to refine your search by adding more ingredients.")
    st.write("You can login to save your sessions and preferences, or signup if you’re a new user!")

# Function to handle login
def login_page():
    st.header("Login")
    with st.form("login_form"):
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.form_submit_button("Login"):
            response = requests.post(f"{FASTAPI_ENDPOINT}/login", json={"username": login_username, "password": login_password})
            if response.status_code == 200:
                session_data = response.json()
                st.session_state["session_id"] = session_data.get("session_id")
                st.session_state["username"] = login_username
                st.session_state["page"] = "logged_in"  # Update the page state after login
                st.success("Login successful!")
            else:
                st.error("Login failed. Please check your credentials.")

# Dropdown options for countries and recipe categories
COUNTRIES = [
    "United States", "Canada", "India", "United Kingdom", "Australia",
    "Germany", "France", "Japan", "China", "Brazil", "South Africa",
    "Italy", "Mexico", "Russia", "Spain", "Sweden"
]

CATEGORIES = [
    "Frozen Desserts", "Chicken Breast", "Beverages", "Soy/Tofu", "Vegetable",
    "Pie", "Chicken", "Dessert", "Sauces", "Black Beans", "< 60 Mins",
    "Whole Chicken", "Cheesecake", "High In...", "Breakfast", "Breads",
    "Bar Cookie", "Pork", "Halibut", "Lamb/Sheep", "Very Low Carbs",
    "Drop Cookies", "Lunch/Snacks", "Punch Beverage", "< 30 Mins",
    "Sourdough Breads", "Steak", "Lobster", "Chutneys", "European", "Manicotti",
    "Chicken Thigh & Leg", "Lentil", "Summer", "Gelatin", "Spicy", "Stew",
    "Lactose Free", "Oranges", "Spaghetti", "Scones", "Low Cholesterol",
    "Coconut", "Broil/Grill", "Candy", "Greek", "Salad Dressings", "Melons",
    "Mexican", "< 15 Mins", "Weeknight", "Yeast Breads", "High Protein",
    "Free Of...", "Brazilian", "Brown Rice", "Beans", "Curries", "Chicken Livers",
    "Healthy", "Rice", "Chowders", "Spanish", "Clear Soup", "Southwestern U.S.",
    "Asian", "Potato", "Cheese", "Apple", "Cauliflower", "Tex Mex", "German",
    "Fruit", "Hungarian", "New Zealand", "Corn", "Long Grain Rice",
    "Southwest Asia (Middle East)", "Dutch", "Tuna", "Peppers", "Raspberries",
    "Crawfish", "Beef Organ Meats", "Strawberry", "Shakes", "Thai", "Cajun",
    "Low Protein", "Crab", "Jellies", "Pears", "White Rice", "Onions",
    "Short Grain Rice", "One Dish Meal", "Smoothies", "Microwave", "Poultry"
]

# Function to handle signup
def signup_page():
    st.header("Signup")
    with st.form("signup_form"):
        # New fields: Name, Country, Recipe Category
        name = st.text_input("Name", key="signup_name")
        username = st.text_input("Username", key="signup_username")
        password = st.text_input("Password", type="password", key="signup_password")
        country = st.selectbox("Country", COUNTRIES, key="signup_country")
        selected_categories = st.multiselect(
            "Favorite Recipe Categories (Select up to 5)", CATEGORIES, key="recipe_categories"
        )

        # Enforce a maximum of 5 selections
        if len(selected_categories) > 5:
            st.warning("You can select up to 5 categories only.")

        # Display selected categories as badges
        if selected_categories:
            st.markdown("### Selected Categories:")
            badges_html = " ".join(
                [f'<span class="badge">{category}</span>' for category in selected_categories]
            )
            st.markdown(f'<div class="badge-container">{badges_html}</div>', unsafe_allow_html=True)

        if st.form_submit_button("Signup"):
            if len(selected_categories) > 5:
                st.error("Please select only up to 5 categories.")
            else:
                response = requests.post(f"{FASTAPI_ENDPOINT}/signup", 
                                         json={
                                             "name": name,
                                             "username": username,
                                             "password": password,
                                             "country": country,
                                             "favorite_categories": selected_categories
                                         })
                if response.status_code == 200:
                    st.success("Signup successful! You can now log in.")
                else:
                    st.error("Signup failed. Please try again.")


# Function to add a recipe to the wishlist
def add_to_wishlist(recipe_name):
    if recipe_name not in st.session_state["wishlist"]:
        st.session_state["wishlist"].add(recipe_name)
        payload = {
            "username": st.session_state["username"],
            "recipe_name": recipe_name
        }
        response = requests.post(f"{FASTAPI_ENDPOINT}/wishlist", json=payload)
        if response.status_code == 200:
            st.success(f"{recipe_name} has been added to your wishlist!")
        else:
            st.error("Failed to add recipe to wishlist. Please try again.")

# Function to search for recipes with UI and wishlist button
def recipe_search():
    st.header("Recipe Search 🍝 ✨")

    # Input for search query
    ingredient = st.text_input("Enter a recipe or ingredient to search for recipes", key="ingredient_search_input")

    # Check if results already exist in session state
    if "search_results" not in st.session_state:
        st.session_state["search_results"] = None

    # Perform search on button click
    if st.button("Search"):
        if ingredient:
            response = requests.post(f"{FASTAPI_ENDPOINT}/search_recipes/",
                                     json={"query": ingredient, "session_id": st.session_state["session_id"]})

            if response.status_code == 200:
                data = response.json()
                st.session_state["search_results"] = data  # Save results in session state
                st.session_state["search_ingredient"] = ingredient  # Save the ingredient
            else:
                st.error("Failed to fetch recipes. Please try again later.")

    # Display search results
    if st.session_state["search_results"]:
        data = st.session_state["search_results"]
        summary = data.get("summary")
        recipes = data.get("recipes")

        # Display the summary
        if summary:
            st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True)

        # Display the recipes
        if recipes:
            for recipe in recipes:
                # Check if the recipe is already wishlisted
                is_wishlisted = recipe["Name"] in st.session_state["wishlist"]
                wishlist_button_label = "Wishlisted ❤️" if is_wishlisted else f"Add to Wishlist: {recipe['Name']}"
                # Recipe card content with details
                card_content = f"""
                <div class='recipe-card'>
                        <div class='recipe-header'>
                            <h2 class='recipe-title'>{recipe['Name']}</h2>
                        </div>
                        <div class='recipe-info'><strong>Preparation Time:</strong> {convert_iso8601_to_time(recipe['PrepTime'])}</div>
                        <div class='recipe-info'><strong>Cook Time:</strong> {convert_iso8601_to_time(recipe['CookTime'])}</div>
                        <div class='recipe-info'><strong>Total Time:</strong> {convert_iso8601_to_time(recipe['TotalTime'])}</div>
                        <div class='recipe-info'><strong>Description:</strong> {recipe['Description']}</div>
                        """

                # Display top 5 images horizontally
                if recipe.get('Images'):
                    card_content += "<div class='scrolling-wrapper'>"
                    for img_url in recipe['Images'][:5]:
                        card_content += f"<img class='scroll-img' src='{img_url}' width='150' height='150'>"
                    card_content += "</div>"

                card_content += "</div>"  # Close recipe card

                # Render the card content
                st.markdown(card_content, unsafe_allow_html=True)

                # Expander for ingredients, instructions, and nutrition analysis
                with st.expander(f"Read More: {recipe['Name']}"):
                     # Ingredients
                    quantities = recipe.get('RecipeIngredientQuantities', [])
                    parts = recipe.get('RecipeIngredientParts', [])
                    if quantities and parts:
                        combined_ingredients = ", ".join([f"{quantity} {part}" for quantity, part in zip(quantities, parts)])
                        st.markdown(f"<div class='ingredients'><strong>Ingredients:</strong> {combined_ingredients}</div>", unsafe_allow_html=True)

                    # Instructions combined into a single "bubble"
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
                

                # Add Wishlist button
                if st.button(wishlist_button_label, key=f"wishlist_{recipe['Name']}"):
                    add_to_wishlist(recipe["Name"])

        else:
            st.write("No matching recipes found.")
    

# Function to handle logout
def logout():
    st.session_state["session_id"] = None
    st.session_state["username"] = None
    st.session_state["page"] = "logged_out"
    st.session_state["wishlist"] = set()  # Reset the wishlist
    st.success("Logged out successfully!")

# Main content with tabs
def main_content():
    tab1, tab2, tab3 = st.tabs(["About", "Login", "Signup"])

    with tab1:
        about_page()

    with tab2:
        login_page()

    with tab3:
        signup_page()

# Main app function
def main():
    sidebar()

    if st.session_state["session_id"] is None:
        main_content()
    elif st.session_state["page"] == "logged_in":
        recipe_search()
    elif st.session_state["page"] == "wishlisted_recipes":
        display_wishlisted_recipes()  
    elif st.session_state["page"] == "recommendations":
        recommendations_page() 
# Run the main function
if __name__ == "__main__":
    main()
