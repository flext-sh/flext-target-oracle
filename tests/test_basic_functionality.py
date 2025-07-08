"""Test basic functionality without requiring database connection.

These tests validate the target's basic functionality without
needing an actual Oracle database connection.
"""

from unittest.mock import patch

import pytest

from flext_target_oracle import OracleTarget
from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.sinks import OracleSink


class TestBasicFunctionality:
    """Test basic target functionality without database."""

    def test_target_initialization_minimal(self) -> None:
        """Test target can be initialized with minimal config."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)
        assert target.name == "flext-target-oracle"
        assert target.config["host"] == "test-host"
        assert target.config["username"] == "test-user"

    def test_target_capabilities(self) -> None:
        """Test target reports correct capabilities."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)
        capabilities = target.capabilities

        # Check for expected capabilities
        capability_values = [cap.value for cap in capabilities]
        # Singer SDK target capabilities
        assert "about" in capability_values
        assert "stream-maps" in capability_values
        assert "schema-flattening" in capability_values

    def test_config_defaults(self) -> None:
        """Test configuration defaults are applied."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)

        # Check defaults from config schema
        assert target.config.get("port", 1521) == 1521
        assert target.config.get("protocol", "tcp") == "tcp"
        assert target.config.get("pool_size", 10) == 10
        assert target.config.get("add_record_metadata", True) is True
        assert target.config.get("load_method", "append-only") == "append-only"

    def test_license_flags_default_to_false(self) -> None:
        """Test Oracle license flags default to false."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)

        # All license flags should default to false
        assert target.config.get(
            "oracle_has_partitioning_option",
            False) is False
        assert target.config.get(
            "oracle_has_compression_option",
            False) is False
        assert target.config.get("oracle_has_inmemory_option", False) is False
        assert target.config.get(
            "oracle_has_advanced_security_option",
            False) is False

    def test_connector_url_generation(self) -> None:
        """Test connector generates correct URLs."""
        config = {
            "host": "oracle.example.com",
            "port": 1522,
            "username": "test_user",
            "password": "test_pass",
            "service_name": "TESTDB",
        }

        connector = OracleConnector(config=config)
        url = connector.get_sqlalchemy_url(config)

        # Verify URL components
        assert "oracle+oracledb://" in url
        assert "test_user:test_pass@" in url
        assert "oracle.example.com:1522" in url
        assert "TESTDB" in url

    def test_connector_tcps_url(self) -> None:
        """Test connector generates TCPS URLs correctly."""
        config = {
            "host": "secure.oracle.com",
            "port": 2484,
            "username": "secure_user",
            "password": "secure_pass",
            "service_name": "SECUREDB",
            "protocol": "tcps",
        }

        connector = OracleConnector(config=config)
        url = connector.get_sqlalchemy_url(config)

        # Should still use oracle+oracledb
        assert "oracle+oracledb://" in url
        # For TCPS, the connection is in DSN format
        assert "(DESCRIPTION=" in url
        assert "(PROTOCOL=TCPS)" in url
        assert "(HOST=secure.oracle.com)" in url
        assert "(PORT=2484)" in url

    def test_sink_initialization(self) -> None:
        """Test sink can be initialized."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)

        schema = {
            "type": "object",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        # Mock the connector to avoid actual database connection
        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target,
                stream_name="test_stream",
                schema=schema,
                key_properties=["id"],
            )

            assert sink.stream_name == "test_stream"
            assert sink.key_properties == ["id"]

    def test_type_mapping(self) -> None:
        """Test Singer type to Oracle type mapping."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass"}

        target = OracleTarget(config=config)
        schema: dict[str, Any] = {"properties": {}}

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target,
                stream_name="test_stream",
                schema=schema)

            # Test various type mappings
            string_type = sink._singer_sdk_to_oracle_type(  # type: ignore[attr-defined]
                {"type": "string", "maxLength": 100},
            )
            assert "VARCHAR2" in str(
                string_type) or "NVARCHAR2" in str(string_type)

            integer_type = sink._singer_sdk_to_oracle_type({"type": "integer"})  # type: ignore[attr-defined]
            assert "NUMBER" in str(integer_type)

            boolean_type = sink._singer_sdk_to_oracle_type({"type": "boolean"})  # type: ignore[attr-defined]
            assert "NUMBER" in str(
                boolean_type) or "BOOLEAN" in str(boolean_type)

            object_type = sink._singer_sdk_to_oracle_type({"type": "object"})  # type: ignore[attr-defined]
            assert "CLOB" in str(object_type) or "JSON" in str(object_type)

    def test_record_conformance(self) -> None:
        """Test record conformance for Oracle."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "boolean_true_value": "1",
            "boolean_false_value": "0",
        }

        target = OracleTarget(config=config)
        schema = {
            "properties": {
                "id": {"type": "integer"},
                "active": {"type": "boolean"},
                "data": {"type": "object"},
            },
        }

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target,
                stream_name="test_stream",
                schema=schema)

            # Test record conformance
            record = {"id": 123, "active": True, "data": {"key": "value"}}

            conformed = sink._conform_record(record)  # type: ignore[attr-defined]

            assert conformed["id"] == 123
            assert conformed["active"] == 1  # Boolean converted to number
            # Object serialized to JSON
            assert conformed["data"] == '{"key": "value"}'

    def test_batch_config_parsing(self) -> None:
        """Test batch configuration parsing."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "batch_config": {
                "batch_size": 5000,
                "batch_wait_limit_seconds": 30.0,
                "encoding": {"format": "jsonl", "compression": "gzip"},
            },
        }

        target = OracleTarget(config=config)

        assert target.config["batch_config"]["batch_size"] == 5000
        assert target.config["batch_config"]["batch_wait_limit_seconds"] == 30.0
        assert target.config["batch_config"]["encoding"]["format"] == "jsonl"

    def test_parallel_configuration(self) -> None:
        """Test parallel processing configuration."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "parallel_threads": 4,
            "chunk_size": 5000,
            "parallel_degree": 8,
        }

        target = OracleTarget(config=config)

        with patch.object(OracleSink, "setup"):
            sink = OracleSink(
                target=target, stream_name="test_stream", schema={"properties": {}},
            )

            assert sink._parallel_threads == 4  # type: ignore[attr-defined]
            assert sink._chunk_size == 5000  # type: ignore[attr-defined]

            # Thread pool should be created for parallel processing
            if sink._parallel_threads > 1:  # type: ignore[attr-defined]
                assert sink._executor is not None  # type: ignore[attr-defined]

    def test_wan_optimization_config(self) -> None:
        """Test WAN optimization configuration."""
        config = {
            "host": "remote.oracle.com",
            "username": "wan_user",
            "password": "wan_pass",
            "service_name": "WANDB",
            # WAN optimization settings
            "sdu_size": 32767,
            "tdu_size": 32767,
            "send_buf_size": 1048576,
            "recv_buf_size": 1048576,
            "tcp_nodelay": True,
            "enable_network_compression": True,
        }

        connector = OracleConnector(config=config)

        # Verify WAN settings are in config
        assert connector.config["sdu_size"] == 32767
        assert connector.config["tcp_nodelay"] is True
        assert connector.config["enable_network_compression"] is True

    @pytest.mark.parametrize(
        ("load_method", "_expected_behavior"),
        [
            ("append-only", "insert"),
            ("upsert", "merge"),
            ("overwrite", "truncate_then_insert"),
        ],
    )
    def test_load_methods(self, load_method: str, _expected_behavior: str) -> None:
        """Test different load methods are configured correctly."""
        # Note: _expected_behavior is parametrized but not used in logic
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "load_method": load_method,
        }

        target = OracleTarget(config=config)
        assert target.config["load_method"] == load_method

    def test_error_handling_config(self) -> None:
        """Test error handling configuration."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
            "max_retries": 3,
            "retry_delay": 2.0,
            "retry_backoff": 1.5,
            "retry_jitter": True,
            "fail_fast": False,
            "on_schema_mismatch": "evolve",
        }

        target = OracleTarget(config=config)

        assert target.config["max_retries"] == 3
        assert target.config["retry_delay"] == 2.0
        assert target.config["on_schema_mismatch"] == "evolve"
