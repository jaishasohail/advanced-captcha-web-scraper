from __future__ import annotations

import random
from pathlib import Path
from typing import List, Optional, Set

from utils.logger import get_logger

logger = get_logger(__name__)


class ProxyManager:
    """
    Simple in-memory proxy rotation with bad-proxy tracking.
    """

    def __init__(self, proxy_file: Path) -> None:
    self.proxy_file = proxy_file
    self.proxies: List[str] = []
    self.bad_proxies: Set[str] = set()
    self._load_proxies()

    def _load_proxies(self) -> None:
    if not self.proxy_file.exists():
    logger.warning(
        "Proxy file %s does not exist; proxy rotation disabled.", self.proxy_file)
    return

    lines = [line.strip() for line in self.proxy_file.read_text(
        encoding="utf-8").splitlines()]
    self.proxies = [
        line for line in lines if line and not line.startswith("#")]
    logger.info("Loaded %d proxies from %s",
                len(self.proxies), self.proxy_file)

    def get_proxy(self) -> Optional[str]:
    candidates = [p for p in self.proxies if p not in self.bad_proxies]
    if not candidates:
    logger.debug("No healthy proxies available.")
    return None
    proxy = random.choice(candidates)
    logger.debug("Selected proxy %s", proxy)
    return proxy

    def mark_bad(self, proxy: str) -> None:
    if proxy in self.proxies:
    self.bad_proxies.add(proxy)
    logger.info("Marked proxy as bad: %s (bad=%d)",
                proxy, len(self.bad_proxies))
