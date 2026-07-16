"""Service base for flext-target-oracle tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_target_oracle import m, p
from tests.settings import TestsFlextTargetOracleSettings


class TestsFlextTargetOracleServiceBase(tests_s):
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
    def _runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTargetOracleSettings)


s = TestsFlextTargetOracleServiceBase

__all__: list[str] = ["TestsFlextTargetOracleServiceBase", "s"]
