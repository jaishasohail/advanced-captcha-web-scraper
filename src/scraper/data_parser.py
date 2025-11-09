from __future__ import annotations

import re
from typing import List, Dict

from bs4 import BeautifulSoup

from utils.logger import get_logger

logger = get_logger(__name__)


class DataParser:
    """
    Extracts structured product-like data from HTML pages.

    By default it looks for card-like structures with:
    - data-product-id or [id] attributes
    - title elements
    - price strings
    """

    PRICE_RE = re.compile(r"\$?\s*\d+(?:\.\d{2})?")

    def parse_product_list(self, html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    items: List[Dict] = []

    # Generic "product card" pattern
    product_nodes = soup.select("[data-product-id], .product-card, .product")
    logger.debug("Found %d potential product nodes", len(product_nodes))

    for node in product_nodes:
    item = self._parse_single_product(node)
    if item:
    items.append(item)

    # Fallback: table or list-based products
    if not items:
    table_items = self._parse_table_products(soup)
    items.extend(table_items)

    logger.info("DataParser produced %d items from page", len(items))
    return items

    # type: ignore[override]
    def _parse_single_product(self, node) -> Dict | None:
    product_id = (
        node.get("data-product-id")
        or node.get("data-id")
        or node.get("id")
    )

    title_el = node.select_one(".product-title, .title, h1, h2, h3")
    product_name = title_el.get_text(strip=True) if title_el else None

    price_el = node.select_one(".price, .product-price, [data-price]")
    price_text = price_el.get_text(" ", strip=True) if price_el else None
    if not price_text:
    price_text = self._find_price_nearby(node.get_text(" ", strip=True))

    availability_el = node.select_one(".availability, .stock, .status")
    availability = (
        availability_el.get_text(" ", strip=True) if availability_el else None
    )

    if not (product_id or product_name or price_text):
    return None

    item = {
        "product_id": product_id or "",
        "product_name": product_name or "",
        "price": price_text or "",
        "availability": availability or "",
    }
    return item

    def _parse_table_products(self, soup: BeautifulSoup) -> List[Dict]:
    items: List[Dict] = []
    table = soup.find("table")
    if not table:
    return items

    headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
    for row in table.find_all("tr"):
    cells = [td.get_text(" ", strip=True) for td in row.find_all("td")]
    if not cells:
    continue

    data = dict(zip(headers, cells))
    if not data:
    continue

    product_id = data.get("id") or data.get("product_id") or ""
    product_name = data.get("name") or data.get("product_name") or ""
    price = data.get("price") or self._find_price_nearby(" ".join(cells)) or ""
    availability = data.get("availability") or data.get("stock") or ""

    if not (product_id or product_name or price):
    continue

    items.append(
        {
            "product_id": product_id,
            "product_name": product_name,
            "price": price,
            "availability": availability,
        }
    )
    return items

    def _find_price_nearby(self, text: str) -> str | None:
    match = self.PRICE_RE.search(text)
    return match.group(0) if match else None
