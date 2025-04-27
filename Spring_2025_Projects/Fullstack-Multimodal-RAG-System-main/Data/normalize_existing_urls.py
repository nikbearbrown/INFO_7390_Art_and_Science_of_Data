#!/usr/bin/env python3
"""
Script to normalize and deduplicate an existing list of URLs.
Use this to clean up a previously scraped URL list.
"""

import sys
from url_scraper import normalize_url

def normalize_url_file(input_file, output_file=None):
    """
    Read URLs from a file, normalize them, and save the unique URLs to a new file.
    
    Args:
        input_file: Path to the input file containing URLs (one per line)
        output_file: Path to the output file (defaults to input_file + '.normalized.txt')
    """
    if output_file is None:
        output_file = input_file + '.normalized.txt'
    
    try:
        # Read URLs from input file
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        print(f"Read {len(urls)} URLs from {input_file}")
        
        # Normalize URLs and remove duplicates
        normalized_urls = set()
        for url in urls:
            normalized_urls.add(normalize_url(url))
        
        # Sort URLs for better readability
        sorted_urls = sorted(normalized_urls)
        
        # Save normalized URLs to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for url in sorted_urls:
                f.write(f"{url}\n")
        
        print(f"Normalized and saved {len(sorted_urls)} unique URLs to {output_file}")
        print(f"Removed {len(urls) - len(sorted_urls)} duplicate URLs")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python normalize_existing_urls.py input_file [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if normalize_url_file(input_file, output_file):
        print("URL normalization completed successfully.")
    else:
        print("URL normalization failed.")
        sys.exit(1)
