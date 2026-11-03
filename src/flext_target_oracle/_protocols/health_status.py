# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/health_status
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

from flext_target_oracle import t


class FlextTargetOracleProtocolsHealthStatus:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class FlextTargetOracleModelsHealthStatus(FlextMeltanoProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def timestamp(self) -> float:
            """Unix timestamp captured when the health check ran."""
            ...

        @property
        def status(self) -> str:
            """Aggregate health status of the target."""
            ...

        @property
        def checks(self) -> t.MutableJsonMapping:
            """Per-check results keyed by capability name."""
            ...

        @property
        def metrics(self) -> t.MutableJsonMapping:
            """Collected metrics for the health snapshot."""
            ...

        @property
        def error(self) -> str | None:
            """Error detail when the snapshot reports a failure."""
            ...


__all__: list[str] = [
    "FlextTargetOracleProtocolsHealthStatus",
]
