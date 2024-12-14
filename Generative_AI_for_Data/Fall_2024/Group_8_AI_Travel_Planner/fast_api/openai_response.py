import os
from dotenv import load_dotenv
import logging
from pinecone import Pinecone, ServerlessSpec
import openai
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_log = logging.getLogger(__name__)
# Initialize OpenAI

# API keys and environment configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


youtube_index_name = "youtube-query-index"
DIMENSION = 1536
METRIC = "cosine"

# Ensure all required API keys are set
if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT or not OPENAI_API_KEY:
    logging.error("API keys missing in environment variables. Check your .env file.")
    exit(1)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    logging.info("Pinecone initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing Pinecone: {e}")
    exit(1)

# Check if the index exists, otherwise create it
if youtube_index_name not in pc.list_indexes().names():
    logging.info(f"Index '{youtube_index_name}' does not exist. Creating it...")
    try:
        pc.create_index(
            name=youtube_index_name,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        logging.info(f"Index '{youtube_index_name}' created successfully.")
    except Exception as e:
        logging.error(f"Failed to create Pinecone index: {e}")
        exit(1)
else:
    logging.info(f"Index '{youtube_index_name}' already exists.")

# Connect to the index
try:
    youtube_index = pc.Index(youtube_index_name)
    logging.info(f"Connected to Pinecone index '{youtube_index_name}'.")
except Exception as e:
    logging.error(f"Error connecting to Pinecone index: {e}")
    exit(1)

# Function to embed user query using OpenAI's text-embedding-ada-002 model
def embed_query(query):
    try:
        response = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']
    except Exception as e:
        logging.error(f"Error generating embedding for query: {e}")
        return None

def is_travel_related_gpt(query):
    """
    Uses OpenAI's GPT model to determine if the query is travel-related.
    """
    try:
        # Define the system role and user prompt
        messages = [
            {"role": "system", "content": "You are an assistant that determines if a query is related to travel."},
            {"role": "user", "content": f"Is the following query related to travel? Respond with 'Yes' or 'No' only.\n\nQuery: {query}"}
        ]
        
        # Generate response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        # Extract and process the response content
        answer = response.choices[0].message.content.strip().lower()
        logging.info(f"Query relevance determined: {answer}")
        return answer == "yes"
    except Exception as e:
        logging.error(f"Error while checking query relevance: {e}")
        return False


def query_pinecone_with_threshold(query_vector, top_k=5, threshold=0.75):
    """
    Query Pinecone for the top k matches and filter by relevance threshold.
    """
    try:
        # Query Pinecone for matches
        result = youtube_index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
        logging.info(f"Fetched {len(result['matches'])} matches from Pinecone.")
        
        # Apply threshold filtering
        filtered_matches = [match for match in result['matches'] if match['score'] >= threshold]
        
        if not filtered_matches:
            logging.warning("No matches exceeded the relevance threshold.")
        else:
            logging.info(f"{len(filtered_matches)} matches passed the relevance threshold of {threshold}.")
        return filtered_matches
    except Exception as e:
        logging.error(f"Error querying Pinecone: {e}")
        return []

def generate_response_with_relevant_data(query, relevant_matches):
    """
    Generate a response using only the relevant matches filtered by similarity.
    """
    if not relevant_matches:
        return "Sorry, I couldn't find relevant information for your query. Please try again with more details."

    # Prepare context from the filtered matches
    context = "\n".join([
        f"Text: {match['metadata']['text']} (Source: {match['metadata'].get('title', 'Unknown')})"
        for match in relevant_matches
    ])
    
    # Define the messages for OpenAI's ChatCompletion API
    messages = [
        {
            "role": "system",
            "content": """
You are an expert travel assistant. Your job is to create detailed, engaging, and personalized travel itineraries for users based on the provided context and query.

When crafting a response:
- Include a well-structured itinerary with clear days and activities.
- Mention must-visit attractions, local landmarks, and hidden gems.
- Suggest the best stores for shopping, including local markets, luxury boutiques, and specialty stores relevant to the destination.
- Recommend restaurants or cafes for meals, including breakfast, lunch, and dinner, highlighting local cuisines.
- Add tips for efficient travel, such as transportation options, best times to visit attractions, and any special considerations (e.g., tickets, attire).
- Include brief cultural insights or unique experiences that enhance the trip.
- Use an engaging, friendly, and professional tone.

If the user asks for an itinerary for a specific duration (e.g., "3 days in Paris"), structure your response by days:
- Day 1: Morning, afternoon, and evening activities.
- Day 2: Repeat with a similar structure.
- Add extra details for each activity (e.g., timings, location, and why it's worth visiting).
            """
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}\n\nProvide a detailed and accurate response."}
    ]

    try:
        # Generate the response using OpenAI's ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4",  # Specify GPT model
            messages=messages,
            max_tokens=1500,  # Adjust token limit based on your requirements
            temperature=0.7  # Creativity level
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating response from GPT: {e}")
        return "Sorry, there was an error generating your response."


def fetch_and_generate_response(query, top_k=5, threshold=0.75):
    """
    Fetch relevant data from Pinecone and use GPT to craft a response.
    """
    # Step 1: Embed the query
    query_vector = embed_query(query)
    if query_vector is None:
        return "Failed to generate embedding for the query."

    # Step 2: Fetch and filter results from Pinecone
    relevant_matches = query_pinecone_with_threshold(query_vector, top_k=top_k, threshold=threshold)
    
    # Step 3: Generate a response using the filtered data
    return generate_response_with_relevant_data(query, relevant_matches)

def main():
    query = input("Enter your travel-related question: ")
    
    if not is_travel_related_gpt(query):
        print("This system only answers travel-related questions. Please try again with a travel-focused query.")
        return
    
    response = fetch_and_generate_response(query, top_k=5, threshold=0.75)
    print("\nGPT Response:\n")
    print(response)

# Run the main script
if __name__ == "__main__":
    main()