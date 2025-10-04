"""Real Oracle Loader Tests - Using Docker Oracle Container.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from collections.abc import Callable
from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol

import pytest
from flext_core import FlextTypes
from sqlalchemy import Engine, MetaData, Table, func, select, text

from flext_target_oracle import (
    FlextTargetOracleConfig,
    FlextTargetOracleConnectionError,
    FlextTargetOracleLoader,
    FlextTargetOracleSchemaError,
    LoadMethod,
)


class LoaderProtocol(Protocol):
    """Protocol for loader objects in tests."""

    def load_record(self, stream_name: str, record: FlextTypes.Dict) -> None:
        """Load a single record into Oracle."""

    def load_batch(self, stream_name: str, records: list[FlextTypes.Dict]) -> None:
        """Load a batch of records into Oracle."""

    def ensure_table_exists(
        self,
        stream_name: str,
        schema: FlextTypes.Dict,
    ) -> None:
        """Ensure Oracle table exists for the stream."""

    def finalize_streams(self, stream_name: str) -> FlextTypes.Dict:
        """Finalize Oracle streams and return metrics."""


def safe_table_name(name: str) -> str:
    """Create a safe quoted Oracle table name for testing."""
    return f'"{name.upper()}"'


@pytest.mark.oracle
class TestRealOracleLoader:
    """Test Oracle loader with real database connection."""

    @pytest.fixture
    def real_loader(
        self,
        oracle_config: FlextTargetOracleConfig,
        _oracle_engine: Engine,
        _clean_database: None,
    ) -> FlextTargetOracleLoader:
        """Create real loader instance connected to Oracle."""
        loader = FlextTargetOracleLoader(oracle_config)
        result = loader.connect()
        assert result.is_success
        return loader
        # Cleanup is handled by _clean_database fixture

    def test_real_connect_disconnect(
        self,
        oracle_config: FlextTargetOracleConfig,
    ) -> None:
        """Test real connection and disconnection."""
        loader = FlextTargetOracleLoader(oracle_config)

        # Test connect
        result = loader.connect()
        assert result.is_success
        assert loader.oracle_api is not None
        assert loader._connection is not None

        # Test disconnect - loader doesn't have disconnect method, connection cleanup happens automatically

    @pytest.mark.usefixtures("_mock_oracle_loader")
    def test_real_connect_with_invalid_credentials(self) -> None:
        """Test method."""
        """Test connection with invalid credentials."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="invalid_user",
            oracle_password="invalid_pass",
            default_target_schema="TEST",
        )

        loader = FlextTargetOracleLoader(config)
        with pytest.raises(FlextTargetOracleConnectionError) as exc_info:
            loader.connect()

        assert "Failed to establish Oracle connection" in str(exc_info.value)
        assert exc_info.value.host == "localhost"
        assert exc_info.value.port == 1521

    def test_real_ensure_table_exists_new_table(
        self,
        real_loader: LoaderProtocol,
        _simple_schema: FlextTypes.Dict,
        _oracle_engine: Engine,
    ) -> None:
        """Test creating a new table in real Oracle."""
        stream_name = "test_users"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        result = real_loader.ensure_table_exists(
            stream_name,
            schema,
            key_properties,
        )
        assert result.is_success

        # Verify table exists in database
        with real_loader._connection.connect() as conn:
            result = conn.execute(
                text(
                    """

                  SELECT COUNT(*)
                  FROM user_tables
                  WHERE table_name = :table_name
                  """,
                ),
                {"table_name": "TEST_USERS"},
            )
            assert result.scalar() == 1

            # Verify columns
            result = conn.execute(
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
            columns = {row[0]: row[1] for row in result}

            # Should have schema columns + SDC columns
            assert "ID" in columns
            assert "NAME" in columns
            assert "EMAIL" in columns
            assert "_SDC_EXTRACTED_AT" in columns
            assert "_SDC_LOADED_AT" in columns

    def test_real_ensure_table_exists_existing_table(
        self,
        real_loader: LoaderProtocol,
        _simple_schema: FlextTypes.Dict,
        _oracle_engine: Engine,
    ) -> None:
        """Test handling existing table in real Oracle."""
        stream_name = "existing_table"

        # Create table first
        with _oracle_engine.connect() as conn:
            table_name = safe_table_name(stream_name)
            conn.execute(
                text(
                    f"CREATE TABLE {table_name} (id NUMBER PRIMARY KEY, name VARCHAR2(100))",
                ),
            )
            conn.commit()

        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Should handle existing table
        result = real_loader.ensure_table_exists(
            stream_name,
            schema,
            key_properties,
        )
        assert result.is_success

    def test_real_force_recreate_table(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test force recreating table in real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            force_recreate_tables=True,
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "recreate_table"

        # Create table with data first
        with _oracle_engine.connect() as conn:
            # Use quoted identifier for safety in test environment
            safe_table_name = f'"{stream_name.upper()}"'
            conn.execute(
                text(
                    f"CREATE TABLE {safe_table_name} (id NUMBER PRIMARY KEY, old_column VARCHAR2(50))",
                ),
            )
            # Controlled test insert with static values (table name is quoted identifier)
            conn.execute(
                text(
                    "INSERT INTO \"RECREATE_TABLE\" (id, old_column) VALUES (1, 'old_data')",
                ),
            )
            conn.commit()

        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Force recreate
        result = loader.ensure_table_exists(stream_name, schema, key_properties)
        assert result.is_success

        # Verify old data is gone and new structure exists
        with _oracle_engine.connect() as conn:
            # Check no data
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 0

            # Check new columns exist
            result = conn.execute(
                text(
                    """

                  SELECT column_name
                  FROM user_tab_columns
                  WHERE table_name = :table_name
                  """,
                ),
                {"table_name": stream_name.upper()},
            )
            columns = [row[0] for row in result]
            assert "NAME" in columns  # New column from schema
            assert "OLD_COLUMN" not in columns  # Old column gone

    def test_real_truncate_before_load(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test truncating table before load in real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            truncate_before_load=True,
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "truncate_table"

        # Create table with data first
        with _oracle_engine.connect() as conn:
            table_name = safe_table_name(stream_name)
            conn.execute(
                text(
                    f"CREATE TABLE {table_name} (id NUMBER PRIMARY KEY, name VARCHAR2(100))",
                ),
            )
            # Controlled test insert with static values (safe table name computed above)
            conn.execute(
                text(
                    "INSERT INTO \"TRUNCATE_TABLE\" (id, name) VALUES (1, 'existing_data')",
                ),
            )
            conn.commit()

            # Verify data exists
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 1

        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists with truncate
        result = loader.ensure_table_exists(stream_name, schema, key_properties)
        assert result.is_success

        # Verify table is empty
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 0

    def test_real_load_record_single(
        self,
        real_loader: LoaderProtocol,
        _simple_schema: FlextTypes.Dict,
        _oracle_engine: Engine,
    ) -> None:
        """Test loading a single record into real Oracle."""
        stream_name = "load_single"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists
        real_loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load single record
        record = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
        }

        result = real_loader.load_record(stream_name, record, schema)
        assert result.is_success

        # Finalize to flush
        real_loader.finalize_all_streams()

        # Verify in database
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            result = conn.execute(
                select(table.c.ID, table.c.NAME, table.c.EMAIL).where(table.c.ID == 1),
            )
            row = result.fetchone()
            assert row is not None
            assert row[0] == 1
            assert row[1] == "Test User"
            assert row[2] == "test@example.com"

    def test_real_load_record_batch(
        self,
        real_loader: LoaderProtocol,
        _simple_schema: FlextTypes.Dict,
        _oracle_engine: Engine,
    ) -> None:
        """Test loading batch of records into real Oracle."""
        stream_name = "load_batch"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists
        real_loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load batch of records
        for i in range(10):
            record = {
                "id": i + 1,
                "name": f"User {i + 1}",
                "email": f"user{i + 1}@example.com",
            }
            result = real_loader.load_record(stream_name, record, schema)
            assert result.is_success

        # Finalize to flush
        real_loader.finalize_all_streams()

        # Verify in database
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 10

    @pytest.mark.usefixtures("oracle_engine")
    def test_real_bulk_insert_mode(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test bulk insert mode with real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            load_method=LoadMethod.BULK_INSERT,
            batch_size=5,
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "bulk_insert"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists
        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load records - should trigger bulk insert when batch is full
        for i in range(12):  # More than batch size
            record = {
                "id": i + 1,
                "name": f"Bulk User {i + 1}",
                "email": f"bulk{i + 1}@example.com",
            }
            result = loader.load_record(stream_name, record, schema)
            assert result.is_success

        # Finalize to flush remaining
        loader.finalize_all_streams()

        # Verify all records
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 12

    def test_real_merge_mode(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test merge mode (upsert) with real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            sdc_mode="merge",
            load_method=LoadMethod.MERGE,
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "merge_test"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists
        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Insert initial record
        record1 = {
            "id": 1,
            "name": "Original Name",
            "email": "original@example.com",
        }
        loader.load_record(stream_name, record1, schema)
        loader.finalize_all_streams()

        # Update the record
        record2 = {
            "id": 1,
            "name": "Updated Name",
            "email": "updated@example.com",
        }
        loader.load_record(stream_name, record2, schema)
        loader.finalize_all_streams()

        # Verify update
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            result = conn.execute(
                select(table.c.NAME, table.c.EMAIL).where(table.c.ID == 1),
            )
            row = result.fetchone()
            assert row[0] == "Updated Name"
            assert row[1] == "updated@example.com"

            # Should still have only one record
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 1

    def test_real_nested_json_flattening(
        self,
        real_loader: LoaderProtocol,
        nested_schema: FlextTypes.Dict,
        _oracle_engine: Engine,
    ) -> None:
        """Test flattening nested JSON structures in real Oracle."""
        stream_name = "nested_json"
        schema = nested_schema["schema"]
        key_properties = nested_schema["key_properties"]

        # Ensure table exists
        real_loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load nested record
        record = {
            "order_id": "ORD-001",
            "customer": {
                "id": 123,
                "name": "John Doe",
                "address": {
                    "street": "123 Main St",
                    "city": "objecttown",
                    "country": "USA",
                },
            },
            "items": [
                {"sku": "ITEM-1", "quantity": 2, "price": 99.99},
                {"sku": "ITEM-2", "quantity": 1, "price": 149.99},
            ],
            "total": 349.97,
        }

        result = real_loader.load_record(stream_name, record, schema)
        assert result.is_success

        real_loader.finalize_all_streams()

        # Verify flattened columns
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            result = conn.execute(select(table).where(table.c.ORDER_ID == "ORD-001"))
            row = result.fetchone()
            assert row is not None

            # Check flattened columns exist via query
            result = conn.execute(
                text(
                    """

                  SELECT column_name
                  FROM user_tab_columns
                  WHERE table_name = :table_name
                  AND column_name LIKE 'CUSTOMER__%'
                  ORDER BY column_name
                  """,
                ),
                {"table_name": stream_name.upper()},
            )
            customer_cols = [row[0] for row in result]
            assert "CUSTOMER__ID" in customer_cols
            assert "CUSTOMER__NAME" in customer_cols
            assert "CUSTOMER__ADDRESS__STREET" in customer_cols
            assert "CUSTOMER__ADDRESS__CITY" in customer_cols

    @pytest.mark.usefixtures("oracle_engine")
    def test_real_type_conversions(
        self,
        real_loader: object,
        _oracle_engine: Engine,
    ) -> None:
        """Test various data type conversions in real Oracle."""
        stream_name = "type_test"

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "is_active": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "metadata": {"type": "object"},
            },
        }
        key_properties = ["id"]

        # Ensure table exists
        real_loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load record with various types
        record = {
            "id": 1,
            "name": "Test Product",
            "price": Decimal("99.99"),
            "is_active": True,
            "created_at": datetime.now(UTC).isoformat(),
            "tags": ["electronics", "mobile", "smartphone"],
            "metadata": {"color": "black", "weight": 150},
        }

        result = real_loader.load_record(stream_name, record, schema)
        assert result.is_success

        real_loader.finalize_all_streams()

        # Verify types in database
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            result = conn.execute(
                select(
                    table.c.ID,
                    table.c.NAME,
                    table.c.PRICE,
                    table.c.IS_ACTIVE,
                    table.c.CREATED_AT,
                ).where(table.c.ID == 1),
            )
            row = result.fetchone()
            assert row[0] == 1  # INTEGER -> NUMBER
            assert row[1] == "Test Product"  # STRING -> VARCHAR2
            assert float(row[2]) == 99.99  # NUMBER -> NUMBER
            assert row[3] == 1  # BOOLEAN -> NUMBER(1)
            assert row[4] is not None  # DATETIME -> TIMESTAMP

    def test_real_error_handling_invalid_schema(
        self,
        real_loader: object,
    ) -> None:
        """Test error handling with invalid schema."""
        stream_name = "invalid_schema"

        # Schema missing required "type" field
        invalid_schema = {
            "properties": {
                "id": {"type": "integer"},
            },
        }

        with pytest.raises(FlextTargetOracleSchemaError):
            real_loader.ensure_table_exists(stream_name, invalid_schema, ["id"])

    def test_real_column_ordering(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test column ordering in real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            column_ordering="custom",
            column_order_rules={
                "primary_keys": 1,
                "regular_columns": 2,
                "audit_columns": 3,
                "sdc_columns": 4,
            },
            audit_column_patterns=["created_at", "updated_at"],
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "ordered_columns"

        # Schema with audit columns
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
                "status": {"type": "string"},
            },
        }
        key_properties = ["id"]

        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Check column order
        with _oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """

                  SELECT column_name, column_id
                  FROM user_tab_columns
                  WHERE table_name = :table_name
                  ORDER BY column_id
                  """,
                ),
                {"table_name": stream_name.upper()},
            )
            columns = [(row[0], row[1]) for row in result]

            # Verify order: PK first, then regular, then audit, then SDC
            column_names = [col[0] for col in columns]

            # Primary key should be first
            assert column_names[0] == "ID"

            # Regular columns next
            regular_cols = ["NAME", "EMAIL", "STATUS"]
            for col in regular_cols:
                assert col in column_names[1:4]

            # Audit columns
            audit_cols = ["CREATED_AT", "UPDATED_AT"]
            for col in audit_cols:
                assert col in column_names[4:6]

            # SDC columns last
            sdc_cols = [col for col in column_names if col.startswith("_SDC_")]
            assert len(sdc_cols) > 0
            for sdc_col in sdc_cols:
                assert column_names.index(sdc_col) > column_names.index("UPDATED_AT")

    def test_real_custom_indexes(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test custom index creation in real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            custom_indexes={
                "indexed_table": [
                    {"name": "idx_email_unique", "columns": ["email"], "unique": True},
                    {"name": "idx_name", "columns": ["name"]},
                ],
            },
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "indexed_table"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Verify indexes created
        with _oracle_engine.connect() as conn:
            result = conn.execute(
                text(
                    """

                  SELECT index_name, uniqueness
                  FROM user_indexes
                  WHERE table_name = :table_name
                  AND index_name NOT LIKE 'SYS_%'
                  ORDER BY index_name
                  """,
                ),
                {"table_name": stream_name.upper()},
            )
            indexes = {row[0]: row[1] for row in result}

            assert "IDX_EMAIL_UNIQUE" in indexes
            assert indexes["IDX_EMAIL_UNIQUE"] == "UNIQUE"
            assert "IDX_NAME" in indexes
            assert indexes["IDX_NAME"] == "NONUNIQUE"

    def test_real_finalize_streams_metrics(
        self,
        real_loader: LoaderProtocol,
        _simple_schema: FlextTypes.Dict,
    ) -> None:
        """Test finalize streams with metrics in real Oracle."""
        stream_name = "metrics_test"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        # Ensure table exists
        real_loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load some records
        for i in range(5):
            record = {
                "id": i + 1,
                "name": f"User {i + 1}",
                "email": f"user{i + 1}@example.com",
            }
            real_loader.load_record(stream_name, record, schema)

        # Finalize and get metrics
        result = real_loader.finalize_all_streams()
        assert result.is_success

        metrics = result.value
        assert metrics["total_records"] == 5
        assert metrics["successful_records"] == 5
        assert metrics["failed_records"] == 0
        assert len(metrics["streams"]) == 1
        assert stream_name in metrics["streams"]
        assert metrics["streams"][stream_name]["count"] == 5

    def test_real_get_table_name_variants(
        self,
        real_loader: object,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test method."""
        """Test table name generation with various options."""
        # Test default behavior
        assert real_loader._get_table_name("my_stream") == "MY_STREAM"

        # Test with prefix
        real_loader.config.table_name_prefix = "stg_"
        assert real_loader._get_table_name("my_stream") == "STG_MY_STREAM"

        # Test with custom mapping
        real_loader.config.table_name_mapping = {"my_stream": "custom_table"}
        assert real_loader._get_table_name("my_stream") == "CUSTOM_TABLE"

    def test_real_parallel_and_direct_path(
        self,
        _oracle_engine: Engine,
        _simple_schema: FlextTypes.Dict,
        _clean_database: Callable[[], None],
    ) -> None:
        """Test parallel and direct path options in real Oracle."""
        config = FlextTargetOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="FLEXT_TEST",
            oracle_password="test_password",
            default_target_schema="FLEXT_TEST",
            load_method=LoadMethod.BULK_INSERT,
            use_direct_path=True,
            parallel_degree=4,
            batch_size=100,
        )

        loader = FlextTargetOracleLoader(config)
        loader.connect()

        stream_name = "parallel_test"
        schema = _simple_schema["schema"]
        key_properties = _simple_schema["key_properties"]

        loader.ensure_table_exists(stream_name, schema, key_properties)

        # Load many records to test performance options
        for i in range(200):
            record = {
                "id": i + 1,
                "name": f"Parallel User {i + 1}",
                "email": f"parallel{i + 1}@example.com",
            }
            loader.load_record(stream_name, record, schema)

        loader.finalize_all_streams()

        # Verify all records loaded
        with _oracle_engine.connect() as conn:
            table = Table(stream_name.upper(), MetaData(), autoload_with=conn)
            count = conn.execute(select(func.count()).select_from(table)).scalar()
            assert count == 200
