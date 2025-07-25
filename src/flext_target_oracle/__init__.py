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

# Import consolidated implementations from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.targets.oracle import TargetOracle, TargetOracleConfig

# Backward compatibility aliases
FlextTargetOracle = TargetOracle
FlextTargetOracleConfig = TargetOracleConfig
OracleTarget = TargetOracle
TargetConfig = TargetOracleConfig

__version__ = "0.8.0-wrapper"

__all__ = [
    # Backward compatibility
    "FlextTargetOracle",
    "FlextTargetOracleConfig",
    "OracleTarget",
    "TargetConfig",
    "TargetOracle",
    "TargetOracleConfig",
    "__version__",
]
