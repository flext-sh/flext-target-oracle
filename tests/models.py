"""Models for flext-target-oracle tests - uses m.Oracle.Tests.* namespace pattern.

This module provides test-specific models that extend the main flext-target-oracle models.
Uses the unified namespace pattern m.Oracle.Tests.* for test-only objects.
Combines FlextTestsModels functionality with project-specific test models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle import m
from flext_tests import FlextTestsModels


class TestsFlextTargetOracleModels(FlextTestsModels, m):
    """Test models combining FlextTestsModels and project-specific models."""

    class Oracle(m.Oracle):
        """Oracle domain models extending project models."""

        class Tests:
            """Internal tests declarations for test-only objects."""


m = TestsFlextTargetOracleModels

__all__ = ["TestsFlextTargetOracleModels", "m"]
