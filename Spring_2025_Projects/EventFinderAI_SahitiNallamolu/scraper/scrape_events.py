import os
import json as js
import asyncio
import aiohttp
import bs4

# Ensure data/ folder exists
os.makedirs('data', exist_ok=True)

# Define the categories and base URL
categories = [
    "business",
    "music",
    "family-and-education",
    "arts",
    "hobbies",
    "science-and-tech",
    "travel-and-outdoor",
    "film-and-media"
]

base_url = "https://www.eventbrite.com/d/ma--boston/{category}--events/?page={page}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Function to fetch the HTML of a page
async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to parse a single event page (without Tags)
async def parse_event(session, url):
    html = await fetch(session, url)
    if html is None:
        return None

    soup = bs4.BeautifulSoup(html, "html.parser")
    
    # Title
    try:
        title = soup.find('h1').get_text(strip=True)
    except AttributeError:
        title = "N/A"

    # Date and Time
    try:
        date_time_container = soup.find("div", {"data-testid": "dateAndTime"})
        date_time = date_time_container.find("span", class_="date-info__full-datetime").get_text(strip=True)
    except AttributeError:
        date_time = "N/A"

    # Location
    try:
        location_container = soup.find("div", {"data-testid": "location"})
        location_info = location_container.find("div", class_="location-info__address")
        location = location_info.get_text(separator=" ", strip=True) if location_info else "N/A"
    except AttributeError:
        location = "N/A"

    # About the event
    try:
        about_section = soup.find("div", {"class": "structured-content-rich-text"}).get_text(separator=" ", strip=True)
    except AttributeError:
        about_section = "N/A"

    return {
        "title": title,
        "date_time": date_time,
        "location": location,
        "about": about_section,
        "event_link": url
    }

# Main function to scrape category
async def scrape_category(category):
    print(f"Scraping category: {category}...")
    all_event_links = []

    async with aiohttp.ClientSession() as session:
        # Step 1: Collect event links from pages 1-3
        for page in range(1, 4):
            url = base_url.format(category=category, page=page)
            html = await fetch(session, url)
            if html is None:
                continue
            soup = bs4.BeautifulSoup(html, "html.parser")
            link_objects = soup.find_all('a', href=True)
            for link in link_objects:
                href = link['href']
                if "/e/" in href and href.startswith("https://www.eventbrite.com/e/"):
                    all_event_links.append(href)

        # Remove duplicates
        all_event_links = list(dict.fromkeys(all_event_links))
        print(f"Found {len(all_event_links)} event links in category '{category}'")

        # Step 2: Scrape all events in parallel
        tasks = [parse_event(session, url) for url in all_event_links]
        all_events = await asyncio.gather(*tasks)

        # Filter out any None results
        all_events = [event for event in all_events if event is not None]

        # Step 3: Save to JSON
        output_filename = f"data/{category}_events.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            js.dump(all_events, f, ensure_ascii=False, indent=4)

        print(f"Saved {len(all_events)} events for category '{category}' to {output_filename}")

# Master runner
async def main():
    tasks = [scrape_category(category) for category in categories]
    await asyncio.gather(*tasks)

# Start
if __name__ == "__main__":
    asyncio.run(main())
