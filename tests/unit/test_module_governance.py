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

from flext_tests import u

from tests import m


class TestsFlextTargetOracleModuleGovernance(u.FlextTestsModuleGovernanceMixin):
    """Behavior contract for test_module_governance."""

    _test_file = __file__

    @staticmethod
    def test_target_oracle_namespace_does_not_wrap_meltano_singer_models() -> None:
        """Test target oracle namespace does not wrap meltano singer models."""
        assert hasattr(m.TargetOracle, "SingerStreamModel")
        assert not hasattr(m.TargetOracle, "Meltano")
        assert not hasattr(m.TargetOracle, "SingerSchemaMessage")
        assert not hasattr(m.TargetOracle, "SingerRecordMessage")
        assert not hasattr(m.TargetOracle, "SingerStateMessage")
        assert not hasattr(m.TargetOracle, "SingerActivateVersionMessage")
        assert not hasattr(m.TargetOracle, "SingerCatalogMetadata")
        assert not hasattr(m.TargetOracle, "SingerCatalogEntry")
        assert not hasattr(m.TargetOracle, "SingerCatalog")
