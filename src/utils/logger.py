from __future__ import annotations

import logging
import sys

from config import settings

_LOGGER_CACHE: dict[str, logging.Logger] = {}


def _configure_root_logger() -> None:
    root = logging.getLogger()
    if root.handlers:
    return

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    if name in _LOGGER_CACHE:
    return _LOGGER_CACHE[name]

    _configure_root_logger()
    logger = logging.getLogger(name)
    _LOGGER_CACHE[name] = logger
    return logger
