# base_scraper.py
from utility import *
from config import *
from imports import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BaseScraper:
    def __init__(self,max_pages_limit=None):
        self.driver = None
        self.wait=None
        self.logger=setup_logging()
        self.current_page=1
        self.max_pages_limit = max_pages_limit if max_pages_limit is not None else MAX_PAGES
        self.total_links = 0   # Track total links found

        
    
    def create_driver(self):
        """Create and configure Firefox driver"""
        try:
            service = FirefoxService(executable_path=GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()

            # Add arguments
            for arg in FIREFOX_ARGUMENTS:
                options.add_argument(arg)

            # Set preferences
            for pref_key, pref_value in FIREFOX_PREFERENCES.items():
                options.set_preference(pref_key, pref_value)

            # Set random user agent
            options.set_preference("general.useragent.override", get_random_user_agent())

            # Create driver
            self.driver = webdriver.Firefox(service=service, options=options)

            # Set timeouts
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(IMPLICIT_WAIT)

            # Create wait objects
            self.wait = WebDriverWait(self.driver, 5)
            self.long_wait = WebDriverWait(self.driver, 20)

            # Try to install adblocker
            self._install_adblocker()

            self.logger.info("Firefox driver created successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create driver: {e}")
            return False

    def _install_adblocker(self):
        """Try to install uBlock Origin addon"""
        try:
            self.driver.install_addon(UBLOCK_PATH, temporary=True)
            self.logger.info("uBlock Origin installed")
        except Exception as e:
            self.logger.warning(f"Could not install adblocker: {e}")

    @retry_on_failure()
    def load_page(self, url: str) -> bool:
        """Load a page with retry logic"""
        if not self.driver:
            if not self.create_driver():
                return False

        try:
            self.logger.info(f"Loading: {url}")
            self.driver.get(url)

            # Wait for page to load
            self.long_wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Random delay
            random_delay()

            return True

        except TimeoutException:
            self.logger.warning(f"Timeout loading {url}")
            raise
        except WebDriverException as e:
            self.logger.warning(f"WebDriver error: {e}")
            # Try to recreate driver
            self.quit_driver()
            if not self.create_driver():
                raise
            raise
    
    