"""FlextTargetOracleConfig — frozen config singleton for flext-target-oracle (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``TargetOracle:`` key and
are exposed through the open ``config.TargetOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TargetOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_meltano import FlextMeltanoConfig


class _TargetOracleNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextTargetOracleConfig(FlextMeltanoConfig):
    """TargetOracle config auto-loaded model-less from ``config/*.yaml``."""

    TargetOracle: _TargetOracleNamespace = _TargetOracleNamespace()


config: FlextTargetOracleConfig = FlextTargetOracleConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_target_oracle import config``."""

__all__: list[str] = ["FlextTargetOracleConfig", "config"]
