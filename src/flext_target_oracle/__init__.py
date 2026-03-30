# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_target_oracle.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_db_oracle import d, e, h, r, s, x

    from flext_target_oracle import (
        _models as _models,
        _utilities as _utilities,
        constants as constants,
        models as models,
        protocols as protocols,
        settings as settings,
        target_client as target_client,
        target_exceptions as target_exceptions,
        target_loader as target_loader,
        target_observability as target_observability,
        target_refactored as target_refactored,
        target_service as target_service,
        target_services as target_services,
        typings as typings,
        utilities as utilities,
    )
    from flext_target_oracle._models import (
        commands as commands,
        config as config,
        results as results,
        singer as singer,
    )
    from flext_target_oracle._models.commands import (
        FlextTargetOracleModelsCommands as FlextTargetOracleModelsCommands,
        load_target_settings as load_target_settings,
    )
    from flext_target_oracle._models.config import (
        FlextTargetOracleModelsConfig as FlextTargetOracleModelsConfig,
    )
    from flext_target_oracle._models.results import (
        FlextTargetOracleModelsResults as FlextTargetOracleModelsResults,
    )
    from flext_target_oracle._models.singer import (
        FlextTargetOracleModelsSinger as FlextTargetOracleModelsSinger,
    )
    from flext_target_oracle._utilities import (
        cli as cli,
        client as client,
        errors as errors,
        loader as loader,
        observability as observability,
        service as service,
        services as services,
    )
    from flext_target_oracle._utilities.cli import (
        FlextTargetOracleCliService as FlextTargetOracleCliService,
        main as main,
    )
    from flext_target_oracle._utilities.client import (
        FlextTargetOracle as FlextTargetOracle,
    )
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata as FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions as FlextTargetOracleExceptions,
    )
    from flext_target_oracle._utilities.loader import (
        FlextTargetOracleLoader as FlextTargetOracleLoader,
    )
    from flext_target_oracle._utilities.observability import (
        FlextOracleError as FlextOracleError,
        FlextOracleObs as FlextOracleObs,
        configure_oracle_observability as configure_oracle_observability,
    )
    from flext_target_oracle._utilities.service import (
        FlextTargetOracleService as FlextTargetOracleService,
    )
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService as FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService as FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService as FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService as FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory as FlextTargetOracleServiceFactory,
    )
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants as FlextTargetOracleConstants,
        FlextTargetOracleConstants as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels as FlextTargetOracleModels,
        FlextTargetOracleModels as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols as FlextTargetOracleProtocols,
        FlextTargetOracleProtocols as p,
    )
    from flext_target_oracle.settings import (
        FlextTargetOracleSettings as FlextTargetOracleSettings,
        logger as logger,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes as FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities as FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleError": ["flext_target_oracle._utilities.observability", "FlextOracleError"],
    "FlextOracleObs": ["flext_target_oracle._utilities.observability", "FlextOracleObs"],
    "FlextTargetOracle": ["flext_target_oracle._utilities.client", "FlextTargetOracle"],
    "FlextTargetOracleBatchService": ["flext_target_oracle._utilities.services", "FlextTargetOracleBatchService"],
    "FlextTargetOracleCliService": ["flext_target_oracle._utilities.cli", "FlextTargetOracleCliService"],
    "FlextTargetOracleConnectionService": ["flext_target_oracle._utilities.services", "FlextTargetOracleConnectionService"],
    "FlextTargetOracleConstants": ["flext_target_oracle.constants", "FlextTargetOracleConstants"],
    "FlextTargetOracleErrorMetadata": ["flext_target_oracle._utilities.errors", "FlextTargetOracleErrorMetadata"],
    "FlextTargetOracleExceptions": ["flext_target_oracle._utilities.errors", "FlextTargetOracleExceptions"],
    "FlextTargetOracleLoader": ["flext_target_oracle._utilities.loader", "FlextTargetOracleLoader"],
    "FlextTargetOracleModels": ["flext_target_oracle.models", "FlextTargetOracleModels"],
    "FlextTargetOracleModelsCommands": ["flext_target_oracle._models.commands", "FlextTargetOracleModelsCommands"],
    "FlextTargetOracleModelsConfig": ["flext_target_oracle._models.config", "FlextTargetOracleModelsConfig"],
    "FlextTargetOracleModelsResults": ["flext_target_oracle._models.results", "FlextTargetOracleModelsResults"],
    "FlextTargetOracleModelsSinger": ["flext_target_oracle._models.singer", "FlextTargetOracleModelsSinger"],
    "FlextTargetOracleProtocols": ["flext_target_oracle.protocols", "FlextTargetOracleProtocols"],
    "FlextTargetOracleRecordService": ["flext_target_oracle._utilities.services", "FlextTargetOracleRecordService"],
    "FlextTargetOracleSchemaService": ["flext_target_oracle._utilities.services", "FlextTargetOracleSchemaService"],
    "FlextTargetOracleService": ["flext_target_oracle._utilities.service", "FlextTargetOracleService"],
    "FlextTargetOracleServiceFactory": ["flext_target_oracle._utilities.services", "FlextTargetOracleServiceFactory"],
    "FlextTargetOracleSettings": ["flext_target_oracle.settings", "FlextTargetOracleSettings"],
    "FlextTargetOracleTypes": ["flext_target_oracle.typings", "FlextTargetOracleTypes"],
    "FlextTargetOracleUtilities": ["flext_target_oracle.utilities", "FlextTargetOracleUtilities"],
    "_models": ["flext_target_oracle._models", ""],
    "_utilities": ["flext_target_oracle._utilities", ""],
    "c": ["flext_target_oracle.constants", "FlextTargetOracleConstants"],
    "cli": ["flext_target_oracle._utilities.cli", ""],
    "client": ["flext_target_oracle._utilities.client", ""],
    "commands": ["flext_target_oracle._models.commands", ""],
    "config": ["flext_target_oracle._models.config", ""],
    "configure_oracle_observability": ["flext_target_oracle._utilities.observability", "configure_oracle_observability"],
    "constants": ["flext_target_oracle.constants", ""],
    "d": ["flext_db_oracle", "d"],
    "e": ["flext_db_oracle", "e"],
    "errors": ["flext_target_oracle._utilities.errors", ""],
    "h": ["flext_db_oracle", "h"],
    "load_target_settings": ["flext_target_oracle._models.commands", "load_target_settings"],
    "loader": ["flext_target_oracle._utilities.loader", ""],
    "logger": ["flext_target_oracle.settings", "logger"],
    "m": ["flext_target_oracle.models", "FlextTargetOracleModels"],
    "main": ["flext_target_oracle._utilities.cli", "main"],
    "models": ["flext_target_oracle.models", ""],
    "observability": ["flext_target_oracle._utilities.observability", ""],
    "p": ["flext_target_oracle.protocols", "FlextTargetOracleProtocols"],
    "protocols": ["flext_target_oracle.protocols", ""],
    "r": ["flext_db_oracle", "r"],
    "results": ["flext_target_oracle._models.results", ""],
    "s": ["flext_db_oracle", "s"],
    "service": ["flext_target_oracle._utilities.service", ""],
    "services": ["flext_target_oracle._utilities.services", ""],
    "settings": ["flext_target_oracle.settings", ""],
    "singer": ["flext_target_oracle._models.singer", ""],
    "t": ["flext_target_oracle.typings", "FlextTargetOracleTypes"],
    "target_client": ["flext_target_oracle.target_client", ""],
    "target_exceptions": ["flext_target_oracle.target_exceptions", ""],
    "target_loader": ["flext_target_oracle.target_loader", ""],
    "target_observability": ["flext_target_oracle.target_observability", ""],
    "target_refactored": ["flext_target_oracle.target_refactored", ""],
    "target_service": ["flext_target_oracle.target_service", ""],
    "target_services": ["flext_target_oracle.target_services", ""],
    "typings": ["flext_target_oracle.typings", ""],
    "u": ["flext_target_oracle.utilities", "FlextTargetOracleUtilities"],
    "utilities": ["flext_target_oracle.utilities", ""],
    "x": ["flext_db_oracle", "x"],
}

_EXPORTS: Sequence[str] = [
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
    "load_target_settings",
    "loader",
    "logger",
    "m",
    "main",
    "models",
    "observability",
    "p",
    "protocols",
    "r",
    "results",
    "s",
    "service",
    "services",
    "settings",
    "singer",
    "t",
    "target_client",
    "target_exceptions",
    "target_loader",
    "target_observability",
    "target_refactored",
    "target_service",
    "target_services",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
