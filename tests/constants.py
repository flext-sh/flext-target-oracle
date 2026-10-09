"""Test constants combining FlextTestsConstants and project-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_tests import FlextTestsConstants

from flext_target_oracle import FlextTargetOracleConstants


class TestsFlextTargetOracleConstants(FlextTargetOracleConstants, FlextTestsConstants):
    """Test constants combining FlextTestsConstants and project-specific constants."""

    class TargetOracle(FlextTargetOracleConstants.TargetOracle):
        """TargetOracle domain constants extending project constants."""

        class Tests:
            """Internal tests declarations for test-only objects."""

            ORACLE_HOST: Final[str] = "localhost"
            ORACLE_PORT: Final[int] = 1521
            ORACLE_SERVICE: Final[str] = "XE"
            TEST_SCHEMA: Final[str] = "FLEXT_TEST"
            PROJECT_ROOT_PARENT_DEPTH: Final[int] = 1
            # Why: the flext-tests governance protocol exposes SRC_DIR and
            # PACKAGE_DIR as read-only properties; plain instance declarations
            # satisfy that structural contract for both checkers.
            SRC_DIR: str = "src"
            PACKAGE_DIR: str = "flext_target_oracle"
            ALLOWED_MODULE_FUNCTIONS: Final[dict[str, frozenset[str]]] = {
                "cli.py": frozenset({"main"}),
            }


c = TestsFlextTargetOracleConstants

__all__: list[str] = ["TestsFlextTargetOracleConstants", "c"]
