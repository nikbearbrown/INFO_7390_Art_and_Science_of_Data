#!/usr/bin/env python3
"""
Simple wrapper script for the URL scraper with interactive prompts.
"""

import os
import asyncio
import subprocess
import sys
from url_scraper import collect_domain_urls, save_urls_to_file

async def interactive_scraper():
    """Run the URL scraper with interactive prompts."""
    print("=" * 50)
    print("Domain URL Scraper - Interactive Mode")
    print("=" * 50)
    
    # Get domain
    domain = input("Enter the domain to crawl (e.g., https://example.com): ")
    if not domain:
        print("Error: Domain is required.")
        return
        
    # Ensure domain starts with a scheme
    if not domain.startswith(('http://', 'https://')):
        domain = 'https://' + domain
    
    # Get optional parameters
    output_file = input("Enter output file path [default: urls.txt]: ") or "urls.txt"
    
    # Get depth with validation
    depth_str = input("Enter maximum crawl depth [default: 2]: ") or "2"
    try:
        depth = int(depth_str)
        if depth < 1:
            print("Depth must be at least 1. Using default value of 2.")
            depth = 2
    except ValueError:
        print("Invalid depth. Using default value of 2.")
        depth = 2
    
    # Get max pages with validation
    max_pages_str = input("Enter maximum number of pages to crawl [default: 100]: ") or "100"
    try:
        max_pages = int(max_pages_str)
        if max_pages < 1:
            print("Max pages must be at least 1. Using default value of 100.")
            max_pages = 100
    except ValueError:
        print("Invalid max pages. Using default value of 100.")
        max_pages = 100
    
    # Get strategy
    strategy = input("Enter crawling strategy (bfs/dfs) [default: bfs]: ").lower() or "bfs"
    if strategy not in ["bfs", "dfs"]:
        print("Invalid strategy. Using default value of bfs.")
        strategy = "bfs"
    
    print("\nStarting crawler with the following settings:")
    print(f"Domain: {domain}")
    print(f"Output file: {output_file}")
    print(f"Maximum depth: {depth}")
    print(f"Maximum pages: {max_pages}")
    print(f"Crawling strategy: {strategy}")
    print("-" * 50)
    
    try:
        # Collect unique URLs
        unique_urls = await collect_domain_urls(
            start_url=domain,
            max_depth=depth,
            max_pages=max_pages,
            crawl_strategy=strategy,
            remove_fragments=True
        )
        
        # Save URLs to file
        save_urls_to_file(unique_urls, output_file)
        
        print("\nCrawling complete!")
        print(f"Found {len(unique_urls)} unique URLs")
        print(f"Results saved to: {os.path.abspath(output_file)}")
        
        # Ask if the user wants to view the results
        view_results = input("\nWould you like to view the results? (y/n): ").lower()
        if view_results == 'y':
            try:
                # Try to use a pager if available
                if sys.platform == 'win32':
                    os.system(f"type {output_file}")
                else:
                    try:
                        subprocess.run(["less", output_file])
                    except FileNotFoundError:
                        with open(output_file, 'r') as f:
                            print(f.read())
            except Exception as e:
                print(f"Error displaying file: {str(e)}")
                with open(output_file, 'r') as f:
                    print(f.read())
                    
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
    except Exception as e:
        print(f"\nError during crawling: {str(e)}")
    
    print("\nThank you for using the Domain URL Scraper!")

if __name__ == "__main__":
    asyncio.run(interactive_scraper())
