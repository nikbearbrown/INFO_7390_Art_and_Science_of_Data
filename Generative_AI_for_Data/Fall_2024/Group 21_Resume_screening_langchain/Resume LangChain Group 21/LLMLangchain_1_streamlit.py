# import streamlit as st
# import openai
# from pinecone import Pinecone, ServerlessSpec
# from PyPDF2 import PdfReader  # For extracting text from PDFs
 
# # Initialize OpenAI API
# openai.api_key = "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"
 
# # Initialize Pinecone API
# pinecone_api_key = "pcsk_6JH24x_KS4QjYfKYKppLDKLfcEwZNviWhKrMZBeqGDTuMAi8ANmcGobmrxZ6C3nSRCcGPz"
# pinecone_env = "us-west-1"  # Replace with your environment (e.g., "us-west-1" or "gcp-us-east1")
 
# pc = Pinecone(api_key=pinecone_api_key)
 
# # Define index name and specifications
# index_name = "langchain"
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=1536,  # Adjust dimension to your embedding size
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",  # Replace with your cloud provider
#             region=pinecone_env
#         )
#     )
 
# # Connect to the index
# index = pc.Index(name=index_name)
 
# # Streamlit App
# st.title("Resume Screening Tool")
# st.write("Upload resumes, extract key information, and evaluate candidates.")
 
# # File uploader for PDF
# uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
 
# if uploaded_file:
#     # Extract text from PDF
#     pdf_reader = PdfReader(uploaded_file)
#     pdf_text = ""
#     for page in pdf_reader.pages:
#         pdf_text += page.extract_text()
 
#     # Display the extracted text
#     st.write("Extracted PDF Content:")
#     st.text_area("PDF Content", pdf_text, height=200)
 
#     # Generate embeddings for the PDF content and store in Pinecone
#     if st.button("Process PDF"):
#         st.write("Clearing old data and processing the PDF...")
#         # Delete existing data in the index
#         index.delete(delete_all=True)  # Clears the entire index
 
#         # Split PDF text into chunks to fit embedding token limits
#         chunk_size = 800  # Adjust based on OpenAI token limit
#         chunks = [pdf_text[i:i+chunk_size] for i in range(0, len(pdf_text), chunk_size)]
 
#         # Generate embeddings for each chunk and upsert to Pinecone
#         for idx, chunk in enumerate(chunks):
#             response = openai.Embedding.create(
#                 input=[chunk],  # Input must be a list
#                 model="text-embedding-ada-002"
#             )
#             embedding = response['data'][0]['embedding']
#             index.upsert([
#                 {"id": f"doc_chunk_{idx}", "values": embedding, "metadata": {"text": chunk}}
#             ])
#         st.success("PDF content processed and stored in Pinecone.")
 
# # Input for user query
# query = st.text_input("Enter your query:")
 
# if st.button("Evaluate Candidate"):
#     if query:
#         # Generate embedding for the query
#         response = openai.Embedding.create(
#             input=[query],  # Input must be a list
#             model="text-embedding-ada-002"
#         )
#         query_embedding = response['data'][0]['embedding']
 
#         # Query Pinecone for relevant context
#         query_result = index.query(
#             vector=query_embedding,
#             top_k=5,
#             include_metadata=True
#         )
 
#         # Combine contexts
#         context = "\n\n".join([match['metadata'].get('text', '') for match in query_result['matches']])
 
#         # Generate GPT-4 response
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant who answers questions based on uploaded documents."},
#                 {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
#             ],
#             max_tokens=300,
#             temperature=0.5
#         )
 
#         # Display the response
#         st.write(f"Your query: {query}")
#         st.write("Response:")
#         st.write(response['choices'][0]['message']['content'].strip())
#     else:
#         st.write("Please enter a query!")

import streamlit as st
import openai
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
 
# Access API keys securely from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
pinecone_env = st.secrets["PINECONE_ENV"]
 
# Initialize OpenAI API
openai.api_key = openai_api_key
 
# Initialize Pinecone API
pc = Pinecone(api_key=pinecone_api_key)
 
# Define index name and specifications
index_name = "langchain"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=pinecone_env
        )
    )
 
# Connect to the index
index = pc.Index(name=index_name)
 
# Streamlit App
st.title("Resume Screening Tool")
st.write("Upload resumes, extract key information, and evaluate candidates.")
 
# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
 
if uploaded_file:
    # Extract text from PDF
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
 
    # Display the extracted text
    st.write("Extracted PDF Content:")
    st.text_area("PDF Content", pdf_text, height=200)
 
    # Generate embeddings for the PDF content and store in Pinecone
    if st.button("Process PDF"):
        st.write("Clearing old data and processing the PDF...")
        index.delete(delete_all=True)
 
        # Split PDF text into chunks to fit embedding token limits
        chunk_size = 800
        chunks = [pdf_text[i:i+chunk_size] for i in range(0, len(pdf_text), chunk_size)]
 
        for idx, chunk in enumerate(chunks):
            response = openai.Embedding.create(
                input=[chunk],
                model="text-embedding-ada-002"
            )
            embedding = response['data'][0]['embedding']
            index.upsert([
                {"id": f"doc_chunk_{idx}", "values": embedding, "metadata": {"text": chunk}}
            ])
        st.success("PDF content processed and stored in Pinecone.")
 
query = st.text_input("Enter your query:")
 
if st.button("Evaluate Candidate"):
    if query:
        response = openai.Embedding.create(
            input=[query],
            model="text-embedding-ada-002"
        )
        query_embedding = response['data'][0]['embedding']
 
        query_result = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )
 
        context = "\n\n".join([match['metadata'].get('text', '') for match in query_result['matches']])
 
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who answers questions based on uploaded documents."},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            max_tokens=300,
            temperature=0.5
        )
 
        st.write(f"Your query: {query}")
        st.write("Response:")
        st.write(response['choices'][0]['message']['content'].strip())
    else:
        st.write("Please enter a query!")
