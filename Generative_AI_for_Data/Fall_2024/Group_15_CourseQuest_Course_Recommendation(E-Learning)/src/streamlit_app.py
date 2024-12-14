# import os
# import openai
# import streamlit as st
# import json
# from dotenv import load_dotenv
# from src.fetch_results import fetch_and_save_results

# # Load environment variables
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def load_results_from_json(file_path="src/results.json"):
#     """
#     Load results from a JSON file.
#     """
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as json_file:
#             return json.load(json_file)
#     else:
#         return []

# st.title("Query Interface with Knowledge Base")
# st.write("This app retrieves responses from Pinecone and displays results from a JSON file.")

# user_query = st.text_input("Enter your query:")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Generate embedding for the query
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",
#             input=user_query
#         )
#         query_embedding = response['data'][0]['embedding']

#         # Fetch and save results
#         fetch_and_save_results(query_embedding, top_k=3)

#         # Load results from JSON
#         results = load_results_from_json()

#         # Display results
#         if results:
#             for idx, result in enumerate(results, start=1):
#                 metadata = result['metadata']
#                 st.write(f"### Result {idx}")
#                 st.write(f"**Course Title:** {metadata.get('Course Title', 'N/A')}")
#                 st.write(f"**Rating:** {metadata.get('Rating', 'N/A')}")
#                 st.write(f"**Level:** {metadata.get('Level', 'N/A')}")
#                 st.write(f"**Instructor:** {metadata.get('Instructor', 'N/A')}")
#                 st.write(f"**Duration:** {metadata.get('Duration to complete (Approx.)', 'N/A')} weeks")
#                 st.write(f"**Relevance Score:** {result.get('score', 'N/A')}")
#                 st.write("---")
#         else:
#             st.write("No relevant answers found in the knowledge base.")

#     except Exception as e:
#         st.error(f"Error: {e}")

# import os ### This code works
# import openai
# import streamlit as st
# import json
# from dotenv import load_dotenv
# from integrate_llm import get_enhanced_recommendations

# # Load environment variables
# load_dotenv()

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Streamlit app UI
# st.title("Course Recommender System")
# st.write("This app retrieves course recommendations based on your query using embeddings and GPT for enhanced responses.")

# # User query input
# user_query = st.text_input("Enter your query (e.g., 'I want machine learning courses'):")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Path to local JSON file with embeddings
#         json_file_path = "all_embeddings.json"  # Ensure this file exists in your project

#         # Call the enhanced recommendation function
#         enhanced_response = get_enhanced_recommendations(
#             query_text=user_query,
#             json_file=json_file_path,
#             top_k=5  # Fetch the top 5 results
#         )

#         # Display contextual data
#         st.write("### Contextual Data Retrieved:")
#         with open(json_file_path, "r") as json_file:
#             all_embeddings = json.load(json_file)

#         # Extract contextual data and show it
#         for idx, embedding in enumerate(all_embeddings[:5], start=1):  # Display top 5 results
#             metadata = embedding.get("metadata", {})
#             st.write(f"**Result {idx}:**")
#             st.write(f"- **Course Title:** {metadata.get('Course Title', 'N/A')}")
#             st.write(f"- **Rating:** {metadata.get('Rating', 'N/A')}")
#             st.write(f"- **Level:** {metadata.get('Level', 'N/A')}")
#             st.write(f"- **Instructor:** {metadata.get('Instructor', 'N/A')}")
#             st.write(f"- **Duration:** {metadata.get('Duration', 'N/A')} weeks")
#             st.write("---")

#         # Display enhanced recommendation response
#         st.write("### Enhanced Recommendation from GPT:")
#         st.write(enhanced_response)

#     except Exception as e:
#         st.error(f"Error: {e}")

# import os ######################################################################
# import openai
# import streamlit as st
# import json
# from dotenv import load_dotenv
# from integrate_llm import get_enhanced_recommendations

# # Load environment variables
# load_dotenv()

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Check if the API key is loaded
# if not openai.api_key:
#     st.error("OpenAI API key not found. Please set it in the .env file.")
#     st.stop()

# # Streamlit app UI
# st.title("Course Recommender System")
# st.write("This app retrieves course recommendations based on your query using embeddings and GPT for enhanced responses.")

# # User query input
# user_query = st.text_input("Enter your query (e.g., 'I want machine learning courses'):")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Path to local JSON file with embeddings
#         json_file_path = "all_embeddings.json"  # Ensure this file exists in your project

#         # Call the enhanced recommendation function
#         enhanced_response = get_enhanced_recommendations(
#             query_text=user_query,
#             json_file=json_file_path,
#             top_k=5  # Fetch the top 5 results
#         )

#         # Display contextual data
#         st.write("### Contextual Data Retrieved:")
#         with open(json_file_path, "r") as json_file:
#             all_embeddings = json.load(json_file)

#         if all_embeddings:
#             # Extract contextual data and show it
#             for idx, embedding in enumerate(all_embeddings[:5], start=1):  # Display top 5 results
#                 metadata = embedding.get("metadata", {})
#                 st.write(f"**Result {idx}:**")
#                 st.write(f"- **Course Title:** {metadata.get('Course Title', 'N/A')}")
#                 st.write(f"- **Rating:** {metadata.get('Rating', 'N/A')}")
#                 st.write(f"- **Level:** {metadata.get('Level', 'N/A')}")
#                 st.write(f"- **Instructor:** {metadata.get('Instructor', 'N/A')}")
#                 st.write(f"- **Duration:** {metadata.get('Duration', 'N/A')} weeks")
#                 st.write("---")
#         else:
#             st.write("No embeddings found in the knowledge base.")

#         # Display enhanced recommendation response
#         st.write("### Enhanced Recommendation from GPT:")
#         if enhanced_response.strip():
#             st.write(enhanced_response)
#         else:
#             st.write("GPT could not generate a response. Please refine your query.")

#     except FileNotFoundError:
#         st.error(f"The file {json_file_path} was not found. Please ensure it exists in the specified path.")
#     except json.JSONDecodeError:
#         st.error("The JSON file is corrupted or not formatted correctly. Please check the file contents.")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}")


# import os
# import openai
# import streamlit as st
# import json
# from dotenv import load_dotenv
# from integrate_llm import get_enhanced_recommendations

# # Load environment variables
# load_dotenv()

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Check if the API key is loaded
# if not openai.api_key:
#     st.error("OpenAI API key not found. Please set it in the .env file.")
#     st.stop()

# # Streamlit app UI
# st.title("Course Recommender System")
# st.write("This app retrieves course recommendations based on your query using embeddings and GPT for enhanced responses.")

# # User query input
# user_query = st.text_input("Enter your query (e.g., 'I want machine learning courses'):")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Path to local JSON file with embeddings
#         json_file_path = "all_embeddings.json"  # Ensure this file exists in your project

#         # Call the enhanced recommendation function
#         enhanced_response = get_enhanced_recommendations(
#             query_text=user_query,
#             json_file=json_file_path,
#             top_k=5  # Fetch the top 5 results
#         )

#         # Load embeddings from the JSON file
#         with open(json_file_path, "r") as json_file:
#             all_embeddings = json.load(json_file)

#         if all_embeddings:
#             # Display contextual data
#             st.write("### Contextual Data Retrieved:")
            
#             contextual_data = [
#                 {
#                     "Course Title": item["metadata"].get("Course Title", "N/A"),
#                     "Rating": item["metadata"].get("Rating", "N/A"),
#                     "Level": item["metadata"].get("Level", "N/A"),
#                     "Instructor": item["metadata"].get("Instructor", "N/A"),
#                     "Duration": item["metadata"].get("Duration to complete (Approx.)", "N/A")
#                 }
#                 for item in all_embeddings[:5]  # Display top 5 results
#             ]

#             # Render the contextual data dynamically
#             for idx, course in enumerate(contextual_data, start=1):
#                 st.write(f"**Result {idx}:**")
#                 st.write(f"- **Course Title:** {course['Course Title']}")
#                 st.write(f"- **Rating:** {course['Rating']}")
#                 st.write(f"- **Level:** {course['Level']}")
#                 st.write(f"- **Instructor:** {course['Instructor']}")
#                 st.write(f"- **Duration:** {course['Duration']} weeks")
#                 st.write("---")
#         else:
#             st.write("No embeddings found in the knowledge base.")

#         # Display enhanced recommendation response
#         st.write("### Enhanced Recommendation from GPT:")
#         if enhanced_response.strip():
#             st.write(enhanced_response)
#         else:
#             st.write("GPT could not generate a response. Please refine your query.")

#     except FileNotFoundError:
#         st.error(f"The file {json_file_path} was not found. Please ensure it exists in the specified path.")
#     except json.JSONDecodeError:
#         st.error("The JSON file is corrupted or not formatted correctly. Please check the file contents.")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}") -- working but NA


# import os
# import openai
# import streamlit as st
# import json
# from dotenv import load_dotenv
# from integrate_llm import get_enhanced_recommendations

# # Load environment variables
# load_dotenv()

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Check if the API key is loaded
# if not openai.api_key:
#     st.error("OpenAI API key not found. Please set it in the .env file.")
#     st.stop()

# # Streamlit app UI
# st.title("Course Recommender System")
# st.write("This app retrieves course recommendations based on your query using embeddings and GPT for enhanced responses.")

# # User query input
# user_query = st.text_input("Enter your query (e.g., 'I want machine learning courses'):")  # Input query

# if user_query:
#     st.write("Processing your query...")  # Display a message while processing
#     try:
#         # Path to local JSON file with embeddings
#         json_file_path = "all_embeddings.json"  # Make sure this file exists

#         # Call the enhanced recommendation function
#         enhanced_response, contextual_data = get_enhanced_recommendations(
#             query_text=user_query,
#             json_file=json_file_path,
#             top_k=5  # Fetch the top 5 results
#         )

#         # Load embeddings from the JSON file
#         with open(json_file_path, "r") as json_file:
#             all_embeddings = json.load(json_file)

#         if all_embeddings:
#             # Display contextual data
#             st.write("### Contextual Data Retrieved:")

#             # Iterate over the embeddings and display metadata
#             print(contextual_data)
#             for idx, item in enumerate(contextual_data, start=1):  # Display top 5 results

#                 st.write(f"**Result {idx}:**")
#                 st.write(f"- **Course Title:** {item.get('Course Title', 'N/A')}")
#                 st.write(f"- **Rating:** {item.get('Rating', 'N/A')}")
#                 st.write(f"- **Level:** {item.get('Level', 'N/A')}")
#                 st.write(f"- **Instructor:** {item.get('Instructor', 'N/A')}")
#                 st.write(f"- **Duration:** {item.get('Duration', 'N/A')} weeks")
                
#                 st.write("---")  # Separator for results
#         else:
#             st.write("No embeddings found in the knowledge base.")

#         # Display enhanced recommendation response
#         st.write("### Enhanced Recommendation from GPT:")
#         if enhanced_response.strip():
#             st.write(enhanced_response)
#         else:
#             st.write("GPT could not generate a response. Please refine your query.")

#     except FileNotFoundError:
#         st.error(f"The file {json_file_path} was not found. Please ensure it exists in the specified path.")
#     except json.JSONDecodeError:
#         st.error("The JSON file is corrupted or not formatted correctly. Please check the file contents.")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}") ## perfect code

import os
import openai
import streamlit as st
import json
from dotenv import load_dotenv
from integrate_llm import get_enhanced_recommendations

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded
if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in the .env file.")
    st.stop()

# Add custom CSS for background color
st.markdown(
    """
    <style>
    /* Set the background color for the whole page */
    .main {
        background-color: #f5f5f5; /* Light gray */
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app UI
st.title("Course Recommender System")
st.write("This app retrieves course recommendations based on your query using embeddings and GPT for enhanced responses.")

# User query input
user_query = st.text_input("Enter your query (e.g., 'I want machine learning courses'):")  # Input query

if user_query:
    st.write("Processing your query...")  # Display a message while processing
    try:
        # Path to local JSON file with embeddings
        json_file_path = "all_embeddings.json"  # Make sure this file exists

        # Call the enhanced recommendation function
        enhanced_response, contextual_data = get_enhanced_recommendations(
            query_text=user_query,
            json_file=json_file_path,
            top_k=5  # Fetch the top 5 results
        )

        # Load embeddings from the JSON file
        with open(json_file_path, "r") as json_file:
            all_embeddings = json.load(json_file)

        if all_embeddings:
            # Display contextual data
            st.write("### Contextual Data Retrieved:")

            # Iterate over the embeddings and display metadata
            for idx, item in enumerate(contextual_data, start=1):  # Display top 5 results
                st.markdown(f"<h3 style='color:blue;'>Result {idx}:</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:green;'>- <b>Course Title:</b> {item.get('Course Title', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:orange;'>- <b>Rating:</b> {item.get('Rating', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:purple;'>- <b>Level:</b> {item.get('Level', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:red;'>- <b>Instructor:</b> {item.get('Instructor', 'N/A')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:teal;'>- <b>Duration:</b> {item.get('Duration', 'N/A')} weeks</p>", unsafe_allow_html=True)
                st.markdown("<hr>", unsafe_allow_html=True)  # Separator for results
        else:
            st.write("No embeddings found in the knowledge base.")

        # Display enhanced recommendation response
        st.write("### Enhanced Recommendation from GPT:")
        if enhanced_response.strip():
            st.markdown(f"<p style='color:darkblue;'>{enhanced_response}</p>", unsafe_allow_html=True)
        else:
            st.write("GPT could not generate a response. Please refine your query.")

    except FileNotFoundError:
        st.error(f"The file {json_file_path} was not found. Please ensure it exists in the specified path.")
    except json.JSONDecodeError:
        st.error("The JSON file is corrupted or not formatted correctly. Please check the file contents.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")




# import os
# import openai
# import streamlit as st
# from dotenv import load_dotenv
# from pinecone import Pinecone, ServerlessSpec

# # Load environment variables from .env file
# load_dotenv()

# # Set the OpenAI API key from the environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Initialize Pinecone client
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Specify your index name
# index_name = "course-recommend-proj"

# # Check if the index exists, and create it if not
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=1536,  # Adjust according to your embedding model's dimensions
#         metric='cosine',
#         spec=ServerlessSpec(cloud='aws', region='us-east-1')
#     )

# # Access the index
# index = pc.Index(index_name)

# # Streamlit UI
# st.title("Query Interface with Knowledge Base")
# st.write("This app retrieves responses based on your knowledge base from Pinecone.")

# # User input
# user_query = st.text_input("Enter your query:")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Generate the embedding for the user query using OpenAI's model
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",  # OpenAI model for embeddings
#             input=user_query
#         )
#         query_embedding = response['data'][0]['embedding']

#         # Query Pinecone with the embedding
#         results = index.query(
#             vector=query_embedding,  # The query vector
#             top_k=1,  # Return the top 1 most similar result
#             include_metadata=True  # Include metadata (if you have it)
#         )
        
#         # Extract the most relevant document from Pinecone
#         if results['matches']:
#             best_match = results['matches'][0]
#             metadata = best_match['metadata']  # Extract metadata dictionary
            
#             # Display structured information line by line
#             st.write("### Course Details")
#             st.write(f"**Course Title:** {metadata.get('Course Title', 'N/A')}")
#             st.write(f"**Rating:** {metadata.get('Rating', 'N/A')}")
#             st.write(f"**Level:** {metadata.get('Level', 'N/A')}")
#             st.write(f"**Instructor:** {metadata.get('Instructor', 'N/A')}")
#             st.write(f"**Duration:** {metadata.get('Duration to complete (Approx.)', 'N/A')} weeks")

#             # Provide a detailed description of the course
#             st.write("### Description")
#             st.write(metadata.get('Description', 'No description available.'))

#         else:
#             st.write("No relevant answers found in the knowledge base.")
        
#     except Exception as e:
#         st.write(f"Error: {str(e)}")



# import os ## This code works
# import openai
# import streamlit as st
# from dotenv import load_dotenv
# from pinecone import Pinecone, ServerlessSpec

# # Load environment variables from .env file
# load_dotenv()

# # Set the OpenAI API key from the environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Initialize Pinecone client
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# # Specify your index name
# index_name = "course-recommend-proj"

# # Check if the index exists, and create it if not
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=1536,  # Adjust according to your embedding model's dimensions
#         metric='cosine',
#         spec=ServerlessSpec(cloud='aws', region='us-east-1')
#     )

# # Access the index
# index = pc.Index(index_name)

# # Streamlit UI
# st.title("Query Interface with Knowledge Base")
# st.write("This app retrieves responses based on your knowledge base from Pinecone.")

# # User input
# user_query = st.text_input("Enter your query:")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Generate the embedding for the user query using OpenAI's model
#         response = openai.Embedding.create(
#             model="text-embedding-ada-002",  # OpenAI model for embeddings
#             input=user_query
#         )
#         query_embedding = response['data'][0]['embedding']

#         # Query Pinecone with the embedding
#         results = index.query(
#             vector=query_embedding,  # The query vector
#             top_k=1,  # Return the top 1 most similar result
#             include_metadata=True  # Include metadata (if you have it)
#         )
        
#         # Extract the most relevant document from Pinecone
#         if results['matches']:
#             best_match = results['matches'][0]
#             answer = best_match['metadata']['text']  # Assumes you stored the text as metadata
#             st.write("Answer:", answer)
#         else:
#             st.write("No relevant answers found in the knowledge base.")
        
#     except Exception as e:
#         st.write(f"Error: {str(e)}")

# import streamlit as st
# from integrate_llm import get_contextual_response

# # Streamlit UI
# st.title("Course Recommender System")
# st.write(
#     "This app provides contextual course recommendations based on your input query. "
#     "It retrieves relevant data from Pinecone and uses OpenAI to enhance the context."
# )

# # Parameters for the query
# top_k = st.slider("Number of results to retrieve:", min_value=1, max_value=10, value=5)
# user_query = st.text_input("Enter your query:")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         # Fetch contextual data
#         contextual_data = get_contextual_response(user_query, top_k=top_k)

#         # Display results
#         if contextual_data:
#             st.write(f"Top {top_k} contextual results:")
#             for idx, data in enumerate(contextual_data, start=1):
#                 st.write(f"### Result {idx}")
#                 st.write(f"**Course Title:** {data.get('Course Title', 'Not available')}")
#                 st.write(f"**Description:** {data.get('Description', 'Not available')}")
#                 st.write(f"**Level:** {data.get('Level', 'Not available')}")
#                 st.write(f"**Duration:** {data.get('Duration to complete (Approx.)', 'Not available')} weeks")
#                 st.write(f"**Rating:** {data.get('Rating', 'Not available')}")
#                 st.write("---")
#         else:
#             st.write("No relevant results found.")
#     except Exception as e:
#         st.error(f"Error: {e}")

# import streamlit as st
# from integrate_llm import get_recommendations

# # Streamlit UI
# st.title("Course Recommender System")
# st.write("Get personalized course recommendations based on your input query.")

# # Parameters for query
# top_k = st.slider("Number of results to retrieve:", min_value=1, max_value=10, value=3)
# user_query = st.text_input("Enter your query:")

# if user_query:
#     st.write("Processing your query...")
#     try:
#         results = get_recommendations(user_query, top_k=top_k)

#         if results['matches']:
#             st.write(f"Top {top_k} results:")
#             for idx, match in enumerate(results['matches'], start=1):
#                 metadata = match.get('metadata', {})
#                 st.write(f"### Result {idx}")
#                 st.write(f"**Title:** {metadata.get('Course Title', 'Not available')}")
#                 st.write(f"**Description:** {metadata.get('Description', 'Not available')}")
#                 st.write(f"**Level:** {metadata.get('Level', 'Not available')}")
#                 st.write(f"**Duration:** {metadata.get('Duration to complete (Approx.)', 'Not available')} weeks")
#                 st.write(f"**Rating:** {metadata.get('Rating', 'Not available')}")
#                 st.write(f"**Relevance Score:** {match['score']:.2f}")
#                 st.write("---")
#         else:
#             st.write("No results found.")
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
