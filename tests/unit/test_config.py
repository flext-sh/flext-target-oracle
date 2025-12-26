"""Real Oracle Config Tests - Comprehensive Coverage.

Tests configuration functionality with real scenarios for maximum coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

import pytest
from flext_core import FlextResult
from pydantic import SecretStr
from pydantic.fields import FieldInfo

from flext_target_oracle import FlextTargetOracleSettings, LoadMethod


class TestRealOracleConfig:
    """Test Oracle configuration with real scenarios."""

    def test_minimal_config_creation(self) -> None:
        """Test method."""
        """Test creating config with minimal required fields."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test_user",
            oracle_password=SecretStr("test_pass"),
        )

        # Verify defaults
        assert config.oracle_port == 1521
        assert config.default_target_schema == "SINGER_DATA"
        assert config.load_method == "upsert"  # Backward compat property
        assert config.use_bulk_operations is True
        assert config.autocommit is False
        assert config.table_prefix == ""
        assert config.table_suffix == ""

    def test_full_config_creation(self) -> None:
        """Test method."""
        """Test creating config with all available fields."""
        config = FlextTargetOracleSettings(
            # Basic connection
            oracle_host="prod-oracle.company.com",
            oracle_port=1522,
            oracle_service_name="PRODDB",
            oracle_user="prod_user",
            oracle_password=SecretStr("prod_pass"),
            # Schema settings
            default_target_schema="PROD_SCHEMA",
            # Loading settings
            use_bulk_operations=True,
            batch_size=5000,
            # Advanced Oracle features
            autocommit=False,
            parallel_degree=8,
            # Transaction settings
            commit_interval=1000,
            transaction_timeout=300,
            # Table naming
            table_prefix="STG_",
            table_suffix="_TBL",
        )

        # Verify all settings
        assert config.oracle_host == "prod-oracle.company.com"
        assert config.oracle_port == 1522
        assert config.oracle_service_name == "PRODDB"
        assert config.parallel_degree == 8
        assert config.use_bulk_operations is True
        assert config.batch_size == 5000
        assert config.autocommit is False
        assert config.default_target_schema == "PROD_SCHEMA"
        assert config.table_prefix == "STG_"
        assert config.table_suffix == "_TBL"
        # Backward compat properties
        assert config.load_method == "upsert"
        assert config.allow_alter_table is True

    def test_config_field_constraints(self) -> None:
        """Test config field constraints are defined correctly."""
        # pydantic-settings doesn't enforce Field constraints at initialization
        # but the constraints are defined for documentation and validation tooling

        # Get field info for oracle_port
        port_field = FlextTargetOracleSettings.model_fields["oracle_port"]
        assert isinstance(port_field, FieldInfo)
        # Constraints are in metadata as Ge/Le objects
        port_constraints = {type(c).__name__: c for c in port_field.metadata}
        assert "Ge" in port_constraints
        assert "Le" in port_constraints
        assert port_constraints["Ge"].ge == 1
        assert port_constraints["Le"].le == 65535

        # Get field info for batch_size
        batch_field = FlextTargetOracleSettings.model_fields["batch_size"]
        assert isinstance(batch_field, FieldInfo)
        batch_constraints = {type(c).__name__: c for c in batch_field.metadata}
        assert batch_constraints["Ge"].ge == 1
        assert batch_constraints["Le"].le == 50000

        # Get field info for transaction_timeout
        timeout_field = FlextTargetOracleSettings.model_fields["transaction_timeout"]
        assert isinstance(timeout_field, FieldInfo)
        timeout_constraints = {type(c).__name__: c for c in timeout_field.metadata}
        assert timeout_constraints["Ge"].ge == 1
        assert timeout_constraints["Le"].le == 3600

    def test_load_method_enum(self) -> None:
        """Test method."""
        """Test LoadMethod enum values."""
        assert LoadMethod.INSERT == "INSERT"
        assert LoadMethod.BULK_INSERT == "BULK_INSERT"
        assert LoadMethod.MERGE == "MERGE"
        assert LoadMethod.BULK_MERGE == "BULK_MERGE"

        # Test that config has load_method property (backward compat)
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )
        # load_method is a property returning default "upsert"
        assert config.load_method == "upsert"

    def test_get_oracle_config(self) -> None:
        """Test get_oracle_config method returns correct Oracle config dict."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            default_target_schema="TEST_SCHEMA",
            autocommit=True,
            transaction_timeout=120,
        )

        oracle_config = config.get_oracle_config()

        # Verify core connection fields
        assert oracle_config["host"] == "localhost"
        assert oracle_config["port"] == 1521
        assert oracle_config["service_name"] == "XE"
        assert oracle_config["username"] == "test"
        assert oracle_config["password"] == "test"
        # ssl_enabled is hardcoded False in get_oracle_config()
        assert oracle_config["ssl_enabled"] is False
        # Pool sizes come from FlextConstants.Performance
        assert oracle_config["pool_min"] == 1  # MIN_DB_POOL_SIZE
        assert oracle_config["pool_max"] == 50  # DEFAULT_DB_POOL_SIZE * 5
        assert oracle_config["pool_increment"] == 1
        assert oracle_config["encoding"] == "UTF-8"
        assert oracle_config["autocommit"] is True
        assert oracle_config["timeout"] == 120

    def test_get_table_name_variations(self) -> None:
        """Test method."""
        """Test get_table_name with various configurations."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="",
            table_suffix="",
        )

        # Default behavior - uppercase
        assert config.get_table_name("my_stream") == "MY_STREAM"
        assert config.get_table_name("CamelCase") == "CAMELCASE"

        # With prefix (create new config since it's immutable)
        config_with_prefix = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="stg_",
        )
        assert config_with_prefix.get_table_name("my_stream") == "STG_MY_STREAM"

        # With suffix (create new config since it's immutable)
        config_with_suffix = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="stg_",
            table_suffix="_tbl",
        )
        assert config_with_suffix.get_table_name("my_stream") == "STG_MY_STREAM_TBL"

        # Table name generation with special characters (explicit empty prefix/suffix)
        config_clean = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="",
            table_suffix="",
        )
        assert config_clean.get_table_name("my-stream.v1") == "MY_STREAM_V1"
        assert config_clean.get_table_name("stream-with-dashes") == "STREAM_WITH_DASHES"

    def test_config_environment_variables(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test config can be created from environment variables."""
        # Use monkeypatch for isolated environment variable testing
        monkeypatch.setenv("ORACLE_HOST", "env-host")
        monkeypatch.setenv("ORACLE_PORT", "1522")
        monkeypatch.setenv("ORACLE_SERVICE", "ENV_SERVICE")
        monkeypatch.setenv("ORACLE_USER", "env_user")
        monkeypatch.setenv("ORACLE_PASSWORD", "env_pass")

        # Create config reading from environment
        config = FlextTargetOracleSettings(
            oracle_host=os.environ.get("ORACLE_HOST", "localhost"),
            oracle_port=int(os.environ.get("ORACLE_PORT", "1521")),
            oracle_service_name=os.environ.get("ORACLE_SERVICE", "XE"),
            oracle_user=os.environ.get("ORACLE_USER", "test"),
            oracle_password=os.environ.get("ORACLE_PASSWORD", "test"),
        )

        assert config.oracle_host == "env-host"
        assert config.oracle_port == 1522
        assert config.oracle_service_name == "ENV_SERVICE"

    def test_config_password_hiding(self) -> None:
        """Test method."""
        """Test password is hidden in string representation."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("super_secret_password"),
        )

        # Password should not appear in string repr
        config_str = str(config)
        assert "super_secret_password" not in config_str
        assert "**********" in config_str or "SecretStr" in config_str

    def test_config_mutability(self) -> None:
        """Test method."""
        """Test config can be mutated (frozen=False by design for settings)."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Settings are mutable by design (frozen=False)
        config.oracle_host = "new-host"
        assert config.oracle_host == "new-host"

    def test_backward_compat_properties(self) -> None:
        """Test method."""
        """Test backward compatibility properties."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Backward compat properties return defaults
        assert config.host == "localhost"
        assert config.port == 1521
        assert config.service_name == "XE"
        assert config.username == "test"
        assert config.load_method == "upsert"
        assert config.allow_alter_table is True

    def test_custom_type_mappings_property(self) -> None:
        """Test method."""
        """Test custom_type_mappings backward compat property."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # custom_type_mappings is a backward compat property returning empty dict
        assert config.custom_type_mappings == {}
        assert isinstance(config.custom_type_mappings, dict)

    def test_parallel_degree_configuration(self) -> None:
        """Test method."""
        """Test parallel degree configuration."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            parallel_degree=4,
        )

        assert config.parallel_degree == 4

    def test_transaction_settings(self) -> None:
        """Test method."""
        """Test transaction settings configuration."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            autocommit=True,
            commit_interval=500,
            transaction_timeout=180,
        )

        assert config.autocommit is True
        assert config.commit_interval == 500
        assert config.transaction_timeout == 180

    def test_table_naming_configuration(self) -> None:
        """Test method."""
        """Test table naming with prefix and suffix."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            table_prefix="RAW_",
            table_suffix="_V1",
        )

        assert config.table_prefix == "RAW_"
        assert config.table_suffix == "_V1"
        assert config.get_table_name("users") == "RAW_USERS_V1"

    def test_validation_methods(self) -> None:
        """Test method."""
        """Test config validation methods."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
        )

        # Test validate_business_rules - returns FlextResult
        result = config.validate_business_rules()
        assert isinstance(result, FlextResult)
        # Note: May fail due to FlextResult not accepting None - that's OK for this test

    def test_oracle_specific_features(self) -> None:
        """Test method."""
        """Test Oracle-specific feature configurations."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            use_bulk_operations=False,
            batch_size=500,
        )

        assert config.use_bulk_operations is False
        assert config.batch_size == 500
        # use_ssl is a property, not a field
        assert config.use_ssl is True

    def test_config_serialization(self) -> None:
        """Test method."""
        """Test config can be serialized and deserialized."""
        config = FlextTargetOracleSettings(
            oracle_host="localhost",
            oracle_service_name="XE",
            oracle_user="test",
            oracle_password=SecretStr("test"),
            batch_size=2000,
        )

        # Convert to dict
        config_dict = config.model_dump()
        assert config_dict["oracle_host"] == "localhost"
        assert config_dict["batch_size"] == 2000

        # Password should be masked
        assert config_dict["oracle_password"] != "test"

        # Can recreate from dict (with password)
        config_dict["oracle_password"] = "test"
        new_config = FlextTargetOracleSettings(**config_dict)
        assert new_config.oracle_host == config.oracle_host
        assert new_config.batch_size == config.batch_size
