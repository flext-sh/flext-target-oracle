"""Target Oracle models — canonical location is models.py via m.TargetOracle.*.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_oracle.models import FlextTargetOracleModels

# Re-export for any remaining callers; prefer m.TargetOracle.* in new code.
LoadStatisticsModel = FlextTargetOracleModels.TargetOracle.LoadStatisticsModel
OracleConnectionModel = FlextTargetOracleModels.TargetOracle.OracleConnectionModel
SingerStreamModel = FlextTargetOracleModels.TargetOracle.SingerStreamModel

__all__ = [
    "LoadStatisticsModel",
    "OracleConnectionModel",
    "SingerStreamModel",
]
