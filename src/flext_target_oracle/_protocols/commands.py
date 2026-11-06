# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/commands
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_target_oracle import c, t


class FlextTargetOracleProtocolsCommands:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class OracleTargetAboutCommand(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        command_type: t.NonEmptyStr
        command_id: t.NonEmptyStr
        issuer_id: t.NonEmptyStr | None
        format: str

    @runtime_checkable
    class OracleTargetLoadCommand(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        command_type: t.NonEmptyStr
        command_id: t.NonEmptyStr
        issuer_id: t.NonEmptyStr | None
        config_file: str | None
        state_file: str | None

    @runtime_checkable
    class OracleTargetValidateCommand(FlextMeltanoProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message_type(self) -> Literal[c.HandlerMode.COMMAND]:
            """Message type discriminator (always 'command')."""
            ...

        command_type: t.NonEmptyStr
        command_id: t.NonEmptyStr
        issuer_id: t.NonEmptyStr | None
        config_file: str | None


__all__: list[str] = [
    "FlextTargetOracleProtocolsCommands",
]
