from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys
from dotenv import load_dotenv

# Add project path to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import functions from the provided scripts
from src.scrape_to_s3 import scrape_documents
from src.store_embeddings import process_documents

# Load environment variables
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    "f1_pipeline",
    default_args=default_args,
    description="F1 Data Processing Pipeline",
    schedule_interval=None,  # Trigger manually or set a schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Task 1: Scrape documents and upload to S3
def scrape_and_upload_to_s3():
    scrape_documents(os.getenv("url"))

scrape_task = PythonOperator(
    task_id="scrape_and_upload_to_s3",
    python_callable=scrape_and_upload_to_s3,
    dag=dag,
)

# Task 2: Process documents for embeddings and store in Pinecone
def process_documents_for_embeddings():
    process_documents()

embedding_task = PythonOperator(
    task_id="process_documents_for_embeddings",
    python_callable=process_documents_for_embeddings,
    dag=dag,
)

# Define task dependencies
scrape_task >> embedding_task