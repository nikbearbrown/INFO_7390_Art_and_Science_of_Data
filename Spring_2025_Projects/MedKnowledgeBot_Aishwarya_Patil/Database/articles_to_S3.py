import boto3
import os
import pandas as pd
import requests
import time
import logging
from dotenv import load_dotenv
load_dotenv()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("s3_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# AWS S3 Configuration
def initialize_s3_client():
    try:
        # Create S3 client - using credentials from environment variables or AWS configuration
        s3_client = boto3.client(
            's3',
            aws_access_key_id = os.getenv("aws_access_key_id"),
            aws_secret_access_key= os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        return s3_client
    except Exception as e:
        logger.error(f"Error initializing S3 client: {e}")
        return None

def download_pdf(pdf_url, filename, max_retries=3):
    """Download a PDF file from URL with retry logic"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(pdf_url, headers=headers, stream=True, timeout=30)
            
            if response.status_code == 200:
                # Check if it's actually a PDF
                content_type = response.headers.get('Content-Type', '')
                if 'application/pdf' in content_type or pdf_url.endswith('.pdf'):
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"Successfully downloaded: {filename}")
                    return True
                else:
                    logger.warning(f"URL does not point to a PDF: {pdf_url}, Content-Type: {content_type}")
                    return False
            else:
                logger.warning(f"Failed to download {pdf_url}: HTTP {response.status_code}, attempt {attempt+1}/{max_retries}")
                time.sleep(2)  # Wait before retry
        except Exception as e:
            logger.error(f"Error downloading {pdf_url}: {e}, attempt {attempt+1}/{max_retries}")
            time.sleep(2)  # Wait before retry
    
    return False

def upload_file_to_s3(s3_client, file_path, bucket_name, object_name=None):
    """Upload a file to S3 bucket"""
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{object_name}")
        return f"s3://{bucket_name}/{object_name}"
    except Exception as e:
        logger.error(f"Error uploading {file_path}: {e}")
        return None

def process_articles_and_upload(csv_file_path, bucket_name, limit=None):
    """Process articles from CSV and upload PDFs to S3"""
    # Initialize S3 client
    s3_client = initialize_s3_client()
    if not s3_client:
        return False
    
    # Check if bucket exists and is accessible
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Successfully connected to bucket: {bucket_name}")
    except Exception as e:
        logger.error(f"Error accessing bucket {bucket_name}: {e}")
        return False
    
    # Create directories for local processing
    os.makedirs('pdfs', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    
    # Upload the original CSV metadata file
    csv_s3_path = upload_file_to_s3(
        s3_client, 
        csv_file_path, 
        bucket_name, 
        'metadata/articles/original_metadata.csv'
    )
    
    # Load article data
    df_articles = pd.read_csv(csv_file_path)
    logger.info(f"Loaded {len(df_articles)} articles from CSV")
    
    # Apply limit if specified
    if limit and limit > 0:
        df_articles = df_articles.head(limit)
        logger.info(f"Limited processing to {limit} articles")
    
    # Add S3 path column
    df_articles['s3_pdf_path'] = None
    
    # Process each article with a PDF URL
    successful_count = 0
    failed_count = 0
    
    for index, row in df_articles.iterrows():
        if pd.notna(row['PDF URL']) and row['PDF URL']:
            logger.info(f"Processing article {index+1}/{len(df_articles)}: {row['Title']}")
            
            # Create a safe filename based on DOI or title
            if pd.notna(row['DOI']) and row['DOI']:
                doi = row['DOI']
                safe_doi = ''.join(c if c.isalnum() or c in '.-_' else '_' for c in doi)
                filename = f"pdfs/{safe_doi}.pdf"
            else:
                # Use a part of the title if DOI is not available
                safe_title = ''.join(c if c.isalnum() or c in '.-_ ' else '_' for c in row['Title'])
                safe_title = safe_title[:100]  # Limit length
                filename = f"pdfs/{safe_title}.pdf"
            
            # Download the PDF
            if download_pdf(row['PDF URL'], filename):
                # Upload to S3
                s3_object_name = f"articles/pdfs/{os.path.basename(filename)}"
                s3_path = upload_file_to_s3(s3_client, filename, bucket_name, s3_object_name)
                
                if s3_path:
                    df_articles.at[index, 's3_pdf_path'] = s3_path
                    successful_count += 1
                else:
                    failed_count += 1
            else:
                logger.warning(f"Failed to download PDF for article: {row['Title']}")
                failed_count += 1
            
            # Be nice to the server - add a small delay
            time.sleep(1)
    
    # Save enhanced metadata with S3 paths
    enhanced_csv_path = 'processed/articles_with_s3_paths.csv'
    df_articles.to_csv(enhanced_csv_path, index=False)
    
    # Upload the enhanced CSV
    upload_file_to_s3(
        s3_client, 
        enhanced_csv_path, 
        bucket_name, 
        'metadata/processed/articles_with_s3_paths.csv'
    )
    
    logger.info(f"Processing complete. Successfully processed {successful_count} PDFs, failed on {failed_count} PDFs.")
    logger.info(f"Enhanced metadata saved to s3://{bucket_name}/metadata/processed/articles_with_s3_paths.csv")
    
    return True

if __name__ == "__main__":
    # Configuration
    CSV_FILE_PATH = 'bmc_medicine_all_topics.csv'  # Your article CSV file
    BUCKET_NAME = os.getenv("bucket_name") # Your existing S3 bucket name
    LIMIT = 50  # Process only the first 50 articles (set to None for all)
    
    # Run the process
    success = process_articles_and_upload(CSV_FILE_PATH, BUCKET_NAME, LIMIT)
    
    if success:
        print("Article processing and upload completed successfully!")
    else:
        print("Article processing and upload failed. Check logs for details.")