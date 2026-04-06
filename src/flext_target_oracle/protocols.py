"""Target Oracle protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols
from flext_target_oracle import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Singer Target Oracle protocols extending Oracle and Meltano protocols."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Singer Target domain protocols."""


p = FlextTargetOracleProtocols
__all__ = ["FlextTargetOracleProtocols", "p"]
