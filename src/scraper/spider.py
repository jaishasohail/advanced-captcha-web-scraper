from __future__ import annotations

import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, List, Dict, Optional

import requests
from bs4 import BeautifulSoup

from config import settings
from scraper.captcha_solver import CaptchaSolver
from scraper.data_parser import DataParser
from scraper.proxy_manager import ProxyManager
from utils.helpers import jitter_sleep, build_headers
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class PageResult:
    url: str
    status_code: int
    html: str
    proxy: Optional[str]


class AdvancedSpider:
    """
    High-level spider responsible for:
    - Fetching pages with optional rotating proxies
    - Detecting Captcha challenges
    - Delegating HTML parsing to DataParser
    """

    def __init__(
        self,
        target_urls: Iterable[str],
        max_pages: int,
        headless: bool = True,
        use_proxies: bool = False,
    ) -> None:
    self.session = requests.Session()
    self.target_urls = list(target_urls)[:max_pages]
    self.max_pages = max_pages
    self.headless = headless
    self.use_proxies = use_proxies
    self.captcha_solver = CaptchaSolver()
    self.data_parser = DataParser()
    self.proxy_manager = ProxyManager(
        settings.PROXY_FILE) if use_proxies else None

    def run(self) -> List[Dict]:
    scraped_items: List[Dict] = []
    for url in self.target_urls:
    logger.info("Fetching %s", url)
    page = self._fetch_with_retries(url)
    if not page:
    logger.warning("Skipping %s because it could not be fetched.", url)
    continue

    if self._contains_captcha(page.html):
    logger.info("Captcha detected on %s - attempting to bypass", page.url)
    self._handle_captcha(page)

    parsed = self._parse_items(page.html, page.url)
    scraped_items.extend(parsed)
    jitter_sleep(settings.REQUEST_DELAY_SECONDS,
                 settings.REQUEST_JITTER_SECONDS)

    return scraped_items

    # Networking -----------------------------------------------------------------

    def _fetch_with_retries(self, url: str) -> Optional[PageResult]:
    attempts = 0
    while attempts bool:
    """Naive captcha detection based on known markers."""
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True).lower()

    if "captcha" in text:
    return True

    # look for common providers
    if soup.find("div", {"class": "g-recaptcha"}):
    return True
    if soup.find("iframe", {"src": lambda x: x and "recaptcha" in x}):
    return True
    if soup.find("iframe", {"src": lambda x: x and "hcaptcha" in x}):
    return True

    return False

    def _handle_captcha(self, page: PageResult) -> None:
    """
 Placeholder for more sophisticated captcha flows.

 In a real-world integration we might:
 - Use Selenium to load the page
 - Identify the Captcha widget
 - Send sitekey + URL to CaptchaSolver
 - Inject solution token into the page and resubmit
 """
    try:
    solution = self.captcha_solver.solve_generic(page.url)
    logger.info("Captcha solution token acquired (length=%d)", len(solution))
    except Exception as exc:  # noqa: BLE001
    logger.error("Could not solve captcha for %s: %s", page.url, exc)

    # Parsing --------------------------------------------------------------------

    def _parse_items(self, html: str, url: str) -> List[Dict]:
    parsed = self.data_parser.parse_product_list(html)
    now_iso = datetime.now(timezone.utc).isoformat()

    for item in parsed:
    item.setdefault("source_url", url)
    item.setdefault("scraped_at", now_iso)

    logger.info("Parsed %d items from %s", len(parsed), url)
    return parsed
