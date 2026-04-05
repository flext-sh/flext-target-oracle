"""Test utilities combining FlextTestsUtilities and project-specific utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_target_oracle import FlextTargetOracleUtilities


class FlextTargetOracleTestUtilities(FlextTestsUtilities, FlextTargetOracleUtilities):
    """Test utilities combining FlextTestsUtilities and project-specific utilities."""

    class TargetOracle(FlextTargetOracleUtilities.TargetOracle):
        """TargetOracle domain utilities extending project utilities."""

        class Tests:
            """Internal tests declarations for test-only objects."""


u = FlextTargetOracleTestUtilities

__all__ = ["FlextTargetOracleTestUtilities", "u"]
