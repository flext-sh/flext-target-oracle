"""Test constants combining FlextTestsConstants and project-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_target_oracle import FlextTargetOracleConstants


class TestsFlextTargetOracleConstants(FlextTestsConstants, FlextTargetOracleConstants):
    """Test constants combining FlextTestsConstants and project-specific constants."""

    class TargetOracle(FlextTargetOracleConstants.TargetOracle):
        """TargetOracle domain constants extending project constants."""

        class Tests:
            """Internal tests declarations for test-only objects."""


c = TestsFlextTargetOracleConstants

__all__: list[str] = ["TestsFlextTargetOracleConstants", "c"]
