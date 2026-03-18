"""Models for flext-target-oracle tests - uses m.Oracle.Tests.* namespace pattern.

This module provides test-specific models that extend the main flext-target-oracle models.
Uses the unified namespace pattern m.Oracle.Tests.* for test-only objects.
Combines m functionality with project-specific test models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import m

from flext_target_oracle import FlextTargetOracleModels


class TestsFlextTargetOracleModels(m, FlextTargetOracleModels):
    """Test models combining m and project-specific models."""

    class TargetOracle(FlextTargetOracleModels.TargetOracle):
        """TargetOracle domain models extending project models."""

        class Tests:
            """Internal tests declarations for test-only objects."""


m = TestsFlextTargetOracleModels

__all__ = ["TestsFlextTargetOracleModels", "m"]
