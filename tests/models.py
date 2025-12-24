"""Test models for flext-target-oracle tests.

Provides TestsFlextTargetOracleModels, extending FlextTestsModels with
flext-target-oracle-specific models using COMPOSITION INHERITANCE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.models import FlextTestsModels

from flext_target_oracle.models import FlextTargetOracleModels


class TestsFlextTargetOracleModels(FlextTestsModels, FlextTargetOracleModels):
    """Models for flext-target-oracle tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsModels - for test infrastructure (.Tests.*)
    2. FlextTargetOracleModels - for domain models

    Access patterns:
    - tm.Tests.* (generic test models from FlextTestsModels)
    - tm.* (Target Oracle domain models)
    - m.* (production models via alternative alias)
    """

    class Tests:
        """Project-specific test fixtures namespace."""

        class TargetOracle:
            """Target Oracle-specific test fixtures."""


# Short aliases per FLEXT convention
tm = TestsFlextTargetOracleModels
m = TestsFlextTargetOracleModels

__all__ = [
    "TestsFlextTargetOracleModels",
    "m",
    "tm",
]
