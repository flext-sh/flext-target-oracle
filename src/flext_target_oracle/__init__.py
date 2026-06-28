# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Target Oracle package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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

if _t.TYPE_CHECKING:
    from flext_meltano import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_target_oracle._constants.base import (
        FlextTargetOracleConstantsBase as FlextTargetOracleConstantsBase,
    )
    from flext_target_oracle._models.commands import (
        FlextTargetOracleModelsCommands as FlextTargetOracleModelsCommands,
    )
    from flext_target_oracle._models.results import (
        FlextTargetOracleModelsResults as FlextTargetOracleModelsResults,
    )
    from flext_target_oracle._models.settings import (
        FlextTargetOracleModelsSettings as FlextTargetOracleModelsSettings,
    )
    from flext_target_oracle._models.singer import (
        FlextTargetOracleModelsSinger as FlextTargetOracleModelsSinger,
    )
    from flext_target_oracle._protocols.base import (
        FlextTargetOracleProtocolsBase as FlextTargetOracleProtocolsBase,
    )
    from flext_target_oracle._typings.base import (
        FlextTargetOracleTypesBase as FlextTargetOracleTypesBase,
    )
    from flext_target_oracle._utilities.base import (
        FlextTargetOracleUtilitiesBase as FlextTargetOracleUtilitiesBase,
    )
    from flext_target_oracle._utilities.cli import (
        FlextTargetOracleCliService as FlextTargetOracleCliService,
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
        FlextTargetOracleUtilitiesObservability as FlextTargetOracleUtilitiesObservability,
    )
    from flext_target_oracle._utilities.services import (
        FlextTargetOracleBatchService as FlextTargetOracleBatchService,
        FlextTargetOracleConnectionService as FlextTargetOracleConnectionService,
        FlextTargetOracleRecordService as FlextTargetOracleRecordService,
        FlextTargetOracleSchemaService as FlextTargetOracleSchemaService,
    )
    from flext_target_oracle.api import (
        FlextTargetOracleService as FlextTargetOracleService,
        target_oracle as target_oracle,
    )
    from flext_target_oracle.constants import (
        FlextTargetOracleConstants as FlextTargetOracleConstants,
        c as c,
    )
    from flext_target_oracle.models import (
        FlextTargetOracleModels as FlextTargetOracleModels,
        m as m,
    )
    from flext_target_oracle.protocols import (
        FlextTargetOracleProtocols as FlextTargetOracleProtocols,
        p as p,
    )
    from flext_target_oracle.settings import (
        FlextTargetOracleSettings as FlextTargetOracleSettings,
    )
    from flext_target_oracle.typings import (
        FlextTargetOracleTypes as FlextTargetOracleTypes,
        t as t,
    )
    from flext_target_oracle.utilities import (
        FlextTargetOracleUtilities as FlextTargetOracleUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._constants",
        "._models",
        "._protocols",
        "._typings",
        "._utilities",
    ),
    build_lazy_import_map(
        {
            "._constants.base": ("FlextTargetOracleConstantsBase",),
            "._models.commands": ("FlextTargetOracleModelsCommands",),
            "._models.results": ("FlextTargetOracleModelsResults",),
            "._models.settings": ("FlextTargetOracleModelsSettings",),
            "._models.singer": ("FlextTargetOracleModelsSinger",),
            "._protocols.base": ("FlextTargetOracleProtocolsBase",),
            "._typings.base": ("FlextTargetOracleTypesBase",),
            "._utilities.base": ("FlextTargetOracleUtilitiesBase",),
            "._utilities.cli": ("FlextTargetOracleCliService",),
            "._utilities.client": ("FlextTargetOracle",),
            "._utilities.errors": (
                "FlextTargetOracleErrorMetadata",
                "FlextTargetOracleExceptions",
            ),
            "._utilities.loader": ("FlextTargetOracleLoader",),
            "._utilities.observability": ("FlextTargetOracleUtilitiesObservability",),
            "._utilities.services": (
                "FlextTargetOracleBatchService",
                "FlextTargetOracleConnectionService",
                "FlextTargetOracleRecordService",
                "FlextTargetOracleSchemaService",
            ),
            ".api": (
                "FlextTargetOracleService",
                "target_oracle",
            ),
            ".constants": (
                "FlextTargetOracleConstants",
                "c",
            ),
            ".models": (
                "FlextTargetOracleModels",
                "m",
            ),
            ".protocols": (
                "FlextTargetOracleProtocols",
                "p",
            ),
            ".settings": ("FlextTargetOracleSettings",),
            ".typings": (
                "FlextTargetOracleTypes",
                "t",
            ),
            ".utilities": (
                "FlextTargetOracleUtilities",
                "u",
            ),
            "flext_meltano": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
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

__all__: list[str] = [
    "FlextTargetOracleConstants",
    "FlextTargetOracleModels",
    "FlextTargetOracleProtocols",
    "FlextTargetOracleService",
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
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "target_oracle",
    "u",
    "x",
]
