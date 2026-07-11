"""Command models for Oracle target operations."""

from __future__ import annotations

from typing import Annotated

# NOTE (multi-agent): mro-rn88 — layer-m models import ONLY external facades + the
# constants submodule (never the own package facade at runtime), which dissolves the
# models→utilities→client circular import. Execution moved to FlextTargetOracleService.
from flext_meltano import m, u
from flext_target_oracle.constants import c


class FlextTargetOracleModelsCommands:
    """Command models MRO mixin for TargetOracle namespace."""

    class OracleTargetAboutCommand(m.Command):
        """Command to return target metadata and capabilities."""

        format: Annotated[
            str,
            u.Field(
                description="Output format for about command response",
            ),
        ] = "json"

    class OracleTargetLoadCommand(m.Command):
        """Command to prepare target for data loading."""

        config_file: Annotated[
            str | None,
            u.Field(
                description="Path to JSON configuration file for target settings",
            ),
        ] = None
        state_file: Annotated[
            str | None,
            u.Field(
                description="Path to Singer state file for incremental loads",
            ),
        ] = None

    class OracleTargetValidateCommand(m.Command):
        """Command to validate target configuration."""

        config_file: Annotated[
            str | None,
            u.Field(
                description="Path to JSON configuration file to validate",
            ),
        ] = None

    class OracleTargetCommandFactory:
        """Create Oracle target command objects."""

        @staticmethod
        def create_about_command(
            output_format: str = "json",
        ) -> FlextTargetOracleModelsCommands.OracleTargetAboutCommand:
            """Create about command instance."""
            return FlextTargetOracleModelsCommands.OracleTargetAboutCommand(
                command_type=c.TargetOracle.COMMAND_TYPE_ABOUT,
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
                command_type=c.TargetOracle.COMMAND_TYPE_LOAD,
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
                command_type=c.TargetOracle.COMMAND_TYPE_VALIDATE,
                command_id="cmd_oracle_validate",
                config_file=config_file,
            )
