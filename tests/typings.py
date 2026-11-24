"""Types for flext-target-oracle tests - uses t.Tests.* namespace pattern.

This module provides test-specific types that extend the main flext-target-oracle types.
Uses the unified namespace pattern t.Tests.* for test-only objects.
Combines TestsFlextTypes functionality with project-specific test types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from tests import FlextTargetOracleTypes


class TestsFlextTargetOracleTypes(FlextTestsTypes, FlextTargetOracleTypes):
    """Test types combining TestsFlextTypes and project-specific types."""

    class Tests(FlextTestsTypes.Tests):
        """Internal tests declarations for test-only objects."""


t = TestsFlextTargetOracleTypes

__all__: list[str] = ["TestsFlextTargetOracleTypes", "t"]
