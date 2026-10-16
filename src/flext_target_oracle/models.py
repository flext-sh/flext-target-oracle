# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models for Oracle target operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_target_oracle/models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_db_oracle import FlextDbOracleModels
from flext_meltano import FlextMeltanoModels

from flext_target_oracle._models import (
    FlextTargetOracleModelsBase,
    FlextTargetOracleModelsCommands,
    FlextTargetOracleModelsErrorMetadata,
    FlextTargetOracleModelsHealthStatus,
    FlextTargetOracleModelsResults,
    FlextTargetOracleModelsSettings,
    FlextTargetOracleModelsSinger,
)


class FlextTargetOracleModels(FlextMeltanoModels, FlextDbOracleModels):
    """Complete models for Oracle target operations extending FlextModels."""

    class TargetOracle(
        FlextTargetOracleModelsBase,
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsErrorMetadata,
        FlextTargetOracleModelsHealthStatus,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSettings,
        FlextTargetOracleModelsSinger,
    ):
        """Namespace of models for Oracle target."""


m = FlextTargetOracleModels

__all__: list[str] = ["FlextTargetOracleModels", "m"]
