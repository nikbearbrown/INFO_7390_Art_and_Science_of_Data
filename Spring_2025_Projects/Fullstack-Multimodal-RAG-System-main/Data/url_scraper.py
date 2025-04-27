import asyncio
import os
import argparse
from urllib.parse import urlparse, urljoin, urldefrag
from typing import Set, List, Dict
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy

def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing fragments and trailing slashes.
    
    Args:
        url: The URL to normalize
        
    Returns:
        The normalized URL
    """
    # Remove fragment identifier (#)
    url_without_fragment = urldefrag(url)[0]
    
    # Remove trailing slash if present, except for domain root
    if url_without_fragment.endswith('/'):
        parsed = urlparse(url_without_fragment)
        # Keep trailing slash only for domain root (path is empty or '/')
        if parsed.path and parsed.path != '/':
            return url_without_fragment[:-1]
    
    return url_without_fragment

async def collect_domain_urls(start_url: str, max_depth: int = 2, max_pages: int = 100, 
                              crawl_strategy: str = "bfs", 
                              remove_fragments: bool = True) -> Set[str]:
    """
    Collect all unique URLs within a domain.
    
    Args:
        start_url: The starting URL to crawl from
        max_depth: Maximum crawl depth
        max_pages: Maximum number of pages to crawl
        crawl_strategy: The crawling strategy, either "bfs" or "dfs"
        
    Returns:
        A set of unique URLs within the domain
    """
    # Normalize the starting URL
    start_url = normalize_url(start_url)
    
    # Parse domain from URL to ensure we stay within the same domain
    domain = urlparse(start_url).netloc
    print(f"Starting crawl of domain: {domain}")
    
    # Setup browser configuration
    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )
    
    # Choose the appropriate crawl strategy
    if crawl_strategy.lower() == "dfs":
        deep_crawl_strategy = DFSDeepCrawlStrategy(
            max_depth=max_depth,
            max_pages=max_pages,
            include_external=False            
        )
    else:  # Default to BFS
        deep_crawl_strategy = BFSDeepCrawlStrategy(
            max_depth=max_depth,
            max_pages=max_pages,
            include_external=False
            
        )
    
    # Setup crawler run configuration with minimal processing since we only care about links
    crawler_config = CrawlerRunConfig(
        deep_crawl_strategy=deep_crawl_strategy,
        cache_mode=CacheMode.ENABLED,
        stream=True,  # Enable streaming for processing results as they arrive
        verbose=True
    )
    
    # Container for unique URLs
    unique_urls = set()
    unique_urls.add(start_url)  # Add the starting URL
    
    # Initialize the crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            # Start the crawl with streaming enabled to process results as they come in
            stream = await crawler.arun(start_url, config=crawler_config)
            
            async for result in stream:
                if result.success:
                    # Add the current URL (normalized)
                    unique_urls.add(normalize_url(result.url))
                    
                    # Process all links found on the page
                    if result.links:
                        internal_links = result.links.get("internal", [])
                        for link_data in internal_links:
                            # Only add URLs from the same domain
                            if 'href' in link_data and link_data['href']:
                                # Join relative URLs with base URL
                                full_url = urljoin(result.url, link_data['href'])
                                
                                # Only add URLs from the same domain
                                if urlparse(full_url).netloc == domain:
                                    # Normalize URL before adding
                                    normalized_url = normalize_url(full_url)
                                    unique_urls.add(normalized_url)
                    
                    # Print progress
                    print(f"Processed: {result.url} - Found {len(unique_urls)} unique URLs so far")
                else:
                    print(f"Failed to crawl: {result.url} - {result.error_message}")
        except Exception as e:
            print(f"Error during crawling: {str(e)}")
    
    return unique_urls

def save_urls_to_file(urls: Set[str], output_file: str):
    """
    Save a set of URLs to a file, one URL per line.
    
    Args:
        urls: Set of URLs to save
        output_file: Path to the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in sorted(urls):
            f.write(f"{url}\n")
    
    print(f"Saved {len(urls)} unique URLs to {output_file}")

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Collect all unique URLs within a domain.')
    parser.add_argument('domain', help='The domain to crawl (e.g., https://example.com)')
    parser.add_argument('--output', '-o', default='urls.txt', 
                        help='Output file path (default: urls.txt)')
    parser.add_argument('--depth', '-d', type=int, default=2, 
                        help='Maximum crawl depth (default: 2)')
    parser.add_argument('--max-pages', '-m', type=int, default=100, 
                        help='Maximum number of pages to crawl (default: 100)')
    parser.add_argument('--strategy', '-s', choices=['bfs', 'dfs'], default='bfs',
                        help='Crawling strategy: breadth-first (bfs) or depth-first (dfs) (default: bfs)')
    
    args = parser.parse_args()
    
    # Ensure domain starts with a scheme (http:// or https://)
    if not args.domain.startswith(('http://', 'https://')):
        args.domain = 'https://' + args.domain
    
    try:
        # Collect unique URLs
        unique_urls = await collect_domain_urls(
            start_url=args.domain,
            max_depth=args.depth,
            max_pages=args.max_pages,
            crawl_strategy=args.strategy,
            remove_fragments=True
        )
        
        # Save URLs to file
        save_urls_to_file(unique_urls, args.output)
        
        print(f"Completed crawling of {args.domain}")
        print(f"Found {len(unique_urls)} unique URLs (depth: {args.depth}, max pages: {args.max_pages})")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
