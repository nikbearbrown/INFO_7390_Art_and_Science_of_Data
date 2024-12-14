import boto3
import requests
import time
import os
import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
import re

# Set up logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

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
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ["AWS_REGION"]
        )
        bucket_name = os.environ["AWS_BUCKET_NAME"]
        logging.info("Successfully connected to AWS S3")
        return s3, bucket_name
    except Exception as e:
        logging.error(f"Error setting up S3 client: {e}")
        raise

def setup_webdriver():
    """Sets up Chrome webdriver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.page_load_strategy = 'eager'
    
    # Add additional options to handle timeouts better
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver

def upload_to_s3(s3, bucket, key_name, content, content_type):
    """Upload content to S3 with error handling and retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            s3.put_object(Bucket=bucket, Key=key_name, Body=content, ContentType=content_type)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                logging.error(f"Failed to upload {key_name} after {max_retries} attempts: {e}")
                return False
            time.sleep(2 ** attempt)
    return False

def clean_filename(title):
    """Create a safe filename from title."""
    return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

def extract_pdf_first_page_as_image(pdf_content):
    """Extract first page of PDF as image."""
    try:
        # Load PDF from memory
        pdf_stream = BytesIO(pdf_content)
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        
        # Get first page
        first_page = pdf_document[0]
        
        # Convert to image with higher resolution
        pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        # Convert to PIL Image
        img_data = BytesIO(pix.tobytes())
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Convert to JPEG format
        output = BytesIO()
        image.save(output, format='JPEG', quality=85)
        return output.getvalue()
        
    except Exception as e:
        logging.warning(f"Failed to extract PDF first page as image: {e}")
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
        logging.warning(f"Error extracting text content: {e}")
    
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
                logging.info("Found image in book cover section")
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

def scrape_publication_page(driver, publication_url, s3, bucket):
    """Scrapes the publication page using Selenium for dynamic content."""
    max_retries = 3
    current_retry = 0
    folder_success = True
    
    while current_retry < max_retries:
        try:
            driver.set_page_load_timeout(60)
            
            try:
                driver.get(publication_url)
                time.sleep(2)
            except Exception as e:
                driver.refresh()
                time.sleep(5)
            
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
                scraping_stats.failed_folders.add(publication_url)
                return

            safe_title = clean_filename(title)

            metadata = {
                'title': title,
                'url': publication_url,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'has_image': False,
                'has_summary': False,
                'has_pdf': False,
                'has_full_text': False
            }

            # First try to get PDF and extract first page as image
            try:
                pdf_link = driver.find_element(By.CSS_SELECTOR, ".content-asset.content-asset--primary")
                if pdf_link:
                    pdf_url = pdf_link.get_attribute('href')
                    if pdf_url and '.pdf' in pdf_url:
                        if pdf_url.startswith('/-/media'):
                            pdf_url = f"https://rpc.cfainstitute.org{pdf_url}"
                            
                        pdf_response = requests.get(pdf_url, timeout=60)
                        if pdf_response.status_code == 200:
                            # Extract and upload PDF first page as image
                            image_content = extract_pdf_first_page_as_image(pdf_response.content)
                            if image_content:
                                if upload_to_s3(s3, bucket, f"{safe_title}/image.jpg", 
                                              image_content, 'image/jpeg'):
                                    metadata['has_image'] = True
                                    metadata['image_source'] = 'pdf_first_page'
                                    logging.info(f"Uploaded PDF first page as image for: {safe_title}")
                            
                            # Upload PDF
                            if upload_to_s3(s3, bucket, f"{safe_title}/document.pdf", 
                                          pdf_response.content, 'application/pdf'):
                                metadata['has_pdf'] = True
                            else:
                                folder_success = False
            except Exception as e:
                logging.warning(f"Failed to process PDF for {safe_title}: {e}")
                folder_success = False

            # Extract and upload text content
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
            if not upload_to_s3(s3, bucket, f"{safe_title}/metadata.json", 
                              json.dumps(metadata, indent=2).encode('utf-8'), 'application/json'):
                folder_success = False

            if folder_success:
                logging.info(f"Successfully processed: {safe_title}")
                scraping_stats.successful_folders.add(safe_title)
            else:
                logging.error(f"Failed to process some files for: {safe_title}")
                scraping_stats.failed_folders.add(safe_title)
            
            return
            
        except Exception as e:
            current_retry += 1
            if current_retry == max_retries:
                scraping_stats.failed_folders.add(publication_url)
                return
            time.sleep(5 * current_retry)

def scrape_main_page(main_url, s3, bucket):
    """Scrapes the main publications page using Selenium."""
    driver = setup_webdriver()
    try:
        page = 1
        processed_urls = set()
        max_pages = 10

        while page <= max_pages:
            try:
                logging.info(f"Scraping page {page}/{max_pages}")
                
                url = f"{main_url}#first={10 * (page - 1)}&sort=%40officialz32xdate%20descending"
                
                driver.get(url)
                time.sleep(5)

                publications = []
                # Wait for content to load
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CoveoSearchInterface")))
                time.sleep(5)
                
                # Find all publication links
                elements = driver.find_elements(By.TAG_NAME, "a")
                for element in elements:
                    href = element.get_attribute('href')
                    if href and '/research/foundation/' in href and not any(x in href for x in ['/donate', '/rf-review-board']):
                        publications.append(href)

                new_publications = [pub_url for pub_url in publications if pub_url not in processed_urls]

                if not new_publications:
                    break

                for pub_url in new_publications:
                    scrape_publication_page(driver, pub_url, s3, bucket)
                    processed_urls.add(pub_url)
                    time.sleep(2)

                page += 1

            except Exception as e:
                logging.error(f"Error processing page {page}: {e}")
                time.sleep(5)

    finally:
        driver.quit()
        
    logging.info(f"\nScraping Summary:")
    logging.info(f"Total folders successfully uploaded: {len(scraping_stats.successful_folders)}")
    logging.info(f"Total folders failed to upload: {len(scraping_stats.failed_folders)}")
    if scraping_stats.failed_folders:
        logging.info("Failed folders:")
        for folder in scraping_stats.failed_folders:
            logging.info(f"- {folder}")

def main():
    load_dotenv()
    s3, bucket = setup_s3_client()
    
    main_url = 'https://rpc.cfainstitute.org/en/research-foundation/publications'
    logging.info(f"Starting scrape of {main_url}")

    
    # Start scraping
    scrape_main_page(main_url, s3, bucket)
        
    # Print completion message
    logging.info("\nScraping process completed successfully!")

if __name__ == "__main__":
    main()