# data_retrieval.py
import snowflake.connector
from fast_api.config.config_settings import create_snowflake_connection
import pandas as pd
import boto3
from urllib.parse import urlparse, unquote
import os
import requests
from dotenv import load_dotenv 
from io import BytesIO

# Load environment variables from .env file (if applicable)
load_dotenv()

def fetch_data_from_db() -> pd.DataFrame:
    mydata = None  # Initialize mydata to None
    mydb = None    # Initialize mydb to None
    try:
        # Connect to snowflake database
        mydb = create_snowflake_connection()
        
        # logging_module.log_success("Connected to the database for fetching data.")
        print("Connected to the database for fetching data.")
        # Create a cursor object
        mydata = mydb.cursor()

        # Execute the query
        mydata.execute("SELECT * FROM edw.pdf_metadata_table_1")
        
        # Fetch all the data
        myresult = mydata.fetchall()

        # logging_module.log_success("Fetched data from edw.pdf_metadata_table")
        print("Fetched data from edw.pdf_metadata_table_1")
        # Get column names
        columns = [col[0] for col in mydata.description]

        # Store the fetched data into a pandas DataFrame
        df = pd.DataFrame(myresult, columns=columns)

        return df

    except snowflake.connector.Error as e:
        # logging_module.log_error(f"Database error occurred: {e}")
        print(f"Database error occurred: {e}")
        return None

    except Exception as e:
        # logging_module.log_error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        return None


def fetch_pdf_urls_from_snowflake():
    conn=create_snowflake_connection()
    
    query = "SELECT PDF_S3_URL FROM edw.pdf_metadata_table_1;"
    cursor = conn.cursor()
    cursor.execute(query)
    
    pdf_urls = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [url[0] for url in pdf_urls] 


def parse_s3_url(s3_url):
    if s3_url.startswith('s3://'):
        # For 's3://' format
        parsed_url = urlparse(s3_url)
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip('/')
    else:
        # For 'https://' format (if needed in future)
        parsed_url = urlparse(s3_url)
        bucket = parsed_url.netloc.split('.')[0]  # Get the bucket name from the URL
        key = parsed_url.path.lstrip('/')
    
    return bucket, key

def download_pdf_from_s3(bucket, key, local_file_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    # Download the file
    s3.download_file(bucket, key, local_file_name)
    print(f"Downloaded {local_file_name} from S3 bucket {bucket}.")

def generate_presigned_url(pdf_name, expiration: int = 3600) -> str:
    key = f'research-files/{pdf_name}'
    
    try:

        s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        # Generate pre-signed URL that expires in the given time (default: 1 hour)
        presigned_url = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': os.getenv("S3_BUCKET_NAME_AWS"), 'Key': key},
                                                  ExpiresIn=expiration)
        return presigned_url
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

def download_file(pdf_name) -> dict:
    # Parse the URL to extract the file name
    file_name = generate_presigned_url(pdf_name)
    parsed_url = urlparse(file_name)
    path = unquote(parsed_url.path)
    filename = os.path.basename(path)
    extension = os.path.splitext(filename)[1]

    # Get the file from the URL
    response = requests.get(file_name)
    response.raise_for_status()  # Ensure the request was successful
    file_content = response.content

    # Use /tmp directory for saving files
    temp_dir = "/tmp/temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Return file details
    return {
        "file_name": filename,
        "pdf_content": BytesIO(file_content),
        "extension": extension,
        "file_path": file_path
    }

