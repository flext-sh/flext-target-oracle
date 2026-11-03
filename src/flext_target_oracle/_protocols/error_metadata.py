# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/error_metadata
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

from flext_target_oracle import t


class FlextTargetOracleProtocolsErrorMetadata:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ErrorMetadata(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def code(self) -> str:
            """Canonical error code."""
            ...

        @property
        def context(self) -> t.JsonMapping | None:
            """Structured error context."""
            ...

        @property
        def correlation_id(self) -> str | None:
            """Cross-service correlation identifier."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsErrorMetadata",
]
