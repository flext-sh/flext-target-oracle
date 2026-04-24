"""Test constants combining FlextTestsConstants and project-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_tests import FlextTestsConstants

from flext_target_oracle import FlextTargetOracleConstants


class TestsFlextTargetOracleConstants(FlextTestsConstants, FlextTargetOracleConstants):
    """Test constants combining FlextTestsConstants and project-specific constants."""

    class TargetOracle(FlextTargetOracleConstants.TargetOracle):
        """TargetOracle domain constants extending project constants."""

        class Tests:
            """Internal tests declarations for test-only objects."""

            class Integration:
                """Integration constants for target-oracle tests."""

                ORACLE_HOST: Final[str] = "localhost"
                ORACLE_PORT: Final[int] = 1521
                ORACLE_SERVICE: Final[str] = "XE"
                TEST_SCHEMA: Final[str] = "FLEXT_TEST"

            class ModuleGovernance:
                """Module-governance constants for target-oracle tests."""

                PROJECT_ROOT_PARENT_DEPTH: Final[int] = 1
                SRC_DIR: Final[str] = "src"
                PACKAGE_DIR: Final[str] = "flext_target_oracle"
                ALLOWED_MODULE_FUNCTIONS: Final[dict[str, frozenset[str]]] = {
                    "_utilities/cli.py": frozenset({"main"}),
                }


c = TestsFlextTargetOracleConstants

__all__: list[str] = ["TestsFlextTargetOracleConstants", "c"]
