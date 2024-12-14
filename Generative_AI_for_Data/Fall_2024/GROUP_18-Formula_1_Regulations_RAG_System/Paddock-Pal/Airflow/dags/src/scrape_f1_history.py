import requests
from bs4 import BeautifulSoup
import boto3
import os
from dotenv import load_dotenv
from urllib.parse import urljoin

# Load environment variables
load_dotenv()

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = "f1wikipedia"
S3_FOLDER_NAME = "History"

# S3 client setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Wikipedia URL for the history of F1
WIKI_URL = "https://en.wikipedia.org/wiki/History_of_Formula_One"

# Step 1: Scrape the History Content from Wikipedia
def scrape_f1_history():
    response = requests.get(WIKI_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve Wikipedia page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    
    if content_div is None:
        raise Exception("Failed to find the content on the Wikipedia page.")
    
    # Extract text content from the div
    paragraphs = content_div.find_all('p')
    history_text = ""
    for para in paragraphs:
        history_text += para.get_text() + "\n"
    
    return history_text, soup

# Step 2: Scrape Images from the Wikipedia Page
def scrape_images(soup):
    images = []
    content_div = soup.find('div', {'class': 'mw-parser-output'})

    # Find all images inside the content div
    image_tags = content_div.find_all('img')
    base_url = "https://en.wikipedia.org"
    
    for img in image_tags:
        # Construct full image URL
        img_url = urljoin(base_url, img.get('src'))
        
        # Avoid icons or irrelevant images
        if 'thumb' in img_url or 'upload.wikimedia.org' in img_url:
            images.append(img_url)
    
    return images

# Step 3: Upload Text and Images to Amazon S3
def upload_to_s3(content, images, bucket_name, folder_name, text_file_name):
    try:
        # Upload text content
        text_s3_key = f"{folder_name}/{text_file_name}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=text_s3_key,
            Body=content.encode('utf-8'),
            ContentType='text/plain'
        )
        print(f"Successfully uploaded text to S3 at: s3://{bucket_name}/{text_s3_key}")

        # Upload images
        for img_url in images:
            img_response = requests.get(img_url, stream=True)
            if img_response.status_code == 200:
                img_name = img_url.split("/")[-1]
                img_s3_key = f"{folder_name}/images/{img_name}"
                
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=img_s3_key,
                    Body=img_response.content,
                    ContentType='image/jpeg'  # Assuming images are JPEG (could also be PNG)
                )
                print(f"Successfully uploaded image to S3 at: s3://{bucket_name}/{img_s3_key}")
    
    except Exception as e:
        print(f"Error uploading files to S3: {e}")
        raise

# Main function
if __name__ == "__main__":
    try:
        # Step 1: Scrape the Wikipedia content and images
        f1_history_text, soup = scrape_f1_history()
        print("Successfully scraped the history of F1 from Wikipedia.")
        
        # Step 2: Scrape images
        images = scrape_images(soup)
        print(f"Successfully scraped {len(images)} images from Wikipedia.")

        # Step 3: Upload text and images to Amazon S3
        upload_to_s3(f1_history_text, images, S3_BUCKET_NAME, S3_FOLDER_NAME, "f1_history.txt")

    except Exception as e:
        print(f"Error during scraping or uploading: {e}")
