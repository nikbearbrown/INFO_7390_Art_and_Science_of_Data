import os
from dotenv import load_dotenv

load_dotenv()

import os
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = "fitness-assistant"
if index_name in [index['name'] for index in pc.list_indexes()]:
    print(f"Index '{index_name}' already exists. Skipping creation.")
else:
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Index '{index_name}' created successfully")

import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:  # If no event loop is available, create a new one
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
import time
from langchain_pinecone import PineconeEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document  # Import Document class

# Directory containing the data files
data_folder = "data"

# Ensure the folder exists
if not os.path.exists(data_folder):
    raise FileNotFoundError(f"Data folder '{data_folder}' does not exist.")

# Read files and load their content
documents = []

# Text splitter for general text (default chunk size is 1000 characters)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Process each file in the data folder
for filename in os.listdir(data_folder):
    filepath = os.path.join(data_folder, filename)
    
    # Skip non-text files
    if not filename.endswith(".txt"):
        continue
    
    with open(filepath, "r", encoding="utf-8") as file:
        file_content = file.read()
        
        # Split the content into chunks
        chunks = text_splitter.split_text(file_content)
        
        # Wrap each chunk in a Document object
        for chunk in chunks:
            documents.append(Document(page_content=chunk))

# Initialize a LangChain embedding object
model_name = "multilingual-e5-large"
async def create_embeddings():
    embeddings = PineconeEmbeddings(
        model=model_name,
        pinecone_api_key=os.environ.get("PINECONE_API_KEY")
    )
    return embeddings

embeddings = asyncio.run(create_embeddings())

# Embed and upsert the documents into Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=documents,
    index_name=index_name,
    embedding=embeddings,
    namespace="fitness-tips"
)

# Pause to allow Pinecone to process requests
time.sleep(1)

print(f"Successfully processed {len(documents)} text chunks from '{data_folder}' and uploaded embeddings to Pinecone.")

index = pc.Index(index_name)
namespace = "fitnessassistant"

for ids in index.list(namespace=namespace):
    query = index.query(
        id=ids[0],
        namespace=namespace,
        top_k=1,
        include_values=True,
        include_metadata=True
    )
    print(query)

from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize a LangChain object for chatting with the LLM
# without knowledge from Pinecone.
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.0)

# Initialize a LangChain object for chatting with the LLM
# with knowledge from Pinecone.
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever()
)

def query_index(query):
    print(f"query - ***\n{query}***")
    return qa.invoke(query).get("result")
