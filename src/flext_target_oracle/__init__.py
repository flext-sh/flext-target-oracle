# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
from flext_target_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)
from flext_target_oracle._exports import (
    FLEXT_TARGET_ORACLE_LAZY_IMPORTS,
    FLEXT_TARGET_ORACLE_PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_core._root_typing_parts import (
        d as d,
        e as e,
        h as h,
        r as r,
        s as s,
        x as x,
    )
    from flext_target_oracle._utilities.client import (
        FlextTargetOracle as FlextTargetOracle,
    )
    from flext_target_oracle.api import (
        FlextTargetOracleService as FlextTargetOracleService,
        target_oracle as target_oracle,
    )
    from flext_target_oracle.cli import (
        FlextTargetOracleCli as FlextTargetOracleCli,
        main as main,
    )
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants as FlextTargetOracleConstants,
        c as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels as FlextTargetOracleModels,
        m as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols as FlextTargetOracleProtocols,
        p as p,
    )
    from flext_target_oracle.settings import (
        FlextTargetOracleSettings as FlextTargetOracleSettings,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes as FlextTargetOracleTypes,
        t as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities as FlextTargetOracleUtilities,
        u as u,
    )


_LAZY_IMPORTS = {
    name: target
    for name, target in FLEXT_TARGET_ORACLE_LAZY_IMPORTS.items()
    if name in FLEXT_TARGET_ORACLE_PUBLIC_EXPORTS
}


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = FLEXT_TARGET_ORACLE_PUBLIC_EXPORTS

__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleCli",
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "t",
    "target_oracle",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
