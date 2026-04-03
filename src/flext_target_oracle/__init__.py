# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target oracle package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_db_oracle.exceptions import FlextDbOracleExceptions as e
    from flext_target_oracle import (
        _models,
        _utilities,
        api,
        cli,
        client,
        commands,
        config,
        constants,
        errors,
        loader,
        models,
        observability,
        protocols,
        results,
        services,
        settings,
        singer,
        typings,
        utilities,
    )
    from flext_target_oracle._models import (
        FlextTargetOracleModelsCommands,
        FlextTargetOracleModelsConfig,
        FlextTargetOracleModelsResults,
        FlextTargetOracleModelsSinger,
    )
    from flext_target_oracle._utilities import (
        FlextOracleError,
        FlextOracleObs,
        FlextTargetOracle,
        FlextTargetOracleCliService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleExceptions,
        FlextTargetOracleLoader,
        code,
        configure_oracle_observability,
        context,
        correlation_id,
        main,
    )
    from flext_target_oracle.api import FlextTargetOracleService
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
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
        "_models": "flext_target_oracle._models",
        "_utilities": "flext_target_oracle._utilities",
        "api": "flext_target_oracle.api",
        "c": ("flext_target_oracle.constants", "FlextTargetOracleConstants"),
        "cli": "flext_target_oracle.cli",
        "client": "flext_target_oracle.client",
        "commands": "flext_target_oracle.commands",
        "config": "flext_target_oracle.config",
        "constants": "flext_target_oracle.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_db_oracle.exceptions", "FlextDbOracleExceptions"),
        "errors": "flext_target_oracle.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "loader": "flext_target_oracle.loader",
        "logger": "flext_target_oracle.settings",
        "m": ("flext_target_oracle.models", "FlextTargetOracleModels"),
        "models": "flext_target_oracle.models",
        "observability": "flext_target_oracle.observability",
        "p": ("flext_target_oracle.protocols", "FlextTargetOracleProtocols"),
        "protocols": "flext_target_oracle.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "results": "flext_target_oracle.results",
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_target_oracle.services",
        "settings": "flext_target_oracle.settings",
        "singer": "flext_target_oracle.singer",
        "t": ("flext_target_oracle.typings", "FlextTargetOracleTypes"),
        "typings": "flext_target_oracle.typings",
        "u": ("flext_target_oracle.utilities", "FlextTargetOracleUtilities"),
        "utilities": "flext_target_oracle.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
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
