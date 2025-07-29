"""FLEXT Target Oracle - Wrapper for flext-meltano consolidated implementation.

CONSOLIDATION: This project is now a library wrapper that imports the real
Singer/Meltano/DBT consolidated implementations from flext-meltano to eliminate
code duplication across the FLEXT ecosystem.

This follows the architectural principle:
- flext-* projects are LIBRARIES, not services
- tap/target/dbt/ext are Meltano plugins
- Real implementations are in flext-meltano

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import flext-core patterns for consistency
from flext_core import FlextError, FlextResult

# Import consolidated implementations from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.targets.oracle import (
    FlextOracleTarget,
    FlextOracleTargetConfig,
    LoadMethod,
)


# Local exceptions for backward compatibility
class FlextOracleTargetError(FlextError):
    """Base exception for Oracle target operations."""


class FlextOracleTargetConnectionError(FlextOracleTargetError):
    """Oracle connection-related errors."""


class FlextOracleTargetAuthenticationError(FlextOracleTargetError):
    """Oracle authentication-related errors."""


class FlextOracleTargetSchemaError(FlextOracleTargetError):
    """Oracle schema-related errors."""


class FlextOracleTargetProcessingError(FlextOracleTargetError):
    """Oracle data processing errors."""


__version__ = "0.8.0"

__all__ = [
    # Main implementation (from flext-meltano)
    "FlextOracleTarget",
    "FlextOracleTargetAuthenticationError",
    "FlextOracleTargetConfig",
    "FlextOracleTargetConnectionError",
    # Local exceptions (backward compatibility)
    "FlextOracleTargetError",
    "FlextOracleTargetProcessingError",
    "FlextOracleTargetSchemaError",
    # Core patterns
    "FlextResult",
    "LoadMethod",
    "__version__",
]
