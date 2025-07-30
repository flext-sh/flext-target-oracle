"""Tests for FlextOracleTargetConfig."""

import pytest
from flext_core import FlextResult
from pydantic import ValidationError

from flext_target_oracle.config import FlextOracleTargetConfig, LoadMethod

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3


class TestFlextOracleTargetConfig:
    """Test FlextOracleTargetConfig."""

    def test_basic_config_creation(self) -> None:
        """Test basic configuration creation."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
        )

        if config.oracle_host != "localhost":
            raise AssertionError(f"Expected {'localhost'}, got {config.oracle_host}")
        assert config.oracle_port == 1521
        if config.oracle_service != "XE":
            raise AssertionError(f"Expected {'XE'}, got {config.oracle_service}")
        assert config.oracle_user == "test_user"
        if config.oracle_password != "test_pass":
            raise AssertionError(
                f"Expected {'test_pass'}, got {config.oracle_password}"
            )
        assert config.default_target_schema == "TEST_SCHEMA"

    def test_default_values(self) -> None:
        """Test default values."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        if config.oracle_port != 1521:
            raise AssertionError(f"Expected {1521}, got {config.oracle_port}")
        if config.default_target_schema != "target":
            raise AssertionError(
                f"Expected {'target'}, got {config.default_target_schema}"
            )
        assert config.batch_size == 1000
        assert config.load_method == LoadMethod.INSERT
        if not config.use_bulk_operations:
            raise AssertionError(f"Expected True, got {config.use_bulk_operations}")
        assert config.connection_timeout == 30

    def test_custom_values(self) -> None:
        """Test custom values."""
        config = FlextOracleTargetConfig(
            oracle_host="oracle.example.com",
            oracle_port=1522,
            oracle_service="PROD",
            oracle_user="admin",
            oracle_password="secret",
            default_target_schema="DATA_WAREHOUSE",
            batch_size=5000,
            load_method=LoadMethod.MERGE,
            use_bulk_operations=False,
            connection_timeout=60,
        )

        if config.oracle_host != "oracle.example.com":
            raise AssertionError(
                f"Expected {'oracle.example.com'}, got {config.oracle_host}"
            )
        assert config.oracle_port == 1522
        if config.oracle_service != "PROD":
            raise AssertionError(f"Expected {'PROD'}, got {config.oracle_service}")
        assert config.oracle_user == "admin"
        if config.oracle_password != "secret":
            raise AssertionError(f"Expected {'secret'}, got {config.oracle_password}")
        if config.default_target_schema != "DATA_WAREHOUSE":
            raise AssertionError(
                f"Expected {'DATA_WAREHOUSE'}, got {config.default_target_schema}"
            )
        if config.batch_size != 5000:
            raise AssertionError(f"Expected {5000}, got {config.batch_size}")
        if config.load_method != LoadMethod.MERGE:
            raise AssertionError(
                f"Expected {LoadMethod.MERGE}, got {config.load_method}"
            )
        if config.use_bulk_operations:
            raise AssertionError(f"Expected False, got {config.use_bulk_operations}")
        assert config.connection_timeout == 60

    def test_validate_oracle_config_success(self) -> None:
        """Test successful Oracle configuration validation."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        result = config.validate_domain_rules()
        assert result.is_success

    def test_validate_oracle_config_missing_host(self) -> None:
        """Test Oracle configuration validation with missing host."""
        config = FlextOracleTargetConfig(
            oracle_host="",  # Empty host
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        result = config.validate_domain_rules()
        assert not result.is_success
        if result.error and "Oracle host is required" not in result.error:
            raise AssertionError(
                f"Expected 'Oracle host is required' in {result.error}"
            )

    def test_validate_oracle_config_invalid_port(self) -> None:
        """Test Oracle configuration validation with invalid port."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=0,  # Invalid port
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        result = config.validate_domain_rules()
        assert not result.is_success
        if result.error and "port must be between 1 and 65535" not in result.error:
            raise AssertionError(
                f"Expected 'port must be between 1 and 65535' in {result.error}"
            )

    def test_validate_oracle_config_missing_username(self) -> None:
        """Test Oracle configuration validation with missing username."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="",  # Empty username
            oracle_password="test",
        )

        result = config.validate_domain_rules()
        assert not result.is_success
        if result.error and "Oracle username is required" not in result.error:
            expected_msg = "Oracle username is required"
            raise AssertionError(f"Expected '{expected_msg}' in {result.error}")

    def test_validate_oracle_config_missing_password(self) -> None:
        """Test Oracle configuration validation with missing password."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test",
            oracle_password="",  # Empty password
        )

        result = config.validate_domain_rules()
        assert not result.is_success
        if result.error and "Oracle password is required" not in result.error:
            expected_msg = "Oracle password is required"
            raise AssertionError(f"Expected '{expected_msg}' in {result.error}")

    def test_validate_oracle_config_missing_service(self) -> None:
        """Test Oracle configuration validation with missing service."""
        with pytest.raises(ValidationError, match="oracle_service"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_port=1521,
                oracle_user="test",
                oracle_password="test",
                # oracle_service is missing - this should raise validation error
            )

    def test_get_oracle_config(self) -> None:
        """Test Oracle configuration generation."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
            batch_size=2000,
            connection_timeout=45,
        )

        oracle_config = config.get_oracle_config()

        if oracle_config["host"] != "localhost":
            raise AssertionError(f"Expected 'localhost', got {oracle_config['host']}")
        assert oracle_config["port"] == 1521
        if oracle_config["service_name"] != "XE":
            raise AssertionError(f"Expected 'XE', got {oracle_config['service_name']}")
        assert oracle_config["username"] == "test"
        if oracle_config["password"] != "test":
            raise AssertionError(f"Expected 'test', got {oracle_config['password']}")
        # connection_timeout is not included in FlextDbOracleConfig

    def test_get_table_name_basic(self) -> None:
        """Test basic table name generation."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        table_name = config.get_table_name("users")
        if table_name != "USERS":
            raise AssertionError(f"Expected {'USERS'}, got {table_name}")

    def test_get_table_name_uppercase(self) -> None:
        """Test table name generation with uppercase conversion."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        table_name = config.get_table_name("users")
        if table_name != "USERS":
            raise AssertionError(f"Expected {'USERS'}, got {table_name}")

    def test_get_table_name_special_chars(self) -> None:
        """Test table name generation with special characters."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        table_name = config.get_table_name("user-profiles")
        if table_name != "USER_PROFILES":
            raise AssertionError(f"Expected {'USER_PROFILES'}, got {table_name}")

    def test_get_table_name_with_special_chars_only(self) -> None:
        """Test table name generation with special characters."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
        )

        table_name = config.get_table_name("user-profiles.data")
        if table_name != "USER_PROFILES_DATA":
            raise AssertionError(f"Expected {'USER_PROFILES_DATA'}, got {table_name}")

    def test_load_method_enum_values(self) -> None:
        """Test LoadMethod enum values."""
        if LoadMethod.INSERT.value != "insert":
            raise AssertionError(f"Expected {'insert'}, got {LoadMethod.INSERT.value}")
        assert LoadMethod.MERGE.value == "merge"
        if LoadMethod.BULK_INSERT.value != "bulk_insert":
            raise AssertionError(
                f"Expected {'bulk_insert'}, got {LoadMethod.BULK_INSERT.value}"
            )
        assert LoadMethod.BULK_MERGE.value == "bulk_merge"

    def test_load_method_from_config(self) -> None:
        """Test LoadMethod from configuration."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="XE",
            oracle_user="test",
            oracle_password="test",
            load_method=LoadMethod.MERGE,
        )

        if config.load_method != LoadMethod.MERGE:
            raise AssertionError(
                f"Expected {LoadMethod.MERGE}, got {config.load_method}"
            )
        assert config.load_method.value == "merge"
