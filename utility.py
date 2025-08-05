# utility.py - Utility functions for web scraping

import logging
import random
import time
import requests
import json
import csv
from typing import Dict, List
from urllib.parse import urljoin
from dataclasses import dataclass

# Import all required modules
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, 
    TimeoutException, 
    WebDriverException,
    InvalidSessionIdException
)

from urllib3.exceptions import ReadTimeoutError

from config import *

@dataclass
class PropertyListing:
    """Data class for property listing information"""
    title: str
    price: str
    category: str
    origin: str
    size: str
    weight: str
    description: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV writing"""
        return {
            'Title': self.title,
            'Price': self.price,
            'Description': self.description,
            'Origin': self.origin,  
            'Weight': self.weight,
            'Size': self.size,
            'Category': self.category
        }


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )
    return logging.getLogger(__name__)

def get_random_user_agent() -> str:
    """Get a random user agent from the configured list"""
    return random.choice(USER_AGENTS)

def random_delay(min_seconds: float = MIN_DELAY, max_seconds: float = MAX_DELAY):
    """Sleep for a random amount of time between min and max seconds"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def save_links_to_file(links: List[str], filename: str):
    """Save links to a text file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for link in links:
                f.write(link + '\n')
        return True
    except Exception as e:
        logging.error(f"Error saving links to {filename}: {e}")
        return False

def load_links_from_file(filename: str) -> List[str]:
    """Load links from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Error loading links from {filename}: {e}")
        return []

# FIXED: Removed the 'self' parameter from this utility function and added logger
def save_to_csv(results: List[PropertyListing], filename: str) -> bool:
    """
    Save property listings to CSV file
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if not results:
                logger.warning("No properties to save")
                return False
                
            fieldnames = ['Title','Price','Description','Origin','Weight','Size','Category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow(result.to_dict())
        
        logger.info(f"Successfully saved {len(results)} properties to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
        return False

def is_valid_product_url(url: str, base_url: str = BASE_URL) -> bool:
    """Check if URL is a valid product URL"""
    if not url:
        return False
    
    # Convert relative URLs to absolute
    if url.startswith('/'):
        url = urljoin(base_url, url)
    
    return 'product' in url.lower() and base_url in url

def remove_duplicates(links: List[str]) -> List[str]:
    """Remove duplicate links while preserving order"""
    seen = set()
    unique_links = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    return unique_links

def retry_on_failure(max_retries: int = MAX_RETRIES, delay_range: tuple = (RETRY_DELAY_MIN, RETRY_DELAY_MAX)):
    """Decorator for retrying functions on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(__name__)
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        delay = random.uniform(*delay_range)
                        logger.info(f"Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        raise e
        return wrapper
    return decorator

def create_session() -> requests.Session:
    """Create a configured requests session"""
    session = requests.Session()
    headers = REQUEST_HEADERS.copy()
    headers['User-Agent'] = get_random_user_agent()
    session.headers.update(headers)
    session.timeout = PAGE_LOAD_TIMEOUT
    return session

def check_error_page(content: str, indicators: List[str] = ERROR_PAGE_INDICATORS) -> bool:
    """Check if page content indicates an error/404 page"""
    if not content:
        return True
    
    content_lower = content.lower()
    return any(indicator.lower() in content_lower for indicator in indicators)

def format_progress_message(current_page: int, total_links: int, page_links: int = 0) -> str:
    """Format a progress message"""
    if page_links:
        return f"Page {current_page}: Found {page_links} links | Total: {total_links} links"
    else:
        return f"Progress: Page {current_page} | Total links collected: {total_links}"

def calculate_stats(links: List[str]) -> dict:
    """Calculate statistics about collected links"""
    unique_links = remove_duplicates(links)
    return {
        'total_links': len(links),
        'unique_links': len(unique_links),
        'duplicates': len(links) - len(unique_links),
        'duplicate_percentage': ((len(links) - len(unique_links)) / len(links) * 100) if links else 0
    }

SIZE_KEYWORDS = {
    '180ML': ['180', '180ml'],
    '375ML': ['375', '375ml'],
    '700ML': ['700', '700ml'],
    '750ML': ['750', '750ml'],
    '1500ML': ['1500', '1500ml'],
}

def get_size_from_title(title):
    """
    Infers the size from a product title using a keyword dictionary.
    """
    if not title:
        return "Unspecified"
        
    title_lower = title.lower()
    for size, keywords in SIZE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return size  
    return "Unspecified"

# You might want to add more wine-specific terms
cat_keywords = {
    'White Wine': ['blanc', 'chardonnay', 'moscato', 'gewürztraminer', 'verdejo', 'blanco', 'white', 
                   'sauvignon blanc', 'pinot grigio', 'riesling', 'albariño', 'viognier'],
    'Red Wine': ['merlot', 'red', 'malbec', 'cabernet', 'rosso', 'pinot noir', 'shiraz', 'syrah', 
                 'tempranillo', 'sangiovese', 'grenache', 'zinfandel'],
    'Rose Wine': ['rosé', 'rosado', 'rosato', 'pink', 'blush'],
    'Sparkling Wine': ['champagne', 'prosecco', 'cava', 'asti', 'crémant', 'sparkling', 'spumante', 
                       'sekt', 'franciacorta'],
    'Fortified Wine': ['port', 'sherry', 'madeira', 'marsala', 'porto']
}

def get_cat_from_title(title):
    """
    Infers the category from a product title using a keyword dictionary.
    """
    if not title:
        return "Uncategorized"
        
    title_lower = title.lower()
    for category, keywords in cat_keywords.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category  
    return "Uncategorized"

def get_cat_from_desc(description):
    """
    Infers the category from product short description
    """
    if not description:
        return "Uncategorized"
        
    desc_lower = description.lower()  
    for category, keywords in cat_keywords.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return "Uncategorized"  # Added return for no match