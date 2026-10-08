"""Test constants combining FlextTestsConstants and project-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final

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
            # Why: the flext-tests governance protocol declares these as
            # ClassVar; Final instance-variable declarations would not satisfy
            # the structural contract consumed by test_module_governance.
            SRC_DIR: ClassVar[str] = "src"
            PACKAGE_DIR: ClassVar[str] = "flext_target_oracle"
            ALLOWED_MODULE_FUNCTIONS: Final[dict[str, frozenset[str]]] = {
                "cli.py": frozenset({"main"}),
            }


c = TestsFlextTargetOracleConstants

__all__: list[str] = ["TestsFlextTargetOracleConstants", "c"]
