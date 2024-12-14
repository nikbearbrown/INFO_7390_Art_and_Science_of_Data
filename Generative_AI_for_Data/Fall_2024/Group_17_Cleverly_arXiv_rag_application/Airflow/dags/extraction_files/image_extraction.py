import requests
from bs4 import BeautifulSoup
from transformers import CLIPProcessor, CLIPModel
from openai.embeddings_utils import get_embedding
from pinecone import Pinecone, ServerlessSpec
from nltk.tokenize import sent_tokenize
import torch
import os
import openai
from huggingface_hub import login
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Pinecone instance
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define Pinecone index configurations
TEXT_INDEX_NAME = os.getenv("TEXT_INDEX_NAME", "text-gfg-index")
IMAGE_INDEX_NAME = os.getenv("IMAGE_INDEX_NAME", "image-index")
TEXT_INDEX_DIMENSION = int(os.getenv("TEXT_INDEX_DIMENSION", 1536))  
IMAGE_INDEX_DIMENSION = int(os.getenv("IMAGE_INDEX_DIMENSION", 512))  
METRIC = os.getenv("METRIC", "cosine")
SPEC = ServerlessSpec(cloud="aws", region="us-east-1")  

# Pinecone index exists
def initialize_pinecone_index(index_name, dimension):
    if index_name not in pc.list_indexes().names():
        print(f"Index '{index_name}' does not exist. Creating it now...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=METRIC,
            spec=SPEC
        )
        print(f"Index '{index_name}' created successfully.")
    return pc.Index(index_name)

# Connect to Pinecone indices
text_index = initialize_pinecone_index(TEXT_INDEX_NAME, TEXT_INDEX_DIMENSION)
image_index = initialize_pinecone_index(IMAGE_INDEX_NAME, IMAGE_INDEX_DIMENSION)

# Chunk text function
def chunk_pdtext(text, max_chars=500, overlap_sentences=1):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_char_count = 0
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        if current_chunk_char_count + len(sentence) > max_chars:
            chunks.append(" ".join(current_chunk).strip())
            current_chunk = current_chunk[-overlap_sentences:]
            current_chunk_char_count = sum(len(s) for s in current_chunk)
        current_chunk.append(sentence)
        current_chunk_char_count += len(sentence)
        i += 1
    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())
    return chunks

# Clean extracted content
def clean_content(content):
    lines = content.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("👉🏽") and not line.startswith("Similar Reads"):
            cleaned_lines.append(line)
    return " ".join(cleaned_lines)

# Validate if the image URL is valid
def is_valid_image_url(url):
    """
    Validate if the given URL is a valid image URL.
    """
    if not url.startswith(('http://', 'https://')):
        return False

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    if not any(url.lower().endswith(ext) for ext in valid_extensions):
        return False

    return True

def normalize_url(base_url, img_url):
    """
    Normalize image URL by adding a scheme if missing.
    """
    if img_url.startswith('/'):
        return f"{base_url.rstrip('/')}{img_url}"
    return img_url

# Function to generate embeddings for images
def embed_image(image_content, model, processor):
    img = Image.open(BytesIO(image_content)).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        image_embedding = model.get_image_features(**inputs).numpy().flatten()
    return image_embedding

# Function to upsert embedding and metadata to Pinecone
def upsert_to_pinecone(index, embedding, image_url):
    metadata = {"image_url": image_url}
    index.upsert([{"id": os.path.basename(image_url.split("?")[0]), "values": embedding.tolist(), "metadata": metadata}])

# Initialize CLIP model and processor
def initialize_clip():
    try:
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        return model, processor
    except Exception as e:
        print(f"Failed to initialize CLIP: {e}")
        exit()

# Scrape and process data
def scrape_and_store(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for unwanted in soup.find_all(class_=["header-main__wrapper", "similarReadDropdownItem", "leftbar-dropdown", "footer-wrapper_links"]):
            unwanted.decompose()
        hslider = soup.find('ul', id='hslider')
        if hslider:
            hslider.decompose()

        # Extract title and content
        title = soup.find('h1').get_text(strip=True)
        title_keywords = [word.lower() for word in title.split()]
        content = []
        for element in soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ol', 'ul'], recursive=True):
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                content.append(f"{element.get_text(strip=True)}\n")
            elif element.name in ['p', 'ol', 'ul']:
                content.append(f"{element.get_text(strip=True)}\n")
        full_text = " ".join(content)

        # Clean the extracted content
        cleaned_text = clean_content(full_text)

        # Chunk the text
        text_chunks = chunk_pdtext(cleaned_text)

        # Scan the webpage for images
        images = soup.find_all('img')
        relevant_image_links = []
        for img in images:
            if 'src' in img.attrs:
                src = img['src']
                if any(keyword in src.lower() for keyword in title_keywords):
                    relevant_image_links.append(src)

        for i, chunk in enumerate(text_chunks):
            metadata = {
                "title": title,
                "chunk_index": i,
                "type": "text",
                "source_url": url,
                "content": chunk
            }
            text_embedding = get_embedding(chunk, engine="text-embedding-ada-002")
            text_index.upsert([(f"{title}-text-{i}", text_embedding, metadata)])

        for i, img_url in enumerate(relevant_image_links):
            try:
                img_response = requests.get(img_url, stream=True)
                if img_response.status_code == 200:
                    img_embedding = embed_image(img_response.content, clip_model, clip_processor)
                    metadata = {
                        "title": title,
                        "image_url": img_url,
                        "type": "image",
                        "source_url": url
                    }
                    image_index.upsert([(f"{title}-image-{i}", img_embedding, metadata)])
            except Exception as e:
                print(f"Error processing image {img_url}: {e}")

        print("Data successfully stored in Pinecone.")
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)

# URL to scrape
if __name__ == "__main__":
    clip_model, clip_processor = initialize_clip()
    url = "https://www.geeksforgeeks.org/what-is-exploratory-data-analysis/"
    scrape_and_store(url)
