# AUTO-GENERATED FILE — Regenerate with: make gen
"""E2e package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_target_oracle.tests.e2e.test_singer import (
        TestsFlextTargetOracleSinger as TestsFlextTargetOracleSinger,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_singer": ("TestsFlextTargetOracleSinger",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
