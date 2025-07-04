"""Batch processing models.

These models represent batches of data and their processing results,
ensuring type safety and clear contracts.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProcessingStrategy(str, Enum):
    """Batch processing strategies."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DIRECT_PATH = "direct_path"
    BULK_INSERT = "bulk_insert"
    MERGE = "merge"


class BatchStatus(str, Enum):
    """Status of batch processing."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class Batch(BaseModel):
    """Represents a batch of records for processing."""

    id: str = Field(..., description="Unique batch identifier")
    stream_name: str = Field(..., description="Name of the stream")
    records: list[dict[str, Any]] = Field(..., description="Records in the batch")
    size: int = Field(..., description="Number of records")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Batch creation time")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    model_config = {
        "frozen": True,
    }

    @classmethod
    def from_records(cls, stream_name: str, records: list[dict[str, Any]], batch_id: str | None = None) -> Batch:
        """Create a batch from records."""
        import uuid

        return cls(
            id=batch_id or str(uuid.uuid4()),
            stream_name=stream_name,
            records=records,
            size=len(records),
        )

    def split(self, chunk_size: int) -> list[Batch]:
        """Split batch into smaller chunks."""
        chunks = []
        for i in range(0, self.size, chunk_size):
            chunk_records = self.records[i:i + chunk_size]
            chunks.append(
                Batch.from_records(
                    stream_name=self.stream_name,
                    records=chunk_records,
                    batch_id=f"{self.id}_{i // chunk_size}",
                )
            )
        return chunks


class BatchResult(BaseModel):
    """Result of batch processing."""

    batch_id: str = Field(..., description="Batch identifier")
    status: BatchStatus = Field(..., description="Processing status")
    records_processed: int = Field(0, description="Number of records processed")
    records_failed: int = Field(0, description="Number of records failed")
    start_time: datetime = Field(..., description="Processing start time")
    end_time: datetime | None = Field(None, description="Processing end time")
    duration_seconds: float | None = Field(None, description="Processing duration")
    errors: list[str] = Field(default_factory=list, description="Processing errors")
    warnings: list[str] = Field(default_factory=list, description="Processing warnings")
    metrics: dict[str, float] = Field(default_factory=dict, description="Performance metrics")

    model_config = {
        "frozen": True,
    }

    @classmethod
    def success(cls, batch_id: str, records_processed: int, metrics: dict[str, float] | None = None) -> BatchResult:
        """Create a successful batch result."""
        now = datetime.utcnow()
        return cls(
            batch_id=batch_id,
            status=BatchStatus.COMPLETED,
            records_processed=records_processed,
            start_time=now,
            end_time=now,
            duration_seconds=0,
            metrics=metrics or {},
        )

    @classmethod
    def failure(cls, batch_id: str, errors: list[str]) -> BatchResult:
        """Create a failed batch result."""
        now = datetime.utcnow()
        return cls(
            batch_id=batch_id,
            status=BatchStatus.FAILED,
            start_time=now,
            end_time=now,
            errors=errors,
        )

    def merge_with(self, other: BatchResult) -> BatchResult:
        """Merge two batch results."""
        return BatchResult(
            batch_id=f"{self.batch_id}+{other.batch_id}",
            status=BatchStatus.COMPLETED if self.status == other.status == BatchStatus.COMPLETED else BatchStatus.PARTIAL,
            records_processed=self.records_processed + other.records_processed,
            records_failed=self.records_failed + other.records_failed,
            start_time=min(self.start_time, other.start_time),
            end_time=max(self.end_time or self.start_time, other.end_time or other.start_time),
            duration_seconds=(self.duration_seconds or 0) + (other.duration_seconds or 0),
            errors=self.errors + other.errors,
            warnings=self.warnings + other.warnings,
            metrics={**self.metrics, **other.metrics},
        )
