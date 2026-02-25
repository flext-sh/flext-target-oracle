"""Command helpers for Oracle target CLI flows."""

from __future__ import annotations

import json
from pathlib import Path

from flext_core import FlextModels, FlextResult, h, u

from .settings import FlextTargetOracleSettings
from .target_client import FlextTargetOracle


class OracleTargetValidateCommand(FlextModels.Command):
    """Validate configuration and connectivity for the Oracle target."""

    config_file: str | None = None

    def execute(self) -> FlextResult[str]:
        """Validate configuration and Oracle connectivity."""
        config_result = _load_settings(self.config_file)
        if config_result.is_failure:
            return FlextResult[str].fail(config_result.error or "Config load failed")

        config = config_result.value
        if config is None:
            return FlextResult[str].fail("Configuration could not be loaded")

        validation_result = config.validate_business_rules()
        if validation_result.is_failure:
            return FlextResult[str].fail(
                validation_result.error or "Validation failed",
            )

        target = FlextTargetOracle(config)
        test_result = target.test_connection()
        if test_result.is_failure:
            return FlextResult[str].fail(test_result.error or "Connection test failed")

        return FlextResult[str].ok("Oracle target validation completed successfully")


class OracleTargetLoadCommand(FlextModels.Command):
    """Initialize Oracle target for load operations."""

    config_file: str | None = None
    state_file: str | None = None

    def execute(self) -> FlextResult[str]:
        """Initialize target and verify it is ready for loads."""
        config_result = _load_settings(self.config_file)
        if config_result.is_failure:
            return FlextResult[str].fail(config_result.error or "Config load failed")

        config = config_result.value
        if config is None:
            return FlextResult[str].fail("Configuration could not be loaded")

        target = FlextTargetOracle(config)
        init_result = target.initialize()
        if init_result.is_failure:
            return FlextResult[str].fail(
                init_result.error or "Target initialization failed",
            )

        message = "Oracle target initialized and ready for data loading"
        if self.state_file:
            message = f"{message} (state file: {self.state_file})"
        return FlextResult[str].ok(message)


class OracleTargetAboutCommand(FlextModels.Command):
    """Return metadata about this target package."""

    format: str = "json"

    def execute(self) -> FlextResult[str]:
        """Return formatted project metadata."""
        info: dict[str, str | list[str]] = {
            "name": "flext-target-oracle",
            "version": "0.9.0",
            "description": "Singer target for loading records into Oracle",
            "capabilities": ["discover", "load", "state"],
        }
        if self.format == "text":
            lines = [
                f"{info['name']} v{info['version']}",
                str(info["description"]),
                "Capabilities: " + ", ".join(info["capabilities"]),
            ]
            return FlextResult[str].ok("\n".join(lines))
        return FlextResult[str].ok(json.dumps(info, indent=2))


class OracleTargetCommandHandler(h[FlextModels.Command, str]):
    """Dispatch command objects to their `execute` implementation."""

    def handle(self, message: FlextModels.Command) -> FlextResult[str]:
        """Invoke command execute methods in a typed-safe way."""
        execute_method = getattr(message, "execute", None)
        if execute_method is None:
            return FlextResult[str].fail(
                f"Unsupported command: {type(message).__name__}"
            )
        result = execute_method()
        if not isinstance(result, FlextResult):
            return FlextResult[str].fail(
                f"Invalid result type: {type(result).__name__}"
            )
        return result


class OracleTargetCommandFactory:
    """Create Oracle target command objects."""

    @staticmethod
    def create_validate_command(
        config_file: str | None = None,
    ) -> OracleTargetValidateCommand:
        """Create validation command instance."""
        return OracleTargetValidateCommand(
            command_type="oracle_target_validate", config_file=config_file
        )

    @staticmethod
    def create_load_command(
        config_file: str | None = None,
        state_file: str | None = None,
    ) -> OracleTargetLoadCommand:
        """Create load command instance."""
        return OracleTargetLoadCommand(
            command_type="oracle_target_load",
            config_file=config_file,
            state_file=state_file,
        )

    @staticmethod
    def create_about_command(output_format: str = "json") -> OracleTargetAboutCommand:
        """Create about command instance."""
        return OracleTargetAboutCommand(
            command_type="oracle_target_about", format=output_format
        )


def _load_settings(config_file: str | None) -> FlextResult[FlextTargetOracleSettings]:
    """Load settings from JSON file or environment defaults."""
    if config_file is None:
        return FlextResult[FlextTargetOracleSettings].ok(FlextTargetOracleSettings())

    config_path = Path(config_file)
    if not config_path.exists():
        return FlextResult[FlextTargetOracleSettings].fail(
            f"Configuration file not found: {config_file}",
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
            f"Invalid configuration file: {exc}",
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
