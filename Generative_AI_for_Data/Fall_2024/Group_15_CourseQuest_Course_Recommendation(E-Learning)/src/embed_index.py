import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
import openai
from pinecone import Pinecone

# Load API keys from the .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API keys
if not all([PINECONE_API_KEY, PINECONE_ENV, OPENAI_API_KEY]):
    raise ValueError("Ensure that PINECONE_API_KEY, PINECONE_ENV, and OPENAI_API_KEY are properly set in the .env file.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone using the new method
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define Pinecone index name and configuration
INDEX_NAME = "course-recommend-proj"

# Check if the index exists, create if not
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # OpenAI embedding size
        metric="cosine"
    )

# Access the index directly using the Index class
index = pc.Index(INDEX_NAME)

# Function to generate embeddings using OpenAI
def generate_embedding(text):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Combine fields into a single string for embedding
def combine_fields(course_data):
    return f"Course Title: {course_data.get('Course Title', '')}, Rating: {course_data.get('Rating', '')}, Level: {course_data.get('Level', '')}, " \
           f"Instructor: {course_data.get('Instructor', '')}, Duration: {course_data.get('Duration to complete (Approx.)', '')} weeks"

# Upload embeddings from JSON file
def upload_embeddings_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    vectors = []
    for idx, item in tqdm(enumerate(data), total=len(data)):
        text = combine_fields(item)
        unique_id = str(idx)
        embedding = generate_embedding(text)
        if embedding:
            vectors.append((unique_id, embedding, {"text": text}))

        # Batch upload to Pinecone
        if len(vectors) >= 100:
            index.upsert(vectors)
            vectors = []

    # Upload remaining vectors
    if vectors:
        index.upsert(vectors)

if __name__ == "__main__":
    # Path to the JSON file
    json_file_path = "C:/Users/prani/Downloads/Adv. Data Science Project 2/Adv.Data Science Project/data/processed/preprocessed_data.json"  # Replace with the correct path
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")

    print("Uploading embeddings to Pinecone...")
    upload_embeddings_from_json(json_file_path)
    print("Upload complete!")


# import os
# import pandas as pd
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

# # Initialize Pinecone using the new method
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Define Pinecone index name and configuration
# INDEX_NAME = "course-recommender"

# # Check if the index exists, create if not
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,  # OpenAI embedding size
#         metric="cosine"
#     )

# # Access the index directly using the Index class
# index = pc.Index(INDEX_NAME)

# # Function to generate embeddings using OpenAI (Updated for 1.0.0+)
# def generate_embedding(text):
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",  # Adjust the model if needed
#             input=text
#         )
#         # Correctly access the embedding data
#         return response['data'][0]['embedding']
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None

# # Function to combine relevant columns into a single text
# def combine_columns(row):
#     # Combine relevant columns into a single text string
#     text = f"Course Title: {row['Course Title']}, Rating: {row['Rating']}, Level: {row['Level']}, " \
#            f"Instructor: {row['Instructor']}, Duration: {row['Duration to complete (Approx.)']} weeks"
#     return text

# # Upload embeddings to Pinecone
# def upload_embeddings(csv_file):
#     # Load the CSV file into a DataFrame
#     data = pd.read_csv(csv_file)

#     data = data.head(10)

#     # Batch insert data into Pinecone
#     vectors = []
#     for idx, row in tqdm(data.iterrows(), total=data.shape[0]):
#         # Combine the columns for the text embedding
#         text = combine_columns(row)
#         unique_id = str(idx)  # Using the row index as a unique identifier
#         embedding = generate_embedding(text)
#         if embedding:
#             vectors.append((unique_id, embedding, {"text": text}))

#         # Batch upsert after every 100 vectors
#         if len(vectors) >= 100:
#             index.upsert(vectors)
#             vectors = []  # Clear the batch

#     # Upsert remaining vectors
#     if vectors:
#         index.upsert(vectors)

# if __name__ == "__main__":
#     # Path to the CSV file
#     csv_file_path = "data\\raw\\CourseraDataset-Clean.csv"  # Replace with the correct path to your CSV file
#     if not os.path.exists(csv_file_path):
#         raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

#     print("Uploading embeddings to Pinecone...")
#     upload_embeddings(csv_file_path)
#     print("Upload complete!")




# import os
# import pandas as pd
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

# # Initialize Pinecone using the new method
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Define Pinecone index name and configuration
# INDEX_NAME = "course-recommender"

# # Check if the index exists, create if not
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,  # OpenAI embedding size
#         metric="cosine"
#     )

# # Access the index directly using the Index class
# index = pc.Index(INDEX_NAME)

# # Function to generate embeddings using OpenAI (Updated for 1.0.0+)
# def generate_embedding(text):
#     try:
#         response = openai.embeddings.create(
#             model="text-embedding-ada-002",  # Adjust the model if needed
#             input=text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None

# # Function to combine relevant columns into a single text
# def combine_columns(row):
#     # Combine relevant columns into a single text string
#     text = f"Course Title: {row['Course Title']}, Rating: {row['Rating']}, Level: {row['Level']}, " \
#            f"Instructor: {row['Instructor']}, Duration: {row['Duration to complete (Approx.)']} weeks"
#     return text

# # Upload embeddings to Pinecone
# def upload_embeddings(csv_file):
#     # Load the CSV file into a DataFrame
#     data = pd.read_csv(csv_file)

#     # Batch insert data into Pinecone
#     vectors = []
#     for idx, row in tqdm(data.iterrows(), total=data.shape[0]):
#         # Combine the columns for the text embedding
#         text = combine_columns(row)
#         unique_id = str(idx)  # Using the row index as a unique identifier
#         embedding = generate_embedding(text)
#         if embedding:
#             vectors.append((unique_id, embedding, {"text": text}))

#         # Batch upsert after every 100 vectors
#         if len(vectors) >= 100:
#             index.upsert(vectors)
#             vectors = []  # Clear the batch

#     # Upsert remaining vectors
#     if vectors:
#         index.upsert(vectors)

# if __name__ == "__main__":
#     # Path to the CSV file
#     csv_file_path = "data\\raw\\CourseraDataset-Clean.csv"  # Replace with the correct path to your CSV file
#     if not os.path.exists(csv_file_path):
#         raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

#     print("Uploading embeddings to Pinecone...")
#     upload_embeddings(csv_file_path)
#     print("Upload complete!")








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

# # Initialize Pinecone using the new method
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Define Pinecone index name and configuration
# INDEX_NAME = "course-recommender"

# # Check if the index exists, create if not
# if INDEX_NAME not in pc.list_indexes().names():
#     pc.create_index(
#         name=INDEX_NAME,
#         dimension=1536,  # OpenAI embedding size
#         metric="cosine"
#     )

# # Access the index directly using the Index class
# index = pc.Index(INDEX_NAME)

# # Function to generate embeddings using OpenAI (Updated for 1.0.0+)
# def generate_embedding(text):
#     try:
#         response = openai.embeddings.create(
#             model="text-embedding-ada-002",  # Adjust the model if needed
#             input=text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         print(f"Error generating embedding: {e}")
#         return None

# # Upload embeddings to Pinecone
# def upload_embeddings(json_file):
#     with open(json_file, 'r') as f:
#         data = json.load(f)

#     # Batch insert data into Pinecone
#     vectors = []
#     for record in tqdm(data):
#         text = record.get("text")
#         unique_id = record.get("id", str(hash(text)))
#         embedding = generate_embedding(text)
#         if embedding:
#             vectors.append((unique_id, embedding, {"text": text}))

#         # Batch upsert after every 100 vectors
#         if len(vectors) >= 100:
#             index.upsert(vectors)
#             vectors = []

#     # Upsert remaining vectors
#     if vectors:
#         index.upsert(vectors)

# if __name__ == "__main__":
#     # Path to the preprocessed JSON file
#     json_file_path = "data\processed\preprocessed_data.json"
#     if not os.path.exists(json_file_path):
#         raise FileNotFoundError(f"JSON file not found at {json_file_path}")

#     print("Uploading embeddings to Pinecone...")
#     upload_embeddings(json_file_path)
#     print("Upload complete!")
