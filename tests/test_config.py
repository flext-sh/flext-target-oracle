"""Tests for FlextOracleTargetConfig."""

import pytest
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
            msg = f"Expected {'localhost'}, got {config.oracle_host}"
            raise AssertionError(msg)
        assert config.oracle_port == 1521
        if config.oracle_service != "XE":
            msg = f"Expected {'XE'}, got {config.oracle_service}"
            raise AssertionError(msg)
        assert config.oracle_user == "test_user"
        if config.oracle_password != "test_pass":
            msg = f"Expected {'test_pass'}, got {config.oracle_password}"
            raise AssertionError(
                msg,
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
            msg = f"Expected {1521}, got {config.oracle_port}"
            raise AssertionError(msg)
        if config.default_target_schema != "target":
            msg = f"Expected {'target'}, got {config.default_target_schema}"
            raise AssertionError(
                msg,
            )
        assert config.batch_size == 1000
        assert config.load_method == LoadMethod.INSERT
        if not config.use_bulk_operations:
            msg = f"Expected True, got {config.use_bulk_operations}"
            raise AssertionError(msg)
        assert config.connection_timeout == 30

    def test_custom_values(self) -> None:
        """Test custom values."""
        config = FlextOracleTargetConfig(
            oracle_host="oracle.example.com",
            oracle_port=1522,
            oracle_service="PROD",
            oracle_user="REDACTED_LDAP_BIND_PASSWORD",
            oracle_password="secret",
            default_target_schema="DATA_WAREHOUSE",
            batch_size=5000,
            load_method=LoadMethod.MERGE,
            use_bulk_operations=False,
            connection_timeout=60,
        )

        if config.oracle_host != "oracle.example.com":
            msg = f"Expected {'oracle.example.com'}, got {config.oracle_host}"
            raise AssertionError(
                msg,
            )
        assert config.oracle_port == 1522
        if config.oracle_service != "PROD":
            msg = f"Expected {'PROD'}, got {config.oracle_service}"
            raise AssertionError(msg)
        assert config.oracle_user == "REDACTED_LDAP_BIND_PASSWORD"
        if config.oracle_password != "secret":
            msg = f"Expected {'secret'}, got {config.oracle_password}"
            raise AssertionError(msg)
        if config.default_target_schema != "DATA_WAREHOUSE":
            msg = f"Expected {'DATA_WAREHOUSE'}, got {config.default_target_schema}"
            raise AssertionError(
                msg,
            )
        if config.batch_size != 5000:
            msg = f"Expected {5000}, got {config.batch_size}"
            raise AssertionError(msg)
        if config.load_method != LoadMethod.MERGE:
            msg = f"Expected {LoadMethod.MERGE}, got {config.load_method}"
            raise AssertionError(
                msg,
            )
        if config.use_bulk_operations:
            msg = f"Expected False, got {config.use_bulk_operations}"
            raise AssertionError(msg)
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
            msg = f"Expected 'Oracle host is required' in {result.error}"
            raise AssertionError(
                msg,
            )

    def test_validate_oracle_config_invalid_port(self) -> None:
        """Test Oracle configuration validation with invalid port."""
        # Pydantic validates at creation time, so we expect ValidationError
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_port=0,  # Invalid port
                oracle_service="XE",
                oracle_user="test",
                oracle_password="test",
            )

        # Verify the error is about port validation
        assert "port must be between 1 and 65535" in str(exc_info.value)

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
            msg = f"Expected '{expected_msg}' in {result.error}"
            raise AssertionError(msg)

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
            msg = f"Expected '{expected_msg}' in {result.error}"
            raise AssertionError(msg)

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
            msg = f"Expected 'localhost', got {oracle_config['host']}"
            raise AssertionError(msg)
        assert oracle_config["port"] == 1521
        if oracle_config["service_name"] != "XE":
            msg = f"Expected 'XE', got {oracle_config['service_name']}"
            raise AssertionError(msg)
        assert oracle_config["username"] == "test"
        if oracle_config["password"] != "test":
            msg = f"Expected 'test', got {oracle_config['password']}"
            raise AssertionError(msg)
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
            msg = f"Expected {'USERS'}, got {table_name}"
            raise AssertionError(msg)

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
            msg = f"Expected {'USERS'}, got {table_name}"
            raise AssertionError(msg)

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
            msg = f"Expected {'USER_PROFILES'}, got {table_name}"
            raise AssertionError(msg)

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
            msg = f"Expected {'USER_PROFILES_DATA'}, got {table_name}"
            raise AssertionError(msg)

    def test_load_method_enum_values(self) -> None:
        """Test LoadMethod enum values."""
        if LoadMethod.INSERT.value != "insert":
            msg = f"Expected {'insert'}, got {LoadMethod.INSERT.value}"
            raise AssertionError(msg)
        assert LoadMethod.MERGE.value == "merge"
        if LoadMethod.BULK_INSERT.value != "bulk_insert":
            msg = f"Expected {'bulk_insert'}, got {LoadMethod.BULK_INSERT.value}"
            raise AssertionError(
                msg,
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
            msg = f"Expected {LoadMethod.MERGE}, got {config.load_method}"
            raise AssertionError(
                msg,
            )
        assert config.load_method.value == "merge"
