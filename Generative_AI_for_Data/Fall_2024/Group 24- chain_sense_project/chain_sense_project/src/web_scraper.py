# Add a try-except block to handle import errors
try:
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import json
    import os
    import time
    import re
except ImportError as e:
    print(f"Import error: {e}. Please ensure all required libraries are installed.")
    exit(1)  # Exit if imports fail

# Base URL of Bloomberg
BASE_URL = "https://www.bloomberg.com"

# Use a Bloomberg search results URL for "supply chain"
LISTING_URL = "https://www.bloomberg.com/search?query=supply%20chain"

def get_article_links_with_selenium(listing_url):
    """Fetch article links using Selenium for dynamic content."""
    # Set up the WebDriver (ensure you have ChromeDriver or appropriate driver installed)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)  # Adjust for your browser and driver

    # Load the URL
    driver.get(listing_url)

    # Wait for JavaScript content to load
    time.sleep(15)

    # Get the page source after rendering
    html = driver.page_source
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Selecting all story items
    article_divs = soup.select('div.storyItem__aaf871c15')
    print(f"Found {len(article_divs)} article elements on the listing page.")

    articles = []
    for div in article_divs:
        # Extract the headline link and text
        headline_tag = div.select_one('a.headline_3a97424275')
        if headline_tag:
            link = headline_tag['href']
            title = headline_tag.get_text(strip=True)
            if not link.startswith("http"):
                link = BASE_URL + link

            # Extract the publication date
            date_tag = div.select_one('div.publishedAt__dc9df8db4')
            date = date_tag.get_text(strip=True) if date_tag else "No Date"

            # Append the article info
            articles.append({
                "title": title,
                "url": link,
                "date": date
            })

    return articles

def clean_text(text):
    """Clean up text by removing extra whitespace."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_article_content(article_url):
    """Extract the article title and content."""
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/101.0.4951.67 Safari/537.36")
    }

    response = requests.get(article_url, headers=headers)
    print(f"Status code for article page {article_url}: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to retrieve article: {article_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Update the title extraction based on your HTML structure
    # The headline is inside <div class="media-ui-HedAndDek_headline"> h1
    title_element = soup.select_one('h1.media-ui-HedAndDek_headline')
    title = title_element.get_text(strip=True) if title_element else "No Title"

    # Extract the article content paragraphs
    # Based on assumption from previous examples
    content_elements = soup.select('div.article-body__content p')
    paragraphs = [clean_text(p.get_text()) for p in content_elements if p.get_text(strip=True)]
    content = " ".join(paragraphs)

    if not content:
        print("No content found in the article.")
        return None

    return {
        "url": article_url,
        "title": title,
        "text": content
    }

def scrape_articles(listing_url, max_articles=5):
    """Scrape articles starting from the listing page."""
    articles_metadata = get_article_links_with_selenium(listing_url)
    all_articles = []

    for article in articles_metadata[:max_articles]:
        print(f"Scraping article: {article['title']}")
        article_content = extract_article_content(article['url'])
        if article_content:
            # Add metadata (title, URL, date) from the listing page
            article_content['date'] = article['date']
            all_articles.append(article_content)

        # Pause to avoid hitting the site too fast
        time.sleep(2)

    return all_articles

if __name__ == "__main__":
    # Create the data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    articles = scrape_articles(LISTING_URL, max_articles=5)

    # Save scraped articles to a JSON file
    output_path = os.path.join("data", "scraped_articles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Scraping complete. {len(articles)} articles saved to {output_path}")









# # Add a try-except block to handle import errors
# try:
#     import requests
#     from bs4 import BeautifulSoup
#     import json
#     import os
#     import time
#     import re
# except ImportError as e:
#     print(f"Import error: {e}. Please ensure all required libraries are installed.")
#     exit(1)  # Exit if imports fail

# # Base URL of Bloomberg
# BASE_URL = "https://www.bloomberg.com"

# # Use a Bloomberg search results URL for "supply chain"
# # Inspect the page to confirm it shows multiple articles
# LISTING_URL = "https://www.bloomberg.com/search?query=supply%20chain"

# def get_article_links(listing_url):
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(listing_url, headers=headers)
#     print(f"Status code for listing page: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve {listing_url}")
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Selecting all story items
#     article_divs = soup.select('div.storyItem__aaf871c15')
#     print(f"Found {len(article_divs)} article elements on the listing page.")

#     articles = []
#     for div in article_divs:
#         # Extract the headline link and text
#         headline_tag = div.select_one('a.headline_3a97424275')
#         if headline_tag:
#             link = headline_tag['href']
#             title = headline_tag.get_text(strip=True)
#             if not link.startswith("http"):
#                 link = BASE_URL + link  # Ensure full URL

#             # Extract the publication date
#             date_tag = div.select_one('div.publishedAt__dc9df8db4')
#             date = date_tag.get_text(strip=True) if date_tag else "No Date"

#             # Append the article info
#             articles.append({
#                 "title": title,
#                 "url": link,
#                 "date": date
#             })

#     return articles

# def clean_text(text):
#     # Basic text cleanup: remove extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_article_content(article_url):
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(article_url, headers=headers)
#     print(f"Status code for article page {article_url}: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve article: {article_url}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Extract the article headline
#     title_element = soup.select_one('div[data-component="hed-and-dek"] h1')
#     title = title_element.get_text(strip=True) if title_element else "No Title"

#     # Extract the article content paragraphs
#     content_elements = soup.select('article p')
#     paragraphs = [clean_text(p.get_text()) for p in content_elements if p.get_text(strip=True)]
#     content = " ".join(paragraphs)

#     if not content:
#         print("No content found in the article.")
#         return None

#     return {
#         "url": article_url,
#         "title": title,
#         "text": content
#     }

# def scrape_articles(listing_url, max_articles=5):
#     articles = get_article_links(listing_url)
#     all_articles = []

#     for article in articles[:max_articles]:
#         print(f"Scraping article: {article['title']}")
#         article_content = extract_article_content(article['url'])
#         if article_content:
#             # Add title and date from the listing page metadata
#             article_content['date'] = article['date']
#             all_articles.append(article_content)

#         # Pause to avoid hitting the site too fast
#         time.sleep(2)

#     return all_articles

# if __name__ == "__main__":
#     # Create the data directory if it doesn't exist
#     if not os.path.exists("data"):
#         os.makedirs("data")

#     articles = scrape_articles(LISTING_URL, max_articles=5)

#     # Save scraped articles to a JSON file
#     output_path = os.path.join("data", "scraped_articles.json")
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(articles, f, ensure_ascii=False, indent=2)

#     print(f"Scraping complete. {len(articles)} articles saved to {output_path}")












# # Add a try-except block to handle import errors
# try:
#     import requests
#     from bs4 import BeautifulSoup
#     import json
#     import os
#     import time
#     import re
# except ImportError as e:
#     print(f"Import error: {e}. Please ensure all required libraries are installed.")
#     exit(1)  # Exit if imports fail

# # Base URL of Bloomberg
# BASE_URL = "https://www.bloomberg.com"

# # Use a Bloomberg search results URL for "supply chain"
# # Inspect the page to confirm it shows multiple articles
# LISTING_URL = "https://www.bloomberg.com/search?query=supply%20chain"

# def get_article_links(listing_url):
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(listing_url, headers=headers)
#     print(f"Status code for listing page: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve {listing_url}")
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Based on your screenshot:
#     # <div class="storyItem__...">
#     #   ...
#     #   <a class="headline_3a97424275" href="...">Article Title</a>
#     #   ...
#     # </div>
#     #
#     # We'll select all 'a' tags with class starting with "headline_"
#     # If the exact class changes, re-check the HTML and adjust.
#     article_elements = soup.select('a[class^="headline_"]')

#     print(f"Found {len(article_elements)} article elements on the listing page.")
#     links = [a.get('href') for a in article_elements if a.get('href')]

#     # Ensure full URLs
#     full_links = []
#     for link in links:
#         if link.startswith('http'):
#             full_links.append(link)
#         else:
#             full_links.append(BASE_URL + link)

#     # Deduplicate if needed
#     full_links = list(set(full_links))

#     return full_links

# def clean_text(text):
#     # Basic text cleanup: remove extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_article_content(article_url):
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(article_url, headers=headers)
#     print(f"Status code for article page {article_url}: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve article: {article_url}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Based on previous examples and your snippet:
#     # The headline might be under div[data-component="hed-and-dek"] h1
#     # Verify by inspecting the article page.
#     title_element = soup.select_one('div[data-component="hed-and-dek"] h1')
#     title = title_element.get_text(strip=True) if title_element else "No Title"

#     # For paragraphs:
#     # Check if <article> contains the paragraphs. If not, inspect the HTML carefully.
#     content_elements = soup.select('article p')
#     paragraphs = [clean_text(p.get_text()) for p in content_elements if p.get_text(strip=True)]
#     content = " ".join(paragraphs)

#     if not content:
#         print("No content found in the article.")
#         return None

#     return {
#         "url": article_url,
#         "title": title,
#         "text": content
#     }

# def scrape_articles(listing_url, max_articles=5):
#     article_links = get_article_links(listing_url)
#     all_articles = []

#     # Limit to a few articles for demonstration
#     for link in article_links[:max_articles]:
#         article_data = extract_article_content(link)
#         if article_data:
#             all_articles.append(article_data)
#             # Pause to be respectful, avoid hitting the site too fast
#             time.sleep(2)

#     return all_articles

# if __name__ == "__main__":
#     # Create the data directory if it doesn't exist
#     if not os.path.exists("data"):
#         os.makedirs("data")

#     articles = scrape_articles(LISTING_URL, max_articles=5)

#     # Save scraped articles to a JSON file
#     output_path = os.path.join("data", "scraped_articles.json")
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(articles, f, ensure_ascii=False, indent=2)

#     print(f"Scraping complete. {len(articles)} articles saved to {output_path}")













# # Add a try-except block to handle import errors
# try:
#     import requests
#     from bs4 import BeautifulSoup
#     import json
#     import os
#     import time
#     import re
# except ImportError as e:
#     print(f"Import error: {e}. Please ensure all required libraries are installed.")
#     exit(1)  # Exit the program if imports fail

# # Base URL of the site we want to scrape
# BASE_URL = "https://www.bloomberg.com"
# # Update this URL to a current Bloomberg page listing articles of interest
# LISTING_URL = "https://www.bloomberg.com/search?query=supply%20chain"

# def get_article_links(listing_url):
#     # Add a user-agent to potentially avoid request blocking
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(listing_url, headers=headers)
#     print(f"Status code for listing page: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve {listing_url}")
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # TODO: Update this selector based on Bloomberg’s actual structure
#     # The selector below is from the previous example and likely won't work.
#     # Inspect the Bloomberg listing page to find the correct selector.
#     article_elements = soup.select('h3.feed_item_title a')
#     print(f"Found {len(article_elements)} article elements on the listing page.")

#     links = [BASE_URL + a['href'] for a in article_elements if a.get('href')]
#     return links

# def clean_text(text):
#     # Basic text cleanup: remove extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_article_content(article_url):
#     headers = {
#         "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/101.0.4951.67 Safari/537.36")
#     }

#     response = requests.get(article_url, headers=headers)
#     print(f"Status code for article page {article_url}: {response.status_code}")
#     if response.status_code != 200:
#         print(f"Failed to retrieve article: {article_url}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # TODO: Update these selectors based on Bloomberg’s article page structure.
#     # Example placeholders:
#     title_element = soup.select_one('h1.article-headline')
#     title = title_element.get_text(strip=True) if title_element else "No Title"

#     content_elements = soup.select('div.article-body p')
#     paragraphs = [clean_text(p.get_text()) for p in content_elements if p.get_text(strip=True)]
#     content = " ".join(paragraphs)

#     if not content:
#         return None

#     return {
#         "url": article_url,
#         "title": title,
#         "text": content
#     }

# def scrape_articles(listing_url, max_articles=5):
#     article_links = get_article_links(listing_url)
#     all_articles = []

#     # Limit to a few articles for demonstration
#     for link in article_links[:max_articles]:
#         article_data = extract_article_content(link)
#         if article_data:
#             all_articles.append(article_data)
#             # Pause to be respectful
#             time.sleep(2)

#     return all_articles

# if __name__ == "__main__":
#     # Create the data directory if it doesn't exist
#     if not os.path.exists("data"):
#         os.makedirs("data")

#     articles = scrape_articles(LISTING_URL, max_articles=5)

#     # Save scraped articles to a JSON file
#     output_path = os.path.join("data", "scraped_articles.json")
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(articles, f, ensure_ascii=False, indent=2)

#     print(f"Scraping complete. {len(articles)} articles saved to {output_path}")





# # Add a try-except block to handle import errors
# try:
#     import requests
#     from bs4 import BeautifulSoup
#     import json
#     import os
#     import time
#     import re
# except ImportError as e:
#     print(f"Import error: {e}. Please ensure all required libraries are installed.")
#     exit(1)  # Exit the program if imports fail

# # Base URL of the site we want to scrape
# BASE_URL = "https://www.bloomberg.com"
# # For demonstration, let's pick a page that lists supply chain disruptions
# # This URL may change over time, so update it as needed:
# LISTING_URL = "https://www.bloomberg.com/news/newsletters/2024-06-25/supply-chain-latest-global-trade-disruptions-and-shipping"

# def get_article_links(listing_url):
#     response = requests.get(listing_url)
#     if response.status_code != 200:
#         print(f"Failed to retrieve {listing_url}")
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Using the updated selector based on the provided screenshot and structure
#     # h3.feed_item_title a -> selects article links in h3 tags with class 'feed_item_title'
#     article_elements = soup.select('h3.feed_item_title a')
#     links = [BASE_URL + a['href'] for a in article_elements if a.get('href')]
#     return links

# def clean_text(text):
#     # Basic text cleanup: remove extra whitespace
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_article_content(article_url):
#     response = requests.get(article_url)
#     if response.status_code != 200:
#         print(f"Failed to retrieve article: {article_url}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find the article title
#     # Adjust the selector if the site's structure changes
#     title_element = soup.select_one('h1.article-headline')
#     title = title_element.get_text(strip=True) if title_element else "No Title"

#     # Extract main content paragraphs
#     # Adjust the container class if needed. Check the site's HTML for the correct class name.
#     content_elements = soup.select('div.article-body p')
#     paragraphs = [clean_text(p.get_text()) for p in content_elements if p.get_text(strip=True)]
#     content = " ".join(paragraphs)

#     if not content:
#         return None

#     return {
#         "url": article_url,
#         "title": title,
#         "text": content
#     }

# def scrape_articles(listing_url, max_articles=5):
#     # Get a list of article links from the listing page
#     article_links = get_article_links(listing_url)
#     all_articles = []

#     # Limit to a few articles for demonstration
#     for link in article_links[:max_articles]:
#         article_data = extract_article_content(link)
#         if article_data:
#             all_articles.append(article_data)
#             # Pause to be respectful, avoid hitting the site too fast
#             time.sleep(2)

#     return all_articles

# if __name__ == "__main__":
#     # Create the data directory if it doesn't exist
#     if not os.path.exists("data"):
#         os.makedirs("data")

#     articles = scrape_articles(LISTING_URL, max_articles=5)

#     # Save scraped articles to a JSON file
#     output_path = os.path.join("data", "scraped_articles.json")
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(articles, f, ensure_ascii=False, indent=2)

#     print(f"Scraping complete. {len(articles)} articles saved to {output_path}")
