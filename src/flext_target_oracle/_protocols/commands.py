# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/commands
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

from flext_target_oracle import c, t


class FlextTargetOracleProtocolsCommands:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class OracleTargetAboutCommand(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        @property
        def command_type(self) -> t.NonEmptyStr:
            """Command discriminator for target metadata queries."""
            ...

        @property
        def command_id(self) -> t.NonEmptyStr:
            """Stable identifier for the target metadata command."""
            ...

        @property
        def issuer_id(self) -> t.NonEmptyStr | None:
            """Identity of the principal that issued this command."""
            ...

        @property
        def format(self) -> str:
            """Output format for about command response."""
            ...

    @runtime_checkable
    class OracleTargetLoadCommand(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        @property
        def command_type(self) -> t.NonEmptyStr:
            """Command discriminator for target load preparation."""
            ...

        @property
        def command_id(self) -> t.NonEmptyStr:
            """Stable identifier for the target load command."""
            ...

        @property
        def issuer_id(self) -> t.NonEmptyStr | None:
            """Identity of the principal that issued this command."""
            ...

        @property
        def config_file(self) -> str | None:
            """Path to JSON configuration file for target settings."""
            ...

        @property
        def state_file(self) -> str | None:
            """Path to Singer state file for incremental loads."""
            ...

    @runtime_checkable
    class OracleTargetValidateCommand(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        @property
        def command_type(self) -> t.NonEmptyStr:
            """Command discriminator for target validation."""
            ...

        @property
        def command_id(self) -> t.NonEmptyStr:
            """Stable identifier for the target validation command."""
            ...

        @property
        def issuer_id(self) -> t.NonEmptyStr | None:
            """Identity of the principal that issued this command."""
            ...

        @property
        def config_file(self) -> str | None:
            """Path to JSON configuration file to validate."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsCommands",
]
