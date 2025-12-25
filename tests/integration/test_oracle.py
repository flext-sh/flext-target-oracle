"""Integration tests for Oracle Target with real database.

These tests require a running Oracle database container and test
actual database operations including DDL, DML, and bulk operations.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import json
import time
from typing import cast

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine



    FlextTargetOracle,
    FlextTargetOracleLoader,
    FlextTargetOracleSettings,
    LoadMethod,
)


@pytest.mark.integration
@pytest.mark.oracle
class TestOracleIntegration:
    """Integration tests with real Oracle database."""

    @pytest.mark.usefixtures("_clean_database")
    def test_create_simple_table(
        self,
        connected_loader: FlextTargetOracleLoader,
        oracle_engine: Engine,
        simple_schema: dict[str, object],
    ) -> None:
        """Test creating a simple table with basic data types."""
        stream_name = "test_users"
        schema = simple_schema["schema"]
        key_properties = simple_schema["key_properties"]

        # Ensure table is created (synchronous API returning FlextResult)
        schema_dict = cast("dict[str, object]", schema)
        key_props = cast("list[str] | None", key_properties)

        table_res = connected_loader.ensure_table_exists(
            stream_name,
            schema_dict,
            key_props,
        )
        assert table_res.is_success

        # Verify table exists in database
        with oracle_engine.connect() as conn:
            cursor = conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM user_tables
                    WHERE table_name = :table_name
                    """,
                ),
                {"table_name": "TEST_USERS"},
            )
            assert cursor.scalar() == 1

            # Verify columns
            cursor = conn.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM user_tab_columns
                    WHERE table_name = :table_name
                    ORDER BY column_id
                    """,
                ),
                {"table_name": "TEST_USERS"},
            )
            columns = {row[0]: row[1] for row in cursor}

        # Should have schema columns + SDC columns
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
        simple_schema: dict[str, object],
    ) -> None:
        """Test inserting data and retrieving it."""
        stream_name = "test_insert"
        schema = simple_schema["schema"]
        key_properties = simple_schema["key_properties"]

        schema = cast("dict[str, object]", schema)
        key_properties = cast("list[str] | None", key_properties)

        # Create table
        create_res = connected_loader.ensure_table_exists(
            stream_name,
            schema,
            key_properties,
        )
        assert create_res.is_success

        # Insert records
        records = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]

        result = connected_loader.insert_records(stream_name, records)
        assert result.is_success

        # Verify data in database
        with oracle_engine.connect() as conn:
            cursor = conn.execute(
                text("SELECT id, name, email FROM test_insert ORDER BY id"),
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
        simple_schema: dict[str, object],
    ) -> None:
        """Test merge mode for updating existing records."""
        # Pydantic models are value objects; use model_copy to produce a mutable copy
        oracle_config = oracle_config.model_copy(update={"sdc_mode": "merge"})
        loader = FlextTargetOracleLoader(oracle_config)

        # synchronous connect via underlying API - call directly
        connect_result = loader.connect()
        assert connect_result.is_success

        stream_name = "test_merge"
        schema = simple_schema["schema"]
        key_properties = simple_schema["key_properties"]
        schema = cast("dict[str, object]", schema)
        key_properties = cast("list[str] | None", key_properties)

        # Create table and insert initial data
        table_res = loader.ensure_table_exists(stream_name, schema, key_properties)
        assert table_res.is_success

        initial_records = [
            {"id": 1, "name": "Original Name", "email": "original@example.com"},
        ]
        insert_result = loader.insert_records(stream_name, initial_records)
        assert insert_result.is_success

        # Update the record
        updated_records = [
            {"id": 1, "name": "Updated Name", "email": "updated@example.com"},
        ]
        result = loader.insert_records(stream_name, updated_records)
        assert result.is_success

        # Verify update
        with oracle_engine.connect() as conn:
            cursor_result = conn.execute(
                text("SELECT name, email FROM test_merge WHERE id = 1"),
            )
            row = cursor_result.fetchone()
            assert row is not None
            assert row[0] == "Updated Name"
            assert row[1] == "updated@example.com"

        disconnect_result = loader.disconnect()
        assert disconnect_result.is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_bulk_insert_performance(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
    ) -> None:
        """Test bulk insert with large dataset."""
        # Use a copy of the config to avoid mutating a shared fixture
        oracle_config = oracle_config.model_copy(
            update={"load_method": LoadMethod.BULK_INSERT, "batch_size": 1000},
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success

        stream_name = "test_bulk"
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "data": {"type": "string"},
                "value": {"type": "number"},
            },
        }
        key_properties = ["id"]

        # Create table
        schema_dict = cast("dict[str, object]", schema)
        key_props = cast("list[str] | None", key_properties)
        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert table_res.is_success

        # Generate large dataset
        records = [
            {
                "id": i,
                "data": f"Bulk test data {i}",
                "value": i * 1.5,
            }
            for i in range(5000)
        ]

        # Measure bulk insert performance
        start_time = time.time()
        result = loader.insert_records(stream_name, records)
        elapsed = time.time() - start_time
        assert result.is_success

        # Verify all records inserted
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_bulk")).scalar()
            assert count == 5000

        # Performance assertion (should be fast with bulk)
        assert elapsed < 10.0  # Should complete within 10 seconds

        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_json_storage_mode(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        nested_schema: dict[str, object],
    ) -> None:
        """Test JSON storage mode with nested data."""
        oracle_config = oracle_config.model_copy(update={})
        # storage_mode and json_column_name are defined on the config; use model_copy
        oracle_config = oracle_config.model_copy(
            update={"storage_mode": "json", "json_column_name": "json_data"},
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success

        stream_name = "test_json"
        schema = nested_schema["schema"]
        key_properties = nested_schema["key_properties"]
        schema = cast("dict[str, object]", schema)
        key_properties = cast("list[str] | None", key_properties)

        # Create table
        create_res = loader.ensure_table_exists(stream_name, schema, key_properties)
        assert create_res.is_success

        # Insert nested record
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
        insert_res = loader.insert_records(stream_name, [record])
        assert insert_res.is_success

        # Verify JSON data
        with oracle_engine.connect() as conn:
            result = conn.execute(text("SELECT json_data FROM test_json WHERE id = 1"))
            json_str = result.scalar()
            # guard against None
            assert json_str is not None
            stored_data = json.loads(json_str)

            assert stored_data["customer"]["name"] == "Acme Corp"
            assert stored_data["customer"]["address"]["city"] == "objecttown"
            assert len(stored_data["items"]) == 2

        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_column_ordering(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
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
            },
        )
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success

        stream_name = "test_ordering"
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "zebra_field": {"type": "string"},
                "alpha_field": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        }
        key_properties = ["id"]

        # ensure types match expected signatures
        schema_dict = cast("dict[str, object]", schema)
        key_props = cast("list[str] | None", key_properties)

        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        assert table_res.is_success

        # Check column order
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                  SELECT column_name, column_id
                  FROM user_tab_columns
                  WHERE table_name = :table_name
                  ORDER BY column_id
                  """,
                ),
                {"table_name": "TEST_ORDERING"},
            )

            columns = [row[0] for row in result]

            # Primary key should be first
            assert columns[0] == "ID"

            # Regular columns alphabetically
            regular_start = 1
            assert columns[regular_start] == "ALPHA_FIELD"
            assert columns[regular_start + 1] == "ZEBRA_FIELD"

            # Audit columns
            audit_cols = [c for c in columns if c in {"CREATED_AT", "UPDATED_AT"}]
            assert len(audit_cols) == 2

            # SDC columns at the end
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
        simple_schema: dict[str, object],
    ) -> None:
        """Test truncate table before loading data."""
        oracle_config = oracle_config.model_copy(update={"truncate_before_load": True})
        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_truncate"
        schema = simple_schema["schema"]
        key_properties = simple_schema["key_properties"]
        schema = cast("dict[str, object]", schema)
        key_properties = cast("list[str] | None", key_properties)

        # Create table and insert initial data
        create_res = loader.ensure_table_exists(stream_name, schema, key_properties)
        assert create_res.is_success
        insert_initial = loader.insert_records(
            stream_name,
            [{"id": 1, "name": "Initial"}],
        )
        assert insert_initial.is_success

        # Verify initial data exists
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_truncate")).scalar()
            assert count == 1

        # Run ensure_table_exists again with truncate enabled
        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Table should be empty
        with oracle_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM test_truncate")).scalar()
            assert count == 0

        assert loader.disconnect().is_success

    @pytest.mark.usefixtures("_clean_database")
    def test_custom_indexes(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
        simple_schema: dict[str, object],
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
                    ],
                },
            },
        )

        loader = FlextTargetOracleLoader(oracle_config)
        assert loader.connect().is_success
        stream_name = "test_indexes"
        schema = simple_schema["schema"]
        key_properties = simple_schema["key_properties"]
        schema = cast("dict[str, object]", schema)
        key_properties = cast("list[str] | None", key_properties)

        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Verify indexes created
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                  SELECT index_name, uniqueness
                  FROM user_indexes
                  WHERE table_name = :table_name
                  """,
                ),
                {"table_name": "TEST_INDEXES"},
            )

            indexes = {row[0]: row[1] for row in result}

            # Should have unique email index
            assert "IDX_EMAIL_UNIQUE" in indexes
            assert indexes["IDX_EMAIL_UNIQUE"] == "UNIQUE"

            # Should have composite index (auto-named)
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
        singer_messages: list[dict[str, object]],
    ) -> None:
        """Test complete Singer workflow: schema -> records -> state."""
        target = FlextTargetOracle(config=oracle_config)

        # Initialize target
        init_result = target.initialize()
        assert init_result.is_success

        # Process messages
        for message in singer_messages:
            result = target.execute(json.dumps(message))
            assert result.is_success

        # Verify data in database
        with oracle_engine.connect() as conn:
            # Check table exists
            table_count = conn.execute(
                text(
                    """
                  SELECT COUNT(*)
                  FROM user_tables
                  WHERE table_name = 'USERS'
                  """,
                ),
            ).scalar()
            assert table_count == 1

            # Check data inserted
            data_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
            assert data_count is not None
            assert data_count > 0

    @pytest.mark.usefixtures("_clean_database")
    def test_column_mapping_and_filtering(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: Engine,
    ) -> None:
        """Test column mapping and filtering features."""
        oracle_config = oracle_config.model_copy(
            update={
                "column_mappings": {
                    "users": {"name": "full_name", "email": "email_address"},
                },
                "ignored_columns": ["password", "internal_id"],
            },
        )

        target = FlextTargetOracle(config=oracle_config)
        target.initialize()

        # Process schema with extra columns
        schema_msg = {
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},  # Should be ignored
                    "internal_id": {"type": "string"},  # Should be ignored
                },
            },
            "key_properties": ["id"],
        }

        target.execute(json.dumps(schema_msg))

        # Process record
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

        target.execute(json.dumps(record_msg))

        # Verify column mapping and filtering
        with oracle_engine.connect() as conn:
            # Check columns
            result = conn.execute(
                text(
                    """
                  SELECT column_name
                  FROM user_tab_columns
                  WHERE table_name = 'USERS'
                  """,
                ),
            )
            columns = [row[0] for row in result]

            # Mapped columns should exist
            assert "FULL_NAME" in columns
            assert "EMAIL_ADDRESS" in columns

            # Ignored columns should not exist
            assert "PASSWORD" not in columns
            assert "INTERNAL_ID" not in columns

            # Check data with mapped names
            result = conn.execute(
                text("SELECT full_name, email_address FROM users WHERE id = 1"),
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == "John Doe"
            assert row[1] == "john@example.com"
