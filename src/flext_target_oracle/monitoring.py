"""Modern monitoring setup for Oracle target.

Simple metrics and health monitoring following KISS principle.
"""

from __future__ import annotations

import time
from typing import Any

# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT


class PerformanceTimer:
    """Simple performance timer."""

    def __init__(self) -> None:
        """Initialize performance timer with zero times."""
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def start(self) -> None:
        """Start the performance timer."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop the performance timer."""
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        """Get the elapsed duration.

        Returns:
            Duration in seconds since start.

        """
        if self.end_time == 0.0:
            return time.time() - self.start_time
        return self.end_time - self.start_time


class SimpleMonitor:
    """Simple monitoring implementation."""

    def __init__(self) -> None:
        """Initialize monitoring with empty metrics dictionary."""
        self.metrics: dict[str, Any] = {}

    def record_metric(self, name: str, value: str | float | bool) -> None:  # noqa: FBT001
        """Record a metric value.

        Args:
            name: The metric name.
            value: The metric value.

        """
        self.metrics[name] = value

    def get_metrics(self) -> dict[str, Any]:
        """Get all recorded metrics.

        Returns:
            Copy of all metrics.

        """
        return self.metrics.copy()


def create_monitor(_config: dict[str, Any] | None = None) -> SimpleMonitor:
    """Create a monitor instance.

    Args:
        _config: Optional configuration (unused).

    Returns:
        A new SimpleMonitor instance.

    """
    return SimpleMonitor()


__all__ = ["PerformanceTimer", "SimpleMonitor", "create_monitor"]
