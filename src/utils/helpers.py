from __future__ import annotations

import random
import time
from typing import Dict

from config import settings


def jitter_sleep(base: float, jitter: float) -> None:
    """
    Sleep for base +/- random jitter seconds to mimic human behavior.
    """
    delta = random.uniform(-jitter, jitter)
    duration = max(0.0, base + delta)
    time.sleep(duration)


def build_headers() -> Dict[str, str]:
    """
    Construct a randomized HTTP header set for outbound requests.
    """
    user_agent = random.choice(settings.USER_AGENTS)
    return {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }
