import os
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from utils.fetch_weather import preprocess_weather_data
from utils.embedding_utils import get_embedding

load_dotenv()

# Load API keys and environment details from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

openai.api_key = OPENAI_API_KEY

# Our index names
SUPPLY_CHAIN_INDEX = "chain-sense-index"
WEATHER_INDEX = "weather-data-index"
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Ensure supply chain index exists
if SUPPLY_CHAIN_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=SUPPLY_CHAIN_INDEX,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Ensure weather index exists
if WEATHER_INDEX not in pc.list_indexes().names():
    pc.create_index(
        name=WEATHER_INDEX,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Use the indexes
supply_chain_index = pc.Index(SUPPLY_CHAIN_INDEX)
weather_index = pc.Index(WEATHER_INDEX)

def retrieve_context(query, index, top_k=3):
    """
    Retrieve the most relevant contexts for a given query using Pinecone.
    Assumes that each match in the index has 'text' in its metadata.
    """
    query_embedding = get_embedding(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    contexts = [match['metadata']['text'] for match in results['matches']]
    return contexts

def retrieve_weather_context(query, top_k=3):
    """
    Retrieve relevant weather data from Pinecone based on the query.
    """
    return retrieve_context(query, weather_index, top_k)

def retrieve_supply_chain_context(query, top_k=3):
    """
    Retrieve relevant supply chain data from Pinecone based on the query.
    """
    return retrieve_context(query, supply_chain_index, top_k)

def generate_answer_with_weather(query, supply_chain_contexts, weather_contexts):
    """
    Generate an answer combining supply chain and weather contexts.
    """
    combined_context = "\n\n".join(supply_chain_contexts + weather_contexts)
    prompt = f"""
    You are a supply chain and weather expert. Use the following context to answer the question below.
    Only use the provided context to generate your response. Do not create or assume any additional scenarios
    or information that is not explicitly mentioned in the context.

    Context:
    {combined_context}

    Question: {query}

    Answer:
    """
    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message['content'].strip()

def answer_query_with_weather(query, location=None):
    """
    Answer a query by retrieving supply chain and weather contexts, then generating a response.
    If a location is provided, preprocess its weather data, store it temporarily in Pinecone,
    and then retrieve it.
    """
    # Retrieve supply chain context
    supply_chain_contexts = retrieve_supply_chain_context(query)
    
    # Retrieve weather context
    weather_contexts = []
    if location:
        preprocessed_weather = preprocess_weather_data(location)
        if preprocessed_weather:
            # Include text in metadata
            full_metadata = preprocessed_weather["metadata"]
            full_metadata["text"] = preprocessed_weather["text"]
            
            # Embed and store the weather data temporarily for this query
            temp_weather_embedding = get_embedding(preprocessed_weather['text'])
            weather_index.upsert(vectors=[
                {
                    "id": f"temp-{location}",
                    "values": temp_weather_embedding,
                    "metadata": full_metadata
                }
            ])
            # Retrieve weather context
            weather_contexts = retrieve_weather_context(query)

    # Generate the final answer
    answer = generate_answer_with_weather(query, supply_chain_contexts, weather_contexts)
    return answer



    # You are a supply chain and weather expert. Use the following context to answer the question below.
    # If the context does not explicitly mention how weather impacts the supply chain, infer logical impacts 
    # based on the provided weather conditions (e.g., temperature, wind speed, precipitation, etc.) and typical 
    # supply chain operations (e.g., transportation, storage, logistics, and delivery). Provide your reasoning.




# import os
# import openai
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv
# from utils.fetch_weather import preprocess_weather_data
# from utils.embedding_utils import get_embedding

# load_dotenv()

# # Load API keys and environment details from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")

# openai.api_key = OPENAI_API_KEY

# # Our index names
# SUPPLY_CHAIN_INDEX = "chain-sense-index"
# WEATHER_INDEX = "weather-data-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# # Initialize Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Check if supply chain index exists
# if SUPPLY_CHAIN_INDEX not in pc.list_indexes().names():
#     pc.create_index(
#         name=SUPPLY_CHAIN_INDEX,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"
#         )
#     )

# # Check if weather index exists
# if WEATHER_INDEX not in pc.list_indexes().names():
#     pc.create_index(
#         name=WEATHER_INDEX,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"
#         )
#     )

# # Use the indexes
# supply_chain_index = pc.Index(SUPPLY_CHAIN_INDEX)
# weather_index = pc.Index(WEATHER_INDEX)

# def retrieve_context(query, index, top_k=3):
#     """
#     Retrieve the most relevant contexts for a given query using Pinecone.
#     """
#     # Embed the query
#     query_embedding = get_embedding(query)
#     # Query Pinecone
#     results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#     # Extract the text from the top matches
#     contexts = [match['metadata']['text'] for match in results['matches']]
#     return contexts

# def retrieve_weather_context(query, top_k=3):
#     """
#     Retrieve relevant weather data from Pinecone based on the query.
#     """
#     return retrieve_context(query, weather_index, top_k)

# def retrieve_supply_chain_context(query, top_k=3):
#     """
#     Retrieve relevant supply chain data from Pinecone based on the query.
#     """
#     return retrieve_context(query, supply_chain_index, top_k)

# def generate_answer_with_weather(query, supply_chain_contexts, weather_contexts):
#     """
#     Generate an answer combining supply chain and weather contexts.
#     """
#     combined_context = "\n\n".join(supply_chain_contexts + weather_contexts)
#     prompt = f"""
#     You are a supply chain and weather expert. Use the following context to answer the question below.
#     If you don't know the answer, just say you don't know. Do not make up facts.

#     Context:
#     {combined_context}

#     Question: {query}

#     Answer:
#     """
#     response = openai.ChatCompletion.create(
#         model=LLM_MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )
#     return response.choices[0].message['content'].strip()

# def answer_query_with_weather(query, location=None):
#     """
#     Answer a query by retrieving supply chain and weather contexts, then generating a response.
#     """
#     # Retrieve supply chain context
#     supply_chain_contexts = retrieve_supply_chain_context(query)
    
#     # Retrieve weather context
#     weather_contexts = []
#     if location:
#         preprocessed_weather = preprocess_weather_data(location)
#         if preprocessed_weather:
#             # Embed and store the weather data temporarily for this query
#             temp_weather_embedding = get_embedding(preprocessed_weather['text'])
#             weather_index.upsert(vectors=[
#                 {
#                     "id": f"temp-{location}",
#                     "values": temp_weather_embedding,
#                     "metadata": preprocessed_weather["metadata"]
#                 }
#             ])
#             # Retrieve weather context
#             weather_contexts = retrieve_weather_context(query)

#     # Generate the final answer
#     answer = generate_answer_with_weather(query, supply_chain_contexts, weather_contexts)
#     return answer






#-correct - below code 

# import os
# import openai
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# load_dotenv()

# # Load API keys and environment details from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")  # Not needed with the new Pinecone API

# openai.api_key = OPENAI_API_KEY

# # Our index name
# INDEX_NAME = "chain-sense-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# # Initialize Pinecone
# pc = Pinecone(
#     api_key=PINECONE_API_KEY  # Replace with your API key variable
# )

# # Check if the index exists or create one if needed
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,  # Adjust this dimension to match your embeddings
#         metric="cosine",  # Use "cosine", "dotproduct", or "euclidean"
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-west-2"  # Replace with your Pinecone environment region
#         )
#     )

# # Use the index
# index = pc.Index(INDEX_NAME)

# def get_embedding(text):
#     """
#     Generate an embedding for a given text using OpenAI's embedding model.
#     """
#     response = openai.Embedding.create(
#         input=[text],
#         engine=EMBEDDING_MODEL
#     )
#     return response['data'][0]['embedding']

# def retrieve_context(query, top_k=3):
#     """
#     Retrieve the most relevant contexts for a given query using Pinecone.
#     """
#     # Embed the query
#     query_embedding = get_embedding(query)
#     # Query Pinecone
#     results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#     # Extract the text from the top matches
#     contexts = [match['metadata']['text'] for match in results['matches']]
#     return contexts

# def generate_answer(query, contexts):
#     """
#     Generate an answer using the LLM based on the given contexts.
#     """
#     # Prepare the prompt for the LLM
#     prompt = f"""
# You are a supply chain expert. Use the following context to answer the question below.
# If you don't know the answer, just say you don't know. Do not make up facts.

# Context:
# {contexts}

# Question: {query}

# Answer:
# """
#     response = openai.ChatCompletion.create(
#         model=LLM_MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )
#     return response.choices[0].message['content'].strip()

# def answer_query(query):
#     """
#     Answer a query by retrieving relevant contexts and generating a response.
#     """
#     # Get relevant context from Pinecone
#     contexts = retrieve_context(query)
#     combined_context = "\n\n".join(contexts)
#     # Generate the final answer
#     answer = generate_answer(query, combined_context)
#     return answer






# import os
# import openai
# import pinecone
# from dotenv import load_dotenv

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")

# openai.api_key = OPENAI_API_KEY

# # Our index name
# INDEX_NAME = "chain-sense-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# index = pinecone.Index(INDEX_NAME)

# def get_embedding(text):
#     response = openai.Embedding.create(
#         input=[text],
#         engine=EMBEDDING_MODEL
#     )
#     return response['data'][0]['embedding']

# def retrieve_context(query, top_k=3):
#     # Embed the query
#     query_embedding = get_embedding(query)
#     # Query Pinecone
#     results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#     # Extract the text from the top matches
#     contexts = [match['metadata']['text'] for match in results['matches']]
#     return contexts

# def generate_answer(query, contexts):
#     # Prepare the prompt for the LLM
#     prompt = f"""
# You are a supply chain expert. Use the following context to answer the question below.
# If you don't know the answer, just say you don't know. Do not make up facts.

# Context:
# {contexts}

# Question: {query}

# Answer:
# """
#     response = openai.ChatCompletion.create(
#         model=LLM_MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )
#     return response.choices[0].message['content'].strip()

# def answer_query(query):
#     # Get relevant context from Pinecone
#     contexts = retrieve_context(query)
#     combined_context = "\n\n".join(contexts)
#     # Generate the final answer
#     answer = generate_answer(query, combined_context)
#     return answer
