from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import logging
import os
import boto3
import asyncio
import time
import csv  
import requests
from urllib.parse import urlparse
from io import StringIO
import snowflake.connector
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
DATA_DIR = "/tmp/triphobo_data"
os.makedirs(DATA_DIR, exist_ok=True)

RAW_TOURS_PATH = f"{DATA_DIR}/triphobo_multi_city_tours.csv"
CLEAN_TOURS_PATH = f"{DATA_DIR}/cleaned_tours.csv"
GEOCODED_TOURS_PATH = f"{DATA_DIR}/tours_with_coords.csv"

# AWS + S3
S3_BUCKET = os.getenv("S3_BUCKET", "bigdatafinal2025")
RAW_TOURS_S3_KEY = "raw/triphobo_multi_city_tours.csv"
CLEAN_TOURS_S3_KEY = "clean/cleaned_tours.csv"
GEOCODED_TOURS_S3_KEY = "clean/tours_with_coords.csv"

# Snowflake table
SNOWFLAKE_TOURS_TABLE = "FINAL_PROJECT.SCRAPING.TRIPHOBO_TOURS"
SNOWFLAKE_CREDENTIALS = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")
}
S3_STAGE = os.getenv("SNOWFLAKE_STAGE", "Data")

# City data for geocoding
CITY_CENTERS = {
    'new york city': 'New York City, NY, USA',
    'chicago': 'Chicago, IL, USA',
    'san francisco': 'San Francisco, CA, USA',
    'seattle': 'Seattle, WA, USA',
    'las vegas': 'Las Vegas, NV, USA',
    'los angeles': 'Los Angeles, CA, USA'
}

# Verify environment variables
def verify_env_vars():
    required_vars = {
        "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
        "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY"),
        "AWS_REGION": os.getenv("AWS_REGION"),
        "S3_BUCKET": os.getenv("S3_BUCKET"),
        "SNOWFLAKE_USER": os.getenv("SNOWFLAKE_USER"),
        "SNOWFLAKE_PASSWORD": os.getenv("SNOWFLAKE_PASSWORD"),
        "SNOWFLAKE_ACCOUNT": os.getenv("SNOWFLAKE_ACCOUNT"),
        "SNOWFLAKE_WAREHOUSE": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "SNOWFLAKE_DATABASE": os.getenv("SNOWFLAKE_DATABASE"),
        "SNOWFLAKE_SCHEMA": os.getenv("SNOWFLAKE_SCHEMA"),
        "SNOWFLAKE_STAGE": os.getenv("SNOWFLAKE_STAGE"),
        "SNOWFLAKE_ROLE": os.getenv("SNOWFLAKE_ROLE"),
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY")
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logger.info("All required environment variables are set")
    return True

# ====== S3 FUNCTIONS ======

def download_from_s3(bucket, s3_key, local_file_path):
    """Download a file from S3 to a local path"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    
    try:
        s3.download_file(bucket, s3_key, local_file_path)
        logging.info(f"Downloaded s3://{bucket}/{s3_key} to {local_file_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to download from s3://{bucket}/{s3_key}: {e}")
        raise

def upload_to_s3(file_path, bucket, s3_key, aws_access_key, aws_secret_key):
    """Upload a local file to S3"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=os.getenv("AWS_REGION")
    )
    
    try:
        s3.upload_file(file_path, bucket, s3_key)
        logging.info(f"Uploaded {file_path} to s3://{bucket}/{s3_key}")
    except Exception as e:
        logging.error(f"Failed to upload {file_path} to s3://{bucket}/{s3_key}: {e}")
        raise

# ====== SCRAPING FUNCTIONS ======

BASE_URL = "https://www.triphobo.com"
CITY_URLS = [
    "https://www.triphobo.com/tours/new-york-city-united-states",
    "https://www.triphobo.com/tours/san-francisco-united-states",
    "https://www.triphobo.com/tours/chicago-united-states",
    "https://www.triphobo.com/tours/las-vegas-united-states",
    "https://www.triphobo.com/tours/los-angeles-united-states",
    "https://www.triphobo.com/tours/seattle-united-states"
]

async def extract_tour_links(page, url):
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(3000)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        tour_links = []
        tour_divs = soup.select("div.tour-image > a")
        for tag in tour_divs:
            href = tag.get("href")
            if href:
                full_url = href if href.startswith("http") else BASE_URL + href
                tour_links.append(full_url)
        return tour_links
    except Exception as e:
        logging.error(f"Error extracting tour links from {url}: {e}")
        return []

async def extract_tour_details(page, url, city_name):
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(3000)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        def extract_text(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else "N/A"

        def extract_list(selector):
            return "\n".join([li.get_text(strip=True) for li in soup.select(selector)])

        def extract_reviews():
            review_elements = soup.select("ul#review-box li .review-text-inner p")
            return "\n\n".join([rev.get_text(strip=True) for rev in review_elements])

        def extract_price():
            currency = extract_text("div.cueernt-price span")
            amount = extract_text("div.cueernt-price label")
            return f"{currency} {amount}" if currency != "N/A" and amount != "N/A" else "N/A"

        # Try to extract image URL
        image_url = "N/A"
        try:
            img_tag = soup.select_one(".tour-banner-img img, .tour-image img")
            if img_tag and img_tag.get("src"):
                image_url = img_tag.get("src")
                if not image_url.startswith("http"):
                    image_url = "https:" + image_url if image_url.startswith("//") else BASE_URL + image_url
        except Exception as img_err:
            logging.error(f"Error extracting image from {url}: {img_err}")

        return {
            "City": city_name,
            "URL": url,
            "Title": extract_text("div.sec-head-cont h1"),
            "Rating": extract_text("div.sec-head-cont b.rating-value"),
            "Review Count": extract_text("div.sec-head-cont .rate-revw span:nth-of-type(3)"),
            "Price": extract_price(),
            "Overview": extract_text("#overview"),
            "Know More": extract_text("#details article"),
            "Itinerary": extract_text("#itinerary"),
            "Inclusions": extract_list("#inclusions li"),
            "Exclusions": extract_list("#exclusions li"),
            "Additional Info": extract_text("#additionalInfo"),
            "Key Details": extract_list("div.key-details li"),
            "Reviews": extract_reviews(),
            "Image": image_url
        }
    except Exception as e:
        logging.error(f"Error extracting details from {url}: {e}")
        return {
            "City": city_name,
            "URL": url,
            "Error": str(e),
            "Image": "N/A"
        }

async def main_scrape(output_path):
    # Initialize with existing data if file exists
    all_data = []
    if os.path.exists(output_path):
        try:
            existing_df = pd.read_csv(output_path)
            all_data = existing_df.to_dict('records')
            logging.info(f"Loaded {len(all_data)} existing records from {output_path}")
            
            # Extract already scraped URLs to avoid duplicates
            existing_urls = set(existing_df['URL'].tolist())
            logging.info(f"Found {len(existing_urls)} existing URLs in the dataset")
        except Exception as e:
            logging.error(f"Error loading existing data: {e}")
            existing_urls = set()
    else:
        existing_urls = set()
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        total_new_data = 0
        
        for city_url in CITY_URLS:
            city_name = city_url.split("/")[4].replace("-", " ").title()
            city_data_count = 0
            logging.info(f"Scraping city: {city_name}")

            for page_num in range(1, 11):
                url = f"{city_url}?page={page_num}"
                try:
                    logging.info(f" Visiting Page {page_num}: {url}")
                    tour_links = await extract_tour_links(page, url)
                    logging.info(f" Found {len(tour_links)} tour links on page {page_num}")

                    for idx, link in enumerate(tour_links):
                        # Skip already scraped URLs
                        if link in existing_urls:
                            logging.info(f"Skipping already scraped URL: {link}")
                            continue
                            
                        try:
                            logging.info(f"Scraping {idx + 1}/{len(tour_links)}: {link}")
                            data = await extract_tour_details(page, link, city_name)
                            all_data.append(data)
                            existing_urls.add(link)  # Add to scraped URLs
                            city_data_count += 1
                            total_new_data += 1
                        except Exception as e:
                            logging.error(f"Failed on tour {idx + 1}: {e}")
                            all_data.append({"City": city_name, "URL": link, "Error": str(e)})
                except Exception as e:
                    logging.error(f"Failed to process page {page_num} of {city_name}: {e}")
            
            logging.info(f"Scraped {city_data_count} new tours for {city_name}")

        await browser.close()
        logging.info(f"Total new tours scraped: {total_new_data}")

    # Save all data to CSV
    try:
        df = pd.DataFrame(all_data)
        df.to_csv(output_path, index=False)
        logging.info(f"All data saved to {output_path} with {len(df)} total records")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")

def scrape_tours(output_path):
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        asyncio.run(main_scrape(output_path))
        logging.info(f"Tour scraping completed, data saved to {output_path}")
    except Exception as e:
        logging.error(f"Scraping process failed: {e}")
        raise

# ====== CLEANING FUNCTIONS ======

def clean_tours_csv(s3_bucket, s3_key, output_path):
    """Clean tours CSV from S3 instead of local file"""
    try:
        # Download from S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        
        logging.info(f"Downloading tours data from s3://{s3_bucket}/{s3_key}")
        response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Load into pandas
        df = pd.read_csv(StringIO(csv_content))
        logging.info(f"Downloaded CSV has {len(df)} rows and {len(df.columns)} columns")
        
        # Clean data
        df.replace(["N/A", "", " ", "nan", "NaN"], pd.NA, inplace=True)
        df.drop_duplicates(inplace=True)

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip() if hasattr(df[col], 'str') else df[col]

        df["Reviews"] = df["Reviews"].fillna("No reviews provided")
        df["Short Reviews"] = df["Reviews"].apply(lambda x: x[:300] + "..." if isinstance(x, str) and len(x) > 300 else x)
        df["Rating"] = df["Rating"].fillna("Not Rated")
        df["Price"] = df["Price"].fillna("Unknown")
        df["Title"] = df["Title"].fillna("Unnamed Tour")
        
        # Add Image column if not present
        if "Image" not in df.columns:
            df["Image"] = "N/A"

        df.fillna("Not Provided", inplace=True)

        # Save cleaned data
        df.to_csv(output_path, index=False)
        logging.info(f"Cleaned tour data saved to {output_path}")
        
        return len(df)

    except Exception as e:
        logging.error(f"Error cleaning tours CSV: {e}", exc_info=True)
        raise

# ====== GEOCODING FUNCTIONS ======

def extract_place_from_url(url):
    """Extract place name from URL"""
    try:
        path = urlparse(url).path
        last_part = path.strip('/').split('/')[-1]
        return ' '.join(word.capitalize() for word in last_part.replace('-', ' ').split())
    except Exception as e:
        logging.warning(f"Failed to extract place from URL: {url} - {e}")
        return "Unknown Place"

def extract_city_name(city_string):
    """Extract city name from city string"""
    if not city_string:
        return None
    parts = city_string.lower().split()
    for city in CITY_CENTERS.keys():
        if city.split()[0] in parts:
            return city
    return parts[0]

def geocode_place(place_name, city_name):
    """Geocode a place using Google Maps API"""
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    search_query = f"{place_name}, {CITY_CENTERS.get(city_name, '')}" if city_name in CITY_CENTERS else place_name
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": search_query, "key": API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return {
                'lat': location['lat'],
                'lng': location['lng'],
                'formatted_address': data['results'][0]['formatted_address'],
                'search_query': search_query
            }
        else:
            logging.warning(f"No results for: {search_query}. Status: {data['status']}")
            return {'lat': '', 'lng': '', 'formatted_address': '', 'search_query': search_query}
    except Exception as e:
        logging.error(f"Error geocoding '{search_query}': {e}", exc_info=True)
        return {'lat': '', 'lng': '', 'formatted_address': '', 'search_query': search_query}

def process_csv_in_batches(input_path, output_path, batch_size=100):
    """Process CSV in batches for geocoding"""
    try:
        with open(input_path, 'r', encoding='utf-8') as input_file:
            reader = csv.DictReader(input_file)
            all_rows = list(reader)

        total_rows = len(all_rows)
        logging.info(f"Total tours to process: {total_rows}")

        try:
            # Check if output file exists to resume
            with open(output_path, 'r', encoding='utf-8') as test_file:
                processed_count = sum(1 for _ in csv.DictReader(test_file))
                logging.info(f"Resuming from existing output file with {processed_count} rows")
                start_index = processed_count
                append_mode = True
        except FileNotFoundError:
            start_index = 0
            append_mode = False

        all_fields = list(all_rows[0].keys())
        output_fields = all_fields + ['Latitude', 'Longitude', 'PlaceName', 'FormattedAddress', 'SearchQuery']
        
        mode = 'a' if append_mode else 'w'

        with open(output_path, mode, encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=output_fields)
            if not append_mode:
                writer.writeheader()

            for i in range(start_index, total_rows, batch_size):
                batch_end = min(i + batch_size, total_rows)
                logging.info(f"Processing batch {i // batch_size + 1}: rows {i + 1} to {batch_end}")

                for idx in range(i, batch_end):
                    row = all_rows[idx]
                    place_name = extract_place_from_url(row.get('URL', ''))
                    city_name = extract_city_name(row.get('City', ''))

                    logging.info(f"  ({idx + 1}/{total_rows}) Geocoding: {place_name}")
                    geo_results = geocode_place(place_name, city_name)

                    updated_row = row.copy()
                    updated_row['Latitude'] = geo_results['lat']
                    updated_row['Longitude'] = geo_results['lng']
                    updated_row['PlaceName'] = place_name
                    updated_row['FormattedAddress'] = geo_results.get('formatted_address', '')
                    updated_row['SearchQuery'] = geo_results.get('search_query', '')

                    writer.writerow(updated_row)
                    time.sleep(0.1)  

                logging.info(f"Completed batch {i // batch_size + 1}. Sleeping before next batch...")
                time.sleep(2)  
                output_file.flush()

        logging.info(f"Successfully processed all {total_rows} tours")
        logging.info(f"Output saved to: {output_path}")

    except Exception as e:
        logging.error(f"Error processing CSV: {e}", exc_info=True)
        raise 

def add_coordinates_to_csv(input_path, output_path):
    """Add coordinates to a CSV file"""
    logging.info(f"Processing file from {input_path} to {output_path}")
    process_csv_in_batches(input_path, output_path, batch_size=50)

# ====== SNOWFLAKE LOADING FUNCTIONS ======

def load_tours_from_s3_to_snowflake():
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        response = s3.get_object(Bucket=S3_BUCKET, Key=GEOCODED_TOURS_S3_KEY)
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content), on_bad_lines='skip')
        logger.info(f"Downloaded CSV with {len(df)} rows from s3://{S3_BUCKET}/{GEOCODED_TOURS_S3_KEY}")
        
        # Ensure proper columns exist
        required_columns = ['URL', 'Title', 'Rating', 'Review Count', 'Price', 'Overview', 'Know More', 'Itinerary', 
                           'Inclusions', 'Exclusions', 'Additional Info', 'Key Details', 'Reviews', 'Image', 
                           'City', 'Short Reviews', 'Latitude', 'Longitude', 'PlaceName', 'FormattedAddress']
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = "N/A"
                
        # Create a new dataframe with columns in proper order
        ordered_df = pd.DataFrame()
        for col in required_columns:
            ordered_df[col] = df[col] if col in df.columns else "N/A"

        # Save to temp file
        temp_file = "/tmp/tours_with_coords.csv"
        ordered_df.to_csv(temp_file, index=False)

        conn = snowflake.connector.connect(**SNOWFLAKE_CREDENTIALS)
        cursor = conn.cursor()

        # Create or replace the table
        create_table_sql = f"""
        CREATE OR REPLACE TABLE {SNOWFLAKE_TOURS_TABLE} (
            URL VARCHAR(16777216),
            TITLE VARCHAR(16777216),
            RATING VARCHAR(16777216),
            "Review Count" VARCHAR(16777216),
            PRICE VARCHAR(16777216),
            OVERVIEW VARCHAR(16777216),
            "Know More" VARCHAR(16777216),
            ITINERARY VARCHAR(16777216),
            INCLUSIONS VARCHAR(16777216),
            EXCLUSIONS VARCHAR(16777216),
            "Additional Info" VARCHAR(16777216),
            "Key Details" VARCHAR(16777216),
            REVIEWS VARCHAR(16777216),
            IMAGE VARCHAR(16777216),
            CITY VARCHAR(16777216),
            "Short Reviews" VARCHAR(16777216),
            LATITUDE NUMBER(38,14),
            LONGITUDE NUMBER(38,14),
            PLACENAME VARCHAR(16777216),
            FORMATTEDADDRESS VARCHAR(16777216)
        )
        """
        cursor.execute(create_table_sql)

        logger.info("Uploading file to Snowflake stage...")
        cursor.execute(f"PUT file://{temp_file} @{S3_STAGE} OVERWRITE = TRUE")

        file_name = os.path.basename(temp_file)
        copy_sql = f"""
            COPY INTO {SNOWFLAKE_TOURS_TABLE}
            FROM @{S3_STAGE}/{file_name}
            FILE_FORMAT = (
                TYPE = 'CSV'
                FIELD_OPTIONALLY_ENCLOSED_BY = '"'
                SKIP_HEADER = 1
                COMPRESSION = 'AUTO'
                ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
                EMPTY_FIELD_AS_NULL = TRUE
                REPLACE_INVALID_CHARACTERS = TRUE
            )
            ON_ERROR = 'CONTINUE';
        """

        logger.info("Executing COPY INTO...")
        cursor.execute(copy_sql)

        cursor.execute(f"SELECT COUNT(*) FROM {SNOWFLAKE_TOURS_TABLE}")
        count = cursor.fetchone()[0]
        logger.info(f"Snowflake table row count: {count}")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error uploading to Snowflake: {e}")
        raise

# DAG definition
with DAG(
    dag_id="triphobo_tours_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="30 7 * * *",  # Run at 7:30 AM daily
    catchup=False,
    tags=["triphobo", "tourism", "etl"]
) as dag:
    
    verify_env_vars_task = PythonOperator(
        task_id="verify_env_vars",
        python_callable=verify_env_vars
    )
    
    scrape_tours_task = PythonOperator(
        task_id="scrape_tours",
        python_callable=scrape_tours,
        op_kwargs={"output_path": RAW_TOURS_PATH}
    )

    upload_raw_tours_task = PythonOperator(
        task_id="upload_raw_tours",
        python_callable=upload_to_s3,
        op_kwargs={
            "file_path": RAW_TOURS_PATH,
            "bucket": S3_BUCKET,
            "s3_key": RAW_TOURS_S3_KEY,
            "aws_access_key": os.getenv("AWS_ACCESS_KEY"),
            "aws_secret_key": os.getenv("AWS_SECRET_KEY")
        }
    )
    
    clean_tours_task = PythonOperator(
        task_id="clean_tours",
        python_callable=clean_tours_csv,
        op_kwargs={
            "s3_bucket": S3_BUCKET,
            "s3_key": RAW_TOURS_S3_KEY,
            "output_path": CLEAN_TOURS_PATH
        }
    )

    geocode_tours_task = PythonOperator(
        task_id="geocode_tours",
        python_callable=add_coordinates_to_csv,
        op_kwargs={"input_path": CLEAN_TOURS_PATH, "output_path": GEOCODED_TOURS_PATH}
    )

    upload_geocoded_tours_task = PythonOperator(
        task_id="upload_geocoded_tours",
        python_callable=upload_to_s3,
        op_kwargs={
            "file_path": GEOCODED_TOURS_PATH,
            "bucket": S3_BUCKET,
            "s3_key": GEOCODED_TOURS_S3_KEY,
            "aws_access_key": os.getenv("AWS_ACCESS_KEY"),
            "aws_secret_key": os.getenv("AWS_SECRET_KEY")
        }
    )

    load_tours_snowflake_task = PythonOperator(
        task_id="load_tours_snowflake",
        python_callable=load_tours_from_s3_to_snowflake
    )

    # DAG dependencies
    verify_env_vars_task >> scrape_tours_task >> upload_raw_tours_task >> clean_tours_task >> geocode_tours_task >> upload_geocoded_tours_task >> load_tours_snowflake_task
   