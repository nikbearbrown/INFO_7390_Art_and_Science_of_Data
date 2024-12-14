from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import logging

# Load environment variables
load_dotenv()

# Access the NEWSAPI_KEY variable
api_key = os.getenv("NEWSAPI_KEY")

if not api_key:
    raise ValueError("API key not found. Please ensure 'NEWSAPI_KEY' is set in your .env file.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_news(query: str = None, country: str = "us") -> list:
    """
    Fetch news articles using NewsAPI first, then fallback to Bing and Google scraping.

    Parameters:
        query (str): Search term for news articles (e.g., 'Scholarships', 'Events').
        country (str): Country code for news localization (default is 'us').

    Returns:
        list: A list of news articles with title, description, and source.
    """
    try:
        # Try NewsAPI
        logger.info("Attempting to fetch news using NewsAPI...")
        articles = fetch_news_api(query, country)
        if articles:
            logger.info(f"NewsAPI fetched {len(articles)} articles.")
            return articles
    except Exception as e:
        logger.error(f"NewsAPI failed: {e}")

    try:
        # Fallback to Bing News scraping
        logger.info("Falling back to Bing News scraping...")
        articles = scrape_backup_news_bing(query)
        if articles:
            logger.info(f"Bing News scraping fetched {len(articles)} articles.")
            return articles
    except Exception as e:
        logger.error(f"Bing News scraping failed: {e}")

    try:
        # Fallback to Google News scraping
        logger.info("Falling back to Google News scraping...")
        articles = scrape_backup_news(query)
        if articles:
            logger.info(f"Google News scraping fetched {len(articles)} articles.")
            return articles
    except Exception as e:
        logger.error(f"Google News scraping failed: {e}")

    # If all sources fail
    logger.warning("No articles found from any source.")
    return []

def fetch_news_api(query: str, country: str) -> list:
    """
    Fetch articles from NewsAPI.

    Parameters:
        query (str): Search term for news articles.
        country (str): Country code for news localization.

    Returns:
        list: A list of news articles from NewsAPI.
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "q": query,
        "category": "education",
        "country": country,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok" and data.get("articles"):
            logger.info(f"Number of articles fetched from NewsAPI: {len(data['articles'])}")
            return [
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "source": article["source"]["name"],
                }
                for article in data["articles"]
            ]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news from NewsAPI: {e}")
        raise
    return []

def scrape_backup_news_bing(query: str) -> list:
    """
    Scrape news articles from Bing News.

    Parameters:
        query (str): Search term for news articles.

    Returns:
        list: A list of scraped news articles from Bing.
    """
    search_url = f"https://www.bing.com/news/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Parse search results for news articles
        articles = []
        for item in soup.select(".news-card"):  # Update CSS selector based on Bing's structure
            title = item.select_one("a.title").get_text() if item.select_one("a.title") else "No Title"
            url = item.select_one("a.title")["href"] if item.select_one("a.title") else "No URL"
            snippet = item.select_one(".snippet").get_text() if item.select_one(".snippet") else "No Description"
            articles.append({"title": title, "description": snippet, "url": url, "source": "Bing News"})
            if len(articles) >= 10:  # Limit to 10 articles
                break

        logger.info(f"Number of articles fetched from Bing: {len(articles)}")
        return articles
    except Exception as e:
        logger.error(f"Error during Bing scraping: {e}")
        return []

def scrape_backup_news(query: str) -> list:
    """
    Scrape news articles using Beautiful Soup as a fallback.

    Parameters:
        query (str): Search term for news articles.

    Returns:
        list: A list of scraped news articles with title and URL.
    """
    search_url = f"https://www.google.com/search?q={query}+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # Debugging: Print the raw HTML response
        logger.debug("Raw HTML content: %s", response.text[:1000])  # Print first 1000 characters

        soup = BeautifulSoup(response.text, "html.parser")

        # Parse search results for news articles
        articles = []
        for item in soup.select("div.tF2Cxc"):  # Adjust CSS selectors for the target website
            title = item.select_one("h3").get_text() if item.select_one("h3") else "No Title"
            url = item.select_one("a")["href"] if item.select_one("a") else "No URL"
            snippet = item.select_one(".IsZvec").get_text() if item.select_one(".IsZvec") else "No Description"
            articles.append({"title": title, "description": snippet, "url": url, "source": "Google News"})
            if len(articles) >= 10:  # Limit to 10 articles
                break

        logger.info(f"Number of articles fetched from Google scraping: {len(articles)}")
        return articles
    except Exception as e:
        logger.error(f"Error during Google scraping: {e}")
        return []
