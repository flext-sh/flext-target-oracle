"""Result and payload models for Oracle target operations."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from flext_meltano import FlextMeltanoModels
from flext_target_oracle import t, u


class FlextTargetOracleModelsResults:
    """Result models MRO mixin for TargetOracle namespace."""

    class ExecuteResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Target execute readiness payload."""

        name: Annotated[str, u.Field(description="Target package name")]
        status: Annotated[
            Literal["ready"],
            u.Field(
                description="Target readiness status",
            ),
        ] = "ready"
        oracle_host: Annotated[str, u.Field(description="Configured Oracle host")]
        oracle_service: Annotated[
            str,
            u.Field(description="Configured Oracle service name"),
        ]

    class ProcessingSummary(FlextMeltanoModels.ArbitraryTypesModel):
        """Singer batch processing summary payload."""

        messages_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="Total Singer messages processed",
            ),
        ]
        streams: Annotated[
            t.StrSequence,
            u.Field(
                description="Singer stream names seen during processing",
            ),
        ] = u.Field(default_factory=list)
        state: Annotated[
            FlextMeltanoModels.Meltano.SingerStateMessage,
            u.Field(
                description="Accumulated Singer STATE payload",
            ),
        ] = u.Field(
            default_factory=lambda: FlextMeltanoModels.Meltano.SingerStateMessage(
                type="STATE",
                value={},
            )
        )

    class LoaderReadyResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Loader readiness payload after Oracle connectivity checks."""

        status: Annotated[
            Literal["ready"],
            u.Field(
                description="Loader readiness status",
            ),
        ] = "ready"
        host: Annotated[str, u.Field(description="Configured Oracle host")]
        service: Annotated[str, u.Field(description="Configured Oracle service name")]
        target_schema: Annotated[
            str,
            u.Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Configured Oracle target schema",
            ),
        ]

    class LoaderOperation(FlextMeltanoModels.ArbitraryTypesModel):
        """Detailed load operation summary for all streams."""

        stream_name: Annotated[str, u.Field(description="Logical stream identifier")]
        started_at: Annotated[
            str,
            u.Field(description="Load operation start timestamp"),
        ]
        completed_at: Annotated[
            str,
            u.Field(description="Load operation completion timestamp"),
        ]
        records_loaded: Annotated[
            t.NonNegativeInt,
            u.Field(description="Number of loaded records"),
        ]
        records_failed: Annotated[
            t.NonNegativeInt,
            u.Field(description="Number of failed records"),
        ]

    class LoaderFinalizeResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Loader finalization payload for flush operations."""

        total_records: Annotated[
            t.NonNegativeInt,
            u.Field(description="Total records processed"),
        ]
        streams_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="Number of processed streams",
            ),
        ]
        status: Annotated[
            Literal["completed"],
            u.Field(
                description="Finalization status",
            ),
        ] = "completed"
        loading_operation: FlextTargetOracleModelsResults.LoaderOperation = u.Field(
            description="Aggregated loading operation details",
        )
        buffer_status: Annotated[
            t.IntMapping,
            u.Field(
                description="Remaining buffered records by stream",
            ),
        ] = u.Field(default_factory=dict)

    class ImplementationMetrics(FlextMeltanoModels.ArbitraryTypesModel):
        """Oracle target implementation metrics."""

        streams_configured: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="Number of configured streams",
            ),
        ]
        batch_size: Annotated[
            t.BatchSize,
            u.Field(description="Configured batch size"),
        ]
        use_bulk_operations: Annotated[
            bool,
            u.Field(
                description="Whether bulk operations are enabled",
            ),
        ]

    class LoadStatisticsModel(FlextMeltanoModels.ArbitraryTypesModel):
        """Statistics for data load operation."""

        stream_name: Annotated[str, u.Field(description="Stream identifier")]
        total_records_processed: Annotated[
            t.NonNegativeInt,
            u.Field(
                description="Total processed records",
            ),
        ]
        successful_records: Annotated[
            t.NonNegativeInt,
            u.Field(description="Successful records"),
        ]
        failed_records: Annotated[
            t.NonNegativeInt,
            u.Field(description="Failed records"),
        ]
        batches_processed: Annotated[
            t.NonNegativeInt,
            u.Field(description="Processed batch count"),
        ]

        def finalize(self) -> Self:
            """Finalize statistics and return self."""
            return self
