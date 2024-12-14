import requests
from bs4 import BeautifulSoup
import snowflake.connector
import os
import logging
from pinecone import Pinecone, Index, ServerlessSpec
from nltk.tokenize import sent_tokenize
import nltk
from dotenv import load_dotenv
import re
import openai
import time
import random

logging.basicConfig(filename='scraping_pinecone_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

nltk.download('punkt')
nltk.data.path.append('/Users/nishitamatlani/nltk_data')  # Update with your NLTK data path

load_dotenv()

SNOWFLAKE_CONFIG = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA'),
}

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
TEXT_INDEX_NAME = os.getenv("TEXT_INDEX_NAME")
DIMENSION = int(os.getenv("DIMENSION_TEXT"))
METRIC = os.getenv("METRIC")
openai.api_key = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT or not openai.api_key:
    logging.error("API keys missing in environment variables.")
    exit(1)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
if TEXT_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=TEXT_INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    logging.info(f"Index '{TEXT_INDEX_NAME}' created successfully.")
else:
    logging.info(f"Index '{TEXT_INDEX_NAME}' already exists.")

text_index = pc.Index(TEXT_INDEX_NAME)

nltk.download("punkt")


def fetch_links_from_snowflake():
    try:
        logging.info("Connecting to Snowflake to fetch links.")
        connection = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cursor = connection.cursor()
        
        query = 'SELECT ID, LINK, TITLE FROM TECH_LINKS WHERE STATUS = \'NEW\''
        logging.info(f"Executing query: {query}")
        cursor.execute(query)
        
        links = cursor.fetchall()
        logging.info(f"Fetched links: {links}")  # Log the actual rows fetched
        
        cursor.close()
        connection.close()
        logging.info(f"Fetched {len(links)} links from Snowflake.")
        return links
    except snowflake.connector.Error as e:
        logging.error(f"Error while fetching links from Snowflake: {e}")
        return []
    
#  Update the STATUS of processed links in Snowflake to 'PROCESSED'.
def mark_links_as_processed(link_ids):
    connection = None
    cursor = None

    try:
        if not isinstance(link_ids, list) or not all(isinstance(link_id, int) for link_id in link_ids):
            logging.error("Invalid link_ids provided. Expected a list of integers.")
            raise ValueError("link_ids must be a list of integers.")

        # Check if there are IDs to process
        if not link_ids:
            logging.info("No link IDs provided for processing. Skipping update.")
            return

        # Connect to Snowflake
        logging.info(f"Connecting to Snowflake to update {len(link_ids)} processed links.")
        connection = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cursor = connection.cursor()

        # Debug log for IDs being processed
        logging.debug(f"Processing link IDs: {link_ids}")

        # Update query
        update_query = "UPDATE TECH_LINKS SET STATUS = 'PROCESSED' WHERE ID = %s"
        cursor.executemany(update_query, [(link_id,) for link_id in link_ids])
        connection.commit()
        logging.info(f"Successfully updated {len(link_ids)} links to PROCESSED.")
        return True

    except snowflake.connector.Error as e:
        logging.error(f"Error updating link statuses in Snowflake for IDs: {link_ids}. Error: {e}")
        raise  
    except Exception as e:
        logging.error(f"Unexpected error in mark_links_as_processed: {e}")
        raise  
    finally:
        try:
            if cursor:
                cursor.close()
                logging.debug("Snowflake cursor closed.")
            if connection:
                connection.close()
                logging.debug("Snowflake connection closed.")
        except Exception as cleanup_error:
            logging.warning(f"Error during cleanup: {cleanup_error}")
        return False


#Scraping Webpages
def scrape_webpage(page_url, extract_images=False):
    try:
        logging.info(f"Starting to scrape URL: {page_url}")
        
        # Fetch the webpage
        response = requests.get(page_url, timeout=10)
        logging.info(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None, None, None, None, None
        
        logging.info(f"Extracted HTML content (first 500 chars): {response.text[:500]}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Clean unwanted elements
        for unwanted in soup.find_all(class_=["header-main__wrapper", "similarReadDropdownItem", "leftbar-dropdown", "footer-wrapper_links"]):
            unwanted.decompose()
        hslider = soup.find('ul', id='hslider')
        if hslider:
            hslider.decompose()

        # Extract the title
        title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else "Untitled"
        title_keywords = [word.lower() for word in title.split()]  # Generate keywords from title

        # Extract main content
        content = []
        for element in soup.body.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ol', 'ul'], recursive=True):
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                content.append(f"{element.get_text(strip=True)}\n")
            elif element.name in ['p', 'ol', 'ul']:
                content.append(f"{element.get_text(strip=True)}\n")
        full_text = " ".join(content)

        # Clean the extracted content
        cleaned_text = clean_text(full_text)  

        # Chunk the text
        text_chunks = chunk_text(cleaned_text)  

        # Extract image URLs 
        image_urls = []
        if extract_images:
            images = soup.find_all('img')
            image_urls = [img['src'] for img in images if 'src' in img.attrs]

        logging.info(f"Successfully scraped content for URL: {page_url}")
        return title, title_keywords, cleaned_text, text_chunks, image_urls

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error while scraping {page_url}: {req_err}")
    except Exception as e:
        logging.error(f"Unexpected error scraping page {page_url}: {e}")

    return None, None, None, None, None


# Function to clean text
def clean_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Function to chunk text
def chunk_text(text, max_chars=500, overlap_sentences=1):
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

# Generate an embedding for the text using OpenAI's Ada embedding model.
def get_ada_embedding(text):
    try:
        logging.info(f"Generating embedding for text: {text[:100]}...")  # Log first 100 characters of text
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        logging.info(f"Received embedding response: {response}")  
        return response["data"][0]["embedding"]
    except Exception as e:
        logging.error(f"Error generating ADA embedding for text: {e}")
        return None


# Function to upload embeddings to Pinecone
def upload_to_pinecone(embeddings):
    try:
        text_index.upsert(vectors=embeddings)
        logging.info("Uploaded embeddings to Pinecone.")
    except Exception as e:
        logging.error(f"Error uploading embeddings to Pinecone: {e}")


# Main processing function
def process_links():
    links = fetch_links_from_snowflake()
    for article_id, page_url, title in links:
        article_title, text = scrape_webpage(page_url)
        if text:
            cleaned_text = clean_text(text)
            chunks = chunk_text(cleaned_text)
            embeddings = []
            for idx, chunk in enumerate(chunks):
                embedding = get_ada_embedding(chunk)
                if embedding:
                    embeddings.append({
                        "id": f"{article_id}-{idx}",
                        "values": embedding,
                        "metadata": {"article_id": article_id, "chunk_id": idx, "title": article_title, "text": chunk}
                    })
            if embeddings:
                upload_to_pinecone(embeddings)


# Example Execution
if __name__ == "__main__":
    logging.info("Starting the scraping and Pinecone upload process.")
    process_links()
    logging.info("Process completed.")