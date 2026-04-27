"""Target Oracle type facade."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleTypes
from flext_meltano import t as meltano_t
from flext_target_oracle._typings.base import FlextTargetOracleTypesBase


class FlextTargetOracleTypes(meltano_t, FlextDbOracleTypes):
    """Oracle target type facade."""

    class TargetOracle(FlextTargetOracleTypesBase):
        """Oracle target type namespace."""


t = FlextTargetOracleTypes

__all__: list[str] = ["FlextTargetOracleTypes", "t"]
