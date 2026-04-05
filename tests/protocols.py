"""Test protocols combining FlextTestsProtocols and project-specific protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_target_oracle import FlextTargetOracleProtocols


class FlextTargetOracleTestProtocols(FlextTestsProtocols, FlextTargetOracleProtocols):
    """Test protocols combining FlextTestsProtocols and project-specific protocols."""

    class TargetOracle(FlextTargetOracleProtocols.TargetOracle):
        """TargetOracle domain protocols extending project protocols."""

        class Tests:
            """Internal tests declarations for test-only objects."""


p = FlextTargetOracleTestProtocols

__all__ = ["FlextTargetOracleTestProtocols", "p"]
