# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle.application package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle.application.client import FlextTargetOracle
    from flext_target_oracle.application.loader import FlextTargetOracleLoader


__all__: tuple[str, ...] = ("FlextTargetOracle", "FlextTargetOracleLoader")

install_lazy_exports(
    __name__,
    globals(),
    {"FlextTargetOracle": ".client", "FlextTargetOracleLoader": ".loader"},
    public_exports=__all__,
)
