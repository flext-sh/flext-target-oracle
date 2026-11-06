# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/_protocols/health_status
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_meltano import FlextMeltanoProtocols

if TYPE_CHECKING:
    from flext_target_oracle import t


class FlextTargetOracleProtocolsHealthStatus:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class FlextTargetOracleModelsHealthStatus(
        FlextMeltanoProtocols.BaseModel, Protocol
    ):
        """Structural data contract projected from the owning model."""

        timestamp: float
        status: str
        checks: t.MutableJsonMapping
        metrics: t.MutableJsonMapping
        error: str | None


__all__: list[str] = [
    "FlextTargetOracleProtocolsHealthStatus",
]
