import os
import time
import logging
import json
import sys
from datetime import datetime, timedelta
from io import BytesIO

import boto3
import requests
import fitz  # PyMuPDF
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException
import subprocess

# Import environment variables
from env_var import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME
)

# Set up logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('airflow_scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set environment variables
os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
os.environ['AWS_REGION'] = AWS_REGION
os.environ['AWS_BUCKET_NAME'] = AWS_BUCKET_NAME

class ScrapingStats:
    def __init__(self):
        self.successful_uploads = 0
        self.failed_uploads = 0
        self.successful_folders = set()
        self.failed_folders = set()

scraping_stats = ScrapingStats()

def setup_s3_client():
    """Sets up AWS S3 client."""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        bucket_name = AWS_BUCKET_NAME
        logger.info("Successfully connected to AWS S3")
        return s3, bucket_name
    except Exception as e:
        logger.error(f"Error setting up S3 client: {e}")
        raise AirflowException(f"Error setting up S3 client: {e}")

def setup_webdriver():
    """Sets up Chrome webdriver with appropriate options."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.page_load_strategy = 'eager'
        chrome_options.binary_location = "/usr/bin/chromium"
        
        # Add additional options to handle timeouts better
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        
        service = Service(
            executable_path="/usr/bin/chromedriver",
            log_path="/opt/airflow/logs/chromedriver.log"
        )
        
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        
        logger.info("Successfully initialized Chrome WebDriver")
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
        raise AirflowException(f"Failed to initialize Chrome WebDriver: {str(e)}")

def upload_to_s3(s3, bucket, key_name, content, content_type):
    """Upload content to S3 with error handling and retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            s3.put_object(Bucket=bucket, Key=key_name, Body=content, ContentType=content_type)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to upload {key_name} after {max_retries} attempts: {e}")
                return False
            time.sleep(2 ** attempt)
    return False

def clean_filename(title):
    """Creates a safe filename from title."""
    return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

def extract_pdf_first_page_as_image(pdf_content):
    """Extract first page of PDF as image."""
    try:
        pdf_stream = BytesIO(pdf_content)
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        
        if pdf_document.page_count == 0:
            raise ValueError("PDF document has no pages")
            
        first_page = pdf_document[0]
        pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = BytesIO(pix.tobytes())
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error extracting PDF first page: {e}")
        return None

def extract_all_text(driver):
    """Extract all text content from the page."""
    text_content = []
    
    try:
        # Get text from article paragraphs
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for p in paragraphs:
            try:
                text = p.text.strip()
                if text:
                    text_content.append(text)
            except:
                continue
                
        # Get text from specific article sections
        sections = driver.find_elements(By.CLASS_NAME, "article__paragraph")
        for section in sections:
            try:
                text = section.text.strip()
                if text:
                    text_content.append(text)
            except:
                continue
                
        # Get text from overview section
        try:
            overview = driver.find_element(By.CLASS_NAME, "overview__content")
            if overview:
                text_content.append(overview.text.strip())
        except:
            pass

        # Get text from spotlight hero section
        try:
            hero_text = driver.find_element(By.CLASS_NAME, "spotlight-hero__text")
            if hero_text:
                text_content.append(hero_text.text.strip())
        except:
            pass

        # Get text from content-asset section
        try:
            content_asset = driver.find_element(By.CLASS_NAME, "content-asset__title")
            if content_asset:
                text_content.append(content_asset.text.strip())
        except:
            pass

    except Exception as e:
        logger.warning(f"Error extracting text content: {e}")
    
    # Remove duplicates while maintaining order
    seen = set()
    unique_content = []
    for text in text_content:
        if text not in seen:
            seen.add(text)
            unique_content.append(text)
    
    return "\n\n".join(unique_content)

def extract_image_url(driver):
    """Extract image URL with priority order."""
    try:
        # First priority: book cover image from article element
        cover_image = driver.find_element(By.CSS_SELECTOR, ".book__cover-image img, .article-cover")
        if cover_image:
            src = cover_image.get_attribute('src')
            if src:
                logger.info("Found image in book cover section")
                return src
    except:
        pass

    try:
        # Second priority: spotlight hero image
        hero_image = driver.find_element(By.CSS_SELECTOR, ".spotlight-hero__image img")
        if hero_image:
            srcset = hero_image.get_attribute('srcset')
            if srcset:
                sources = srcset.split(',')
                if sources:
                    highest_res = sources[-1].strip().split(' ')[0]
                    return highest_res
            return hero_image.get_attribute('src')
    except:
        pass

    return None

@task
def setup_s3_and_driver():
    """Task to set up S3 client and webdriver."""
    try:
        # Initialize both resources
        s3, bucket = setup_s3_client()
        
        # Return only serializable configuration
        return {
            "bucket_name": bucket,
            "initialized": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise AirflowException(f"Setup failed: {e}")

@task
def scrape_publication_links(setup_info):
    """Scrapes links to individual publications."""
    driver = setup_webdriver()
    try:
        main_url = 'https://rpc.cfainstitute.org/en/research-foundation/publications'
        page = 1
        processed_urls = set()
        max_pages = 10
        publications = []

        while page <= max_pages:
            try:
                logger.info(f"Scraping page {page}/{max_pages}")
                url = f"{main_url}#first={10 * (page - 1)}&sort=%40officialz32xdate%20descending"
                
                driver.get(url)
                time.sleep(5)  # Wait for dynamic content
                
                # Wait for content to load
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CoveoSearchInterface")))
                time.sleep(5)
                
                # Find all publication links
                elements = driver.find_elements(By.TAG_NAME, "a")
                for element in elements:
                    href = element.get_attribute('href')
                    if href and '/research/foundation/' in href and not any(x in href for x in ['/donate', '/rf-review-board']):
                        if href not in processed_urls:
                            publications.append(href)
                            processed_urls.add(href)

                if not publications:
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error processing page {page}: {e}")
                time.sleep(5)
                continue

        logger.info(f"Successfully scraped {len(publications)} publication links")
        return {"links": publications}
    finally:
        driver.quit()

@task
def process_publications(scrape_result, setup_info):
    """Downloads and processes publication content."""
    driver = setup_webdriver()
    s3, bucket = setup_s3_client()
    processed_data = []
    
    try:
        for link in scrape_result["links"]:
            try:
                driver.get(link)
                time.sleep(2)
                
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                
                # Extract title
                try:
                    title_element = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "spotlight-hero__title"))
                    )
                    title = title_element.text.strip() if title_element else None
                except:
                    title_element = driver.find_element(By.TAG_NAME, "h1")
                    title = title_element.text.strip() if title_element else None

                if not title:
                    logger.error(f"No title found for {link}")
                    continue

                safe_title = clean_filename(title)
                folder_success = True

                metadata = {
                    'title': title,
                    'url': link,
                    'timestamp': datetime.utcnow().isoformat(),
                    'has_image': False,
                    'has_pdf': False,
                    'has_full_text': False,
                    'has_summary': False
                }

                # Process PDF and extract first page as image
                try:
                    pdf_link = driver.find_element(By.CSS_SELECTOR, ".content-asset.content-asset--primary")
                    if pdf_link:
                        pdf_url = pdf_link.get_attribute('href')
                        if pdf_url and '.pdf' in pdf_url:
                            if pdf_url.startswith('/-/media'):
                                pdf_url = f"https://rpc.cfainstitute.org{pdf_url}"
                                
                            pdf_response = requests.get(pdf_url, timeout=60)
                            if pdf_response.status_code == 200:
                                # Extract and upload image from PDF
                                image_content = extract_pdf_first_page_as_image(pdf_response.content)
                                if image_content:
                                    if upload_to_s3(s3, bucket, f"{safe_title}/image.jpg", 
                                                  image_content, 'image/jpeg'):
                                        metadata['has_image'] = True
                                        metadata['image_source'] = 'pdf_first_page'
                                        logger.info(f"Uploaded PDF first page as image for: {safe_title}")
                                
                                # Upload PDF
                                if upload_to_s3(s3, bucket, f"{safe_title}/document.pdf", 
                                              pdf_response.content, 'application/pdf'):
                                    metadata['has_pdf'] = True
                                else:
                                    folder_success = False
                except Exception as e:
                    logger.warning(f"Failed to process PDF for {safe_title}: {e}")
                    folder_success = False

                # Process text content
                full_text = extract_all_text(driver)
                if full_text:
                    if upload_to_s3(s3, bucket, f"{safe_title}/full_text.txt", 
                                  full_text.encode('utf-8'), 'text/plain'):
                        metadata['has_full_text'] = True
                    else:
                        folder_success = False
                        
                    summary = full_text[:1000] + "..." if len(full_text) > 1000 else full_text
                    if upload_to_s3(s3, bucket, f"{safe_title}/summary.txt", 
                                  summary.encode('utf-8'), 'text/plain'):
                        metadata['has_summary'] = True
                    else:
                        folder_success = False

                # Upload metadata
                if upload_to_s3(s3, bucket, f"{safe_title}/metadata.json", 
                              json.dumps(metadata, indent=2).encode('utf-8'), 'application/json'):
                    processed_data.append({
                        'url': link,
                        'data': metadata,
                        'status': 'success' if folder_success else 'partial_success'
                    })
                # Upload metadata
                if upload_to_s3(s3, bucket, f"{safe_title}/metadata.json", 
                              json.dumps(metadata, indent=2).encode('utf-8'), 'application/json'):
                    if folder_success:
                        scraping_stats.successful_folders.add(safe_title)
                        logger.info(f"Successfully processed: {safe_title}")
                    else:
                        scraping_stats.failed_folders.add(safe_title)
                        logger.error(f"Partially failed to process: {safe_title}")
                        
                    processed_data.append({
                        'url': link,
                        'data': metadata,
                        'status': 'success' if folder_success else 'partial_success'
                    })
                
            except Exception as e:
                logger.error(f"Failed to process {link}: {e}")
                processed_data.append({
                    'url': link,
                    'status': 'failed',
                    'error': str(e)
                })
                scraping_stats.failed_folders.add(link)
    
    finally:
        driver.quit()
    
    # Create summary of processing
    summary = {
        'processed_data': processed_data,
        'stats': {
            'total_publications': len(scrape_result["links"]),
            'successful_folders': len(scraping_stats.successful_folders),
            'failed_folders': len(scraping_stats.failed_folders),
            'successful_folders_list': list(scraping_stats.successful_folders),
            'failed_folders_list': list(scraping_stats.failed_folders)
        }
    }
    
    logger.info(f"Processing complete. Successful: {len(scraping_stats.successful_folders)}, Failed: {len(scraping_stats.failed_folders)}")
    return summary

@task
def upload_processed_data(process_result, setup_info):
    """Creates and uploads final report."""
    s3, bucket = setup_s3_client()
    
    # Create final report
    report = {
        'timestamp': datetime.utcnow().isoformat(),
        'total_publications': process_result['stats']['total_publications'],
        'successful_uploads': process_result['stats']['successful_folders'],
        'failed_uploads': process_result['stats']['failed_folders'],
        'successful_folders': process_result['stats']['successful_folders_list'],
        'failed_folders': process_result['stats']['failed_folders_list'],
        'details': process_result['processed_data']
    }
    
    # Upload report
    report_key = f"reports/scraping_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    if upload_to_s3(s3, bucket, report_key,
                   json.dumps(report, indent=2).encode('utf-8'),
                   'application/json'):
        logger.info(f"Successfully uploaded final report: {report_key}")
        logger.info(f"Total publications processed: {report['total_publications']}")
        logger.info(f"Successful uploads: {report['successful_uploads']}")
        logger.info(f"Failed uploads: {report['failed_uploads']}")
    else:
        logger.error("Failed to upload final report")
    
    return report

# DAG definition
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'execution_timeout': timedelta(hours=2)
}

with DAG(
    dag_id='aws_ingestion_pipeline',
    default_args=default_args,
    description='Web scraping and PDF processing pipeline',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['scraping', 'pdf', 'upload']
) as dag:
    
    # Define tasks
    setup_task = setup_s3_and_driver()
    scrape_task = scrape_publication_links(setup_task)
    process_task = process_publications(scrape_task, setup_task)
    upload_task = upload_processed_data(process_task, setup_task)
    
    # Set dependencies
    setup_task >> scrape_task >> process_task >> upload_task