from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import CLIPProcessor, CLIPModel
import os
from pinecone import Pinecone, Index, ServerlessSpec
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

# Import functions from external scripts
from extraction_files.extraction import (
    fetch_links_from_snowflake,
    scrape_webpage,
    clean_text,
    chunk_text,
    get_ada_embedding,
    upload_to_pinecone,
    mark_links_as_processed
)

from extraction_files.links import scrape_tech_links, insert_into_snowflake_bulk, BASE_URL, TECH_KEYWORDS

# Configure logging to print directly to the Airflow logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Pinecone and OpenAI configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
TEXT_INDEX_NAME = os.getenv("TEXT_INDEX_NAME")
IMAGE_INDEX_NAME = os.getenv("IMAGE_INDEX_NAME")
DIMENSION_TEXT = int(os.getenv("DIMENSION_TEXT"))
DIMENSION_IMAGE = int(os.getenv("DIMENSION_IMAGE"))
METRIC = os.getenv("METRIC")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create text index if not exists
if TEXT_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=TEXT_INDEX_NAME,
        dimension=DIMENSION_TEXT,
        metric=METRIC,
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    logging.info(f"Index '{TEXT_INDEX_NAME}' created successfully.")
else:
    logging.info(f"Index '{TEXT_INDEX_NAME}' already exists.")

# Create image index if not exists
if IMAGE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=IMAGE_INDEX_NAME,
        dimension=DIMENSION_IMAGE,
        metric=METRIC,
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    logging.info(f"Index '{IMAGE_INDEX_NAME}' created successfully.")
else:
    logging.info(f"Index '{IMAGE_INDEX_NAME}' already exists.")

text_index = pc.Index(TEXT_INDEX_NAME)
image_index = pc.Index(IMAGE_INDEX_NAME)

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize CLIP model and processor
def initialize_clip():
    """Initialize the CLIP model and processor."""
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

clip_model, clip_processor = initialize_clip()

# Function to generate embeddings for images
def embed_image(image_content, model, processor):
    img = Image.open(BytesIO(image_content)).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        image_embedding = model.get_image_features(**inputs).numpy().flatten()
    return image_embedding

def upsert_to_pinecone(index, embeddings):
    """
    Upserts embeddings to the specified Pinecone index.

    :param index: Pinecone index instance.
    :param embeddings: List of embeddings with metadata.
    """
    try:
        vectors = [
            {
                "id": embedding["id"],
                "values": embedding["values"],
                "metadata": embedding["metadata"],
            }
            for embedding in embeddings
        ]

        response = index.upsert(vectors)
        logging.info(f"Successfully upserted {len(vectors)} embeddings to index.")
    except Exception as e:
        logging.error(f"Error upserting to Pinecone index: {e}")


# Define the DAG
with DAG(
    dag_id='scraping_final_dag_with_images',
    default_args=default_args,
    description='DAG to scrape, process, and upload embeddings to Pinecone, including images',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Scrape links from GeeksforGeeks
    def scrape_links_task():
        logging.info("Scraping links from GeeksforGeeks...")
        tech_links = scrape_tech_links(BASE_URL, TECH_KEYWORDS)
        if tech_links:
            logging.info(f"Scraped {len(tech_links)} links.")
            insert_into_snowflake_bulk(tech_links)
        else:
            logging.info("No links were scraped.")

    # Task 2: Fetch new links from Snowflake
    def fetch_new_links_task(ti):
        logging.info("Fetching new links from Snowflake...")
        links = fetch_links_from_snowflake()  # Fetch only links with STATUS='NEW'
        logging.info(f"Links fetched: {links}")  # Log fetched links for debugging
        if links:
            logging.info(f"Fetched {len(links)} new links from Snowflake.")
            ti.xcom_push(key='links', value=links)
        else:
            logging.info("No new links to process.")

    def process_new_links_task(ti):
        links = ti.xcom_pull(key='links', task_ids='fetch_new_links')
        if not links:
            logging.warning("No links pulled from XCom. Exiting task.")
            return

        for article_id, page_url, title in links:
            try:
                logging.info(f"Processing link: {page_url} (ID: {article_id})")
                
                # Scrape content and images
                article_title, _, cleaned_content, text_chunks, image_urls = scrape_webpage(page_url, extract_images=True)

                # Filter and process only .png images
                image_embeddings = []
                png_image_urls = [url for url in image_urls if url.lower().endswith('.png')]

                for idx, img_url in enumerate(png_image_urls):
                    try:
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        response = requests.get(img_url, headers=headers, stream=True)
                        if response.status_code == 200:
                            img_embedding = embed_image(response.content, clip_model, clip_processor)
                            image_embeddings.append({
                                "id": f"{article_id}-image-{idx}",
                                "values": img_embedding.tolist(),
                                "metadata": {
                                    "article_id": article_id,
                                    "image_id": idx,
                                    "title": article_title,
                                    "type": "image",
                                    "url": img_url
                                }
                            })
                            logging.info(f"Processed .png image: {img_url}")
                        else:
                            logging.warning(f"Failed to download image: {img_url}, Status Code: {response.status_code}")
                    except Exception as e:
                        logging.error(f"Error processing image {img_url}: {e}")

                if image_embeddings:
                    upsert_to_pinecone(image_index, image_embeddings)
                    logging.info(f"Uploaded {len(image_embeddings)} image embeddings for article ID {article_id}.")

                # Process text embeddings
                text_embeddings = []
                for idx, chunk in enumerate(text_chunks):
                    embedding = get_ada_embedding(chunk)
                    if embedding:
                        text_embeddings.append({
                            "id": f"{article_id}-text-{idx}",
                            "values": embedding,
                            "metadata": {
                                "article_id": article_id,
                                "chunk_id": idx,
                                "title": article_title,
                                "type": "text",
                                "url": page_url
                            }
                        })

                if text_embeddings:
                    upsert_to_pinecone(text_index, text_embeddings)
                    logging.info(f"Uploaded {len(text_embeddings)} text embeddings for article ID {article_id}.")

                mark_links_as_processed([article_id])
                logging.info(f"Marked link ID {article_id} as processed.")

            except Exception as e:
                logging.error(f"Error processing link {page_url}: {e}")


    # Define tasks
    scrape_links = PythonOperator(
        task_id='scrape_links',
        python_callable=scrape_links_task,
    )

    fetch_new_links = PythonOperator(
        task_id='fetch_new_links',
        python_callable=fetch_new_links_task,
    )

    process_new_links = PythonOperator(
        task_id='process_new_links',
        python_callable=process_new_links_task,
        provide_context=True,  # Ensure Airflow provides the context if required
    )

    # Task dependencies
    scrape_links >> fetch_new_links >> process_new_links