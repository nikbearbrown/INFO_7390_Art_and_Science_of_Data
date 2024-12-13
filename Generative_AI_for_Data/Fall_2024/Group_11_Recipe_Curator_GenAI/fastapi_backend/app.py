import os
import snowflake.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
import uuid
import json
from transformers import AutoTokenizer, AutoModel
import torch
from pinecone import Pinecone
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Setup FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware for conversational memory
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecretkey"))

# Pinecone configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "recipes-index-v1"
index = pc.Index(name=INDEX_NAME)

# Load Hugging Face model for embedding generation
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Configure Google Gemini (Generative AI)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Snowflake connection details
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

# In-memory storage for conversational state (use Redis for production)
user_conversational_memory = {}

# Snowflake connection setup
def connect_to_snowflake():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

# Model for user query
class RecipeQuery(BaseModel):
    query: str
    session_id: Optional[str] = None

# Model for user credentials and additional fields
class UserSignup(BaseModel):
    username: str
    password: str
    name: str
    country: str
    favorite_categories: List[str]

# Model for login credentials
class UserCredentials(BaseModel):
    username: str
    password: str

# Model for wishlist
class Wishlist(BaseModel):
    username: str
    recipe_name: str

@app.post("/wishlist")
def add_to_wishlist(wishlist: Wishlist):
    logging.info(f"Received request to add {wishlist.recipe_name} for user {wishlist.username}")
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO WISHLIST (wishlist_id, username, recipe_name)
            VALUES (%s, %s, %s)
        """
        values = (str(uuid.uuid4()), wishlist.username, wishlist.recipe_name)
        logging.info(f"Executing query: {query} with values {values}")
        cursor.execute(query, values)
        conn.commit()
        logging.info(f"Successfully added {wishlist.recipe_name} to wishlist for user {wishlist.username}")
        return {"message": f"{wishlist.recipe_name} added to wishlist"}
    except Exception as e:
        logging.error(f"Error adding to wishlist: {e}")
        raise HTTPException(status_code=400, detail="Failed to add to wishlist.")
    finally:
        cursor.close()
        conn.close()


# Function to perform user signup
@app.post("/signup")
def signup(user: UserSignup):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USERS (user_id, username, password, name, country, favorite_categories)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), user.username, user.password, user.name, user.country, json.dumps(user.favorite_categories)))
        return {"message": "Signup successful"}
    except Exception as e:
        logging.error(f"Error during signup: {e}")
        raise HTTPException(status_code=400, detail="Signup failed.")
    finally:
        cursor.close()
        conn.close()

# Function to perform user login
@app.post("/login")
def login(user: UserCredentials):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM USERS WHERE username = %s AND password = %s
        """, (user.username, user.password))
        result = cursor.fetchone()
        if result:
            return {"message": "Login successful", "session_id": str(uuid.uuid4())}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise HTTPException(status_code=400, detail="Login failed.")
    finally:
        cursor.close()
        conn.close()

# Function to generate query embedding
def generate_query_embedding(query):
    inputs = tokenizer(query, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Function to fetch recipes from Snowflake
def fetch_recipes_from_snowflake(recipe_ids):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        sql_query = '''
        SELECT RecipeId, Name, Description, Images, PrepTime, CookTime, TotalTime, 
               RecipeIngredientQuantities, RecipeIngredientParts, RecipeInstructions, 
               Calories, AggregatedRating, ReviewCount, RecipeCategory
        FROM RECIPES
        WHERE RecipeId IN ({})
        '''.format(','.join(['%s'] * len(recipe_ids)))
        cursor.execute(sql_query, recipe_ids)
        rows = cursor.fetchall()
        recipes = []
        for row in rows:
            recipe = {
                'RecipeId': row[0],
                'Name': row[1],
                'Description': row[2],
                'Images': json.loads(row[3]) if row[3] else [],
                'PrepTime': row[4],
                'CookTime': row[5],
                'TotalTime': row[6],
                'RecipeIngredientQuantities': json.loads(row[7]) if row[7] else [],
                'RecipeIngredientParts': json.loads(row[8]) if row[8] else [],
                'RecipeInstructions': json.loads(row[9]) if row[9] else [],
                'Calories': row[10],
                'AggregatedRating': row[11],
                'ReviewCount': row[12],
                'RecipeCategory': row[13]
            }
            recipes.append(recipe)
        return recipes
    except Exception as e:
        logging.error(f"Failed to fetch recipes from Snowflake: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to summarize the results using Google Gemini
def summarize_results(query, recipes):
    try:
        if recipes:
            content_to_summarize = f"Based on your query for {query}, here are five recommended recipes: "
            for i, recipe in enumerate(recipes[:5]):
                content_to_summarize += (
                    f"'{recipe['Name']}', a {recipe['RecipeCategory']} dish that takes {recipe['TotalTime']} to prepare. "
                    f"It has {recipe['Calories']} calories and an average rating of {recipe['AggregatedRating']} from {recipe['ReviewCount']} reviews. "
                )

            prompt = (
                f"Please provide a single paragraph summarizing these recipes in a friendly tone without asking questions or requesting more details. "
                f"{content_to_summarize}"
            )

            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content([prompt])
            summary = response.text.strip()
            return summary
        else:
            return "No matching recipes found for your query."
    except Exception as e:
        logging.error(f"Error with Google Gemini API: {e}")
        return "An error occurred while summarizing the results."

# Recipe search endpoint with conversational memory and summarization
@app.post("/search_recipes/")
def search_recipes(data: RecipeQuery):
    session_id = data.session_id or str(uuid.uuid4())

    if session_id not in user_conversational_memory:
        user_conversational_memory[session_id] = []

    user_conversational_memory[session_id].append(data.query)
    combined_query = " ".join(user_conversational_memory[session_id])

    embedding = generate_query_embedding(combined_query)
    embedding_list = embedding.tolist()

    response = index.query(vector=embedding_list, top_k=10)
    recipe_ids = [match.id for match in response.matches]

    recipes = fetch_recipes_from_snowflake(recipe_ids)
    summary = summarize_results(data.query, recipes)

    return {"summary": summary, "recipes": recipes, "session_id": session_id}

@app.get("/wishlist/{username}")
def get_wishlisted_recipes(username: str):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()

        # Fetch wishlisted recipe names for the given username
        cursor.execute("""
            SELECT recipe_name FROM WISHLIST WHERE username = %s
        """, (username,))
        wishlisted_recipe_names = [row[0] for row in cursor.fetchall()]

        if not wishlisted_recipe_names:
            return {"recipes": []}

        # Fetch full recipe details for all wishlisted recipes
        placeholders = ','.join(['%s'] * len(wishlisted_recipe_names))
        query = f"""
            SELECT RecipeId, Name, Description, Images, PrepTime, CookTime, TotalTime, 
                   RecipeIngredientQuantities, RecipeIngredientParts, RecipeInstructions, 
                   Calories, AggregatedRating, ReviewCount, RecipeCategory
            FROM RECIPES
            WHERE Name IN ({placeholders})
        """
        cursor.execute(query, wishlisted_recipe_names)
        recipes = [
            {
                "RecipeId": row[0],
                "Name": row[1],
                "Description": row[2],
                "Images": json.loads(row[3]) if row[3] else [],
                "PrepTime": row[4],
                "CookTime": row[5],
                "TotalTime": row[6],
                "RecipeIngredientQuantities": json.loads(row[7]) if row[7] else [],
                "RecipeIngredientParts": json.loads(row[8]) if row[8] else [],
                "RecipeInstructions": json.loads(row[9]) if row[9] else [],
                "Calories": row[10],
                "AggregatedRating": row[11],
                "ReviewCount": row[12],
                "RecipeCategory": row[13],
            }
            for row in cursor.fetchall()
        ]

        return {"recipes": recipes}

    except Exception as e:
        logging.error(f"Failed to fetch wishlisted recipes for {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch wishlisted recipes.")
    finally:
        cursor.close()
        conn.close()

@app.delete("/wishlist")
def remove_from_wishlist(wishlist: Wishlist):
    logging.info(f"Received request to remove {wishlist.recipe_name} for user {wishlist.username}")
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        query = """
            DELETE FROM WISHLIST
            WHERE username = %s AND recipe_name = %s
        """
        values = (wishlist.username, wishlist.recipe_name)
        logging.info(f"Executing query: {query} with values {values}")
        cursor.execute(query, values)
        conn.commit()
        logging.info(f"Successfully removed {wishlist.recipe_name} from wishlist for user {wishlist.username}")
        return {"message": f"{wishlist.recipe_name} removed from wishlist"}
    except Exception as e:
        logging.error(f"Error removing from wishlist: {e}")
        raise HTTPException(status_code=400, detail="Failed to remove from wishlist.")
    finally:
        cursor.close()
        conn.close()

@app.get("/recommendations/{username}")
def get_recommendations(username: str):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()

        # Fetch the user's favorite categories
        cursor.execute("""
            SELECT favorite_categories FROM USERS WHERE username = %s
        """, (username,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        favorite_categories = json.loads(result[0])  # Convert JSON string to list

        # Fetch top 3 recipes for each favorite category
        recommendations = []
        for category in favorite_categories:
            cursor.execute("""
                SELECT RecipeId, Name, Description, Images, PrepTime, CookTime, TotalTime, 
                       RecipeIngredientQuantities, RecipeIngredientParts, RecipeInstructions, 
                       Calories, AggregatedRating, ReviewCount, RecipeCategory 
                FROM RECIPES 
                WHERE RecipeCategory = %s 
                LIMIT 3
            """, (category,))
            rows = cursor.fetchall()

            for row in rows:
                recommendations.append({
                    "RecipeId": row[0],
                    "Name": row[1],
                    "Description": row[2],
                    "Images": json.loads(row[3]) if row[3] else [],
                    "PrepTime": row[4] or "N/A",
                    "CookTime": row[5] or "N/A",
                    "TotalTime": row[6] or "N/A",
                    "RecipeIngredientQuantities": json.loads(row[7]) if row[7] else [],
                    "RecipeIngredientParts": json.loads(row[8]) if row[8] else [],
                    "RecipeInstructions": json.loads(row[9]) if row[9] else [],
                    "Calories": row[10] or "N/A",
                    "AggregatedRating": row[11] or "N/A",
                    "ReviewCount": row[12] or "N/A",
                    "RecipeCategory": row[13]
                })

        return {"recipes": recommendations}

    except Exception as e:
        logging.error(f"Failed to fetch recommendations for {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations.")
    finally:
        cursor.close()
        conn.close()

@app.get("/user/{username}")
def get_user(username: str):
    conn = connect_to_snowflake()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT favorite_categories FROM USERS WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        favorite_categories = json.loads(result[0])  # Convert JSON string to list
        return {"username": username, "favorite_categories": favorite_categories}
    except Exception as e:
        logging.error(f"Failed to fetch user data for {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user data.")
    finally:
        cursor.close()
        conn.close()
