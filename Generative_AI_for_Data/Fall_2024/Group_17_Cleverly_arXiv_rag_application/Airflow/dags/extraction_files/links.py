import requests
from bs4 import BeautifulSoup
import re
import time
import snowflake.connector
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='scraping_log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Keywords to filter data-related links
TECH_KEYWORDS = [
    'data', 'data-science', 'machine-learning', 'artificial-intelligence', 'deep-learning',
    'python', 'statistics', 'data-analytics', 'data-engineering', 'data-pipelines',
    'data-processing', 'data-visualization', 'data-wrangling', 'data-mining',
    'data-management', 'data-governance', 'data-security', 'data-modeling',
    'data-quality', 'data-transformation', 'data-lakes', 'data-warehousing',
    'predictive-modeling', 'classification', 'regression', 'clustering',
    'dimensionality-reduction', 'time-series-analysis', 'database', 'sql', 'etl'
]

BASE_URL = "https://www.geeksforgeeks.org/"

# Snowflake configuration
SNOWFLAKE_CONFIG = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
    'database': os.getenv("SNOWFLAKE_DATABASE"),
    'schema': os.getenv("SNOWFLAKE_SCHEMA"),
}

# Verify that environment variables are loaded correctly
logging.debug(f"Loaded environment variables: SNOWFLAKE_USER={SNOWFLAKE_CONFIG['user']}, SNOWFLAKE_ACCOUNT={SNOWFLAKE_CONFIG['account']}, SNOWFLAKE_WAREHOUSE={SNOWFLAKE_CONFIG['warehouse']}, SNOWFLAKE_DATABASE={SNOWFLAKE_CONFIG['database']}, SNOWFLAKE_SCHEMA={SNOWFLAKE_CONFIG['schema']}")

# Snowflake database connection
def get_db_connection():
    logging.info(f"Connecting to Snowflake account: {SNOWFLAKE_CONFIG['account']}")
    try:
        connection = snowflake.connector.connect(
            user=SNOWFLAKE_CONFIG['user'],
            password=SNOWFLAKE_CONFIG['password'],
            account=SNOWFLAKE_CONFIG['account'],
            warehouse=SNOWFLAKE_CONFIG['warehouse'],
            database=SNOWFLAKE_CONFIG['database'],
            schema=SNOWFLAKE_CONFIG['schema']
        )
        logging.info("Successfully connected to Snowflake.")
        return connection
    except snowflake.connector.Error as e:
        logging.error(f"Failed to connect to Snowflake: {e}")
        raise

# Function to collect links and titles related to data topics from GeeksforGeeks
def scrape_tech_links(base_url, keywords, max_links=1000):
    links = []
    pages_to_scrape = [base_url]
    visited_pages = set()
    try:
        while pages_to_scrape and len(links) < max_links:
            current_url = pages_to_scrape.pop(0)
            if current_url in visited_pages:
                continue
            visited_pages.add(current_url)

            logging.info(f"Scraping page: {current_url}")
            response = requests.get(current_url)
            if response.status_code != 200:
                logging.error(f"Unable to fetch page: {current_url}, Status code: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                title = a_tag.get_text(strip=True)
                lower_title = title.lower()
                if any(keyword in href.lower() for keyword in keywords) or any(keyword in lower_title for keyword in keywords): # Add links that match the keywords either in the URL or title
                    full_link = href if href.startswith('http') else base_url + href
                    if full_link not in [link[1] for link in links]:
                        links.append((len(links) + 1, full_link, title, datetime.utcnow()))
                        logging.info(f"Found link: {full_link} with title: {title}")
                        if base_url in full_link and full_link not in visited_pages and full_link not in pages_to_scrape:
                            pages_to_scrape.append(full_link)
                
                if len(links) >= max_links:
                    break
            time.sleep(1)
    
    except requests.RequestException as e:
        logging.error(f"Error occurred: {e}")
    
    return links

def insert_into_snowflake_bulk(links):
    try:
        # Connect to Snowflake
        connection = get_db_connection()
        cursor = connection.cursor()

        # Create the main table with AUTO_INCREMENT for the ID column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TECH_LINKS (
                ID INT AUTOINCREMENT,  -- Auto-incrementing ID
                LINK STRING UNIQUE,   -- Ensures no duplicate links
                TITLE STRING,
                TIMESTAMP TIMESTAMP_NTZ
            )
        ''')
        logging.info("Main table TECH_LINKS created or already exists.")

        # Create a temporory table for adding the new links 
        cursor.execute('''
            CREATE TEMPORARY TABLE TEMP_TECH_LINKS (
                LINK STRING,
                TITLE STRING,
                TIMESTAMP TIMESTAMP_NTZ
            )
        ''')
        logging.info("Temporary table TEMP_TECH_LINKS created.")

        # inserting into the temporary table
        cursor.executemany('''
            INSERT INTO TEMP_TECH_LINKS (LINK, TITLE, TIMESTAMP)
            VALUES (%s, %s, %s)
        ''', [(link[1], link[2], link[3]) for link in links])  # Skip link[0] (ID) in the insert
        logging.info(f"Inserted {len(links)} records into TEMP_TECH_LINKS.")

        # Merge data from the temporary table into the main table - logic to avoid duplicate links
        cursor.execute('''
            MERGE INTO TECH_LINKS AS TARGET
            USING TEMP_TECH_LINKS AS SOURCE
            ON TARGET.LINK = SOURCE.LINK
            WHEN NOT MATCHED THEN
                INSERT (LINK, TITLE, TIMESTAMP)
                VALUES (SOURCE.LINK, SOURCE.TITLE, SOURCE.TIMESTAMP);
        ''')
        logging.info("Merged records from TEMP_TECH_LINKS into TECH_LINKS.")

        connection.commit()
        logging.info("Database operations completed successfully.")
    except snowflake.connector.Error as e:
        logging.error(f"Snowflake error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    logging.info("Starting the scraping process.")
    tech_links = scrape_tech_links(BASE_URL, TECH_KEYWORDS)
    
    if tech_links:
        insert_into_snowflake_bulk(tech_links)
    else:
        logging.info("No links collected.")