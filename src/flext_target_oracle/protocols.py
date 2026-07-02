"""Target Oracle protocol facade."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import p as _p
from flext_target_oracle._protocols.base import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(_p, FlextDbOracleProtocols):
    """Oracle target protocol facade."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Oracle target protocol namespace."""


p = FlextTargetOracleProtocols
__all__: list[str] = ["FlextTargetOracleProtocols", "p"]
