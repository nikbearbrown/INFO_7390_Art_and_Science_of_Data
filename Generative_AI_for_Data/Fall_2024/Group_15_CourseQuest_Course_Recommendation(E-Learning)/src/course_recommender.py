import os
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Define the get_embedding function directly here
def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response['data'][0]['embedding']

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Sample course data (replace with actual course data if available)
course_data = [
    {
        "title": "Introduction to Python Programming",
        "rating": 4.7,
        "level": "Beginner",
        "instructor": "Dr. Sarah Smith",
        "duration": "6 weeks",
        "description": "This course introduces Python programming for beginners..."
    },
    {
        "title": "Advanced Python Programming",
        "rating": 4.9,
        "level": "Advanced",
        "instructor": "Dr. John Doe",
        "duration": "8 weeks",
        "description": "This advanced Python programming course dives into data structures..."
    }
]

# Example: Get embeddings for course descriptions and store in Pinecone
for course in course_data:
    embedding = get_embedding(course["description"])
    # Create a unique ID for each course
    course_id = course["title"].replace(" ", "_").lower()
    
    # Upsert into Pinecone (replace `course_index` with your Pinecone index)
    course_index = pc.Index("course-recommender-index")
    course_index.upsert(vectors=[{
        "id": course_id,
        "values": embedding,
        "metadata": course
    }])

# To query the course data from Pinecone and generate recommendations
query = "I want to learn Python programming"
query_embedding = get_embedding(query)

# Perform a search in Pinecone to find similar courses
results = course_index.query(vector=query_embedding, top_k=3, include_metadata=True)

# Display the top 3 recommended courses based on the query
for result in results['matches']:
    print(f"Course Title: {result['metadata']['title']}")
    print(f"Rating: {result['metadata']['rating']}")
    print(f"Level: {result['metadata']['level']}")
    print(f"Instructor: {result['metadata']['instructor']}")
    print(f"Duration: {result['metadata']['duration']}")
    print(f"Description: {result['metadata']['description']}\n")


# import os
# import openai
# from pinecone import Pinecone, ServerlessSpec
# import numpy as np
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load API keys and environment details from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")

# openai.api_key = OPENAI_API_KEY

# # Index name for Course Recommender
# COURSE_INDEX = "course-recommender-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# # Initialize Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Create the Pinecone index for courses
# COURSE_INDEX = "course-recommendation-index"

# if COURSE_INDEX not in pc.list_indexes().names():
#     pc.create_index(
#         name=COURSE_INDEX,
#         dimension=1536,  # Based on the embedding size
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )

# # Get the index
# course_index = pc.Index(COURSE_INDEX)

# # Embed and store courses
# for course in course_data:
#     course_embedding = get_embedding(course['description'])
#     course_index.upsert(vectors=[{
#         "id": course['title'],  # Use course title as ID
#         "values": course_embedding,
#         "metadata": {
#             "title": course['title'],
#             "rating": course['rating'],
#             "level": course['level'],
#             "instructor": course['instructor'],
#             "duration": course['duration'],
#             "description": course['description']
#         }
#     }])

# def retrieve_course_context(query, top_k=3):
#     query_embedding = get_embedding(query)
#     results = course_index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
#     contexts = []
#     for match in results['matches']:
#         context = f"""
#         Course Title: {match['metadata']['title']}
#         Rating: {match['metadata']['rating']}
#         Level: {match['metadata']['level']}
#         Instructor: {match['metadata']['instructor']}
#         Duration: {match['metadata']['duration']}

#         {match['metadata']['description']}
#         """
#         contexts.append(context)
#     return contexts

# def get_embedding(text):
#     """
#     Generate embedding for the given text using OpenAI's API.
#     """
#     response = openai.Embedding.create(
#         model=EMBEDDING_MODEL,
#         input=text
#     )
#     return np.array(response['data'][0]['embedding'])


# def generate_detailed_explanation(course_contexts):
#     """
#     Generate an in-depth explanation of the course context by combining various metadata fields
#     such as title, rating, instructor, duration, etc.
#     """
#     explanations = []
    
#     for course in course_contexts:
#         title = course.get('title', 'No Title')
#         rating = course.get('rating', 'Not Available')
#         level = course.get('level', 'Not Available')
#         instructor = course.get('instructor', 'Not Available')
#         duration = course.get('duration', 'Not Available')
        
#         explanation = f"""
#         Course Title: {title}
#         Rating: {rating}
#         Level: {level}
#         Instructor: {instructor}
#         Duration: {duration}
        
#         This course provides in-depth knowledge and practical insights into its field. 
#         The instructor {instructor} has a wealth of experience in the subject matter, 
#         and the course duration of {duration} weeks ensures that learners have ample time to master key concepts.
#         The course is highly rated by previous participants, with a rating of {rating}.
#         """
#         explanations.append(explanation.strip())

#     # Combine all explanations into one block of text
#     return "\n\n".join(explanations)

# def generate_course_recommendation(query, course_contexts):
#     """
#     Generate course recommendations based on the given query and the retrieved course contexts.
#     This function asks the model to generate an explanation based on the context.
#     """
#     combined_context = generate_detailed_explanation(course_contexts)  # Generate detailed explanation
#     prompt = f"""
#     You are an expert course recommender. Based on the provided course information, explain the features of each course in detail. 
    
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

# def recommend_courses(query):
#     """
#     Recommend courses based on a user query. Retrieves relevant course descriptions and generates a detailed recommendation.
#     """
#     # Retrieve relevant course context from Pinecone
#     course_contexts = retrieve_course_context(query)
    
#     # Generate the final course recommendation with detailed explanation
#     recommendation = generate_course_recommendation(query, course_contexts)
#     return recommendation

# import os
# import openai
# from pinecone import Pinecone, ServerlessSpec
# import numpy as np
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load API keys and environment details from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")

# openai.api_key = OPENAI_API_KEY

# # Index name for Course Recommender
# COURSE_INDEX = "course-recommender-index"
# EMBEDDING_MODEL = "text-embedding-ada-002"
# LLM_MODEL = "gpt-4"  # If you don't have GPT-4, use "gpt-3.5-turbo"

# # Initialize Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)

# # Ensure the course index exists
# if COURSE_INDEX not in pc.list_indexes().names():
#     pc.create_index(
#         name=COURSE_INDEX,
#         dimension=1536,
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )

# # Access the course index
# course_index = pc.Index(COURSE_INDEX)

# def get_embedding(text):
#     """
#     Generate embedding for the given text using OpenAI's API.
#     """
#     response = openai.Embedding.create(
#         model=EMBEDDING_MODEL,
#         input=text
#     )
#     return np.array(response['data'][0]['embedding'])

# def retrieve_course_context(query, top_k=3):
#     """
#     Retrieve the most relevant courses for a given query using Pinecone.
#     Assumes each match in the index has 'text' (course description) in its metadata.
#     """
#     query_embedding = get_embedding(query)  # Get embedding for the user's query
#     results = course_index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
#     # Extract relevant course information from the matches
#     contexts = [match['metadata']['text'] for match in results['matches']]  # Assuming 'text' holds the course description
#     return contexts

# def generate_course_recommendation(query, course_contexts):
#     """
#     Generate course recommendations based on the given query and the retrieved course contexts.
#     """
#     combined_context = "\n\n".join(course_contexts)  # Combine the retrieved course descriptions
#     prompt = f"""
#     You are an expert course recommender. Use the following context to recommend the best courses for the question below.
#     Only use the provided context to generate your response. Do not assume or create additional scenarios not mentioned in the context.
    
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

# def recommend_courses(query):
#     """
#     Recommend courses based on a user query. Retrieves relevant course descriptions and generates a recommendation.
#     """
#     # Retrieve relevant course context from Pinecone
#     course_contexts = retrieve_course_context(query)
    
#     # Generate the final course recommendation
#     recommendation = generate_course_recommendation(query, course_contexts)
#     return recommendation