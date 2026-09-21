"""Target Oracle protocol facade."""

from __future__ import annotations

from flext_db_oracle import p as _db_oracle_p
from flext_meltano import p as _p

from ._protocols.base import FlextTargetOracleProtocolsBase


class FlextTargetOracleProtocols(_p, _db_oracle_p):
    """Oracle target protocol facade."""

    class TargetOracle(FlextTargetOracleProtocolsBase):
        """Oracle target protocol namespace."""


p = FlextTargetOracleProtocols
__all__: list[str] = ["FlextTargetOracleProtocols", "p"]
