"""Test protocol definitions for flext-target-oracle.

Provides TestsFlextTargetOracleProtocols, combining FlextTestsProtocols with
FlextTargetOracleProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols

from flext_target_oracle.protocols import FlextTargetOracleProtocols


class TestsFlextTargetOracleProtocols(FlextTestsProtocols, FlextTargetOracleProtocols):
    """Test protocols combining FlextTestsProtocols and FlextTargetOracleProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.TargetOracle.* (from FlextTargetOracleProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with TargetOracle-specific protocols.
        """

        class TargetOracle:
            """TargetOracle-specific test protocols."""


# Runtime aliases
p = TestsFlextTargetOracleProtocols
tp = TestsFlextTargetOracleProtocols

__all__ = ["TestsFlextTargetOracleProtocols", "p", "tp"]
