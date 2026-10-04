"""Target Oracle protocol facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/protocols
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols

from flext_target_oracle._protocols.base import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Oracle target protocol facade."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Oracle target protocol namespace."""


p = FlextTargetOracleProtocols
__all__: list[str] = ["FlextTargetOracleProtocols", "p"]
