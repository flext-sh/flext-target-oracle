"""FLEXT TARGET ORACLE - Singer Oracle Database Loading with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Singer Oracle Target with simplified public API:
- All common imports available from root: from flext_target_oracle import OracleTarget
- Built on flext-core foundation for robust Oracle integration
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Import from flext-core for foundational patterns
from flext_core import BaseConfig, DomainBaseModel
from flext_core.domain.shared_types import ServiceResult

try:
    __version__ = importlib.metadata.version("flext-target-oracle")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextTargetOracleDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT TARGET ORACLE import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT TARGET ORACLE docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextTargetOracleDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Re-export commonly used imports from flext-core - NO FALLBACKS (per user instructions)
from flext_core import (
    BaseConfig as OracleBaseConfig,  # Configuration base
    DomainBaseModel as BaseModel,  # Base for Oracle models
    DomainError as OracleError,  # Oracle-specific errors
    ValidationError as ValidationError,  # Validation errors
)

# Singer Target exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_oracle.target import OracleTarget

# Oracle Database Integration exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_db_oracle import (
        OracleConfig,
        OracleConnectionService,
        OracleQueryService,
    )

# Application Services exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_oracle.application.services import (
        OracleLoaderService,
        SingerTargetService,
    )

# CLI exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_oracle.cli import main as cli_main

# Sinks exports (compatibility layer) - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_oracle.sinks import OracleSink

# Domain Models exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_oracle.domain.models import (
        LoadStatistics,
        SingerRecord,
        SingerSchema,
        TargetConfig,
    )

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "BaseModel",  # from flext_target_oracle import BaseModel
    # Deprecation utilities
    "FlextTargetOracleDeprecationWarning",
    # Domain Models (simplified access)
    "LoadStatistics",  # from flext_target_oracle import LoadStatistics
    # Core Patterns (from flext-core)
    "OracleBaseConfig",  # from flext_target_oracle import OracleBaseConfig
    # Oracle Database Integration (from flext-db-oracle)
    "OracleConfig",  # from flext_target_oracle import OracleConfig
    "OracleConnectionService",  # from flext_target_oracle import OracleConnectionService
    "OracleError",  # from flext_target_oracle import OracleError
    # Application Services (simplified access)
    "OracleLoaderService",  # from flext_target_oracle import OracleLoaderService
    "OracleQueryService",  # from flext_target_oracle import OracleQueryService
    # Compatibility layer (simplified access)
    "OracleSink",  # from flext_target_oracle import OracleSink
    # Main Singer Target (simplified access)
    "OracleTarget",  # from flext_target_oracle import OracleTarget
    "ServiceResult",  # from flext_target_oracle import ServiceResult
    # Domain Models (simplified access)
    "SingerRecord",  # from flext_target_oracle import SingerRecord
    "SingerSchema",  # from flext_target_oracle import SingerSchema
    "SingerTargetService",  # from flext_target_oracle import SingerTargetService
    "TargetConfig",  # from flext_target_oracle import TargetConfig
    "ValidationError",  # from flext_target_oracle import ValidationError
    # Version
    "__version__",
    "__version_info__",
    # CLI (simplified access)
    "cli_main",  # from flext_target_oracle import cli_main
]
