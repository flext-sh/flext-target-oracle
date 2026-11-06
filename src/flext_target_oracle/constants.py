# AUTO-GENERATED FILE — Regenerate with: make gen
"""Target Oracle constants facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/constants
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import c as flext_db_oracle_c
from flext_meltano import c as flext_meltano_c

from flext_target_oracle._constants import FlextTargetOracleConstantsBase


class FlextTargetOracleConstants(flext_meltano_c, flext_db_oracle_c):
    """Oracle target constant facade."""

    class TargetOracle(FlextTargetOracleConstantsBase):
        """Oracle target constant namespace."""


c = FlextTargetOracleConstants
__all__: list[str] = ["FlextTargetOracleConstants", "c"]
