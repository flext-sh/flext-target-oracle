# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

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
        "._constants",
        "._models",
        "._protocols",
        "._typings",
        "._utilities",
    ),
    {
        "FlextTargetOracleConstants": ".constants",
        "FlextTargetOracleModels": ".models",
        "FlextTargetOracleProtocols": ".protocols",
        "FlextTargetOracleService": ".api",
        "FlextTargetOracleSettings": ".settings",
        "FlextTargetOracleTypes": ".typings",
        "FlextTargetOracleUtilities": ".utilities",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version__": ".__version__",
        "__version_info__": ".__version__",
        "c": (".constants", "FlextTargetOracleConstants"),
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": (".models", "FlextTargetOracleModels"),
        "p": (".protocols", "FlextTargetOracleProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "s": (".api", "FlextTargetOracleService"),
        "t": (".typings", "FlextTargetOracleTypes"),
        "u": (".utilities", "FlextTargetOracleUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)

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
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
