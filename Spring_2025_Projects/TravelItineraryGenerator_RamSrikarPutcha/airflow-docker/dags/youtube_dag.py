from datetime import datetime, timedelta
import os
import re
import json
import pandas as pd
import googleapiclient.discovery
import boto3
from pinecone import Pinecone, ServerlessSpec
import spacy
from openai import OpenAI
import time
from collections import defaultdict
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Application constants
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536
MAX_RESULTS_PER_QUERY = 20
LOCAL_BASE_DIR = "/opt/airflow/data/city_transcripts"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# City configuration
CITIES = {
    "NewYork": {
        "folder_name": "Newyork",
        "queries": ["New York City travel vlog", "NYC travel guide", "Manhattan tourism", 
                   "NYC must see", "NYC hidden gems", "NYC food guide"],
        "landmarks": [
            "times square", "central park", "empire state building", "statue of liberty", 
            "brooklyn bridge", "grand central", "manhattan", "broadway", "fifth avenue", 
            "soho", "chelsea", "greenwich village", "wall street", "brooklyn", "queens", 
            "bronx", "staten island", "high line", "little italy", "chinatown", 
            "world trade center", "9/11 memorial", "rockefeller", "met museum", "moma"
        ]
    },
    "Chicago": {
        "folder_name": "Chicago",
        "queries": ["Chicago travel vlog", "Chicago travel guide", "Chicago tourism", 
                   "Chicago must see", "Chicago hidden gems", "Chicago food guide"],
        "landmarks": [
            "millennium park", "cloud gate", "navy pier", "willis tower", "magnificent mile", 
            "art institute", "field museum", "shedd aquarium", "wrigley field", "lincoln park", 
            "grant park", "chicago riverwalk", "hancock center", "chicago theater", "michigan avenue"
        ]
    },
    "LasVegas": {
        "folder_name": "LasVegas",
        "queries": ["Las Vegas travel vlog", "Las Vegas travel guide", "Vegas Strip tourism", 
                   "Las Vegas must see", "Las Vegas hidden gems", "Las Vegas food guide"],
        "landmarks": [
            "the strip", "bellagio fountains", "fremont street", "high roller", "caesars palace", 
            "venetian", "mgm grand", "paris", "luxor", "mandalay bay", "mirage", "new york new york", 
            "stratosphere", "circus circus", "wynn", "encore", "palazzo"
        ]
    },
    "LosAngeles": {
        "folder_name": "LosAngeles",
        "queries": ["Los Angeles travel vlog", "LA travel guide", "Hollywood tourism", 
                   "LA must see", "Los Angeles hidden gems", "LA food guide"],
        "landmarks": [
            "hollywood sign", "venice beach", "santa monica pier", "griffith observatory", 
            "universal studios", "the getty", "hollywood walk of fame", "beverly hills", 
            "rodeo drive", "disneyland", "tcl chinese theatre", "dodger stadium", "la brea tar pits", 
            "malibu", "staples center", "sunset boulevard", "downtown la"
        ]
    },
    "Seattle": {
        "folder_name": "Seattle",
        "queries": ["Seattle travel vlog", "Seattle travel guide", "Seattle tourism", 
                   "Seattle must see", "Seattle hidden gems", "Seattle food guide"],
        "landmarks": [
            "space needle", "pike place market", "chihuly garden", "museum of pop culture", 
            "seattle great wheel", "gas works park", "kerry park", "pioneer square", 
            "olympic sculpture park", "columbia center", "fremont troll", "lake union", 
            "discovery park", "washington park arboretum", "alki beach"
        ]
    },
    "SanFrancisco": {
        "folder_name": "SanFrancisco", 
        "queries": ["San Francisco travel vlog", "SF travel guide", "San Francisco tourism", 
                   "SF must see", "San Francisco hidden gems", "SF food guide"],
        "landmarks": [
            "golden gate bridge", "alcatraz", "fisherman's wharf", "lombard street", 
            "chinatown", "union square", "cable car", "palace of fine arts", "coit tower", 
            "pier 39", "twin peaks", "golden gate park", "painted ladies", "mission district",
            "ghirardelli square", "presidio", "embarcadero", "ferry building"
        ]
    }
}

# Extraction keywords
LANDMARK_KEYWORDS = [
    "square", "park", "bridge", "village", "museum", "building", "island", "center",
    "statue", "memorial", "tower", "hall", "market", "empire", "terminal", "theater",
    "garden", "zoo", "aquarium", "library", "cathedral", "church", "temple", "synagogue"
]

FOOD_KEYWORDS = [
    "pizza", "bagel", "halal", "deli", "cheesecake", "food", "restaurant", "cafe", 
    "bakery", "coffee", "breakfast", "lunch", "dinner", "brunch", "bar", "pub", 
    "cocktail", "wine", "beer", "burger", "sandwich", "italian", "chinese", "mexican",
    "japanese", "thai", "indian", "korean", "seafood", "steak", "vegan", "vegetarian"
]

TRANSPORT_KEYWORDS = [
    "subway", "metro", "train", "omni", "taxi", "ferry", "bus", "bike", "walk",
    "citibike", "uber", "lyft", "transit", "line", "station", "stop", "terminal"
]

COST_PATTERNS = [
    r"\$\d+(?:\.\d{1,2})?", 
    r"free", 
    r"pay what you wish", 
    r"two for one", 
    r"\d+ percent off",
    r"\d+ dollars"
]

TIME_PATTERNS = [
    r"morning", r"afternoon", r"evening", r"night",
    r"day \d+", r"first day", r"second day", r"third day",
    r"early", r"late", r"noon", r"midnight", r"breakfast", r"lunch", r"dinner"
]

def process_city(city_key, **kwargs):
    logger.info(f"Starting processing for city: {city_key}")
    
    try:
        # Get configuration for this city
        city_config = CITIES.get(city_key)
        if not city_config:
            error_msg = f"City '{city_key}' not found in configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create directory structure
        city_folder = city_config["folder_name"]
        local_output_dir = os.path.join(LOCAL_BASE_DIR, city_folder)
        transcripts_dir = os.path.join(local_output_dir, "transcripts")
        
        logger.info(f"Creating directory structure for {city_key}")
        try:
            os.makedirs(local_output_dir, exist_ok=True)
            os.makedirs(transcripts_dir, exist_ok=True)
            logger.info(f"Created directories: {local_output_dir}, {transcripts_dir}")
        except Exception as e:
            logger.error(f"Failed to create directories for {city_key}: {str(e)}")
            raise
        
        # Get parameters and credentials
        params = kwargs.get('dag_run').conf or {}
        use_existing = params.get('use_existing', False)
        skip_download = params.get('skip_download', False)
        skip_upload = params.get('skip_upload', False)
        
        logger.info(f"Parameters for {city_key}: use_existing={use_existing}, skip_download={skip_download}, skip_upload={skip_upload}")
        
        # Get credentials from environment variables
        try:
            credentials = {
                'youtube_api_key': os.getenv('YOUTUBE_API_KEY', ''),
                'aws_access_key': os.getenv('AWS_ACCESS_KEY', ''),
                'aws_secret_key': os.getenv('AWS_SECRET_KEY', ''),
                'aws_region': os.getenv('AWS_REGION', 'us-east-2'),
                's3_bucket_name': os.getenv('S3_BUCKET_NAME', ''),
                'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
                'pinecone_api_key': os.getenv('PINECONE_API_KEY', ''),
                'pinecone_index': os.getenv('PINECONE_INDEX', ''),
                'pinecone_cloud': os.getenv('PINECONE_CLOUD', 'aws'),
                'pinecone_region': os.getenv('PINECONE_REGION', 'us-east-1'),
            }
            logger.info(f"Successfully retrieved credentials from environment variables")
            
            # Log if any critical credentials are missing
            missing_credentials = []
            if not credentials['youtube_api_key'] and not skip_download:
                missing_credentials.append('YOUTUBE_API_KEY')
            if not credentials['aws_access_key'] and not skip_upload:
                missing_credentials.append('AWS_ACCESS_KEY')
            if not credentials['aws_secret_key'] and not skip_upload:
                missing_credentials.append('AWS_SECRET_KEY')
            if not credentials['s3_bucket_name'] and not skip_upload:
                missing_credentials.append('S3_BUCKET_NAME')
                
            if missing_credentials:
                logger.warning(f"Missing credentials for {city_key}: {', '.join(missing_credentials)}")
        except Exception as e:
            logger.error(f"Failed to retrieve credentials: {str(e)}")
            raise
        
        # Initialize NLP model
        try:
            logger.info(f"Loading spaCy model for {city_key}")
            nlp_model = spacy.load("en_core_web_sm")
            logger.info("Successfully loaded spaCy model")
        except Exception as e:
            logger.error(f"Error loading spaCy model: {str(e)}")
            return {
                "city_key": city_key,
                "error": f"Failed to load NLP model: {str(e)}",
                "status": "failed"
            }
        
        # Load results with defaults
        download_result = {"transcript_count": 0, "video_data": []}
        upload_result = {"uploaded_files": []}
        embed_result = {"successful_count": 0, "failed_count": 0, "total_vectors": 0}
        
        # Step 1: Download transcripts (or use existing)
        if not skip_download:
            if use_existing and os.path.exists(transcripts_dir):
                transcript_files = [f for f in os.listdir(transcripts_dir) if f.endswith('.txt')]
                if transcript_files:
                    logger.info(f"Using {len(transcript_files)} existing transcripts for {city_key}")
                    download_result["transcript_count"] = len(transcript_files)
                else:
                    logger.info(f"No existing transcripts found for {city_key}, proceeding with download")
                    download_result = download_city_transcripts(
                        city_key, city_config, credentials, local_output_dir, transcripts_dir
                    )
            else:
                logger.info(f"Downloading transcripts for {city_key}")
                download_result = download_city_transcripts(
                    city_key, city_config, credentials, local_output_dir, transcripts_dir
                )
        else:
            logger.info(f"Skipping download phase for {city_key}")
        
        # Step 2: Upload to S3
        if not skip_upload and credentials['aws_access_key'] and credentials['aws_secret_key'] and credentials['s3_bucket_name']:
            logger.info(f"Uploading {city_key} data to S3")
            upload_result = upload_city_data_to_s3(
                city_key, city_config, credentials, local_output_dir, transcripts_dir
            )
        else:
            missing_s3_creds = []
            if not credentials['aws_access_key']:
                missing_s3_creds.append('aws_access_key')
            if not credentials['aws_secret_key']:
                missing_s3_creds.append('aws_secret_key')
            if not credentials['s3_bucket_name']:
                missing_s3_creds.append('s3_bucket_name')
                
            if skip_upload:
                logger.info(f"Skipping S3 upload phase for {city_key} (manually skipped)")
            else:
                logger.warning(f"Skipping S3 upload phase for {city_key} due to missing credentials: {', '.join(missing_s3_creds)}")
        
        # Step 3: Process and embed
        if credentials['openai_api_key'] and credentials['pinecone_api_key'] and credentials['pinecone_index']:
            logger.info(f"Processing and embedding {city_key} transcripts")
            embed_result = process_and_embed_city_data(
                city_key, city_config, credentials, nlp_model, local_output_dir, transcripts_dir
            )
        else:
            missing_embed_creds = []
            if not credentials['openai_api_key']:
                missing_embed_creds.append('openai_api_key')
            if not credentials['pinecone_api_key']:
                missing_embed_creds.append('pinecone_api_key')
            if not credentials['pinecone_index']:
                missing_embed_creds.append('pinecone_index')
                
            logger.warning(f"Skipping embedding phase for {city_key} due to missing credentials: {', '.join(missing_embed_creds)}")
        
        # Return combined results
        result = {
            "city_key": city_key,
            "transcript_count": download_result.get("transcript_count", 0),
            "s3_files_uploaded": len(upload_result.get("uploaded_files", [])),
            "successful_embeddings": embed_result.get("successful_count", 0),
            "failed_count": embed_result.get("failed_count", 0),
            "total_vectors": embed_result.get("total_vectors", 0),
            "status": "completed"
        }
        
        logger.info(f"Completed processing for {city_key}: {json.dumps(result)}")
        return result
        
    except Exception as e:
        logger.exception(f"Unexpected error processing {city_key}: {str(e)}")
        return {
            "city_key": city_key,
            "error": str(e),
            "status": "failed"
        }

def download_city_transcripts(city_key, city_config, credentials, local_output_dir, transcripts_dir):
    logger.info(f"Starting transcript download for {city_key}")
    
    try:
        if not credentials['youtube_api_key']:
            logger.error(f"Cannot download transcripts for {city_key}: YouTube API key not provided")
            return {
                "transcript_count": 0,
                "video_data": [],
                "error": "YouTube API key not provided"
            }
        
        # Initialize YouTube client
        try:
            logger.info(f"Initializing YouTube client for {city_key}")
            youtube_client = googleapiclient.discovery.build(
                "youtube", "v3", 
                developerKey=credentials['youtube_api_key'],
                static_discovery=False,
                credentials=None
            )
            logger.info("YouTube client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube client: {str(e)}")
            return {
                "transcript_count": 0,
                "video_data": [],
                "error": f"Failed to initialize YouTube client: {str(e)}"
            }
        
        city_landmarks = city_config["landmarks"]
        city_queries = city_config["queries"]
        
        all_video_data = []
        successful_transcripts = 0
        failed_transcripts = 0
        
        for query_index, query in enumerate(city_queries):
            logger.info(f"[{city_key}] Processing query {query_index + 1}/{len(city_queries)}: '{query}'")
            try:
                video_ids, search_items = search_videos(youtube_client, query, MAX_RESULTS_PER_QUERY)
                logger.info(f"[{city_key}] Found {len(video_ids)} videos for query: '{query}'")
                
                batch_size = 5
                for i in range(0, len(video_ids), batch_size):
                    batch_ids = video_ids[i:i+batch_size]
                    
                    logger.info(f"[{city_key}] Processing batch {i//batch_size + 1}/{(len(video_ids) + batch_size - 1)//batch_size}")
                    
                    try:
                        batch_details = get_video_details(youtube_client, batch_ids)
                        
                        for video_details in batch_details:
                            video_id = video_details["id"]
                            
                            logger.info(f"[{city_key}] Retrieving transcript for video {video_id}")
                            transcript_data = get_video_transcript(video_id)
                            
                            if not transcript_data:
                                logger.warning(f"[{city_key}] No transcript available for video {video_id}")
                                failed_transcripts += 1
                                continue
                            
                            transcript = transcript_data['text']
                            logger.info(f"[{city_key}] Retrieved transcript for video {video_id} ({len(transcript.split())} words)")
                            successful_transcripts += 1
                            
                            city_info = extract_city_info(transcript, city_landmarks, city_key)
                            
                            title = video_details.get("snippet", {}).get("title", "")
                            channel = video_details.get("snippet", {}).get("channelTitle", "")
                            publish_date = video_details.get("snippet", {}).get("publishedAt", "")
                            view_count = int(video_details.get("statistics", {}).get("viewCount", 0))
                            
                            sanitized_title = re.sub(r'[^\w\s-]', '', title)
                            sanitized_title = re.sub(r'[\s]+', '_', sanitized_title)
                            filename = f"{video_id}_{sanitized_title[:50]}.txt"
                            file_path = os.path.join(transcripts_dir, filename)
                            
                            info_header = "NYC INFORMATION:" if city_key == "NewYork" else f"{city_key.upper()} INFORMATION:"
                            
                            transcript_content = f"Title: {title}\n"
                            transcript_content += f"Channel: {channel}\n"
                            transcript_content += f"Video ID: {video_id}\n"
                            transcript_content += f"URL: https://www.youtube.com/watch?v={video_id}\n"
                            transcript_content += f"Published: {publish_date}\n"
                            transcript_content += f"Views: {view_count}\n\n"
                            transcript_content += f"{info_header}\n"
                            transcript_content += f"Landmarks mentioned: {json.dumps(city_info['landmarks'], indent=2)}\n"
                            transcript_content += f"Costs mentioned: {city_info['costs']}\n"
                            transcript_content += f"Average cost: {city_info['avg_cost']}\n"
                            transcript_content += f"Days mentioned: {city_info['days']}\n"
                            transcript_content += f"Average days: {city_info['avg_days']}\n"
                            transcript_content += f"Transportation mentioned: {json.dumps(city_info['transport'], indent=2)}\n"
                            transcript_content += f"Food mentioned: {json.dumps(city_info['food'], indent=2)}\n\n"
                            transcript_content += "TRANSCRIPT:\n\n"
                            transcript_content += transcript
                            
                            try:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(transcript_content)
                                logger.info(f"[{city_key}] Saved transcript to {file_path}")
                                
                                json_filename = f"{video_id}_{sanitized_title[:50]}_segments.json"
                                json_path = os.path.join(transcripts_dir, json_filename)
                                with open(json_path, 'w', encoding='utf-8') as f:
                                    json.dump(transcript_data['segments'], f, indent=2)
                                logger.info(f"[{city_key}] Saved transcript segments to {json_path}")
                                
                                video_data = {
                                    "video_id": video_id,
                                    "title": title,
                                    "channel": channel,
                                    "publish_date": publish_date,
                                    "view_count": view_count,
                                    "transcript_word_count": len(transcript.split()),
                                    "file_path": file_path,
                                    "segments_file": json_path,
                                    "landmarks_mentioned": len(city_info["landmarks"]),
                                    "avg_cost_mentioned": city_info["avg_cost"],
                                    "avg_days_mentioned": city_info["avg_days"],
                                    "transport_mentions": len(city_info["transport"]),
                                    "food_mentions": len(city_info["food"])
                                }
                                
                                all_video_data.append(video_data)
                            except Exception as e:
                                logger.error(f"[{city_key}] Error saving transcript for {video_id}: {str(e)}")
                    except Exception as e:
                        logger.error(f"[{city_key}] Error processing batch: {str(e)}")
                    
                    time.sleep(1)
            except Exception as e:
                logger.error(f"[{city_key}] Error processing query '{query}': {str(e)}")
        
        csv_path = ""
        if all_video_data:
            try:
                df = pd.DataFrame(all_video_data)
                
                if city_key == "NewYork":
                    csv_path = os.path.join(local_output_dir, "nyc_vlog_transcripts.csv")
                else:
                    csv_path = os.path.join(local_output_dir, f"{city_key.lower()}_vlog_transcripts.csv")
                
                df.to_csv(csv_path, index=False)
                logger.info(f"[{city_key}] Saved transcript metadata to {csv_path}")
            except Exception as e:
                logger.error(f"[{city_key}] Error saving transcript metadata to CSV: {str(e)}")
        
        logger.info(f"[{city_key}] Download summary: {successful_transcripts} successful, {failed_transcripts} failed")
        
        return {
            "transcript_count": successful_transcripts,
            "failed_count": failed_transcripts,
            "video_data": all_video_data,
            "csv_path": csv_path
        }
    except Exception as e:
        logger.exception(f"[{city_key}] Unhandled error downloading transcripts: {str(e)}")
        return {
            "transcript_count": 0,
            "video_data": [],
            "error": str(e)
        }

# In your CityTravelProcessor class or upload_city_data_to_s3 function
def upload_city_data_to_s3(city_key, city_config, credentials, local_output_dir, transcripts_dir):
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            region_name=credentials['aws_region'],
            aws_access_key_id=credentials['aws_access_key'],
            aws_secret_access_key=credentials['aws_secret_key']
        )
        
        bucket_name = credentials['s3_bucket_name']
        city_folder = city_config["folder_name"]
        
        # Add the parent folder "youtube_transcripts" to all S3 paths
        parent_folder = "youtube_transcripts"
        
        uploaded_files = []
        
        # Create folder structure in S3
        try:
            # Create parent folder
            s3_client.put_object(Bucket=bucket_name, Key=f"{parent_folder}/")
            # Create city folder within parent folder
            s3_client.put_object(Bucket=bucket_name, Key=f"{parent_folder}/{city_folder}/")
            # Create transcripts folder within city folder
            s3_client.put_object(Bucket=bucket_name, Key=f"{parent_folder}/{city_folder}/transcripts/")
            logger.info(f"[{city_key}] Created S3 folder structure in bucket {bucket_name}")
        except Exception as e:
            logger.warning(f"[{city_key}] Note: S3 folders may already exist: {str(e)}")
        
        # Upload transcript files with modified S3 paths
        for filename in os.listdir(transcripts_dir):
            file_path = os.path.join(transcripts_dir, filename)
            # Add parent folder to S3 key
            s3_key = f"{parent_folder}/{city_folder}/transcripts/{filename}"
            
            try:
                s3_client.upload_file(file_path, bucket_name, s3_key)
                uploaded_files.append(s3_key)
                logger.info(f"[{city_key}] Successfully uploaded {filename} to S3")
            except Exception as e:
                logger.error(f"[{city_key}] Error uploading {filename} to S3: {str(e)}")
        
        # Update CSV path with parent folder
        if city_key == "NewYork":
            csv_path = os.path.join(local_output_dir, "nyc_vlog_transcripts.csv")
            s3_csv_key = f"{parent_folder}/{city_folder}/nyc_vlog_transcripts.csv"
        else:
            csv_path = os.path.join(local_output_dir, f"{city_key.lower()}_vlog_transcripts.csv")
            s3_csv_key = f"{parent_folder}/{city_folder}/{city_key.lower()}_vlog_transcripts.csv"
        
        # Upload CSV with modified S3 path
        if os.path.exists(csv_path):
            try:
                s3_client.upload_file(csv_path, bucket_name, s3_csv_key)
                uploaded_files.append(s3_csv_key)
                logger.info(f"[{city_key}] Successfully uploaded CSV metadata to S3")
            except Exception as e:
                logger.error(f"[{city_key}] Error uploading CSV metadata to S3: {str(e)}")
        
        logger.info(f"[{city_key}] S3 upload summary: {len(uploaded_files)} successful")
        
        return {
            "uploaded_files": uploaded_files,
            "s3_csv_key": s3_csv_key if os.path.exists(csv_path) else None
        }
    except Exception as e:
        logger.exception(f"[{city_key}] Unhandled error uploading to S3: {str(e)}")
        return {
            "uploaded_files": [],
            "error": str(e)
        }

def process_and_embed_city_data(city_key, city_config, credentials, nlp_model, local_output_dir, transcripts_dir):
    """
    Process city transcripts and upload embeddings to Pinecone
    """
    logger.info(f"Starting processing and embedding for {city_key}")
    
    try:
        # Validate credentials
        if not credentials['openai_api_key']:
            logger.error(f"Cannot process data for {city_key}: OpenAI API key not provided")
            return {
                "successful_count": 0,
                "failed_count": 0,
                "total_vectors": 0,
                "error": "OpenAI API key not provided"
            }
        
        if not credentials['pinecone_api_key'] or not credentials['pinecone_index']:
            logger.error(f"Cannot process data for {city_key}: Pinecone credentials not provided")
            return {
                "successful_count": 0,
                "failed_count": 0,
                "total_vectors": 0,
                "error": "Pinecone credentials not provided"
            }
        
        # Initialize OpenAI client
        try:
            logger.info(f"Initializing OpenAI client for {city_key}")
            openai_client = OpenAI(api_key=credentials['openai_api_key'])
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            return {
                "successful_count": 0,
                "failed_count": 0,
                "total_vectors": 0,
                "error": f"Failed to initialize OpenAI client: {str(e)}"
            }
        
        # Initialize Pinecone
        try:
            logger.info(f"Initializing Pinecone for {city_key}")
            pc = Pinecone(api_key=credentials['pinecone_api_key'])
            
            # Check if index exists, if not create it
            existing_indexes = pc.list_indexes().names()
            logger.info(f"Existing Pinecone indexes: {existing_indexes}")
            
            if credentials['pinecone_index'] not in existing_indexes:
                logger.info(f"Creating Pinecone index: {credentials['pinecone_index']}")
                try:
                    pc.create_index(
                        name=credentials['pinecone_index'],
                        dimension=EMBEDDING_DIMENSION,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud=credentials['pinecone_cloud'],
                            region=credentials['pinecone_region']
                        )
                    )
                    logger.info(f"Created Pinecone index: {credentials['pinecone_index']}")
                except Exception as index_e:
                    # Handle region compatibility issues
                    if "Your free plan does not support indexes in the" in str(index_e):
                        logger.warning(f"Region {credentials['pinecone_region']} not supported by free plan, trying us-east-1")
                        try:
                            pc.create_index(
                                name=credentials['pinecone_index'],
                                dimension=EMBEDDING_DIMENSION,
                                metric="cosine",
                                spec=ServerlessSpec(
                                    cloud=credentials['pinecone_cloud'],
                                    region="us-east-1"  # Fallback to us-east-1
                                )
                            )
                            logger.info(f"Created Pinecone index in fallback region us-east-1")
                        except Exception as fallback_e:
                            logger.error(f"Failed to create index in fallback region: {str(fallback_e)}")
                            raise
                    else:
                        raise index_e
            else:
                logger.info(f"Using existing Pinecone index: {credentials['pinecone_index']}")
            
            # Connect to the index
            pinecone_index = pc.Index(credentials['pinecone_index'])
            logger.info("Pinecone client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            return {
                "successful_count": 0,
                "failed_count": 0, 
                "total_vectors": 0,
                "error": f"Failed to initialize Pinecone: {str(e)}"
            }
        
        city_folder = city_config["folder_name"]
        
        # Check if transcript directory exists and contains files
        if not os.path.exists(transcripts_dir):
            logger.error(f"[{city_key}] Transcript directory not found: {transcripts_dir}")
            return {
                "successful_count": 0,
                "failed_count": 0,
                "total_vectors": 0,
                "error": f"Transcript directory not found: {transcripts_dir}"
            }
        
        transcript_files = [f for f in os.listdir(transcripts_dir) if f.endswith('.txt')]
        
        if not transcript_files:
            logger.warning(f"[{city_key}] No transcript files found in {transcripts_dir}")
            return {
                "successful_count": 0,
                "failed_count": 0,
                "total_vectors": 0,
                "error": "No transcript files found"
            }
        
        logger.info(f"[{city_key}] Found {len(transcript_files)} transcript files to process")
        
        successful_count = 0
        failed_count = 0
        total_vectors = 0
        
        for i, filename in enumerate(transcript_files):
            file_path = os.path.join(transcripts_dir, filename)
            logger.info(f"[{city_key}] Processing transcript {i+1}/{len(transcript_files)}: {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract metadata
                metadata = {}
                patterns = {
                    'title': r'Title: (.+)',
                    'channel': r'Channel: (.+)',
                    'video_id': r'Video ID: (.+)',
                    'url': r'URL: (.+)',
                    'published': r'Published: (.+)',
                    'views': r'Views: (\d+)'
                }
                
                for key, pattern in patterns.items():
                    match = re.search(pattern, content)
                    if match:
                        metadata[key] = match.group(1)
                
                # Extract transcript text
                transcript_match = re.search(r'TRANSCRIPT:\s*\n\n([\s\S]+)', content)
                if not transcript_match:
                    logger.error(f"[{city_key}] Could not extract transcript text from {filename}")
                    failed_count += 1
                    continue
                
                transcript_text = transcript_match.group(1)
                
                # Clean the text
                cleaned_text = clean_text(transcript_text)
                logger.info(f"[{city_key}] Cleaned transcript text ({len(cleaned_text)} chars)")
                
                # Add metadata
                s3_key = f"youtube_transcripts/{city_folder}/transcripts/{filename}"
                metadata['s3_key'] = s3_key
                metadata['city'] = city_key
                
                # Make sure the cleaned text isn't too long for spaCy
                if len(cleaned_text) > 1000000:
                    logger.warning(f"[{city_key}] Truncating very long text ({len(cleaned_text)} chars)")
                    cleaned_text = cleaned_text[:1000000]
                
                # Split into chunks - call the function directly
                chunks = chunk_text(cleaned_text, nlp_model)  # Use the function, don't try to access global variable
                logger.info(f"[{city_key}] Created {len(chunks)} chunks from transcript")
                
                # Process and upload each chunk
                chunk_vectors = 0
                chunk_failures = 0
                
                for j, chunk in enumerate(chunks):
                    try:
                        # Create chunk metadata
                        chunk_metadata = dict(metadata)
                        chunk_metadata['chunk_index'] = j
                        chunk_metadata['text_sample'] = chunk[:200] + '...' if len(chunk) > 200 else chunk
                        
                        # Extract entities from chunk
                        extracted_data = extract_entities(chunk, nlp_model)
                        
                        # Prepare metadata for Pinecone
                        chunk_metadata['landmarks'] = list(extracted_data['landmarks'].keys())
                        chunk_metadata['transport'] = list(extracted_data['transport'].keys())
                        chunk_metadata['food'] = list(extracted_data['food'].keys())
                        chunk_metadata['locations'] = extracted_data['locations']
                        
                        # Handle costs separately
                        if extracted_data['costs']:
                            chunk_metadata['costs'] = [str(cost) for cost in extracted_data['costs']]
                            # Add average for numeric costs if possible
                            numeric_costs = []
                            for cost in extracted_data['costs']:
                                if isinstance(cost, str) and '$' in cost:
                                    try:
                                        numeric_costs.append(float(re.sub(r'[^\d.]', '', cost)))
                                    except:
                                        pass
                            if numeric_costs:
                                chunk_metadata['avg_cost'] = sum(numeric_costs) / len(numeric_costs)
                        
                        # Add time references
                        if extracted_data['time_references']:
                            chunk_metadata['time_references'] = [ref[:100] for ref in extracted_data['time_references']]
                        
                        # Get embedding for the text
                        logger.info(f"[{city_key}] Getting embedding for chunk {j+1}/{len(chunks)}")
                        embedding = get_embedding(chunk, openai_client)
                        if not embedding:
                            logger.error(f"[{city_key}] Failed to get embedding for chunk {j+1}")
                            chunk_failures += 1
                            continue
                        
                        # Create a unique ID for the vector
                        vector_id = f"{city_key}_{metadata['video_id']}_{j}"
                        
                        # Upload to Pinecone
                        logger.info(f"[{city_key}] Uploading vector {j+1} to Pinecone")
                        pinecone_index.upsert(
                            vectors=[{
                                'id': vector_id,
                                'values': embedding,
                                'metadata': chunk_metadata
                            }]
                        )
                        chunk_vectors += 1
                        total_vectors += 1
                        logger.info(f"[{city_key}] Successfully uploaded vector {j+1} for {filename}")
                    except Exception as e:
                        logger.error(f"[{city_key}] Error processing chunk {j+1}: {str(e)}")
                        chunk_failures += 1
                
                if chunk_vectors > 0:
                    successful_count += 1
                    logger.info(f"[{city_key}] Successfully processed {chunk_vectors} chunks from {filename}")
                else:
                    failed_count += 1
                    logger.warning(f"[{city_key}] Failed to process any chunks from {filename}")
            
            except Exception as e:
                logger.error(f"[{city_key}] Error processing file {filename}: {str(e)}")
                failed_count += 1
        
        logger.info(f"[{city_key}] Processing complete!")
        logger.info(f"[{city_key}] Successfully processed {successful_count} transcripts")
        logger.info(f"[{city_key}] Failed to process {failed_count} transcripts")
        logger.info(f"[{city_key}] Total vectors uploaded: {total_vectors}")
        
        return {
            "successful_count": successful_count,
            "failed_count": failed_count,
            "total_vectors": total_vectors
        }
    except Exception as e:
        logger.exception(f"[{city_key}] Unhandled error processing and embedding: {str(e)}")
        return {
            "successful_count": 0,
            "failed_count": 0,
            "total_vectors": 0,
            "error": str(e)
        }

def generate_processing_summary(**kwargs):
    logger.info("Generating processing summary")
    
    try:
        ti = kwargs['ti']
        cities = kwargs['dag_run'].conf.get('cities', list(CITIES.keys()))
        
        summary = {
            "total_transcripts": 0,
            "total_s3_files": 0,
            "total_vectors": 0,
            "city_results": {}
        }
        
        for city_key in cities:
            try:
                result = ti.xcom_pull(task_ids=f'process_city_{city_key}')
                
                if result:
                    summary["total_transcripts"] += result.get("transcript_count", 0)
                    summary["total_s3_files"] += result.get("s3_files_uploaded", 0)
                    summary["total_vectors"] += result.get("total_vectors", 0)
                    summary["city_results"][city_key] = result
                    logger.info(f"Retrieved results for {city_key}: {result.get('transcript_count', 0)} transcripts, {result.get('total_vectors', 0)} vectors")
                else:
                    logger.warning(f"No result found for {city_key}")
                    summary["city_results"][city_key] = {
                        "city": city_key,
                        "status": "unknown",
                        "transcript_count": 0,
                        "s3_files_uploaded": 0,
                        "successful_embeddings": 0,
                        "failed_embeddings": 0,
                        "total_vectors": 0
                    }
            except Exception as e:
                logger.error(f"Error retrieving results for {city_key}: {str(e)}")
                summary["city_results"][city_key] = {
                    "city": city_key,
                    "status": "error",
                    "error": str(e)
                }
        
        logger.info("\n===== MULTI-CITY PROCESSING SUMMARY =====")
        logger.info(f"Total transcripts processed: {summary['total_transcripts']}")
        logger.info(f"Total files uploaded to S3: {summary['total_s3_files']}")
        logger.info(f"Total vectors uploaded to Pinecone: {summary['total_vectors']}")
        logger.info("\nPer-city breakdown:")
        
        for city, result in summary["city_results"].items():
            logger.info(f"  {city}: {result.get('transcript_count', 0)} transcripts, {result.get('total_vectors', 0)} vectors")
        
        return summary
    except Exception as e:
        logger.exception(f"Error generating summary: {str(e)}")
        return {
            "error": str(e),
            "total_transcripts": 0,
            "total_s3_files": 0,
            "total_vectors": 0,
            "city_results": {}
        }

def search_videos(youtube, query, max_results=50):
    """Search for videos matching the query."""
    try:
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video",
            relevanceLanguage="en",
            regionCode="US"
        ).execute()
        
        video_ids = [item["id"]["videoId"] for item in search_response["items"]]
        return video_ids, search_response["items"]
    except Exception as e:
        logger.error(f"Error searching videos for query '{query}': {str(e)}")
        raise

def get_video_details(youtube, video_ids):
    """Get detailed information about specific videos."""
    try:
        video_response = youtube.videos().list(
            part="snippet,contentDetails,statistics,recordingDetails",
            id=",".join(video_ids)
        ).execute()
        
        return video_response["items"]
    except Exception as e:
        logger.error(f"Error getting video details: {str(e)}")
        raise

def get_video_transcript(video_id):
    """Get transcript for a YouTube video with error handling and retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            try:
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                # If successful, return immediately
                full_text = " ".join([item.get('text', '') for item in transcript_data])
                return {
                    'text': full_text,
                    'segments': transcript_data
                }
            except NoTranscriptFound:
                logger.info(f"No English transcript found for {video_id}, trying en-US")
                try:
                    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US'])
                    full_text = " ".join([item.get('text', '') for item in transcript_data])
                    return {
                        'text': full_text,
                        'segments': transcript_data
                    }
                except NoTranscriptFound:
                    logger.info(f"No en-US transcript found for {video_id}, trying auto-translate")
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                        for transcript in transcript_list:
                            try:
                                if transcript.language_code != 'en':
                                    logger.info(f"Translating {transcript.language_code} transcript to English for {video_id}")
                                    transcript = transcript.translate('en')
                                
                                transcript_data = transcript.fetch()
                                full_text = " ".join([item['text'] for item in transcript_data])
                                return {
                                    'text': full_text,
                                    'segments': transcript_data
                                }
                            except Exception as e:
                                logger.error(f"Error translating transcript for {video_id}: {str(e)}")
                                continue
                    except Exception as e:
                        logger.error(f"Error listing transcripts for {video_id}: {str(e)}")
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            logger.warning(f"No transcript available for video {video_id}: {str(e)}")
            return None
        except Exception as e:
            if "YouTube is blocking requests from your IP" in str(e):
                # If it's an IP block error, wait longer before retrying
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 30 
                    logger.warning(f"YouTube IP block detected. Waiting {wait_time} seconds before retry {attempt+1}/{max_retries}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Max retries reached for IP block on video {video_id}")
                    return None
            else:
                logger.error(f"Unexpected error retrieving transcript for video {video_id}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)  
                else:
                    return None
    
    logger.warning(f"Could not find any usable transcript for {video_id} after {max_retries} attempts")
    return None

def clean_text(text):
    """Clean and normalize transcript text."""
    if not text:
        return ""
    
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\b(uh|um|like|you know|so|well|actually|basically|literally|obviously)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(subscribe|like|comment|follow|channel|notification|bell)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def extract_city_info(transcript_text, city_landmarks, city_name):
    """Extract city-specific information from transcript text."""
    if not transcript_text:
        return {
            "landmarks": {},
            "costs": [],
            "avg_cost": None,
            "days": [],
            "avg_days": None,
            "transport": {},
            "food": {}
        }
    
    text = transcript_text.lower()
    
    landmark_counts = {}
    for landmark in city_landmarks:
        count = len(re.findall(r'\b' + re.escape(landmark) + r'\b', text))
        if count > 0:
            landmark_counts[landmark] = count
    
    cost_patterns = [
        r'\$(\d+(?:,\d+)*(?:\.\d+)?)',  
        r'(\d+) dollars', 
        r'cost(?:s)? (?:about|around)? \$?(\d+)',
        r'budget of \$?(\d+)',
        r'spent \$?(\d+)'
    ]
    
    costs = []
    for pattern in cost_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):  
                match = match[0]  
            clean_match = match.replace(',', '')
            try:
                costs.append(float(clean_match))
            except ValueError:
                continue
    
    city_name_words = city_name.lower().split()
    city_pattern = '|'.join([re.escape(word) for word in city_name_words])
    
    days_patterns = [
        rf'(\d+) days? in (?:{city_pattern})',
        r'spent (\d+) days?',
        r'stay for (\d+) days?',
        r'(\d+)-day (?:trip|itinerary)'
    ]
    
    days = []
    for pattern in days_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                days.append(int(match))
            except ValueError:
                continue
    
    transport_keywords = [
        "subway", "metro", "taxi", "uber", "lyft", "yellow cab", "train", 
        "bus", "bike", "walking", "ferry", "tram", "cable car"
    ]
    
    transport_mentions = {}
    for transport in transport_keywords:
        count = len(re.findall(r'\b' + re.escape(transport) + r'\b', text))
        if count > 0:
            transport_mentions[transport] = count
    
    food_keywords = [
        "pizza", "bagel", "cheesecake", "hotdog", "hot dog", "pretzel", "deli", 
        "restaurant", "cafe", "coffee", "food truck", "halal", "seafood", "burger"
    ]
    
    food_mentions = {}
    for food in food_keywords:
        count = len(re.findall(r'\b' + re.escape(food) + r'\b', text))
        if count > 0:
            food_mentions[food] = count
    
    return {
        "landmarks": landmark_counts,
        "costs": costs,
        "avg_cost": sum(costs) / len(costs) if costs else None,
        "days": days,
        "avg_days": sum(days) / len(days) if days else None,
        "transport": transport_mentions,
        "food": food_mentions
    }

def extract_entities(text, nlp):
    """Extract city-specific information from text using NLP."""
    try:
        doc = nlp(text)
        
        data = {
            "landmarks": defaultdict(int),
            "transport": defaultdict(int),
            "food": defaultdict(int),
            "costs": [],
            "time_references": [],
            "locations": []
        }
        
        # Extract named locations
        for ent in doc.ents:
            if ent.label_ in ["GPE", "FAC", "ORG", "LOC"]:
                data["locations"].append(ent.text)
        
        # Process by sentences for context-aware extraction
        for sent in doc.sents:
            s = sent.text.lower()
            
            # Landmarks
            for keyword in LANDMARK_KEYWORDS:
                if keyword in s:
                    for ent in sent.ents:
                        if ent.label_ in ["GPE", "FAC", "ORG", "LOC"]:
                            data["landmarks"][ent.text.lower()] += 1
            
            # Transportation
            for keyword in TRANSPORT_KEYWORDS:
                if keyword in s:
                    data["transport"][keyword] += 1
            
            # Food
            for keyword in FOOD_KEYWORDS:
                if keyword in s:
                    data["food"][keyword] += 1
            
            # Costs
            for pattern in COST_PATTERNS:
                matches = re.findall(pattern, s)
                if matches:
                    data["costs"].extend(matches)
            
            # Time references
            for pattern in TIME_PATTERNS:
                if re.search(pattern, s):
                    data["time_references"].append(sent.text.strip())
                    break  # Only add each sentence once
        
        # Clean up and deduplicate
        data["locations"] = list(set(data["locations"]))
        
        return data
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        # Return empty data structure in case of error
        return {
            "landmarks": defaultdict(int),
            "transport": defaultdict(int),
            "food": defaultdict(int),
            "costs": [],
            "time_references": [],
            "locations": []
        }

def chunk_text(text, nlp):
    """Split text into semantic chunks for processing."""
    try:
        chunks = []
        
        # First try to split by time/day references
        time_chunk_texts = split_by_time_references(text)
        
        if time_chunk_texts and len(time_chunk_texts) > 1:
            # Use time-based chunks if found
            chunks = time_chunk_texts
            logger.info(f"Split text into {len(chunks)} time-based chunks")
        else:
            # Otherwise use character-based chunking with sentence boundaries
            doc = nlp(text)
            current_chunk = []
            current_length = 0
            
            for sent in doc.sents:
                sent_text = sent.text.strip()
                if not sent_text:
                    continue
                
                if current_length + len(sent_text) > CHUNK_SIZE and current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # Keep some overlap for context
                    current_chunk = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                    current_length = sum(len(s) for s in current_chunk)
                
                current_chunk.append(sent_text)
                current_length += len(sent_text)
            
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            logger.info(f"Split text into {len(chunks)} sentence-based chunks")
        
        # Ensure we have at least one chunk
        if not chunks and text:
            logger.warning("Chunking failed, using original text as a single chunk")
            chunks = [text]
        
        return chunks
    except Exception as e:
        logger.error(f"Error chunking text: {str(e)}")
        # Return original text as a single chunk in case of error
        return [text] if text else []

def split_by_time_references(text):
    """Split text by time references like days, morning, afternoon etc."""
    try:
        day_patterns = [
            r'(?:^|\n|\. )day\s+\d+',
            r'(?:^|\n|\. )(?:first|second|third|fourth)\s+day',
            r'(?:^|\n|\. )(?:morning|afternoon|evening)'
        ]
        
        # Find all breaks
        break_positions = []
        for pattern in day_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                break_positions.append(match.start())
        
        # If we have multiple break positions, use them to split the text
        if len(break_positions) >= 2:
            break_positions.sort()
            chunks = []
            
            for i in range(len(break_positions)):
                start = break_positions[i]
                end = break_positions[i+1] if i < len(break_positions) - 1 else len(text)
                
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
            
            return chunks
        
        return None
    except Exception as e:
        logger.error(f"Error splitting by time references: {str(e)}")
        return None

def get_embedding(text, client):
    """Get embeddings for a text using OpenAI's API."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Error getting embedding, retrying in 2 seconds: {str(e)}")
                time.sleep(2)
            else:
                logger.error(f"Failed to get embedding after {max_retries} attempts: {str(e)}")
                return None

# DAG definition
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'city_travel_transcripts_processing',
    default_args=default_args,
    description='Process YouTube travel vlog transcripts for multiple cities',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['travel', 'nlp', 'transcripts'],
) as dag:
    
    start_task = DummyOperator(
        task_id='start_processing',
    )
    
    city_processors = []
    for city_key in CITIES.keys():
        city_task = PythonOperator(
            task_id=f'process_city_{city_key}',
            python_callable=process_city,
            op_kwargs={'city_key': city_key},
        )
        city_processors.append(city_task)
    
    summary_task = PythonOperator(
        task_id='generate_summary',
        python_callable=generate_processing_summary,
    )
    
    end_task = DummyOperator(
        task_id='end_processing',
    )
    
    # Set up task dependencies
    start_task >> city_processors >> summary_task >> end_task