"""Settings tests for flext-target-oracle."""

from __future__ import annotations

from pydantic import SecretStr

from flext_target_oracle import FlextTargetOracleSettings, LoadMethod


class TestOracleSettings:
    """Validate canonical Oracle settings behavior."""

    def test_defaults_and_core_fields(self) -> None:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test_user",
            oracle_password=SecretStr("test_pass"),
        )

        assert config.oracle_port == 1521
        assert config.default_target_schema == "SINGER_DATA"
        assert config.use_bulk_operations is True
        assert config.autocommit is False

    def test_load_method_enum_contract(self) -> None:
        assert LoadMethod.INSERT == "INSERT"
        assert LoadMethod.BULK_INSERT == "BULK_INSERT"
        assert LoadMethod.MERGE == "MERGE"
        assert LoadMethod.BULK_MERGE == "BULK_MERGE"

    def test_get_oracle_config(self) -> None:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            default_target_schema="TEST_SCHEMA",
            autocommit=True,
            transaction_timeout=120,
            parallel_degree=4,
            use_bulk_operations=True,
        )

        oracle_config = config.get_oracle_config()

        assert oracle_config["host"] == "localhost"
        assert oracle_config["port"] == 1521
        assert oracle_config["service_name"] == "XE"
        assert oracle_config["username"] == "test"
        assert oracle_config["password"] == "test"
        assert oracle_config["ssl_enabled"] is False
        assert oracle_config["autocommit"] is True
        assert oracle_config["timeout"] == 120
        assert oracle_config["parallel_degree"] == 4
        assert oracle_config["use_bulk_operations"] is True

    def test_get_table_name_with_prefix_suffix_and_cleanup(self) -> None:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="stg_",
            table_suffix="_tbl",
        )

        assert config.get_table_name("my-stream.v1") == "STG_MY_STREAM_V1_TBL"

    def test_validate_business_rules_failure_for_commit_interval(self) -> None:
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            batch_size=100,
            commit_interval=200,
        )

        result = config.validate_business_rules()
        assert result.is_failure
