"""Command helpers for Oracle target CLI flows."""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import FlextModels, h, r
from pydantic import TypeAdapter

from .constants import c
from .settings import FlextTargetOracleSettings


class OracleTargetAboutCommand(FlextModels.Command):
    """Command to return target metadata and capabilities."""

    format: str = c.TargetOracle.OutputFormats.JSON

    def execute(self) -> r[str]:
        """Execute about command returning target information."""
        payload = {
            "name": "flext-target-oracle",
            "description": "Singer target for Oracle loading",
            "format": self.format,
        }
        if self.format == c.TargetOracle.OutputFormats.TEXT:
            return r[str].ok("flext-target-oracle")
        return r[str].ok(TypeAdapter(dict[str, str]).dump_json(payload).decode("utf-8"))


class OracleTargetLoadCommand(FlextModels.Command):
    """Command to prepare target for data loading."""

    config_file: str | None = None
    state_file: str | None = None

    def execute(self) -> r[str]:
        """Execute load command to initialize target."""
        settings_result = _load_settings(self.config_file)
        if settings_result.is_failure:
            return r[str].fail(settings_result.error or "Invalid settings")
        _ = self.state_file
        return r[str].ok("load_ready")


class OracleTargetValidateCommand(FlextModels.Command):
    """Command to validate target configuration."""

    config_file: str | None = None

    def execute(self) -> r[str]:
        """Execute validation of target configuration."""
        settings_result = _load_settings(self.config_file)
        if settings_result.is_failure:
            return r[str].fail(
                settings_result.error or "Configuration validation failed",
            )
        validation_result = settings_result.value.validate_business_rules()
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
            OracleTargetAboutCommand
            | OracleTargetLoadCommand
            | OracleTargetValidateCommand,
        ):
            return message.execute()
        return r[str].fail(f"Unsupported command: {type(message).__name__}")


class OracleTargetCommandFactory:
    """Create Oracle target command objects."""

    @staticmethod
    def create_about_command(
        output_format: str = c.TargetOracle.OutputFormats.JSON,
    ) -> OracleTargetAboutCommand:
        """Create about command instance."""
        return OracleTargetAboutCommand(
            command_type=c.TargetOracle.CommandTypes.ABOUT.value,
            command_id="cmd_oracle_about",
            format=output_format,
        )

    @staticmethod
    def create_load_command(
        config_file: str | None = None,
        state_file: str | None = None,
    ) -> OracleTargetLoadCommand:
        """Create load command instance."""
        return OracleTargetLoadCommand(
            command_type=c.TargetOracle.CommandTypes.LOAD.value,
            command_id="cmd_oracle_load",
            config_file=config_file,
            state_file=state_file,
        )

    @staticmethod
    def create_validate_command(
        config_file: str | None = None,
    ) -> OracleTargetValidateCommand:
        """Create validation command instance."""
        return OracleTargetValidateCommand(
            command_type=c.TargetOracle.CommandTypes.VALIDATE.value,
            command_id="cmd_oracle_validate",
            config_file=config_file,
        )


def _load_settings(config_file: str | None) -> r[FlextTargetOracleSettings]:
    """Load settings from JSON file or environment defaults."""
    if config_file is None:
        return r[FlextTargetOracleSettings].ok(
            FlextTargetOracleSettings.model_validate({}),
        )
    config_path = Path(config_file)
    if not config_path.exists():
        return r[FlextTargetOracleSettings].fail(
            f"Configuration file not found: {config_file}",
        )
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
        return r[FlextTargetOracleSettings].fail(f"Invalid configuration file: {exc}")
    return r[FlextTargetOracleSettings].ok(settings)


__all__ = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
