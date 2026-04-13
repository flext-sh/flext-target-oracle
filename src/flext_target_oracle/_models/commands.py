"""Command models for Oracle target operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, override

from pydantic import Field

from flext_meltano import m
from flext_target_oracle import (
    FlextTargetOracleConstants,
    h,
    r,
    t,
    u,
)

if TYPE_CHECKING:
    from flext_target_oracle import p


class FlextTargetOracleModelsCommands:
    """Command models MRO mixin for TargetOracle namespace."""

    class OracleTargetAboutCommand(m.Command):
        """Command to return target metadata and capabilities."""

        format: Annotated[
            str,
            Field(
                default="json",
                description="Output format for about command response",
            ),
        ]

        def execute(self) -> p.Result[str]:
            """Execute about command returning target information."""
            payload: t.StrMapping = {
                "name": "flext-target-oracle",
                "description": "Singer target for Oracle loading",
                "format": self.format,
            }
            if (
                self.format
                == FlextTargetOracleConstants.TargetOracle.OUTPUT_FORMAT_TEXT
            ):
                return r[str].ok("flext-target-oracle")
            return r[str].ok(
                t.TargetOracle.STR_MAP_ADAPTER.dump_json(payload).decode("utf-8"),
            )

    class OracleTargetLoadCommand(m.Command):
        """Command to prepare target for data loading."""

        config_file: Annotated[
            str | None,
            Field(
                default=None,
                description="Path to JSON configuration file for target settings",
            ),
        ]
        state_file: Annotated[
            str | None,
            Field(
                default=None,
                description="Path to Singer state file for incremental loads",
            ),
        ]

        def execute(self) -> p.Result[str]:
            """Execute load command to initialize target."""
            settings_result = u.TargetOracle.load_target_settings(self.config_file)
            if settings_result.failure:
                return r[str].fail(settings_result.error or "Invalid settings")
            _ = self.state_file
            return r[str].ok("load_ready")

    class OracleTargetValidateCommand(m.Command):
        """Command to validate target configuration."""

        config_file: Annotated[
            str | None,
            Field(
                default=None,
                description="Path to JSON configuration file to validate",
            ),
        ]

        def execute(self) -> p.Result[str]:
            """Execute validation of target configuration."""
            settings_result = u.TargetOracle.load_target_settings(self.config_file)
            if settings_result.failure:
                return r[str].fail(
                    settings_result.error or "Configuration validation failed",
                )
            settings: p.TargetOracle.OracleSettingsProtocol = settings_result.value
            validation_result = settings.validate_business_rules()
            if validation_result.failure:
                return r[str].fail(
                    validation_result.error or "Configuration validation failed",
                )
            return r[str].ok("validation_ok")

    class OracleTargetCommandHandler(h[m.Command, str]):
        """Dispatch command objects to their `execute` implementation."""

        @override
        def handle(
            self,
            message: m.Command,
        ) -> p.Result[str]:
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
                command_type=FlextTargetOracleConstants.TargetOracle.COMMAND_TYPE_ABOUT,
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
                command_type=FlextTargetOracleConstants.TargetOracle.COMMAND_TYPE_LOAD,
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
                command_type=FlextTargetOracleConstants.TargetOracle.COMMAND_TYPE_VALIDATE,
                command_id="cmd_oracle_validate",
                config_file=config_file,
            )
