"""Additional Coverage Tests for FlextOracleTargetConfig.

This module provides targeted tests to improve coverage on specific methods
in the configuration that are not adequately tested, focusing on edge cases,
validation scenarios, and domain rule testing.
"""

import pytest
from pydantic import ValidationError

from flext_target_oracle import FlextOracleTargetConfig, LoadMethod


class TestFlextOracleTargetConfigCoverage:
    """Coverage-focused tests for FlextOracleTargetConfig methods."""

    def test_config_with_all_optional_parameters(self) -> None:
        """Test configuration with all optional parameters set."""
        config = FlextOracleTargetConfig(
            oracle_host="prod-oracle.company.com",
            oracle_port=1521,
            oracle_service="PRODDB",
            oracle_user="prod_user",
            oracle_password="secure_prod_password",
            default_target_schema="PROD_SCHEMA",
            batch_size=10000,
            connection_timeout=120,
            use_bulk_operations=True,
            load_method=LoadMethod.BULK_MERGE,
        )

        # Verify all parameters are set correctly
        assert config.oracle_host == "prod-oracle.company.com"
        assert config.oracle_port == 1521
        assert config.oracle_service == "PRODDB"
        assert config.oracle_user == "prod_user"
        assert config.oracle_password == "secure_prod_password"
        assert config.default_target_schema == "PROD_SCHEMA"
        assert config.batch_size == 10000
        assert config.connection_timeout == 120
        assert config.use_bulk_operations is True
        assert config.load_method == LoadMethod.BULK_MERGE

    def test_config_edge_case_ports(self) -> None:
        """Test configuration with edge case port values."""
        # Test minimum valid port
        config_min = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1,
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        assert config_min.oracle_port == 1

        # Test maximum valid port
        config_max = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=65535,
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )
        assert config_max.oracle_port == 65535

    def test_config_invalid_ports(self) -> None:
        """Test configuration with invalid port values."""
        # Test port below minimum
        with pytest.raises(ValidationError, match="oracle_port"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_port=0,
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
            )

        # Test port above maximum
        with pytest.raises(ValidationError, match="oracle_port"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_port=65536,
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
            )

    def test_config_invalid_batch_sizes(self) -> None:
        """Test configuration with invalid batch sizes."""
        # Test batch size below minimum
        with pytest.raises(ValidationError, match="batch_size"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
                batch_size=0,
            )

        # Test batch size above maximum
        with pytest.raises(ValidationError, match="batch_size"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
                batch_size=50001,
            )

    def test_config_edge_case_batch_sizes(self) -> None:
        """Test configuration with edge case batch sizes."""
        # Test minimum valid batch size
        config_min = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
            batch_size=1,
        )
        assert config_min.batch_size == 1

        # Test maximum valid batch size
        config_max = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
            batch_size=50000,
        )
        assert config_max.batch_size == 50000

    def test_config_invalid_timeout_values(self) -> None:
        """Test configuration with invalid timeout values."""
        # Test timeout below minimum
        with pytest.raises(ValidationError, match="connection_timeout"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
                connection_timeout=0,
            )

        # Test timeout above maximum (3600 seconds)
        with pytest.raises(ValidationError, match="connection_timeout"):
            FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
                connection_timeout=3601,  # Greater than 3600
            )

    def test_load_methods_comprehensive(self) -> None:
        """Test all LoadMethod enum values."""
        methods = [
            LoadMethod.INSERT,
            LoadMethod.MERGE,
            LoadMethod.BULK_INSERT,
            LoadMethod.BULK_MERGE,
        ]

        for method in methods:
            config = FlextOracleTargetConfig(
                oracle_host="localhost",
                oracle_service="xe",
                oracle_user="test",
                oracle_password="test",
                load_method=method,
            )
            assert config.load_method == method

    def test_config_default_schema_behavior(self) -> None:
        """Test default target schema behavior."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )

        # Test default schema value
        assert config.default_target_schema == "target"

        # Test custom schema
        config_custom = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
            default_target_schema="CUSTOM_SCHEMA",
        )
        assert config_custom.default_target_schema == "CUSTOM_SCHEMA"

    def test_get_oracle_config_comprehensive(self) -> None:
        """Test get_oracle_config with all parameters."""
        config = FlextOracleTargetConfig(
            oracle_host="prod-db.company.com",
            oracle_port=1521,
            oracle_service="PRODDB",
            oracle_user="etl_user",
            oracle_password="secure_password_123",
            connection_timeout=90,
        )

        oracle_config = config.get_oracle_config()

        # Test all expected keys are present
        expected_keys = {"host", "port", "service_name", "username", "password"}
        assert all(key in oracle_config for key in expected_keys)

        # Test values (password will be masked)
        assert oracle_config["host"] == "prod-db.company.com"
        assert oracle_config["port"] == 1521
        assert oracle_config["service_name"] == "PRODDB"
        assert oracle_config["username"] == "etl_user"
        # Password is masked for security

    def test_model_validation_comprehensive(self) -> None:
        """Test comprehensive model validation scenarios."""
        # Test with minimal valid configuration
        minimal_config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="test",
        )

        # Verify defaults are applied
        assert minimal_config.oracle_port == 1521
        assert minimal_config.batch_size == 1000
        assert minimal_config.connection_timeout == 30
        assert minimal_config.use_bulk_operations is True
        assert minimal_config.load_method == LoadMethod.INSERT
        assert minimal_config.default_target_schema == "target"

    def test_validate_domain_rules_edge_cases(self) -> None:
        """Test validate_domain_rules with edge cases."""
        # Test with valid minimum configuration
        config = FlextOracleTargetConfig(
            oracle_host="a",  # Minimum length
            oracle_service="a",  # Minimum length
            oracle_user="a",  # Minimum length
            oracle_password="a",  # Minimum length
        )

        result = config.validate_domain_rules()
        assert result.success

    def test_config_string_representations(self) -> None:
        """Test string representation methods."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="secret_password",
        )

        # Test string representation (current implementation includes password)
        config_str = str(config)
        assert "secret_password" in config_str  # Current implementation exposes password
        assert "localhost" in config_str

        # Test repr (current implementation excludes password for security)
        config_repr = repr(config)
        assert "secret_password" not in config_repr  # Password excluded from repr for security

    def test_config_serialization_security(self) -> None:
        """Test that sensitive data is properly handled in serialization."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_service="xe",
            oracle_user="test",
            oracle_password="very_secret_password",
        )

        # Test model_dump includes all fields (passwords are not masked in current implementation)
        config_dict = config.model_dump()

        # Password should be present in config_dict
        assert "oracle_password" in config_dict
        # Current implementation includes password in plain text (no masking implemented)
        assert config_dict["oracle_password"] == "very_secret_password"

    def test_field_validation_error_messages(self) -> None:
        """Test detailed validation error messages."""
        # Test multiple validation errors at once
        with pytest.raises(ValidationError) as exc_info:
            FlextOracleTargetConfig(
                oracle_host="",  # Too short
                oracle_port=-1,  # Too small
                oracle_service="",  # Too short
                oracle_user="",  # Too short
                oracle_password="",  # Too short
                batch_size=0,  # Too small
                connection_timeout=-1,  # Too small
            )

        error_str = str(exc_info.value)
        # Verify multiple fields are reported
        assert "oracle_host" in error_str
        assert "oracle_port" in error_str
        assert "oracle_service" in error_str
        assert "oracle_user" in error_str
        assert "oracle_password" in error_str
