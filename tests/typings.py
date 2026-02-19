"""Types for flext-target-oracle tests - uses t.Oracle.Tests.* namespace pattern.

This module provides test-specific types that extend the main flext-target-oracle types.
Uses the unified namespace pattern t.Oracle.Tests.* for test-only objects.
Combines FlextTestsTypes functionality with project-specific test types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle import t
from flext_tests import FlextTestsTypes


class TestsFlextTargetOracleTypes(FlextTestsTypes, t):
    """Test types combining FlextTestsTypes and project-specific types."""

    class Oracle(t.Oracle):
        """Oracle domain types extending project types."""

        class Tests:
            """Internal tests declarations for test-only objects."""


t = TestsFlextTargetOracleTypes

__all__ = ["TestsFlextTargetOracleTypes", "t"]
