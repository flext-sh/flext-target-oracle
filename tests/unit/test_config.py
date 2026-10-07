"""Settings tests for flext-target-oracle.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import tm

from flext_target_oracle import FlextTargetOracleSettings
from tests import c
from tests.base import s


class TestsFlextTargetOracleConfig:
    """Validate the public Oracle settings contract (namespaced TargetOracle.*)."""

    # NOTE (multi-agent): mro-rn88 — ADR-005 made settings simple scalars namespaced
    # under
    # TargetOracle.*; the old
    # get_oracle_config/get_table_name/validate_business_rules were
    # dropped as dead code (inlined into consumers), so the contract is the typed
    # scalars.
    @staticmethod
    def test_defaults_and_core_fields() -> None:
        """Test defaults and core fields."""
        config = FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_host": "localhost",
                "oracle_service_name": "XE",
                "oracle_user": "test_user",
                "oracle_password": "p" + "0" * 12,
            },
        })
        target = config.TargetOracle
        tm.that(target.oracle_host, eq="localhost")
        tm.that(target.oracle_port, eq=1521)
        tm.that(target.default_target_schema, eq="SINGER_DATA")
        tm.that(target.use_bulk_operations, eq=True)
        tm.that(target.autocommit, eq=False)

    @staticmethod
    def test_test_service_settings_include_tests_namespace() -> None:
        """Test test service settings include tests namespace."""
        settings = s.fetch_settings()

        # NOTE (multi-agent): mro-rn88 — the composed test settings expose BOTH the
        # shared
        # Tests namespace and the project TargetOracle namespace via the public surface.
        tm.that(settings.Tests.model_dump(), none=False)
        assert settings.TargetOracle.oracle_host

    @staticmethod
    def test_load_method_enum_contract() -> None:
        """Test load method enum contract."""
        tm.that(c.TargetOracle.LOAD_METHOD_INSERT, eq="INSERT")
        tm.that(c.TargetOracle.LOAD_METHOD_BULK_INSERT, eq="BULK_INSERT")
        tm.that(c.TargetOracle.LOAD_METHOD_MERGE, eq="MERGE")
        tm.that(c.TargetOracle.LOAD_METHOD_BULK_MERGE, eq="BULK_MERGE")

    @staticmethod
    def test_connection_scalars_round_trip_through_namespace() -> None:
        """Test connection scalars round trip through namespace."""
        config = FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_host": "localhost",
                "oracle_port": 1521,
                "oracle_service_name": "XE",
                "oracle_user": "test",
                "oracle_password": "test",
                "default_target_schema": "TEST_SCHEMA",
                "autocommit": True,
                "transaction_timeout": 120,
                "parallel_degree": 4,
                "use_bulk_operations": True,
            },
        })
        target = config.TargetOracle
        tm.that(target.oracle_host, eq="localhost")
        tm.that(target.oracle_port, eq=1521)
        tm.that(target.oracle_service_name, eq="XE")
        tm.that(target.oracle_user, eq="test")
        tm.that(target.oracle_password, eq="test")
        tm.that(target.autocommit, eq=True)
        tm.that(target.transaction_timeout, eq=120)
        tm.that(target.parallel_degree, eq=4)
        tm.that(target.use_bulk_operations, eq=True)
        tm.that(target.default_target_schema, eq="TEST_SCHEMA")

    @staticmethod
    def test_table_prefix_and_suffix_scalars_are_preserved() -> None:
        """Test table prefix and suffix scalars are preserved."""
        config = FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_host": "localhost",
                "oracle_service_name": "XE",
                "oracle_user": "test",
                "oracle_password": "test",
                "table_prefix": "stg_",
                "table_suffix": "_tbl",
            },
        })
        target = config.TargetOracle
        tm.that(target.table_prefix, eq="stg_")
        tm.that(target.table_suffix, eq="_tbl")

    @staticmethod
    def test_batch_and_commit_interval_scalars_are_preserved() -> None:
        """Test batch and commit interval scalars are preserved."""
        config = FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_host": "localhost",
                "oracle_service_name": "XE",
                "oracle_user": "test",
                "oracle_password": "test",
                "batch_size": 100,
                "commit_interval": 200,
            },
        })
        target = config.TargetOracle
        tm.that(target.batch_size, eq=100)
        tm.that(target.commit_interval, eq=200)
