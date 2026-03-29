# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal models subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_target_oracle._models.commands import (
        FlextTargetOracleModelsCommands,
        load_target_settings,
    )
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
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
    "load_target_settings": [
        "flext_target_oracle._models.commands",
        "load_target_settings",
    ],
}

__all__ = [
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsConfig",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSinger",
    "load_target_settings",
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
