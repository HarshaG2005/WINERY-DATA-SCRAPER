from imports import *
from config import *
from utility import *
from base_scraper import BaseScraper
import csv

class DataScraper(BaseScraper):
    def __init__(self):
        super().__init__()
    
    def extract_product_title(self):
        """Extract product name/title"""
        title = None  # Initialize variable
        try:
            for selector in PRODUCT_TITLE_SELECTORS:
                try:
                    if selector.startswith('//'):   # XPath
                        title = self.wait.until(EC.presence_of_element_located((By.XPATH, selector))).text
                    else:   # CSS selector
                        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text

                    if title:
                        return title.strip()  # Return immediately when found
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue

            if not title:
                self.logger.warning("No title found with any selector")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in extract_product_title: {e}")
            return None
    
    def extract_product_price(self):
        """Extract product price"""
        price = None  # Initialize variable
        try:
            for selector in PRODUCT_PRICE_SELECTORS:
                try:
                    if selector.startswith("//"):
                        # FIXED: Typo 'presnece_of_element_located' -> 'presence_of_element_located'
                        price = self.wait.until(EC.presence_of_element_located((By.XPATH, selector))).text
                    else:
                        price = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    
                    if price:  # Fixed: was checking 'title' instead of 'price'
                        return price.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            if not price:
                self.logger.warning("No price found with any selector")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in extract_product_price: {e}")
            return None
    
    def extract_product_description(self):
        """Extract the short description about the product"""
        description = None  # Initialize variable
        try:
            for selector in PRODUCT_DESC_SELECTORS:
                try:
                    if selector.startswith("//"):
                        description = self.wait.until(EC.presence_of_element_located((By.XPATH, selector))).text
                    else:
                        description = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    
                    if description:
                        return description.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            if not description:
                self.logger.warning("No description found with any selector")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in extract_product_description: {e}")
            return None
    
    def extract_product_weight(self):
        """Extract product weight (kg)"""
        weight = None  # Initialize variable
        try:
            for selector in PRODUCT_WEIGHT_SELECTORS:
                try:
                    # FIXED: Missing 'until' method call
                    weight = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    if weight:
                        return weight.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            # If no weight found, return default
            return "-"
            
        except Exception as e:
            self.logger.error(f"Error in extract_product_weight: {e}")
            return "-"
    
    def extract_product_country(self):
        """Extract the origin country"""
        origin = None  # Initialize variable
        try:
            for selector in PRODUCT_COUNTRY_SELECTORS:
                try:
                    origin = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    if origin:
                        return origin.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            # If no origin found, return default
            return "-"
            
        except Exception as e:
            self.logger.error(f"Error in extract_product_country: {e}")
            return "-"
    
    def extract_product_size(self):
        """Extract product size in ML"""
        size = None  # Initialize variable
        try:
            for selector in PRODUCT_SIZE_SELECTORS:
                try:
                    # FIXED: Missing 'located' in method name
                    size = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    if size:
                        return size.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            # Fallback: try to extract from title
            title = self.extract_product_title()  # Get title first
            if title:
                size = get_size_from_title(title)
                return size
            
            return "Unspecified"
            
        except Exception as e:
            self.logger.error(f"Error in extract_product_size: {e}")
            return "Unspecified"
    
    def extract_product_category(self):
        """Extract product category"""
        category = None  # Initialize variable
        try:
            # First try direct selectors
            for selector in PRODUCT_CAT_SELECTORS:
                try:
                    category = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))).text
                    if category:
                        return category.strip()
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # FIXED: Use self.extract_product_title() instead of extract_product_title()
            # Fallback 1: Try to get from title
            title = self.extract_product_title()
            if title:
                category = get_cat_from_title(title)
                if category != "Uncategorized":
                    return category
            
            # Fallback 2: Try to get from description
            description = self.extract_product_description()
            if description:
                category = get_cat_from_desc(description)
                if category != "Uncategorized":
                    return category
            
            return "Uncategorized"
            
        except Exception as e:
            self.logger.error(f"Error in extract_product_category: {e}")
            return "Uncategorized"
    
    def scrape_product_data(self, url):
        """Main method to scrape all product data from a URL"""
        try:
            # Load the page
            if not self.load_page(url):
                return None
            
            # Extract all data
            title = self.extract_product_title()
            price = self.extract_product_price()
            description = self.extract_product_description()
            origin = self.extract_product_country()
            weight = self.extract_product_weight()
            size = self.extract_product_size()
            category = self.extract_product_category()
            
            # Create PropertyListing object
            listing = PropertyListing(
                title=title or "N/A",
                price=price or "N/A", 
                category=category or "Uncategorized",
                origin=origin or "-",
                size=size or "Unspecified",
                weight=weight or "-",
                description=description or "N/A"
            )
            
            self.logger.info(f"Successfully scraped: {title}")
            return listing
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def save_to_csv(self, results: List[PropertyListing], filename: str) -> bool:
        """
        Save property listings to CSV file
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not results:
                    self.logger.warning("No properties to save")
                    return False
                    
                fieldnames = ['Title','Price','Description','Origin','Weight','Size','Category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in results:
                    writer.writerow(result.to_dict())
                
            self.logger.info(f"Successfully saved {len(results)} properties to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
            return False
    
    def scrape_multiple_products(self, urls=None):
        """Scrape multiple product URLs"""
        results = []
        
        # FIXED: Load URLs properly
        if urls is None:
            urls = load_links_from_file(LINKS_FILE)  # Use the config variable, not hardcoded filename
        
        if not urls:
            self.logger.error("No URLs to scrape!")
            return []
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Scraping product {i}/{len(urls)}: {url}")
            
            listing = self.scrape_product_data(url)
            if listing:
                results.append(listing)
            
            # Add delay between requests
            random_delay()
        
        # FIXED: Save CSV results if we have data
        if results:
            # FIXED: Define CSV_OUTPUT_FILE or use a default filename
            csv_filename = "wine_products.csv"
            if self.save_to_csv(results, csv_filename):
                self.logger.info(f"Scraping completed. {len(results)} properties saved to {csv_filename}.")
            return results
        else:
            self.logger.warning('Data scraping unsuccessful!')
            return []

if __name__ == "__main__":
    # Create scraper
    scraper = DataScraper()
    
    # Start scraping
    results = scraper.scrape_multiple_products()
    
    print(f"Scraping completed. Found {len(results)} product data entries.")