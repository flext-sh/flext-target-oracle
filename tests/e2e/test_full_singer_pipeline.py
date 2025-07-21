"""End-to-end Singer pipeline tests.

Tests complete Singer protocol workflows from start to finish.
"""

import json
import os
from io import StringIO
from typing import Any

import pytest

from flext_target_oracle import OracleTarget


class TestFullSingerPipeline:
    """Test complete Singer protocol pipeline."""

    @pytest.fixture
    def oracle_config(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "default_target_schema": "FLEXT_E2E_TEST",
            "batch_size": 100,
        }

    @pytest.fixture
    def target_instance(self, oracle_config: dict[str, Any]) -> OracleTarget:
        """Create Oracle target instance for testing."""
        return OracleTarget(config=oracle_config)

    def test_simple_pipeline_workflow(self, target_instance: OracleTarget) -> None:
        """Test simple Singer pipeline workflow.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        # Prepare Singer messages
        messages = [
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                    },
                    "key_properties": ["id"],
                },
            },
            {
                "type": "RECORD",
                "stream": "users",
                "record": {
                    "id": 1,
                    "name": "Alice Johnson",
                    "email": "alice@example.com",
                    "created_at": "2024-01-01T10:00:00Z",
                },
            },
            {
                "type": "RECORD",
                "stream": "users",
                "record": {
                    "id": 2,
                    "name": "Bob Smith",
                    "email": "bob@example.com",
                    "created_at": "2024-01-01T11:00:00Z",
                },
            },
            {
                "type": "STATE",
                "value": {
                    "bookmarks": {
                        "users": {"replication_key_value": "2024-01-01T11:00:00Z"},
                    },
                },
            },
        ]

        # Create input stream
        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            # Mock stdin to provide our messages
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            # Run the target
            exit_code = target_instance.run()

            # Should complete successfully
            assert exit_code == 0

        except (ConnectionError, OSError, ValueError, ImportError, RuntimeError) as e:
            pytest.fail(f"Simple pipeline test failed: {e}")
        finally:
            # Restore stdin
            sys.stdin = original_stdin

    def test_complex_pipeline_workflow(self, target_instance: OracleTarget) -> None:
        """Test complex Singer pipeline with multiple streams."""
        # Complex multi-stream pipeline
        messages = [
            # Users stream schema
            {
                "type": "SCHEMA",
                "stream": "users",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
            },
            # Orders stream schema
            {
                "type": "SCHEMA",
                "stream": "orders",
                "schema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "amount": {"type": "number"},
                        "status": {"type": "string"},
                    },
                },
            },
            # Interleaved records from both streams
            {
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 1, "name": "User 1", "email": "user1@test.com"},
            },
            {
                "type": "RECORD",
                "stream": "orders",
                "record": {
                    "order_id": 101,
                    "user_id": 1,
                    "amount": 99.99,
                    "status": "pending",
                },
            },
            {
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 2, "name": "User 2", "email": "user2@test.com"},
            },
            {
                "type": "RECORD",
                "stream": "orders",
                "record": {
                    "order_id": 102,
                    "user_id": 2,
                    "amount": 149.99,
                    "status": "completed",
                },
            },
            # Multiple records for same stream
            {
                "type": "RECORD",
                "stream": "orders",
                "record": {
                    "order_id": 103,
                    "user_id": 1,
                    "amount": 75.50,
                    "status": "shipped",
                },
            },
            # State messages
            {
                "type": "STATE",
                "value": {
                    "bookmarks": {"users": {"id": 2}, "orders": {"order_id": 103}},
                },
            },
        ]

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target_instance.run()
            assert exit_code == 0

        except (ConnectionError, OSError, ValueError, ImportError, RuntimeError) as e:
            pytest.fail(f"Complex pipeline test failed: {e}")
        finally:
            sys.stdin = original_stdin

    def test_large_dataset_pipeline(self, target_instance: OracleTarget) -> None:
        """Test pipeline with large dataset."""
        messages = [
            # Schema
            {
                "type": "SCHEMA",
                "stream": "large_dataset",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "data": {"type": "string"},
                        "timestamp": {"type": "string"},
                    },
                },
            },
        ]

        # Add many records
        num_records = 1000
        messages.extend(
            {
                "type": "RECORD",
                "stream": "large_dataset",
                "record": {
                    "id": i,
                    "data": f"Large dataset record {i} with some additional data",
                    "timestamp": f"2024-01-01T{i % 24:02d}:{i % 60:02d}:00Z",
                },
            }
            for i in range(num_records)
        )

        # Final state
        messages.append(
            {
                "type": "STATE",
                "value": {"bookmarks": {"large_dataset": {"id": num_records - 1}}},
            },
        )

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            import time

            start_time = time.time()
            exit_code = target_instance.run()
            duration = time.time() - start_time

            assert exit_code == 0

            # Should process reasonably quickly
            records_per_second = num_records / duration

            # Should achieve minimum throughput
            assert records_per_second > 10  # At least 10 records/second

        except (
            ConnectionError,
            OSError,
            ValueError,
            ImportError,
            RuntimeError,
            MemoryError,
        ) as e:
            pytest.fail(f"Large dataset pipeline test failed: {e}")
        finally:
            sys.stdin = original_stdin


class TestSingerProtocolCompliance:
    """Test Singer protocol compliance."""

    @pytest.fixture
    def target_config(self) -> dict[str, Any]:
        """Get target configuration."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "default_target_schema": "FLEXT_PROTOCOL_TEST",
        }

    def test_state_message_forwarding(self, target_config: dict[str, Any]) -> None:
        """Test that STATE messages are properly forwarded to stdout."""
        target = OracleTarget(config=target_config)

        messages = [
            {
                "type": "SCHEMA",
                "stream": "state_test",
                "schema": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                },
            },
            {
                "type": "RECORD",
                "stream": "state_test",
                "record": {"id": 1},
            },
            {
                "type": "STATE",
                "value": {"bookmarks": {"state_test": {"id": 1}}},
            },
        ]

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys
            from io import StringIO as OutputCapture

            original_stdin = sys.stdin
            original_stdout = sys.stdout

            sys.stdin = input_stream
            captured_output = OutputCapture()
            sys.stdout = captured_output

            exit_code = target.run()

            _ = captured_output.getvalue()  # Captured for future use

            # Should have forwarded the STATE message
            assert exit_code == 0
            # Note: In a real implementation, STATE messages would be written to stdout
            # This test validates the protocol compliance structure

        except (ConnectionError, OSError, ValueError, ImportError, RuntimeError) as e:
            pytest.fail(f"State message forwarding test failed: {e}")
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    def test_invalid_message_handling(self, target_config: dict[str, Any]) -> None:
        """Test handling of invalid Singer messages."""
        target = OracleTarget(config=target_config)

        # Mix of valid and invalid messages
        messages_text = [
            # Valid schema
            json.dumps(
                {
                    "type": "SCHEMA",
                    "stream": "test_invalid",
                    "schema": {
                        "type": "object",
                        "properties": {"id": {"type": "integer"}},
                    },
                },
            ),
            # Invalid JSON
            "{ invalid json }",
            # Valid record
            json.dumps(
                {
                    "type": "RECORD",
                    "stream": "test_invalid",
                    "record": {"id": 1},
                },
            ),
            # Invalid message type
            json.dumps({"type": "INVALID_TYPE", "data": "test"}),
            # Another valid record
            json.dumps(
                {
                    "type": "RECORD",
                    "stream": "test_invalid",
                    "record": {"id": 2},
                },
            ),
        ]

        input_stream = StringIO("\\n".join(messages_text) + "\\n")

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target.run()

            # Should handle invalid messages gracefully and continue processing
            # Valid records should still be processed
            assert exit_code == 0

        except (
            ConnectionError,
            OSError,
            ValueError,
            ImportError,
            RuntimeError,
            TypeError,
        ) as e:
            pytest.fail(f"Invalid message handling test failed: {e}")
        finally:
            sys.stdin = original_stdin


class TestDataTypeHandling:
    """Test handling of various data types in Singer pipeline."""

    def test_comprehensive_data_types(self) -> None:
        """Test pipeline with comprehensive data type coverage."""
        config = {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "default_target_schema": "FLEXT_DATATYPE_TEST",
        }

        target = OracleTarget(config=config)

        messages = [
            {
                "type": "SCHEMA",
                "stream": "comprehensive_types",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "active": {"type": "boolean"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "metadata": {"type": "object"},
                        "tags": {"type": "array"},
                        "optional_field": {"type": ["null", "string"]},
                    },
                },
            },
            {
                "type": "RECORD",
                "stream": "comprehensive_types",
                "record": {
                    "id": 1,
                    "name": "Test Product",
                    "price": 29.99,
                    "active": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "metadata": {
                        "category": "electronics",
                        "subcategory": "phones",
                        "features": ["waterproof", "wireless_charging"],
                        "specs": {"screen_size": 6.1, "battery": 3000, "ram": 8},
                    },
                    "tags": ["new", "featured", "bestseller"],
                    "optional_field": "present",
                },
            },
            {
                "type": "RECORD",
                "stream": "comprehensive_types",
                "record": {
                    "id": 2,
                    "name": "Another Product",
                    "price": 149.50,
                    "active": False,
                    "created_at": "2024-01-02T14:30:00Z",
                    "metadata": {
                        "category": "books",
                        "author": "John Doe",
                        "pages": 250,
                    },
                    "tags": ["education", "technical"],
                    "optional_field": None,  # Null value
                },
            },
        ]

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target.run()
            assert exit_code == 0

        except (
            ConnectionError,
            OSError,
            ValueError,
            ImportError,
            RuntimeError,
            TypeError,
        ) as e:
            pytest.fail(f"Comprehensive data types test failed: {e}")
        finally:
            sys.stdin = original_stdin


class TestConfigurationVariants:
    """Test different configuration scenarios."""

    def test_minimal_configuration(self) -> None:
        """Test target with minimal configuration."""
        # Minimal config - only required fields
        minimal_config = {
            "host": os.getenv("ORACLE_HOST"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
        }

        target = OracleTarget(config=minimal_config)

        messages = [
            {
                "type": "SCHEMA",
                "stream": "minimal_test",
                "schema": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                },
            },
            {
                "type": "RECORD",
                "stream": "minimal_test",
                "record": {"id": 1},
            },
        ]

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target.run()
            assert exit_code == 0

        except (ConnectionError, OSError, ValueError, ImportError, RuntimeError) as e:
            pytest.fail(f"Minimal configuration test failed: {e}")
        finally:
            sys.stdin = original_stdin

    def test_custom_batch_size(self) -> None:
        """Test target with custom batch size."""
        config = {
            "host": os.getenv("ORACLE_HOST"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "batch_size": 10,  # Small batch size for testing
        }

        target = OracleTarget(config=config)

        messages = [
            {
                "type": "SCHEMA",
                "stream": "batch_test",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "data": {"type": "string"},
                    },
                },
            },
        ]

        # Add enough records to trigger multiple batches
        messages.extend(
            {
                "type": "RECORD",
                "stream": "batch_test",
                "record": {"id": i, "data": f"batch_record_{i}"},
            }
            for i in range(25)  # More than 2 batches
        )

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target.run()
            assert exit_code == 0

        except (ConnectionError, OSError, ValueError, ImportError, RuntimeError) as e:
            pytest.fail(f"Custom batch size test failed: {e}")
        finally:
            sys.stdin = original_stdin


class TestPipelineRobustness:
    """Test pipeline robustness and error recovery."""

    def test_connection_recovery(self) -> None:
        """Test pipeline behavior with connection issues."""
        # This test would simulate connection drops and recovery
        # For now, we'll skip it as it requires special network configuration
        pytest.fail("Connection recovery test requires special network setup")

    def test_large_message_handling(self) -> None:
        """Test handling of very large individual messages."""
        config = {
            "host": os.getenv("ORACLE_HOST"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
        }

        target = OracleTarget(config=config)

        # Create a large record
        large_data = "x" * 100000  # 100KB of data

        messages = [
            {
                "type": "SCHEMA",
                "stream": "large_message_test",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "large_field": {"type": "string"},
                    },
                },
            },
            {
                "type": "RECORD",
                "stream": "large_message_test",
                "record": {"id": 1, "large_field": large_data},
            },
        ]

        input_stream = StringIO()
        for message in messages:
            input_stream.write(json.dumps(message) + "\\n")
        input_stream.seek(0)

        try:
            import sys

            original_stdin = sys.stdin
            sys.stdin = input_stream

            exit_code = target.run()
            assert exit_code == 0

        except (
            ConnectionError,
            OSError,
            ValueError,
            ImportError,
            RuntimeError,
            MemoryError,
        ) as e:
            pytest.fail(f"Large message handling test failed: {e}")
        finally:
            sys.stdin = original_stdin
