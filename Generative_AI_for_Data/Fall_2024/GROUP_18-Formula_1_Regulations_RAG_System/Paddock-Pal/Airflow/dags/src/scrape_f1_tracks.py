import requests
from bs4 import BeautifulSoup
import boto3
import os
from dotenv import load_dotenv
from urllib.parse import urljoin, quote
from io import BytesIO
import time

# Load environment variables
load_dotenv()

# Set up AWS credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = "f1wikipedia"
S3_FOLDER_NAME = "Tracks"

# S3 client setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# List of F1 tracks for the 2024 season
tracks = [
    "Bahrain International Circuit",
    "Jeddah Street Circuit",
    "Albert Park Circuit",
    "Suzuka International Racing Course",
    "Shanghai International Circuit",
    "Miami International Autodrome",
    "Autodromo Enzo e Dino Ferrari",
    "Circuit de Monaco",
    "Circuit Gilles Villeneuve",
    "Circuit de Barcelona-Catalunya",
    "Red Bull Ring",
    "Silverstone Circuit",
    "Hungaroring",
    "Circuit de Spa-Francorchamps",
    "Circuit Zandvoort",
    "Monza Circuit",
    "Baku City Circuit",
    "Marina Bay Street Circuit",
    "Circuit of the Americas",
    "Autódromo Hermanos Rodríguez",
    "Autódromo José Carlos Pace",
    "Las Vegas Strip Circuit",
    "Losail International Circuit",
    "Yas Marina Circuit"
]

def get_wikipedia_url(track_name):
    search_url = f"https://en.wikipedia.org/w/index.php?search={quote(track_name)}&title=Special:Search&profile=advanced&fulltext=1&ns0=1"
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to search Wikipedia for {track_name}, status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    search_result = soup.find('div', class_='mw-search-result-heading')
    if search_result:
        return "https://en.wikipedia.org" + search_result.find('a')['href']
    return None

def scrape_track_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve Wikipedia page at {url}, status code: {response.status_code}")
        return {}, None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    response.encoding = 'utf-8'

    track_info = {}

    # Extract track information from the infobox
    info_box = soup.find('table', class_='infobox')
    if info_box:
        rows = info_box.find_all('tr')
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            if header and data:
                track_info[header.get_text(strip=True)] = data.get_text(strip=True)

    # Extract content from the main body
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    if content_div:
        # Extract all paragraphs
        paragraphs = content_div.find_all('p')
        track_info['Description'] = "\n\n".join([p.get_text() for p in paragraphs if len(p.get_text().strip()) > 0])

        # Extract section headings and their content
        sections = content_div.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol'])
        current_section = "Main"
        for section in sections:
            if section.name in ['h2', 'h3', 'h4']:
                current_section = section.get_text().strip()
                track_info[current_section] = ""
            elif section.name in ['p', 'ul', 'ol']:
                content = section.get_text().strip()
                if content:
                    if current_section in track_info:
                        track_info[current_section] += "\n" + content
                    else:
                        track_info[current_section] = content

    # Extract the main image from the infobox or the page content
    image_url = None
    if info_box:
        img_tag = info_box.find('img')
        if img_tag:
            image_url = urljoin(url, img_tag.get('src'))

    return track_info, image_url

def upload_to_s3(content, filename, content_type='text/plain'):
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{S3_FOLDER_NAME}/{filename}",
            Body=content,
            ContentType=content_type
        )
        print(f"Successfully uploaded {filename} to S3.")
    except Exception as e:
        print(f"Error uploading {filename} to S3: {e}")

def process_track(track_name):
    print(f"Processing {track_name}...")
    wiki_url = get_wikipedia_url(track_name)
    
    if wiki_url:
        track_info, image_url = scrape_track_info(wiki_url)

        # Upload track info to S3
        if track_info:
            formatted_info = "\n\n".join([f"{key}:\n{value}" for key, value in track_info.items()])
            upload_to_s3(formatted_info.encode('utf-8'), f"{track_name.replace(' ', '_')}_info.txt")

        # Upload track image to S3 if available
        if image_url:
            try:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_content = BytesIO(image_response.content)
                    image_filename = f"{track_name.replace(' ', '_')}_image.jpg"
                    s3_client.upload_fileobj(image_content, S3_BUCKET_NAME, f"{S3_FOLDER_NAME}/{image_filename}")
                    print(f"Successfully uploaded image for {track_name} to S3.")
                else:
                    print(f"Failed to retrieve image for {track_name}, status code: {image_response.status_code}")
            except Exception as e:
                print(f"Error uploading image for {track_name}: {e}")
    else:
        print(f"Could not find Wikipedia page for {track_name}")

# Main process
if __name__ == "__main__":
    for track in tracks:
        process_track(track)
        time.sleep(1)  # Adding a delay to prevent getting blocked by Wikipedia

    print("Scraping and uploading completed.")