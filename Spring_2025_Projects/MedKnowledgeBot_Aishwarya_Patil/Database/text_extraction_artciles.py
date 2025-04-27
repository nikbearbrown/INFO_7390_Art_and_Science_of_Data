import boto3
import os
import pandas as pd
import json
import PyPDF2
from io import BytesIO
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Initialize S3 client
def initialize_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        return s3_client
    except Exception as e:
        logger.error(f"Error initializing S3 client: {e}")
        return None

def extract_text_from_pdf_in_s3(s3_client, bucket_name, s3_key):
    """Extract text from a PDF file stored in S3"""
    try:
        # Download PDF from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        pdf_content = response['Body'].read()
        
        # Use BytesIO to work with the PDF in memory
        pdf_file = BytesIO(pdf_content)
        
        # Extract text using PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() + "\n\n"
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {s3_key}: {e}")
        return ""

def process_articles_to_json(csv_s3_key, bucket_name, output_dir="json_data"):
    """Process articles and their metadata into JSON format"""
    # Initialize S3 client
    s3_client = initialize_s3_client()
    if not s3_client:
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Download the CSV with metadata from S3
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=csv_s3_key)
        df = pd.read_csv(BytesIO(csv_obj['Body'].read()))
        logger.info(f"Loaded CSV with {len(df)} rows")
        
        # Filter only rows with S3 PDF paths
        df_with_pdfs = df[df['s3_pdf_path'].notna()]
        logger.info(f"Found {len(df_with_pdfs)} rows with PDF paths")
        
        # List to store all documents
        all_documents = []
        
        # Process each article
        for index, row in df_with_pdfs.iterrows():
            try:
                logger.info(f"Processing article {index+1}/{len(df_with_pdfs)}: {row['Title']}")
                
                # Extract S3 key from the S3 path
                s3_path = row['s3_pdf_path']
                s3_key = s3_path.replace(f"s3://{bucket_name}/", "")
                
                # Extract text from PDF
                text = extract_text_from_pdf_in_s3(s3_client, bucket_name, s3_key)
                
                if not text:
                    logger.warning(f"No text extracted from PDF: {s3_key}")
                    continue
                
                # Create document object with all metadata fields
                document = {
                    "id": f"doc_{index}",
                    "text": text,
                    "metadata": {
                        # Include all available metadata fields
                        "title": row['Title'],
                        "authors": row['Authors'],
                        "publication_date": row['Publication Date'],
                        "journal": row['Journal'],
                        "citation_info": row.get('Citation Info', ''),
                        "content_type": row.get('Content Type', ''),
                        "article_url": row.get('Article URL', ''),
                        "pdf_url": row.get('PDF URL', ''),
                        "doi": row.get('DOI', ''),
                        "page_number": row.get('Page Number', ''),
                        "search_topic": row.get('Search Topic', ''),
                        "s3_pdf_path": s3_path
                    }
                }
                
                # Save individual JSON file
                doc_filename = f"doc_{index}.json"
                json_path = os.path.join(output_dir, doc_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(document, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Saved JSON to {json_path}")
                
                # Add to the collection of all documents
                all_documents.append(document)
                
            except Exception as e:
                logger.error(f"Error processing article {index}: {e}")
        
        # Save all documents to a single JSON file
        all_docs_path = os.path.join(output_dir, "all_documents.json")
        with open(all_docs_path, 'w', encoding='utf-8') as f:
            json.dump(all_documents, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved all {len(all_documents)} documents to {all_docs_path}")
        
        # Upload the combined JSON file to S3
        s3_client.upload_file(
            all_docs_path,
            bucket_name,
            "processed/all_documents.json"
        )
        logger.info(f"Uploaded all_documents.json to S3: s3://{bucket_name}/processed/all_documents.json")
        
        return all_documents
        
    except Exception as e:
        logger.error(f"Error in process_articles_to_json: {e}")
        return False

if __name__ == "__main__":
    # Configuration
    CSV_S3_KEY = "metadata/processed/articles_with_s3_paths.csv"  # S3 key of your CSV
    BUCKET_NAME = os.getenv("bucket_name")
    
    # Process articles to JSON
    documents = process_articles_to_json(CSV_S3_KEY, BUCKET_NAME)
    
    if documents:
        print(f"Successfully processed {len(documents)} documents to JSON")
    else:
        print("Failed to process documents. Check logs for details.")