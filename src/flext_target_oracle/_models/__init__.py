# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal models subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._models import (
        commands as commands,
        config as config,
        results as results,
        singer as singer,
    )
    from flext_target_oracle._models.commands import (
        FlextTargetOracleModelsCommands as FlextTargetOracleModelsCommands,
        load_target_settings as load_target_settings,
    )
    from flext_target_oracle._models.config import (
        FlextTargetOracleModelsConfig as FlextTargetOracleModelsConfig,
    )
    from flext_target_oracle._models.results import (
        FlextTargetOracleModelsResults as FlextTargetOracleModelsResults,
    )
    from flext_target_oracle._models.singer import (
        FlextTargetOracleModelsSinger as FlextTargetOracleModelsSinger,
    )

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
    "commands": ["flext_target_oracle._models.commands", ""],
    "config": ["flext_target_oracle._models.config", ""],
    "load_target_settings": [
        "flext_target_oracle._models.commands",
        "load_target_settings",
    ],
    "results": ["flext_target_oracle._models.results", ""],
    "singer": ["flext_target_oracle._models.singer", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsConfig",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSinger",
    "commands",
    "config",
    "load_target_settings",
    "results",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
