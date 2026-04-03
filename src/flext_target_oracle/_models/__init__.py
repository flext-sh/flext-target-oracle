# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_target_oracle import commands, config, results, singer
    from flext_target_oracle.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle.config import FlextTargetOracleModelsConfig
    from flext_target_oracle.results import FlextTargetOracleModelsResults
    from flext_target_oracle.singer import FlextTargetOracleModelsSinger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetOracleModelsCommands": "flext_target_oracle.commands",
    "FlextTargetOracleModelsConfig": "flext_target_oracle.config",
    "FlextTargetOracleModelsResults": "flext_target_oracle.results",
    "FlextTargetOracleModelsSinger": "flext_target_oracle.singer",
    "commands": "flext_target_oracle.commands",
    "config": "flext_target_oracle.config",
    "results": "flext_target_oracle.results",
    "singer": "flext_target_oracle.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
