"""Governance checks for target-oracle module structure.

Uses ``importlib`` + ``inspect`` to walk the live module objects rather
than parsing Python source via ``ast`` — keeping the test free of
``import ast`` and aligned with the workspace ``regex/ast-from-constants``
directive.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_module_governance
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests import m, tm, u


class TestsFlextTargetOracleModuleGovernance(u.FlextTestsModuleGovernanceMixin):
    """Behavior contract for test_module_governance."""

    _test_file = __file__

    @staticmethod
    def test_target_oracle_namespace_does_not_wrap_meltano_singer_models() -> None:
        """Test target oracle namespace does not wrap meltano singer models."""
        tm.that(hasattr(m.TargetOracle, "SingerStreamModel"), eq=True)
        tm.that(hasattr(m.TargetOracle, "Meltano"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerSchemaMessage"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerRecordMessage"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerStateMessage"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerActivateVersionMessage"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerCatalogMetadata"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerCatalogEntry"), eq=False)
        tm.that(hasattr(m.TargetOracle, "SingerCatalog"), eq=False)
