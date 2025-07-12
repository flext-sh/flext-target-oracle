# Copyright (c) 2025 FLEXT Team
# Licensed under the MIT License
# SPDX-License-Identifier: MIT

"""Integration tests for Oracle Target.

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest
from flext_target_oracle.sinks import OracleSink
from flext_target_oracle.target import OracleTarget
from sqlalchemy.pool import QueuePool


class TestOracleTargetIntegration:  """Integration tests for Oracle Target."""

    @staticmethod
    @pytest.fixture
    def basic_config() -> Any: return {
            "host": "localhost",
            "port": 1521,
            "username": "test_user",
            "password": "test_pass",
            "service_name": "ORCL",
            "default_target_schema": "TEST",
            "add_record_metadata": True,
        }

    @staticmethod
    @pytest.fixture
    def singer_schema() -> Any: return {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string", "maxLength": 100},
                "email": {"type": "string", "maxLength": 255},
                "active": {"type": "boolean"},
                "amount": {"type": "number"},
                "created_at": {"type": "string", "format": "date-time"},
            },
        }

    @staticmethod
    @pytest.fixture
    def sample_records() -> Any: return [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "active": True,
                "amount": 100.50,
                "created_at": "2024-01-01T10:00:00Z",
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "active": False,
                "amount": 250.75,
                "created_at": "2024-01-02T11:00:00Z",
            },
        ]

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_target_initialization(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
    ) -> None: # Mock engines
        mock_engine = Mock()
        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        target = OracleTarget(config=basic_config)

        assert target.name == "flext-target-oracle"
        assert target.config["host"] == "localhost"
        assert target.config["default_target_schema"] == "TEST"

        # Verify engine creation
        mock_sync_engine.assert_called_once()
        call_kwargs = mock_sync_engine.call_args[1]
        assert call_kwargs["poolclass"] == QueuePool
        assert call_kwargs["pool_size"] == 10  # Default
        assert call_kwargs["future"] is True  # SQLAlchemy 2.0

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_sink_creation(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
        singer_schema: Any,
    ) -> None: mock_engine = Mock()
        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        target = OracleTarget(config=basic_config)

        # Get sink
        sink = target.get_sink(
            stream_name="customers",
            schema=singer_schema,
            key_properties=["id"],
        )

        assert isinstance(sink, OracleSink)
        assert sink.stream_name == "customers"
        assert sink.key_properties == ["id"]

    @patch("flext_target_oracle.sinks.create_engine")
    @staticmethod
    def test_end_to_end_data_flow(
        mock_create_engine: Any,
        basic_config: Any,
        singer_schema: Any,
        sample_records: Any,
    ) -> None: # Mock database engine and connection
        mock_engine = Mock()
        mock_conn = MagicMock()
        mock_trans = MagicMock()

        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_conn.begin.return_value.__enter__.return_value = mock_trans
        mock_create_engine.return_value = mock_engine

        # Mock table
        mock_table = Mock()
        mock_table.name = "CUSTOMERS"
        mock_table.schema = "TEST"

        # Create target
        with (: patch("flext_target_oracle.target.create_engine") as mock_target_engine,
            patch("flext_target_oracle.target.create_async_engine"),
        ): mock_target_engine.return_value = mock_engine
            target = OracleTarget(config=basic_config)

            # Create sink
            sink = target.get_sink(
                stream_name="customers",
                schema=singer_schema,
                key_properties=["id"],
            )

            # Mock the table - using setattr to avoid mypy error
            sink._table = mock_table

            # Process records
            for record in sample_records: sink.process_record(record, {})

            # Process batch
            sink.process_batch({})

            # Verify database operations
            assert mock_conn.execute.called

            # Check that records were prepared with audit fields
            call_args = mock_conn.execute.call_args[0][1]
            assert len(call_args) == 2  # Two records
            for record in call_args:
                assert "CREATE_TS" in record
                assert "MOD_TS" in record
                assert record["CREATE_USER"] == "SINGER"

    @staticmethod
    def test_sql_type_mapping(basic_config: Any) -> None:
            from flext_target_oracle.connectors import (  # TODO: Move import to module level
            OracleConnector,
        )

        connector = OracleConnector(basic_config)

        # Test various type mappings
        test_cases = [
            ({"type": "integer"}, "NUMBER(precision=38, scale=0)"),
            ({"type": "number"}, "NUMBER"),
            ({"type": "boolean"}, "NUMBER(precision=1, scale=0)"),
            ({"type": "string", "maxLength": 100}, "VARCHAR2(length=100)"),
            ({"type": "string", "maxLength": 5000}, "CLOB"),
            ({"type": "string", "format": "date-time"}, "TIMESTAMP(timezone=True)"),
            ({"type": "array"}, "CLOB"),
            ({"type": "object"}, "CLOB"),
        ]

        for schema, expected_type in test_cases: sql_type = connector.to_sql_type(schema)  # type: ignore[arg-type]
            assert str(sql_type) == expected_type

    @staticmethod
    def test_column_pattern_recognition(basic_config: Any) -> None:
            from flext_target_oracle.connectors import (  # TODO: Move import to module level
            OracleConnector,
        )

        config = basic_config.copy()
        config["enable_column_patterns"] = True
        connector = OracleConnector(config)

        # Test pattern recognition
        test_cases = [
            ("user_id", {"type": "integer"}, "NUMBER(precision=38, scale=0)"),
            ("active_flg", {"type": "string"}, "NUMBER(precision=1, scale=0)"),
            ("created_ts", {"type": "string"}, "TIMESTAMP(timezone=True)"),
            ("total_amount", {"type": "number"}, "NUMBER(precision=19, scale=4)"),
            ("order_qty", {"type": "number"}, "NUMBER(precision=19, scale=4)"),
            ("discount_pct", {"type": "number"}, "NUMBER(precision=5, scale=2)"),
        ]

        for column_name, schema, expected_type in test_cases: sql_type = connector.get_column_type(column_name, schema)  # type: ignore[attr-defined]
            assert str(sql_type) == expected_type

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_bulk_operations(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
    ) -> None: mock_engine = Mock()
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        # Large batch of records
        large_batch = [{"id": i, "name": f"User {i}"} for i in range(1000)]

        target = OracleTarget(config=basic_config)
        sink = target.get_sink(
            stream_name="users",
            schema={
                "type":  "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
            key_properties=["id"],
        )

        # Mock table
        sink._table = Mock()
        sink.connector = Mock()
        sink.connector._engine = mock_engine  # type: ignore[attr-defined]

        # Process large batch
        if hasattr(sink, "_process_batch_append"): sink._process_batch_append(large_batch)

        # Verify bulk insert was used
        mock_conn.execute.assert_called_once()

        # Check batch size
        call_args = mock_conn.execute.call_args[0][1]
        assert len(call_args) == 1000

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_upsert_operations(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
    ) -> None: mock_engine = Mock()
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        config = basic_config.copy()
        config["load_method"] = "upsert"

        target = OracleTarget(config=config)
        sink = target.get_sink(
            stream_name="customers",
            schema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            key_properties=["id"],
        )

        # Mock table
        mock_table = Mock()
        mock_table.name = "CUSTOMERS"
        mock_table.schema = "TEST"
        sink._table = mock_table
        sink.connector = Mock()
        sink.connector._engine = mock_engine  # type: ignore[attr-defined]

        # Process upsert
        records = [
            {"id": 1, "name": "John Updated", "email": "john.new@example.com"},
            {"id": 3, "name": "New User", "email": "new@example.com"},
        ]

        if hasattr(sink, "_process_batch_upsert"): sink._process_batch_upsert(records)

        # Verify MERGE was executed
        assert mock_conn.execute.called
        # Should execute one MERGE per record
        assert mock_conn.execute.call_count == 2

        # Check that MERGE statement was used
        call_args = mock_conn.execute.call_args_list[0][0][0]
        assert hasattr(call_args, "text")  # SQLAlchemy text object

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_parallel_processing(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
    ) -> None: mock_engine = Mock()
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        config = basic_config.copy()
        config["parallel_threads"] = 4

        target = OracleTarget(config=config)
        sink = target.get_sink(
            stream_name="large_table",
            schema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
            },
            key_properties=["id"],
        )

        # Mock table and connector
        sink._table = Mock()
        sink.connector = Mock()
        sink.connector._engine = mock_engine  # type: ignore[attr-defined]

        # Large batch that should trigger parallel processing
        large_batch = [{"id": i} for i in range(5000)]

        # Mock ThreadPoolExecutor
        with patch("flext_target_oracle.sinks.ThreadPoolExecutor") as mock_executor: mock_pool = Mock()
            mock_executor.return_value = mock_pool

            # Re-initialize sink to get mocked executor
            sink.__init__(  # type: ignore[misc]
                target=target,
                stream_name="large_table",
                schema=sink.schema,
                key_properties=["id"],
            )
            sink._table = Mock()
            sink.connector = Mock()
            sink.connector._engine = mock_engine  # type: ignore[attr-defined]

            if hasattr(sink, "_process_batch_append"): sink._process_batch_append(large_batch)

            # Verify parallel execution was used
            assert mock_executor.called
            assert mock_executor.call_args[1]["max_workers"] == 4

    @staticmethod
    def test_audit_fields(basic_config: Any) -> None:
            from flext_target_oracle.sinks import (  # TODO: Move import to module level
            OracleSink,
        )

        target = Mock()
        target.config = basic_config

        sink = OracleSink(
            target=target,
            stream_name="test",
            schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            key_properties=["id"],
        )

        # Test record preparation
        records = [{"id": 1, "data": "test"}]
        if hasattr(sink, "_prepare_records"): prepared = sink._prepare_records(records)
        else:
            prepared = {}

        assert len(prepared) == 1
        record = prepared[0]

        # Check audit fields
        assert "CREATE_TS" in record
        assert "MOD_TS" in record
        assert record["CREATE_USER"] == "SINGER"
        assert record["MOD_USER"] == "SINGER"

        # Check timestamps are datetime objects
        assert isinstance(record["CREATE_TS"], datetime)
        assert isinstance(record["MOD_TS"], datetime)

    @patch("flext_target_oracle.target.text")
    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_health_check(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        mock_text: Any,
        basic_config: Any,
    ) -> None: # Mock engine with pool
        mock_engine = Mock()
        mock_pool = Mock()
        mock_pool.size.return_value = 10
        mock_pool.checkedout.return_value = 2
        mock_engine.pool = mock_pool

        # Mock connection
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        target = OracleTarget(config=basic_config)

        # Perform health check
        health = target._check_engine_health()  # type: ignore[attr-defined]

        assert health["sync_engine"]["status"] == "healthy"
        assert health["sync_engine"]["pool_size"] == 10
        assert health["sync_engine"]["checked_out"] == 2

        # Verify health check query
        mock_text.assert_called_with("SELECT 1 FROM DUAL")
        mock_conn.execute.assert_called_once()

    @patch("flext_target_oracle.target.create_engine")
    @patch("flext_target_oracle.target.create_async_engine")
    @staticmethod
    def test_error_handling(
        mock_async_engine: Any,
        mock_sync_engine: Any,
        basic_config: Any,
    ) -> None: mock_engine = Mock()
        mock_conn = MagicMock()

        # Simulate connection error
        mock_conn.execute.side_effect = Exception("ORA-12154: TNS could not resolve")
        mock_engine.begin.return_value.__enter__.return_value = mock_conn

        mock_sync_engine.return_value = mock_engine
        mock_async_engine.return_value = Mock()

        target = OracleTarget(config=basic_config)
        sink = target.get_sink(
            stream_name="test",
            schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            key_properties=["id"],
        )

        # Mock table
        sink._table = Mock()
        sink.connector = Mock()
        sink.connector._engine = mock_engine  # type: ignore[attr-defined]

        # Attempt to process batch - should raise
        with pytest.raises(Exception) as exc_info: if hasattr(sink, "_process_batch_append"): sink._process_batch_append([{"id": 1}])

        assert "ORA-12154" in str(exc_info.value)


if __name__ == "__main__": pytest.main([__file__, "-v"])
