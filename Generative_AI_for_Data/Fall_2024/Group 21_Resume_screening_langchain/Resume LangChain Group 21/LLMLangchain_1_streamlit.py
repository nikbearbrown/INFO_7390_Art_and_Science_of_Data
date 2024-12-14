import streamlit as st
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

# Validation to ensure API keys are present
if not all([openai_api_key, pinecone_api_key, pinecone_env]):
    st.error("Please set OPENAI_API_KEY, PINECONE_API_KEY, and PINECONE_ENV in your .env file")
    st.stop()

# Debugging: Print API keys (remove in production)
st.write(f"OpenAI API Key (last 4 chars): {openai_api_key[-4:] if openai_api_key else 'Not set'}")

# Initialize OpenAI Client with error handling
try:
    client = OpenAI(api_key=openai_api_key)
    # Verify API key by testing a simple call
    client.models.list()
except Exception as e:
    st.error(f"OpenAI API Authentication Error: {e}")
    st.error("Please check your OpenAI API key. Ensure it is correct and has the necessary permissions.")
    st.stop()
 
# Initialize Pinecone API
try:
    pc = Pinecone(api_key=pinecone_api_key)
except Exception as e:
    st.error(f"Pinecone API Initialization Error: {e}")
    st.stop()
 
# Define index name and specifications
index_name = "langchain"
namespace = "resume_screening"

# Check if index exists, if not create it
try:
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
except Exception as e:
    st.error(f"Pinecone Index Error: {e}")
    st.stop()
 
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
        
        # Delete vectors in the specific namespace
        try:
            index.delete(delete_all=True, namespace=namespace)
        except Exception as e:
            st.warning(f"Warning when deleting vectors: {e}")
 
        # Split PDF text into chunks to fit embedding token limits
        chunk_size = 800
        chunks = [pdf_text[i:i+chunk_size] for i in range(0, len(pdf_text), chunk_size)]
 
        try:
            for idx, chunk in enumerate(chunks):
                # Use the new OpenAI embeddings API
                response = client.embeddings.create(
                    input=[chunk],
                    model="text-embedding-ada-002"
                )
                embedding = response.data[0].embedding
                index.upsert([
                    {"id": f"doc_chunk_{idx}", "values": embedding, "metadata": {"text": chunk}}
                ], namespace=namespace)
            st.success("PDF content processed and stored in Pinecone.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
 
query = st.text_input("Enter your query:")
 
if st.button("Evaluate Candidate"):
    if query:
        try:
            # Generate query embedding
            response = client.embeddings.create(
                input=[query],
                model="text-embedding-ada-002"
            )
            query_embedding = response.data[0].embedding
 
            # Query Pinecone index
            query_result = index.query(
                vector=query_embedding,
                top_k=5,
                include_metadata=True,
                namespace=namespace
            )
 
            context = "\n\n".join([match['metadata'].get('text', '') for match in query_result['matches']])
 
            # Use chat completion with new API
            response = client.chat.completions.create(
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
            st.write(response.choices[0].message.content.strip())
        except Exception as e:
            st.error(f"Error processing query: {e}")
    else:
        st.write("Please enter a query!")
