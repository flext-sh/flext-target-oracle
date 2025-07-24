"""Logging configuration for Oracle target.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module now delegates to flext-infrastructure.monitoring.flext-observability for
standardized logging.
"""

from __future__ import annotations

# Removed circular dependency - use DI pattern
import logging

# Removed circular dependency - use DI pattern
import logging as obs_setup_logging
from typing import Any


def configure_logger(
    name: str = "flext_target_oracle",
    level: str = "INFO",
    format_string: str | None = None,
) -> Any:
    """Configure logger for flext-data.targets.flext-target-oracle.

    Args:
        name: Logger name
        level: Log level
        format_string: Format string for log messages

    Returns:
        Configured logger instance

    """
    # Logging is configured globally by
    # flext-infrastructure.monitoring.flext-observability
    # Just return the logger for the given name
    return logging.getLogger(name)


def setup_logging(config: dict[str, Any]) -> Any:
    """Set up logging configuration for flext-data.targets.flext-target-oracle.

    Args:
        config: Configuration dictionary with logging settings

    Returns:
        Configured logger instance for the module

    """
    # Note: log_level configuration is applied globally by
    # flext-infrastructure.monitoring.flext-observability

    # Setup global logging if not already done:
    obs_setup_logging()

    # Return logger for this module
    return logging.getLogger("flext_target_oracle")


__all__ = ["configure_logger", "setup_logging"]
