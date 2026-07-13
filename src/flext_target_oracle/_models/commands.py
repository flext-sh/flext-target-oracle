"""Command models for Oracle target operations."""

from __future__ import annotations

from typing import Annotated

# NOTE (multi-agent): mro-rn88 — layer-m models import ONLY external facades + the
# constants submodule (never the own package facade at runtime), which dissolves the
# models→utilities→client circular import. Execution moved to FlextTargetOracleService.
from flext_meltano import m, t, u
from flext_target_oracle import c


class FlextTargetOracleModelsCommands:
    """Command models MRO mixin for TargetOracle namespace."""

    # NOTE (multi-agent): mro-wgwh.2 — flext-law §2a: command identity is declarative
    # field default (Pydantic 2-way direct construction); OracleTargetCommandFactory
    # deleted — models facet carries zero methods.
    class OracleTargetAboutCommand(m.Command):
        """Command to return target metadata and capabilities."""

        command_type: t.NonEmptyStr = c.TargetOracle.COMMAND_TYPE_ABOUT
        command_id: t.NonEmptyStr = "cmd_oracle_about"
        format: Annotated[
            str,
            u.Field(
                description="Output format for about command response",
            ),
        ] = "json"

    class OracleTargetLoadCommand(m.Command):
        """Command to prepare target for data loading."""

        command_type: t.NonEmptyStr = c.TargetOracle.COMMAND_TYPE_LOAD
        command_id: t.NonEmptyStr = "cmd_oracle_load"
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

        command_type: t.NonEmptyStr = c.TargetOracle.COMMAND_TYPE_VALIDATE
        command_id: t.NonEmptyStr = "cmd_oracle_validate"
        config_file: Annotated[
            str | None,
            u.Field(
                description="Path to JSON configuration file to validate",
            ),
        ] = None
