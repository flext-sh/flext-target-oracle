"""Constants for FLEXT Target Oracle module.

This module defines centralized constants following the FlextConstants pattern
from flext-core, extending it with Oracle target-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants
from flext_target_oracle import FlextTargetOracleConstantsBase


class FlextTargetOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Target Oracle constants extending FlextConstants."""

    class TargetOracle(FlextTargetOracleConstantsBase):
        """TargetOracle domain constants namespace."""


c = FlextTargetOracleConstants
__all__ = ["FlextTargetOracleConstants", "c"]
