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
    from flext_target_oracle._models import commands, config, results, singer
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextTargetOracleModelsCommands": "flext_target_oracle._models.commands",
    "FlextTargetOracleModelsConfig": "flext_target_oracle._models.config",
    "FlextTargetOracleModelsResults": "flext_target_oracle._models.results",
    "FlextTargetOracleModelsSinger": "flext_target_oracle._models.singer",
    "commands": "flext_target_oracle._models.commands",
    "config": "flext_target_oracle._models.config",
    "results": "flext_target_oracle._models.results",
    "singer": "flext_target_oracle._models.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
