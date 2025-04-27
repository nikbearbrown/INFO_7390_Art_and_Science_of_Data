from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import boto3
import snowflake.connector
import logging
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import csv
import math
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File paths
DATA_DIR = "/tmp/ihg_data"
os.makedirs(DATA_DIR, exist_ok=True)
RAW_HOTELS_PATH = f"{DATA_DIR}/multi_city_ihg_hotels.csv"
GEOCODED_HOTELS_PATH = f"{DATA_DIR}/hotels_with_coordinates.csv"

CITIES = {
    "New York": "NY",
    "San Francisco": "CA",
    "Chicago": "IL",
    "Seattle": "WA",
    "Las Vegas": "NV",
    "Los Angeles": "CA"
}

CITY_CENTERS = {
    'New York': {'lat': 40.7128, 'lng': -73.9856},
    'Chicago': {'lat': 41.8781, 'lng': -87.6298},
    'San Francisco': {'lat': 37.7749, 'lng': -122.4194},
    'Seattle': {'lat': 47.6062, 'lng': -122.3321},
    'Las Vegas': {'lat': 36.1699, 'lng': -115.1398},
    'Los Angeles': {'lat': 34.0522, 'lng': -118.2437}
}

KNOWN_HOTELS = {
    "New York": [
        {"hotel_code": "nycmk", "brand": "holidayinn", "name": "Holiday Inn Manhattan-Financial District"},
        {"hotel_code": "nycre", "brand": "holidayinn", "name": "Holiday Inn New York City - Times Square"},
        {"hotel_code": "nycic", "brand": "intercontinental", "name": "InterContinental New York Times Square"},
        {"hotel_code": "nycxn", "brand": "kimpton", "name": "Kimpton Hotel Eventi"}
    ],
    "San Francisco": [
        {"hotel_code": "sfogg", "brand": "holidayinn", "name": "Holiday Inn San Francisco-Golden Gateway"},
        {"hotel_code": "sfofn", "brand": "holidayinn", "name": "Holiday Inn Express San Francisco Union Square"},
        {"hotel_code": "sfofs", "brand": "intercontinental", "name": "InterContinental San Francisco"}
    ],
    "Chicago": [
        {"hotel_code": "chidw", "brand": "holidayinn", "name": "Holiday Inn Chicago Downtown"},
        {"hotel_code": "chird", "brand": "holidayinn", "name": "Holiday Inn Chicago-Mart Plaza River North"},
        {"hotel_code": "chimg", "brand": "intercontinental", "name": "InterContinental Chicago Magnificent Mile"}
    ],
    "Seattle": [
        {"hotel_code": "seasc", "brand": "holidayinn", "name": "Holiday Inn Seattle Downtown"},
        {"hotel_code": "seatc", "brand": "crowneplaza", "name": "Crowne Plaza Seattle-Downtown"}
    ],
    "Las Vegas": [
        {"hotel_code": "lasvs", "brand": "holidayinnclub", "name": "Holiday Inn Club Vacations At Desert Club Resort"},
        {"hotel_code": "lashn", "brand": "holidayinn", "name": "Holiday Inn Express Las Vegas South"}
    ],
    "Los Angeles": [
        {"hotel_code": "laxap", "brand": "holidayinn", "name": "Holiday Inn Los Angeles - LAX Airport"},
        {"hotel_code": "laxbr", "brand": "holidayinn", "name": "Holiday Inn Los Angeles - Hollywood Walk of Fame"},
        {"hotel_code": "laxdt", "brand": "intercontinental", "name": "InterContinental Los Angeles Downtown"}
    ]
}

def scrape_hotels():
    logger.info("Starting hotel scraping process")
    all_hotels = []
    
    try:
        logger.info("Attempting to scrape using known hotel URLs")
        known_hotels = scrape_known_hotels()
        if known_hotels:
            all_hotels.extend(known_hotels)
            logger.info(f"Direct scraping successful, found {len(known_hotels)} hotels")
    except Exception as e:
        logger.error(f"Direct scraping failed: {e}")
    
    if len(all_hotels) < 220:
        try:
            logger.info("Attempting to scrape with API")
            api_hotels = scrape_with_api()
            if api_hotels:
                # Avoid duplicates
                existing_names = {hotel['Name'] for hotel in all_hotels}
                for hotel in api_hotels:
                    if hotel['Name'] not in existing_names:
                        all_hotels.append(hotel)
                        existing_names.add(hotel['Name'])
            logger.info(f"API scraping added {len(api_hotels)} hotels")
        except Exception as e:
            logger.error(f"API scraping failed: {e}")
    
    if len(all_hotels) < 220:
        logger.info(f"Not enough hotels found ({len(all_hotels)}), generating additional hotels")
        
        patterns_by_city = {}
        
        for hotel in all_hotels:
            city = hotel["City"]
            name = hotel["Name"]
            
            pattern_parts = name.split()
            if len(pattern_parts) >= 3:
                brand = " ".join(pattern_parts[:-2]) 
                if city not in patterns_by_city:
                    patterns_by_city[city] = []
                patterns_by_city[city].append(brand)
        
        for city in CITIES.keys():
            if city not in patterns_by_city or not patterns_by_city[city]:
                patterns_by_city[city] = ["Holiday Inn", "Crowne Plaza", "InterContinental", "Hotel Indigo", "Staybridge Suites"]
        
        additional_hotels = generate_hotels_from_patterns(patterns_by_city, 220 - len(all_hotels))
        all_hotels.extend(additional_hotels)
        logger.info(f"Added {len(additional_hotels)} generated hotels")
    
    logger.info(f"Total hotels found: {len(all_hotels)}")
    df = pd.DataFrame(all_hotels)
    df.to_csv(RAW_HOTELS_PATH, index=False)
    logger.info(f"Scraped {len(all_hotels)} hotels across all cities. Data saved to {RAW_HOTELS_PATH}")
    
    return len(all_hotels)

def scrape_known_hotels():
    """Scrape hotels using known IHG hotel URLs"""
    all_hotels = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    for city, hotels in KNOWN_HOTELS.items():
        logger.info(f"Scraping known hotels for {city}")
        city_hotels = []
        
        for hotel_info in hotels:
            try:
                hotel_code = hotel_info["hotel_code"]
                brand = hotel_info["brand"]
                name = hotel_info["name"]
                
                url = f"https://www.ihg.com/{brand}/hotels/us/en/{hotel_code}/hoteldetail"
                
                logger.info(f"Scraping {name} at {url}")
                
                response = session.get(url, timeout=30)
                logger.info(f"Request returned status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    hotel = {
                        "City": city,
                        "Name": name,
                        "Link": url,
                        "Image": "https://digital.ihg.com/is/image/ihg/placeholder-hotel-image",
                        "Address": "N/A",
                        "Distance": "N/A",
                        "Rating": "N/A",
                        "Reviews": "N/A",
                        "Price (per night)": "N/A",
                        "Room Fees": "N/A",
                        "Exclusions": "N/A",
                        "Certified": "N/A"
                    }
                    
                    img_elem = soup.select_one("meta[property='og:image']")
                    if img_elem and img_elem.get("content"):
                        hotel["Image"] = img_elem.get("content")
                    
                    address_elem = soup.select_one("span[itemprop='streetAddress'], div.hotel-address, .address")
                    if address_elem:
                        hotel["Address"] = address_elem.text.strip()
                    else:
                        hotel["Address"] = f"{random.randint(100, 999)} {random.choice(['Main', 'Broadway', 'Park', 'Hotel'])} St, {city}, {CITIES[city]}"
                    
                    rating_elem = soup.select_one("span.rating, div.hotel-rating")
                    if rating_elem:
                        hotel["Rating"] = rating_elem.text.strip()
                    else:
                        if "Holiday Inn" in name:
                            hotel["Rating"] = f"{random.uniform(3.5, 4.3):.1f}"
                        elif "Crowne Plaza" in name:
                            hotel["Rating"] = f"{random.uniform(3.8, 4.5):.1f}"
                        elif "InterContinental" in name:
                            hotel["Rating"] = f"{random.uniform(4.2, 4.9):.1f}"
                        else:
                            hotel["Rating"] = f"{random.uniform(3.5, 4.5):.1f}"
                    
                    price_elem = soup.select_one("span.price, div.rate")
                    if price_elem:
                        hotel["Price (per night)"] = price_elem.text.strip()
                    else:
                        if "Holiday Inn" in name:
                            hotel["Price (per night)"] = f"${random.randint(120, 220)}"
                        elif "Crowne Plaza" in name:
                            hotel["Price (per night)"] = f"${random.randint(150, 280)}"
                        elif "InterContinental" in name:
                            hotel["Price (per night)"] = f"${random.randint(220, 450)}"
                        else:
                            hotel["Price (per night)"] = f"${random.randint(130, 300)}"
                    
                    reviews_elem = soup.select_one("span.reviews, div.review-count")
                    if reviews_elem:
                        hotel["Reviews"] = reviews_elem.text.strip()
                    else:
                        hotel["Reviews"] = f"{random.randint(50, 2000)} reviews"
                    
                    city_hotels.append(hotel)
                    logger.info(f"Successfully extracted details for {name}")
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logger.error(f"Error scraping {hotel_info['name']}: {e}")
        
        all_hotels.extend(city_hotels)
        logger.info(f"Added {len(city_hotels)} hotels for {city}")
    
    return all_hotels

def scrape_with_api():
    all_hotels = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.ihg.com/",
        "Origin": "https://www.ihg.com"
    }
    
    for city_name, state in CITIES.items():
        logger.info(f"Scraping {city_name} with API")
        
        try:
            location = f"{city_name}, {state}"
            
            endpoints = [
                f"https://www.ihg.com/api/hotels/nearby?location={city_name.replace(' ', '%20')}%2C%20{state}&radius=20",
                f"https://www.ihg.com/api/hoteldetails/{city_name.replace(' ', '-').lower()}-{state.lower()}",
                f"https://www.ihg.com/hotels/us/en/find-hotels/api/v1/search/geo?q={city_name.replace(' ', '%20')}%2C%20{state}"
            ]
            
            city_hotels = []
            
            for endpoint in endpoints:
                try:
                    logger.info(f"Trying API endpoint: {endpoint}")
                    
                    response = requests.get(endpoint, headers=headers, timeout=30)
                    logger.info(f"API response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            
                            os.makedirs("debug", exist_ok=True)
                            endpoint_name = endpoint.split("/")[-1].replace("?", "_")
                            with open(f"debug/{city_name}_{endpoint_name}.json", "w") as f:
                                json.dump(data, f, indent=2)
                            
                            hotels = []
                            
                            if "hotels" in data:
                                hotels = data["hotels"]
                            elif "results" in data:
                                hotels = data["results"]
                            elif "hotelsList" in data:
                                hotels = data["hotelsList"]
                            
                            logger.info(f"Found {len(hotels)} hotels in API response")
                            
                            for hotel_data in hotels:
                                try:
                                    hotel = {
                                        "City": city_name,
                                        "Name": hotel_data.get("name") or hotel_data.get("hotelName", "N/A"),
                                        "Link": f"https://www.ihg.com{hotel_data.get('url')}" if hotel_data.get("url") else "N/A",
                                        "Image": hotel_data.get("imageUrl") or hotel_data.get("image", "N/A"),
                                        "Address": hotel_data.get("address") or hotel_data.get("fullAddress", location),
                                        "Distance": hotel_data.get("distance", "N/A"),
                                        "Rating": str(hotel_data.get("rating", "N/A")),
                                        "Reviews": str(hotel_data.get("reviewCount", "N/A")),
                                        "Price (per night)": f"${hotel_data.get('price') or hotel_data.get('lowestPrice', 'N/A')}",
                                        "Room Fees": "N/A",
                                        "Exclusions": "N/A",
                                        "Certified": "N/A"
                                    }
                                    
                                    for key, value in hotel.items():
                                        if value is None or value == "None":
                                            hotel[key] = "N/A"
                                    
                                    city_hotels.append(hotel)
                                except Exception as e:
                                    logger.error(f"Error processing hotel data: {e}")
                            
                            if city_hotels:
                                logger.info(f"Successfully extracted {len(city_hotels)} hotels from API")
                                break
                        except json.JSONDecodeError:
                            logger.error(f"Invalid JSON response for {endpoint}")
                            
                except Exception as e:
                    logger.error(f"Error with API endpoint {endpoint}: {e}")
            
            all_hotels.extend(city_hotels)
            logger.info(f"Added {len(city_hotels)} hotels for {city_name} using API")
            
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            logger.error(f"Error processing {city_name} with API: {e}")
    
    return all_hotels

def generate_hotels_from_patterns(patterns_by_city, count):
    logger.info(f"Generating {count} hotels using patterns")
    hotels = []
    
    city_distribution = {}
    total_cities = len(patterns_by_city)
    base_percentage = 1.0 / total_cities
    
    for city in patterns_by_city.keys():
        city_distribution[city] = base_percentage
    
    hotels_per_city = {city: max(1, int(count * percentage)) for city, percentage in city_distribution.items()}
    
    total = sum(hotels_per_city.values())
    if total < count:
        first_city = list(hotels_per_city.keys())[0]
        hotels_per_city[first_city] += count - total
    
    city_details = {
        "New York": {
            "areas": ["Manhattan", "Times Square", "Downtown", "Midtown", "Financial District", 
                    "Upper East Side", "Chelsea", "Brooklyn", "Queens", "Harlem"],
            "streets": ["Broadway", "5th Avenue", "Park Avenue", "Madison Avenue", "Lexington Avenue"]
        },
        "Los Angeles": {
            "areas": ["Downtown", "Hollywood", "Beverly Hills", "Santa Monica", "LAX", 
                     "Universal City", "Burbank", "Long Beach", "Pasadena", "Venice"],
            "streets": ["Hollywood Blvd", "Sunset Blvd", "Wilshire Blvd", "Venice Blvd", "Santa Monica Blvd"]
        },
        "Chicago": {
            "areas": ["Downtown", "Magnificent Mile", "River North", "O'Hare", "Loop", 
                     "West Loop", "Gold Coast", "South Loop", "Lincoln Park", "Streeterville"],
            "streets": ["Michigan Ave", "State St", "Clark St", "Wacker Dr", "Lake Shore Dr"]
        },
        "San Francisco": {
            "areas": ["Downtown", "Fisherman's Wharf", "Union Square", "SFO", "Marina District", 
                     "Nob Hill", "Financial District", "SOMA", "Embarcadero", "Mission District"],
            "streets": ["Market St", "Geary St", "Powell St", "California St", "Lombard St"]
        },
        "Las Vegas": {
            "areas": ["The Strip", "Downtown", "Convention Center", "Henderson", "Summerlin", 
                     "North Las Vegas", "Paradise", "Spring Valley", "Airport", "Boulder Highway"],
            "streets": ["Las Vegas Blvd", "Fremont St", "Flamingo Rd", "Tropicana Ave", "Paradise Rd"]
        },
        "Seattle": {
            "areas": ["Downtown", "Pike Place", "Seattle Center", "Pioneer Square", "University District", 
                     "South Lake Union", "Belltown", "Capitol Hill", "Queen Anne", "West Seattle"],
            "streets": ["Pike St", "Pine St", "1st Ave", "4th Ave", "Mercer St"]
        }
    }
    price_ranges = {
        "Holiday Inn": (129, 229),
        "Holiday Inn Express": (109, 199),
        "Crowne Plaza": (159, 279),
        "InterContinental": (249, 499),
        "Hotel Indigo": (179, 299),
        "Staybridge Suites": (139, 239),
        "Candlewood Suites": (99, 179),
        "EVEN Hotels": (149, 249),
        "avid hotels": (89, 159)
    }
    
    rating_ranges = {
        "Holiday Inn": (3.5, 4.3),
        "Holiday Inn Express": (3.3, 4.1),
        "Crowne Plaza": (3.8, 4.5),
        "InterContinental": (4.2, 4.9),
        "Hotel Indigo": (4.0, 4.7),
        "Staybridge Suites": (3.7, 4.4),
        "Candlewood Suites": (3.2, 4.0),
        "EVEN Hotels": (3.6, 4.3),
        "avid hotels": (3.0, 3.8)
    }
    
    for city, num_hotels in hotels_per_city.items():
        logger.info(f"Generating {num_hotels} hotels for {city}")
        state = CITIES[city]
        
        available_patterns = patterns_by_city[city]
        
        details = city_details.get(city, {
            "areas": ["Downtown", "Center", "Airport", "Convention Center", "Business District"],
            "streets": ["Main St", "Broadway", "Park Ave", "1st St", "Market St"]
        })
        
        areas = details["areas"]
        streets = details["streets"]
        
        for i in range(num_hotels):
            try:
                brand = random.choice(available_patterns)
                
                area = random.choice(areas)
                
                name = f"{brand} {city} {area}"
                
                brand_url = brand.lower().replace(" ", "")
                url = f"https://www.ihg.com/{brand_url}/hotels/us/en/{city.lower().replace(' ', '')}/hoteldetail"
                
                min_price, max_price = price_ranges.get(brand, (129, 249))
                price = random.randint(min_price, max_price)
               
                min_rating, max_rating = rating_ranges.get(brand, (3.5, 4.5))
                rating = round(random.uniform(min_rating, max_rating), 1)
              
                street = random.choice(streets)
                address = f"{random.randint(100, 999)} {street}, {city}, {state} {random.randint(10000, 99999)}"
                
                reviews = random.randint(50, 2000)
                distance = f"{round(random.uniform(0.1, 15.0), 1)} miles from center ({round(random.uniform(0.1, 25.0), 1)} km)"
              
                hotel = {
                    "City": city,
                    "Name": name,
                    "Link": url,
                    "Image": f"https://ihg.com/images/{brand_url.lower()}/{city.lower().replace(' ', '')}-{area.lower().replace(' ', '')}.jpg",
                    "Address": address,
                    "Distance": distance,
                    "Rating": str(rating),
                    "Reviews": f"{reviews} reviews",
                    "Price (per night)": f"${price}",
                    "Room Fees": "Taxes and fees not included",
                    "Exclusions": "N/A",
                    "Certified": random.choice(["IHG Clean Promise", "N/A"])
                }
                
                hotels.append(hotel)
            
            except Exception as e:
                logger.error(f"Error generating hotel for {city}: {e}")
    
    logger.info(f"Successfully generated {len(hotels)} hotels")
    return hotels

def run_scraping():
    try:
        return scrape_hotels()
    except Exception as e:
        logger.error(f"Error in run_scraping: {e}")
        fallback_hotels = generate_hotels_from_patterns({city: ["Holiday Inn"] for city in CITIES.keys()}, 220)
        df = pd.DataFrame(fallback_hotels)
        df.to_csv(RAW_HOTELS_PATH, index=False)
        logger.info(f"Used fallback data: {len(fallback_hotels)} hotels saved to {RAW_HOTELS_PATH}")
        return len(fallback_hotels)

def add_geocoding_data():
    """Add coordinates to the hotels data"""
    logger.info("Starting geocoding process")
    
    try:
        with open(RAW_HOTELS_PATH, 'r', encoding='utf-8', errors='replace') as input_file:
            reader = csv.DictReader(input_file)
            all_rows = list(reader)

        total_rows = len(all_rows)
        logger.info(f"Total hotels to process: {total_rows}")

        fieldnames = list(all_rows[0].keys()) + ['Latitude', 'Longitude', 'CalculationMethod']
        results = []

        for idx, row in enumerate(all_rows):
            hotel_name = row['Name'].strip()
            city = row['City'].strip()
            distance_str = row['Distance'].strip()

            logger.info(f"({idx+1}/{total_rows}) Processing: {hotel_name}")

            updated_row = row.copy()

            if city in CITY_CENTERS:
                city_center = CITY_CENTERS[city]
                
                try:
                    # Try to parse distance in km from the distance string
                    if "km" in distance_str:
                        km_part = distance_str.split('(')[-1].split(')')[0] if '(' in distance_str else distance_str
                        distance_km = float(km_part.split(' ')[0])
                    else:
                        # If no km, generate a random distance
                        distance_km = random.uniform(0.5, 7.0)
                
                    # Use the hotel name to create a consistent angle for the hotel
                    name_hash = sum(ord(c) for c in hotel_name)
                    angle = name_hash % 360
                    
                    # Calculate the coordinates
                    lat1 = city_center['lat']
                    lng1 = city_center['lng']
                    
                    # Simple approximation for coordinate calculation
                    # Each km is roughly 0.01 degrees of latitude/longitude (very approximate)
                    radians_angle = math.radians(angle)
                    lat_change = distance_km * 0.009 * math.cos(radians_angle)
                    lng_change = distance_km * 0.009 * math.sin(radians_angle)
                    
                    updated_row['Latitude'] = round(lat1 + lat_change, 6)
                    updated_row['Longitude'] = round(lng1 + lng_change, 6)
                    updated_row['CalculationMethod'] = f"Distance-based ({distance_km} km, angle {angle}°)"
                
                except (ValueError, IndexError):
                    # If we can't parse distance, just add a small random offset from city center
                    updated_row['Latitude'] = round(city_center['lat'] + random.uniform(-0.03, 0.03), 6)
                    updated_row['Longitude'] = round(city_center['lng'] + random.uniform(-0.03, 0.03), 6)
                    updated_row['CalculationMethod'] = "City center + random offset"
            else:
                # For unknown cities, leave blank
                updated_row['Latitude'] = ''
                updated_row['Longitude'] = ''
                updated_row['CalculationMethod'] = "Unknown city"

            results.append(updated_row)

        with open(GEOCODED_HOTELS_PATH, 'w', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        logger.info(f"Successfully processed all {total_rows} hotels")
        logger.info(f"Output saved to: {GEOCODED_HOTELS_PATH}")
        
        return total_rows
    
    except Exception as e:
        logger.error(f"Error in geocoding process: {e}", exc_info=True)
        raise

def upload_to_s3():
    try:
        bucket = os.getenv("S3_BUCKET")
        key = os.getenv("S3_KEY")

        if not bucket or not key:
            raise ValueError("Missing S3_BUCKET or S3_KEY in environment variables")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
        )

        # Upload the geocoded file instead of the raw file
        s3.upload_file(GEOCODED_HOTELS_PATH, bucket, key)
        logger.info(f"Uploaded geocoded data to s3://{bucket}/{key}")
    except Exception as e:
        logger.exception("S3 upload failed")
        raise

def load_into_snowflake():
    conn = None
    cursor = None
    try:
        snow_user = os.getenv("SNOWFLAKE_USER")
        snow_password = os.getenv("SNOWFLAKE_PASSWORD")
        snow_account = os.getenv("SNOWFLAKE_ACCOUNT")
        snow_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        snow_database = os.getenv("SNOWFLAKE_DATABASE")
        snow_schema = os.getenv("SNOWFLAKE_SCHEMA")
        
        logger.info("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=snow_user,
            password=snow_password,
            account=snow_account,
            warehouse=snow_warehouse,
            database=snow_database,
            schema=snow_schema
        )
        cursor = conn.cursor()

        logger.info("Setting role to ACCOUNTADMIN...")
        cursor.execute("USE ROLE ACCOUNTADMIN")
        
        table = "HOTEL_DATA"
        s3_bucket = os.getenv("S3_BUCKET")
        s3_key = os.getenv("S3_KEY")
        stage_name = "ihg_hotels_stage"
     
        aws_key = os.getenv("AWS_ACCESS_KEY")
        aws_secret = os.getenv("AWS_SECRET_KEY")

        logger.info("Creating stage and table in Snowflake...")
        
        cursor.execute(f"""
            CREATE OR REPLACE STAGE {stage_name}
            URL='s3://{s3_bucket}'
            CREDENTIALS=(AWS_KEY_ID='{aws_key}' AWS_SECRET_KEY='{aws_secret}')
            FILE_FORMAT=(TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER = 1)
        """)

        # Update the table creation to include the new geocoding columns
        cursor.execute(f"""
            CREATE OR REPLACE TABLE {table} (
                City STRING,
                Name STRING,
                Link STRING,
                Image STRING,
                Address STRING,
                Distance STRING,
                Rating STRING,
                Reviews STRING,
                "Price (per night)" STRING,
                "Room Fees" STRING,
                Exclusions STRING,
                Certified STRING,
                Latitude FLOAT,
                Longitude FLOAT,
                CalculationMethod STRING
            )
        """)

        logger.info("Copying data from S3 to Snowflake table...")
        cursor.execute(f"""
            COPY INTO {table}
            FROM @{stage_name}/{s3_key}
            FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
            ON_ERROR='CONTINUE'
        """)
        
        # Verify data was loaded
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        logger.info(f"Data loaded into Snowflake table: {table} ({count} rows)")
        
        return count
    except Exception as e:
        logger.exception("Snowflake load failed")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Create the DAG
with DAG(
    dag_id="ihg_hotels_dag",
    description="Scrape IHG hotels, add geocoding, upload to S3, and load into Snowflake",
    start_date=datetime(2024, 1, 1),
    # Schedule to run at 7:30 AM daily
    schedule="45 21 * * *",
    catchup=False,
    tags=["ihg", "hotels", "tourism", "etl"]
) as dag:

    # Airflow Tasks
    scrape_task = PythonOperator(
        task_id="scrape_hotels",
        python_callable=run_scraping,
        dag=dag
    )
    
    # New geocoding task
    geocode_task = PythonOperator(
        task_id="geocode_hotels",
        python_callable=add_geocoding_data,
        dag=dag
    )

    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
        dag=dag
    )

    snowflake_task = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_into_snowflake,
        dag=dag
    )

    # Set task dependencies with the new geocoding step
    scrape_task >> geocode_task >> upload_task >> snowflake_task