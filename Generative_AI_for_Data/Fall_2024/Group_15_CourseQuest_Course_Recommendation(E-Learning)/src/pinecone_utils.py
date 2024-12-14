# import os
# import json
# from dotenv import load_dotenv
# from pinecone import Pinecone, ServerlessSpec

# # Load environment variables
# load_dotenv()

# def initialize_pinecone():
#     """
#     Initialize Pinecone client using environment variables.
#     """
#     return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# def get_index(pc, index_name):
#     """
#     Retrieve the existing Pinecone index.
#     """
#     return pc.Index(index_name)

# def query_pinecone_from_file(json_file, query_vector, top_k=5):
#     """
#     Query embeddings stored in a JSON file (all_embeddings.json) for the most relevant matches.

#     Parameters:
#     - json_file: Path to the JSON file containing embeddings and metadata.
#     - query_vector: Query embedding to compare against.
#     - top_k: Number of top matches to return.

#     Returns:
#     - A dictionary with matches containing metadata.
#     """
#     # Load embeddings from the JSON file
#     if not os.path.exists(json_file):
#         raise FileNotFoundError(f"JSON file {json_file} not found.")

#     with open(json_file, "r") as file:
#         embeddings_data = json.load(file)

#     # Function to calculate cosine similarity
#     def cosine_similarity(vec1, vec2):
#         dot_product = sum(a * b for a, b in zip(vec1, vec2))
#         magnitude1 = sum(a**2 for a in vec1) ** 0.5
#         magnitude2 = sum(b**2 for b in vec2) ** 0.5
#         return dot_product / (magnitude1 * magnitude2)

#     # Rank embeddings by similarity
#     ranked_data = sorted(
#         embeddings_data,
#         key=lambda item: cosine_similarity(query_vector, item["embedding"]),
#         reverse=True
#     )

#     # Return top_k results
#     return {"matches": ranked_data[:top_k]}

# def query_pinecone(index, query_vector, top_k=5):
#     """
#     Query Pinecone index directly with an embedding vector and retrieve metadata.
#     """
#     results = index.query(
#         vector=query_vector,
#         top_k=top_k,
#         include_metadata=True
#     )
#     return results

import os
import json
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

def initialize_pinecone():
    """
    Initialize Pinecone client using environment variables.
    """
    return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_index(pc, index_name):
    """
    Retrieve the existing Pinecone index.
    """
    return pc.Index(index_name)

def parse_metadata_text(metadata_text):
    """
    Parse the metadata 'text' field into a dictionary with individual fields.
    """
    metadata = {}
    try:
        # Regex patterns to extract fields
        metadata["Course Title"] = re.search(r"Course Title: (.*?),", metadata_text).group(1)
        metadata["Rating"] = re.search(r"Rating: (.*?),", metadata_text).group(1)
        metadata["Level"] = re.search(r"Level: (.*?),", metadata_text).group(1)
        metadata["Instructor"] = re.search(r"Instructor: (.*?),", metadata_text).group(1)
        metadata["Duration"] = re.search(r"Duration: (.*?) weeks", metadata_text).group(1)
    except AttributeError:
        # If a field is missing, it will default to 'N/A'
        metadata["Course Title"] = "N/A"
        metadata["Rating"] = "N/A"
        metadata["Level"] = "N/A"
        metadata["Instructor"] = "N/A"
        metadata["Duration"] = "N/A"
    return metadata

def query_pinecone_from_file(json_file, query_vector, top_k=5):
    """
    Query embeddings stored in a JSON file (all_embeddings.json) for the most relevant matches.

    Parameters:
    - json_file: Path to the JSON file containing embeddings and metadata.
    - query_vector: Query embedding to compare against.
    - top_k: Number of top matches to return.

    Returns:
    - A dictionary with matches containing metadata.
    """
    # Load embeddings from the JSON file
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON file {json_file} not found.")

    with open(json_file, "r") as file:
        embeddings_data = json.load(file)

    # Function to calculate cosine similarity
    def cosine_similarity(vec1, vec2):
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a**2 for a in vec1) ** 0.5
        magnitude2 = sum(b**2 for b in vec2) ** 0.5
        return dot_product / (magnitude1 * magnitude2)

    # Rank embeddings by similarity
    ranked_data = sorted(
        embeddings_data,
        key=lambda item: cosine_similarity(query_vector, item["embedding"]),
        reverse=True
    )

    # Parse metadata text into structured data
    for item in ranked_data[:top_k]:
        if "metadata" in item and "text" in item["metadata"]:
            item["metadata"] = parse_metadata_text(item["metadata"]["text"])

    # Return top_k results with parsed metadata
    return {"matches": ranked_data[:top_k]}

def query_pinecone(index, query_vector, top_k=5):
    """
    Query Pinecone index directly with an embedding vector and retrieve metadata.
    """
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    # Parse metadata text for each match
    for match in results['matches']:
        if "metadata" in match and "text" in match["metadata"]:
            match["metadata"] = parse_metadata_text(match["metadata"]["text"])
    return results





# import os
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize Pinecone
# def initialize_pinecone():
#     return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Create or retrieve an index
# def get_index(pc, index_name, dimension=1536, metric="cosine"):
#     if index_name not in pc.list_indexes().names():
#         pc.create_index(
#             name=index_name,
#             dimension=dimension,
#             metric=metric,
#             spec=ServerlessSpec(
#                 cloud="aws",
#                 region=os.getenv("PINECONE_ENV")
#             )
#         )
#     return pc.Index(index_name)

# # Query the Pinecone index
# def query_pinecone(index, embedding, top_k=3):
#     return index.query(
#         vector=embedding,
#         top_k=top_k,
#         include_metadata=True
#     )

# import os
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize Pinecone client
# def initialize_pinecone():
#     """
#     Initializes Pinecone client using API key from environment variables.
#     """
#     return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Create or get the index
# def get_index(pc, index_name, dimension=1536, metric="cosine", region="us-east-1"):
#     """
#     Checks if the index exists; creates it if it does not.
#     """
#     if index_name not in pc.list_indexes().names():
#         pc.create_index(
#             name=index_name,
#             dimension=dimension,
#             metric=metric,
#             spec=ServerlessSpec(
#                 cloud="aws",
#                 region=region
#             )
#         )
#     return pc.Index(index_name)

# # Query Pinecone index
# def query_pinecone(index, embedding, top_k=10):
#     """
#     Queries the Pinecone index with the provided embedding.
#     """
#     return index.query(
#         vector=embedding,
#         top_k=top_k,
#         include_metadata=True
#     )
