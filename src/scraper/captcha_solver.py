from __future__ import annotations

import os
from dataclasses import dataclass

import requests

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CaptchaConfig:
    provider_url: str | None
    api_key: str | None


class CaptchaSolver:
    """
    Simple integration wrapper for external Captcha solving services.

    The solver works in two modes:
    - Production mode: when CAPTCHA_PROVIDER_URL and CAPTCHA_API_KEY are set.
    - Debug mode: when no credentials are provided; a deterministic dummy token is returned.
    """

    def __init__(self) -> None:
    self.config = CaptchaConfig(
        provider_url=os.getenv("CAPTCHA_PROVIDER_URL"),
        api_key=os.getenv("CAPTCHA_API_KEY"),
    )

    def _debug_token(self, payload: str) -> str:
    token = f"DUMMY_CAPTCHA_TOKEN_{abs(hash(payload))}"
    logger.debug("Returning debug captcha token: %s", token)
    return token

    def solve_generic(self, url: str) -> str:
    """
 Generic solver entrypoint for high-level flows.
 """
    payload = {"type": "generic", "url": url}
    return self._solve(payload)

    def solve_recaptcha(self, site_key: str, url: str) -> str:
    payload = {"type": "recaptcha_v2", "site_key": site_key, "url": url}
    return self._solve(payload)

    def solve_image_captcha(self, image_bytes: bytes) -> str:
    payload = {"type": "image"}
    if not self.config.provider_url or not self.config.api_key:
        # Just hash the length as a predictable dummy response
    token = f"DUMMY_IMAGE_SOLUTION_{len(image_bytes)}"
    logger.debug("Returning debug image captcha token: %s", token)
    return token

    files = {"file": ("captcha.jpg", image_bytes, "image/jpeg")}
    try:
    response = requests.post(
        self.config.provider_url.rstrip("/") + "/solve-image",
        headers={"Authorization": f"Bearer {self.config.api_key}"},
        files=files,
        timeout=120,
    )
    response.raise_for_status()
    solution = response.json().get("solution")
    if not solution:
    raise ValueError("Captcha provider did not return a solution.")
    return solution
    except Exception as exc:  # noqa: BLE001
    logger.error(
        "Image captcha solving failed, falling back to debug token: %s", exc)
    return self._debug_token("image")

    def _solve(self, payload: dict) -> str:
    if not self.config.provider_url or not self.config.api_key:
    logger.warning(
        "Captcha provider not configured. Operating in debug mode. "
        "Set CAPTCHA_PROVIDER_URL and CAPTCHA_API_KEY for real solving."
    )
    return self._debug_token(str(payload))

    try:
    response = requests.post(
        self.config.provider_url.rstrip("/") + "/solve",
        headers={"Authorization": f"Bearer {self.config.api_key}"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    solution = response.json().get("solution")
    if not solution:
    raise ValueError("Captcha provider did not return a solution.")
    logger.debug("Received captcha solution from provider.")
    return solution
    except Exception as exc:  # noqa: BLE001
    logger.error(
        "Captcha solving failed, falling back to debug token: %s", exc)
    return self._debug_token(str(payload))
