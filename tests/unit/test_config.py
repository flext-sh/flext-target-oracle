"""Unit Tests for FlextOracleTargetConfig - Enterprise Configuration Management.

This module provides comprehensive unit tests for the FlextOracleTargetConfig class,
validating configuration creation, validation, domain rules, and Oracle integration
patterns. Tests ensure type safety, business rule compliance, and proper FLEXT
ecosystem integration.

The test suite covers:
    - Configuration creation with various parameter combinations
    - Field validation including edge cases and error conditions
    - Domain validation rules using Chain of Responsibility pattern
    - Oracle configuration generation for flext-db-oracle integration
    - Table name generation and Oracle naming convention compliance
    - LoadMethod enumeration usage and validation

Test Categories:
    - Basic Configuration: Core configuration creation and defaults
    - Validation Tests: Pydantic and domain validation rule testing
    - Integration Tests: Oracle config generation and compatibility
    - Business Logic Tests: Table naming and load method selection

Note:
    These tests validate the configuration layer in isolation. Integration
    tests with actual Oracle connectivity are located in tests/integration/.

"""

import pytest
from pydantic import ValidationError

from flext_target_oracle import FlextOracleTargetConfig, LoadMethod

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3


class TestFlextOracleTargetConfig:
    """Comprehensive test suite for FlextOracleTargetConfig validation and functionality.

    This test class validates all aspects of the Oracle target configuration including
    creation, validation, domain rules, and integration with the FLEXT ecosystem.
    Tests ensure the configuration class properly handles various scenarios from
    basic setup to edge cases and error conditions.
    """

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
          msg: str = f"Expected {'localhost'}, got {config.oracle_host}"
          raise AssertionError(msg)
      assert config.oracle_port == 1521
      if config.oracle_service != "XE":
          msg: str = f"Expected {'XE'}, got {config.oracle_service}"
          raise AssertionError(msg)
      assert config.oracle_user == "test_user"
      if config.oracle_password != "test_pass":
          msg: str = f"Expected {'test_pass'}, got {config.oracle_password}"
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
          msg: str = f"Expected {1521}, got {config.oracle_port}"
          raise AssertionError(msg)
      if config.default_target_schema != "target":
          msg: str = f"Expected {'target'}, got {config.default_target_schema}"
          raise AssertionError(
              msg,
          )
      assert config.batch_size == 1000
      assert config.load_method == LoadMethod.INSERT
      if not config.use_bulk_operations:
          msg: str = f"Expected True, got {config.use_bulk_operations}"
          raise AssertionError(msg)
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
          msg: str = f"Expected {'oracle.example.com'}, got {config.oracle_host}"
          raise AssertionError(
              msg,
          )
      assert config.oracle_port == 1522
      if config.oracle_service != "PROD":
          msg: str = f"Expected {'PROD'}, got {config.oracle_service}"
          raise AssertionError(msg)
      assert config.oracle_user == "admin"
      if config.oracle_password != "secret":
          msg: str = f"Expected {'secret'}, got {config.oracle_password}"
          raise AssertionError(msg)
      if config.default_target_schema != "DATA_WAREHOUSE":
          msg: str = (
              f"Expected {'DATA_WAREHOUSE'}, got {config.default_target_schema}"
          )
          raise AssertionError(
              msg,
          )
      if config.batch_size != 5000:
          msg: str = f"Expected {5000}, got {config.batch_size}"
          raise AssertionError(msg)
      if config.load_method != LoadMethod.MERGE:
          msg: str = f"Expected {LoadMethod.MERGE}, got {config.load_method}"
          raise AssertionError(
              msg,
          )
      if config.use_bulk_operations:
          msg: str = f"Expected False, got {config.use_bulk_operations}"
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
      assert result.success

    def test_validate_oracle_config_missing_host(self) -> None:
      """Test Oracle configuration validation with missing host."""
      # Pydantic validation should prevent empty host during creation
      with pytest.raises(ValidationError) as exc_info:
          FlextOracleTargetConfig(
              oracle_host="",  # Empty host
              oracle_port=1521,
              oracle_service="XE",
              oracle_user="test",
              oracle_password="test",
          )

      # Verify the validation error is about host
      assert "oracle_host" in str(exc_info.value).lower()

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
      assert "oracle_port" in str(exc_info.value)

    def test_validate_oracle_config_missing_username(self) -> None:
      """Test Oracle configuration validation with missing username."""
      # Pydantic validation should prevent empty username during creation
      with pytest.raises(ValidationError) as exc_info:
          FlextOracleTargetConfig(
              oracle_host="localhost",
              oracle_port=1521,
              oracle_service="XE",
              oracle_user="",  # Empty username
              oracle_password="test",
          )

      # Verify the validation error is about username
      assert "oracle_user" in str(exc_info.value).lower()

    def test_validate_oracle_config_missing_password(self) -> None:
      """Test Oracle configuration validation with missing password."""
      # Pydantic validation should prevent empty password during creation
      with pytest.raises(ValidationError) as exc_info:
          FlextOracleTargetConfig(
              oracle_host="localhost",
              oracle_port=1521,
              oracle_service="XE",
              oracle_user="test",
              oracle_password="",  # Empty password
          )

      # Verify the validation error is about password
      assert "oracle_password" in str(exc_info.value).lower()

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
          msg: str = f"Expected 'localhost', got {oracle_config['host']}"
          raise AssertionError(msg)
      assert oracle_config["port"] == 1521
      if oracle_config["service_name"] != "XE":
          msg: str = f"Expected 'XE', got {oracle_config['service_name']}"
          raise AssertionError(msg)
      assert oracle_config["username"] == "test"
      # Password is correctly masked for security - verify it exists but don't check value
      assert "password" in oracle_config
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
          msg: str = f"Expected {'USERS'}, got {table_name}"
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
          msg: str = f"Expected {'USERS'}, got {table_name}"
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
          msg: str = f"Expected {'USER_PROFILES'}, got {table_name}"
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
          msg: str = f"Expected {'USER_PROFILES_DATA'}, got {table_name}"
          raise AssertionError(msg)

    def test_load_method_enum_values(self) -> None:
      """Test LoadMethod enum values."""
      if LoadMethod.INSERT.value != "insert":
          msg: str = f"Expected {'insert'}, got {LoadMethod.INSERT.value}"
          raise AssertionError(msg)
      assert LoadMethod.MERGE.value == "merge"
      if LoadMethod.BULK_INSERT.value != "bulk_insert":
          msg: str = f"Expected {'bulk_insert'}, got {LoadMethod.BULK_INSERT.value}"
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
          msg: str = f"Expected {LoadMethod.MERGE}, got {config.load_method}"
          raise AssertionError(
              msg,
          )
      assert config.load_method.value == "merge"
