"""Target Oracle constants facade."""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import c as _c
from flext_target_oracle import t
from flext_target_oracle._constants.base import FlextTargetOracleConstantsBase


class FlextTargetOracleConstants(_c, FlextDbOracleConstants):
    """Oracle target constant facade."""

    class TargetOracle(FlextTargetOracleConstantsBase):
        """Oracle target constant namespace."""


c = FlextTargetOracleConstants
__all__: t.StrSequence = ("FlextTargetOracleConstants", "c")
