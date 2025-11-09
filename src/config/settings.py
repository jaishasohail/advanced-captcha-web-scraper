from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Target pages to crawl; replace with real URLs for production usage
TARGET_URLS = [
    "https://example.com/product-list-1",
    "https://example.com/product-list-2",
]

MAX_PAGES = 10

# Network settings
REQUEST_TIMEOUT_SECONDS = 20
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

REQUEST_DELAY_SECONDS = 1.0
REQUEST_JITTER_SECONDS = 0.75

# Files & paths
PROXY_FILE = PROJECT_ROOT / "src" / "config" / "proxies.txt"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

# User agent pool for randomization
USER_AGENTS = [
    # Common desktop agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

# Selenium
SELENIUM_IMPLICIT_WAIT = 10
SELENIUM_PAGE_LOAD_TIMEOUT = 60

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
