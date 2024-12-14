from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import logging
import sys
import os

# Add the directory containing links.py to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import your script functions
from extraction_files.links import scrape_tech_links, insert_into_snowflake_bulk, BASE_URL, TECH_KEYWORDS

# Configure logging for the DAG
log_file = "airflow_scraping_log.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting Airflow DAG setup for scraping and storing links.")

# Default arguments for the DAG
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
    dag_id='scrape_and_store_links_dag',
    default_args=default_args,
    description='Scrape technology-related links and store them in Snowflake',
    schedule_interval='@daily',
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    def scrape_links_task(**kwargs):
        """
        Task to scrape links from GeeksforGeeks.
        Logs progress and stores scraped links in XCom.
        """
        logging.info("Starting the scrape_links_task.")
        try:
            links = scrape_tech_links(BASE_URL, TECH_KEYWORDS, max_links=100)
            if not links:
                logging.warning("No links scraped!")
                raise ValueError("No links were scraped!")
            logging.info(f"Scraped {len(links)} links successfully.")
            kwargs['ti'].xcom_push(key='scraped_links', value=links)
        except Exception as e:
            logging.error(f"Error in scrape_links_task: {e}")
            raise

    def store_links_task(**kwargs):
        """
        Task to store scraped links into Snowflake.
        Retrieves links from XCom and logs the storage process.
        """
        logging.info("Starting the store_links_task.")
        try:
            # Retrieve links from XCom
            scraped_links = kwargs['ti'].xcom_pull(key='scraped_links', task_ids='scrape_links_task')
            if not scraped_links:
                logging.warning("No links available in XCom for insertion into Snowflake!")
                raise ValueError("No scraped links found in XCom!")
            logging.info(f"Storing {len(scraped_links)} links into Snowflake.")
            insert_into_snowflake_bulk(scraped_links)
            logging.info("All links successfully stored in Snowflake.")
        except Exception as e:
            logging.error(f"Error in store_links_task: {e}")
            raise

    # Define tasks
    scrape_links = PythonOperator(
        task_id='scrape_links_task',
        python_callable=scrape_links_task,
        provide_context=True,
    )

    store_links = PythonOperator(
        task_id='store_links_task',
        python_callable=store_links_task,
        provide_context=True,
    )

    # Set task dependencies
    scrape_links >> store_links
