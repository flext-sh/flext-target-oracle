"""Protocols for flext-target-oracle tests - uses p.Oracle.Tests.* namespace pattern.

This module provides test-specific protocols that extend the main flext-target-oracle protocols.
Uses the unified namespace pattern p.Oracle.Tests.* for test-only objects.
Combines FlextTestsProtocols functionality with project-specific test protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_target_oracle import p
from flext_tests import FlextTestsProtocols


class TestsFlextTargetOracleProtocols(FlextTestsProtocols, p):
    """Test protocols combining FlextTestsProtocols and project-specific protocols."""

    class TargetOracle(p.TargetOracle):
        """TargetOracle domain protocols extending project protocols."""

        class Tests:
            """Internal tests declarations for test-only objects."""


p = TestsFlextTargetOracleProtocols

__all__ = ["TestsFlextTargetOracleProtocols", "p"]
