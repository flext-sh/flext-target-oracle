# AUTO-GENERATED FILE — Regenerate with: make gen
"""Target Oracle protocol facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/protocols
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import p as flext_db_oracle_p
from flext_meltano import p as flext_meltano_p

from flext_target_oracle._protocols import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(flext_meltano_p, flext_db_oracle_p):
    """Oracle target protocol facade."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Oracle target protocol namespace."""


p = FlextTargetOracleProtocols
__all__: list[str] = ["FlextTargetOracleProtocols", "p"]
