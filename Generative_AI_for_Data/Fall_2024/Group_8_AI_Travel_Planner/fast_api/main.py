from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import snowflake.connector
from passlib.context import CryptContext
import os
from fastapi import Form
from websearch_normal import search_web, generate_response
from youtube_search import search_youtube
from openai_response import is_travel_related_gpt, fetch_and_generate_response, generate_response_with_relevant_data
from typing import Optional
import json
from openai import OpenAI
import pandas as pd

# FastAPI app
app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Snowflake connection details (update with your credentials)
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )

class SignupModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

class BudgetRequest(BaseModel):
    itinerary: str
    modification_query: Optional[str] = None  # Accepts `None` for modification_query   

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/signup")
async def signup(username: str, password: str):
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already taken")

        # Insert the new user
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password),
        )
        conn.commit()
        return {"message": "User signed up successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.post("/login")
async def login(username: str, password: str):
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        # Check if the user exists
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Verify the password
        stored_password_hash = result[0]
        if not verify_password(password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

## --- websearch----
# Request model for search_web endpoint
class SearchRequest(BaseModel):
    query: str
    max_results: int = 1  # Default to 1 result

# Endpoint for the search_web function
@app.post("/search")
async def search(request: SearchRequest):
    try:
        results = search_web(query=request.query, max_results=request.max_results)
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Request model for generate_response endpoint
class GenerateRequest(BaseModel):
    query: str

# Endpoint for the generate_response function
@app.post("/generate-response")
async def generate(request: GenerateRequest):
    try:
        response = generate_response(query=request.query)
        if response.startswith("Error"):
            raise HTTPException(status_code=400, detail=response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ------youtube search --------
# Request model for the YouTube search endpoint
class YouTubeSearchRequest(BaseModel):
    query: str
    max_results: int = 1  # Default to 1 result

# Endpoint for the YouTube search function
@app.post("/youtube-search")
async def youtube_search(request: YouTubeSearchRequest):
    try:
        results = search_youtube(query=request.query, max_results=request.max_results)
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------Open ai response ------
# Request model for the OpenAI response generation
class GenerateResponseRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.75

# Endpoint to validate if a query is travel-related
@app.post("/validate-query")
async def validate_query(query: str):
    try:
        is_travel_related = is_travel_related_gpt(query)
        return {"is_travel_related": is_travel_related}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating query: {e}")

# Endpoint to fetch and generate a detailed response
@app.post("/generate-openai-response")
async def generate_openai_response(request: GenerateResponseRequest):
    try:
        # Validate if the query is travel-related
        is_travel_related = is_travel_related_gpt(request.query)
        if not is_travel_related:
            raise HTTPException(
                status_code=400, 
                detail="This query doesn't seem travel-related. Please try with a travel-focused query."
            )
        
        # Fetch relevant matches from Pinecone (use request.top_k and request.threshold)
        # Mock Pinecone results for demonstration
        relevant_matches = [
            {"metadata": {"text": "Visit the Eiffel Tower and the Louvre Museum.", "title": "Paris Highlights"}},
            {"metadata": {"text": "Enjoy a Seine River Cruise and explore Montmartre.", "title": "Romantic Paris"}},
        ]

        # Generate the response using OpenAI
        response = generate_response_with_relevant_data(request.query, relevant_matches)
        return {"response": response}
    except HTTPException as http_err:
        # Log and re-raise HTTP exceptions
        logging.error(f"HTTP Error: {http_err.detail}")
        raise http_err
    except Exception as e:
        # Handle other exceptions gracefully
        logging.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing your request.")

@app.post("/generate-budget")
def generate_budget(request: BudgetRequest):
    """
    Generate or modify a budget using LLM.
    """
    try:
        system_prompt = (
            "You are a highly skilled assistant specializing in creating structured and actionable travel budgets that inspire users to plan and manage their trips effectively. "
            "Your budgets should balance precision and realism, providing clear and engaging breakdowns that reflect accurate, region-specific costs. "
            "Descriptions should be practical yet approachable, with relatable examples demonstrating how the costs align with real-world scenarios. "
            "Each budget plan should include:\n"
            "- A concise and compelling title summarizing the budget's purpose.\n"
            "- A motivational and clear objective explaining what the budget achieves for the user, written in an approachable and inspiring manner.\n"
            "- Key cost categories broken into digestible and intuitive segments to simplify budget management.\n"
            "- A detailed breakdown of costs for each category with insightful descriptions that explain the relevance and practicality of these expenses. Use relatable examples to showcase real-world applications.\n"
            "- A structured and measurable expected total to give users a comprehensive understanding of the trip’s financial requirements.\n"
            "If updating an existing budget, carefully refine the relevant sections based on the user's query while preserving the overall structure and coherence of the plan. "
            "Strictly return a valid JSON output only. Do not include any introductory text, explanations, or comments. The response should consist solely of the JSON structure in this format:\n"
            "{\n"
            '  "Title": "Budget for a 5-Day Paris Trip",\n'
            '  "Objective": "A clear and concise plan to help you manage expenses effectively for a 5-day trip to Paris.",\n'
            '  "KeyCategories": ["Accommodation", "Food", "Transportation", "Activities", "Miscellaneous"],\n'
            '  "Breakdown": [\n'
            '    {"Category": "Accommodation", "Item": "Hotel Stay (5 Nights)", "Cost": 500},\n'
            '    {"Category": "Food", "Item": "Daily Meals", "Cost": 150},\n'
            '    {"Category": "Transportation", "Item": "Flights", "Cost": 300},\n'
            '    {"Category": "Transportation", "Item": "Local Transport", "Cost": 50},\n'
            '    {"Category": "Activities", "Item": "Museum Tickets", "Cost": 40},\n'
            '    {"Category": "Activities", "Item": "Guided Tours", "Cost": 100},\n'
            '    {"Category": "Miscellaneous", "Item": "Souvenirs", "Cost": 50}\n'
            "  ],\n"
            '  "ExpectedTotal": 1190\n'
            "}\n"
            "Focus on providing content that is practical, accurate, and relatable while ensuring the JSON structure is complete, valid, and error-free. Tailor each budget to the user's itinerary to make the financial planning journey personal and impactful. Ensure that the output contains only the JSON and nothing else."
        )

        # Prepare the messages payload
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Itinerary: {request.itinerary}"},
        ]
        if request.modification_query:
            messages.append({"role": "user", "content": f"Modification: {request.modification_query}"})

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        # Extract response content
        raw_output = response.choices[0].message.content
        print("Raw OpenAI Output:", raw_output)

        # Validate JSON output
        budget_data = json.loads(raw_output)
        return {"budget": budget_data}

    except json.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))
        raise HTTPException(
            status_code=500,
            detail="LLM returned invalid JSON. Please refine your input or contact support.",
        )
    except Exception as e:
        print("Unhandled Exception:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate budget: {str(e)}",
        )
