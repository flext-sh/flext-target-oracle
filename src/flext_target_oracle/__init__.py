# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_target_oracle.__version__ import *

if _t.TYPE_CHECKING:
    import flext_target_oracle._models as _flext_target_oracle__models
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

    _models = _flext_target_oracle__models
    import flext_target_oracle._models.commands as _flext_target_oracle__models_commands

    commands = _flext_target_oracle__models_commands
    import flext_target_oracle._models.config as _flext_target_oracle__models_config
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands

    config = _flext_target_oracle__models_config
    import flext_target_oracle._models.results as _flext_target_oracle__models_results
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig

    results = _flext_target_oracle__models_results
    import flext_target_oracle._models.singer as _flext_target_oracle__models_singer
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults

    singer = _flext_target_oracle__models_singer
    import flext_target_oracle._utilities as _flext_target_oracle__utilities
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger

    _utilities = _flext_target_oracle__utilities
    import flext_target_oracle._utilities.cli as _flext_target_oracle__utilities_cli

    cli = _flext_target_oracle__utilities_cli
    import flext_target_oracle._utilities.client as _flext_target_oracle__utilities_client
    from flext_target_oracle._utilities.cli import FlextTargetOracleCliService, main

    client = _flext_target_oracle__utilities_client
    import flext_target_oracle._utilities.errors as _flext_target_oracle__utilities_errors
    from flext_target_oracle._utilities.client import FlextTargetOracle

    errors = _flext_target_oracle__utilities_errors
    import flext_target_oracle._utilities.loader as _flext_target_oracle__utilities_loader
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
    )

    loader = _flext_target_oracle__utilities_loader
    import flext_target_oracle._utilities.observability as _flext_target_oracle__utilities_observability
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader

    observability = _flext_target_oracle__utilities_observability
    import flext_target_oracle._utilities.services as _flext_target_oracle__utilities_services
    from flext_target_oracle._utilities.observability import (
        FlextOracleError,
        FlextOracleObs,
        configure_oracle_observability,
    )

    services = _flext_target_oracle__utilities_services
    import flext_target_oracle.api as _flext_target_oracle_api
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory,
    )

    api = _flext_target_oracle_api
    import flext_target_oracle.constants as _flext_target_oracle_constants
    from flext_target_oracle.api import (
        FlextTargetOracleService,
        FlextTargetOracleService as s,
    )

    constants = _flext_target_oracle_constants
    import flext_target_oracle.models as _flext_target_oracle_models
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants,
        FlextTargetOracleConstants as c,
    )

    models = _flext_target_oracle_models
    import flext_target_oracle.protocols as _flext_target_oracle_protocols
    from flext_target_oracle.models import (
        FlextTargetOracleModels,
        FlextTargetOracleModels as m,
    )

    protocols = _flext_target_oracle_protocols
    import flext_target_oracle.settings as _flext_target_oracle_settings
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols,
        FlextTargetOracleProtocols as p,
    )

    settings = _flext_target_oracle_settings
    import flext_target_oracle.typings as _flext_target_oracle_typings
    from flext_target_oracle.settings import FlextTargetOracleSettings

    typings = _flext_target_oracle_typings
    import flext_target_oracle.utilities as _flext_target_oracle_utilities
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )

    utilities = _flext_target_oracle_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_target_oracle._models",
        "flext_target_oracle._utilities",
    ),
    {
        "FlextTargetOracleConstants": "flext_target_oracle.constants",
        "FlextTargetOracleModels": "flext_target_oracle.models",
        "FlextTargetOracleProtocols": "flext_target_oracle.protocols",
        "FlextTargetOracleService": "flext_target_oracle.api",
        "FlextTargetOracleSettings": "flext_target_oracle.settings",
        "FlextTargetOracleTypes": "flext_target_oracle.typings",
        "FlextTargetOracleUtilities": "flext_target_oracle.utilities",
        "__author__": "flext_target_oracle.__version__",
        "__author_email__": "flext_target_oracle.__version__",
        "__description__": "flext_target_oracle.__version__",
        "__license__": "flext_target_oracle.__version__",
        "__title__": "flext_target_oracle.__version__",
        "__url__": "flext_target_oracle.__version__",
        "__version__": "flext_target_oracle.__version__",
        "__version_info__": "flext_target_oracle.__version__",
        "_models": "flext_target_oracle._models",
        "_utilities": "flext_target_oracle._utilities",
        "api": "flext_target_oracle.api",
        "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
        "constants": "flext_target_oracle.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
        "models": "flext_target_oracle.models",
        "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
        "protocols": "flext_target_oracle.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_target_oracle.api", "FlextTargetOracleService"),
        "settings": "flext_target_oracle.settings",
        "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
        "typings": "flext_target_oracle.typings",
        "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
        "utilities": "flext_target_oracle.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

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
    "api",
    "c",
    "cli",
    "client",
    "commands",
    "config",
    "configure_oracle_observability",
    "constants",
    "d",
    "e",
    "errors",
    "h",
    "loader",
    "m",
    "main",
    "models",
    "observability",
    "p",
    "protocols",
    "r",
    "results",
    "s",
    "services",
    "settings",
    "singer",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
