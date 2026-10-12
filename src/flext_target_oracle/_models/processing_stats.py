from __future__ import annotations

from flext_target_oracle import m


class ProcessingStats(m.BaseModel):
    """In-memory counters for Singer stream processing."""

    processing_start_time: float
    processing_end_time: float | None = None
    processing_duration_seconds: float = 0.0
    messages_processed: int = 0
    schemas_processed: int = 0
    records_processed: int = 0
    states_processed: int = 0
    errors_encountered: int = 0
