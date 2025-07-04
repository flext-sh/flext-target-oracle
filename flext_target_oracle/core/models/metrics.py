"""Metrics and monitoring models.

These models represent metrics collected during processing,
enabling consistent monitoring across the system.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MetricType(str, Enum):
    """Types of metrics."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MetricUnit(str, Enum):
    """Units for metric values."""

    COUNT = "count"
    BYTES = "bytes"
    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    PERCENTAGE = "percentage"
    ROWS = "rows"
    BATCHES = "batches"


class Metric(BaseModel):
    """Represents a single metric."""

    name: str = Field(..., description="Metric name")
    type: MetricType = Field(..., description="Metric type")
    value: float = Field(..., description="Metric value")
    unit: MetricUnit = Field(MetricUnit.COUNT, description="Metric unit")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Measurement time"
    )
    tags: dict[str, str] = Field(default_factory=dict, description="Metric tags")
    description: str | None = Field(None, description="Metric description")

    model_config = {
        "frozen": True,
        "use_enum_values": True,
    }

    def to_prometheus(self) -> str:
        """Convert to Prometheus format."""
        # Build tags string
        if self.tags:
            tags_str = ",".join(f'{k}="{v}"' for k, v in self.tags.items())
            return f"{self.name}{{{tags_str}}} {self.value}"
        return f"{self.name} {self.value}"


class MetricsSummary(BaseModel):
    """Summary of collected metrics."""

    period_start: datetime = Field(..., description="Period start time")
    period_end: datetime = Field(..., description="Period end time")
    total_batches: int = Field(0, description="Total batches processed")
    total_records: int = Field(0, description="Total records processed")
    total_errors: int = Field(0, description="Total errors encountered")
    avg_batch_size: float = Field(0.0, description="Average batch size")
    avg_processing_time: float = Field(
        0.0, description="Average processing time per batch"
    )
    throughput_records_per_second: float = Field(0.0, description="Records per second")
    success_rate: float = Field(0.0, description="Success rate percentage")

    model_config = {
        "frozen": True,
    }

    @property
    def duration_seconds(self) -> float:
        """Calculate period duration in seconds."""
        return (self.period_end - self.period_start).total_seconds()

    @classmethod
    def from_metrics(cls, metrics: list[Metric]) -> MetricsSummary:
        """Create summary from list of metrics."""
        if not metrics:
            now = datetime.utcnow()
            return cls(period_start=now, period_end=now)

        # Extract relevant metrics
        batch_metrics = [m for m in metrics if m.name.endswith("_batches")]
        record_metrics = [m for m in metrics if m.name.endswith("_records")]
        error_metrics = [m for m in metrics if m.name.endswith("_errors")]
        time_metrics = [m for m in metrics if m.unit == MetricUnit.SECONDS]

        # Calculate summary
        total_batches = sum(m.value for m in batch_metrics)
        total_records = sum(m.value for m in record_metrics)
        total_errors = sum(m.value for m in error_metrics)

        avg_batch_size = total_records / total_batches if total_batches > 0 else 0
        avg_processing_time = (
            sum(m.value for m in time_metrics) / len(time_metrics)
            if time_metrics
            else 0
        )

        period_start = min(m.timestamp for m in metrics)
        period_end = max(m.timestamp for m in metrics)
        duration = (period_end - period_start).total_seconds()

        throughput = total_records / duration if duration > 0 else 0
        success_rate = (
            ((total_records - total_errors) / total_records * 100)
            if total_records > 0
            else 0
        )

        return cls(
            period_start=period_start,
            period_end=period_end,
            total_batches=int(total_batches),
            total_records=int(total_records),
            total_errors=int(total_errors),
            avg_batch_size=avg_batch_size,
            avg_processing_time=avg_processing_time,
            throughput_records_per_second=throughput,
            success_rate=success_rate,
        )
