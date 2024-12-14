import os
import streamlit as st
import PyPDF2
import textwrap
from pymilvus import Collection, DataType, utility, connections
import openai

# Environment Variables (Ensure these are set correctly)
openai_api_key = st.secrets["OPENAI_API_KEY"]
zilliz_cloud_uri = os.environ["ZILLIZ_CLOUD_URI"] = "https://in03-f2db10c5f456b31.serverless.gcp-us-west1.cloud.zilliz.com"
zilliz_cloud_api_key = os.environ["ZILLIZ_CLOUD_API_KEY"] = "98807cbae03002ff10c5a6f14d3959c6dfad9a01127f351cbd0701e45b62751522a9e8acb409eb6f4fbcf6417595000b4df67623"

# Initialize Milvus Connection
def initialize_milvus():
    try:
        connections.connect(
            alias="default",
            uri=os.environ["ZILLIZ_CLOUD_URI"],
            token=os.environ["ZILLIZ_CLOUD_API_KEY"]
        )
        st.info("Successfully connected to Milvus.")
        return True
    except Exception as e:
        st.error(f"Failed to connect to Milvus: {e}")
        return False

# Extract text from uploaded PDFs
def extract_text_from_uploaded_pdfs(uploaded_files):
    extracted_text = {}
    for uploaded_file in uploaded_files:
        text = ""
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            extracted_text[uploaded_file.name] = text.strip()
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")
    return extracted_text

# Chunk text for embeddings
def chunk_text(text, chunk_size=1000):
    return textwrap.wrap(text, chunk_size)

# Generate OpenAI embeddings
def generate_embeddings(text_chunks):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    embeddings = []
    for chunk in text_chunks:
        try:
            response = openai.Embedding.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embeddings.append(response['data'][0]['embedding'])
        except Exception as e:
            st.error(f"Error generating embedding for chunk: {chunk[:50]}...: {e}")
    return embeddings

# Store data in Milvus
def store_in_milvus(collection_name, extracted_text):
    try:
        # Check if the collection exists, if not create it
        if not utility.has_collection(collection_name):
            schema = {
                "fields": [
                    {"name": "id", "type": DataType.INT64, "is_primary": True},
                    {"name": "vector", "type": DataType.FLOAT_VECTOR, "dim": 1536},
                    {"name": "text", "type": DataType.VARCHAR, "max_length": 65535}
                ]
            }
            collection = Collection(name=collection_name, schema=schema)
            st.info(f"Collection '{collection_name}' created.")
        else:
            collection = Collection(collection_name)

        data = []
        id_counter = 0
        for file, text in extracted_text.items():
            chunks = chunk_text(text)
            embeddings = generate_embeddings(chunks)
            for chunk, embedding in zip(chunks, embeddings):
                data.append([id_counter, embedding, chunk])
                id_counter += 1

        # Insert data into Milvus
        if data:
            insert_results = collection.insert(data)
            st.success(f"Inserted {len(insert_results.primary_keys)} records into Milvus collection '{collection_name}'.")
        else:
            st.warning("No data to insert.")
    except Exception as e:
        st.error(f"Failed to store data in Milvus: {e}")

# Query Milvus
def query_milvus(collection_name, query_text, top_k=5):
    try:
        if not utility.has_collection(collection_name):
            st.error("Collection does not exist. Please process and store PDFs first.")
            return []

        collection = Collection(collection_name)
        query_embedding = generate_embeddings([query_text])[0]
        results = collection.search(
            data=[query_embedding],
            anns_field="vector",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k
        )
        if not results or len(results[0]) == 0:
            st.warning("No results found for your query.")
            return []

        return results[0]
    except Exception as e:
        st.error(f"Failed to query Milvus: {e}")
        return []

# Streamlit App
st.title("Windows 11 error Bot")

# Initialize Milvus
if not initialize_milvus():
    st.stop()

# Upload PDFs
uploaded_files = st.file_uploader("Upload your PDF files", type="pdf", accept_multiple_files=True)
if uploaded_files:
    st.write("Processing uploaded PDFs...")
    extracted_text = extract_text_from_uploaded_pdfs(uploaded_files)
    st.write("Extracted Text:", extracted_text)  # Debugging: View extracted content

    if st.button("Store PDFs in Vector Database"):
        store_in_milvus("my_rag_collection", extracted_text)

# Query the database
query = st.text_input("Ask a question:")
if query and st.button("Search"):
    results = query_milvus("my_rag_collection", query)
    for result in results:
        st.write(f"Text: {result.entity.get('text', 'N/A')} (Score: {result.distance:.4f})")
