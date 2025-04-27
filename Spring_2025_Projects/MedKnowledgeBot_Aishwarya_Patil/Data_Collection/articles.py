import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")  # Run in headless mode for efficiency
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Base URL
base_url = "https://bmcmedicine.biomedcentral.com/articles"

# List of topics to search for
topics = [
    "mental+health",
    "diabetes",
    "cancer",
    "cardiovascular+disease",
    "infectious+disease"
]

# Create directory for CSV files if it doesn't exist
os.makedirs("data", exist_ok=True)

# Number of pages to scrape per topic
start_page = 1
end_page = 5  # Reduced to 5 pages per topic to keep total time reasonable

# Process each topic
for topic in topics:
    print(f"\n==== STARTING SCRAPING FOR TOPIC: {topic.replace('+', ' ')} ====\n")
    
    # List to store article data for this topic
    articles_data = []
    
    search_params = f"?tab=keyword&searchType=journalSearch&sort=Relevance&query={topic}"
    
    try:
        for page_num in range(start_page, end_page + 1):
            # Construct URL for the current page
            if page_num == 1:
                current_url = f"{base_url}{search_params}"
            else:
                current_url = f"{base_url}{search_params}&page={page_num}"
            
            print(f"Navigating to page {page_num}: {current_url}")
            driver.get(current_url)
            
            # Accept cookies if the dialog appears (only needed on first page of first topic)
            if page_num == 1 and topic == topics[0]:
                try:
                    cookie_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                    )
                    cookie_button.click()
                    print("Accepted cookies")
                except:
                    print("No cookie dialog found or already accepted")
            
            # Wait for the article list to load
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.c-listing__item"))
                )
                
                # Extract all article elements
                articles = driver.find_elements(By.CSS_SELECTOR, "li.c-listing__item")
                print(f"Found {len(articles)} articles on page {page_num}.")
                
                if len(articles) == 0:
                    print(f"No articles found on page {page_num}. This might be the last page.")
                    break
                    
                # Iterate over each article and extract details
                for article in articles:
                    try:
                        # Extract article title
                        try:
                            title_element = article.find_element(By.CSS_SELECTOR, ".c-listing__title a")
                            title = title_element.text.strip()
                            article_url = title_element.get_attribute("href")
                        except Exception as e:
                            print(f"Error extracting title: {e}")
                            title = "Title not found"
                            article_url = None

                        # Extract authors
                        try:
                            authors_element = article.find_element(By.CSS_SELECTOR, ".c-listing__authors-list")
                            authors = authors_element.text.strip()
                        except Exception as e:
                            print(f"Error extracting authors: {e}")
                            authors = "Authors not found"

                        # Extract publication date
                        try:
                            date_element = article.find_element(By.CSS_SELECTOR, "[itemprop='datePublished']")
                            publication_date = date_element.text.strip()
                        except Exception:
                            try:
                                date_info = article.find_element(By.CSS_SELECTOR, "[data-test='published-on']")
                                publication_date = date_info.text.replace("Published on: ", "").strip()
                            except Exception as e:
                                print(f"Error extracting publication date: {e}")
                                publication_date = "Date not found"

                        # Extract journal and citation info
                        try:
                            journal_element = article.find_element(By.CSS_SELECTOR, "[data-test='journal-title']")
                            journal = journal_element.text.strip()
                            
                            # Get citation info (year, volume, etc.)
                            citation_text = article.find_element(By.CSS_SELECTOR, "[data-test='teaser-citation']").text.strip()
                            # Clean up the citation text
                            citation_info = citation_text.replace(journal, "").strip()
                        except Exception as e:
                            print(f"Error extracting journal info: {e}")
                            journal = "BMC Medicine"
                            citation_info = "Citation not found"

                        # Extract content type (Article, Commentary, etc.)
                        try:
                            content_type = article.find_element(By.CSS_SELECTOR, "[data-test='result-list']").text.strip()
                        except Exception as e:
                            print(f"Error extracting content type: {e}")
                            content_type = "Type not found"

                        # Extract PDF URL
                        try:
                            pdf_link_element = article.find_element(By.CSS_SELECTOR, "[data-test='pdf-link']")
                            pdf_url = pdf_link_element.get_attribute("href")
                            
                            # For relative URLs, construct full URL
                            if pdf_url and pdf_url.startswith("/"):
                                base_url_domain = "https://bmcmedicine.biomedcentral.com"
                                pdf_url = base_url_domain + pdf_url
                        except Exception as e:
                            print(f"Error extracting PDF URL: {e}")
                            pdf_url = None

                        # Extract DOI
                        doi = None
                        if article_url and '/articles/' in article_url:
                            doi = article_url.split('/articles/')[1]

                        # Add all extracted data to articles_data list
                        articles_data.append({
                            "Title": title,
                            "Authors": authors,
                            "Publication Date": publication_date,
                            "Journal": journal,
                            "Citation Info": citation_info,
                            "Content Type": content_type,
                            "Article URL": article_url,
                            "PDF URL": pdf_url,
                            "DOI": doi,
                            "Page Number": page_num,
                            "Search Topic": topic.replace('+', ' ')
                        })
                        
                        print(f"Scraped: {title}")
                        
                    except Exception as e:
                        print(f"Error processing an article: {e}")
                
                # Add a delay between pages to avoid overloading the server
                if page_num < end_page:
                    print(f"Waiting before loading next page...")
                    time.sleep(3)  # 3-second delay
                    
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                if "no such element" in str(e).lower():
                    print("No more articles found. This might be the last page.")
                    break

        # After processing all pages for this topic
        if articles_data:
            # Convert the topic's data to a DataFrame
            topic_df = pd.DataFrame(articles_data)
            
            # Create a clean filename
            topic_filename = topic.replace('+', '_')
            csv_file_path = f"data/bmc_medicine_{topic_filename}_articles.csv"
            
            # Save the DataFrame to a CSV file
            topic_df.to_csv(csv_file_path, index=False, encoding='utf-8')
            
            print(f"\nScraping for topic '{topic.replace('+', ' ')}' completed!")
            print(f"Total articles scraped: {len(articles_data)}")
            print(f"Data saved to {csv_file_path}")
            
        else:
            print(f"\nNo articles were found for topic '{topic.replace('+', ' ')}'")

    except Exception as e:
        print(f"Critical error during scraping for topic '{topic.replace('+', ' ')}': {e}")

# After processing all topics, combine into one master CSV
try:
    print("\nCombining all topic data into one master CSV...")
    all_data = []
    
    for topic in topics:
        topic_filename = topic.replace('+', '_')
        csv_file_path = f"data/bmc_medicine_{topic_filename}_articles.csv"
        
        if os.path.exists(csv_file_path):
            topic_df = pd.read_csv(csv_file_path)
            all_data.append(topic_df)
    
    if all_data:
        # Combine all DataFrames
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save to master CSV
        master_csv_path = "data/bmc_medicine_all_topics.csv"
        combined_df.to_csv(master_csv_path, index=False, encoding='utf-8')
        
        print(f"Combined data from all topics saved to {master_csv_path}")
        print(f"Total articles: {len(combined_df)}")
    else:
        print("No data found to combine.")
        
except Exception as e:
    print(f"Error combining topic data: {e}")

finally:
    # Close browser after all scraping is complete
    driver.quit()

print("\nScript execution completed.")