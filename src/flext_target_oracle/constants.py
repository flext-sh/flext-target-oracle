"""Target Oracle constants facade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_db_oracle import FlextDbOracleConstants
from flext_meltano import FlextMeltanoConstants

from ._constants.base import FlextTargetOracleConstantsBase

if TYPE_CHECKING:
    from flext_target_oracle import t


class FlextTargetOracleConstants(FlextMeltanoConstants, FlextDbOracleConstants):
    """Oracle target constant facade."""

    class TargetOracle(FlextTargetOracleConstantsBase):
        """Oracle target constant namespace."""


c = FlextTargetOracleConstants
__all__: t.StrSequence = ("FlextTargetOracleConstants", "c")
