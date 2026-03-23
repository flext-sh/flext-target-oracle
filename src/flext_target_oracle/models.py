"""Models for Oracle target operations."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal, Protocol, Self, override

from flext_core import FlextModels, h, r, t
from flext_db_oracle.models import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels
from pydantic import Field, TypeAdapter

from flext_target_oracle.constants import FlextTargetOracleConstants


class _OracleSettingsProtocol(Protocol):
    """Protocol for Oracle settings used by command classes."""

    def validate_business_rules(self) -> r[bool]:
        """Validate Oracle target configuration business rules."""
        ...


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
                t.NonNegativeInt,
                Field(
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
                    default_factory=lambda: (
                        FlextMeltanoModels.Meltano.SingerStateMessage(
                            type="STATE", value={}
                        )
                    ),
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
                t.NonNegativeInt,
                Field(description="Number of loaded records"),
            ]
            records_failed: Annotated[
                t.NonNegativeInt,
                Field(description="Number of failed records"),
            ]

        class LoaderFinalizeResult(FlextModels.ArbitraryTypesModel):
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
                t.PortNumber,
                Field(description="Oracle database port"),
            ]
            service_name: Annotated[str, Field(description="Oracle service name")]
            username: Annotated[str, Field(description="Oracle database username")]
            password: Annotated[str, Field(description="Oracle database password")]
            timeout: Annotated[
                t.PositiveInt,
                Field(description="Connection timeout in seconds"),
            ]
            pool_min: Annotated[
                t.PositiveInt,
                Field(description="Oracle connection pool minimum"),
            ]
            pool_max: Annotated[
                t.PositiveInt,
                Field(description="Oracle connection pool maximum"),
            ]
            pool_increment: Annotated[
                t.PositiveInt,
                Field(
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
                t.PositiveInt,
                Field(
                    default=1,
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
            batch_size: Annotated[t.BatchSize, Field(description="Target batch size")]
            table_prefix: Annotated[str, Field(description="Target table name prefix")]
            table_suffix: Annotated[str, Field(description="Target table name suffix")]

        class ImplementationMetrics(FlextModels.ArbitraryTypesModel):
            """Oracle target implementation metrics."""

            streams_configured: Annotated[
                t.NonNegativeInt,
                Field(
                    description="Number of configured streams",
                ),
            ]
            batch_size: Annotated[
                t.BatchSize, Field(description="Configured batch size")
            ]
            use_bulk_operations: Annotated[
                bool,
                Field(
                    description="Whether bulk operations are enabled",
                ),
            ]

        class OracleConnectionModel(OracleConnectionConfig):
            """Oracle database connection configuration model."""

        class SingerStreamModel(FlextModels.ArbitraryTypesModel):
            """Singer stream mapping to Oracle table with column configuration."""

            stream_name: Annotated[str, Field(description="Singer stream name")]
            table_name: Annotated[
                str, Field(description="Oracle destination table name")
            ]
            ignored_columns: Annotated[
                list[str],
                Field(
                    default_factory=list,
                    description="Columns ignored during record transformation",
                ),
            ]
            column_mappings: Annotated[
                dict[str, str],
                Field(
                    default_factory=dict,
                    description="Singer column to Oracle column mapping",
                ),
            ]

        class LoadStatisticsModel(FlextModels.ArbitraryTypesModel):
            """Statistics for data load operation."""

            stream_name: Annotated[str, Field(description="Stream identifier")]
            total_records_processed: Annotated[
                int,
                Field(
                    ge=0,
                    description="Total processed records",
                ),
            ]
            successful_records: Annotated[
                int, Field(ge=0, description="Successful records")
            ]
            failed_records: Annotated[int, Field(ge=0, description="Failed records")]
            batches_processed: Annotated[
                int, Field(ge=0, description="Processed batch count")
            ]

            def finalize(self) -> Self:
                """Finalize statistics and return self."""
                return self

        class OracleTargetAboutCommand(FlextModels.Command):
            """Command to return target metadata and capabilities."""

            format: str = "json"

            def execute(self) -> r[str]:
                """Execute about command returning target information."""
                payload: dict[str, str] = {
                    "name": "flext-target-oracle",
                    "description": "Singer target for Oracle loading",
                    "format": self.format,
                }
                if (
                    self.format
                    == FlextTargetOracleConstants.TargetOracle.OutputFormats.TEXT
                ):
                    return r[str].ok("flext-target-oracle")
                return r[str].ok(
                    TypeAdapter(dict[str, str]).dump_json(payload).decode("utf-8")
                )

        class OracleTargetLoadCommand(FlextModels.Command):
            """Command to prepare target for data loading."""

            config_file: str | None = None
            state_file: str | None = None

            def execute(self) -> r[str]:
                """Execute load command to initialize target."""
                settings_result = _load_target_settings(self.config_file)
                if settings_result.is_failure:
                    return r[str].fail(settings_result.error or "Invalid settings")
                _ = self.state_file
                return r[str].ok("load_ready")

        class OracleTargetValidateCommand(FlextModels.Command):
            """Command to validate target configuration."""

            config_file: str | None = None

            def execute(self) -> r[str]:
                """Execute validation of target configuration."""
                settings_result = _load_target_settings(self.config_file)
                if settings_result.is_failure:
                    return r[str].fail(
                        settings_result.error or "Configuration validation failed",
                    )
                settings: _OracleSettingsProtocol = settings_result.value
                validation_result = settings.validate_business_rules()
                if validation_result.is_failure:
                    return r[str].fail(
                        validation_result.error or "Configuration validation failed",
                    )
                return r[str].ok("validation_ok")

        class OracleTargetCommandHandler(h[FlextModels.Command, str]):
            """Dispatch command objects to their `execute` implementation."""

            @override
            def handle(
                self,
                message: FlextModels.Command,
            ) -> r[str]:
                """Invoke command execute methods in a typed-safe way."""
                if isinstance(
                    message,
                    FlextTargetOracleModels.TargetOracle.OracleTargetAboutCommand
                    | FlextTargetOracleModels.TargetOracle.OracleTargetLoadCommand
                    | FlextTargetOracleModels.TargetOracle.OracleTargetValidateCommand,
                ):
                    return message.execute()
                return r[str].fail(f"Unsupported command: {type(message).__name__}")

        class OracleTargetCommandFactory:
            """Create Oracle target command objects."""

            @staticmethod
            def create_about_command(
                output_format: str = "json",
            ) -> FlextTargetOracleModels.TargetOracle.OracleTargetAboutCommand:
                """Create about command instance."""
                return FlextTargetOracleModels.TargetOracle.OracleTargetAboutCommand(
                    command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.ABOUT.value,
                    command_id="cmd_oracle_about",
                    format=output_format,
                )

            @staticmethod
            def create_load_command(
                config_file: str | None = None,
                state_file: str | None = None,
            ) -> FlextTargetOracleModels.TargetOracle.OracleTargetLoadCommand:
                """Create load command instance."""
                return FlextTargetOracleModels.TargetOracle.OracleTargetLoadCommand(
                    command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.LOAD.value,
                    command_id="cmd_oracle_load",
                    config_file=config_file,
                    state_file=state_file,
                )

            @staticmethod
            def create_validate_command(
                config_file: str | None = None,
            ) -> FlextTargetOracleModels.TargetOracle.OracleTargetValidateCommand:
                """Create validate command instance."""
                return FlextTargetOracleModels.TargetOracle.OracleTargetValidateCommand(
                    command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.VALIDATE.value,
                    command_id="cmd_oracle_validate",
                    config_file=config_file,
                )


def _load_target_settings(config_file: str | None) -> r[_OracleSettingsProtocol]:
    """Load settings from JSON file or environment defaults."""
    from flext_target_oracle.settings import FlextTargetOracleSettings  # noqa: PLC0415

    result_type: type[r[_OracleSettingsProtocol]] = r[_OracleSettingsProtocol]
    if config_file is None:
        return result_type.ok(FlextTargetOracleSettings.model_validate({}))
    config_path = Path(config_file)
    if not config_path.exists():
        return result_type.fail(f"Configuration file not found: {config_file}")
    try:
        content = config_path.read_text(encoding="utf-8")
        settings = FlextTargetOracleSettings.model_validate_json(content)
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ) as exc:
        return result_type.fail(f"Invalid configuration file: {exc}")
    return result_type.ok(settings)


m = FlextTargetOracleModels

__all__ = ["FlextTargetOracleModels", "m"]
