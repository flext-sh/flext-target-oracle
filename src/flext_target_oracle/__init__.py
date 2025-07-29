"""FLEXT Target Oracle - Self-contained Oracle target implementation.

This project provides a complete Singer target for Oracle Database using flext-core
patterns and flext-db-oracle infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import flext-core patterns for consistency
from flext_core import FlextError, FlextResult

from flext_target_oracle.config import FlextOracleTargetConfig, LoadMethod

# Import local implementations
from flext_target_oracle.target import FlextOracleTarget


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
