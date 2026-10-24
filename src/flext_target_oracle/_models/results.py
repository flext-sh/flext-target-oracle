"""Result and payload models for Oracle target operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Literal, Self

# NOTE (multi-agent): mro-rn88 — source `u` from flext_meltano (external, cycle-safe),
# not the own package facade, to avoid the models→utilities→client circular import.
from flext_meltano import m, t


class FlextTargetOracleModelsResults:
    """Result models MRO mixin for TargetOracle namespace."""

    class ExecuteResult(m.ArbitraryTypesModel):
        """Target execute readiness payload."""

        name: Annotated[
            str,
            m.Field(..., description="Target package name", validate_default=True),
        ]
        status: Annotated[
            Literal["ready"],
            m.Field(..., description="Target readiness status", validate_default=True),
        ] = "ready"
        oracle_host: Annotated[
            str,
            m.Field(..., description="Configured Oracle host", validate_default=True),
        ]
        oracle_service: Annotated[
            str,
            m.Field(
                ...,
                description="Configured Oracle service name",
                validate_default=True,
            ),
        ]

    class ProcessingSummary(m.ArbitraryTypesModel):
        """Singer batch processing summary payload."""

        messages_processed: Annotated[
            t.NonNegativeInt,
            m.Field(
                ...,
                description="Total Singer messages processed",
                validate_default=True,
            ),
        ]
        streams: Annotated[
            t.StrSequence,
            m.Field(
                ...,
                description="Singer stream names seen during processing",
                validate_default=True,
            ),
        ] = m.Field(default_factory=tuple, validate_default=True)
        state: Annotated[
            m.Meltano.SingerStateMessage,
            m.Field(
                ...,
                description="Accumulated Singer STATE payload",
                validate_default=True,
            ),
        ]

    class LoaderOperation(m.ArbitraryTypesModel):
        """Detailed load operation summary for all streams."""

        stream_name: Annotated[
            str,
            m.Field(
                ...,
                description="Logical stream identifier",
                validate_default=True,
            ),
        ]
        started_at: Annotated[
            str,
            m.Field(
                ...,
                description="Load operation start timestamp",
                validate_default=True,
            ),
        ]
        completed_at: Annotated[
            str,
            m.Field(
                ...,
                description="Load operation completion timestamp",
                validate_default=True,
            ),
        ]
        records_loaded: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Number of loaded records", validate_default=True),
        ]
        records_failed: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Number of failed records", validate_default=True),
        ]

    class LoaderFinalizeResult(m.ArbitraryTypesModel):
        """Loader finalization payload for flush operations."""

        total_records: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Total records processed", validate_default=True),
        ]
        streams_processed: Annotated[
            t.NonNegativeInt,
            m.Field(
                ...,
                description="Number of processed streams",
                validate_default=True,
            ),
        ]
        status: Annotated[
            Literal["completed"],
            m.Field(..., description="Finalization status", validate_default=True),
        ] = "completed"
        loading_operation: Annotated[
            FlextTargetOracleModelsResults.LoaderOperation,
            m.Field(description="Aggregated loading operation details"),
        ]
        buffer_status: Annotated[
            t.MappingKV[str, int],
            m.Field(
                ...,
                description="Remaining buffered records by stream",
                validate_default=True,
            ),
        ]

    class ImplementationMetrics(m.ArbitraryTypesModel):
        """Oracle target implementation metrics."""

        streams_configured: Annotated[
            t.NonNegativeInt,
            m.Field(
                ...,
                description="Number of configured streams",
                validate_default=True,
            ),
        ]
        batch_size: Annotated[
            t.BatchSize,
            m.Field(..., description="Configured batch size", validate_default=True),
        ]
        use_bulk_operations: Annotated[
            bool,
            m.Field(
                ...,
                description="Whether bulk operations are enabled",
                validate_default=True,
            ),
        ]

    class LoadStatisticsModel(m.ArbitraryTypesModel):
        """Statistics for data load operation."""

        stream_name: Annotated[
            str,
            m.Field(..., description="Stream identifier", validate_default=True),
        ]
        total_records_processed: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Total processed records", validate_default=True),
        ]
        successful_records: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Successful records", validate_default=True),
        ]
        failed_records: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Failed records", validate_default=True),
        ]
        batches_processed: Annotated[
            t.NonNegativeInt,
            m.Field(..., description="Processed batch count", validate_default=True),
        ]

        def finalize(self) -> Self:
            """Finalize statistics and return self.

            Returns:
                The finalized statistics model.

            """
            return self


__all__: list[str] = ["FlextTargetOracleModelsResults"]
