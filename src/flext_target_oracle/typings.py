"""Target Oracle type facade."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import FlextMeltanoTypes

from ._typings.base import FlextTargetOracleTypesBase


class FlextTargetOracleTypes(FlextMeltanoTypes, FlextDbOracleTypes):
    """Oracle target type facade."""

    class TargetOracle(FlextTargetOracleTypesBase):
        """Oracle target type namespace."""


t = FlextTargetOracleTypes

__all__: list[str] = ["FlextTargetOracleTypes", "t"]
