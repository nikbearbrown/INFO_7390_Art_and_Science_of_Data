import os
import logging
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
import time
import urllib.request
import ntplib
import subprocess

import snowflake.connector
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException

# Import environment variables
from env_var import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME,
    SNOWFLAKE_USER,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_WAREHOUSE,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_ROLE
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('snowflake_loader.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
os.environ['AWS_REGION'] = AWS_REGION
os.environ['AWS_BUCKET_NAME'] = AWS_BUCKET_NAME
os.environ['SNOWFLAKE_USER'] = SNOWFLAKE_USER
os.environ['SNOWFLAKE_PASSWORD'] = SNOWFLAKE_PASSWORD
os.environ['SNOWFLAKE_ACCOUNT'] = SNOWFLAKE_ACCOUNT
os.environ['SNOWFLAKE_WAREHOUSE'] = SNOWFLAKE_WAREHOUSE
os.environ['SNOWFLAKE_DATABASE'] = SNOWFLAKE_DATABASE
os.environ['SNOWFLAKE_SCHEMA'] = SNOWFLAKE_SCHEMA
os.environ['SNOWFLAKE_ROLE'] = SNOWFLAKE_ROLE

@dataclass
class SnowflakeConfig:
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    schema: str
    role: str

@dataclass
class AWSConfig:
    access_key_id: str
    secret_access_key: str
    region: str
    bucket: str

def sync_system_time() -> Tuple[bool, Optional[str]]:
    """
    Attempt to synchronize system time using NTP servers and, as a fallback, AWS time sync.
    Returns: (success: bool, error_message: Optional[str])
    """
    try:
        # First try using ntplib
        ntp_client = ntplib.NTPClient()
        ntp_servers = ['pool.ntp.org', 'time.google.com', 'time.windows.com', 'time.apple.com']

        for server in ntp_servers:
            try:
                response = ntp_client.request(server, timeout=2)
                offset = response.offset
                if abs(offset) > 300:  # 5 minutes
                    # Adjust system time only if skewed significantly (requires root)
                    new_time = datetime.fromtimestamp(response.tx_time)
                    subprocess.run(['sudo', 'date', '-s', new_time.strftime('%Y-%m-%d %H:%M:%S')],
                                   check=True, capture_output=True)
                return True, None  # Successfully synced time
            except Exception as e:
                continue

        # Fallback to AWS time sync if NTP servers are unavailable
        aws_time = get_aws_time()
        if aws_time:
            logger.info("System time synced using AWS instance metadata.")
            return True, None
        return False, "Could not sync with NTP servers or retrieve AWS time."
    except Exception as e:
        return False, str(e)

def setup_s3_client(aws_config: AWSConfig) -> boto3.client:
    max_retries = 3

    for attempt in range(max_retries):
        sync_success, error_msg = sync_system_time()
        if not sync_success:
            logger.warning(f"Time sync failed: {error_msg}")

        config = Config(
            retries={'max_attempts': 3, 'mode': 'adaptive'},
            connect_timeout=5,
            read_timeout=10
        )

        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_config.access_key_id,
                aws_secret_access_key=aws_config.secret_access_key,
                region_name=aws_config.region,
                config=config
            )

            # Attempt to make an API call to verify time skew is resolved
            s3_client.list_buckets()
            logger.info(f"Successfully set up S3 client for bucket: {aws_config.bucket}")
            return s3_client

        except ClientError as e:
            if e.response['Error']['Code'] == 'RequestTimeTooSkewed' and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Time skew detected; retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue  # Retry after waiting
            else:
                logger.error("Failed to resolve time skew after maximum retries")
                raise
        except Exception as e:
            logger.error(f"Error setting up S3 client: {e}")
            raise

def get_aws_time() -> Optional[datetime]:
    """Get current time from AWS Time Sync service."""
    try:
        response = urllib.request.urlopen(
            'http://169.254.169.123/latest/meta-data/instance-identity/document',
            timeout=1
        )
        instance_data = json.loads(response.read().decode('utf-8'))
        if 'pendingTime' in instance_data:
            return datetime.strptime(instance_data['pendingTime'], '%Y-%m-%dT%H:%M:%SZ')
    except:
        return None

def process_metadata(metadata: Dict[str, Any], bucket: str) -> Dict[str, Any]:
    """Process metadata and construct required fields."""
    try:
        folder_name = metadata['url'].split('/')[-1]
        
        image_url = f"https://{bucket}.s3.amazonaws.com/{folder_name}/cover.jpg" if metadata.get('has_image') else ''
        pdf_url = f"https://{bucket}.s3.amazonaws.com/{folder_name}/full-text.pdf" if metadata.get('has_pdf') else ''
        
        summary = metadata.get('summary', "Summary will be updated") if metadata.get('has_summary') else "Summary not available"
        
        return {
            'TITLE': metadata.get('title', 'Unknown Title'),
            'SUMMARY': summary,
            'IMAGE_URL': image_url,
            'PDF_URL': pdf_url,
            'URL': metadata.get('url', ''),
            'S3_BUCKET': bucket
        }
    except Exception as e:
        logger.error(f"Error processing metadata: {e}")
        raise

@task
def create_snowflake_table():
    """Task to create Snowflake table."""
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse='BIGDATA7245',  # Changed to BIGDATA7245
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE
        )
        
        with conn.cursor() as cursor:
            # Resume warehouse explicitly
            cursor.execute("ALTER WAREHOUSE BIGDATA7245 RESUME IF SUSPENDED")
            cursor.execute("USE WAREHOUSE BIGDATA7245")
            
            # Drop existing table
            drop_table_sql = f"""
            DROP TABLE IF EXISTS {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.CFA_PUBLICATION
            """
            cursor.execute(drop_table_sql)
            
            # Create new table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.CFA_PUBLICATION (
                ID NUMBER AUTOINCREMENT,
                TITLE VARCHAR(500),
                SUMMARY TEXT,
                IMAGE_URL VARCHAR(1000),
                PDF_URL VARCHAR(1000),
                URL VARCHAR(1000),
                S3_BUCKET VARCHAR(100),
                CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                PRIMARY KEY (ID)
            )
            """
            cursor.execute(create_table_sql)
            conn.commit()
            
            logger.info("Successfully created Snowflake table")
            return True
    except Exception as e:
        logger.error(f"Error creating Snowflake table: {e}")
        raise AirflowException(f"Failed to create Snowflake table: {e}")
    finally:
        if conn:
            conn.close()

@task(retries=3, retry_delay=timedelta(minutes=1))
def process_s3_metadata():
    """Task to process metadata from S3 files with improved error handling."""
    aws_config = AWSConfig(
        access_key_id=AWS_ACCESS_KEY_ID,
        secret_access_key=AWS_SECRET_ACCESS_KEY,
        region=AWS_REGION,
        bucket=AWS_BUCKET_NAME
    )
    
    s3_client = setup_s3_client(aws_config)
    processed_data = []
    
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        
        # Add verification logging
        logger.info(f"Starting to process files from bucket: {aws_config.bucket}")
        
        for page in paginator.paginate(Bucket=aws_config.bucket):
            # Log the number of objects in this page
            logger.info(f"Found {len(page.get('Contents', []))} objects in current page")
            
            for obj in page.get('Contents', []):
                if not obj['Key'].endswith('metadata.json'):
                    continue
                
                logger.info(f"Processing metadata file: {obj['Key']}")
                
                try:
                    response = s3_client.get_object(
                        Bucket=aws_config.bucket,
                        Key=obj['Key']
                    )
                    metadata = json.loads(response['Body'].read().decode('utf-8'))
                    publication_data = process_metadata(metadata, aws_config.bucket)
                    processed_data.append(publication_data)
                    logger.info(f"Successfully processed metadata from {obj['Key']}")
                    
                except Exception as e:
                    logger.error(f"Error processing {obj['Key']}: {str(e)}", exc_info=True)
                    continue
        
        if not processed_data:
            logger.warning("No metadata files were processed!")
            return []
            
        logger.info(f"Total processed records: {len(processed_data)}")
        return processed_data
        
    except Exception as e:
        logger.error(f"Error in process_s3_metadata: {str(e)}", exc_info=True)
        raise AirflowException(f"Failed to process S3 metadata: {str(e)}")

@task
def load_to_snowflake(processed_data: list):
    """Task to load processed data into Snowflake."""
    if not processed_data:
        logger.warning("No data received for loading into Snowflake")
        return {"records_loaded": 0}
        
    try:
        logger.info(f"Attempting to load {len(processed_data)} records to Snowflake")
        
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse='BIGDATA7245',  # Changed to BIGDATA7245
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE
        )
        
        successful_count = 0
        failed_records = []
        
        with conn.cursor() as cursor:
            # Explicitly resume BIGDATA7245 warehouse
            cursor.execute("ALTER WAREHOUSE BIGDATA7245 RESUME IF SUSPENDED")
            
            # Use the correct warehouse
            cursor.execute("USE WAREHOUSE BIGDATA7245")
            
            # Verify warehouse is running
            cursor.execute("SELECT CURRENT_WAREHOUSE()")
            current_warehouse = cursor.fetchone()[0]
            logger.info(f"Using warehouse: {current_warehouse}")
            
            # Verify table exists and is accessible
            cursor.execute(f"SHOW TABLES LIKE 'CFA_PUBLICATION' IN {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}")
            if not cursor.fetchone():
                raise Exception("Table CFA_PUBLICATION not found!")
                
            for publication_data in processed_data:
                try:
                    insert_sql = f"""
                    INSERT INTO {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.CFA_PUBLICATION (
                        TITLE, SUMMARY, IMAGE_URL, PDF_URL, URL, S3_BUCKET
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s
                    )
                    """
                    
                    # Log the actual values being inserted
                    logger.info(f"Inserting record: {publication_data['TITLE']}")
                    
                    cursor.execute(insert_sql, (
                        publication_data['TITLE'],
                        publication_data['SUMMARY'],
                        publication_data['IMAGE_URL'],
                        publication_data['PDF_URL'],
                        publication_data['URL'],
                        publication_data['S3_BUCKET']
                    ))
                    successful_count += 1
                    
                except Exception as e:
                    logger.error(f"Error inserting record {publication_data['TITLE']}: {str(e)}", exc_info=True)
                    failed_records.append(publication_data)
                    continue
            
            conn.commit()
            
            # Verify data was inserted
            cursor.execute(f"SELECT COUNT(*) FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.CFA_PUBLICATION")
            total_records = cursor.fetchone()[0]
            logger.info(f"Total records in table after insertion: {total_records}")
            
            if failed_records:
                logger.warning(f"Failed to insert {len(failed_records)} records")
                
            return {
                "records_loaded": successful_count,
                "total_records": total_records,
                "failed_records": len(failed_records)
            }
            
    except Exception as e:
        logger.error(f"Error in load_to_snowflake: {str(e)}", exc_info=True)
        raise AirflowException(f"Failed to load data to Snowflake: {str(e)}")
    finally:
        if conn:
            conn.close()

# DAG definition
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': True
}

with DAG(
    'snowflake_data_loader',
    default_args=default_args,
    description='Load data from S3 to Snowflake',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['snowflake', 's3', 'data_loading']
) as dag:
     
    # Define task flow with different variable names
    create_table_task = create_snowflake_table()
    process_metadata_task = process_s3_metadata()
    load_data_task = load_to_snowflake(process_metadata_task)
    
    # Set dependencies using the new variable names
    create_table_task >> process_metadata_task >> load_data_task