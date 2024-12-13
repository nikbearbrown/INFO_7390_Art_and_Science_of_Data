import os
import boto3
from datasets import load_dataset
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Credentials and bucket name
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Function to upload dataset to S3
def upload_to_s3(file_name, bucket, object_name=None):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Upload Successful: {object_name}")
    except Exception as e:
        print(f"Upload Failed: {e}")

# Load dataset from Hugging Face
def load_and_save_dataset():
    dataset = load_dataset("AkashPS11/recipes_data_food.com")["train"]

    # Save locally
    file_name = "recipes_data.csv"
    dataset.to_csv(file_name)
    return file_name

if __name__ == "__main__":
    file_to_upload = load_and_save_dataset()
    
    # Upload to S3
    upload_to_s3(file_to_upload, S3_BUCKET_NAME, "recipes_data/recipes_data.csv")
