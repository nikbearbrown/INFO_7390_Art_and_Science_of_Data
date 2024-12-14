import json
import logging
from typing import Optional, List
from pydantic import BaseModel, ValidationError
from datetime import datetime
from fastapi import HTTPException
from openai import OpenAI
from pinecone import Pinecone
import tiktoken
from functools import lru_cache
from hashlib import sha256
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
    get_db_connection,
    get_current_username,
    get_user,
    create_user,
    inspect_index,
    YouTubeVideoResponse,
    Module,
    Plan,
    pool,
)  
from config import (
    SNOWFLAKE_CONFIG,
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    YOUTUBE_API_KEY,
    INDEX_NAME,
    YOUTUBE_INDEX,
    DIMENSION,
    METRIC,
    CLOUD_PROVIDER,
    REGION,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    client,
    pc,
    youtube,
    index,
    youtube_index,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache for query results and embeddings
cached_chunks = {}
cached_embeddings = {}

# Function to get embeddings with caching
@lru_cache(maxsize=2000)
def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Fetch embedding for the given text, with caching."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(text)
        MAX_TOKENS = 8192

        if len(tokens) > MAX_TOKENS:
            text = encoding.decode(tokens[:MAX_TOKENS])

        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to get embedding for text: {text[:50]}... Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate embedding.")

def retrieve_cached_chunks(query_embedding):
    """Retrieve cached chunks for a semantically similar query embedding."""
    if not cached_embeddings:
        logger.info("Cache is empty. No cached chunks available.")
        return None

    # Calculate similarity with cached embeddings
    cached_keys = list(cached_embeddings.keys())
    cached_vectors = np.array([cached_embeddings[key] for key in cached_keys])
    similarities = cosine_similarity([query_embedding], cached_vectors)
    max_sim_index = np.argmax(similarities)

    if similarities[0][max_sim_index] > 0.9:  # Similarity threshold
        similar_key = cached_keys[max_sim_index]
        logger.info(f"Cache hit for query. Similarity: {similarities[0][max_sim_index]}")
        return cached_chunks.get(similar_key, None)

    logger.info("Cache miss. No similar chunks found.")
    return None

def cache_chunks(query_embedding, chunks):
    """Cache retrieved chunks using a hash of the query embedding."""
    query_hash = sha256(np.array(query_embedding).tobytes()).hexdigest()
    logger.info(f"Caching new chunks with hash: {query_hash}")
    cached_chunks[query_hash] = chunks
    cached_embeddings[query_hash] = query_embedding

def retrieve_information(user_query: str) -> Optional[str]:
    """Retrieve relevant information from the index based on the user query."""
    try:
        query_embedding = get_embedding(user_query)

        # Check for similar cached chunks
        cached_results = retrieve_cached_chunks(query_embedding)
        if cached_results:
            return cached_results

        # Query the vector database if no cached results are found
        results = index.query(vector=query_embedding, top_k=4, include_metadata=True)

        RELEVANCE_THRESHOLD = 0.8
        relevant_matches = [
            match for match in results["matches"] if match.get("score", 0) >= RELEVANCE_THRESHOLD
        ]

        if not relevant_matches:
            logger.info(f"No relevant matches found for query: {user_query}")
            return None

        context_info = " ".join([
            f"Chunk ID: {match['metadata'].get('chunk_id', 'Unknown')}. Text: {match['metadata'].get('text', '').strip()}"
            for match in relevant_matches
        ])

        # Cache the retrieved chunks
        cache_chunks(query_embedding, context_info)

        return context_info
    except Exception as e:
        logger.error(f"Error retrieving information for query: {user_query}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving information.")

def generate_plan(user_query, context_info, current_plan=None):
    try:
        if not context_info and not current_plan:
            return "No relevant information found in the Knowledge Base"

        system_prompt = (
            "You are a highly skilled assistant specializing in crafting structured and actionable MVP-style JSON learning plans that inspire users to learn and achieve their goals. "
            "Your plans should strike a balance between brevity and depth, providing clear and engaging content that motivates users to progress. "
            "Descriptions should be intellectual yet accessible, with relatable examples to demonstrate real-world applications and outcomes. "
            "Each learning plan should include:\n"
            "- A concise, compelling title that encapsulates the learning journey.\n"
            "- A clear and motivational objective outlining what the user will accomplish, written in an approachable and inspiring manner.\n"
            "- Key topics broken into digestible concepts to serve as milestones for learning progress.\n"
            "- Step-by-step modules with detailed yet exciting descriptions that highlight the value, relevance, and potential real-world impact of each step. Use relatable examples to illustrate key concepts and outcomes.\n"
            "- A measurable and inspiring expected outcome to give the user a sense of achievement and direction upon completing the plan.\n"
            "If updating an existing plan, carefully refine the relevant sections based on the user's query while preserving the overall structure and coherence of the plan. "
            "Strictly return a valid JSON output only. Do not include any introductory text, explanations, or comments. The response should consist solely of the JSON structure in this format:\n"
            "{\n"
            '  "Title": "An engaging and concise title for the learning plan",\n'
            '  "Objective": "A clear, inspiring summary of what the user will achieve",\n'
            '  "KeyTopics": ["Key topic 1", "Key topic 2", "Key topic 3"],\n'
            '  "Modules": [\n'
            '    {"module": 1, "title": "Catchy module title", "description": "A motivating, easy-to-read, and intellectually stimulating description that highlights the value of this module. Include a relatable example to showcase its practical application."},\n'
            '    {"module": 2, "title": "Another engaging module title", "description": "An actionable, detailed, and exciting description that keeps users interested and demonstrates the real-world impact of this module through examples."},\n'
            "    ...\n"
            "  ],\n"
            '  "ExpectedOutcome": "A clear, measurable, and inspiring outcome to help users stay focused and motivated."\n'
            "}"
            "Focus on providing content that is practical, motivating, and relatable while ensuring the JSON structure is complete, valid, and error-free. Tailor each plan to the user's query to make the learning journey personal and impactful. Ensure that the output contains only the JSON and nothing else."
        )

        if current_plan:
            current_plan_text = json.dumps(current_plan, indent=2)
            user_prompt = (
                f"Here is the current learning plan:\n{current_plan_text}\n\n"
                f"User Query: {user_query}\n"
                "Update the learning plan based on the query. Modify only the relevant sections (e.g., adjust focus, add emphasis, or refine topics). "
                "Ensure that the updated plan reflects the user's request while retaining the original structure and relevant parts."
            )
        else:
            user_prompt = (
                f"User Query: {user_query}\nContext: {context_info}\n"
                "Create a new structured learning plan based on the query and context."
            )

        plan_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        )

        plan_content = plan_response.choices[0].message.content

        plan_content = plan_content.replace(",\n  ]", "\n  ]").replace(",\n}", "\n}")  # Fix invalid JSON

        return plan_content
    except Exception as e:
        return '{"error": "Plan generation failed due to an internal error."}'

def validate_and_clean_json(response_text: str) -> Optional[dict]:
    try:
        response_json = json.loads(response_text)
        plan = Plan(**response_json)
        return plan.dict()
    except (ValidationError, json.JSONDecodeError) as e:
        return None

def summarize_plan(plan: dict) -> str:
    """Summarize the given learning plan."""
    try:
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that creates simple, logical, and professional summaries of learning plans. "
                        "The output should be concise, focused, and practical. Avoid lists or unnecessary detail."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Learning Plan: {json.dumps(plan)}\n"
                        "Summarize the learning plan into a practical and logical overview."
                    )
                },
            ]
        )
        summary = summary_response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error(f"Failed to summarize plan: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to summarize plan.")
