"""Models for Oracle target operations."""

from __future__ import annotations

from typing import Annotated, Literal

from flext_core import FlextModels
from flext_db_oracle.models import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels
from pydantic import Field


class FlextTargetOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Complete models for Oracle target operations extending FlextModels."""

    class Meltano(FlextMeltanoModels.Meltano):
        """Namespaced Meltano runtime model references (inherits all Singer types)."""

    class TargetOracle:
        """TargetOracle domain namespace."""

        class SingerSchemaMessage(FlextMeltanoModels.Meltano.SingerSchemaMessage):
            """Singer SCHEMA message specialized for Oracle target domain."""

        class SingerRecordMessage(FlextMeltanoModels.Meltano.SingerRecordMessage):
            """Singer RECORD message specialized for Oracle target domain."""

        class SingerStateMessage(FlextMeltanoModels.Meltano.SingerStateMessage):
            """Singer STATE message specialized for Oracle target domain."""

        class SingerActivateVersionMessage(
            FlextMeltanoModels.Meltano.SingerActivateVersionMessage,
        ):
            """Singer ACTIVATE_VERSION message specialized for Oracle target domain."""

        class SingerCatalogMetadata(FlextMeltanoModels.Meltano.SingerCatalogMetadata):
            """Singer catalog metadata specialized for Oracle target domain."""

        class SingerCatalogEntry(FlextMeltanoModels.Meltano.SingerCatalogEntry):
            """Singer catalog entry specialized for Oracle target domain."""

        class SingerCatalog(FlextMeltanoModels.Meltano.SingerCatalog):
            """Singer catalog specialized for Oracle target domain."""

        class ExecuteResult(FlextModels.ArbitraryTypesModel):
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

        class ProcessingSummary(FlextModels.ArbitraryTypesModel):
            """Singer batch processing summary payload."""

            messages_processed: Annotated[
                int,
                Field(
                    ge=0,
                    description="Total Singer messages processed",
                ),
            ]
            streams: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="Singer stream names seen during processing",
                ),
            ]
            state: Annotated[
                FlextMeltanoModels.Meltano.SingerStateMessage,
                Field(
                    default_factory=FlextMeltanoModels.Meltano.SingerStateMessage,
                    description="Accumulated Singer STATE payload",
                ),
            ]

        class LoaderReadyResult(FlextModels.ArbitraryTypesModel):
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

        class LoaderOperation(FlextModels.ArbitraryTypesModel):
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
                int,
                Field(ge=0, description="Number of loaded records"),
            ]
            records_failed: Annotated[
                int,
                Field(ge=0, description="Number of failed records"),
            ]

        class LoaderFinalizeResult(FlextModels.ArbitraryTypesModel):
            """Loader finalization payload for flush operations."""

            total_records: Annotated[
                int,
                Field(ge=0, description="Total records processed"),
            ]
            streams_processed: Annotated[
                int,
                Field(
                    ge=0,
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
            loading_operation: FlextTargetOracleModels.TargetOracle.LoaderOperation = (
                Field(
                    description="Aggregated loading operation details",
                )
            )
            buffer_status: Annotated[
                dict[str, int],
                Field(
                    default_factory=dict,
                    description="Remaining buffered records by stream",
                ),
            ]

        class OracleConnectionConfig(FlextModels.ArbitraryTypesModel):
            """Oracle connection configuration payload."""

            host: Annotated[str, Field(description="Oracle database host")]
            port: Annotated[
                int,
                Field(ge=1, le=65535, description="Oracle database port"),
            ]
            service_name: Annotated[str, Field(description="Oracle service name")]
            username: Annotated[str, Field(description="Oracle database username")]
            password: Annotated[str, Field(description="Oracle database password")]
            timeout: Annotated[
                int,
                Field(ge=1, description="Connection timeout in seconds"),
            ]
            pool_min: Annotated[
                int,
                Field(ge=1, description="Oracle connection pool minimum"),
            ]
            pool_max: Annotated[
                int,
                Field(ge=1, description="Oracle connection pool maximum"),
            ]
            pool_increment: Annotated[
                int,
                Field(
                    ge=1,
                    description="Oracle connection pool increment",
                ),
            ]
            encoding: Annotated[str, Field(description="Oracle connection encoding")]
            ssl_enabled: Annotated[bool, Field(description="Whether SSL is enabled")]
            autocommit: Annotated[
                bool,
                Field(description="Whether autocommit is enabled"),
            ]
            use_bulk_operations: Annotated[
                bool,
                Field(
                    default=False,
                    description="Whether bulk operations are enabled",
                ),
            ]
            parallel_degree: Annotated[
                int,
                Field(
                    default=1,
                    ge=1,
                    description="Oracle parallel execution degree",
                ),
            ]

        class TargetConfig(FlextModels.ArbitraryTypesModel):
            """Target runtime configuration payload."""

            default_target_schema: Annotated[
                str,
                Field(
                    description="Default Oracle target schema",
                ),
            ]
            use_bulk_operations: Annotated[
                bool,
                Field(
                    description="Whether bulk loading is enabled",
                ),
            ]
            batch_size: Annotated[int, Field(ge=1, description="Target batch size")]
            table_prefix: Annotated[str, Field(description="Target table name prefix")]
            table_suffix: Annotated[str, Field(description="Target table name suffix")]

        class ImplementationMetrics(FlextModels.ArbitraryTypesModel):
            """Oracle target implementation metrics."""

            streams_configured: Annotated[
                int,
                Field(
                    ge=0,
                    description="Number of configured streams",
                ),
            ]
            batch_size: Annotated[int, Field(ge=1, description="Configured batch size")]
            use_bulk_operations: Annotated[
                bool,
                Field(
                    description="Whether bulk operations are enabled",
                ),
            ]


m = FlextTargetOracleModels

__all__ = ["FlextTargetOracleModels", "m"]
