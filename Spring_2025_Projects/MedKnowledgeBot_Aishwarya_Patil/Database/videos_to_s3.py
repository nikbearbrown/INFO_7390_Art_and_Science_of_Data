import pandas as pd
import json
import os
import logging
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("youtube_processing.log"),
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

def process_youtube_to_json(csv_file_path, output_dir="json_data"):
    """Process YouTube transcript data to JSON format"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load the CSV
        df = pd.read_csv(csv_file_path)
        logger.info(f"Loaded CSV with {len(df)} rows")
        
        # Filter rows with transcripts
        df_with_transcripts = df[df['transcript'].notna() & (df['transcript'] != "")]
        logger.info(f"Found {len(df_with_transcripts)} rows with transcripts")
        
        # List to store all documents
        all_documents = []
        
        # Process each video
        for index, row in df_with_transcripts.iterrows():
            try:
                logger.info(f"Processing video {index+1}/{len(df_with_transcripts)}: {row['title']}")
                
                # Create document object
                document = {
                    "id": f"video_{row['video_id']}",
                    "text": row['transcript'],
                    "metadata": {
                        "video_id": row['video_id'],
                        "title": row['title'],
                        "description": row['description'],
                        "published_at": row['published_at'],
                        "duration": row['duration'],
                        "view_count": str(row['view_count']),
                        "channel": row['channel'],
                        "url": row['url'],
                        "search_query": row['search_query'],
                        "content_type": "youtube_video"
                    }
                }
                
                # Save individual JSON file
                video_filename = f"video_{row['video_id']}.json"
                json_path = os.path.join(output_dir, video_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(document, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Saved JSON to {json_path}")
                
                # Add to the collection of all documents
                all_documents.append(document)
                
            except Exception as e:
                logger.error(f"Error processing video {index}: {e}")
        
        # Save all documents to a single JSON file
        all_videos_path = os.path.join(output_dir, "all_videos.json")
        with open(all_videos_path, 'w', encoding='utf-8') as f:
            json.dump(all_documents, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved all {len(all_documents)} video documents to {all_videos_path}")
        
        return all_documents
        
    except Exception as e:
        logger.error(f"Error in process_youtube_to_json: {e}")
        return False

def upload_to_s3(file_path, bucket_name, object_name):
    """Upload a file to S3"""
    s3_client = initialize_s3_client()
    if not s3_client:
        return False
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{object_name}")
        return True
    except Exception as e:
        logger.error(f"Error uploading {file_path} to S3: {e}")
        return False

def combine_article_and_video_data(articles_json_path, videos_json_path, output_dir="json_data"):
    """Combine article and video JSON data into a single file"""
    try:
        # Load article data
        with open(articles_json_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        logger.info(f"Loaded {len(articles)} articles from {articles_json_path}")
        
        # Load video data
        with open(videos_json_path, 'r', encoding='utf-8') as f:
            videos = json.load(f)
        logger.info(f"Loaded {len(videos)} videos from {videos_json_path}")
        
        # Combine data
        all_documents = articles + videos
        logger.info(f"Combined {len(all_documents)} documents")
        
        # Save combined data
        combined_path = os.path.join(output_dir, "all_documents_combined.json")
        with open(combined_path, 'w', encoding='utf-8') as f:
            json.dump(all_documents, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved combined data to {combined_path}")
        
        return combined_path
        
    except Exception as e:
        logger.error(f"Error combining data: {e}")
        return False

if __name__ == "__main__":
    # Configuration
    CSV_FILE_PATH = "all_medical_videos_with_transcripts.csv"
    BUCKET_NAME =  os.getenv("bucket_name")
    OUTPUT_DIR = "json_data"
    
    # Process YouTube data
    videos = process_youtube_to_json(CSV_FILE_PATH, OUTPUT_DIR)
    
    if videos:
        print(f"Successfully processed {len(videos)} videos to JSON")
        
        # Upload to S3
        upload_success = upload_to_s3(
            os.path.join(OUTPUT_DIR, "all_videos.json"),
            BUCKET_NAME,
            "processed/all_videos.json"
        )
        
        if upload_success:
            print("Successfully uploaded videos JSON to S3")
            
            # If you already have article data, combine them
            articles_path = os.path.join(OUTPUT_DIR, "all_documents.json")
            videos_path = os.path.join(OUTPUT_DIR, "all_videos.json")
            
            if os.path.exists(articles_path):
                combined_path = combine_article_and_video_data(articles_path, videos_path, OUTPUT_DIR)
                
                if combined_path:
                    print(f"Successfully combined article and video data in {combined_path}")
                    
                    # Upload combined data to S3
                    upload_success = upload_to_s3(
                        combined_path,
                        BUCKET_NAME,
                        "processed/all_documents_combined.json"
                    )
                    
                    if upload_success:
                        print("Successfully uploaded combined data to S3")
                    else:
                        print("Failed to upload combined data to S3")
                else:
                    print("Failed to combine article and video data")
            else:
                print(f"Article data not found at {articles_path}. Only video data processed.")
        else:
            print("Failed to upload videos JSON to S3")
    else:
        print("Failed to process videos. Check logs for details.")