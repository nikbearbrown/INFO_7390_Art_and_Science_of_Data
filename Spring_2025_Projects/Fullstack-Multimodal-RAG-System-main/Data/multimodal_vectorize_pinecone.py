# Install required packages
from langchain_opentutorial import package
from langchain_upstage import UpstageDocumentParseLoader
from langchain_core.documents import Document
from google.generativeai import configure, GenerativeModel
import base64
import os
import tempfile
from collections import defaultdict

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter  
from langchain_openai import OpenAIEmbeddings                       
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import pymupdf4llm
from google.cloud import storage

# Configure Google Generative AI
configure()

# Install required packages
package.install(
    [
        "pymupdf4llm",
        "langchain-upstage",
        "langchain-google-genai",
        "langchain-openai",
        "google-cloud-storage",
    ],
    verbose=False,
    upgrade=False,
)

# Load environment variables
load_dotenv()

# GCS bucket configuration
BUCKET_NAME = "cfa-pdfs"
FOLDER_PREFIX = "cfa_pdfs/"
PDF_FILES = ["peksevim_rf_brief_2025_online.pdf", "1706.03762v7.pdf"] # "beyond-active-and-passive.pdf"


# Function to download PDF from GCS bucket
def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}")
    return destination_file_name[8]

def sanitize_index_name(name):
    """Sanitize index name to comply with Pinecone naming restrictions."""
    # Replace underscores with dashes
    sanitized = name.replace('_', '-')
    # Ensure only lowercase alphanumeric and dashes
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '-').lower()
    return sanitized

# Function to create image descriptions
def create_image_descriptions(docs):
    model = GenerativeModel("gemini-2.5-pro-preview-03-25") #gemini-1.5-flash-8b 
    new_documents = []
    
    for doc in docs:
        if 'base64_encodings' in doc.metadata:
            for img_base64 in doc.metadata['base64_encodings']:
                try:
                    # Build the content package correctly
                    response = model.generate_content(
                        contents=[
                            {
                                "parts": [
                                    """
                                    Describe in exhaustive detail all factual content visible in the image.

                                    Instructions:

                                    1. If the image is decorative or non-informational, output only: <---image--->

                                    2. For content images, follow these rules:

                                    - General Images:
                                        - List every visible object, person, or entity, including their positions, colors, sizes, and spatial relationships.
                                        - Describe all actions, interactions, and the full context (foreground, background, setting, environment).
                                        - Transcribe all visible text, labels, or signage exactly as shown, using quotation marks.
                                        - Include any numbers, dates, or identifiers present.

                                    - Charts, Graphs, and Infographics:
                                        - State the chart/graph type (e.g., bar chart, line graph, scatter plot, pie chart).
                                        - List every axis label, unit, and scale, including axis ranges and tick values.
                                        - For each data series, describe its color/style and all data points with their exact values and labels.
                                        - Transcribe all legends, annotations, captions, and footnotes.
                                        - Describe any patterns, groupings, or outliers strictly as visible (do not interpret).

                                    - Tables:
                                        - Convert the entire table into markdown table format, preserving the exact row and column order, headers, and all cell values.
                                        - Include footnotes or superscripts if present.

                                    General Rules:
                                    - Include only what is directly observable-do not interpret, summarize, or omit details.
                                    - Use original numbers, text, and labels without modification.
                                    - Be as complete and specific as possible, even if the description is long.
                                    - For complex images, break down the description into logical sections (e.g., "Title," "Legend," "X-axis," "Data Points," etc.).
                                    """,
                                    {
                                        "mime_type": "image/png",
                                        "data": base64.b64decode(img_base64)
                                    }
                                ]
                            }
                        ]
                    )
                    
                    # Extract text safely
                    if response.candidates:
                        description = response.candidates[0].content.parts[0].text
                    else:
                        description = "<---image--->"
                        
                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    description = "<---image--->"
                
                new_documents.append(
                    Document(
                        page_content=description,
                        metadata={"page": doc.metadata.get("page", "unknown")}
                    )
                )
    
    return new_documents

# Function to merge text and images
def merge_text_and_images(md_text, image_description_docs):
    # Create a dictionary to collect data by page
    page_contents = defaultdict(list)
    page_metadata = {}
    
    # Process md_text
    for text_item in md_text:
        # Standardize page numbers to integer
        page = int(text_item['metadata']['page'])
        page_contents[page].append(text_item['text'])
        # Save metadata for each page
        if page not in page_metadata:
            page_metadata[page] = {
                'source': text_item['metadata']['file_path'],
                'page': page
            }
    
    # Process image_description_docs
    for img_doc in image_description_docs:
        # Standardize page numbers to integer
        page = int(img_doc.metadata.get('page', 0))  # Default to page 0 if missing
        page_contents[page].append(img_doc.page_content)
    
    # Create the final list of Document objects
    merged_docs = []
    for page in sorted(page_contents.keys()):
        # Combine all content of the page into a single string
        full_content = '\n\n'.join(page_contents[page])
        
        # Create a Document object
        doc = Document(
            page_content=full_content,
            metadata=page_metadata.get(page, {'page': page})
        )
        merged_docs.append(doc)
    
    return merged_docs

# Function to process a PDF and store in Pinecone
def process_pdf_to_pinecone(pdf_name):
    # Create a temporary directory for downloaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the PDF from GCS
        gcs_path = f"{FOLDER_PREFIX}{pdf_name}"
        local_file_path = os.path.join(temp_dir, pdf_name)
        download_from_gcs(BUCKET_NAME, gcs_path, local_file_path)
        
        print(f"Processing {pdf_name}...")
        
        # Extract markdown text
        md_text = pymupdf4llm.to_markdown(
            doc=local_file_path,
            page_chunks=True,
            show_progress=True,
        )
        
        # Parse document for text and images
        loader = UpstageDocumentParseLoader(
            local_file_path, 
            split="page", 
            output_format="markdown",
            base64_encoding=["figure", "chart", "table"]
        )
        docs = loader.load_and_split()
        
        # Create image descriptions
        image_description_docs = create_image_descriptions(docs)
        
        # Merge text and images
        merged_documents = merge_text_and_images(md_text, image_description_docs)
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(merged_documents)
        
        # Create or access Pinecone index (use filename without extension as index name)
        # Create or access Pinecone index (sanitize filename for index name)
        base_name = os.path.splitext(pdf_name)[0]
        index_name = sanitize_index_name(base_name)

        
        # Initialize Pinecone client
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        if not PINECONE_API_KEY:
            raise ValueError("Missing PINECONE_API_KEY in environment variables")
        
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if index exists, create if not
        existing_indexes = [i.name for i in pc.list_indexes()]
        if index_name not in existing_indexes:
            print(f"Creating new index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Store vectors in Pinecone
        print(f"Storing vectors in Pinecone index: {index_name}")
        vector_store = PineconeVectorStore.from_documents(
            documents=all_splits,
            embedding=embeddings,
            index_name=index_name
        )
        
        print(f"Successfully processed {pdf_name} and stored in Pinecone index: {index_name}")

# Main execution
def main():
    # Process each PDF
    for pdf_file in PDF_FILES:
        process_pdf_to_pinecone(pdf_file)
        print(f"Completed processing {pdf_file}")

if __name__ == "__main__":
    main()
