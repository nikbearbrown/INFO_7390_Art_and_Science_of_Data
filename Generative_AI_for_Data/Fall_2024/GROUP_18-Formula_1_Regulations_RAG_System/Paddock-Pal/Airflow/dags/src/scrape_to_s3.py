import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import boto3
from urllib.parse import urljoin
from io import BytesIO

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/aniketpatole/Documents/GitHub/New/Projects/BigData/Final-Project/.env')

AWS_ACCESS_KEY_ID_RAG = os.getenv('AWS_ACCESS_KEY_ID_RAG')
AWS_SECRET_ACCESS_KEY_RAG = os.getenv('AWS_SECRET_ACCESS_KEY_RAG')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
URL = os.getenv('url')  # The base URL to scrape

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID_RAG,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY_RAG
)

def upload_to_s3(file_name, file_content):
    s3_client.upload_fileobj(file_content, AWS_BUCKET_NAME, file_name)

def download_and_upload_pdf(pdf_url, category):
    print(f"Downloading PDF from {pdf_url}")  # Debug print
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_name = pdf_url.split("/")[-1]
        upload_to_s3(f"{category}/{pdf_name}", BytesIO(response.content))
        print(f"Uploaded {pdf_name} to category {category} in S3.")
    else:
        print(f"Failed to download {pdf_url}, status code: {response.status_code}")

def scrape_documents(URL):
    # Sending GET request to fetch the page content
    response = requests.get(URL)
    print(f"Fetched page with status code {response.status_code}")  # Debug print

    # Check if the page request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the document links inside the 'list-item' divs
        document_elements = soup.select(".list-item a")
        print(f"Found {len(document_elements)} document(s)")  # Debug print

        for document in document_elements:
            title = document.get_text().strip()
            pdf_url = document.get('href')

            # Construct the full URL (if the link is relative)
            full_pdf_url = urljoin(URL, pdf_url)
            print(f"Full PDF URL: {full_pdf_url}")  # Debug print

            # Categorize the document based on its title
            if "Sporting" in title:
                category = "sporting"
            elif "Technical" in title:
                category = "technical"
            elif "Financial" in title:
                category = "financial"
            else:
                category = "related_regulations"

            # Download and upload the PDF to S3
            download_and_upload_pdf(full_pdf_url, category)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    print("Starting document processing...")
    scrape_documents(URL)
