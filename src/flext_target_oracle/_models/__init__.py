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
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle._models.error_metadata import (
        FlextTargetOracleModelsErrorMetadata,
    )
    from flext_target_oracle._models.health_status import (
        FlextTargetOracleModelsHealthStatus,
    )
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.settings import FlextTargetOracleModelsSettings
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger


__all__: tuple[str, ...] = (
    "FlextTargetOracleModelsBase",
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsErrorMetadata",
    "FlextTargetOracleModelsHealthStatus",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSettings",
    "FlextTargetOracleModelsSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTargetOracleModelsBase": ".base",
        "FlextTargetOracleModelsCommands": ".commands",
        "FlextTargetOracleModelsErrorMetadata": ".error_metadata",
        "FlextTargetOracleModelsHealthStatus": ".health_status",
        "FlextTargetOracleModelsResults": ".results",
        "FlextTargetOracleModelsSettings": ".settings",
        "FlextTargetOracleModelsSinger": ".singer",
    }),
    public_exports=__all__,
)
