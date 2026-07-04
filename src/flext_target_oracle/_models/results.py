"""Result and payload models for Oracle target operations."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Literal, Self

from flext_meltano import m, t
from flext_target_oracle import u


def _default_buffer_status() -> t.MappingKV[str, int]:
    """Return an immutable empty buffer-status mapping."""
    return MappingProxyType({})


class FlextTargetOracleModelsResults:
    """Result models MRO mixin for TargetOracle namespace."""

    class ExecuteResult(m.ArbitraryTypesModel):
        """Target execute readiness payload."""

        name: Annotated[
            str, u.Field(..., description="Target package name", validate_default=True)
        ]
        status: Annotated[
            Literal["ready"],
            u.Field(
                ...,
                description="Target readiness status",
                validate_default=True,
            ),
        ] = "ready"
        oracle_host: Annotated[
            str,
            u.Field(..., description="Configured Oracle host", validate_default=True),
        ]
        oracle_service: Annotated[
            str,
            u.Field(
                ..., description="Configured Oracle service name", validate_default=True
            ),
        ]

    class ProcessingSummary(m.ArbitraryTypesModel):
        """Singer batch processing summary payload."""

        messages_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                ...,
                description="Total Singer messages processed",
                validate_default=True,
            ),
        ]
        streams: Annotated[
            t.StrSequence,
            u.Field(
                ...,
                description="Singer stream names seen during processing",
                validate_default=True,
            ),
        ] = u.Field(default_factory=tuple, validate_default=True)
        state: Annotated[
            m.Meltano.SingerStateMessage,
            u.Field(
                ...,
                description="Accumulated Singer STATE payload",
                validate_default=True,
            ),
        ] = u.Field(
            default_factory=lambda: m.Meltano.SingerStateMessage(
                type="STATE",
                value={},
            ),
            validate_default=True,
        )

    class LoaderOperation(m.ArbitraryTypesModel):
        """Detailed load operation summary for all streams."""

        stream_name: Annotated[
            str,
            u.Field(
                ..., description="Logical stream identifier", validate_default=True
            ),
        ]
        started_at: Annotated[
            str,
            u.Field(
                ..., description="Load operation start timestamp", validate_default=True
            ),
        ]
        completed_at: Annotated[
            str,
            u.Field(
                ...,
                description="Load operation completion timestamp",
                validate_default=True,
            ),
        ]
        records_loaded: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Number of loaded records", validate_default=True),
        ]
        records_failed: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Number of failed records", validate_default=True),
        ]

    class LoaderFinalizeResult(m.ArbitraryTypesModel):
        """Loader finalization payload for flush operations."""

        total_records: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Total records processed", validate_default=True),
        ]
        streams_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                ...,
                description="Number of processed streams",
                validate_default=True,
            ),
        ]
        status: Annotated[
            Literal["completed"],
            u.Field(
                ...,
                description="Finalization status",
                validate_default=True,
            ),
        ] = "completed"
        loading_operation: FlextTargetOracleModelsResults.LoaderOperation = u.Field(
            ...,
            description="Aggregated loading operation details",
            validate_default=True,
        )
        buffer_status: Annotated[
            t.MappingKV[str, int],
            u.Field(
                ...,
                description="Remaining buffered records by stream",
                validate_default=True,
            ),
        ] = u.Field(default_factory=_default_buffer_status, validate_default=True)

    class ImplementationMetrics(m.ArbitraryTypesModel):
        """Oracle target implementation metrics."""

        streams_configured: Annotated[
            t.NonNegativeInt,
            u.Field(
                ...,
                description="Number of configured streams",
                validate_default=True,
            ),
        ]
        batch_size: Annotated[
            t.BatchSize,
            u.Field(..., description="Configured batch size", validate_default=True),
        ]
        use_bulk_operations: Annotated[
            bool,
            u.Field(
                ...,
                description="Whether bulk operations are enabled",
                validate_default=True,
            ),
        ]

    class LoadStatisticsModel(m.ArbitraryTypesModel):
        """Statistics for data load operation."""

        stream_name: Annotated[
            str, u.Field(..., description="Stream identifier", validate_default=True)
        ]
        total_records_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                ...,
                description="Total processed records",
                validate_default=True,
            ),
        ]
        successful_records: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Successful records", validate_default=True),
        ]
        failed_records: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Failed records", validate_default=True),
        ]
        batches_processed: Annotated[
            t.NonNegativeInt,
            u.Field(..., description="Processed batch count", validate_default=True),
        ]

        def finalize(self) -> Self:
            """Finalize statistics and return self."""
            return self
