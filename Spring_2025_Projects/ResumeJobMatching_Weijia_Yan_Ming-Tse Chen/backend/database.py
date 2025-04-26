import os
import json
import time
from typing import List, Tuple, Dict
from tqdm import tqdm
from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec


# Load API key from .env
def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing PINECONE_API_KEY in .env")
    return api_key


# Load JSONL file with embedded vectors
def load_jsonl(path: str) -> List[Dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    items = []
    with open(path, "r") as f:
        for i, line in enumerate(f):
            obj = json.loads(line)
            if "text" not in obj or "embedding" not in obj:
                raise ValueError(f"Line {i} missing required fields.")
            items.append(obj)
    print(f"Loaded {len(items)} items from {path}")
    return items


# Initialize Pinecone client
def setup_pinecone(api_key: str) -> Pinecone:
    pc = Pinecone(api_key=api_key)
    print("Pinecone client initialized.")
    return pc


# Create index if it doesn't exist
def ensure_index(pc: Pinecone, index_name: str, dimension: int):
    if index_name not in pc.list_indexes().names():
        print(f"Creating index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        while True:
            status = pc.describe_index(index_name).status["ready"]
            if status:
                break
            print("Waiting for index to be ready...")
            time.sleep(2)
    else:
        print(f"Index '{index_name}' already exists.")


# Convert items to Pinecone format
def generate_payload(items: List[Dict]) -> List[Tuple[str, List[float], Dict]]:
    vectors = []
    for i, item in enumerate(items):
        vector_id = f"vec-{i}"
        embedding = item["embedding"]
        metadata = {
            "text": item.get("text", ""),
            "label": item.get("label", ""),
            "source": item.get("source", "")
        }
        vectors.append((vector_id, embedding, metadata))
    return vectors


# Upload vectors in batches
def batch_upload(index, vectors: List[Tuple[str, List[float], Dict]], batch_size: int = 100):
    total = len(vectors)
    for i in tqdm(range(0, total, batch_size), desc="Uploading"):
        end = min(i + batch_size, total)
        batch = vectors[i:end]
        try:
            index.upsert(vectors=batch)
        except Exception as e:
            print(f"Upload failed at batch {i}-{end}: {e}")
            continue
    print(f"Uploaded {total} vectors to index.")


# End-to-end pipeline
def embed_upload_pipeline(data_path: str, index_name: str, dimension: int = 384):
    api_key = load_api_key()
    pc = setup_pinecone(api_key)
    ensure_index(pc, index_name, dimension)

    data = load_jsonl(data_path)
    vectors = generate_payload(data)

    index = pc.Index(index_name)
    batch_upload(index, vectors)

    stats = index.describe_index_stats()
    print(f"Final index vector count: {stats.get('total_vector_count', 0)}")


# Entry point
if __name__ == "__main__":
    DATA_PATH = "../data/processed/embedded_data.jsonl"
    INDEX_NAME = "career-navigator-index"

    try:
        embed_upload_pipeline(DATA_PATH, INDEX_NAME)
    except Exception as e:
        print(f"Fatal error: {e}")
