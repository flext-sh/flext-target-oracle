# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._models.base import FlextTargetOracleModelsBase
    from flext_target_oracle._models.error_metadata import (
        FlextTargetOracleModelsErrorMetadata,
    )
    from flext_target_oracle._models.health_status import (
        FlextTargetOracleModelsHealthStatus,
    )
    from flext_target_oracle._models.settings import FlextTargetOracleModelsSettings


__all__: tuple[str, ...] = (
    "FlextTargetOracleModelsBase",
    "FlextTargetOracleModelsErrorMetadata",
    "FlextTargetOracleModelsHealthStatus",
    "FlextTargetOracleModelsSettings",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetOracleModelsBase": ".base",
        "FlextTargetOracleModelsErrorMetadata": ".error_metadata",
        "FlextTargetOracleModelsHealthStatus": ".health_status",
        "FlextTargetOracleModelsSettings": ".settings",
    }),
    public_exports=__all__,
)
