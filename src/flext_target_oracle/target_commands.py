"""Command helpers for Oracle target CLI flows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import override

from flext_core import FlextModels, FlextResult, h, u

from .constants import c
from .settings import FlextTargetOracleSettings


class OracleTargetAboutCommand(FlextModels.Command):
    """Command to return target metadata and capabilities."""

    format: str = c.TargetOracle.OutputFormats.JSON

    def execute(self) -> FlextResult[str]:
        """Execute about command returning target information."""
        payload = {
            "name": "flext-target-oracle",
            "description": "Singer target for Oracle loading",
            "format": self.format,
        }
        if self.format == c.TargetOracle.OutputFormats.TEXT:
            return FlextResult[str].ok("flext-target-oracle")
        return FlextResult[str].ok(json.dumps(payload))


class OracleTargetLoadCommand(FlextModels.Command):
    """Command to prepare target for data loading."""

    config_file: str | None = None
    state_file: str | None = None

    def execute(self) -> FlextResult[str]:
        """Execute load command to initialize target."""
        settings_result = _load_settings(self.config_file)
        if settings_result.is_failure:
            return FlextResult[str].fail(settings_result.error or "Invalid settings")
        _ = self.state_file
        return FlextResult[str].ok("load_ready")


class OracleTargetValidateCommand(FlextModels.Command):
    """Command to validate target configuration."""

    config_file: str | None = None

    def execute(self) -> FlextResult[str]:
        """Execute validation of target configuration."""
        settings_result = _load_settings(self.config_file)
        if settings_result.is_failure:
            return FlextResult[str].fail(
                settings_result.error or "Configuration validation failed"
            )
        validation_result = settings_result.value.validate_business_rules()
        if validation_result.is_failure:
            return FlextResult[str].fail(
                validation_result.error or "Configuration validation failed"
            )
        return FlextResult[str].ok("validation_ok")


class OracleTargetCommandHandler(h[FlextModels.Command, str]):
    """Dispatch command objects to their `execute` implementation."""

    @override
    def handle(
        self,
        message: FlextModels.Command,
    ) -> FlextResult[str]:
        """Invoke command execute methods in a typed-safe way."""
        if isinstance(
            message,
            OracleTargetAboutCommand
            | OracleTargetLoadCommand
            | OracleTargetValidateCommand,
        ):
            return message.execute()
        return FlextResult[str].fail(f"Unsupported command: {type(message).__name__}")


class OracleTargetCommandFactory:
    """Create Oracle target command objects."""

    @staticmethod
    def create_about_command(
        output_format: str = c.TargetOracle.OutputFormats.JSON,
    ) -> OracleTargetAboutCommand:
        """Create about command instance."""
        return OracleTargetAboutCommand(
            command_type=c.TargetOracle.CommandTypes.ABOUT.value, format=output_format
        )

    @staticmethod
    def create_load_command(
        config_file: str | None = None, state_file: str | None = None
    ) -> OracleTargetLoadCommand:
        """Create load command instance."""
        return OracleTargetLoadCommand(
            command_type=c.TargetOracle.CommandTypes.LOAD.value,
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
            config_file=config_file,
        )


def _load_settings(config_file: str | None) -> FlextResult[FlextTargetOracleSettings]:
    """Load settings from JSON file or environment defaults."""
    if config_file is None:
        return FlextResult[FlextTargetOracleSettings].ok(FlextTargetOracleSettings())
    config_path = Path(config_file)
    if not config_path.exists():
        return FlextResult[FlextTargetOracleSettings].fail(
            f"Configuration file not found: {config_file}"
        )
    try:
        content = config_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ) as exc:
        return FlextResult[FlextTargetOracleSettings].fail(
            f"Invalid configuration file: {exc}"
        )
    if not u.is_dict_like(data):
        return FlextResult[FlextTargetOracleSettings].fail(
            "Configuration must be a JSON object"
        )
    settings = FlextTargetOracleSettings.model_validate(data)
    return FlextResult[FlextTargetOracleSettings].ok(settings)


__all__ = [
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetValidateCommand",
]
