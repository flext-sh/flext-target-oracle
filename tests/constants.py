"""Module skeleton for FlextTargetOracleTestConstants.

Test constants for flext-target-oracle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_target_oracle import FlextTargetOracleConstants


class FlextTargetOracleTestConstants(FlextTestsConstants):
    """Test constants for flext-target-oracle."""

    class TargetOracle(FlextTargetOracleConstants.TargetOracle):
        """TargetOracle constants extending project constants."""

        class Tests:
            """Internal tests declarations for test-only objects."""


c = FlextTargetOracleTestConstants
__all__ = ["FlextTargetOracleTestConstants", "c"]
