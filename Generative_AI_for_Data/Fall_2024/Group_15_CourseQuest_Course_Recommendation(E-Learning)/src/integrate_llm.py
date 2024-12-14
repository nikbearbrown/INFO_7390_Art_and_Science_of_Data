# import openai
# import os
# import json
# from dotenv import load_dotenv
# from pinecone_utils import query_pinecone_from_file

# # Load environment variables
# load_dotenv()

# # Check if the API key is loaded correctly
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise RuntimeError("OpenAI API key not found. Please set it in the .env file or provide it directly.")

# openai.api_key = api_key

# def generate_embedding(query_text):
#     """
#     Generate embeddings for the input query using OpenAI's model.
#     """
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=query_text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         raise RuntimeError(f"Error generating embedding: {e}")

# def enhance_context_with_gpt(query_text, contextual_data):
#     """
#     Use GPT to generate enhanced responses based on the query and contextual data.
#     """
#     try:
#         # Combine the metadata into a single prompt
#         context = "\n".join([
#             f"Course Title: {item.get('Course Title', 'N/A')}, "
#             f"Rating: {item.get('Rating', 'N/A')}, "
#             f"Level: {item.get('Level', 'N/A')}, "
#             f"Instructor: {item.get('Instructor', 'N/A')}, "
#             f"Duration: {item.get('Duration', 'N/A')} weeks"
#             for item in contextual_data
#         ])
        
#         # Create the GPT prompt
#         prompt = (
#             f"You are an expert course recommender. Based on the user's query: '{query_text}', "
#             "and the following relevant courses from the knowledge base:\n\n"
#             f"{context}\n\n"
#             "Generate a concise, helpful response to the user that summarizes the best recommendations."
#         )
        
#         # Call GPT
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{"role": "system", "content": "You are an intelligent course recommender."},
#                       {"role": "user", "content": prompt}],
#             max_tokens=300
#         )
        
#         # Extract the response text
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         raise RuntimeError(f"Error generating GPT response: {e}")

# def get_enhanced_recommendations(query_text, json_file="all_embeddings.json", top_k=5):
#     """
#     Get enhanced recommendations using the query text and the local JSON file.

#     Parameters:
#     - query_text: The user's query.
#     - json_file: Path to the local JSON file containing embeddings.
#     - top_k: Number of top matches to fetch.
#     """
#     # Generate embedding for the query
#     query_vector = generate_embedding(query_text)

#     # Query the local JSON file for relevant embeddings
#     results = query_pinecone_from_file(json_file=json_file, query_vector=query_vector, top_k=top_k)

#     # Extract metadata for contextual data
#     contextual_data = [match.get("metadata", {}) for match in results["matches"]]

#     # Enhance with GPT
#     enhanced_response = enhance_context_with_gpt(query_text, contextual_data)
#     return enhanced_response

# if __name__ == "__main__":
#     # Example usage
#     query = "I want a machine learning course"  # Replace the query text here
    
#     # Use the local JSON file to fetch embeddings
#     json_file_path = "all_embeddings.json"  # Ensure this file exists and contains the necessary data

#     # Get enhanced recommendations
#     try:
#         response = get_enhanced_recommendations(
#             query_text=query,
#             json_file=json_file_path,
#             top_k=5
#         )
#         print("Enhanced Recommendation Response:\n")
#         print(response)
#     except RuntimeError as e:
#         print(f"Error: {e}")

# import openai
# import os
# import json
# from dotenv import load_dotenv
# from pinecone_utils import query_pinecone_from_file

# # Load environment variables
# load_dotenv()

# # Check if the API key is loaded correctly
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise RuntimeError("OpenAI API key not found. Please set it in the .env file or provide it directly.")

# openai.api_key = api_key

# def generate_embedding(query_text):
#     """
#     Generate embeddings for the input query using OpenAI's model.
#     """
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=query_text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         raise RuntimeError(f"Error generating embedding: {e}")

# def enhance_context_with_gpt(query_text, contextual_data):
#     """
#     Use GPT to generate enhanced responses based on the query and contextual data.
#     """
#     try:
#         # Combine the metadata into a single prompt
#         context = "\n".join([
#             f"Course Title: {item.get('Course Title', 'N/A')}, "
#             f"Rating: {item.get('Rating', 'N/A')}, "
#             f"Level: {item.get('Level', 'N/A')}, "
#             f"Instructor: {item.get('Instructor', 'N/A')}, "
#             f"Duration: {item.get('Duration', 'N/A')} weeks"
#             for item in contextual_data
#         ])

#         # Fallback if no contextual data is available
#         if not context.strip():
#             return "No course details are available from the knowledge base. Please try another query."

#         # Create the GPT prompt
#         prompt = (
#             f"You are an expert course recommender. Based on the user's query: '{query_text}', "
#             "and the following relevant courses from the knowledge base:\n\n"
#             f"{context}\n\n"
#             "Generate a concise, helpful response to the user that summarizes the best recommendations."
#         )

#         # Call GPT
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are an intelligent course recommender."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300
#         )

#         # Extract the response text
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"Error generating GPT response: {e}"

# def get_enhanced_recommendations(query_text, json_file="all_embeddings.json", top_k=5):
#     """
#     Get enhanced recommendations using the query text and the local JSON file.

#     Parameters:
#     - query_text: The user's query.
#     - json_file: Path to the local JSON file containing embeddings.
#     - top_k: Number of top matches to fetch.
#     """
#     try:
#         # Generate embedding for the query
#         query_vector = generate_embedding(query_text)

#         # Query the local JSON file for relevant embeddings
#         results = query_pinecone_from_file(json_file=json_file, query_vector=query_vector, top_k=top_k)

#         # Extract metadata for contextual data
#         contextual_data = [match.get("metadata", {}) for match in results["matches"]]

#         # Print debug information
#         print("Contextual Data Retrieved:")
#         print(json.dumps(contextual_data, indent=4))

#         # Enhance with GPT
#         enhanced_response = enhance_context_with_gpt(query_text, contextual_data)
#         return enhanced_response
#     except Exception as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
#     # Example usage
#     query = "I want machine learning courses"

#     # Use the local JSON file to fetch embeddings
#     json_file_path = "all_embeddings.json"  # Ensure this file exists and contains the necessary data

#     # Get enhanced recommendations
#     try:
#         response = get_enhanced_recommendations(
#             query_text=query,
#             json_file=json_file_path,
#             top_k=5
#         )
#         print("Enhanced Recommendation Response:\n")
#         print(response)
#     except RuntimeError as e:
#         print(f"Error: {e}")
import openai
import os
import json
from dotenv import load_dotenv
from pinecone_utils import query_pinecone_from_file

# Load environment variables
load_dotenv()

# Check if the API key is loaded correctly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OpenAI API key not found. Please set it in the .env file or provide it directly.")

openai.api_key = api_key

def generate_embedding(query_text):
    """
    Generate embeddings for the input query using OpenAI's model.
    """
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query_text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")

def enhance_context_with_gpt(query_text, contextual_data):
    """
    Use GPT to generate enhanced responses based on the query and contextual data.
    """
    try:
        # Combine the metadata into a single prompt
        if contextual_data:
            context = "\n".join([
                f"Course Title: {item.get('Course Title', 'N/A')}, "
                f"Rating: {item.get('Rating', 'N/A')}, "
                f"Level: {item.get('Level', 'N/A')}, "
                f"Instructor: {item.get('Instructor', 'N/A')}, "
                f"Duration: {item.get('Duration', 'N/A')} weeks"
                for item in contextual_data
            ])
        else:
            context = "No relevant courses found in the knowledge base."

        # Create the GPT prompt
        prompt = (
            f"You are an expert course recommender. Based on the user's query: '{query_text}', "
            "and the following relevant courses from the knowledge base:\n\n"
            f"{context}\n\n"
            "Generate a concise, helpful response to the user that summarizes the best recommendations."
        )

        # Call GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an intelligent course recommender."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        # Extract the response text
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating GPT response: {e}"

def get_enhanced_recommendations(query_text, json_file="all_embeddings.json", top_k=5):
    """
    Get enhanced recommendations using the query text and the local JSON file.

    Parameters:
    - query_text: The user's query.
    - json_file: Path to the local JSON file containing embeddings.
    - top_k: Number of top matches to fetch.
    """
    try:
        # Generate embedding for the query
        query_vector = generate_embedding(query_text)

        # Query the local JSON file for relevant embeddings
        results = query_pinecone_from_file(json_file=json_file, query_vector=query_vector, top_k=top_k)

        # Extract metadata for contextual data
        print(results['matches'])
        contextual_data = [match.get("metadata", {}) for match in results["matches"]]

        # Debug: Print retrieved contextual data
        if contextual_data:
            print("Contextual Data Retrieved:")
            print(json.dumps(contextual_data, indent=4))
        else:
            print("No contextual data found. The knowledge base might not contain relevant embeddings.")

        # Enhance with GPT
        enhanced_response = enhance_context_with_gpt(query_text, contextual_data)
        # print("ENHANCED RESPONSE", enhanced_response)
        return enhanced_response, contextual_data
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Example usage
    query = "I want machine learning courses"

    # Use the local JSON file to fetch embeddings
    json_file_path = "all_embeddings.json"  # Ensure this file exists and contains the necessary data

    # Get enhanced recommendations
    try:
        response = get_enhanced_recommendations(
            query_text=query,
            json_file=json_file_path,
            top_k=5
        )
        print("\nEnhanced Recommendation Response:")
        print(response)
    except RuntimeError as e:
        print(f"Error: {e}")



# import openai
# import os
# from dotenv import load_dotenv
# from pinecone_utils import initialize_pinecone, get_index, query_pinecone

# # Load environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Generate query embeddings using OpenAI
# def generate_embedding(query_text):
#     """
#     Generate embeddings for the input query using OpenAI's model.
#     """
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=query_text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         raise RuntimeError(f"Error generating embedding: {e}")

# # Fetch contextual responses using OpenAI
# def get_contextual_response(query_text, index_name="course-recommend-proj", top_k=5):
#     """
#     Fetch relevant embeddings from Pinecone and use OpenAI to generate contextual responses.
#     """
#     # Initialize Pinecone
#     pc = initialize_pinecone()
#     index = get_index(pc, index_name)

#     # Generate embedding for the query
#     query_vector = generate_embedding(query_text)

#     # Query Pinecone
#     results = query_pinecone(index, query_vector, top_k=top_k)

#     # Extract metadata for contextual response
#     contextual_data = []
#     for match in results['matches']:
#         metadata = match.get("metadata", {})
#         contextual_data.append(metadata)

#     return contextual_data

# import openai
# import os
# from dotenv import load_dotenv
# from pinecone_utils import initialize_pinecone, get_index, query_pinecone

# # Load environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Generate embedding for a query
# def generate_embedding(query_text):
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=query_text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         raise RuntimeError(f"Error generating embedding: {e}")

# # Query Pinecone for recommendations
# def get_recommendations(query_text, index_name="course-recommend-proj", top_k=3):
#     pc = initialize_pinecone()
#     index = get_index(pc, index_name)
#     embedding = generate_embedding(query_text)
#     results = query_pinecone(index, embedding, top_k)
#     return results

# import openai
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def generate_embedding(query_text: str):
#     """
#     Generate an embedding for the input text using OpenAI's text-embedding-ada-002 model.
#     :param query_text: The input query text.
#     :return: Embedding vector as a list.
#     """
#     try:
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=query_text
#         )
#         return response['data'][0]['embedding']
#     except Exception as e:
#         raise RuntimeError(f"Error generating embedding: {str(e)}")
