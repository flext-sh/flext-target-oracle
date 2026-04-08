"""Test models combining TestsFlextModels and project-specific models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_target_oracle import FlextTargetOracleModels


class TestsFlextTargetOracleModels(FlextTestsModels, FlextTargetOracleModels):
    """Test models combining TestsFlextModels and project-specific models."""

    class TargetOracle(FlextTargetOracleModels.TargetOracle):
        """TargetOracle domain models extending project models."""

        class Tests:
            """Internal tests declarations for test-only objects."""


m = TestsFlextTargetOracleModels

__all__ = ["TestsFlextTargetOracleModels", "m"]
