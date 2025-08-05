# imports.py - Centralized imports for the scraper project

# Standard library imports
import logging
import random
import time
import json
import sys
import argparse
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin
from dataclasses import dataclass

# Selenium imports
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    InvalidSessionIdException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

# Requests and web scraping imports
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib3.exceptions import ReadTimeoutError, ConnectTimeoutError
from bs4 import BeautifulSoup

# Optional imports with error handling

# Export commonly used imports for easy access
__all__ = [
    # Standard library
    'logging', 'random', 'time', 'json', 'sys', 'argparse',
    'List', 'Optional', 'Dict', 'Any', 'urljoin',
    
    # Selenium core
    'webdriver', 'FirefoxService', 
    'GeckoDriverManager',
    'By', 'WebDriverWait', 'EC', 'Keys',
    'FirefoxOptions',
    
    # Selenium exceptions
    'NoSuchElementException', 'TimeoutException', 'WebDriverException',
    'InvalidSessionIdException', 'ElementNotInteractableException',
    'StaleElementReferenceException',
    
    # Requests and parsing
    'requests', 'HTTPAdapter', 'Retry', 'ReadTimeoutError', 
    'ConnectTimeoutError', 'BeautifulSoup',
    
]