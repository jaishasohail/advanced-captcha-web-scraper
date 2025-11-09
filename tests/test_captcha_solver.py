from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure src/ is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from scraper.captcha_solver import CaptchaSolver  # noqa: E402


def test_captcha_solver_returns_dummy_token_without_config(monkeypatch):
    # Ensure environment is not configured
    monkeypatch.delenv("CAPTCHA_PROVIDER_URL", raising=False)
    monkeypatch.delenv("CAPTCHA_API_KEY", raising=False)

    solver = CaptchaSolver()
    token = solver.solve_generic("https://example.com")
    assert token.startswith("DUMMY_CAPTCHA_TOKEN_")


def test_image_captcha_solver_debug_mode(monkeypatch):
    monkeypatch.delenv("CAPTCHA_PROVIDER_URL", raising=False)
    monkeypatch.delenv("CAPTCHA_API_KEY", raising=False)

    solver = CaptchaSolver()
    token = solver.solve_image_captcha(b"fake-bytes")
    assert token == "DUMMY_IMAGE_SOLUTION_10"  # len("fake-bytes") == 10
