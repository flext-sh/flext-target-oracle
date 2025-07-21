# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Test Singer protocol integration.

These tests validate the complete Singer message processing workflow.
"""

from io import StringIO
from unittest.mock import AsyncMock, patch

import pytest

from flext_target_oracle import OracleTarget
from flext_target_oracle.application.services import SingerTargetService


class TestSingerIntegration:
    """Test complete Singer protocol integration."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_schema_message_processing() -> None:
        """Test processing SCHEMA messages."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        schema_message = {
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
            "key_properties": ["id"],
        }

        # Mock the service to avoid database calls
        with patch.object(
            target.target_service,
            "process_singer_message",
            new_callable=AsyncMock,
        ) as mock_process:
            from flext_core import ServiceResult

            mock_process.return_value = ServiceResult.ok(None)

            await target._process_single_message(schema_message, 1)

            assert mock_process.called
            assert mock_process.call_args[0][0] == schema_message

    @staticmethod
    @pytest.mark.asyncio
    async def test_record_message_processing() -> None:
        """Test processing RECORD messages."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        record_message = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
            },
        }

        # Mock the service
        with patch.object(
            target.target_service,
            "process_singer_message",
            new_callable=AsyncMock,
        ) as mock_process:
            from flext_core import ServiceResult

            mock_process.return_value = ServiceResult.ok(None)

            await target._process_single_message(record_message, 1)

            assert mock_process.called
            assert mock_process.call_args[0][0] == record_message

    @staticmethod
    @pytest.mark.asyncio
    async def test_state_message_processing() -> None:
        """Test processing STATE messages."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        state_message = {
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "users": {
                        "replication_key_value": "2023-01-01T00:00:00Z",
                    },
                },
            },
        }

        # Mock the service
        with patch.object(
            target.target_service,
            "process_singer_message",
            new_callable=AsyncMock,
        ) as mock_process:
            from flext_core import ServiceResult

            mock_process.return_value = ServiceResult.ok(None)

            await target._process_single_message(state_message, 1)

            assert mock_process.called
            assert mock_process.call_args[0][0] == state_message

    @staticmethod
    @pytest.mark.asyncio
    async def test_complete_workflow() -> None:
        """Test complete Singer workflow with multiple messages."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        # Simulate a complete Singer session
        messages = [
            {
                "type": "SCHEMA",
                "stream": "users",
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
                "stream": "users",
                "record": {"id": 1, "name": "Alice"},
            },
            {
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 2, "name": "Bob"},
            },
            {
                "type": "STATE",
                "value": {"bookmarks": {"users": {"id": 2}}},
            },
        ]

        # Mock the service
        with patch.object(
            target.target_service,
            "process_singer_message",
            new_callable=AsyncMock,
        ) as mock_process:
            from flext_core import ServiceResult

            mock_process.return_value = ServiceResult.ok(None)

            # Process each message
            for i, message in enumerate(messages):
                result = await target._process_single_message(
                    message,
                    i + 1,
                )
                assert result  # Should succeed

            # Verify all messages were processed
            assert mock_process.call_count == len(messages)


class TestTargetService:
    """Test SingerTargetService functionality."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_service_initialization() -> None:
        """Test service initialization with config."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        assert hasattr(target, "target_service")
        assert isinstance(target.target_service, SingerTargetService)
        assert target.target_service.config == target.config

    @staticmethod
    def test_target_run_sync() -> None:
        """Test synchronous run method."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)

        # Mock stdin and async processing
        with (
            patch("sys.stdin", StringIO("")),
            patch.object(target, "run_async", new_callable=AsyncMock) as mock_run_async,
        ):
            # Mock successful result
            from flext_core import ServiceResult

            mock_run_async.return_value = ServiceResult.ok(None)

            result = target.run()

            assert result == 0  # Success exit code
            mock_run_async.assert_called_once()

    @staticmethod
    def test_target_stop() -> None:
        """Test target stop functionality."""
        config = {
            "host": "test-host",
            "username": "test-user",
            "password": "test-pass",
        }

        target = OracleTarget(config=config)
        target._running = True

        target.stop()

        assert target._running is False
