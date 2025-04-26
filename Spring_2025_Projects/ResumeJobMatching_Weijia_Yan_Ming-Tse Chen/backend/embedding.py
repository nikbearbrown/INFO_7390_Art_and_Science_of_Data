# backend/embedding.py

import os
import time
import json
import pandas as pd
from tqdm import tqdm
from typing import List
from sentence_transformers import SentenceTransformer

# Constants
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 100

# Load model once
model = SentenceTransformer(EMBED_MODEL)

def filter_by_length(data: pd.DataFrame, column: str, min_chars: int = 100) -> pd.DataFrame:
    """Filter short text entries."""
    data["char_length"] = data[column].str.len()
    return data[data["char_length"] >= min_chars].copy()

def batch_embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using sentence-transformers."""
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()

def embed_dataframe(df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
    """Embed entire dataframe in chunks."""
    df = df.reset_index(drop=True)
    all_embeddings = []

    for i in range(0, len(df), CHUNK_SIZE):
        batch = df.iloc[i:i + CHUNK_SIZE]
        print(f"Embedding chunk {i} to {i + len(batch)}")
        batch_embeddings = batch_embed_texts(batch[text_column].tolist())
        all_embeddings.extend(batch_embeddings)

    df["embedding"] = all_embeddings
    return df

def save_embeddings_to_jsonl(df: pd.DataFrame, output_path: str) -> None:
    """Save embeddings to .jsonl format."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        for _, row in df.iterrows():
            json.dump({
                "text": row["text"],
                "label": row["label"],
                "source": row["source"],
                "embedding": row["embedding"]
            }, f)
            f.write("\n")
    print(f"Embeddings saved to: {output_path}")

def embed_and_save_pipeline(input_path: str, output_path: str) -> None:
    """Load data, embed, save result."""
    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    df = filter_by_length(df, "text")
    print(f"{len(df)} rows remain after filtering short texts")

    print(f"Generating embeddings using: {EMBED_MODEL}")
    df = embed_dataframe(df, text_column="text")

    save_embeddings_to_jsonl(df, output_path)

if __name__ == "__main__":
    INPUT_FILE = "../data/processed/merged_cleaned_dataset.csv"
    OUTPUT_FILE = "../data/processed/embedded_data.jsonl"

    embed_and_save_pipeline(INPUT_FILE, OUTPUT_FILE)
