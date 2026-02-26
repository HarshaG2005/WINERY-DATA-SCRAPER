# main.py - Main scraper script

import argparse
import sys
from config import * # This imports MAX_PAGES and other config variables
from utility import * 
from link_scraper import LinkScraper
from data_scraper import DataScraper
from imports import *


def main():
    """Main function to run the scraper"""

    parser = argparse.ArgumentParser(description='Wine World Scraper')

    parser.add_argument(
        '--method',
        choices=['requests', 'selenium'], 
        default='selenium', 
        help='Scraping method to use (default: selenium)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=MAX_PAGES, 
        help=f'Maximum pages to scrape (default: {MAX_PAGES})'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run a quick test to check if the site is accessible'
    )
    parser.add_argument(
        '--resume',
        type=str,
        help='Resume from a backup file (provide the backup file path)'
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging()
    logger.info("Starting Wine World Scraper")

    # Handle resume option
    existing_links = []
    if args.resume:
        existing_links = load_links_from_file(args.resume)
        logger.info(f"Resuming with {len(existing_links)} existing links")

    # Handle test option
    if args.test:
        run_quick_test() 
        return

    # Run scraper based on method
    all_links = []

    if args.method == 'requests':
        all_links = run_requests_scraper(max_pages_limit=args.max_pages)
    else: # selenium method
        all_links = run_selenium_scraper(max_pages_limit=args.max_pages) 

    # Combine with existing links if resuming
    if existing_links:
        all_links = existing_links + all_links

    # Process and save results
    if all_links:
        process_and_save_results(all_links)
        
        # FIXED: Now run data scraping after link scraping is complete
        logger.info("Starting data scraping phase...")
        data_scraper = DataScraper()
        scraped_data = data_scraper.scrape_multiple_products()
        
        if scraped_data:
            logger.info(f"Data scraping completed successfully! {len(scraped_data)} products scraped.")
        else:
            logger.warning("Data scraping completed but no data was collected.")
            
    else:
        logger.error("No links were collected!")
        sys.exit(1)

def run_quick_test():
    """Run a quick test to check site accessibility"""
    logger = setup_logging()
    logger.info("Running quick test...")

    try:
        session = create_session()
        response = session.get(BASE_URL + "/product-category/wines/", timeout=30)

        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Length: {len(response.text)}")

        if response.status_code == 200:
            links = parse_html_for_links(response.text)
            logger.info(f"Found {len(links)} product links")

            if links:
                logger.info("Site is accessible with requests method")
                logger.info("Sample links:")
                for i, link in enumerate(links[:3]):
                    logger.info(f"   {i+1}. {link}")
            else:
                logger.warning(" No product links found - might need Selenium")
        else:
            logger.error(f" Site returned HTTP {response.status_code}")

    except Exception as e:
        logger.error(f" Test failed: {e}")

def run_requests_scraper(max_pages_limit: int):
    """Run the requests-based scraper"""
    logger = setup_logging()
    logger.info("Using requests-based scraper")

    scraper = RequestsScraper(max_pages_limit=max_pages_limit)
    return scraper.scrape_all_pages()

def run_selenium_scraper(max_pages_limit: int):
    """Run the selenium-based scraper"""
    logger = setup_logging()
    logger.info("Using Selenium-based scraper")

    # FIXED: Correct class name and proper flow
    link_scraper = LinkScraper(max_pages_limit=max_pages_limit)
    all_links = link_scraper.scrape_all_pages()
    
    # Return only the links - data scraping will be handled in main()
    return all_links

def process_and_save_results(all_links):
    """Process and save the final results"""
    logger = setup_logging()
    
    # Remove duplicates while preserving order
    unique_links = list(dict.fromkeys(all_links))
    
    # Calculate statistics
    total_links = len(all_links)
    unique_count = len(unique_links)
    duplicates = total_links - unique_count
    duplicate_percentage = (duplicates / total_links * 100) if total_links > 0 else 0
    
    # Log results
    logger.info("=== LINK SCRAPING RESULTS ===")
    logger.info(f"Total links found: {total_links}")
    logger.info(f"Unique links: {unique_count}")
    logger.info(f"Duplicates removed: {duplicates}")
    logger.info(f"Duplicate percentage: {duplicate_percentage:.1f}%")
    
    # Save to text file only (no JSON)
    if save_links_to_file(unique_links, LINKS_FILE):
        logger.info(f"Links saved to {LINKS_FILE}")
    else:
        logger.error(f"Failed to save links to {LINKS_FILE}")
    
    return unique_links

def save_links_to_json(links, filename):
    """Save links to JSON file"""
    import json
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_links": len(links),
            "links": links
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

if __name__ == "__main__":

    main()
