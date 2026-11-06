"""Service base for flext-target-oracle tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/base
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_tests import FlextTestsServiceBase, TestsFlextTargetOracleSettings

from tests import m, p


class TestsFlextTargetOracleServiceBase(FlextTestsServiceBase):
    """Target Oracle test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextTargetOracleSettings:
        """Return the typed target Oracle+Tests settings singleton."""
        # NOTE (multi-agent): mro-rn88 — settings-fallout left this body empty (returned
        # None); return the composed Tests+TargetOracle singleton the base must deliver.
        return TestsFlextTargetOracleSettings.fetch_global()

    @classmethod
    @override
    def runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTargetOracleSettings)


s = TestsFlextTargetOracleServiceBase

__all__: list[str] = ["TestsFlextTargetOracleServiceBase", "s"]
