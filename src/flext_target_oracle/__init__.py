# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

from flext_target_oracle.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

    from flext_target_oracle import _models, _utilities
    from flext_target_oracle._models.commands import (
        FlextTargetOracleModelsCommands,
        load_target_settings,
    )
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger
    from flext_target_oracle._utilities.cli import FlextTargetOracleCliService, main
    from flext_target_oracle._utilities.client import FlextTargetOracle
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
    )
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
    from flext_target_oracle._utilities.observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )
    from flext_target_oracle._utilities.service import FlextTargetOracleService
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory,
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
    from flext_target_oracle.settings import FlextTargetOracleSettings, logger
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleError": [
        "flext_target_oracle._utilities.observability",
        "FlextOracleError",
    ],
    "FlextOracleObs": [
        "flext_target_oracle._utilities.observability",
        "FlextOracleObs",
    ],
    "FlextTargetOracle": ["flext_target_oracle._utilities.client", "FlextTargetOracle"],
    "FlextTargetOracleBatchService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleBatchService",
    ],
    "FlextTargetOracleCliService": [
        "flext_target_oracle._utilities.cli",
        "FlextTargetOracleCliService",
    ],
    "FlextTargetOracleConnectionService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleConnectionService",
    ],
    "FlextTargetOracleConstants": [
        "flext_target_oracle.constants",
        "FlextTargetOracleConstants",
    ],
    "FlextTargetOracleErrorMetadata": [
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleErrorMetadata",
    ],
    "FlextTargetOracleExceptions": [
        "flext_target_oracle._utilities.errors",
        "FlextTargetOracleExceptions",
    ],
    "FlextTargetOracleLoader": [
        "flext_target_oracle._utilities.loader",
        "FlextTargetOracleLoader",
    ],
    "FlextTargetOracleModels": [
        "flext_target_oracle.models",
        "FlextTargetOracleModels",
    ],
    "FlextTargetOracleModelsCommands": [
        "flext_target_oracle._models.commands",
        "FlextTargetOracleModelsCommands",
    ],
    "FlextTargetOracleModelsConfig": [
        "flext_target_oracle._models.config",
        "FlextTargetOracleModelsConfig",
    ],
    "FlextTargetOracleModelsResults": [
        "flext_target_oracle._models.results",
        "FlextTargetOracleModelsResults",
    ],
    "FlextTargetOracleModelsSinger": [
        "flext_target_oracle._models.singer",
        "FlextTargetOracleModelsSinger",
    ],
    "FlextTargetOracleProtocols": [
        "flext_target_oracle.protocols",
        "FlextTargetOracleProtocols",
    ],
    "FlextTargetOracleRecordService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleRecordService",
    ],
    "FlextTargetOracleSchemaService": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleSchemaService",
    ],
    "FlextTargetOracleService": [
        "flext_target_oracle._utilities.service",
        "FlextTargetOracleService",
    ],
    "FlextTargetOracleServiceFactory": [
        "flext_target_oracle._utilities.services",
        "FlextTargetOracleServiceFactory",
    ],
    "FlextTargetOracleSettings": [
        "flext_target_oracle.settings",
        "FlextTargetOracleSettings",
    ],
    "FlextTargetOracleTypes": ["flext_target_oracle.typings", "FlextTargetOracleTypes"],
    "FlextTargetOracleUtilities": [
        "flext_target_oracle.utilities",
        "FlextTargetOracleUtilities",
    ],
    "_models": ["flext_target_oracle._models", ""],
    "_utilities": ["flext_target_oracle._utilities", ""],
    "c": ["flext_target_oracle.constants", "FlextTargetOracleConstants"],
    "configure_oracle_observability": [
        "flext_target_oracle._utilities.observability",
        "configure_oracle_observability",
    ],
    "d": ["flext_db_oracle", "d"],
    "e": ["flext_db_oracle", "e"],
    "h": ["flext_db_oracle", "h"],
    "load_target_settings": [
        "flext_target_oracle._models.commands",
        "load_target_settings",
    ],
    "logger": ["flext_target_oracle.settings", "logger"],
    "m": ["flext_target_oracle.models", "FlextTargetOracleModels"],
    "main": ["flext_target_oracle._utilities.cli", "main"],
    "p": ["flext_target_oracle.protocols", "FlextTargetOracleProtocols"],
    "r": ["flext_db_oracle", "r"],
    "s": ["flext_db_oracle", "s"],
    "t": ["flext_target_oracle.typings", "FlextTargetOracleTypes"],
    "u": ["flext_target_oracle.utilities", "FlextTargetOracleUtilities"],
    "x": ["flext_db_oracle", "x"],
}

__all__ = [
    "FlextOracleError",
    "FlextOracleObs",
    "FlextTargetOracle",
    "FlextTargetOracleBatchService",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleConstants",
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsConfig",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSinger",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleService",
    "FlextTargetOracleServiceFactory",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_models",
    "_utilities",
    "c",
    "configure_oracle_observability",
    "d",
    "e",
    "h",
    "load_target_settings",
    "logger",
    "m",
    "main",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
