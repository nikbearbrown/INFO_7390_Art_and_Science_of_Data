import os
import json
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from utils.fetch_weather import preprocess_weather_data
from utils.embedding_utils import get_embedding

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure OpenAI API key is set
openai.api_key = OPENAI_API_KEY
if not openai.api_key:
    raise ValueError("OpenAI API key not set. Please check your environment variables or .env file.")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "weather-data-index"
if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creating index: {INDEX_NAME}")
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
else:
    print(f"Index '{INDEX_NAME}' already exists.")

index = pc.Index(INDEX_NAME)

def store_weather_data(location):
    """
    Stores weather data in Pinecone index.
    """
    print(f"Processing weather data for location: {location}")
    preprocessed_data = preprocess_weather_data(location)
    if not preprocessed_data:
        print(f"Failed to preprocess weather data for {location}")
        return

    # Include 'text' in metadata
    full_metadata = preprocessed_data["metadata"]
    full_metadata["text"] = preprocessed_data["text"]

    # Generate embedding
    embedding = get_embedding(preprocessed_data["text"])
    if not embedding:
        print(f"Failed to generate embedding for {location}")
        return

    # Upsert data into Pinecone
    try:
        index.upsert(
            vectors=[
                {
                    "id": f"weather-{preprocessed_data['metadata']['location']}",
                    "values": embedding,
                    "metadata": full_metadata
                }
            ]
        )
        print(f"Weather data for {location} stored successfully.")
    except Exception as e:
        print(f"Error upserting data for {location}: {e}")

def batch_store_weather_data(locations):
    """
    Processes and stores weather data for a batch of locations.
    """
    for location in locations:
        store_weather_data(location)

if __name__ == "__main__":
    # Example usage
    locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "Fort Worth", "Columbus", "Indianapolis",
        "Charlotte", "San Francisco", "Seattle", "Denver", "Washington",
        "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
        "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
        "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
        "Mesa", "Kansas City", "Atlanta", "Omaha", "Colorado Springs",
        "Raleigh", "Miami", "Virginia Beach", "Oakland", "Minneapolis",
        "Tulsa", "Arlington", "Tampa", "New Orleans", "Wichita", 
        "Cleveland", "Bakersfield", "Aurora", "Anaheim", "Honolulu",
        "Santa Ana", "Riverside", "Corpus Christi", "Lexington", "Stockton",
        "Henderson", "Saint Paul", "St. Louis", "Cincinnati", "Pittsburgh"]
    
    batch_store_weather_data(locations)








# import os
# import json
# import openai
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv
# from utils.fetch_weather import preprocess_weather_data
# from utils.embedding_utils import get_embedding

# # Load environment variables
# load_dotenv()
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Ensure OpenAI API key is set
# openai.api_key = OPENAI_API_KEY
# if not openai.api_key:
#     raise ValueError("OpenAI API key not set. Please check your environment variables or .env file.")

# # Initialize Pinecone client
# pc = Pinecone(api_key=PINECONE_API_KEY)

# INDEX_NAME = "weather-data-index"
# if INDEX_NAME not in pc.list_indexes().names():
#     print(f"Creating index: {INDEX_NAME}")
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )
# else:
#     print(f"Index '{INDEX_NAME}' already exists.")

# index = pc.Index(INDEX_NAME)

# def store_weather_data(location):
#     """
#     Stores weather data in Pinecone index.
#     """
#     print(f"Processing weather data for location: {location}")
#     preprocessed_data = preprocess_weather_data(location)
#     if not preprocessed_data:
#         print(f"Failed to preprocess weather data for {location}")
#         return

#     # Generate embedding
#     embedding = get_embedding(preprocessed_data["text"])
#     if not embedding:
#         print(f"Failed to generate embedding for {location}")
#         return

#     # Upsert data into Pinecone
#     try:
#         index.upsert(
#             vectors=[
#                 {
#                     "id": f"weather-{preprocessed_data['metadata']['location']}",
#                     "values": embedding,
#                     "metadata": preprocessed_data["metadata"]
#                 }
#             ]
#         )
#         print(f"Weather data for {location} stored successfully.")
#     except Exception as e:
#         print(f"Error upserting data for {location}: {e}")

# def batch_store_weather_data(locations):
#     """
#     Processes and stores weather data for a batch of locations.
#     """
#     for location in locations:
#         store_weather_data(location)

# if __name__ == "__main__":
#     # Example usage
#     locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
#     batch_store_weather_data(locations)



#-correct below

# import os
# import json
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv
# from utils.fetch_weather import fetch_weather

# # Load environment variables
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")

# # Initialize Pinecone client
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Constants
# INDEX_NAME = "weather-data-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# WEATHER_DATA_PATH = os.path.join("data", "weather_data.json")

# def create_index_if_not_exists():
#     """Create a Pinecone index if it doesn't exist."""
#     existing_indexes = pc.list_indexes().names()
#     if INDEX_NAME not in existing_indexes:
#         print(f"Creating index: {INDEX_NAME}")
#         pc.create_index(
#             name=INDEX_NAME,
#             dimension=1536,
#             metric="cosine",
#             spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Adjust to your region
#         )
#     else:
#         print(f"Index '{INDEX_NAME}' already exists.")

# def fetch_and_store_weather_data():
#     """Fetch weather data and store it in weather_data.json."""
#     locations = ["San Francisco", "New York", "London", "Tokyo"]  # Add desired locations
#     weather_data = []

#     for location in locations:
#         print(f"Fetching weather data for {location}...")
#         data = fetch_weather(location)
#         if "error" not in data:
#             weather_data.append(data)
#         else:
#             print(f"Error fetching data for {location}: {data['error']}")

#     with open(WEATHER_DATA_PATH, "w") as f:
#         json.dump(weather_data, f, indent=4)

# def index_weather_data():
#     """Index weather data from weather_data.json into Pinecone."""
#     if not os.path.exists(WEATHER_DATA_PATH) or os.path.getsize(WEATHER_DATA_PATH) == 0:
#         print("Weather data file is empty. Fetching new data...")
#         fetch_and_store_weather_data()

#     with open(WEATHER_DATA_PATH, "r") as f:
#         weather_data = json.load(f)

#     # Connect to the index
#     index = pc.Index(name=INDEX_NAME)

#     vectors = []
#     for i, data in enumerate(weather_data):
#         text = (
#             f"Weather in {data['location']} (lat: {data['latitude']}, "
#             f"lon: {data['longitude']}): {data['description']}, "
#             f"temperature: {data['temperature']}°C, wind speed: {data['wind_speed']} km/h"
#         )
#         embedding = get_embedding(text)
#         if embedding:
#             vectors.append((str(i), embedding, {"text": text, **data}))

#     print(f"Upserting {len(vectors)} weather data vectors to Pinecone...")
#     index.upsert(vectors)
#     print("Indexing complete.")

# def get_embedding(text):
#     """Fetch embeddings from OpenAI."""
#     import openai
#     openai.api_key = OPENAI_API_KEY
#     try:
#         response = openai.Embedding.create(input=[text], engine=EMBEDDING_MODEL)
#         return response["data"][0]["embedding"]
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None

# if __name__ == "__main__":
#     create_index_if_not_exists()
#     index_weather_data()















# import os
# import json
# import openai
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Set API keys and Pinecone configuration
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = "us-east-1"  # Update based on your Pinecone region (change if needed)
# INDEX_NAME = "chain-sense-weather-index"

# openai.api_key = OPENAI_API_KEY

# # Initialize Pinecone client
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Check if the index exists, or create it
# if INDEX_NAME not in [index['name'] for index in pc.list_indexes()]:
#     print(f"Creating index: {INDEX_NAME}")
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,  # Match the embedding size of text-embedding-ada-002
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV)
#     )
# else:
#     print(f"Index '{INDEX_NAME}' already exists.")

# # Connect to the index
# index = pc.Index(name=INDEX_NAME)

# # Path to weather data
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, "data", "weather_data.json")


# def get_embedding(text):
#     """Generate embeddings using OpenAI."""
#     response = openai.Embedding.create(
#         input=[text],
#         engine="text-embedding-ada-002"
#     )
#     return response['data'][0]['embedding']


# def index_weather_data():
#     """Process weather data and upsert it into Pinecone."""
#     # Load weather data from JSON
#     with open(DATA_PATH, "r") as f:
#         weather_data = json.load(f)

#     vectors = []
#     for i, weather in enumerate(weather_data):
#         # Create a descriptive text string for embedding
#         text = (
#             f"Weather in {weather['location']}: {weather['description']}, "
#             f"Temperature: {weather['temperature']}°C, Wind Speed: {weather['wind_speed']} km/h."
#         )
#         embedding = get_embedding(text)
#         vectors.append((f"weather-{i}", embedding, {"text": text}))

#     # Upsert vectors into Pinecone
#     try:
#         index.upsert(vectors=vectors)
#         print(f"Successfully indexed {len(vectors)} weather data points.")
#     except Exception as e:
#         print(f"Error during upsert: {e}")


# if __name__ == "__main__":
#     index_weather_data()






# # import json
# # from utils.fetch_weather import fetch_weather
# # from rag_pipeline import get_embedding
# # import pinecone
# # import os

# # # Load environment variables
# # from dotenv import load_dotenv
# # load_dotenv()

# # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# # PINECONE_ENV = os.getenv("PINECONE_ENV")
# # INDEX_NAME = "weather-data-index"

# # pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# # if INDEX_NAME not in pinecone.list_indexes():
# #     pinecone.create_index(name=INDEX_NAME, dimension=1536)

# # index = pinecone.Index(INDEX_NAME)

# # def preprocess_weather_data(location):
# #     """
# #     Fetch, process, and embed weather data for the specified location.
# #     """
# #     # Fetch raw weather data
# #     weather = fetch_weather(location)
# #     if "error" in weather:
# #         return weather

# #     # Prepare text for embedding
# #     weather_text = (
# #         f"Weather in {weather['location']}: Temperature is {weather['temperature']}°C with "
# #         f"wind speed of {weather['wind_speed']} km/h. Description: {weather['description']}."
# #     )

# #     # Generate embedding
# #     embedding = get_embedding(weather_text)

# #     # Store in Pinecone
# #     metadata = {"location": weather["location"], "text": weather_text}
# #     index.upsert([(location, embedding, metadata)])

# #     return weather_text
