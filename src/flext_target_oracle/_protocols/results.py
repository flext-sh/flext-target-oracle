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

from flext_target_oracle import t

if TYPE_CHECKING:
    from flext_meltano import p


class FlextTargetOracleProtocolsResults:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ExecuteResult(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Target package name."""
            ...

        @property
        def status(self) -> Literal["ready"]:
            """Target readiness status."""
            ...

        @property
        def oracle_host(self) -> str:
            """Configured Oracle host."""
            ...

        @property
        def oracle_service(self) -> str:
            """Configured Oracle service name."""
            ...

    @runtime_checkable
    class ProcessingSummary(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def messages_processed(self) -> t.NonNegativeInt:
            """Total Singer messages processed."""
            ...

        @property
        def streams(self) -> Sequence[str]:
            """Singer stream names seen during processing."""
            ...

        @property
        def state(self) -> p.Meltano.SingerStateMessage:
            """Accumulated Singer STATE payload."""
            ...

    @runtime_checkable
    class LoaderOperation(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def stream_name(self) -> str:
            """Logical stream identifier."""
            ...

        @property
        def started_at(self) -> str:
            """Load operation start timestamp."""
            ...

        @property
        def completed_at(self) -> str:
            """Load operation completion timestamp."""
            ...

        @property
        def records_loaded(self) -> t.NonNegativeInt:
            """Number of loaded records."""
            ...

        @property
        def records_failed(self) -> t.NonNegativeInt:
            """Number of failed records."""
            ...

    @runtime_checkable
    class LoaderFinalizeResult(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def total_records(self) -> t.NonNegativeInt:
            """Total records processed."""
            ...

        @property
        def streams_processed(self) -> t.NonNegativeInt:
            """Number of processed streams."""
            ...

        @property
        def status(self) -> Literal["completed"]:
            """Finalization status."""
            ...

        @property
        def loading_operation(
            self,
        ) -> FlextTargetOracleProtocolsResults.LoaderOperation:
            """Aggregated loading operation details."""
            ...

        @property
        def buffer_status(self) -> Mapping[str, int]:
            """Remaining buffered records by stream."""
            ...

    @runtime_checkable
    class ImplementationMetrics(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def streams_configured(self) -> t.NonNegativeInt:
            """Number of configured streams."""
            ...

        @property
        def batch_size(self) -> t.BatchSize:
            """Configured batch size."""
            ...

        @property
        def use_bulk_operations(self) -> bool:
            """Whether bulk operations are enabled."""
            ...

    @runtime_checkable
    class LoadStatisticsModel(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def stream_name(self) -> str:
            """Stream identifier."""
            ...

        @property
        def total_records_processed(self) -> t.NonNegativeInt:
            """Total processed records."""
            ...

        @property
        def successful_records(self) -> t.NonNegativeInt:
            """Successful records."""
            ...

        @property
        def failed_records(self) -> t.NonNegativeInt:
            """Failed records."""
            ...

        @property
        def batches_processed(self) -> t.NonNegativeInt:
            """Processed batch count."""
            ...

        def finalize(self) -> Self:
            """Finalize statistics and return self."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsResults",
]
