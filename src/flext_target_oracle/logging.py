"""Modern logging configuration for Oracle target.

Simple, clean logging setup following KISS principle.
"""

from __future__ import annotations

import logging
import sys
from typing import Any


def configure_logger(
    name: str = "flext_target_oracle",
    level: str = "INFO",
    format_string: str | None = None,
) -> logging.Logger:
    """Configure logger with modern setup."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper()))

    return logger


def setup_logging(config: dict[str, Any]) -> logging.Logger:
    """Setup logging from configuration."""
    log_level = config.get("log_level", "INFO")
    return configure_logger(level=log_level)


__all__ = ["configure_logger", "setup_logging"]
