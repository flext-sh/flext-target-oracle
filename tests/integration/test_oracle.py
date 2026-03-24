"""Integration tests for Oracle Target with real database.

These tests require a running Oracle database container and test
actual database operations including DDL, DML, and bulk operations.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence

import pytest
from pydantic import TypeAdapter
from sqlalchemy import text
from sqlalchemy.engine import Engine

from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleLoader,
    FlextTargetOracleSettings,
    m,
)
from tests import c, t


def _schema_parts(
    message: Mapping[str, t.NormalizedValue],
) -> tuple[Mapping[str, t.Container], Sequence[str]]:
    schema_message = m.TargetOracle.SingerSchemaMessage.model_validate(message)
    return (schema_message.schema_definition, schema_message.key_properties)


@pytest.mark.integration
@pytest.mark.oracle
class TestOracleIntegration:
    """Integration tests with real Oracle database."""

    @pytest.mark.usefixtures("_clean_database")
    def test_create_simple_table(
        self,
        connected_loader: FlextTargetOracleLoader,
        oracle_engine: Engine,
        simple_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test creating a simple table with basic data types."""
        stream_name = "test_users"
        schema_dict, key_props = _schema_parts(simple_schema)
        table_res = connected_loader.ensure_table_exists(
            stream_name, schema_dict, key_props
        )
        assert table_res.is_success
        with oracle_engine.connect() as conn:
            cursor = conn.execute(
                text(
                    "\n                    SELECT COUNT(*)\n                    FROM user_tables\n                    WHERE table_name = :table_name\n                    "
                ),
                {"table_name": "TEST_USERS"},
            )
            assert cursor.scalar() == 1
            cursor = conn.execute(
                text(
                    "\n                    SELECT column_name, data_type\n                    FROM user_tab_columns\n                    WHERE table_name = :table_name\n                    ORDER BY column_id\n                    "
                ),
                {"table_name": "TEST_USERS"},
            )
            columns = {row[0]: row[1] for row in cursor}
        assert "ID" in columns
        assert "NAME" in columns
        assert "EMAIL" in columns
        assert "_SDC_EXTRACTED_AT" in columns
        assert "_SDC_LOADED_AT" in columns

    @pytest.mark.usefixtures("_clean_database")
    def test_insert_and_retrieve_data(
        self,
        connected_loader: FlextTargetOracleLoader,
        oracle_engine: Engine,
        simple_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test inserting data and retrieving it."""
        stream_name = "test_insert"
        schema_dict, key_props = _schema_parts(simple_schema)
        create_res = connected_loader.ensure_table_exists(
            stream_name, schema_dict, key_props
        )
        assert create_res.is_success
        records: Sequence[t.ScalarMapping] = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
        result = connected_loader.insert_records(stream_name, records)
        assert result.is_success
        with oracle_engine.connect() as conn:
            cursor = conn.execute(
                text("SELECT id, name, email FROM test_insert ORDER BY id")
            )
            rows = list(cursor)
            assert len(rows) == 2
            assert rows[0] == (1, "John Doe", "john@example.com")
            assert rows[1] == (2, "Jane Smith", "jane@example.com")

    @pytest.mark.usefixtures("_clean_database")
    def test_merge_mode_updates(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        simple_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test merge mode for updating existing records."""
        oracle_config = oracle_config.model_copy(update={"sdc_mode": "merge"})
        loader = FlextTargetOracleLoader(oracle_config)
        connect_result = loader.connect()
        assert connect_result.is_success
        stream_name = "test_merge"
        schema_dict, key_props = _schema_parts(simple_schema)
        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert table_res.is_success
        initial_records: Sequence[t.ScalarMapping] = [
            {"id": 1, "name": "Original Name", "email": "original@example.com"}
        ]
        insert_result = loader.insert_records(stream_name, initial_records)
        assert insert_result.is_success
        updated_records: Sequence[t.ScalarMapping] = [
            {"id": 1, "name": "Updated Name", "email": "updated@example.com"}
        ]
        result = loader.insert_records(stream_name, updated_records)
        assert result.is_success
        with oracle_engine.connect() as conn:
            cursor_result = conn.execute(
                text("SELECT name, email FROM test_merge WHERE id = 1")
            )
            row = cursor_result.fetchone()
            assert row is not None
            assert row[0] == "Updated Name"
            assert row[1] == "updated@example.com"
        disconnect_result = loader.disconnect()
        assert disconnect_result.is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_bulk_insert_performance(
        self, oracle_config: FlextTargetOracleSettings, oracle_engine: Engine
    ) -> None:
        """Test bulk insert with large dataset."""
        oracle_config = oracle_config.model_copy(
            update={"load_method": c.LoadMethod.BULK_INSERT, "batch_size": 1000}
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_bulk"
        schema_message = {
            "type": "SCHEMA",
            "stream": stream_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                    "value": {"type": "number"},
                },
            },
            "key_properties": ["id"],
        }
        schema_dict, key_props = _schema_parts(schema_message)
        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert table_res.is_success
        records: Sequence[t.ScalarMapping] = [
            {"id": i, "data": f"Bulk test data {i}", "value": i * 1.5}
            for i in range(5000)
        ]
        start_time = time.time()
        result = loader.insert_records(stream_name, records)
        elapsed = time.time() - start_time
        assert result.is_success
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_bulk")).scalar()
            assert count == 5000
        assert elapsed < 10.0
        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_json_storage_mode(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        nested_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test JSON storage mode with nested data."""
        oracle_config = oracle_config.model_copy(update={})
        oracle_config = oracle_config.model_copy(
            update={"storage_mode": "json", "json_column_name": "json_data"}
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_json"
        schema_dict, key_props = _schema_parts(nested_schema)
        create_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert create_res.is_success
        record = {
            "id": 1,
            "customer": {
                "id": 100,
                "name": "Acme Corp",
                "address": {
                    "street": "123 Main St",
                    "city": "objecttown",
                    "zip": "12345",
                },
            },
            "items": [
                {"product_id": 1, "quantity": 2, "price": 99.99},
                {"product_id": 2, "quantity": 1, "price": 149.99},
            ],
            "total": 349.97,
        }
        typed_record = TypeAdapter(dict[str, t.Scalar]).validate_python(record)
        insert_res = loader.insert_records(stream_name, [typed_record])
        assert insert_res.is_success
        with oracle_engine.connect() as conn:
            result = conn.execute(text("SELECT json_data FROM test_json WHERE id = 1"))
            json_str = result.scalar()
            assert json_str is not None
            stored_data = TypeAdapter(dict[str, t.Container]).validate_json(json_str)
            customer = stored_data.get("customer")
            customer_data = TypeAdapter(dict[str, t.Container]).validate_python(
                customer
            )
            customer_name = customer_data.get("name")
            assert customer_name == "Acme Corp"
            customer_address = customer_data.get("address")
            customer_address_data = TypeAdapter(dict[str, t.Container]).validate_python(
                customer_address
            )
            customer_city = customer_address_data.get("city")
            assert customer_city == "objecttown"
            items = stored_data.get("items")
            items_data = TypeAdapter(list[dict[str, t.Container]]).validate_python(
                items
            )
            assert len(items_data) == 2
        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_column_ordering(
        self, oracle_config: FlextTargetOracleSettings, oracle_engine: Engine
    ) -> None:
        """Test column ordering in created tables."""
        oracle_config = oracle_config.model_copy(
            update={
                "column_ordering": "alphabetical",
                "column_order_rules": {
                    "primary_keys": 1,
                    "regular_columns": 2,
                    "audit_columns": 3,
                    "sdc_columns": 4,
                },
            }
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_ordering"
        schema_message = {
            "type": "SCHEMA",
            "stream": stream_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "zebra_field": {"type": "string"},
                    "alpha_field": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }
        schema_dict, key_props = _schema_parts(schema_message)
        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert table_res.is_success
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    "\n                  SELECT column_name, column_id\n                  FROM user_tab_columns\n                  WHERE table_name = :table_name\n                  ORDER BY column_id\n                  "
                ),
                {"table_name": "TEST_ORDERING"},
            )
            columns = [row[0] for row in result]
            assert columns[0] == "ID"
            regular_start = 1
            assert columns[regular_start] == "ALPHA_FIELD"
            assert columns[regular_start + 1] == "ZEBRA_FIELD"
            audit_cols = [c for c in columns if c in {"CREATED_AT", "UPDATED_AT"}]
            assert len(audit_cols) == 2
            sdc_cols = [c for c in columns if c.startswith("_SDC_")]
            assert all(
                columns.index(sdc) > columns.index("UPDATED_AT") for sdc in sdc_cols
            )
        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_truncate_before_load(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        simple_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test truncate table before loading data."""
        oracle_config = oracle_config.model_copy(update={"truncate_before_load": True})
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_truncate"
        schema_dict, key_props = _schema_parts(simple_schema)
        create_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert create_res.is_success
        insert_initial = loader.insert_records(
            stream_name, [{"id": 1, "name": "Initial"}]
        )
        assert insert_initial.is_success
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_truncate")).scalar()
            assert count == 1
        loader.ensure_table_exists(stream_name, schema_dict, key_props)
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_truncate")).scalar()
            assert count == 0
        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_custom_indexes(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        simple_schema: Mapping[str, t.NormalizedValue],
    ) -> None:
        """Test creation of custom indexes."""
        oracle_config = oracle_config.model_copy(
            update={
                "custom_indexes": {
                    "test_indexes": [
                        {
                            "name": "IDX_EMAIL_UNIQUE",
                            "columns": ["EMAIL"],
                            "unique": True,
                        },
                        {"columns": ["NAME", "CREATED_AT"]},
                    ]
                }
            }
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_indexes"
        schema_dict, key_props = _schema_parts(simple_schema)
        loader.ensure_table_exists(stream_name, schema_dict, key_props)
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    "\n                  SELECT index_name, uniqueness\n                  FROM user_indexes\n                  WHERE table_name = :table_name\n                  "
                ),
                {"table_name": "TEST_INDEXES"},
            )
            indexes = {row[0]: row[1] for row in result}
            assert "IDX_EMAIL_UNIQUE" in indexes
            assert indexes["IDX_EMAIL_UNIQUE"] == "UNIQUE"
            composite_indexes = [idx for idx in indexes if "NAME" in idx]
            assert len(composite_indexes) > 0
        assert loader.disconnect().is_success


@pytest.mark.integration
@pytest.mark.oracle
class TestOracleTargetE2E:
    """End-to-end tests using the full FlextTargetOracle."""

    @pytest.mark.usefixtures("_clean_database")
    def test_full_singer_workflow(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        singer_messages: Sequence[Mapping[str, t.NormalizedValue]],
    ) -> None:
        """Test complete Singer workflow: schema -> records -> state."""
        target = FlextTargetOracle(config=oracle_config)
        init_result = target.initialize()
        assert init_result.is_success
        for message in singer_messages:
            result = target.execute(
                TypeAdapter(object).dump_json(message).decode("utf-8")
            )
            assert result.is_success
        with oracle_engine.connect() as conn:
            table_count = conn.execute(
                text(
                    "\n                  SELECT COUNT(*)\n                  FROM user_tables\n                  WHERE table_name = 'USERS'\n                  "
                )
            ).scalar()
            assert table_count == 1
            data_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
            assert data_count is not None
            assert data_count > 0

    @pytest.mark.usefixtures("_clean_database")
    def test_column_mapping_and_filtering(
        self, oracle_config: FlextTargetOracleSettings, oracle_engine: Engine
    ) -> None:
        """Test column mapping and filtering features."""
        oracle_config = oracle_config.model_copy(
            update={
                "column_mappings": {
                    "users": {"name": "full_name", "email": "email_address"}
                },
                "ignored_columns": ["password", "internal_id"],
            }
        )
        target = FlextTargetOracle(config=oracle_config)
        target.initialize()
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "internal_id": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }
        target.execute(TypeAdapter(object).dump_json(schema_msg).decode("utf-8"))
        record_msg = {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "password": "secret123",
                "internal_id": "INT-001",
            },
        }
        target.execute(TypeAdapter(object).dump_json(record_msg).decode("utf-8"))
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    "\n                  SELECT column_name\n                  FROM user_tab_columns\n                  WHERE table_name = 'USERS'\n                  "
                )
            )
            columns = [row[0] for row in result]
            assert "FULL_NAME" in columns
            assert "EMAIL_ADDRESS" in columns
            assert "PASSWORD" not in columns
            assert "INTERNAL_ID" not in columns
            result = conn.execute(
                text("SELECT full_name, email_address FROM users WHERE id = 1")
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == "John Doe"
            assert row[1] == "john@example.com"
