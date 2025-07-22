"""Modern monitoring setup for Oracle target.

Real implementations following production patterns.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from types import TracebackType

from flext_observability.logging import get_logger

logger = get_logger(__name__)

# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT


class MetricsCollector:
    """Metrics collection with statistics and history management."""

    def __init__(self, max_history: int = 1000) -> None:
        """Initialize metrics collector.

        Args:
            max_history: Maximum number of values to keep per metric

        """
        self._metrics: dict[str, deque[float]] = {}
        self._max_history = max_history
        self._lock = threading.Lock()

    def record_metric(self, name: str, value: float) -> None:
        """Record a metric value.

        Args:
            name: The metric name
            value: The metric value

        """
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = deque(maxlen=self._max_history)
            self._metrics[name].append(float(value))

    def get_all_metrics(self) -> dict[str, dict[str, Any]]:
        """Get all metrics with statistics.

        Returns:
            Dictionary of metrics with stats (count, min, max, avg, sum, latest, first)

        """
        with self._lock:
            result = {}
            for name, values in self._metrics.items():
                if values:
                    result[name] = {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "sum": sum(values),
                        "latest": values[-1],
                        "first": values[0],
                    }
            return result

    def get_metric_stats(self, name: str) -> dict[str, Any]:
        """Get statistics for a specific metric.

        Args:
            name: The metric name

        Returns:
            Dictionary with stats or empty dict if metric doesn't exist

        """
        with self._lock:
            if name not in self._metrics or not self._metrics[name]:
                return {}

            values = self._metrics[name]
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "sum": sum(values),
                "latest": values[-1],
                "first": values[0],
            }


class PerformanceTracker:
    """Performance tracking with context manager support."""

    def __init__(self, operation_name: str = "") -> None:
        """Initialize performance tracker.

        Args:
            operation_name: Name of the operation being tracked

        """
        self.operation_name = operation_name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def start(self) -> None:
        """Start timing the operation."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop timing the operation."""
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        """Get operation duration.

        Returns:
            Duration in seconds

        """
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time

    def get_duration(self) -> float:
        """Get current duration without stopping.

        Returns:
            Current duration in seconds

        """
        return self.duration

    def __enter__(self) -> Self:
        """Start tracking when entering context."""
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Stop tracking and log when exiting context."""
        self.stop()
        if self.operation_name:
            logger.info(
                f"Operation {self.operation_name} completed in "
                f"{self.duration:.4f} seconds duration",
            )


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

    def record_metric(
        self,
        name: str,
        value: str | float | bool,
    ) -> None:
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


__all__ = [
    "MetricsCollector",
    "PerformanceTimer",
    "PerformanceTracker",
    "SimpleMonitor",
    "create_monitor",
]
