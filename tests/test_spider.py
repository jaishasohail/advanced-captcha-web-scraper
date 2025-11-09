from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure src/ is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
 sys.path.insert(0, str(SRC_DIR))

from scraper.spider import AdvancedSpider  # noqa: E402
from scraper.data_parser import DataParser  # noqa: E402

HTML_SNIPPET = """

 Wireless Headphones

 $59.99
 In Stock

 Bluetooth Speaker

 $39.99
 Out of Stock

"""


def test_data_parser_extracts_products():
 parser = DataParser()
 items = parser.parse_product_list(HTML_SNIPPET)
 assert len(items) == 2
 assert items[0]["product_id"] == "A10234"
 assert items[0]["product_name"] == "Wireless Headphones"
 assert "$59.99" in items[0]["price"]


def test_spider_captcha_detection():
 html_with_captcha = "Please complete the CAPTCHA challenge.
"
 spider = AdvancedSpider(target_urls=[], max_pages=1)
 assert spider._contains_captcha(html_with_captcha) is True # noqa: SLF001

 html_without_captcha = "Hello world
"
 assert spider._contains_captcha(html_without_captcha) is False # noqa: SLF001

@pytest.mark.parametrize(
 "html, expected",
 [
 (HTML_SNIPPET, 2),
 ("No products here", 0),
 ],
)
def test_spider_parse_items(html: str, expected: int):
 spider = AdvancedSpider(target_urls=[], max_pages=1)
 items = spider._parse_items(html, "https://example.com") # noqa: SLF001
 assert len(items) == expected
 for item in items:
 assert item["source_url"] == "https://example.com"
 assert "scraped_at" in item