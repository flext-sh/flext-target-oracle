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
    from flext_core import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

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
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants,
        FlextTargetOracleConstants as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels,
        FlextTargetOracleModels as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols,
        FlextTargetOracleProtocols as p,
    )
    from flext_target_oracle.settings import (
        FlextTargetOracleSettings,
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
        OracleErrorMetadata,
    )
    from flext_target_oracle.target_loader import FlextTargetOracleLoader
    from flext_target_oracle.target_models import (
        LoadStatisticsModel,
        OracleConnectionModel,
        SingerStreamModel,
    )
    from flext_target_oracle.target_observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )
    from flext_target_oracle.target_refactored import FlextTargetOracleCliService, main
    from flext_target_oracle.target_service import FlextTargetOracleService
    from flext_target_oracle.target_services import (
        OracleBatchService,
        OracleConnectionService,
        OracleRecordService,
        OracleSchemaService,
        OracleTargetServiceFactory,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
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
    "OracleErrorMetadata": (
        "flext_target_oracle.target_exceptions",
        "OracleErrorMetadata",
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
    "SingerStreamModel": ("flext_target_oracle.target_models", "SingerStreamModel"),
    "__all__": ("flext_target_oracle.__version__", "__all__"),
    "__author__": ("flext_target_oracle.__version__", "__author__"),
    "__author_email__": ("flext_target_oracle.__version__", "__author_email__"),
    "__description__": ("flext_target_oracle.__version__", "__description__"),
    "__license__": ("flext_target_oracle.__version__", "__license__"),
    "__title__": ("flext_target_oracle.__version__", "__title__"),
    "__url__": ("flext_target_oracle.__version__", "__url__"),
    "__version__": ("flext_target_oracle.__version__", "__version__"),
    "__version_info__": ("flext_target_oracle.__version__", "__version_info__"),
    "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
    "configure_oracle_observability": (
        "flext_target_oracle.target_observability",
        "configure_oracle_observability",
    ),
    "d": ("flext_db_oracle", "d"),
    "e": ("flext_db_oracle", "e"),
    "h": ("flext_db_oracle", "h"),
    "logger": ("flext_target_oracle.settings", "logger"),
    "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
    "main": ("flext_target_oracle.target_refactored", "main"),
    "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
    "r": ("flext_db_oracle", "r"),
    "s": ("flext_db_oracle", "s"),
    "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
    "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
    "validate_oracle_configuration": (
        "flext_target_oracle.settings",
        "validate_oracle_configuration",
    ),
    "x": ("flext_db_oracle", "x"),
}

__all__ = [
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
    "LoadStatisticsModel",
    "OracleBatchService",
    "OracleConnectionModel",
    "OracleConnectionService",
    "OracleErrorMetadata",
    "OracleRecordService",
    "OracleSchemaService",
    "OracleTargetAboutCommand",
    "OracleTargetCommandFactory",
    "OracleTargetCommandHandler",
    "OracleTargetLoadCommand",
    "OracleTargetServiceFactory",
    "OracleTargetValidateCommand",
    "SingerStreamModel",
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
    "d",
    "e",
    "h",
    "logger",
    "m",
    "main",
    "p",
    "r",
    "s",
    "t",
    "u",
    "validate_oracle_configuration",
    "x",
]


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
