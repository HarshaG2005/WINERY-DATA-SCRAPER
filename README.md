# Wine World Scraper 🍷

A comprehensive web scraper built with Selenium and Python to extract wine product information from Wine World Sri Lanka. This scraper efficiently collects product links and detailed product data including prices, descriptions, origins, and specifications.

## ✨ Features

- **Dual-Phase Scraping**: Separate link collection and data extraction phases
- **Robust Architecture**: Object-oriented design with clear separation of concerns
- **Multiple Fallback Selectors**: Ensures high success rate even with dynamic content
- **Popup Handling**: Automatically handles age verification and promotional popups
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Data Export**: Exports scraped data to CSV format
- **Error Recovery**: Retry mechanisms and graceful error handling
- **Configurable Limits**: Customizable page limits and scraping parameters


## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Firefox browser installed
- Internet connection

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HarshaG2005/wine-world-scraper.git
   cd wine-world-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper:**
   ```bash
   python main.py
   ```

## 📋 Requirements

Create a `requirements.txt` file with these dependencies:

```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 🔧 Configuration

Key settings in `config.py`:

```python
# Scraping limits
MAX_PAGES = 500                    # Maximum pages to scrape
PAGE_LOAD_TIMEOUT = 60            # Page load timeout in seconds

# Delays (anti-detection)
MIN_DELAY = 1                     # Minimum delay between requests
MAX_DELAY = 3                     # Maximum delay between requests

# Output files
CSV_OUTPUT_FILE = 'wine_products.csv'
LINKS_FILE = 'wine_links.txt'
```

## 🎯 Usage Examples

### Basic Usage
```bash
# Scrape with default settings
python main.py

# Limit to 50 pages
python main.py --max-pages 50

# Run a quick connectivity test
python main.py --test
```

### Advanced Usage
```bash
# Use requests method (faster but less reliable)
python main.py --method requests --max-pages 100

# Resume from a backup file
python main.py --resume links_backup_page_25.txt
```

### Programmatic Usage
```python
from data_scraper import DataScraper
from link_scraper import LinkScraper

# Collect links
link_scraper = LinkScraper(max_pages_limit=10)
links = link_scraper.scrape_all_pages()

# Extract product data
data_scraper = DataScraper()
products = data_scraper.scrape_multiple_products(links)
```

## 📊 Output Format

The scraper outputs data in CSV format with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Title | Product name | "Château Margaux 2015" |
| Price | Product price | "Rs. 25,000.00" |
| Description | Short description | "Premium Bordeaux wine with rich flavor" |
| Origin | Country of origin | "France" |
| Weight | Product weight | "0.75 kg" |
| Size | Bottle size | "750ML" |
| Category | Wine category | "Red Wine" |

## 🛠️ Technical Details

### Core Components

1. **BaseScraper**: Foundation class with driver management and common functionality
2. **LinkScraper**: Handles pagination and link collection with popup management
3. **DataScraper**: Extracts detailed product information using multiple selector strategies
4. **Utility Functions**: Helper functions for data processing and file operations

### Key Features

- **Multi-Selector Strategy**: Uses multiple CSS/XPath selectors for resilient element finding
- **Smart Categorization**: Automatically categorizes wines based on title and description keywords
- **Size Detection**: Extracts bottle sizes from product titles
- **Error Page Detection**: Identifies and skips error pages automatically

### Anti-Detection Measures

- Random delays between requests
- User agent rotation
- Popup handling
- Respectful request patterns

## 🐛 Troubleshooting

### Common Issues

**Firefox Driver Issues:**
```bash
# Update webdriver manager
pip install --upgrade webdriver-manager
```

**Timeout Errors:**
- Increase `PAGE_LOAD_TIMEOUT` in config.py
- Check internet connection stability

**No Products Found:**
- Website structure may have changed
- Update selectors in config.py
- Run with `--test` flag to diagnose

**Memory Issues:**
- Reduce `MAX_PAGES` limit
- Clear browser cache periodically

## 📈 Performance

- **Speed**: ~5-10 seconds per page depending on content
- **Success Rate**: ~95% for accessible pages
- **Memory Usage**: ~100-200MB during operation
- **Output**: Processes 20-50 products per page typically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if implemented)
python -m pytest tests/

# Code formatting
black *.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This scraper is for educational and research purposes only. Users are responsible for:

- Respecting the website's robots.txt and terms of service
- Not overloading the target server with requests
- Using the data ethically and legally
- Complying with applicable data protection laws

## 🎯 Roadmap

- [ ] Add support for multiple wine retailers
- [ ] Implement database storage options
- [ ] Add real-time monitoring dashboard
- [ ] Create Docker containerization
- [ ] Add unit and integration tests
- [ ] Implement data validation and cleaning
- [ ] Add support for image scraping

## 📞 Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/HarshaG2005/wine-world-scraper/issues) page
2. Create a new issue with detailed description
3. Include logs and error messages

## 🙏 Acknowledgments

- Built with [Selenium WebDriver](https://selenium.dev/)
- Uses [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) for automatic driver management
- Inspired by ethical web scraping practices

---

**Made with ❤️ for wine enthusiasts and data lovers**
