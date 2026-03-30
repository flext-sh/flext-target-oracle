# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal models subpackage for flext-target-oracle."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle._models import commands, config, results, singer
    from flext_target_oracle._models.commands import *
    from flext_target_oracle._models.config import *
    from flext_target_oracle._models.results import *
    from flext_target_oracle._models.singer import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTargetOracleModelsCommands": "flext_target_oracle._models.commands",
    "FlextTargetOracleModelsConfig": "flext_target_oracle._models.config",
    "FlextTargetOracleModelsResults": "flext_target_oracle._models.results",
    "FlextTargetOracleModelsSinger": "flext_target_oracle._models.singer",
    "commands": "flext_target_oracle._models.commands",
    "config": "flext_target_oracle._models.config",
    "load_target_settings": "flext_target_oracle._models.commands",
    "results": "flext_target_oracle._models.results",
    "singer": "flext_target_oracle._models.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
