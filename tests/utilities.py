"""Utilities for flext-target-oracle tests - uses u.Oracle.Tests.* namespace pattern.

This module provides test-specific utilities that extend the main flext-target-oracle utilities.
Uses the unified namespace pattern u.Oracle.Tests.* for test-only objects.
Combines FlextTestsUtilities functionality with project-specific test utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle import u
from flext_tests import FlextTestsUtilities


class TestsFlextTargetOracleUtilities(FlextTestsUtilities, u):
    """Test utilities combining FlextTestsUtilities and project-specific utilities."""

    class Oracle(u.Oracle):
        """Oracle domain utilities extending project utilities."""

        class Tests:
            """Internal tests declarations for test-only objects."""


u = TestsFlextTargetOracleUtilities

__all__ = ["TestsFlextTargetOracleUtilities", "u"]
