from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.responses import StreamingResponse, JSONResponse
import boto3
import json
from botocore.exceptions import ClientError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr, validator
from typing import List, Dict, Optional, Any
import io
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
import logging
import bcrypt
import pymysql
from google.cloud import storage
from google.oauth2 import service_account
import openai
import os, pathlib
from pathlib import Path
from pdf_processor import PDFProcessor
import requests
from openai import OpenAI
 
# Load environment variables
load_dotenv()
 
env_path = pathlib.Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
 
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
app = FastAPI()
 
pdf_processor = PDFProcessor()
 
# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
# OpenAI settings
openai.api_key = os.getenv("OPENAI_API_KEY")
 
# GCP bucket settings
TXT_BUCKET_NAME = os.getenv("TXT_BUCKET_NAME")
 
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
# Database connection
def load_sql_db_config():
    try:
        connection = pymysql.connect(
            user=os.getenv("GCP_SQL_USER"),
            password=os.getenv("GCP_SQL_PASSWORD"),
            host=os.getenv("GCP_SQL_HOST"),
            database=os.getenv("GCP_SQL_DATABASE"),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        logger.error(f"Error connecting to Cloud SQL: {e}")
        return None
 
# Google Cloud Storage client setup
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_path:
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    storage_client = storage.Client(credentials=credentials)
else:
    storage_client = storage.Client()
 
# Models
class UserRegister(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
 
    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password should be at least 8 characters long')
        if not any(char.islower() for char in value):
            raise ValueError('Password should contain at least one lowercase letter')
        if not any(char.isupper() for char in value):
            raise ValueError('Password should contain at least one uppercase letter')
        return value
 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
 
 
 
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        logger.error(f"Invalid password hash encountered")
        return False
 
def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email
 
 
    connection = load_sql_db_config()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        with connection.cursor() as cursor:
            check_user_sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(check_user_sql, (user.email,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
 
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
 
            sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
            cursor.execute(sql, (user.email, hashed_password))
        connection.commit()
        return {"message": "User registered successfully"}
 
    except pymysql.Error as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
 
    finally:
        connection.close()
 
@app.post("/register")
def register_user(user: UserRegister):
    connection = load_sql_db_config()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        with connection.cursor() as cursor:
            check_user_sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(check_user_sql, (user.email,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
 
            # Check if password meets the minimum length requirement
            if len(user.password) < 8:
                raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain at least one uppercase letter and one lowercase letter.")
 
            hashed_password = hash_password(user.password)
 
            sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
            cursor.execute(sql, (user.email, hashed_password))
        connection.commit()
        return {"message": "User registered successfully"}
 
    except pymysql.Error as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
 
    finally:
        connection.close()
 
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    connection = load_sql_db_config()
    if not connection:
        logger.error("Database connection failed")
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (form_data.username,))
            user = cursor.fetchone()
            if not user:
                logger.warning(f"Login attempt failed: User not found - {form_data.username}")
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email. Please check your login credentials and try again.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
           
            # Verify the password
            if not verify_password(form_data.password, user['password']):
                logger.warning(f"Login attempt failed: Incorrect password - {form_data.username}")
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect password. Please check your login credentials and try again.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
           
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_jwt_token(
                data={"sub": user['email']}, expires_delta=access_token_expires
            )
            logger.info(f"Login successful: {form_data.username}")
            return {"access_token": access_token, "token_type": "bearer"}
    except pymysql.Error as e:
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Please check your login credentials and try again")
    finally:
        connection.close()
@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
 
@app.get("/test-db-connection")
async def test_db_connection():
    connection = load_sql_db_config()
    if not connection:
        raise HTTPException(status_code=500, detail="Failed to establish database connection")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        return {"message": "Database connection successful", "test_query_result": result}
    except pymysql.Error as e:
        logger.error(f"Database connection test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection test failed: {str(e)}")
    finally:
        connection.close()
 
 
###########################AWS  streamlit show documents ############
class PDFMetadata(BaseModel):
    title: str
    metadata: Dict
    summary: Optional[str]
 
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
 
def get_s3_client():
    """Create and return an S3 client"""
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
 
@app.get("/pdfs/all", response_model=List[PDFMetadata])
async def get_all_pdfs():
    """Get all PDFs with their metadata and cover image URLs"""
    try:
        s3_client = get_s3_client()
        folders = set()
       
        # List all objects in the bucket
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=BUCKET_NAME):
            if 'Contents' in page:
                for obj in page['Contents']:
                    parts = obj['Key'].split('/')
                    if len(parts) > 1:
                        folders.add(parts[0])
       
        # Get metadata and cover URLs for each PDF
        pdfs = []
        for folder in sorted(folders):
            try:
                # Get metadata
                metadata_key = f"{folder}/metadata.json"
                metadata_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_key)
                metadata = json.loads(metadata_obj['Body'].read().decode('utf-8'))
            except ClientError:
                metadata = {}
           
            try:
                # Get summary
                summary_key = f"{folder}/summary.txt"
                summary_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=summary_key)
                summary = summary_obj['Body'].read().decode('utf-8')
            except ClientError:
                summary = "No summary available"
           
            # Create cover image URL
            cover_url = f"/pdfs/{folder}/cover"
           
            pdfs.append(PDFMetadata(
                title=folder,
                metadata=metadata,
                summary=summary,
                cover_url=cover_url
            ))
       
        return pdfs
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/pdfs/{folder_name}/document")
async def get_pdf_document(folder_name: str):
    """Stream the PDF document"""
    try:
        s3_client = get_s3_client()
        pdf_key = f"{folder_name}/document.pdf"
       
        try:
            pdf_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=pdf_key)
            pdf_content = pdf_obj['Body'].read()
           
            return StreamingResponse(
                io.BytesIO(pdf_content),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'inline; filename="{folder_name}.pdf"'
                }
            )
        except ClientError:
            raise HTTPException(status_code=404, detail="PDF not found")
           
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/pdfs/{folder_name}/cover")
async def get_cover_image(folder_name: str):
    """Stream the cover image"""
    try:
        s3_client = get_s3_client()
        image_key = f"{folder_name}/image.jpg"
       
        try:
            image_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=image_key)
            image_content = image_obj['Body'].read()
           
            return StreamingResponse(
                io.BytesIO(image_content),
                media_type="image/jpeg",
                headers={
                    "Content-Disposition": f'inline; filename="{folder_name}_cover.jpg"'
                }
            )
        except ClientError:
            raise HTTPException(status_code=404, detail="Cover image not found")
           
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
   
#################################################generte summay################
# NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
# NVIDIA_API_URL = os.getenv("NVIDIA_API_URL")
# Initialize OpenAI client with NVIDIA endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv('NVIDIA_API_KEY')
)
 
@app.get("/pdfs/{folder_name}/process")
async def process_pdf_content(folder_name: str):
    try:
        # Get PDF from S3
        s3_client = get_s3_client()
        try:
            response = s3_client.get_object(
                Bucket=os.getenv("BUCKET_NAME"),
                Key=f"{folder_name}/document.pdf"
            )
            pdf_content = response['Body'].read()
        except Exception as e:
            logger.error(f"Error reading PDF from S3: {str(e)}")
            raise HTTPException(status_code=404, detail="PDF not found")
       
        # Process PDF and get extracted text
        extracted_text = pdf_processor.process_pdf(pdf_content)
       
        # Truncate text if too long (add this section)
        max_chars = 25000  # Adjust this based on testing
        full_text = extracted_text
        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars] + "\n\n[Text truncated due to length...]"
       
        # Prepare prompt for summary (your existing prompt)
        prompt = f"""Please analyze this document and provide a structured summary following this exact format:
 
Document text:
{extracted_text}
 
Please structure your response exactly as follows:
 
Key Points:
- [First key point]
- [Second key point]
- [Third key point]
(provide 3-5 key points)
 
Main Topics:
- [First main topic]
- [Second main topic]
- [Third main topic]
(provide 2-3 main topics)
 
Summary:
[Provide a 2-3 paragraph summary here]
 
Important: Please maintain this exact structure and format in your response, including the headers 'Key Points:', 'Main Topics:', and 'Summary:'."""
 
        try:
            # Generate summary using NVIDIA's API
            completion = client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct-v0.1",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
           
            summary_text = completion.choices[0].message.content
           
            # Process the response into structured format
            sections = summary_text.split('\n\n')
            key_points = []
            main_topics = []
            detailed_summary = ""
           
            for section in sections:
                section = section.strip()
                if "key points:" in section.lower():
                    points = [p.strip('- ').strip() for p in section.split('\n')[1:]]
                    key_points = [p for p in points if p]
                elif "main topics:" in section.lower():
                    topics = [t.strip('- ').strip() for t in section.split('\n')[1:]]
                    main_topics = [t for t in topics if t]
                elif "summary:" in section.lower():
                    detailed_summary = section.split('Summary:', 1)[-1].strip()
           
            structured_summary = {
                "key_points": key_points,
                "main_topics": main_topics,
                "summary": detailed_summary or summary_text
            }
           
            return {
                "extracted_text": full_text,  # Return full text but use truncated for processing
                "summary": structured_summary
            }
           
        except Exception as e:
            logger.error(f"Error with NVIDIA API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
           
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
 
# Test endpoint
@app.get("/test-llama")
async def test_llama():
    """Test NVIDIA Llama API connection"""
    try:
        completion = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct-v0.1",
            messages=[
                {"role": "user", "content": "Say hello and confirm you're working!"}
            ],
            temperature=0.5,
            max_tokens=50
        )
       
        return {
            "status": "success",
            "response": completion.choices[0].message.content,
            "model": "mistralai/mixtral-8x7b-instruct-v0.1"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "model": "mistralai/mixtral-8x7b-instruct-v0.1"
        }
 
############################ Page3 view ppdf######################
import nest_asyncio
nest_asyncio.apply()
 
from fastapi import FastAPI, HTTPException
from llama_parse import LlamaParse
from typing import List, Dict, Any
import os
from pathlib import Path
import base64
import json
import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from PIL import Image
import io
from dotenv import load_dotenv
from llama_index.core.schema import TextNode
import re
# Load environment variables
load_dotenv()
 
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
 
# Initialize environment variables
LLAMAPARSE_API_KEY = os.getenv("LLAMAPARSE_API_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
 
# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
EXTRACTION_DIR = os.path.join(STORAGE_DIR, "extractions")
IMAGES_DIR = os.path.join(STORAGE_DIR, "images")
 
# Create directories if they don't exist
os.makedirs(EXTRACTION_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
 
def get_s3_client():
    """Create and return an S3 client"""
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        return client
    except Exception as e:
        logger.error(f"Failed to create S3 client: {str(e)}")
        raise
 
def get_page_number(file_name: str) -> int:
    """Extract page number from image filename."""
    match = re.search(r"-page-(\d+)\.jpg$", str(file_name))
    if match:
        return int(match.group(1))
    return 0

def _get_sorted_image_files(image_dir: str) -> List[Path]:
    """Get image files sorted by page number."""
    raw_files = [f for f in list(Path(image_dir).iterdir()) if f.is_file()]
    sorted_files = sorted(raw_files, key=get_page_number)
    return sorted_files




class PDFProcessor_llama:
    def __init__(self, api_key: str):
        """Initialize LlamaParse with enhanced multimodal configuration"""
        self.parser = LlamaParse(
            api_key=api_key,
            result_type="markdown",
            use_vendor_multimodal_model=True,
            vendor_multimodal_model_name="anthropic-sonnet-3.5"
        )
    
    def _get_sorted_image_files(self, image_dir: str) -> List[str]:
        """Get sorted list of image files from directory based on page numbers."""
        if not os.path.exists(image_dir):
            return []
            
        def extract_page_num(filename: str) -> int:
            try:
                # Extract page number from filename format "page_{num}.jpg"
                if "page_" in filename:
                    return int(filename.split("page_")[1].split(".")[0])
                return 0
            except:
                return 0
                
        image_files = []
        for filename in os.listdir(image_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(image_dir, filename)
                page_num = extract_page_num(filename)
                image_files.append((page_num, full_path))
                
        # Sort by page number and return only the paths
        return [path for _, path in sorted(image_files)]

    def get_text_nodes(self, md_json_list: List[Dict], image_dir: Optional[str] = None) -> List[TextNode]:
        """Create text nodes from parsed PDF content with correctly mapped image metadata."""
        nodes = []
        
        # Get sorted image files first
        sorted_images = self._get_sorted_image_files(image_dir) if image_dir else []
        logger.info(f"Found {len(sorted_images)} sorted images")
        
        # Create a mapping of page numbers to image paths
        page_to_image = {}
        for image_path in sorted_images:
            try:
                # Extract page number from image filename
                filename = os.path.basename(image_path)
                if "page_" in filename:
                    page_num = int(filename.split("page_")[1].split(".")[0])
                    page_to_image[page_num] = image_path
            except Exception as e:
                logger.error(f"Error mapping image {image_path}: {str(e)}")
        
        # Create nodes with correct image mappings
        for page in md_json_list:
            page_num = page.get('page', 0)
            content = page.get('md', '').strip()
            
            if not content or content == "NO_CONTENT_HERE":
                continue
            
            # Get corresponding image for this page number
            image_path = page_to_image.get(page_num)
            if image_path:
                logger.info(f"Mapping image {image_path} to page {page_num}")
            
            chunk_metadata = {
                "page_num": page_num,
                "image_path": image_path,
                "parsed_text_markdown": content
            }
            
            node = TextNode(
                text=content,
                metadata=chunk_metadata,
            )
            nodes.append(node)
        
        return nodes

    def process_pdf(self, pdf_path: str, folder_name: str) -> Dict[str, Any]:
        """Process PDF and extract content using LlamaParse with indexing"""
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Get markdown content
            logger.info("Getting JSON result...")
            md_json_objs = self.parser.get_json_result(pdf_path)
            
            if not md_json_objs or not isinstance(md_json_objs, list):
                raise ValueError("Invalid JSON result from parser")
            
            md_json_list = md_json_objs[0]["pages"]
            logger.info(f"Successfully processed {len(md_json_list)} pages")
            
            # Create image directory
            image_dir = os.path.abspath(os.path.join(IMAGES_DIR, folder_name))
            os.makedirs(image_dir, exist_ok=True)
            logger.info(f"Created image directory at: {image_dir}")
            
            # Extract images
            logger.info("Extracting images...")
            image_dicts = self.parser.get_images(
                md_json_objs,
                image_dir
            )
            logger.info(f"Found {len(image_dicts) if image_dicts else 0} images")
            
            # Create text nodes with correct image metadata
            text_nodes = self.get_text_nodes(md_json_list, image_dir)
            logger.info(f"Created {len(text_nodes)} text nodes")
            
            # Validate node creation
            for node in text_nodes:
                page_num = node.metadata.get('page_num')
                image_path = node.metadata.get('image_path')
                if image_path:
                    logger.info(f"Node for page {page_num} has image: {image_path}")
            
            # Structure the content
            extracted_content = {
                "pages": [],
                "images": [],
                "nodes": [],
                "metadata": {
                    "total_pages": len(md_json_list),
                    "file_name": os.path.basename(pdf_path),
                    "extraction_time": datetime.now().isoformat()
                }
            }
            
            # Process pages
            for page in md_json_list:
                extracted_content["pages"].append({
                    "page_num": page.get("page", 0),
                    "content": page.get("md", ""),
                    "has_images": bool(page.get("images", []))
                })
            
            # Process images
            if image_dicts:
                for idx, img in enumerate(image_dicts):
                    try:
                        page_num = img.get("page_number", 0)
                        image_data = {
                            "file_name": f"page_{page_num}.jpg",
                            "local_path": os.path.join(image_dir, f"page_{page_num}.jpg"),
                            "page_number": page_num,
                            "caption": img.get("caption", "")
                        }
                        extracted_content["images"].append(image_data)
                    except Exception as e:
                        logger.error(f"Error processing image {idx}: {str(e)}")
            
            # Add nodes
            for node in text_nodes:
                extracted_content["nodes"].append({
                    "page_num": node.metadata.get("page_num"),
                    "image_path": node.metadata.get("image_path"),
                    "content": node.metadata.get("parsed_text_markdown")
                })
            
            # Save content
            output_dir = os.path.join(EXTRACTION_DIR, folder_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Save markdown
            markdown_path = os.path.join(output_dir, "extracted_content.md")
            markdown_content = "\n\n".join(page["content"] for page in extracted_content["pages"])
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            # Save nodes
            nodes_path = os.path.join(output_dir, "text_nodes.json")
            with open(nodes_path, "w", encoding="utf-8") as f:
                json.dump([{
                    "page_num": node.metadata.get("page_num"),
                    "image_path": node.metadata.get("image_path"),
                    "content": node.metadata.get("parsed_text_markdown")
                } for node in text_nodes], f, indent=2)
            
            return extracted_content
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
        
        
         
# Add this test endpoint to verify paths and processing
@app.post("/pdfs/{folder_name}/test-extract")
async def test_extraction(folder_name: str):
    """Test extraction process with detailed logging"""
    try:
        # Log environment setup
        logger.info("Testing extraction process...")
        logger.info(f"Base directory: {BASE_DIR}")
        logger.info(f"Storage directory: {STORAGE_DIR}")
        logger.info(f"Images directory: {IMAGES_DIR}")
        
        # Verify API key
        if not LLAMAPARSE_API_KEY:
            return {
                "status": "error",
                "detail": "LLAMAPARSE_API_KEY not configured"
            }
        logger.info("API key found")
        
        # Get PDF from S3
        s3_client = get_s3_client()
        pdf_key = f"{folder_name}/document.pdf"
        
        try:
            # Get PDF content
            pdf_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=pdf_key)
            pdf_content = pdf_obj['Body'].read()
            logger.info(f"Retrieved PDF from S3: {len(pdf_content)} bytes")
            
            # Create folder for extraction
            temp_dir = os.path.join(EXTRACTION_DIR, folder_name)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save PDF temporarily
            temp_path = os.path.join(temp_dir, "document.pdf")
            with open(temp_path, "wb") as f:
                f.write(pdf_content)
            logger.info(f"Saved PDF to: {temp_path}")
            
            # Initialize processor
            processor = PDFProcessor_llama(api_key=LLAMAPARSE_API_KEY)
            
            # Process content
            extracted_content = processor.process_pdf(temp_path, folder_name)
            
            # Save extracted content as markdown
            markdown_path = os.path.join(temp_dir, "extracted_content.md")
            markdown_content = ""
            
            # Convert extracted content to markdown format
            for page in extracted_content["pages"]:
                markdown_content += f"\n\n## Page {page['page_num']}\n\n"
                markdown_content += page["content"]
            
            # Save markdown content
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            logger.info(f"Saved markdown content to: {markdown_path}")
            
            # Save image index if there are images
            if extracted_content["images"]:
                image_index_path = os.path.join(temp_dir, "image_index.json")
                with open(image_index_path, "w") as f:
                    json.dump(extracted_content["images"], f, indent=2)
                logger.info(f"Saved image index to: {image_index_path}")
            
            # Clean up temporary PDF
            os.remove(temp_path)
            
            return {
                "status": "success",
                "paths": {
                    "base_dir": BASE_DIR,
                    "storage_dir": STORAGE_DIR,
                    "images_dir": IMAGES_DIR,
                    "markdown_path": markdown_path,
                    "image_index_path": image_index_path if extracted_content["images"] else None
                },
                "content": extracted_content
            }
            
        except ClientError as e:
            return {
                "status": "error",
                "detail": str(e),
                "error_code": e.response['Error']['Code'] if hasattr(e, 'response') else None
            }
            
    except Exception as e:
        logger.error(f"Error in test extraction: {str(e)}")
        return {
            "status": "error",
            "detail": str(e)
        }


@app.post("/pdfs/{folder_name}/get-nodes")
async def get_pdf_nodes(folder_name: str):
    """Get text nodes for a processed PDF"""
    try:
        nodes_path = os.path.join(EXTRACTION_DIR, folder_name, "text_nodes.json")
        
        if not os.path.exists(nodes_path):
            raise HTTPException(
                status_code=404,
                detail="Nodes data not found. Please process the PDF first."
            )
        
        with open(nodes_path, "r", encoding="utf-8") as f:
            nodes_data = json.load(f)
        
        return {
            "status": "success",
            "folder_name": folder_name,
            "total_nodes": len(nodes_data),
            "nodes": nodes_data
        }
        
    except Exception as e:
        logger.error(f"Error retrieving nodes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

######################Embedding#######################
from text_processor import TextProcessor

text_processor = TextProcessor()
class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
    pdf_id: str
    search_all: Optional[bool] = False

class SearchResult(BaseModel):
    note_id: Optional[str] = None
    query: str
    original_query: Optional[str] = None
    timestamp: Optional[str] = None
    content: str
    image_paths: List[str] = []
    match_type: str  # "exact", "semantic", or "document"
    source: str      # "research_note" or "document"
 
@app.post("/pdfs/{folder_name}/process-embeddings")
async def process_pdf_embeddings(folder_name: str):
    """Process PDF nodes and store embeddings"""
    try:
        # Get nodes data
        nodes_path = os.path.join(EXTRACTION_DIR, folder_name, "text_nodes.json")
        
        if not os.path.exists(nodes_path):
            raise HTTPException(
                status_code=404,
                detail="Nodes data not found. Please process the PDF first."
            )
        
        # Read nodes data
        with open(nodes_path, "r", encoding="utf-8") as f:
            nodes_data = json.load(f)
            
        # Log the structure of first node for debugging
        if nodes_data and len(nodes_data) > 0:
            logger.info(f"Sample node structure: {json.dumps(nodes_data[0], indent=2)}")
        
        # Process and store nodes
        text_processor.process_nodes_and_store(nodes_data, folder_name)
        
        return {
            "status": "success",
            "message": f"Successfully processed and stored embeddings for {folder_name}",
            "total_nodes": len(nodes_data)
        }
        
    except Exception as e:
        logger.error(f"Error processing embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_image_info(folder_name: str):
    """Get information about extracted images"""
    try:
        image_index_path = os.path.join(EXTRACTION_DIR, folder_name, "image_index.json")
        
        if not os.path.exists(image_index_path):
            raise HTTPException(
                status_code=404,
                detail="Image index not found. Please process the PDF first."
            )
            
        with open(image_index_path, "r") as f:
            image_info = json.load(f)
            
        return {
            "folder_name": folder_name,
            "total_images": len(image_info),
            "images": image_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/pdfs/{folder_name}/search")
async def search_pdfs(folder_name: str, query: SearchQuery):
    """Search through specific PDF content using embeddings"""
    try:
        # Create filter for specific PDF
        filter_condition = {"pdf_id": folder_name}
        
        # Get search results with filter
        results = text_processor.search_similar(
            query.query, 
            query.top_k,
            filter_condition=filter_condition
        )
        
        return {
            "query": query.query,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error searching PDF {folder_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel, Field
from typing import List, Union, Optional, Dict, Any
from datetime import datetime
import logging
from fastapi import HTTPException

class TextBlock(BaseModel):
    """Text block."""
    text: str = Field(..., description="The text for this block.")

class ImageBlock(BaseModel):
    """Image block."""
    file_path: str = Field(..., description="File path to the image.")

class ReportOutput(BaseModel):
    """Data model for a report.
    Can contain a mix of text and image blocks. MUST contain at least one image block.
    """
    blocks: List[Union[TextBlock, ImageBlock]] = Field(
        ..., description="A list of text and image blocks."
    )
    

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union, Optional, Dict, Any
from datetime import datetime
import logging
from fastapi.responses import FileResponse, JSONResponse

import os
import urllib.parse
from pathlib import Path

# Update the Pydantic models - remove IPython dependency
class TextBlock(BaseModel):
    """Text block."""
    text: str = Field(..., description="The text for this block.")

class ImageBlock(BaseModel):
    """Image block."""
    file_path: str = Field(..., description="File path to the image.")

class ReportOutput(BaseModel):
    """Data model for a report."""
    blocks: List[Union[TextBlock, ImageBlock]] = Field(
        ..., 
        description="A list of text and image blocks."
    )

    def render(self) -> None:
        """Render all blocks in the report."""
        for block in self.blocks:
            if isinstance(block, TextBlock):
                display(Markdown(block.text))
            elif isinstance(block, ImageBlock):
                display(Image(filename=block.file_path))
  
  
@app.post("/pdfs/{folder_name}/search-and-process")
async def search_and_process_chunks(folder_name: str, query: SearchQuery):
    """
    Search through PDF content and generate a structured report with text and images.
    Uses direct image paths from search results instead of scanning directories.
    """
    try:
        # 1. Get search results
        filter_condition = {"pdf_id": folder_name}
        search_results = text_processor.search_similar(
            query.query,
            query.top_k,
            filter_condition=filter_condition
        )
        
        # 2. Process image paths directly from search results
        for chunk in search_results:
            if chunk.get('image_path'):
                # Create URL-safe paths for frontend
                safe_folder = urllib.parse.quote(folder_name)
                # Extract filename from full path
                image_filename = os.path.basename(chunk['image_path'])
                safe_filename = urllib.parse.quote(image_filename)
                chunk['image_url'] = f"/images/{safe_folder}/{safe_filename}"
                logger.info(f"Created image URL for chunk: {chunk['image_url']}")
        
        # 3. Prepare chunks text for LLM with explicit image paths
        chunks_text = [f"""
            Chunk {i}:
            Content from Page {chunk['page_num']}:
            {chunk['content']}
            Relevance Score: {chunk['score']}
            Image Reference: {chunk.get('image_url', 'None')}
            """ for i, chunk in enumerate(search_results, 1)]
        
        # 4. Define system prompt with emphasis on using provided image paths
        system_prompt = """
You are a report generation assistant tasked with producing a well-formatted report from parsed content.
        When referencing images, use ONLY the Image Reference paths provided in the chunks.
        
        Format your response with clear text sections and image references:
        - Start text sections with [TEXT] and end with [/TEXT]
        - Reference images using exact provided paths: [IMAGE]<image_url_from_chunk>[/IMAGE]
        
    FORMAT REQUIREMENTS:
       1. Text Sections:
          - Begin with [TEXT]
          - End with [/TEXT]
          - Must use markdown formatting
          - Keep each section between 50-150 words
          - Maximum 3 text sections total
       
       2. Image References:
          - Format: [IMAGE]<exact_image_url_from_chunk>[/IMAGE]
          - Place immediately after relevant text
          - Use only image paths provided in chunks
          - Include 1-3 images total
       
       3. Data Formatting:
          - Present numbers in clear, readable format
          - Use tables for comparing multiple values
          - Include units where applicable
       
       STRICT RULES:
       - Never return an empty response
       - Never mention chunk numbers
       - Never create or modify image URLs
       - Never exceed 400 words total
       - Always verify response contains both text and image before completing        """
        
        # 5. Define user prompt with emphasis on image handling
        base_prompt = f"""
        Analyze these chunks and generate a structured report:
        
        {'-' * 50}
        {'\n'.join(chunks_text)}
        {'-' * 50}
        
        Query: {query.query}
        
        Important:
        - Use the exact Image Reference paths provided in the chunks
        - Include images only where they directly support the text
        - Format your response as alternating text and image sections
        """
                
        # 6. Get LLM response
        llm_response = text_processor.embeddings_client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct-v0.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        # 7. Process LLM response into blocks
        content = llm_response.choices[0].message.content
        report_blocks = []
        
        # Split content into text and image blocks
        text_blocks = re.findall(r'\[TEXT\](.*?)\[/TEXT\]', content, re.DOTALL)
        image_blocks = re.findall(r'\[IMAGE\](.*?)\[/IMAGE\]', content, re.DOTALL)
        
        # Interleave text and image blocks
        for text in text_blocks:
            clean_text = text.strip()
            clean_text = re.sub(r'```[a-zA-Z]*\n|```', '', clean_text)
            report_blocks.append(TextBlock(text=clean_text))
            
            # Look for corresponding image reference in chunks
            for image_ref in image_blocks:
                image_ref = image_ref.strip()
                if any(chunk.get('image_url') == image_ref for chunk in search_results):
                    report_blocks.append(ImageBlock(file_path=image_ref))
                    image_blocks.remove(image_ref)  # Remove processed image
                    break
        
        # 8. Create final report
        report = ReportOutput(blocks=report_blocks)
        
        # Log the final report structure for debugging
        logger.info(f"Final report blocks: {[type(block).__name__ for block in report_blocks]}")
        logger.info(f"Image blocks: {[block.file_path for block in report_blocks if isinstance(block, ImageBlock)]}")
        
        # 9. Return processed results
        return {
            "status": "success",
            "report": report.dict(),
            "metadata": {
                "query": query.query,
                "folder_name": folder_name,
                "chunks_analyzed": len(search_results),
                "model_used": "mixtral-8x7b-instruct-v0.1",
                "processing_timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error in report generation: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing report: {str(e)}"
        )

@app.get("/images/{folder_name}/{image_name}")
async def get_image(folder_name: str, image_name: str):
    """Serve images from the storage directory."""
    try:
        # Construct the image path
        image_path = os.path.join("/app/storage/images", folder_name, image_name)
        logger.info(f"Attempting to serve image from path: {image_path}")
        
        # Validate path exists
        if not os.path.exists(image_path):
            logger.error(f"Image not found: {image_path}")
            raise HTTPException(status_code=404, detail="Image not found")
        
        if not os.path.isfile(image_path):
            logger.error(f"Path is not a file: {image_path}")
            raise HTTPException(status_code=400, detail="Invalid image path")
        
        # Serve the file
        return FileResponse(
            path=image_path,
            media_type="image/jpeg",
            filename=image_name
        )
        
    except Exception as e:
        logger.error(f"Error serving image {folder_name}/{image_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))    

@app.get("/debug/check-image/{folder_name}/{image_name}")
async def check_image_path(folder_name: str, image_name: str):
    """Debug endpoint to check image paths"""
    try:
        image_path = os.path.join("/app/storage/images", folder_name, image_name)
        return {
            "requested_path": image_path,
            "exists": os.path.exists(image_path),
            "is_file": os.path.isfile(image_path) if os.path.exists(image_path) else False,
            "parent_exists": os.path.exists(os.path.dirname(image_path)),
            "parent_contents": os.listdir(os.path.dirname(image_path)) if os.path.exists(os.path.dirname(image_path)) else [],
            "absolute_path": os.path.abspath(image_path)
        }
    except Exception as e:
        return {
            "error": str(e),
            "folder_name": folder_name,
            "image_name": image_name
        }
    
#################### Reasearch notes############################


class SaveNoteRequest(BaseModel):
    timestamp: str
    query: str
    text_blocks: List[str]
    image_paths: List[str]

@app.post("/pdfs/{folder_name}/save-note")
async def save_note(folder_name: str, note_data: SaveNoteRequest):
    """Save a research note for a document"""
    try:
        # Validate the request data
        if not note_data.text_blocks:
            raise HTTPException(
                status_code=400,
                detail="No text content provided"
            )
            
        # Create a sanitized version of the note data
        clean_note = {
            "timestamp": note_data.timestamp,
            "query": note_data.query,
            "text_blocks": [block for block in note_data.text_blocks if block.strip()],
            "image_paths": [path for path in note_data.image_paths if path.strip()]
        }
        
        # Save note to Pinecone
        note_id = text_processor.save_research_note(folder_name, clean_note)
        
        return {
            "status": "success",
            "note_id": note_id,
            "message": "Research note saved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error saving note: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving note: {str(e)}"
        )

@app.get("/pdfs/{folder_name}/notes")
async def get_notes(folder_name: str):
    """Get all research notes for a document"""
    try:
        notes = text_processor.get_research_notes(folder_name)
        return {
            "status": "success",
            "notes": notes
        }
    except Exception as e:
        logger.error(f"Error retrieving notes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving notes: {str(e)}"
        )
############################################ Research note searching s##################################################################

@app.post("/pdfs/{folder_name}/search-notes")
async def search_notes(folder_name: str, query: SearchQuery):
    """Search through notes then automatically search document content"""
    try:
        logger.info(f"Searching notes for folder {folder_name} with query: {query.query}")
        
        def normalize_query(q: str) -> str:
            return ' '.join(q.lower().split())

        # Get all notes for the document
        all_notes = text_processor.get_research_notes(folder_name)
        user_query = normalize_query(query.query)
        
        # First try research notes
        research_note_found = False
        for note in all_notes:
            saved_query = normalize_query(note.get('query', ''))
            if user_query == saved_query:
                system_prompt = """
                Analyze if the note content contains the answer to the user's question.
                If yes, provide a clear, well-formatted response using markdown.
                If no, respond with exactly 'NO_ANSWER_PRESENT'
                """
                
                response = text_processor.embeddings_client.chat.completions.create(
                    model="mistralai/mixtral-8x7b-instruct-v0.1",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"""
                            Question: {query.query}
                            Note Content: {note.get('content', '')}
                        """}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                
                answer = response.choices[0].message.content
                if "NO_ANSWER_PRESENT" not in answer:
                    research_note_found = True
                    return {
                        "status": "success",
                        "matches": [{
                            "note_id": note.get('note_id'),
                            "query": note.get('query'),
                            "timestamp": note.get('timestamp'),
                            "content": answer,
                            "image_paths": note.get('image_paths', []),
                            "match_type": "exact",
                            "source": "research_note"
                        }],
                        "match_type": "exact",
                        "source": "research_note",
                        "total_matches": 1
                    }

        # If no matches in research notes, search document content
        if not research_note_found:
            logger.info("No matches in research notes, searching document content...")
            
            # Search document embeddings
            doc_results = text_processor.search_similar(
                query.query,
                top_k=5,
                filter_condition={"pdf_id": folder_name}
            )
            
            if doc_results:
                # Format chunks for LLM
                chunks_text = "\n\n".join([
                    f"Content from Page {chunk.get('page_num', 'N/A')}:\n{chunk['content']}"
                    for chunk in doc_results
                ])
                
                # Generate comprehensive answer
                system_prompt = """
                Create a comprehensive answer using the provided document content.
                Format your response in markdown and include:
                1. A clear, direct answer to the question
                2. Supporting evidence from the text with page references
                3. Any relevant key points or insights
                
                Use headers and bullet points for clarity when appropriate.
                If no relevant answer can be found, respond with 'NO_RELEVANT_INFORMATION'
                """
                
                response = text_processor.embeddings_client.chat.completions.create(
                    model="mistralai/mixtral-8x7b-instruct-v0.1",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Question: {query.query}\n\nDocument Content:\n{chunks_text}"}
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )
                
                answer = response.choices[0].message.content
                if "NO_RELEVANT_INFORMATION" not in answer:
                    # Collect images from relevant chunks
                    image_paths = [chunk['image_path'] for chunk in doc_results if chunk.get('image_path')]
                    
                    return {
                        "status": "success",
                        "matches": [{
                            "content": answer,
                            "image_paths": image_paths,
                            "match_type": "document",
                            "source": "document",
                            "query": query.query
                        }],
                        "match_type": "document",
                        "source": "document",
                        "total_matches": 1,
                        "search_path": ["research_notes", "document"]
                    }
        
        # No relevant information found in either source
        return {
            "status": "success",
            "matches": [],
            "match_type": "none",
            "total_matches": 0,
            "search_path": ["research_notes", "document"]
        }
        
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
########################################################################################

@app.get("/folders/list", response_model=List[Dict[str, str]])
async def list_folders():
    """List all folders in the S3 bucket"""
    try:
        s3_client = get_s3_client()
        
        # List objects with delimiter to get "folders"
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Delimiter='/'
        )
        
        folders = []
        
        # Process common prefixes (folders)
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                # Remove trailing slash and get folder name
                folder_name = prefix['Prefix'].rstrip('/')
                folders.append({
                    "title": folder_name,
                    "id": folder_name
                })
        
        return folders
        
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing S3: {str(e)}"
        )