# backend/retrieval.py

import os
import json
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


def load_config():
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY is missing in .env")
    return api_key


def init_embedder(model_name: str = "all-MiniLM-L6-v2"):
    print(f"Loading embedding model '{model_name}'...")
    return SentenceTransformer(model_name)


def init_pinecone_index(api_key: str, index_name: str) -> Tuple[Pinecone, any]:
    pc = Pinecone(api_key=api_key)
    if index_name not in pc.list_indexes().names():
        raise ValueError(f"Index '{index_name}' not found in Pinecone project.")
    index = pc.Index(index_name)
    return pc, index


def search_index(index, embed_model, query: str, category: str = "all", top_k: int = 5) -> List[Dict]:
    vector = embed_model.encode(query).tolist()

    if category == "resume":
        filter_expr = {"source": {"$eq": "resume"}}
    elif category == "job":
        filter_expr = {"source": {"$eq": "job"}}
    else:
        filter_expr = None

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        filter=filter_expr
    )
    return results["matches"]


def format_result(match: Dict, rank: int) -> str:
    metadata = match.get("metadata", {})
    text = metadata.get("text", "")[:500].replace("\n", " ")
    label = metadata.get("label", "")
    source = metadata.get("source", "")
    score = round(match["score"], 4)
    return (
        f"Result {rank}:\n"
        f"Score: {score}\n"
        f"Label: {label}\n"
        f"Source: {source}\n"
        f"Content Preview:\n{text}...\n"
        f"{'-' * 60}"
    )


def retrieve_pipeline(index_name: str, user_query: str, category: str = "all", top_k: int = 5):
    api_key = load_config()
    embed_model = init_embedder()
    pc, index = init_pinecone_index(api_key, index_name)

    print(f"Searching top {top_k} matches for query: '{user_query}' (category: {category})")
    matches = search_index(index, embed_model, user_query, category, top_k)

    if not matches:
        print("No matches found.")
        return

    for i, match in enumerate(matches, 1):
        print(format_result(match, i))


def interactive_cli(index_name: str):
    print("Welcome to Career Navigator Search.")
    print("You can search by query and specify category: 'resume', 'job', or 'all'. Type 'exit' to quit.")
    while True:
        try:
            query = input("\nEnter search query: ").strip()
            if query.lower() in {"exit", "quit"}:
                print("Exiting.")
                break

            category = input("Enter category (resume/job/all): ").strip().lower()
            if category not in {"resume", "job", "all"}:
                print("Invalid category. Using default: all.")
                category = "all"

            retrieve_pipeline(index_name, query, category, top_k=5)

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break


if __name__ == "__main__":
    INDEX_NAME = "career-navigator-index"
    interactive_cli(INDEX_NAME)
