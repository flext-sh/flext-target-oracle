"""Target Models for FLEXT Target Oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle.constants import c

# Oracle schema constants
PUBLIC = "PUBLIC"


# LoadMethodModel moved to constants.py as c.LoadMethod (DRY pattern)
LoadMethodModel = c.LoadMethod

# StorageModeModel moved to constants.py as c.StorageMode (DRY pattern)
StorageModeModel = c.StorageMode


__all__ = [
    # Enums
    "LoadMethodModel",
    "LoadStatisticsModel",
    # Value Objects
    "OracleConnectionModel",
    "SingerStreamModel",
    "StorageModeModel",
]
