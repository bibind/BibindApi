"""Simple logging configuration for the application."""

from __future__ import annotations

import logging

logger = logging.getLogger("bibind")

if not logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

__all__ = ["logger"]
