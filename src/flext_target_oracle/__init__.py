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
    from flext_db_oracle import *

    from flext_target_oracle import (
        constants,
        models,
        protocols,
        settings,
        target_client,
        target_exceptions,
        target_loader,
        target_observability,
        target_refactored,
        target_service,
        target_services,
        typings,
        utilities,
    )
    from flext_target_oracle._models import *
    from flext_target_oracle._utilities import *
    from flext_target_oracle.constants import *
    from flext_target_oracle.models import *
    from flext_target_oracle.protocols import *
    from flext_target_oracle.settings import *
    from flext_target_oracle.typings import *
    from flext_target_oracle.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextOracleError": "flext_target_oracle._utilities.observability",
    "FlextOracleObs": "flext_target_oracle._utilities.observability",
    "FlextTargetOracle": "flext_target_oracle._utilities.client",
    "FlextTargetOracleBatchService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleCliService": "flext_target_oracle._utilities.cli",
    "FlextTargetOracleConnectionService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleConstants": "flext_target_oracle.constants",
    "FlextTargetOracleErrorMetadata": "flext_target_oracle._utilities.errors",
    "FlextTargetOracleExceptions": "flext_target_oracle._utilities.errors",
    "FlextTargetOracleLoader": "flext_target_oracle._utilities.loader",
    "FlextTargetOracleModels": "flext_target_oracle.models",
    "FlextTargetOracleModelsCommands": "flext_target_oracle._models.commands",
    "FlextTargetOracleModelsConfig": "flext_target_oracle._models.config",
    "FlextTargetOracleModelsResults": "flext_target_oracle._models.results",
    "FlextTargetOracleModelsSinger": "flext_target_oracle._models.singer",
    "FlextTargetOracleProtocols": "flext_target_oracle.protocols",
    "FlextTargetOracleRecordService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleSchemaService": "flext_target_oracle._utilities.services",
    "FlextTargetOracleService": "flext_target_oracle._utilities.service",
    "FlextTargetOracleServiceFactory": "flext_target_oracle._utilities.services",
    "FlextTargetOracleSettings": "flext_target_oracle.settings",
    "FlextTargetOracleTypes": "flext_target_oracle.typings",
    "FlextTargetOracleUtilities": "flext_target_oracle.utilities",
    "_models": "flext_target_oracle._models",
    "_utilities": "flext_target_oracle._utilities",
    "c": ["flext_target_oracle.constants", "FlextTargetOracleConstants"],
    "cli": "flext_target_oracle._utilities.cli",
    "client": "flext_target_oracle._utilities.client",
    "commands": "flext_target_oracle._models.commands",
    "config": "flext_target_oracle._models.config",
    "configure_oracle_observability": "flext_target_oracle._utilities.observability",
    "constants": "flext_target_oracle.constants",
    "d": "flext_db_oracle",
    "e": "flext_db_oracle",
    "errors": "flext_target_oracle._utilities.errors",
    "h": "flext_db_oracle",
    "load_target_settings": "flext_target_oracle._models.commands",
    "loader": "flext_target_oracle._utilities.loader",
    "logger": "flext_target_oracle.settings",
    "m": ["flext_target_oracle.models", "FlextTargetOracleModels"],
    "main": "flext_target_oracle._utilities.cli",
    "models": "flext_target_oracle.models",
    "observability": "flext_target_oracle._utilities.observability",
    "p": ["flext_target_oracle.protocols", "FlextTargetOracleProtocols"],
    "protocols": "flext_target_oracle.protocols",
    "r": "flext_db_oracle",
    "results": "flext_target_oracle._models.results",
    "s": "flext_db_oracle",
    "service": "flext_target_oracle._utilities.service",
    "services": "flext_target_oracle._utilities.services",
    "settings": "flext_target_oracle.settings",
    "singer": "flext_target_oracle._models.singer",
    "t": ["flext_target_oracle.typings", "FlextTargetOracleTypes"],
    "target_client": "flext_target_oracle.target_client",
    "target_exceptions": "flext_target_oracle.target_exceptions",
    "target_loader": "flext_target_oracle.target_loader",
    "target_observability": "flext_target_oracle.target_observability",
    "target_refactored": "flext_target_oracle.target_refactored",
    "target_service": "flext_target_oracle.target_service",
    "target_services": "flext_target_oracle.target_services",
    "typings": "flext_target_oracle.typings",
    "u": ["flext_target_oracle.utilities", "FlextTargetOracleUtilities"],
    "utilities": "flext_target_oracle.utilities",
    "x": "flext_db_oracle",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
