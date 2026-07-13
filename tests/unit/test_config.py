"""Settings tests for flext-target-oracle."""

from __future__ import annotations

from flext_target_oracle import FlextTargetOracleSettings
from tests import c
from tests.base import s


class TestsFlextTargetOracleConfig:
    """Validate the public Oracle settings contract (namespaced TargetOracle.*)."""

    # NOTE (multi-agent): mro-rn88 — ADR-005 made settings simple scalars namespaced under
    # TargetOracle.*; the old get_oracle_config/get_table_name/validate_business_rules were
    # dropped as dead code (inlined into consumers), so the contract is the typed scalars.
    def test_defaults_and_core_fields(self) -> None:
        config = FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_host": "localhost",
                "oracle_service_name": "XE",
                "oracle_user": "test_user",
                "oracle_password": "test_pass",
            },
        })
        target = config.TargetOracle
        assert target.oracle_host == "localhost"
        assert target.oracle_port == 1521
        assert target.default_target_schema == "SINGER_DATA"
        assert target.use_bulk_operations is True
        assert target.autocommit is False

    def test_test_service_settings_include_tests_namespace(self) -> None:
        settings = s.fetch_settings()

        # NOTE (multi-agent): mro-rn88 — the composed test settings expose BOTH the shared
        # Tests namespace and the project TargetOracle namespace via the public surface.
        assert settings.Tests.model_dump() is not None
        assert settings.TargetOracle.oracle_host

    def test_load_method_enum_contract(self) -> None:
        assert c.TargetOracle.LOAD_METHOD_INSERT == "INSERT"
        assert c.TargetOracle.LOAD_METHOD_BULK_INSERT == "BULK_INSERT"
        assert c.TargetOracle.LOAD_METHOD_MERGE == "MERGE"
        assert c.TargetOracle.LOAD_METHOD_BULK_MERGE == "BULK_MERGE"

    def test_connection_scalars_round_trip_through_namespace(self) -> None:
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
        assert target.oracle_host == "localhost"
        assert target.oracle_port == 1521
        assert target.oracle_service_name == "XE"
        assert target.oracle_user == "test"
        assert target.oracle_password == "test"
        assert target.autocommit is True
        assert target.transaction_timeout == 120
        assert target.parallel_degree == 4
        assert target.use_bulk_operations is True
        assert target.default_target_schema == "TEST_SCHEMA"

    def test_table_prefix_and_suffix_scalars_are_preserved(self) -> None:
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
        assert target.table_prefix == "stg_"
        assert target.table_suffix == "_tbl"

    def test_batch_and_commit_interval_scalars_are_preserved(self) -> None:
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
        assert target.batch_size == 100
        assert target.commit_interval == 200
