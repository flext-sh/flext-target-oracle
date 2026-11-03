# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/results
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Literal, Protocol, Self, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_meltano import p

    from flext_target_oracle import t


class FlextTargetOracleProtocolsResults:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ExecuteResult(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        status: Literal["ready"]
        oracle_host: str
        oracle_service: str

    @runtime_checkable
    class ProcessingSummary(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        messages_processed: t.NonNegativeInt
        streams: Sequence[str]

        @property
        def state(self) -> p.Meltano.SingerStateMessage:
            """Accumulated Singer STATE payload."""
            ...

    @runtime_checkable
    class LoaderOperation(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        stream_name: str
        started_at: str
        completed_at: str
        records_loaded: t.NonNegativeInt
        records_failed: t.NonNegativeInt

    @runtime_checkable
    class LoaderFinalizeResult(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        total_records: t.NonNegativeInt
        streams_processed: t.NonNegativeInt
        status: Literal["completed"]

        @property
        def loading_operation(
            self,
        ) -> FlextTargetOracleProtocolsResults.LoaderOperation:
            """Aggregated loading operation details."""
            ...

        buffer_status: Mapping[str, int]

    @runtime_checkable
    class ImplementationMetrics(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        streams_configured: t.NonNegativeInt
        batch_size: t.BatchSize
        use_bulk_operations: bool

    @runtime_checkable
    class LoadStatisticsModel(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        stream_name: str
        total_records_processed: t.NonNegativeInt
        successful_records: t.NonNegativeInt
        failed_records: t.NonNegativeInt
        batches_processed: t.NonNegativeInt

        def finalize(self) -> Self:
            """Finalize statistics and return self."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsResults",
]
