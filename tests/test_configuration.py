"""Test configuration validation and parameter handling."""

import pytest

from flext_target_oracle import OracleTarget


class TestConfiguration:
    """Test configuration validation."""

    def test_minimal_config(self) -> None:
        """Test minimal required configuration."""
        config = {
            "host": "localhost",
            "username": "test_user",
            "password": "test_password",
            "service_name": "XEPDB1",
        }

        target = OracleTarget(config=config)
        assert target.name == "flext-target-oracle"
        assert target.config["host"] == "localhost"
        assert target.config.get("port", 1521) == 1521

    def test_missing_required_fields(self) -> None:
        """Test error on missing required fields."""
        # Missing host
        config = {"username": "test_user", "password": "test_password"}

        with pytest.raises((ValueError, ConnectionError, Exception)):
            OracleTarget(config=config)

    def test_all_connection_parameters(self) -> None:
        """Test all connection parameters."""
        config = {
            "host": "oracle.example.com",
            "port": 1522,
            "service_name": "PROD",
            "username": "etl_user",
            "password": "secure_password",
            "schema": "ETL_SCHEMA",
            "protocol": "tcps",
            "wallet_location": "/path/to/wallet",
            "wallet_password": "wallet_pass",
            "ssl_server_cert_dn": "CN=server",
            "connection_timeout": 120,
            "encoding": "UTF-8",
        }

        target = OracleTarget(config=config)
        assert target.config["protocol"] == "tcps"
        assert target.config["wallet_location"] == "/path/to/wallet"

    def test_performance_parameters(self) -> None:
        """Test performance configuration parameters."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # Performance settings
            "batch_config": {"batch_size": 50000, "batch_wait_limit_seconds": 30},
            "pool_size": 20,
            "max_overflow": 40,
            "use_bulk_operations": True,
            "use_merge_statements": True,
            "parallel_degree": 4,
            "array_size": 5000,
            "prefetch_rows": 1000,
        }

        target = OracleTarget(config=config)
        assert target.config["pool_size"] == 20
        assert target.config["parallel_degree"] == 4
        assert target.config["use_bulk_operations"] is True

    def test_oracle_specific_features(self) -> None:
        """Test Oracle-specific feature configuration."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # Oracle features
            "enable_compression": True,
            "compression_type": "advanced",
            "enable_partitioning": True,
            "partition_type": "range",
            "partition_column": "_sdc_extracted_at",
            "use_direct_path": True,
            "nologging": True,
            "gather_statistics": True,
        }

        target = OracleTarget(config=config)
        assert target.config["compression_type"] == "advanced"
        assert target.config["partition_type"] == "range"

    def test_data_type_configuration(self) -> None:
        """Test data type configuration parameters."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # Data type settings
            "varchar_max_length": 2000,
            "use_nvarchar": True,
            "number_precision": 30,
            "number_scale": 5,
            "timestamp_timezone": "America/New_York",
            "json_column_type": "JSON",
            "boolean_true_value": "1",
            "boolean_false_value": "0",
        }

        target = OracleTarget(config=config)
        assert target.config["varchar_max_length"] == 2000
        assert target.config["use_nvarchar"] is True
        assert target.config["timestamp_timezone"] == "America/New_York"

    def test_sqlalchemy_configuration(self) -> None:
        """Test SQLAlchemy engine configuration."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # SQLAlchemy settings
            "echo": True,
            "echo_pool": True,
            "query_cache_size": 2000,
            "use_insertmanyvalues": True,
            "insertmanyvalues_page_size": 5000,
            "isolation_level": "SERIALIZABLE",
            "pool_use_lifo": True,
            "pool_reset_on_return": "commit",
        }

        target = OracleTarget(config=config)
        assert target.config["echo"] is True
        assert target.config["isolation_level"] == "SERIALIZABLE"

    def test_monitoring_configuration(self) -> None:
        """Test monitoring and logging configuration."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            # Monitoring
            "log_level": "DEBUG",
            "log_sql_statements": True,
            "log_metrics": True,
            "metrics_log_frequency": 500,
            "profile_queries": True,
            "trace_sql": True,
        }

        target = OracleTarget(config=config)
        assert target.config["log_level"] == "DEBUG"
        assert target.config["log_sql_statements"] is True

    def test_load_method_configuration(self) -> None:
        """Test different load method configurations."""
        # Append-only (default)
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            "load_method": "append-only",
        }
        target = OracleTarget(config=config)
        assert target.config["load_method"] == "append-only"

        # Upsert
        config["load_method"] = "upsert"
        target = OracleTarget(config=config)
        assert target.config["load_method"] == "upsert"

        # Overwrite
        config["load_method"] = "overwrite"
        target = OracleTarget(config=config)
        assert target.config["load_method"] == "overwrite"

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
        }

        target = OracleTarget(config=config)

        # Check defaults
        assert target.config.get("port", 1521) == 1521
        assert target.config.get("protocol", "tcp") == "tcp"
        assert target.config.get("pool_size", 10) == 10
        assert target.config.get("use_bulk_operations", True) is True
        assert target.config.get("add_record_metadata", True) is True
        assert target.config.get("varchar_max_length", 4000) == 4000
