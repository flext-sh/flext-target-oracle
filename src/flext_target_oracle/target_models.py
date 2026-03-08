"""Target Models for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle.constants import c

PUBLIC = "PUBLIC"
LoadMethodModel = c.LoadMethod
StorageModeModel = c.StorageMode
__all__ = [
    "LoadMethodModel",
    "LoadStatisticsModel",
    "OracleConnectionModel",
    "SingerStreamModel",
    "StorageModeModel",
]
