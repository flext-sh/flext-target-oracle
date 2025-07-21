"""Observability metrics for monitoring system health and performance.

Real implementations of monitoring classes for production use.
"""

from __future__ import annotations

from enum import Enum

from flext_core import DomainBaseModel


class HealthStatus(Enum):
    """System health status enumeration."""

    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class DatabaseMetrics(DomainBaseModel):
    """Database performance metrics model."""

    connections_active: int
    connections_total: int
    query_duration_avg: float
    query_success_rate: float


class RecordMetrics(DomainBaseModel):
    """Record processing performance metrics model."""

    records_processed: int
    records_failed: int
    processing_rate: float
    batch_size_avg: int


__all__ = ["DatabaseMetrics", "HealthStatus", "RecordMetrics"]
