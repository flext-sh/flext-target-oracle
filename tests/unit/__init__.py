# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle.tests.unit.test_config import (
        TestsFlextTargetOracleConfig as TestsFlextTargetOracleConfig,
    )
    from flext_target_oracle.tests.unit.test_loader import (
        TestsFlextTargetOracleLoader as TestsFlextTargetOracleLoader,
    )
    from flext_target_oracle.tests.unit.test_module_governance import (
        TestsFlextTargetOracleModuleGovernance as TestsFlextTargetOracleModuleGovernance,
    )
    from flext_target_oracle.tests.unit.test_target import (
        TestsFlextTargetOracleTarget as TestsFlextTargetOracleTarget,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_config": ("TestsFlextTargetOracleConfig",),
        ".test_loader": ("TestsFlextTargetOracleLoader",),
        ".test_module_governance": ("TestsFlextTargetOracleModuleGovernance",),
        ".test_target": ("TestsFlextTargetOracleTarget",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
