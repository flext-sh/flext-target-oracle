"""FlextTargetOracleConfig — frozen config singleton for flext-target-oracle.

See ADR-005 §7.

Model-less: business rules live in ``config/*.yaml`` under the ``TargetOracle:`` key and
are exposed through the open ``config.TargetOracle`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.TargetOracle.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_meltano import FlextMeltanoConfig, m
from flext_meltano.models import FlextMeltanoModelsConfig


class FlextTargetOracleConfig(FlextMeltanoConfig):
    """TargetOracle config auto-loaded model-less from ``config/*.yaml``.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    TargetOracle: Annotated[
        FlextMeltanoModelsConfig.MeltanoNamespace,
        m.Field(
            description=(
                "Open namespace exposing ``config/*.yaml`` under TargetOracle."
            ),
        ),
    ] = FlextMeltanoModelsConfig.MeltanoNamespace()


config: FlextTargetOracleConfig = FlextTargetOracleConfig.fetch_global()
"""Pre-instantiated frozen config singleton.

Exposed as ``from flext_target_oracle import config``.
"""

__all__: list[str] = ["FlextTargetOracleConfig", "config"]
