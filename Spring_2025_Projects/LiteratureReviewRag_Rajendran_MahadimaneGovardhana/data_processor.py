import os
import json
import requests
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
from dotenv import load_dotenv
import chromadb

# Load environment variables
load_dotenv()

# Constants
BATCH_SIZE = 100  # Process in batches to avoid memory issues
CHROMA_PERSIST_DIR = "data/chroma_db"
COLLECTION_NAME = "literature-review-assistant"

def download_arxiv_dataset(num_papers=1000):
    """
    Download a sample dataset of arXiv papers.
    Returns a pandas DataFrame with paper information.
    """
    print("Downloading arXiv dataset...")
    
    # We'll use the arXiv API to get some sample papers
    # Using a more robust approach this time
    
    base_url = "http://export.arxiv.org/api/query?"
    query = "search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results="
    
    try:
        response = requests.get(f"{base_url}{query}{num_papers}")
        response.raise_for_status()  # Raise an exception for bad status codes
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        # Fall back to using sample data
        return create_sample_dataset()
    
    # Try to parse the XML response
    papers = []
    try:
        entries = response.text.split("<entry>")[1:]
        
        for i, entry in enumerate(entries):
            try:
                # Use safer extraction with defaults
                title = extract_field(entry, "<title>", "</title>", "Untitled Paper")
                abstract = extract_field(entry, "<summary>", "</summary>", "No abstract available")
                id_raw = extract_field(entry, "<id>", "</id>", f"sample_id_{i}")
                
                # Extract paper ID from the full URL
                if "/" in id_raw:
                    paper_id = id_raw.split("/")[-1]
                else:
                    paper_id = id_raw
                
                # Get authors - safer approach
                authors = []
                if "<author>" in entry:
                    authors_raw = entry.split("<author>")[1:]
                    for author_raw in authors_raw:
                        if "<n>" in author_raw:
                            author = extract_field(author_raw, "<n>", "</n>", "Unknown Author")
                            authors.append(author)
                
                # Ensure we have at least one author
                if not authors:
                    authors = ["Unknown Author"]
                
                # Get categories
                categories = []
                if "<category term=" in entry:
                    categories_raw = entry.split("<category term=")
                    for cat_raw in categories_raw[1:]:
                        if '"' in cat_raw:
                            category = cat_raw.split('"')[1]
                            categories.append(category)
                
                # Get date
                date = extract_field(entry, "<published>", "</published>", "Unknown Date")
                
                papers.append({
                    "id": paper_id,
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "categories": categories,
                    "date": date,
                    "source": "arXiv"
                })
                
                if i % 10 == 0:
                    print(f"Processed {i+1}/{len(entries)} entries")
                
            except Exception as e:
                print(f"Error parsing entry {i}: {str(e)}")
                continue
        
    except Exception as e:
        print(f"Error processing arXiv response: {e}")
        # Fall back to using sample data if parsing fails
        return create_sample_dataset()
    
    if not papers:
        print("No papers were successfully parsed. Using sample data instead.")
        return create_sample_dataset()
    
    print(f"Successfully parsed {len(papers)} papers from arXiv.")
    return pd.DataFrame(papers)

def extract_field(text, start_tag, end_tag, default=""):
    """Safely extract a field from XML-like text"""
    try:
        if start_tag in text and end_tag in text:
            start = text.index(start_tag) + len(start_tag)
            end = text.index(end_tag, start)
            return text[start:end].strip()
    except Exception:
        pass
    return default

def create_sample_dataset():
    """Create a sample dataset when the arXiv API fails"""
    print("Creating sample dataset...")
    
    # Create some dummy papers for demonstration
    sample_papers = [
        {
            "id": "2304.12345",
            "title": "Advances in Transformer Models for NLP",
            "abstract": "This paper explores recent advancements in transformer architecture for natural language processing tasks. We present a novel approach to attention mechanisms that improves performance on benchmark datasets while reducing computational complexity.",
            "authors": ["Jane Smith", "John Doe"],
            "categories": ["cs.CL", "cs.AI"],
            "date": "2023-04-15",
            "source": "Sample Data"
        },
        {
            "id": "2305.67890",
            "title": "Reinforcement Learning in Robotic Applications",
            "abstract": "We present a comprehensive survey of reinforcement learning algorithms applied to robotic control systems. The paper examines both model-based and model-free approaches, with particular emphasis on sample efficiency and transfer learning capabilities in real-world scenarios.",
            "authors": ["Alex Johnson", "Maria Garcia"],
            "categories": ["cs.RO", "cs.AI", "cs.LG"],
            "date": "2023-05-22",
            "source": "Sample Data"
        },
        {
            "id": "2306.54321",
            "title": "Graph Neural Networks for Recommendation Systems",
            "abstract": "This paper proposes a novel graph neural network architecture specifically designed for recommendation systems. By incorporating both user-item interactions and content features into a heterogeneous graph, our model achieves state-of-the-art performance on multiple recommendation benchmarks.",
            "authors": ["Wei Zhang", "Sarah Brown"],
            "categories": ["cs.IR", "cs.LG"],
            "date": "2023-06-10",
            "source": "Sample Data"
        },
        {
            "id": "2307.13579",
            "title": "Federated Learning: Challenges and Opportunities",
            "abstract": "We explore the current challenges in federated learning including communication efficiency, privacy preservation, and model personalization. The paper proposes several techniques to address these issues and evaluates them on distributed datasets across multiple domains.",
            "authors": ["David Wilson", "Emma Lee"],
            "categories": ["cs.DC", "cs.LG", "cs.CR"],
            "date": "2023-07-05",
            "source": "Sample Data"
        },
        {
            "id": "2308.97531",
            "title": "Ethical Considerations in AI for Healthcare",
            "abstract": "This paper discusses the ethical challenges that arise when deploying AI systems in healthcare settings. We analyze issues related to bias, fairness, transparency, and accountability, presenting a framework for responsible AI development in medical applications.",
            "authors": ["Michael Chen", "Olivia Taylor"],
            "categories": ["cs.AI", "cs.CY"],
            "date": "2023-08-18",
            "source": "Sample Data"
        },
        {
            "id": "2309.24680",
            "title": "Comparative Analysis of Supervised and Unsupervised Learning for Image Classification",
            "abstract": "We present a systematic comparison of supervised and unsupervised learning approaches for image classification tasks. The study evaluates performance across multiple datasets, with varying levels of labeled data availability, and analyzes the computational requirements of each approach.",
            "authors": ["Robert Anderson", "Jennifer Moore"],
            "categories": ["cs.CV", "cs.LG"],
            "date": "2023-09-30",
            "source": "Sample Data"
        },
        {
            "id": "2310.11223",
            "title": "Large Language Models for Code Generation",
            "abstract": "This paper examines the capabilities and limitations of large language models for automatic code generation. We evaluate several state-of-the-art models on a diverse set of programming tasks and propose modifications to improve code correctness and security.",
            "authors": ["Daniel Kim", "Julia Martinez"],
            "categories": ["cs.SE", "cs.CL", "cs.AI"],
            "date": "2023-10-12",
            "source": "Sample Data"
        },
        {
            "id": "2311.33445",
            "title": "Privacy-Preserving Machine Learning: A Survey",
            "abstract": "This comprehensive survey covers privacy-preserving techniques in machine learning, including differential privacy, homomorphic encryption, and secure multi-party computation. We analyze the trade-offs between privacy guarantees, computational efficiency, and model utility.",
            "authors": ["Thomas Clark", "Rebecca White"],
            "categories": ["cs.CR", "cs.LG", "cs.AI"],
            "date": "2023-11-25",
            "source": "Sample Data"
        },
        {
            "id": "2312.99887",
            "title": "Multimodal Learning for Scientific Discovery",
            "abstract": "We introduce a multimodal learning framework that integrates textual, visual, and structural data for scientific discovery applications. The proposed approach demonstrates promising results in drug discovery, materials science, and protein function prediction tasks.",
            "authors": ["Laura Robinson", "Steven Walker"],
            "categories": ["cs.LG", "cs.AI", "q-bio.QM"],
            "date": "2023-12-08",
            "source": "Sample Data"
        },
        {
            "id": "2401.12321",
            "title": "Generative Models for Synthetic Data Creation",
            "abstract": "This paper presents novel methods for generating synthetic data that preserves privacy while maintaining statistical fidelity to the original dataset. Our approach combines adversarial training with differential privacy guarantees, enabling the creation of high-quality synthetic datasets for sensitive applications.",
            "authors": ["Christopher Lee", "Amanda Harris"],
            "categories": ["cs.LG", "cs.CR", "stat.ML"],
            "date": "2024-01-20",
            "source": "Sample Data"
        }
    ]
    
    # Convert to DataFrame
    return pd.DataFrame(sample_papers)

def prepare_texts(df):
    """Prepare texts for vectorization by combining title and abstract"""
    texts = []
    for _, row in df.iterrows():
        text = f"Title: {row['title']}\nAbstract: {row['abstract']}"
        texts.append(text)
    return texts

def main():
    # Ensure output directory exists
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Download dataset
    df = download_arxiv_dataset(num_papers=100)  # Start with 100 papers for the demo
    print(f"Working with {len(df)} papers")
    
    # Save dataset to CSV for reference
    df.to_csv("data/papers.csv", index=False)
    print("Saved dataset to data/papers.csv")
    
    # Prepare texts for embedding
    texts = prepare_texts(df)
    print(f"Prepared {len(texts)} texts for embedding")
    
    # Initialize ChromaDB client
    print(f"Initializing ChromaDB with persistence directory: {CHROMA_PERSIST_DIR}")
    
    # Initialize Chroma client with persistence
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # Create or get collection
    print(f"Creating collection: {COLLECTION_NAME}")
    
    # Try to get the collection, if it doesn't exist, create it
    try:
        # First check if collection exists
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"Retrieved existing collection: {COLLECTION_NAME}")
    except Exception:
        # Collection doesn't exist, create it
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # Using cosine similarity
        )
        print(f"Created new collection: {COLLECTION_NAME}")
    
    # Process and add documents in batches
    print("Adding documents to ChromaDB...")
    
    batch_size = min(BATCH_SIZE, len(texts))
    for i in range(0, len(texts), batch_size):
        end_idx = min(i + batch_size, len(texts))
        
        batch_ids = [df["id"].iloc[j] for j in range(i, end_idx)]
        batch_texts = texts[i:end_idx]
        
        # Create metadata for each document
        batch_metadata = []
        for j in range(i, end_idx):
            metadata = {
                "title": df["title"].iloc[j],
                "authors": ", ".join(df["authors"].iloc[j]),
                "categories": ", ".join(df["categories"].iloc[j]),
                "date": df["date"].iloc[j],
                "source": df["source"].iloc[j]
            }
            batch_metadata.append(metadata)
        
        # Add documents to collection
        collection.add(
            ids=batch_ids,
            documents=batch_texts,
            metadatas=batch_metadata
        )
        
        print(f"Added batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
    
    # Get collection count to verify
    collection_count = collection.count()
    print(f"Total documents in collection: {collection_count}")
    
    print("Successfully added documents to ChromaDB")
    print(f"ChromaDB is saved at: {os.path.abspath(CHROMA_PERSIST_DIR)}")
    print("Completed processing all papers")

if __name__ == "__main__":
    main()