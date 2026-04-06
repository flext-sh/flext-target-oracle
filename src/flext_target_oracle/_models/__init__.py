# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Models package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_target_oracle._models.commands as _flext_target_oracle__models_commands

    commands = _flext_target_oracle__models_commands
    import flext_target_oracle._models.config as _flext_target_oracle__models_config
    from flext_target_oracle._models.commands import FlextTargetOracleModelsCommands

    config = _flext_target_oracle__models_config
    import flext_target_oracle._models.results as _flext_target_oracle__models_results
    from flext_target_oracle._models.config import FlextTargetOracleModelsConfig

    results = _flext_target_oracle__models_results
    import flext_target_oracle._models.singer as _flext_target_oracle__models_singer
    from flext_target_oracle._models.results import FlextTargetOracleModelsResults

    singer = _flext_target_oracle__models_singer
    from flext_target_oracle._models.singer import FlextTargetOracleModelsSinger
_LAZY_IMPORTS = {
    "FlextTargetOracleModelsCommands": (
        "flext_target_oracle._models.commands",
        "FlextTargetOracleModelsCommands",
    ),
    "FlextTargetOracleModelsConfig": (
        "flext_target_oracle._models.config",
        "FlextTargetOracleModelsConfig",
    ),
    "FlextTargetOracleModelsResults": (
        "flext_target_oracle._models.results",
        "FlextTargetOracleModelsResults",
    ),
    "FlextTargetOracleModelsSinger": (
        "flext_target_oracle._models.singer",
        "FlextTargetOracleModelsSinger",
    ),
    "commands": "flext_target_oracle._models.commands",
    "config": "flext_target_oracle._models.config",
    "results": "flext_target_oracle._models.results",
    "singer": "flext_target_oracle._models.singer",
}

__all__ = [
    "FlextTargetOracleModelsCommands",
    "FlextTargetOracleModelsConfig",
    "FlextTargetOracleModelsResults",
    "FlextTargetOracleModelsSinger",
    "commands",
    "config",
    "results",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
