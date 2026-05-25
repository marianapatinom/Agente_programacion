"""Logging configuration for local and production execution."""

import logging


def configure_logging(level: str) -> None:
    """Configure structured-enough logging for academic production demos."""

    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
