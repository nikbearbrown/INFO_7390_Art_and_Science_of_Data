import requests
from bs4 import BeautifulSoup
import boto3
import os
from dotenv import load_dotenv
from io import BytesIO
import time
import logging
from botocore.exceptions import ClientError
from requests.exceptions import RequestException, Timeout
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = "f1wikipedia"
S3_FOLDER_NAME = "Drivers"

# S3 client setup
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
except ClientError as e:
    logger.error(f"Error initializing S3 client: {e}")
    exit(1)

# List of F1 drivers and their Wikipedia URLs
drivers = {
    "Max Verstappen": "https://en.wikipedia.org/wiki/Max_Verstappen",
    "Lewis Hamilton": "https://en.wikipedia.org/wiki/Lewis_Hamilton",
    "Michael Schumacher": "https://en.wikipedia.org/wiki/Michael_Schumacher",
    "Ayrton Senna": "https://en.wikipedia.org/wiki/Ayrton_Senna",
    "Alain Prost": "https://en.wikipedia.org/wiki/Alain_Prost",
    "Sebastian Vettel": "https://en.wikipedia.org/wiki/Sebastian_Vettel",
    "Niki Lauda": "https://en.wikipedia.org/wiki/Niki_Lauda",
    "Jackie Stewart": "https://en.wikipedia.org/wiki/Jackie_Stewart",
    "Jim Clark": "https://en.wikipedia.org/wiki/Jim_Clark",
    "Fernando Alonso": "https://en.wikipedia.org/wiki/Fernando_Alonso",
    "Juan Manuel Fangio": "https://en.wikipedia.org/wiki/Juan_Manuel_Fangio",
    "Nigel Mansell": "https://en.wikipedia.org/wiki/Nigel_Mansell",
    "Stirling Moss": "https://en.wikipedia.org/wiki/Stirling_Moss",
    "Kimi Räikkönen": "https://en.wikipedia.org/wiki/Kimi_Räikkönen",
    "Damon Hill": "https://en.wikipedia.org/wiki/Damon_Hill",
    "Jenson Button": "https://en.wikipedia.org/wiki/Jenson_Button",
    "Gilles Villeneuve": "https://en.wikipedia.org/wiki/Gilles_Villeneuve",
    "Mika Häkkinen": "https://en.wikipedia.org/wiki/Mika_Häkkinen",
    "Nico Rosberg": "https://en.wikipedia.org/wiki/Nico_Rosberg",
    "Graham Hill": "https://en.wikipedia.org/wiki/Graham_Hill",
    "Jochen Rindt": "https://en.wikipedia.org/wiki/Jochen_Rindt",
    "James Hunt": "https://en.wikipedia.org/wiki/James_Hunt",
    "Mario Andretti": "https://en.wikipedia.org/wiki/Mario_Andretti",
    "Carlos Sainz Jr.": "https://en.wikipedia.org/wiki/Carlos_Sainz_Jr.",
    "Lando Norris": "https://en.wikipedia.org/wiki/Lando_Norris",
    "Charles Leclerc": "https://en.wikipedia.org/wiki/Charles_Leclerc",
    "Oscar Piastri": "https://en.wikipedia.org/wiki/Oscar_Piastri",
    "George Russell": "https://en.wikipedia.org/wiki/George_Russell_(racing_driver)",
    "Sergio Perez": "https://en.wikipedia.org/wiki/Sergio_Pérez",
    "Lance Stroll": "https://en.wikipedia.org/wiki/Lance_Stroll",
    "Pierre Gasly": "https://en.wikipedia.org/wiki/Pierre_Gasly",
    "Esteban Ocon": "https://en.wikipedia.org/wiki/Esteban_Ocon",
    "Alexander Albon": "https://en.wikipedia.org/wiki/Alexander_Albon",
    "Yuki Tsunoda": "https://en.wikipedia.org/wiki/Yuki_Tsunoda",
    "Valtteri Bottas": "https://en.wikipedia.org/wiki/Valtteri_Bottas",
    "Nico Hulkenberg": "https://en.wikipedia.org/wiki/Nico_Hülkenberg",
    "Daniel Ricciardo": "https://en.wikipedia.org/wiki/Daniel_Ricciardo",
    "Zhou Guanyu": "https://en.wikipedia.org/wiki/Zhou_Guanyu",
    "Kevin Magnussen": "https://en.wikipedia.org/wiki/Kevin_Magnussen",
    "Logan Sargeant": "https://en.wikipedia.org/wiki/Logan_Sargeant",
    "Emerson Fittipaldi": "https://en.wikipedia.org/wiki/Emerson_Fittipaldi",
    "Nelson Piquet": "https://en.wikipedia.org/wiki/Nelson_Piquet",
    "Jacques Villeneuve": "https://en.wikipedia.org/wiki/Jacques_Villeneuve",
    "Jack Brabham": "https://en.wikipedia.org/wiki/Jack_Brabham",
    "John Surtees": "https://en.wikipedia.org/wiki/John_Surtees",
    "Clay Regazzoni": "https://en.wikipedia.org/wiki/Clay_Regazzoni",
    "Rene Arnoux": "https://en.wikipedia.org/wiki/René_Arnoux",
    "Ronnie Peterson": "https://en.wikipedia.org/wiki/Ronnie_Peterson",
    "Jean Alesi": "https://en.wikipedia.org/wiki/Jean_Alesi",
    "Riccardo Patrese": "https://en.wikipedia.org/wiki/Riccardo_Patrese",
    "Carlos Reutemann": "https://en.wikipedia.org/wiki/Carlos_Reutemann"
}

@sleep_and_retry
@limits(calls=1, period=3)  # Increased delay between calls
def rate_limited_request(url, headers):
    return requests.get(url, headers=headers, timeout=15)  # Increased timeout

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', {'class': 'mw-parser-output'})
    if not content:
        return None

    wiki_content = []
    for element in content.find_all(['p', 'h2', 'h3', 'ul', 'table']):
        if element.name in ['h2', 'h3']:
            section_title = element.get_text().strip()
            if any(x in section_title.lower() for x in ["references", "external links", "see also", "notes"]):
                continue
            wiki_content.append(f"\n{'#' * (2 if element.name == 'h2' else 3)} {section_title}\n")
        elif element.name == 'p':
            text = element.get_text().strip()
            if text and len(text) > 20:  # Reduced minimum length for paragraphs
                wiki_content.append(text + "\n")
        elif element.name == 'ul':
            for li in element.find_all('li'):
                wiki_content.append(f"- {li.get_text().strip()}\n")
        elif element.name == 'table':
            # Extract basic table information
            table_text = element.get_text().strip()
            if table_text:
                wiki_content.append(f"Table: {table_text[:100]}...\n")  # Truncate long tables

    content = "\n".join(wiki_content)
    return content if len(content) > 500 else None  # Ensure substantial content

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_wikipedia_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = rate_limited_request(url, headers)
        response.raise_for_status()
        content = extract_content(response.content)
        if not content:
            raise ValueError("No substantial content extracted")
        return content
    except (Timeout, RequestException, ValueError) as e:
        logger.error(f"Error getting content from {url}: {e}")
        raise

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_driver_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = rate_limited_request(url, headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            image = infobox.find('img')
            if image and 'src' in image.attrs:
                return f"https:{image['src']}"
        raise ValueError("No image found")
    except (RequestException, ValueError) as e:
        logger.error(f"Error getting image from {url}: {e}")
        raise

def upload_to_s3(content, filename, content_type='text/plain'):
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{S3_FOLDER_NAME}/{filename}",
            Body=content,
            ContentType=content_type
        )
        logger.info(f"Successfully uploaded {filename} to S3")
    except ClientError as e:
        logger.error(f"S3 upload error for {filename}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error uploading {filename} to S3: {e}")

def process_driver(name, wiki_url):
    logger.info(f"Processing {name}...")
    
    try:
        wiki_content = get_wikipedia_content(wiki_url)
        if wiki_content:
            clean_name = name.lower().replace(' ', '_')
            upload_to_s3(wiki_content.encode('utf-8'), f"{clean_name}/wiki_content.txt")
            
            try:
                image_url = get_driver_image(wiki_url)
                if image_url:
                    image_response = rate_limited_request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    image_response.raise_for_status()
                    image_content = BytesIO(image_response.content)
                    s3_client.upload_fileobj(
                        image_content,
                        S3_BUCKET_NAME,
                        f"{S3_FOLDER_NAME}/{clean_name}/profile.jpg",
                        ExtraArgs={'ContentType': 'image/jpeg'}
                    )
                    logger.info(f"Successfully uploaded image for {name}")
            except Exception as img_error:
                logger.error(f"Error processing image for {name}: {img_error}")
        else:
            logger.warning(f"No substantial content extracted for {name}")
    except Exception as e:
        logger.error(f"Error processing {name}: {e}")

def main():
    for driver_name, wiki_url in drivers.items():
        process_driver(driver_name, wiki_url)
    logger.info("Scraping and uploading completed.")

if __name__ == "__main__":
    main()