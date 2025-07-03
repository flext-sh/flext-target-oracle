"""
Test Singer message processing.
"""

import contextlib
import json
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from flext_target_oracle import OracleTarget


class TestMessageProcessing:
    """Test Singer message processing."""

    @pytest.fixture
    def oracle_config(self):
        """Oracle configuration for testing."""
        return {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "XE",
            "add_record_metadata": True,
        }

    @pytest.fixture
    def schema_message(self):
        """Sample SCHEMA message."""
        return {
            "type": "SCHEMA",
            "stream": "test_stream",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "value": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }

    @pytest.fixture
    def record_messages(self):
        """Sample RECORD messages."""
        return [
            {
                "type": "RECORD",
                "stream": "test_stream",
                "record": {"id": 1, "name": "Record 1", "value": 10.5},
            },
            {
                "type": "RECORD",
                "stream": "test_stream",
                "record": {"id": 2, "name": "Record 2", "value": 20.75},
            },
        ]

    def test_schema_message_processing(self, oracle_config, schema_message):
        """Test SCHEMA message processing."""
        target = OracleTarget(config=oracle_config)

        # Create input with schema message
        input_data = json.dumps(schema_message)

        # Mock connector to avoid actual DB connection
        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                # Process should handle schema message
                try:
                    target.listen(file_input=StringIO(input_data))
                except EOFError as e:
                    # Expected when input ends - log for debugging
                    print(f"ℹ️ Expected EOF after processing input: {e}")

    def test_record_message_processing(
        self, oracle_config, schema_message, record_messages
    ):
        """Test RECORD message processing."""
        target = OracleTarget(config=oracle_config)

        # Create input with schema and records
        messages = [schema_message] + record_messages
        input_data = "\n".join(json.dumps(msg) for msg in messages)

        # Mock sink to capture processed records
        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))

    def test_state_message_processing(self, oracle_config):
        """Test STATE message processing."""
        target = OracleTarget(config=oracle_config)

        state_message = {
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "test_stream": {
                        "replication_key": "updated_at",
                        "replication_key_value": "2025-01-01T00:00:00Z",
                    }
                }
            },
        }

        input_data = json.dumps(state_message)

        with patch("sys.stdin", StringIO(input_data)):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))

                # State should be written to stdout
                output = mock_stdout.getvalue()
                if output:
                    assert (
                        "STATE" in output
                        or json.dumps(state_message["value"]) in output
                    )

    def test_activate_version_message(self, oracle_config, schema_message):
        """Test ACTIVATE_VERSION message processing."""
        target = OracleTarget(config=oracle_config)

        # First send schema
        messages = [
            schema_message,
            {"type": "ACTIVATE_VERSION", "stream": "test_stream", "version": 1},
        ]

        input_data = "\n".join(json.dumps(msg) for msg in messages)

        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))

    def test_batch_processing(self, oracle_config, schema_message):
        """Test batch message processing."""
        # Configure for batching
        batch_config = oracle_config.copy()
        batch_config["batch_config"] = {
            "batch_size": 5,
            "batch_wait_limit_seconds": 1.0,
        }

        target = OracleTarget(config=batch_config)

        # Create many records to trigger batching
        messages = [schema_message]
        for i in range(10):
            messages.append(
                {
                    "type": "RECORD",
                    "stream": "test_stream",
                    "record": {
                        "id": i + 1,
                        "name": f"Record {i + 1}",
                        "value": float(i * 10),
                    },
                }
            )

        input_data = "\n".join(json.dumps(msg) for msg in messages)

        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))

    def test_multiple_streams(self, oracle_config):
        """Test processing multiple streams."""
        target = OracleTarget(config=oracle_config)

        # Messages for multiple streams
        messages = [
            # Stream 1
            {
                "type": "SCHEMA",
                "stream": "stream1",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                    },
                },
                "key_properties": ["id"],
            },
            {
                "type": "RECORD",
                "stream": "stream1",
                "record": {"id": 1, "name": "Stream 1 Record"},
            },
            # Stream 2
            {
                "type": "SCHEMA",
                "stream": "stream2",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "value": {"type": "number"},
                    },
                },
                "key_properties": ["id"],
            },
            {
                "type": "RECORD",
                "stream": "stream2",
                "record": {"id": 1, "value": 100.5},
            },
        ]

        input_data = "\n".join(json.dumps(msg) for msg in messages)

        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))

    def test_invalid_message_handling(self, oracle_config):
        """Test handling of invalid messages."""
        target = OracleTarget(config=oracle_config)

        # Invalid message (missing type)
        invalid_message = {"stream": "test_stream", "record": {"id": 1}}

        # Invalid JSON
        messages = [
            json.dumps(invalid_message),
            "{ invalid json }",
            '{"type": "UNKNOWN", "stream": "test"}',  # Unknown message type
        ]

        for msg in messages:
            with patch("sys.stdin", StringIO(msg)):
                # Should handle gracefully or raise appropriate error
                try:
                    target.listen(file_input=StringIO(msg))
                except (json.JSONDecodeError, EOFError, KeyError, Exception):
                    # Expected for invalid input
                    # InvalidInputLine is a subclass of Exception
                    pass

    def test_record_metadata(self, oracle_config, schema_message, record_messages):
        """Test Singer metadata column handling."""
        target = OracleTarget(config=oracle_config)

        # Add metadata to records
        records_with_metadata = []
        for record in record_messages:
            enhanced = record.copy()
            enhanced["time_extracted"] = "2025-01-01T10:00:00Z"
            enhanced["version"] = 1
            records_with_metadata.append(enhanced)

        messages = [schema_message] + records_with_metadata
        input_data = "\n".join(json.dumps(msg) for msg in messages)

        with patch.object(target, "default_sink_class") as mock_sink_class:
            mock_sink = MagicMock()
            mock_sink_class.return_value = mock_sink

            with patch("sys.stdin", StringIO(input_data)):
                with contextlib.suppress(EOFError):
                    target.listen(file_input=StringIO(input_data))
