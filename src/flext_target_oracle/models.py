"""Models for Oracle target operations."""

from __future__ import annotations

from typing import Literal

from flext_core import FlextModels, FlextTypes as t
from flext_core.utilities import u as flext_u
from flext_meltano import FlextMeltanoModels
from pydantic import Field


class FlextTargetOracleModels(FlextModels):
    """Complete models for Oracle target operations extending FlextModels."""

    class Meltano(FlextMeltanoModels.Meltano):
        """Namespaced Meltano runtime model references (inherits all Singer types)."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextTargetOracleModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        flext_u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextTargetOracleModels is deprecated. Use FlextModels directly with composition instead.",
        )

    class TargetOracle:
        """TargetOracle domain namespace."""

        class SingerSchemaMessage(FlextMeltanoModels.Meltano.SingerSchemaMessage):
            """Singer SCHEMA message specialized for Oracle target domain."""

        class SingerRecordMessage(FlextMeltanoModels.Meltano.SingerRecordMessage):
            """Singer RECORD message specialized for Oracle target domain."""

        class SingerStateMessage(FlextMeltanoModels.Meltano.SingerStateMessage):
            """Singer STATE message specialized for Oracle target domain."""

        class SingerActivateVersionMessage(
            FlextMeltanoModels.Meltano.SingerActivateVersionMessage
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

            name: str = Field(description="Target package name")
            status: Literal["ready"] = Field(
                default="ready",
                description="Target readiness status",
            )
            oracle_host: str = Field(description="Configured Oracle host")
            oracle_service: str = Field(description="Configured Oracle service name")

        class ProcessingSummary(FlextModels.ArbitraryTypesModel):
            """Singer batch processing summary payload."""

            messages_processed: int = Field(
                ge=0,
                description="Total Singer messages processed",
            )
            streams: list[str] = Field(
                default_factory=list,
                description="Singer stream names seen during processing",
            )
            state: dict[str, t.GeneralValueType] = Field(
                default_factory=dict,
                description="Accumulated Singer STATE payload",
            )

        class LoaderReadyResult(FlextModels.ArbitraryTypesModel):
            """Loader readiness payload after Oracle connectivity checks."""

            status: Literal["ready"] = Field(
                default="ready",
                description="Loader readiness status",
            )
            host: str = Field(description="Configured Oracle host")
            service: str = Field(description="Configured Oracle service name")
            target_schema: str = Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Configured Oracle target schema",
            )

        class LoaderOperation(FlextModels.ArbitraryTypesModel):
            """Detailed load operation summary for all streams."""

            stream_name: str = Field(description="Logical stream identifier")
            started_at: str = Field(description="Load operation start timestamp")
            completed_at: str = Field(description="Load operation completion timestamp")
            records_loaded: int = Field(ge=0, description="Number of loaded records")
            records_failed: int = Field(ge=0, description="Number of failed records")

        class LoaderFinalizeResult(FlextModels.ArbitraryTypesModel):
            """Loader finalization payload for flush operations."""

            total_records: int = Field(ge=0, description="Total records processed")
            streams_processed: int = Field(
                ge=0, description="Number of processed streams"
            )
            status: Literal["completed"] = Field(
                default="completed",
                description="Finalization status",
            )
            loading_operation: FlextTargetOracleModels.TargetOracle.LoaderOperation = (
                Field(
                    description="Aggregated loading operation details",
                )
            )
            buffer_status: dict[str, int] = Field(
                default_factory=dict,
                description="Remaining buffered records by stream",
            )

        class OracleConnectionConfig(FlextModels.ArbitraryTypesModel):
            """Oracle connection configuration payload."""

            host: str = Field(description="Oracle database host")
            port: int = Field(ge=1, le=65535, description="Oracle database port")
            service_name: str = Field(description="Oracle service name")
            username: str = Field(description="Oracle database username")
            password: str = Field(description="Oracle database password")
            timeout: int = Field(ge=1, description="Connection timeout in seconds")
            pool_min: int = Field(ge=1, description="Oracle connection pool minimum")
            pool_max: int = Field(ge=1, description="Oracle connection pool maximum")
            pool_increment: int = Field(
                ge=1,
                description="Oracle connection pool increment",
            )
            encoding: str = Field(description="Oracle connection encoding")
            ssl_enabled: bool = Field(description="Whether SSL is enabled")
            autocommit: bool = Field(description="Whether autocommit is enabled")
            use_bulk_operations: bool = Field(
                default=False,
                description="Whether bulk operations are enabled",
            )
            parallel_degree: int = Field(
                default=1,
                ge=1,
                description="Oracle parallel execution degree",
            )

        class TargetConfig(FlextModels.ArbitraryTypesModel):
            """Target runtime configuration payload."""

            default_target_schema: str = Field(
                description="Default Oracle target schema"
            )
            use_bulk_operations: bool = Field(
                description="Whether bulk loading is enabled",
            )
            batch_size: int = Field(ge=1, description="Target batch size")
            table_prefix: str = Field(description="Target table name prefix")
            table_suffix: str = Field(description="Target table name suffix")

        class ImplementationMetrics(FlextModels.ArbitraryTypesModel):
            """Oracle target implementation metrics."""

            streams_configured: int = Field(
                ge=0,
                description="Number of configured streams",
            )
            batch_size: int = Field(ge=1, description="Configured batch size")
            use_bulk_operations: bool = Field(
                description="Whether bulk operations are enabled",
            )

    SingerSchemaMessage = TargetOracle.SingerSchemaMessage
    SingerRecordMessage = TargetOracle.SingerRecordMessage
    SingerStateMessage = TargetOracle.SingerStateMessage
    SingerActivateVersionMessage = TargetOracle.SingerActivateVersionMessage
    SingerCatalogMetadata = TargetOracle.SingerCatalogMetadata
    SingerCatalogEntry = TargetOracle.SingerCatalogEntry
    SingerCatalog = TargetOracle.SingerCatalog
    ExecuteResult = TargetOracle.ExecuteResult
    ProcessingSummary = TargetOracle.ProcessingSummary
    LoaderReadyResult = TargetOracle.LoaderReadyResult
    LoaderOperation = TargetOracle.LoaderOperation
    LoaderFinalizeResult = TargetOracle.LoaderFinalizeResult
    OracleConnectionConfig = TargetOracle.OracleConnectionConfig
    TargetConfig = TargetOracle.TargetConfig
    ImplementationMetrics = TargetOracle.ImplementationMetrics


m = FlextTargetOracleModels

ExecuteResult = FlextTargetOracleModels.TargetOracle.ExecuteResult
ImplementationMetrics = FlextTargetOracleModels.TargetOracle.ImplementationMetrics
LoaderFinalizeResult = FlextTargetOracleModels.TargetOracle.LoaderFinalizeResult
LoaderReadyResult = FlextTargetOracleModels.TargetOracle.LoaderReadyResult
OracleConnectionConfig = FlextTargetOracleModels.TargetOracle.OracleConnectionConfig
ProcessingSummary = FlextTargetOracleModels.TargetOracle.ProcessingSummary
SingerActivateVersionMessage = (
    FlextTargetOracleModels.TargetOracle.SingerActivateVersionMessage
)
SingerCatalog = FlextTargetOracleModels.TargetOracle.SingerCatalog
SingerCatalogEntry = FlextTargetOracleModels.TargetOracle.SingerCatalogEntry
SingerCatalogMetadata = FlextTargetOracleModels.TargetOracle.SingerCatalogMetadata
SingerRecordMessage = FlextTargetOracleModels.TargetOracle.SingerRecordMessage
SingerSchemaMessage = FlextTargetOracleModels.TargetOracle.SingerSchemaMessage
SingerStateMessage = FlextTargetOracleModels.TargetOracle.SingerStateMessage
TargetConfig = FlextTargetOracleModels.TargetOracle.TargetConfig

__all__ = [
    "ExecuteResult",
    "FlextTargetOracleModels",
    "ImplementationMetrics",
    "LoaderFinalizeResult",
    "LoaderReadyResult",
    "OracleConnectionConfig",
    "ProcessingSummary",
    "SingerActivateVersionMessage",
    "SingerCatalog",
    "SingerCatalogEntry",
    "SingerCatalogMetadata",
    "SingerRecordMessage",
    "SingerSchemaMessage",
    "SingerStateMessage",
    "TargetConfig",
    "m",
]
