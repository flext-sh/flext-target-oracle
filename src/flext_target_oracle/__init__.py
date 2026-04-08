# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext target oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_target_oracle.__version__ import *

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_target_oracle import (
        _constants,
        _models,
        _protocols,
        _typings,
        _utilities,
        api,
        constants,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_target_oracle._constants.base import FlextTargetOracleConstantsBase
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger
    from flext_target_oracle._protocols.base import FlextTargetOracleProtocolsBase
    from flext_target_oracle._typings.base import FlextTargetOracleTypesBase
    from flext_target_oracle._utilities.base import FlextTargetOracleUtilitiesBase
    from flext_target_oracle._utilities.cli import FlextTargetOracleCliService
    from flext_target_oracle._utilities.client import FlextTargetOracle
    from flext_target_oracle._utilities.errors import (
        FlextTargetOracleErrorMetadata,
        FlextTargetOracleExceptions,
    )
    from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
    from flext_target_oracle._utilities.observability import (
        FlextTargetOracleUtilitiesObservability,
    )
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService,
        FlextTargetOracleServiceFactory,
    )
    from flext_target_oracle.api import (
        FlextTargetOracleService,
        FlextTargetOracleService as s,
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
    from flext_target_oracle.settings import FlextTargetOracleSettings
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes,
        FlextTargetOracleTypes as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities,
        FlextTargetOracleUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_target_oracle._constants",
        "flext_target_oracle._models",
        "flext_target_oracle._protocols",
        "flext_target_oracle._typings",
        "flext_target_oracle._utilities",
    ),
    {
        "FlextTargetOracleConstants": (
            "flext_target_oracle.constants",
            "FlextTargetOracleConstants",
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
            "flext_target_oracle.api",
            "FlextTargetOracleService",
        ),
        "FlextTargetOracleSettings": (
            "flext_target_oracle.settings",
            "FlextTargetOracleSettings",
        ),
        "FlextTargetOracleTypes": (
            "flext_target_oracle.typings",
            "FlextTargetOracleTypes",
        ),
        "FlextTargetOracleUtilities": (
            "flext_target_oracle.utilities",
            "FlextTargetOracleUtilities",
        ),
        "__author__": ("flext_target_oracle.__version__", "__author__"),
        "__author_email__": ("flext_target_oracle.__version__", "__author_email__"),
        "__description__": ("flext_target_oracle.__version__", "__description__"),
        "__license__": ("flext_target_oracle.__version__", "__license__"),
        "__title__": ("flext_target_oracle.__version__", "__title__"),
        "__url__": ("flext_target_oracle.__version__", "__url__"),
        "__version__": ("flext_target_oracle.__version__", "__version__"),
        "__version_info__": ("flext_target_oracle.__version__", "__version_info__"),
        "_constants": "flext_target_oracle._constants",
        "_models": "flext_target_oracle._models",
        "_protocols": "flext_target_oracle._protocols",
        "_typings": "flext_target_oracle._typings",
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
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "FlextTargetOracle",
    "FlextTargetOracleBatchService",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleConstants",
    "FlextTargetOracleConstantsBase",
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleModels",
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsConfig",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSinger",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleProtocolsBase",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleService",
    "FlextTargetOracleServiceFactory",
    "FlextTargetOracleSettings",
    "FlextTargetOracleTypes",
    "FlextTargetOracleTypesBase",
    "FlextTargetOracleUtilities",
    "FlextTargetOracleUtilitiesBase",
    "FlextTargetOracleUtilitiesObservability",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_constants",
    "_models",
    "_protocols",
    "_typings",
    "_utilities",
    "api",
    "c",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
