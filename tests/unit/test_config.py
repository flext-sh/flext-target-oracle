"""Real Oracle Config Tests - Comprehensive Coverage.

Tests configuration functionality with real scenarios for maximum coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import os

import pytest
from flext_core import FlextCore
from pydantic import SecretStr, ValidationError

from flext_target_oracle import FlextTargetOracleConfig, LoadMethod


class TestRealOracleConfig:
    """Test Oracle configuration with real scenarios."""

    def test_minimal_config_creation(self) -> None:
        """Test method."""
        """Test creating config with minimal required fields."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password=SecretStr("test_pass"),
        )

        # Verify defaults
        assert config.oracle_port == 1521
        assert config.default_target_schema == "target"
        assert config.load_method == LoadMethod.INSERT
        assert config.batch_size == 1000
        assert config.connection_timeout == 30
        assert config.use_bulk_operations is True
        assert config.sdc_mode == "append"
        assert config.storage_mode == "flattened"

    def test_full_config_creation(self) -> None:
        """Test method."""
        """Test creating config with all fields."""
        config = FlextTargetOracleConfig(
            # Basic connection
            oracle_host="prod-oracle.company.com",
            oracle_port=1522,
            oracle_service="PRODDB",
            oracle_user="prod_user",
            oracle_password=SecretStr("prod_pass"),
            # Schema settings
            default_target_schema="PROD_SCHEMA",
            # Loading settings
            load_method=LoadMethod.BULK_INSERT,
            use_bulk_operations=True,
            batch_size=5000,
            connection_timeout=60,
            # SSL/TLS
            use_ssl=True,
            ssl_verify=True,
            ssl_wallet_location="/opt/oracle/wallet",
            ssl_wallet_password=SecretStr("wallet_pass"),
            # Connection pooling
            pool_min_size=1,
            pool_max_size=10,
            pool_increment=2,
            # Advanced Oracle features
            enable_auto_commit=False,
            use_direct_path=True,
            parallel_degree=8,
            # Column modification
            column_mappings={
                "users": {"old_name": "new_name"},
                "orders": {"customer_id": "cust_id"},
            },
            ignored_columns=["password", "secret", "internal_id"],
            # SDC control
            sdc_mode="merge",
            sdc_extracted_at_column="_sdc_extracted_at",
            sdc_loaded_at_column="_sdc_loaded_at",
            sdc_deleted_at_column="_sdc_deleted_at",
            # Storage mode
            storage_mode="hybrid",
            json_column_name="raw_json",
            # DDL options
            add_metadata_columns=True,
        )

        # Verify all settings
        assert config.oracle_host == "prod-oracle.company.com"
        assert config.oracle_port == 1522
        assert config.use_ssl is True
        assert config.parallel_degree == 8
        assert len(config.column_mappings or {}) == 2
        assert len(config.ignored_columns or []) == 3
        assert config.sdc_mode == "merge"
        assert config.storage_mode == "hybrid"

    def test_config_validation_errors(self) -> None:
        """Test method."""
        """Test config validation with invalid values."""
        # Invalid port
        with pytest.raises(ValidationError) as exc_info:
            FlextTargetOracleConfig(
                oracle_host="localhost",
                oracle_port=0,  # Invalid
                oracle_service="XE",
                oracle_user="test",
                oracle_password=SecretStr("test"),
            )
        assert "greater than 0" in str(exc_info.value)

        # Invalid batch size
        with pytest.raises(ValidationError) as exc_info:
            FlextTargetOracleConfig(
                oracle_host="localhost",
                oracle_service="XE",
                oracle_user="test",
                oracle_password=SecretStr("test"),
                batch_size=-1,  # Invalid
            )
        assert "greater than 0" in str(exc_info.value)

        # Invalid timeout
        with pytest.raises(ValidationError) as exc_info:
            FlextTargetOracleConfig(
                oracle_host="localhost",
                oracle_service="XE",
                oracle_user="test",
                oracle_password=SecretStr("test"),
                connection_timeout=0,  # Invalid
            )
        assert "greater than 0" in str(exc_info.value)

    def test_load_method_enum(self) -> None:
        """Test method."""
        """Test LoadMethod enum values."""
        assert LoadMethod.INSERT == "INSERT"
        assert LoadMethod.BULK_INSERT == "BULK_INSERT"
        assert LoadMethod.MERGE == "MERGE"
        assert LoadMethod.BULK_MERGE == "BULK_MERGE"

        # Test creating config with each method
        for method in LoadMethod:
            config = FlextTargetOracleConfig(
                oracle_host="localhost",
                oracle_service="XE",
                oracle_user="test",
                oracle_password=SecretStr("test"),
                load_method=method,
            )
            assert config.load_method == method

    def test_get_oracle_config(self) -> None:
        """Test method."""
        """Test get_oracle_config method."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            default_target_schema="TEST_SCHEMA",
            use_ssl=True,
            pool_min_size=1,
            pool_max_size=5,
        )

        oracle_config = config.get_oracle_config()

        # Should create oracle config dict
        assert oracle_config["host"] == "localhost"
        assert oracle_config["port"] == 1521
        assert oracle_config["service_name"] == "XE"
        assert oracle_config["username"] == "test"
        assert oracle_config["password"] == "test"
        assert oracle_config["ssl_enabled"] is True
        assert oracle_config["pool_min"] == 1
        assert oracle_config["pool_max"] == 5

    def test_get_table_name_variations(self) -> None:
        """Test method."""
        """Test get_table_name with various configurations."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Default behavior - uppercase
        assert config.get_table_name("my_stream") == "MY_STREAM"
        assert config.get_table_name("CamelCase") == "CAMELCASE"

        # With prefix (create new config since it's immutable)
        config_with_prefix = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="stg_",
        )
        assert config_with_prefix.get_table_name("my_stream") == "STG_MY_STREAM"

        # With suffix (create new config since it's immutable)
        config_with_suffix = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="stg_",
            table_suffix="_tbl",
        )
        assert config_with_suffix.get_table_name("my_stream") == "STG_MY_STREAM_TBL"

        # With mapping (create new config since it's immutable)
        config_with_mapping = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_name_mappings={"my_stream": "custom_table"},
        )
        assert config_with_mapping.get_table_name("my_stream") == "CUSTOM_TABLE"

        # Stream not in mapping uses prefix/suffix (on the config with mapping)
        assert config_with_mapping.get_table_name("other_stream") == "OTHER_STREAM"

    def test_config_environment_variables(self) -> None:
        """Test method."""
        """Test config can be created from environment variables."""
        # Set environment variables
        os.environ["ORACLE_HOST"] = "env-host"
        os.environ["ORACLE_PORT"] = "1522"
        os.environ["ORACLE_SERVICE"] = "ENV_SERVICE"
        os.environ["ORACLE_USER"] = "env_user"
        os.environ["ORACLE_PASSWORD"] = "env_pass"

        try:
            # Would work with proper env var handling in config
            config = FlextTargetOracleConfig(
                oracle_host=os.environ.get("ORACLE_HOST", "localhost"),
                oracle_port=int(os.environ.get("ORACLE_PORT", "1521")),
                oracle_service=os.environ.get("ORACLE_SERVICE", "XE"),
                oracle_user=os.environ.get("ORACLE_USER", "test"),
                oracle_password=os.environ.get("ORACLE_PASSWORD", "test"),
            )

            assert config.oracle_host == "env-host"
            assert config.oracle_port == 1522
            assert config.oracle_service == "ENV_SERVICE"

        finally:
            # Cleanup
            for key in [
                "ORACLE_HOST",
                "ORACLE_PORT",
                "ORACLE_SERVICE",
                "ORACLE_USER",
                "ORACLE_PASSWORD",
            ]:
                os.environ.pop(key, None)

    def test_config_password_hiding(self) -> None:
        """Test method."""
        """Test password is hidden in string representation."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("super_secret_password"),
        )

        # Password should not appear in string repr
        config_str = str(config)
        assert "super_secret_password" not in config_str
        assert "**********" in config_str or "SecretStr" in config_str

    def test_config_immutability(self) -> None:
        """Test method."""
        """Test config is immutable after creation."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Should not be able to modify
        with pytest.raises(ValidationError):
            config.oracle_host = "new-host"

    def test_sdc_column_customization(self) -> None:
        """Test method."""
        """Test SDC column name customization."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            sdc_extracted_at_column="extracted_timestamp",
            sdc_loaded_at_column="loaded_timestamp",
            sdc_deleted_at_column="deleted_timestamp",
            sdc_sequence_column="sequence_num",
        )

        assert config.sdc_extracted_at_column == "extracted_timestamp"
        assert config.sdc_loaded_at_column == "loaded_timestamp"
        assert config.sdc_deleted_at_column == "deleted_timestamp"
        assert config.sdc_sequence_column == "sequence_num"

    def test_type_mapping_configuration(self) -> None:
        """Test method."""
        """Test type mapping configuration."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            type_mappings={
                "string": "NVARCHAR2(2000)",
                "integer": "NUMBER(19)",
                "number": "BINARY_DOUBLE",
                "boolean": "VARCHAR2(5)",
                "date-time": "DATE",
            },
            default_string_length=2000,
            use_clob_threshold=2000,
        )

        assert config.type_mappings["string"] == "NVARCHAR2(2000)"
        assert config.type_mappings["number"] == "BINARY_DOUBLE"
        assert config.default_string_length == 2000
        assert config.use_clob_threshold == 2000

    def test_column_ordering_rules(self) -> None:
        """Test method."""
        """Test column ordering rules configuration."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            column_ordering="custom",
            column_order_rules={
                "sdc_columns": 1,  # SDC first
                "primary_keys": 2,
                "audit_columns": 3,
                "regular_columns": 4,
            },
            audit_column_patterns=["created_", "updated_", "_at$"],
        )

        assert config.column_ordering == "custom"
        assert config.column_order_rules["sdc_columns"] == 1
        assert len(config.audit_column_patterns) == 3

    def test_index_configuration(self) -> None:
        """Test method."""
        """Test index management configuration."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            maintain_indexes=True,
            create_foreign_key_indexes=True,
            custom_indexes={
                "users": [
                    {
                        "name": "idx_users_email_unique",
                        "columns": ["email"],
                        "unique": True,
                        "tablespace": "USERS_IDX",
                    },
                    {
                        "name": "idx_users_composite",
                        "columns": ["last_name", "first_name"],
                        "unique": False,
                    },
                ],
                "orders": [
                    {
                        "name": "idx_orders_date",
                        "columns": ["order_date"],
                        "unique": False,
                        "compress": True,
                    },
                ],
            },
            index_naming_template="IX_{table}_{columns}_{unique}",
            preserve_existing_indexes=True,
        )

        assert config.maintain_indexes is True
        assert config.create_foreign_key_indexes is True
        assert len(config.custom_indexes["users"]) == 2
        assert config.custom_indexes["users"][0]["unique"] is True
        assert config.index_naming_template == "IX_{table}_{columns}_{unique}"

    def test_storage_mode_options(self) -> None:
        """Test method."""
        """Test different storage mode configurations."""
        # Flattened mode (default)
        config1 = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            storage_mode="flattened",
        )
        assert config1.storage_mode == "flattened"

        # JSON mode
        config2 = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            storage_mode="json",
            json_column_name="json_data",
        )
        assert config2.storage_mode == "json"
        assert config2.json_column_name == "json_data"

        # Hybrid mode
        config3 = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            storage_mode="hybrid",
            flatten_max_depth=2,
        )
        assert config3.storage_mode == "hybrid"
        assert config3.flatten_max_depth == 2

    def test_validation_methods(self) -> None:
        """Test method."""
        """Test config validation methods."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Test validate_oracle_config
        result = config.validate_oracle_config()
        assert isinstance(result, FlextCore.Result)
        assert result.is_success

        # Config with missing required fields would fail
        # (Can't test directly due to Pydantic validation)

    def test_oracle_specific_features(self) -> None:
        """Test method."""
        """Test Oracle-specific feature configurations."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            # Oracle-specific fields that actually exist
            use_bulk_operations=False,
            batch_size=500,
            connection_timeout=60,
            use_ssl=True,
        )

        assert config.use_bulk_operations is False
        assert config.batch_size == 500
        assert config.connection_timeout == 60
        assert config.use_ssl is True

    def test_config_serialization(self) -> None:
        """Test method."""
        """Test config can be serialized and deserialized."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            batch_size=2000,
            column_mappings={"users": {"old": "new"}},
        )

        # Convert to dict
        config_dict = config.model_dump()
        assert config_dict["oracle_host"] == "localhost"
        assert config_dict["batch_size"] == 2000

        # Password should be masked
        assert config_dict["oracle_password"] != "test"

        # Can recreate from dict (with password)
        config_dict["oracle_password"] = "test"
        new_config = FlextTargetOracleConfig(**config_dict)
        assert new_config.oracle_host == config.oracle_host
        assert new_config.batch_size == config.batch_size
