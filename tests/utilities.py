"""Test utilities combining TestsFlextUtilities and project-specific utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_target_oracle import FlextTargetOracleUtilities


class TestsFlextTargetOracleUtilities(FlextTestsUtilities, FlextTargetOracleUtilities):
    """Test utilities combining TestsFlextUtilities and project-specific utilities."""

    class TargetOracle(FlextTargetOracleUtilities.TargetOracle):
        """TargetOracle domain utilities extending project utilities."""

        class Tests:
            """Internal tests declarations for test-only objects."""


u = TestsFlextTargetOracleUtilities

__all__ = ["TestsFlextTargetOracleUtilities", "u"]
