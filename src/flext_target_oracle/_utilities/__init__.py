# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase
    from flext_target_oracle._utilities.client import FlextTargetOracle
    from flext_target_oracle._utilities.errors import FlextTargetOracleUtilitiesErrors
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
    from flext_target_oracle._utilities.observability import (
        FlextTargetOracleUtilitiesObservability,
    )
    from flext_target_oracle._utilities.services import Utilities


__all__: tuple[str, ...] = (
    "FlextTargetOracle",
    "FlextTargetOracleLoader",
    "FlextTargetOracleUtilitiesBase",
    "FlextTargetOracleUtilitiesErrors",
    "FlextTargetOracleUtilitiesObservability",
    "Utilities",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetOracle": ".client",
        "FlextTargetOracleLoader": ".loader",
        "FlextTargetOracleUtilitiesBase": ".base",
        "FlextTargetOracleUtilitiesErrors": ".errors",
        "FlextTargetOracleUtilitiesObservability": ".observability",
        "Utilities": ".services",
    }),
    public_exports=__all__,
)
