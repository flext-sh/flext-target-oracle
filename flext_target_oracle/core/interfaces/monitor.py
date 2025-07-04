"""Monitoring interfaces.

These interfaces define contracts for monitoring and observability,
enabling different monitoring backends while keeping the core decoupled.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ..models.metrics import Metric


@runtime_checkable
class IMetricsCollector(Protocol):
    """Interface for collecting metrics."""

    @abstractmethod
    def increment(
        self, name: str, value: float = 1.0, tags: dict[str, str] | None = None
    ) -> None:
        """Increment a counter metric."""

    @abstractmethod
    def gauge(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Set a gauge metric."""

    @abstractmethod
    def histogram(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Record a histogram value."""

    @abstractmethod
    def timer(self, name: str) -> Any:
        """Get a timer context manager."""


@runtime_checkable
class IMonitor(Protocol):
    """Interface for system monitoring."""

    @abstractmethod
    def start(self) -> None:
        """Start monitoring."""

    @abstractmethod
    def stop(self) -> None:
        """Stop monitoring."""

    @abstractmethod
    def record_batch_processed(self, stream: str, count: int, duration: float) -> None:
        """Record batch processing metrics."""

    @abstractmethod
    def record_error(self, stream: str, error_type: str, error_message: str) -> None:
        """Record an error occurrence."""

    @abstractmethod
    def record_connection_metrics(self, active: int, idle: int, total: int) -> None:
        """Record connection pool metrics."""

    @abstractmethod
    def get_metrics(self) -> dict[str, Metric]:
        """Get all collected metrics."""

    @abstractmethod
    def export_metrics(self, format: str = "prometheus") -> str:
        """Export metrics in specified format."""
