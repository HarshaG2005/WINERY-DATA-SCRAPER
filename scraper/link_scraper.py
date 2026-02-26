from imports import *
from config import *
from utility import *
from base_scraper import BaseScraper

class LinkScraper(BaseScraper):
    def __init__(self,max_pages_limit=None):
        super().__init__(max_pages_limit)
        
        
    

    def handle_age_verification(self) -> bool:
        """Handle age verification popup if present"""
        try:
            age_verification_button = self.long_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.age-gate__submit.age-gate__submit--yes"))
            )
            self.driver.execute_script("arguments[0].click();", age_verification_button)
            self.logger.info("Age verification passed")
            time.sleep(random.uniform(1, 2))
            return True
        except TimeoutException:
            self.logger.info("No age verification popup found")
            return True  # Not an error if popup doesn't exist
        except Exception as e:
            self.logger.warning(f"Error handling age verification: {e}")
            return False

    def handle_promotional_popup(self) -> bool:
        """Handle promotional popup if present"""
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pum-close.popmake-close"))
            )
            self.driver.execute_script("arguments[0].click();", close_button)
            self.logger.info("Promotional popup closed")
            time.sleep(random.uniform(1, 2))
            return True
        except TimeoutException:
            self.logger.info("No promotional popup found")
            return True  # Not an error if popup doesn't exist
        except Exception as e:
            self.logger.warning(f"Error handling promotional popup: {e}")
            return False

    def navigate_to_wine_section(self) -> bool:
        """Navigate to the wine section"""
        try:
            wine_section = self.long_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='https://wineworld.lk/product-category/wines/']"))
            )
            self.driver.execute_script("arguments[0].click();", wine_section)
            self.logger.info("Successfully navigated to wine section")
            time.sleep(random.uniform(2, 3))
            return True
        except TimeoutException:
            self.logger.error("Timeout: Wine section link not found")
            return False
        except Exception as e:
            self.logger.error(f"Error navigating to wine section: {e}")
            return False

    def extract_product_links(self) -> List[str]:
        """Extract product links from current page"""
        links = []

        try:
            # Try different selectors to find product items
            items = []
            for selector in PRODUCT_SELECTORS:
                try:
                    if selector.startswith('//'):   # XPath
                        items = self.driver.find_elements(By.XPATH, selector)
                    else:   # CSS selector
                        items = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    if items:
                        self.logger.debug(f"Found {len(items)} items using selector: {selector}")
                        break
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue

            if not items:
                self.logger.warning("No product items found with any selector")
                return links

            # Extract links from items
            for item in items:
                try:
                    link_element = None

                    # Try different ways to find the link within each item
                    for link_selector in LINK_SELECTORS:
                        try:
                            if link_selector == "a":
                                link_element = item.find_element(By.TAG_NAME, "a")
                            else:
                                link_element = item.find_element(By.CSS_SELECTOR, link_selector)
                            break
                        except NoSuchElementException:
                            continue

                    if link_element:
                        href = link_element.get_attribute("href")
                        if is_valid_product_url(href):
                            links.append(href)
                            self.logger.debug(f"Extracted link: {href}")

                except Exception as e:
                    self.logger.debug(f"Error extracting link from item: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Error in extract_product_links: {e}")

        return links

    def click_next_page(self) -> bool:
        """Click the next page button"""
        try:
            # Wait a bit before looking for next button
            time.sleep(random.uniform(1, 2))
            
            # Look for next button with multiple possible selectors
            next_selectors = [
                "//a[@class='next page-numbers']",
                "//a[contains(@class, 'next')]",
                ".next.page-numbers",
                "a.next",
                "[rel='next']"
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    if selector.startswith('//'):  # XPath
                        next_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:  # CSS selector
                        next_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    self.logger.debug(f"Found next button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not next_button:
                self.logger.info("No next button found - reached end of pagination")
                return False
            
            # Click the next button
            self.driver.execute_script("arguments[0].click();", next_button)
            self.logger.info(f"Clicked next button, moving to page {self.current_page + 1}")
            
            # Wait for new page to load
            time.sleep(random.uniform(2, 4))
            
            return True
            
        except TimeoutException:
            self.logger.info("Next button not found - end of pagination")
            return False
        except Exception as e:
            self.logger.warning(f"Error clicking next page: {e}")
            return False

    def save_progress(self, all_links: List[str]) -> None:
        """Save current progress to backup file - DISABLED"""
        # Backup functionality disabled as requested
        pass

    def quit_driver(self):
        """Safely quit the driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver closed successfully")
            except Exception as e:
                self.logger.warning(f"Error closing driver: {e}")
            finally:
                self.driver = None
                self.wait = None
                self.long_wait = None

    def scrape_all_pages(self) -> List[str]:
        """
        Main scraping method - uses click next button pagination
        """
        all_links = []
        
        try:
            # Step 1: Initialize and load base page
            self.logger.info("Starting wine scraping process...")
            
            if not self.load_page(BASE_URL):
                self.logger.error("Failed to load base page")
                return all_links

            # Step 2: Handle popups and navigation
            if not self.handle_age_verification():
                self.logger.error("Failed to handle age verification")
                return all_links

            if not self.handle_promotional_popup():
                self.logger.error("Failed to handle promotional popup")
                return all_links

            if not self.navigate_to_wine_section():
                self.logger.error("Failed to navigate to wine section")
                return all_links

            # Step 3: Start pagination loop
            self.logger.info("Starting pagination...")
            
            
            while self.current_page <= self.max_pages_limit:
                try:
                    self.logger.info(f"Scraping page {self.current_page}...")
                    
                    # Extract links from current page
                    page_links = self.extract_product_links()
                    
                    if not page_links:
                        self.logger.warning(f"No links found on page {self.current_page}")
                        # Still try to go to next page in case it's a temporary issue
                    else:
                        all_links.extend(page_links)
                        self.total_links = len(all_links)
                        self.logger.info(f"Page {self.current_page}: Found {len(page_links)} links. Total: {self.total_links}")

                    # No backup saves - removed as requested

                    # Try to go to next page
                    if not self.click_next_page():
                        self.logger.info("No more pages available. Scraping complete.")
                        break

                    # Update page counter
                    self.current_page += 1

                except Exception as e:
                    self.logger.error(f"Error on page {self.current_page}: {e}")
                    # Try to continue to next page
                    if not self.click_next_page():
                        break
                    self.current_page += 1

            # Final save
            if all_links:
                final_filename = f"wine_links_final_{len(all_links)}_links.txt"
                save_links_to_file(all_links, final_filename)
                self.logger.info(f"Final results saved to {final_filename}")

        except KeyboardInterrupt:
            self.logger.info("Scraping interrupted by user")
            # No backup save on interrupt - removed as requested
                
        except Exception as e:
            self.logger.error(f"Unexpected error in scrape_all_pages: {e}")
            
        finally:
            self.quit_driver()
            self.logger.info(f"Scraping finished. Total links collected: {len(all_links)}")

        return all_links


# Usage example:
if __name__ == "__main__":
    # Create scraper with max 50 pages limit
    scraper = SeleniumScraper(max_pages_limit=50)
    
    # Start scraping
    links = scraper.scrape_all_pages()
    
    print(f"Scraping completed. Found {len(links)} product links.")