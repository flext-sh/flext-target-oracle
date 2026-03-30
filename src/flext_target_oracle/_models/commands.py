"""Command models for Oracle target operations."""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import h, r
from flext_meltano import FlextMeltanoModels
from pydantic import TypeAdapter

from flext_target_oracle import (
    FlextTargetOracleConstants,
    FlextTargetOracleModelsConfig,
    FlextTargetOracleSettings,
    c,
    t,
)

_STR_MAP_ADAPTER: TypeAdapter[t.StrMapping] = TypeAdapter(t.StrMapping)


def load_target_settings(
    config_file: str | None,
) -> r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]:
    """Load settings from JSON file or environment defaults."""
    result_type: type[r[FlextTargetOracleModelsConfig.OracleSettingsProtocol]] = r[
        FlextTargetOracleModelsConfig.OracleSettingsProtocol
    ]
    if config_file is None:
        return result_type.ok(FlextTargetOracleSettings.model_validate({}))
    config_path = Path(config_file)
    if not config_path.exists():
        return result_type.fail(f"Configuration file not found: {config_file}")
    try:
        content = config_path.read_text(encoding="utf-8")
        settings = FlextTargetOracleSettings.model_validate_json(content)
    except c.Meltano.Singer.SAFE_EXCEPTIONS as exc:
        return result_type.fail(f"Invalid configuration file: {exc}")
    return result_type.ok(settings)


class FlextTargetOracleModelsCommands:
    """Command models MRO mixin for TargetOracle namespace."""

    class OracleTargetAboutCommand(FlextMeltanoModels.Command):
        """Command to return target metadata and capabilities."""

        format: str = "json"

        def execute(self) -> r[str]:
            """Execute about command returning target information."""
            payload: t.StrMapping = {
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
                _STR_MAP_ADAPTER.dump_json(payload).decode("utf-8"),
            )

    class OracleTargetLoadCommand(FlextMeltanoModels.Command):
        """Command to prepare target for data loading."""

        config_file: str | None = None
        state_file: str | None = None

        def execute(self) -> r[str]:
            """Execute load command to initialize target."""
            settings_result = load_target_settings(self.config_file)
            if settings_result.is_failure:
                return r[str].fail(settings_result.error or "Invalid settings")
            _ = self.state_file
            return r[str].ok("load_ready")

    class OracleTargetValidateCommand(FlextMeltanoModels.Command):
        """Command to validate target configuration."""

        config_file: str | None = None

        def execute(self) -> r[str]:
            """Execute validation of target configuration."""
            settings_result = load_target_settings(self.config_file)
            if settings_result.is_failure:
                return r[str].fail(
                    settings_result.error or "Configuration validation failed",
                )
            settings: FlextTargetOracleModelsConfig.OracleSettingsProtocol = (
                settings_result.value
            )
            validation_result = settings.validate_business_rules()
            if validation_result.is_failure:
                return r[str].fail(
                    validation_result.error or "Configuration validation failed",
                )
            return r[str].ok("validation_ok")

    class OracleTargetCommandHandler(h[FlextMeltanoModels.Command, str]):
        """Dispatch command objects to their `execute` implementation."""

        @override
        def handle(
            self,
            message: FlextMeltanoModels.Command,
        ) -> r[str]:
            """Invoke command execute methods in a typed-safe way."""
            if isinstance(
                message,
                FlextTargetOracleModelsCommands.OracleTargetAboutCommand
                | FlextTargetOracleModelsCommands.OracleTargetLoadCommand
                | FlextTargetOracleModelsCommands.OracleTargetValidateCommand,
            ):
                return message.execute()
            return r[str].fail(f"Unsupported command: {type(message).__name__}")

    class OracleTargetCommandFactory:
        """Create Oracle target command objects."""

        @staticmethod
        def create_about_command(
            output_format: str = "json",
        ) -> FlextTargetOracleModelsCommands.OracleTargetAboutCommand:
            """Create about command instance."""
            return FlextTargetOracleModelsCommands.OracleTargetAboutCommand(
                command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.ABOUT.value,
                command_id="cmd_oracle_about",
                format=output_format,
            )

        @staticmethod
        def create_load_command(
            config_file: str | None = None,
            state_file: str | None = None,
        ) -> FlextTargetOracleModelsCommands.OracleTargetLoadCommand:
            """Create load command instance."""
            return FlextTargetOracleModelsCommands.OracleTargetLoadCommand(
                command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.LOAD.value,
                command_id="cmd_oracle_load",
                config_file=config_file,
                state_file=state_file,
            )

        @staticmethod
        def create_validate_command(
            config_file: str | None = None,
        ) -> FlextTargetOracleModelsCommands.OracleTargetValidateCommand:
            """Create validate command instance."""
            return FlextTargetOracleModelsCommands.OracleTargetValidateCommand(
                command_type=FlextTargetOracleConstants.TargetOracle.CommandTypes.VALIDATE.value,
                command_id="cmd_oracle_validate",
                config_file=config_file,
            )
