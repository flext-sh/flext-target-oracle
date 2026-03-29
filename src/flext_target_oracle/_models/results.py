"""Result and payload models for Oracle target operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal, Self

from flext_meltano import FlextMeltanoModels
from pydantic import Field

from flext_target_oracle import t


class FlextTargetOracleModelsResults:
    """Result models MRO mixin for TargetOracle namespace."""

    class ExecuteResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Target execute readiness payload."""

        name: Annotated[str, Field(description="Target package name")]
        status: Annotated[
            Literal["ready"],
            Field(
                default="ready",
                description="Target readiness status",
            ),
        ]
        oracle_host: Annotated[str, Field(description="Configured Oracle host")]
        oracle_service: Annotated[
            str,
            Field(description="Configured Oracle service name"),
        ]

    class ProcessingSummary(FlextMeltanoModels.ArbitraryTypesModel):
        """Singer batch processing summary payload."""

        messages_processed: Annotated[
            t.NonNegativeInt,
            Field(
                description="Total Singer messages processed",
            ),
        ]
        streams: Annotated[
            t.StrSequence,
            Field(
                description="Singer stream names seen during processing",
            ),
        ] = Field(default_factory=list)
        state: Annotated[
            FlextMeltanoModels.Meltano.SingerStateMessage,
            Field(
                description="Accumulated Singer STATE payload",
            ),
        ] = Field(
            default_factory=lambda: FlextMeltanoModels.Meltano.SingerStateMessage(
                type="STATE",
                value={},
            )
        )

    class LoaderReadyResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Loader readiness payload after Oracle connectivity checks."""

        status: Annotated[
            Literal["ready"],
            Field(
                default="ready",
                description="Loader readiness status",
            ),
        ]
        host: Annotated[str, Field(description="Configured Oracle host")]
        service: Annotated[str, Field(description="Configured Oracle service name")]
        target_schema: Annotated[
            str,
            Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Configured Oracle target schema",
            ),
        ]

    class LoaderOperation(FlextMeltanoModels.ArbitraryTypesModel):
        """Detailed load operation summary for all streams."""

        stream_name: Annotated[str, Field(description="Logical stream identifier")]
        started_at: Annotated[
            str,
            Field(description="Load operation start timestamp"),
        ]
        completed_at: Annotated[
            str,
            Field(description="Load operation completion timestamp"),
        ]
        records_loaded: Annotated[
            t.NonNegativeInt,
            Field(description="Number of loaded records"),
        ]
        records_failed: Annotated[
            t.NonNegativeInt,
            Field(description="Number of failed records"),
        ]

    class LoaderFinalizeResult(FlextMeltanoModels.ArbitraryTypesModel):
        """Loader finalization payload for flush operations."""

        total_records: Annotated[
            t.NonNegativeInt,
            Field(description="Total records processed"),
        ]
        streams_processed: Annotated[
            t.NonNegativeInt,
            Field(
                description="Number of processed streams",
            ),
        ]
        status: Annotated[
            Literal["completed"],
            Field(
                default="completed",
                description="Finalization status",
            ),
        ]
        loading_operation: FlextTargetOracleModelsResults.LoaderOperation = Field(
            description="Aggregated loading operation details",
        )
        buffer_status: Annotated[
            Mapping[str, int],
            Field(
                description="Remaining buffered records by stream",
            ),
        ] = Field(default_factory=dict)

    class ImplementationMetrics(FlextMeltanoModels.ArbitraryTypesModel):
        """Oracle target implementation metrics."""

        streams_configured: Annotated[
            t.NonNegativeInt,
            Field(
                description="Number of configured streams",
            ),
        ]
        batch_size: Annotated[
            t.BatchSize,
            Field(description="Configured batch size"),
        ]
        use_bulk_operations: Annotated[
            bool,
            Field(
                description="Whether bulk operations are enabled",
            ),
        ]

    class LoadStatisticsModel(FlextMeltanoModels.ArbitraryTypesModel):
        """Statistics for data load operation."""

        stream_name: Annotated[str, Field(description="Stream identifier")]
        total_records_processed: Annotated[
            t.NonNegativeInt,
            Field(
                description="Total processed records",
            ),
        ]
        successful_records: Annotated[
            t.NonNegativeInt,
            Field(description="Successful records"),
        ]
        failed_records: Annotated[
            t.NonNegativeInt,
            Field(description="Failed records"),
        ]
        batches_processed: Annotated[
            t.NonNegativeInt,
            Field(description="Processed batch count"),
        ]

        def finalize(self) -> Self:
            """Finalize statistics and return self."""
            return self
