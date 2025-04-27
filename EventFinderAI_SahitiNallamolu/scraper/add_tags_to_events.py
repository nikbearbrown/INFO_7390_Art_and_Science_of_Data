import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4

# Set up selenium headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

def fetch_tags_selenium(event_link):
    try:
        driver.get(event_link)
        time.sleep(2)  # Let JS load
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "html.parser")

        # New targeting based on provided structure
        tags_container = soup.find("div", {"data-testid": "tags"})

        tags = []
        if tags_container:
            tag_items = tags_container.find_all("li", class_="tags-item")
            for item in tag_items:
                a_tag = item.find("a")
                if a_tag:
                    tags.append(a_tag.get_text(strip=True))

        return tags
    except Exception as e:
        print(f"Error fetching tags from {event_link}: {e}")
        return []


def process_file(filename):
    print(f"Processing {filename}...")
    filepath = os.path.join("data", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        events = json.load(f)

    updated_events = []
    for event in events:
        if "tags" not in event or not event["tags"]:
            tags = fetch_tags_selenium(event["event_link"])
            event["tags"] = tags
        updated_events.append(event)

    # Save updated JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(updated_events, f, ensure_ascii=False, indent=4)

    print(f"Updated {len(updated_events)} events with tags.")

def main():
    for filename in os.listdir("data"):
        if filename.endswith("_events.json"):
            process_file(filename)

if __name__ == "__main__":
    main()
    driver.quit()
