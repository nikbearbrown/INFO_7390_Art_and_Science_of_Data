import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Specify your index name
index_name = "course-recommend-proj"

# Check if the index exists
if index_name not in pc.list_indexes().names():
    raise ValueError(f"Index {index_name} does not exist. Please check the index name.")

# Access the index
index = pc.Index(index_name)

def fetch_all_embeddings_with_metadata(output_file="embeddings.json", limit=100):
    """
    Fetch all embeddings along with metadata from Pinecone and save them to a JSON file.

    Parameters:
    - output_file: The file path where embeddings and metadata will be saved.
    - limit: Number of embeddings to fetch per batch.
    """
    # Describe index to get total vector count
    index_stats = index.describe_index_stats()
    total_vectors = index_stats["namespaces"][""]["vector_count"]

    if total_vectors == 0:
        print("No embeddings found in the index.")
        return

    print(f"Total vectors in the index: {total_vectors}")

    # Generate placeholder IDs (you need to replace this with your own method of ID generation)
    # Assuming IDs are sequential integers
    all_ids = [str(i) for i in range(total_vectors)]

    # Fetch embeddings in batches
    data_to_save = []
    for batch_start in range(0, len(all_ids), limit):
        batch_ids = all_ids[batch_start:batch_start + limit]
        fetch_results = index.fetch(ids=batch_ids)

        # Parse fetched results
        for id, record in fetch_results["vectors"].items():
            data_to_save.append({
                "id": id,
                "embedding": record["values"],
                "metadata": record.get("metadata", {})
            })

    # Save results to JSON
    with open(output_file, "w") as json_file:
        json.dump(data_to_save, json_file, indent=4)

    print(f"All embeddings and metadata saved to {output_file}")

if __name__ == "__main__":
    # Fetch all embeddings and metadata and save to JSON
    fetch_all_embeddings_with_metadata(output_file="all_embeddings.json", limit=100)





# import os
# import json
# from tqdm import tqdm
# from dotenv import load_dotenv
# import openai
# from pinecone import Pinecone

# # Load API keys from the .env file
# load_dotenv()
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Validate API keys
# if not all([PINECONE_API_KEY, PINECONE_ENV, OPENAI_API_KEY]):
#     raise ValueError("Ensure that PINECONE_API_KEY, PINECONE_ENV, and OPENAI_API_KEY are properly set in the .env file.")

# # Initialize OpenAI API
# openai.api_key = OPENAI_API_KEY

# # Initialize Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)
# INDEX_NAME = "course-recommend-proj"

# # Create index if it doesn't exist
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,
#         metric="cosine"
#     )

# # Access the index
# index = pc.Index(INDEX_NAME)

# # Function to generate embeddings
# def generate_embedding(text):
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None

# # Combine fields for embedding
# def combine_fields(course_data):
#     return f"Course Title: {course_data.get('Course Title', '')}, Rating: {course_data.get('Rating', '')}, Level: {course_data.get('Level', '')}, " \
#            f"Instructor: {course_data.get('Instructor', '')}, Duration: {course_data.get('Duration to complete (Approx.)', '')} weeks"

# # Upload embeddings to Pinecone and save to JSON
# def upload_and_save_embeddings(json_file, output_json):
#     with open(json_file, 'r') as file:
#         data = json.load(file)

#     vectors = []
#     embeddings_data = []  # List to store embedding data
#     for idx, item in tqdm(enumerate(data), total=len(data)):
#         text = combine_fields(item)
#         embedding = generate_embedding(text)
#         if embedding:
#             metadata = {
#                 "Course Title": item.get("Course Title", ""),
#                 "Description": item.get("Description", ""),
#                 "Level": item.get("Level", ""),
#                 "Duration to complete (Approx.)": item.get("Duration to complete (Approx.)", ""),
#                 "Rating": item.get("Rating", ""),
#                 "Instructor": item.get("Instructor", "")
#             }
#             vectors.append((str(idx), embedding, metadata))
#             embeddings_data.append({
#                 "id": str(idx),
#                 "embedding": embedding,
#                 "metadata": metadata
#             })

#         if len(vectors) >= 100:
#             index.upsert(vectors)
#             vectors = []

#     if vectors:
#         index.upsert(vectors)

#     # Save embeddings and metadata to JSON
#     with open(output_json, 'w') as out_file:
#         json.dump(embeddings_data, out_file, indent=4)
#     print(f"Embeddings saved to {output_json}")

# if __name__ == "__main__":
#     json_file_path = "data/processed/preprocessed_data.json"  # Replace with your JSON file path
#     output_json_path = "data/processed/embeddings_data.json"  # Replace with desired output file path

#     if not os.path.exists(json_file_path):
#         raise FileNotFoundError(f"JSON file not found at {json_file_path}")

#     print("Uploading embeddings to Pinecone and saving to JSON...")
#     upload_and_save_embeddings(json_file_path, output_json_path)
#     print("Upload complete! Embeddings saved to JSON.")

# import os
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize Pinecone
# pc = Pinecone(
#     api_key=os.getenv("PINECONE_API_KEY")
# )

# # Define index name
# INDEX_NAME = "course-recommend-proj"

# # Check if the index exists, create it if not
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region=os.getenv("PINECONE_ENV")
#         )
#     )

# # Access the index
# index = pc.Index(INDEX_NAME)

# # Query function
# def query_embedding(embedding, top_k=10):
#     results = index.query(
#         vector=embedding,
#         top_k=top_k,
#         include_metadata=True
#     )
#     return results
