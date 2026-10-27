"""Runtime health snapshot model for flext-target-oracle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import m

from flext_target_oracle import t


class FlextTargetOracleModelsHealthStatus:
    """Runtime health snapshot model for flext-target-oracle."""

    class FlextTargetOracleModelsHealthStatus(m.ArbitraryTypesModel):
        """Runtime health snapshot used by health checks."""

        timestamp: Annotated[
            float,
            m.Field(description="Unix timestamp captured when the health check ran"),
        ]
        status: Annotated[
            str,
            m.Field(description="Aggregate health status of the target"),
        ] = "healthy"
        checks: Annotated[
            t.MutableJsonMapping,
            m.Field(description="Per-check results keyed by capability name"),
        ] = m.Field(default_factory=dict)
        metrics: Annotated[
            t.MutableJsonMapping,
            m.Field(description="Collected metrics for the health snapshot"),
        ] = m.Field(default_factory=dict)
        error: Annotated[
            str | None,
            m.Field(description="Error detail when the snapshot reports a failure"),
        ] = None


__all__: list[str] = ["FlextTargetOracleModelsHealthStatus"]
