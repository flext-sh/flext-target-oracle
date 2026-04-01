# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Production-Grade Singer Target for Oracle Database data loading.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_db_oracle import d, e, h, r, s, x

    from flext_target_oracle import (
        _models,
        _utilities,
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
    from flext_target_oracle._models import (
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsConfig,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSinger,
        commands,
        config,
        load_target_settings,
        results,
        singer,
    )
    from flext_target_oracle._utilities import (
        FlextOracleError,
        FlextOracleObs,
        FlextTargetOracle,
        FlextTargetOracleBatchService,
        FlextTargetOracleCliService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
        FlextTargetOracleLoader,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
        FlextTargetOracleService,
        FlextTargetOracleServiceFactory,
        cli,
        client,
        configure_oracle_observability,
        errors,
        loader,
        main,
        observability,
        service,
        services,
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    (
        "flext_target_oracle._models",
        "flext_target_oracle._utilities",
    ),
    {
        "FlextTargetOracleConstants": "flext_target_oracle.constants",
        "FlextTargetOracleModels": "flext_target_oracle.models",
        "FlextTargetOracleProtocols": "flext_target_oracle.protocols",
        "FlextTargetOracleSettings": "flext_target_oracle.settings",
        "FlextTargetOracleTypes": "flext_target_oracle.typings",
        "FlextTargetOracleUtilities": "flext_target_oracle.utilities",
        "_models": "flext_target_oracle._models",
        "_utilities": "flext_target_oracle._utilities",
        "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
        "constants": "flext_target_oracle.constants",
        "d": "flext_db_oracle",
        "e": "flext_db_oracle",
        "h": "flext_db_oracle",
        "logger": "flext_target_oracle.settings",
        "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
        "models": "flext_target_oracle.models",
        "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
        "protocols": "flext_target_oracle.protocols",
        "r": "flext_db_oracle",
        "s": "flext_db_oracle",
        "settings": "flext_target_oracle.settings",
        "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
        "target_client": "flext_target_oracle.target_client",
        "target_exceptions": "flext_target_oracle.target_exceptions",
        "target_loader": "flext_target_oracle.target_loader",
        "target_observability": "flext_target_oracle.target_observability",
        "target_refactored": "flext_target_oracle.target_refactored",
        "target_service": "flext_target_oracle.target_service",
        "target_services": "flext_target_oracle.target_services",
        "typings": "flext_target_oracle.typings",
        "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
        "utilities": "flext_target_oracle.utilities",
        "x": "flext_db_oracle",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
