import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_iframe_page(main_url):
    """
    Scrapes an HTML page for course details by fetching iframe content.

    Args:
        main_url (str): URL of the main page containing the iframe.

    Returns:
        pd.DataFrame: A DataFrame containing course details.
    """
    try:
        response = requests.get(main_url)
        if response.status_code != 200:
            print(f"Failed to fetch main page. Status code: {response.status_code}")
            return pd.DataFrame()

        soup = BeautifulSoup(response.text, 'html.parser')
        iframe = soup.find('iframe')
        if not iframe or 'src' not in iframe.attrs:
            print("No iframe found or iframe src missing.")
            return pd.DataFrame()

        iframe_url = iframe['src']
        iframe_response = requests.get(iframe_url)
        if iframe_response.status_code != 200:
            print(f"Failed to fetch iframe content. Status code: {iframe_response.status_code}")
            return pd.DataFrame()

        iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
        course_data = []
        tables = iframe_soup.find_all('table', class_='table table-striped')
        for table in tables:
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 4:
                    continue
                name = cells[0].text.strip()
                crn = cells[1].text.strip()
                timing = cells[2].text.strip()
                instructor = cells[3].text.strip()
                course_data.append({
                    'Course Name': name,
                    'CRN': crn,
                    'Instructor': timing,
                    'Timings': instructor
                })
        return pd.DataFrame(course_data)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
