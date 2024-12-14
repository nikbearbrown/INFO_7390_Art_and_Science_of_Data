from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from urllib.parse import urljoin

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

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='scraping_dag',
    default_args=default_args,
    description='DAG to scrape, process, and upload embeddings to Pinecone',
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
        """
        Process links by scraping their content, uploading embeddings, and updating the link status to 'PROCESSED'.
        """
        logging.info("Fetching links from XCom...")
        links = ti.xcom_pull(key='links', task_ids='fetch_new_links')
        if not links:
            logging.warning("No links pulled from XCom. Exiting task.")
            return

        for article_id, page_url, title in links:
            try:
                logging.info(f"Processing link: {page_url} (ID: {article_id})")
                
                # Scrape webpage content
                article_title, title_keywords, cleaned_content, text_chunks = scrape_webpage(page_url)
                if not cleaned_content or not text_chunks:
                    logging.warning(f"No content or chunks found for URL: {page_url}. Skipping.")
                    continue
                
                logging.info(f"Scraped article title: {article_title}")
                logging.info(f"Generated {len(text_chunks)} text chunks for embedding.")
                
                # Generate embeddings for each chunk
                embeddings = []
                for idx, chunk in enumerate(text_chunks):
                    embedding = get_ada_embedding(chunk)  # Assuming this is defined elsewhere
                    if embedding:
                        embeddings.append({
                            "id": f"{article_id}-{idx}",
                            "values": embedding,
                            "metadata": {
                                "article_id": article_id,
                                "chunk_id": idx,
                                "title": article_title,
                                "text": chunk,
                                "url": page_url  # Include the URL in metadata
                            }
                        })
                
                # Upload to Pinecone if embeddings are generated
                if embeddings:
                    upload_to_pinecone(embeddings)  # Assuming this is defined elsewhere
                    logging.info(f"Uploaded {len(embeddings)} embeddings for article ID {article_id}.")

                    # Update the status of the current link to 'PROCESSED'
                    mark_links_as_processed([article_id])
                    logging.info(f"Updated status of link ID {article_id} to 'PROCESSED'.")
                else:
                    logging.warning(f"No embeddings generated for URL: {page_url}. Skipping status update.")
            
            except Exception as e:
                logging.error(f"Error processing link {page_url} (ID: {article_id}): {e}")



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
    )

    # Task dependencies
    scrape_links >> fetch_new_links >> process_new_links
