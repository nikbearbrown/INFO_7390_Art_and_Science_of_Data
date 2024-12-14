from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
import json  # Fix: Add this missing import
from news_fetcher import fetch_news
from push_to_qdrant import push_to_qdrant
from gpt_handler import query_qdrant_and_generate_response

# Default DAG arguments
default_args = {
    'owner': 'ajinabraham',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Task 1: Fetch news and save to news_output.json
def fetch_and_save_news(**kwargs):
    """
    Fetch news articles dynamically based on the category and university name provided.
    """
    # Get parameters from the DAG configuration
    query_params = kwargs.get("dag_run").conf or {}
    category = query_params.get("category", "General News")
    university = query_params.get("university", "University of Texas")
    
    # Generate query using category and university
    query = f"{category} {university}"
    
    # Fetch news based on the query
    news_data = fetch_news(query=query, country="us")
    
    # Save news data
    news_output_path = "/opt/airflow/logs/news_output.json"
    os.makedirs(os.path.dirname(news_output_path), exist_ok=True)
    with open(news_output_path, 'w') as f:
        json.dump(news_data, f, indent=4)
    
    print(f"News saved to {news_output_path}")


# Task 2: Push data to Qdrant
def push_news_to_qdrant(**kwargs):
    """
    Read `news_output.json` and push its content to Qdrant.
    """
    push_to_qdrant()  # Using function from push_to_qdrant.py
    print("News data pushed to Qdrant.")

# Task 3: Query Qdrant and GPT
def query_and_save_gpt_response(**kwargs):
    """
    Query Qdrant for relevant articles and generate a GPT response.
    Save the GPT response to `gpt_response.json`.
    """
    query_text = "education news updates"
    response = query_qdrant_and_generate_response(query_text=query_text)
    print(f"GPT response generated: {response}")

# Define the DAG
with DAG(
    'news_fetcher_pipeline',
    default_args=default_args,
    description='A DAG to fetch news, store in Qdrant, and use GPT for response generation',
    schedule_interval='@daily',
    start_date=datetime(2023, 12, 10),
    catchup=False,
) as dag:

    # Task 1: Fetch news
    fetch_news_task = PythonOperator(
        task_id='fetch_news',
        python_callable=fetch_and_save_news,
    )

    # Task 2: Push news to Qdrant
    push_to_qdrant_task = PythonOperator(
        task_id='push_to_qdrant',
        python_callable=push_news_to_qdrant,
    )

    # Task 3: Query Qdrant and GPT
    query_gpt_task = PythonOperator(
        task_id='query_qdrant_and_gpt',
        python_callable=query_and_save_gpt_response,
    )

    # Task dependencies
    fetch_news_task >> push_to_qdrant_task >> query_gpt_task
