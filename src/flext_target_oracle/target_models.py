"""Target Oracle models — canonical location is models.py via m.TargetOracle.*.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_target_oracle import m

# Re-export for any remaining callers; prefer m.TargetOracle.* in new code.
LoadStatisticsModel = m.TargetOracle.LoadStatisticsModel
OracleConnectionModel = m.TargetOracle.OracleConnectionModel
SingerStreamModel = m.TargetOracle.SingerStreamModel

__all__ = [
    "LoadStatisticsModel",
    "OracleConnectionModel",
    "SingerStreamModel",
]
