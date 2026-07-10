"""Service base for flext-target-oracle tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_target_oracle import m
from tests.settings import TestsFlextTargetOracleSettings


class TestsFlextTargetOracleServiceBase(tests_s):
    """Target Oracle test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextTargetOracleSettings:
        """Return the typed target Oracle+Tests settings singleton."""

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextTargetOracleSettings)


s = TestsFlextTargetOracleServiceBase

__all__: list[str] = ["TestsFlextTargetOracleServiceBase", "s"]
