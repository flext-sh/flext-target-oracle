# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

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

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextOracleError": ["flext_target_oracle._utilities.observability", "FlextOracleError"],
    "FlextOracleObs": ["flext_target_oracle._utilities.observability", "FlextOracleObs"],
    "FlextTargetOracle": ["flext_target_oracle._utilities.client", "FlextTargetOracle"],
    "FlextTargetOracleBatchService": ["flext_target_oracle._utilities.services", "FlextTargetOracleBatchService"],
    "FlextTargetOracleCliService": ["flext_target_oracle._utilities.cli", "FlextTargetOracleCliService"],
    "FlextTargetOracleConnectionService": ["flext_target_oracle._utilities.services", "FlextTargetOracleConnectionService"],
    "FlextTargetOracleErrorMetadata": ["flext_target_oracle._utilities.errors", "FlextTargetOracleErrorMetadata"],
    "FlextTargetOracleExceptions": ["flext_target_oracle._utilities.errors", "FlextTargetOracleExceptions"],
    "FlextTargetOracleLoader": ["flext_target_oracle._utilities.loader", "FlextTargetOracleLoader"],
    "FlextTargetOracleRecordService": ["flext_target_oracle._utilities.services", "FlextTargetOracleRecordService"],
    "FlextTargetOracleSchemaService": ["flext_target_oracle._utilities.services", "FlextTargetOracleSchemaService"],
    "FlextTargetOracleService": ["flext_target_oracle._utilities.service", "FlextTargetOracleService"],
    "FlextTargetOracleServiceFactory": ["flext_target_oracle._utilities.services", "FlextTargetOracleServiceFactory"],
    "configure_oracle_observability": ["flext_target_oracle._utilities.observability", "configure_oracle_observability"],
    "main": ["flext_target_oracle._utilities.cli", "main"],
}

__all__ = [
    "FlextOracleError",
    "FlextOracleObs",
    "FlextTargetOracle",
    "FlextTargetOracleBatchService",
    "FlextTargetOracleCliService",
    "FlextTargetOracleConnectionService",
    "FlextTargetOracleErrorMetadata",
    "FlextTargetOracleExceptions",
    "FlextTargetOracleLoader",
    "FlextTargetOracleRecordService",
    "FlextTargetOracleSchemaService",
    "FlextTargetOracleService",
    "FlextTargetOracleServiceFactory",
    "configure_oracle_observability",
    "main",
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
