"""Observability metrics for monitoring system health and performance.

Real implementations of monitoring classes for production use.
"""

from __future__ import annotations

from enum import Enum

# 🚨 ARCHITECTURAL COMPLIANCE
from flext_target_oracle.infrastructure.di_container import (
    get_domain_entity,
    get_field,
    get_service_result,
)

ServiceResult = get_service_result()
DomainEntity = get_domain_entity()
Field = get_field()


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
