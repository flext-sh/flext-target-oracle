"""FLEXT Target Oracle Configuration - Enhanced FlextSettings Implementation.

Single unified configuration class for Oracle Singer target operations following
FLEXT 1.0.0 patterns with enhanced singleton, SecretStr, and Pydantic 2.11+ features.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult

from .constants import c
from flext_target_oracle.target_loader import FlextTargetOracleSettings

LoadMethod = c.LoadMethod


def validate_oracle_configuration(
    config: FlextTargetOracleSettings,
) -> FlextResult[bool]:
    """Validate Oracle configuration using FlextSettings patterns - ZERO DUPLICATION."""
    return config.validate_business_rules()


__all__: list[str] = [
    "FlextTargetOracleSettings",
    "LoadMethod",
    "validate_oracle_configuration",
]
