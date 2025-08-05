# config.py - Configuration settings for the scraper

# Browser settings
HEADLESS_MODE = True
WINDOW_SIZE = "1920,1080"
PAGE_LOAD_TIMEOUT = 60
IMPLICIT_WAIT = 10

# Scraping settings
BASE_URL = "https://wineworld.lk"
WINE_CATEGORY_URL = "https://wineworld.lk/product-category/wines/page/{page}/"
MAX_PAGES = 500
MAX_RETRIES = 3
MAX_CONSECUTIVE_FAILURES = 5

# Delays (in seconds)
MIN_DELAY = 1
MAX_DELAY = 3
RETRY_DELAY_MIN = 2
RETRY_DELAY_MAX = 5

# File paths
UBLOCK_PATH = 'ublock_origin.xpi'
BACKUP_FILE_PATTERN = 'links_backup_page_{page}.txt'
LINKS_FILE = 'wine_links.txt'
FINAL_LINKS_JSON = 'wine_links_final.json'
CSV_OUTPUT_FILE = 'wine_products.csv'

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

# Error page indicators
ERROR_PAGE_INDICATORS = [
    'error404',
    'experience the finest selection',
    'featured products',
    'shop by brand',
    'best sellers',
    'featured collections',
    'stay in touch',
    'as sri lanka\'s premier destination',
    'sparkling & champagne collection',
    'beer collection',
    'explore our most popular brands'
]

# CSS selectors for finding products (in order of preference)
PRODUCT_SELECTORS = [
    "//ul[@class='products column-3']/li",  # XPath
    ".products li",
    
]
#selectors for the product's name
PRODUCT_TITLE_SELECTORS=[
    "h1.product_title",
    ".product_title",
    "div.summary.entry-summary > h1",
    
]
#xpath & css selectors for product's price
PRODUCT_PRICE_SELECTORS=[
                      "p.price bdi",
                      "div.summary p.price bdi",
                      "div.breadcrumb-wrapper + h1 + p bdi",
                      "//p[@class='price']//bdi",
                        ]
#xpath or css selectors for short description about the product
PRODUCT_DESC_SELECTORS=[
   "//div[contains(@class,'short-description')]/p",
   "//div[contains(@class,'woocommerce-product-details__short-description')]/p",
   "p.price + div p",
   "div[class*='short-description'] p",
]
PRODUCT_COUNTRY_SELECTORS=[
                           "tr.woocommerce-product-attributes-item--attribute_pa_country td.woocommerce-product-attributes-item__value",
                           "tr.woocommerce-product-attributes-item--attribute_pa_country td",
                           "table.woocommerce-product-attributes tr:nth-child(4) td",
]
PRODUCT_WEIGHT_SELECTORS=[
                         "tr.woocommerce-product-attributes-item--weight td.woocommerce-product-attributes-item__value",
                         "tr.woocommerce-product-attributes-item--weight td",
                         "table.woocommerce-product-attributes tr:nth-child(1) td",
]
PRODUCT_SIZE_SELECTORS= [
           "table.woocommerce-product-attributes th:contains('Size') + td",
           "tr.woocommerce-product-attributes-item--attribute_pa_size td.woocommerce-product-attributes-item__value",
           "table.woocommerce-product-attributes tr:nth-child(2) td",
]
PRODUCT_CAT_SELECTORS = [
    "tr.woocommerce-product-attributes-item--attribute_pa_ww-category td.woocommerce-product-attributes-item__value",
    "tr.woocommerce-product-attributes-item--attribute_pa_ww-category td",
    "table.woocommerce-product-attributes tr:nth-child(3) td",
    "tr.woocommerce-product-attributes-item--attribute_pa_ww-category td p",
    "table.woocommerce-product-attributes tbody tr:nth-child(3) td",
    "tr[class*='ww-category'] td",
    "table.shop_attributes tr:nth-child(3) td"
]
# Link selectors
LINK_SELECTORS = [
    "a",
    "a[href*='product']",
    
]

# Firefox preferences
FIREFOX_PREFERENCES = {
    "permissions.default.image": 2,  # Disable images
    "dom.ipc.plugins.enabled.libflashplayer.so": False,
    "media.autoplay.default": 5,
    "media.autoplay.enabled.user-gesture-needed": False,
    "media.autoplay.blocking_policy": 2,
    "network.http.connection-timeout": 60,
    "network.http.connection-retry-timeout": 30,
}

# Firefox arguments
FIREFOX_ARGUMENTS = [
    #"--headless",
    "--no-sandbox", 
    "--disable-dev-shm-usage",
    "--disable-gpu",
    f"--window-size={WINDOW_SIZE}",
    "--disable-popup-blocking",
    "--start-maximized",
    "--disable-extensions"
]

# Requests headers
REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'