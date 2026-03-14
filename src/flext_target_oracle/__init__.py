# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_target_oracle.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_target_oracle.constants import FlextTargetOracleConstants, c
    from flext_target_oracle.models import FlextTargetOracleModels, m
    from flext_target_oracle.protocols import FlextTargetOracleProtocols, p
    from flext_target_oracle.settings import (
        FlextTargetOracleSettings,
        LoadMethod,
        logger,
        validate_oracle_configuration,
    )
    from flext_target_oracle.target_client import FlextTargetOracle
    from flext_target_oracle.target_commands import (
        OracleTargetAboutCommand,
        OracleTargetCommandFactory,
        OracleTargetCommandHandler,
        OracleTargetLoadCommand,
        OracleTargetValidateCommand,
    )
    from flext_target_oracle.target_exceptions import (
        FlextTargetOracleExceptions,
        FlextTargetOracleExceptions as e,
    )
    from flext_target_oracle.target_loader import FlextTargetOracleLoader
    from flext_target_oracle.target_models import (
        LoadMethodModel,
        LoadStatisticsModel,
        OracleConnectionModel,
        SingerStreamModel,
        StorageModeModel,
    )
    from flext_target_oracle.target_observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )
    from flext_target_oracle.target_refactored import (
        FlextTargetOracleCliService,
        FlextTargetOracleCliService as s,
        main,
    )
    from flext_target_oracle.target_service import FlextTargetOracleService
    from flext_target_oracle.target_services import (
        BatchService,
        ConnectionService,
        OracleBatchService,
        OracleConnectionService,
        OracleRecordService,
        OracleSchemaService,
        OracleTargetServiceFactory,
        RecordService,
        SchemaService,
    )
    from flext_target_oracle.typings import FlextTargetOracleTypes, t
    from flext_target_oracle.utilities import FlextTargetOracleUtilities, u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "BatchService": ("flext_target_oracle.target_services", "BatchService"),
    "ConnectionService": ("flext_target_oracle.target_services", "ConnectionService"),
    "FlextOracleError": (
        "flext_target_oracle.target_observability",
        "FlextOracleError",
    ),
    "FlextOracleObs": ("flext_target_oracle.target_observability", "FlextOracleObs"),
    "FlextTargetOracle": ("flext_target_oracle.target_client", "FlextTargetOracle"),
    "FlextTargetOracleCliService": (
        "flext_target_oracle.target_refactored",
        "FlextTargetOracleCliService",
    ),
    "FlextTargetOracleConstants": (
        "flext_target_oracle.constants",
        "FlextTargetOracleConstants",
    ),
    "FlextTargetOracleExceptions": (
        "flext_target_oracle.target_exceptions",
        "FlextTargetOracleExceptions",
    ),
    "FlextTargetOracleLoader": (
        "flext_target_oracle.target_loader",
        "FlextTargetOracleLoader",
    ),
    "FlextTargetOracleModels": (
        "flext_target_oracle.models",
        "FlextTargetOracleModels",
    ),
    "FlextTargetOracleProtocols": (
        "flext_target_oracle.protocols",
        "FlextTargetOracleProtocols",
    ),
    "FlextTargetOracleService": (
        "flext_target_oracle.target_service",
        "FlextTargetOracleService",
    ),
    "FlextTargetOracleSettings": (
        "flext_target_oracle.settings",
        "FlextTargetOracleSettings",
    ),
    "FlextTargetOracleTypes": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
    "FlextTargetOracleUtilities": (
        "flext_target_oracle.utilities",
        "FlextTargetOracleUtilities",
    ),
    "LoadMethod": ("flext_target_oracle.settings", "LoadMethod"),
    "LoadMethodModel": ("flext_target_oracle.target_models", "LoadMethodModel"),
    "LoadStatisticsModel": ("flext_target_oracle.target_models", "LoadStatisticsModel"),
    "OracleBatchService": ("flext_target_oracle.target_services", "OracleBatchService"),
    "OracleConnectionModel": (
        "flext_target_oracle.target_models",
        "OracleConnectionModel",
    ),
    "OracleConnectionService": (
        "flext_target_oracle.target_services",
        "OracleConnectionService",
    ),
    "OracleRecordService": (
        "flext_target_oracle.target_services",
        "OracleRecordService",
    ),
    "OracleSchemaService": (
        "flext_target_oracle.target_services",
        "OracleSchemaService",
    ),
    "OracleTargetAboutCommand": (
        "flext_target_oracle.target_commands",
        "OracleTargetAboutCommand",
    ),
    "OracleTargetCommandFactory": (
        "flext_target_oracle.target_commands",
        "OracleTargetCommandFactory",
    ),
    "OracleTargetCommandHandler": (
        "flext_target_oracle.target_commands",
        "OracleTargetCommandHandler",
    ),
    "OracleTargetLoadCommand": (
        "flext_target_oracle.target_commands",
        "OracleTargetLoadCommand",
    ),
    "OracleTargetServiceFactory": (
        "flext_target_oracle.target_services",
        "OracleTargetServiceFactory",
    ),
    "OracleTargetValidateCommand": (
        "flext_target_oracle.target_commands",
        "OracleTargetValidateCommand",
    ),
    "RecordService": ("flext_target_oracle.target_services", "RecordService"),
    "SchemaService": ("flext_target_oracle.target_services", "SchemaService"),
    "SingerStreamModel": ("flext_target_oracle.target_models", "SingerStreamModel"),
    "StorageModeModel": ("flext_target_oracle.target_models", "StorageModeModel"),
    "__all__": ("flext_target_oracle.__version__", "__all__"),
    "__author__": ("flext_target_oracle.__version__", "__author__"),
    "__author_email__": ("flext_target_oracle.__version__", "__author_email__"),
    "__description__": ("flext_target_oracle.__version__", "__description__"),
    "__license__": ("flext_target_oracle.__version__", "__license__"),
    "__title__": ("flext_target_oracle.__version__", "__title__"),
    "__url__": ("flext_target_oracle.__version__", "__url__"),
    "__version__": ("flext_target_oracle.__version__", "__version__"),
    "__version_info__": ("flext_target_oracle.__version__", "__version_info__"),
    "c": ("flext_target_oracle.constants", "c"),
    "configure_oracle_observability": (
        "flext_target_oracle.target_observability",
        "configure_oracle_observability",
    ),
    "e": ("flext_target_oracle.target_exceptions", "FlextTargetOracleExceptions"),
    "logger": ("flext_target_oracle.settings", "logger"),
    "m": ("flext_target_oracle.models", "m"),
    "main": ("flext_target_oracle.target_refactored", "main"),
    "p": ("flext_target_oracle.protocols", "p"),
    "s": ("flext_target_oracle.target_refactored", "FlextTargetOracleCliService"),
    "t": ("flext_target_oracle.typings", "t"),
    "u": ("flext_target_oracle.utilities", "u"),
    "validate_oracle_configuration": (
        "flext_target_oracle.settings",
        "validate_oracle_configuration",
    ),
}

__all__ = [
    "BatchService",
    "ConnectionService",
    "FlextOracleError",
    "FlextOracleObs",
    "FlextTargetOracle",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConstants",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "LoadMethod",
    "LoadMethodModel",
    "LoadStatisticsModel",
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetServiceFactory",
    "OracleTargetValidateCommand",
    "RecordService",
    "SchemaService",
    "SingerStreamModel",
    "StorageModeModel",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "configure_oracle_observability",
    "e",
    "logger",
    "m",
    "main",
    "p",
    "s",
    "t",
    "u",
    "validate_oracle_configuration",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
