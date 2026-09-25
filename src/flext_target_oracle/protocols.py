"""Target Oracle protocol facade."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleProtocols
from flext_meltano import FlextMeltanoProtocols

from ._protocols.base import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(FlextMeltanoProtocols, FlextDbOracleProtocols):
    """Oracle target protocol facade."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Oracle target protocol namespace."""


p = FlextTargetOracleProtocols
__all__: list[str] = ["FlextTargetOracleProtocols", "p"]
