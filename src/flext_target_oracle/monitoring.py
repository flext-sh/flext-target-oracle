"""Modern monitoring setup for Oracle target.

Simple metrics and health monitoring following KISS principle.
"""

from __future__ import annotations

import time
from typing import Any


class PerformanceTimer:
    """Simple performance timer."""

    def __init__(self) -> None:
        """Initialize timer."""
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def start(self) -> None:
        """Start timing."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop timing."""
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        """Get duration in seconds."""
        if self.end_time == 0.0:
            return time.time() - self.start_time
        return self.end_time - self.start_time


class SimpleMonitor:
    """Simple monitoring implementation."""

    def __init__(self) -> None:
        """Initialize monitor."""
        self.metrics: dict[str, Any] = {}

    def record_metric(self, name: str, value: str | int | float | bool) -> None:
        """Record a metric value."""
        self.metrics[name] = value

    def get_metrics(self) -> dict[str, Any]:
        """Get all recorded metrics."""
        return self.metrics.copy()


def create_monitor(config: dict[str, Any] | None = None) -> SimpleMonitor:
    """Create a simple monitor instance."""
    return SimpleMonitor()


__all__ = ["PerformanceTimer", "SimpleMonitor", "create_monitor"]
