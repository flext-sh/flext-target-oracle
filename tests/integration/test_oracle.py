"""Integration tests for Oracle Target with real database.

These tests require a running Oracle database container and test
actual database operations including DDL, DML, and bulk operations.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time

import pytest
from flext_tests import tm

from flext_db_oracle import FlextDbOracleApi
from flext_target_oracle import FlextTargetOracleSettings
from flext_target_oracle._utilities.client import FlextTargetOracle
from flext_target_oracle._utilities.loader import FlextTargetOracleLoader
from tests import c, m, t

pytestmark = pytest.mark.integration


def _schema_parts(
    message: t.JsonValue,
) -> t.Pair[t.JsonMapping, t.SequenceOf[str]]:
    schema_message = m.Meltano.SingerSchemaMessage.model_validate(message)
    return (schema_message.schema_definition, schema_message.key_properties)


def _query_rows(
    oracle_engine: FlextDbOracleApi,
    sql: str,
    params: t.JsonMapping | None = None,
) -> t.SequenceOf[m.Dict]:
    normalized_params = None if params is None else m.ConfigMap(root=dict(params))
    query_result = oracle_engine.oracle_services.execute_query(sql, normalized_params)
    tm.ok(query_result)
    return query_result.value


def _query_scalar(
    oracle_engine: FlextDbOracleApi,
    sql: str,
    key: str,
    params: t.JsonMapping | None = None,
) -> str:
    rows = _query_rows(oracle_engine, sql, params)
    assert rows
    return str(rows[0].root[key])


@pytest.mark.integration
@pytest.mark.oracle
class TestsFlextTargetOracleOracle:
    """Integration tests with real Oracle database."""

    @pytest.mark.usefixtures("clean_database")
    def test_create_simple_table(
        self,
        oracle_loader: FlextTargetOracleLoader,
        oracle_engine: FlextDbOracleApi,
        simple_schema: t.JsonValue,
    ) -> None:
        """Test creating a simple table with basic data types."""
        stream_name = "test_users"
        schema_dict, key_props = _schema_parts(simple_schema)
        table_res = oracle_loader.ensure_table_exists(
            stream_name,
            schema_dict,
            key_props,
        )
        tm.ok(table_res)
        table_count = _query_scalar(
            oracle_engine,
            'SELECT COUNT(*) AS "count" FROM user_tables WHERE table_name = :table_name',
            "count",
            {"table_name": "TEST_USERS"},
        )
        tm.that(int(table_count), eq=1)
        column_rows = _query_rows(
            oracle_engine,
            'SELECT column_name AS "column_name", data_type AS "data_type" FROM user_tab_columns WHERE table_name = :table_name ORDER BY column_id',
            {"table_name": "TEST_USERS"},
        )
        columns = {
            str(row.root["column_name"]): str(row.root["data_type"])
            for row in column_rows
        }
        tm.that(columns, has="ID")
        tm.that(columns, has="NAME")
        tm.that(columns, has="EMAIL")
        tm.that(columns, has="_SDC_EXTRACTED_AT")
        tm.that(columns, has="_SDC_LOADED_AT")

    @pytest.mark.usefixtures("clean_database")
    def test_insert_and_retrieve_data(
        self,
        oracle_loader: FlextTargetOracleLoader,
        oracle_engine: FlextDbOracleApi,
        simple_schema: t.JsonValue,
    ) -> None:
        """Test inserting data and retrieving it."""
        stream_name = "test_insert"
        schema_dict, key_props = _schema_parts(simple_schema)
        create_res = oracle_loader.ensure_table_exists(
            stream_name,
            schema_dict,
            key_props,
        )
        tm.ok(create_res)
        records: t.SequenceOf[t.JsonMapping] = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
        result = oracle_loader.insert_records(stream_name, records)
        tm.ok(result)
        rows = _query_rows(
            oracle_engine,
            'SELECT id AS "id", name AS "name", email AS "email" FROM test_insert ORDER BY id',
        )
        tm.that(len(rows), eq=2)
        tm.that(
            rows[0].root,
            eq={
                "id": "1",
                "name": "John Doe",
                "email": "john@example.com",
            },
        )
        tm.that(
            rows[1].root,
            eq={
                "id": "2",
                "name": "Jane Smith",
                "email": "jane@example.com",
            },
        )

    @pytest.mark.usefixtures("clean_database")
    def test_merge_mode_updates(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
        simple_schema: t.JsonValue,
    ) -> None:
        """Test merge mode for updating existing records."""
        oracle_config = oracle_config.clone(sdc_mode="merge")
        loader = FlextTargetOracleLoader(oracle_config)
        connect_result = loader.connect()
        tm.ok(connect_result)
        stream_name = "test_merge"
        schema_dict, key_props = _schema_parts(simple_schema)
        table_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        tm.ok(table_res)
        initial_records: t.SequenceOf[t.JsonMapping] = [
            {"id": 1, "name": "Original Name", "email": "original@example.com"},
        ]
        insert_result = loader.insert_records(stream_name, initial_records)
        tm.ok(insert_result)
        updated_records: t.SequenceOf[t.JsonMapping] = [
            {"id": 1, "name": "Updated Name", "email": "updated@example.com"},
        ]
        result = loader.insert_records(stream_name, updated_records)
        tm.ok(result)
        rows = _query_rows(
            oracle_engine,
            'SELECT name AS "name", email AS "email" FROM test_merge WHERE id = 1',
        )
        assert rows
        tm.that(rows[0].root["name"], eq="Updated Name")
        tm.that(rows[0].root["email"], eq="updated@example.com")
        disconnect_result = loader.disconnect()
        tm.ok(disconnect_result)

    @pytest.mark.usefixtures("clean_database")
    def test_bulk_insert_performance(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
    ) -> None:
        """Test bulk insert with large dataset."""
        oracle_config = oracle_config.clone(
            load_method=c.TargetOracle.LOAD_METHOD_BULK_INSERT,
            batch_size=1000,
        )
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "test_bulk"
        schema_message: t.JsonValue = {
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
        tm.ok(table_res)
        records: t.SequenceOf[t.JsonMapping] = [
            {"id": i, "data": f"Bulk test data {i}", "value": i * 1.5}
            for i in range(5000)
        ]
        start_time = time.time()
        result = loader.insert_records(stream_name, records)
        elapsed = time.time() - start_time
        tm.ok(result)
        count = _query_scalar(
            oracle_engine,
            'SELECT COUNT(*) AS "count" FROM test_bulk',
            "count",
        )
        tm.that(int(count), eq=5000)
        assert elapsed < 10.0
        tm.ok(loader.disconnect())

    @pytest.mark.usefixtures("clean_database")
    def test_json_storage_mode(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
        nested_schema: t.JsonValue,
    ) -> None:
        """Test JSON storage mode with nested data."""
        oracle_config = oracle_config.clone()
        oracle_config = oracle_config.clone(
            storage_mode="json",
            json_column_name="json_data",
        )
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "test_json"
        schema_dict, key_props = _schema_parts(nested_schema)
        create_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        tm.ok(create_res)
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
        typed_record = t.json_mapping_adapter().validate_python(record)
        insert_res = loader.insert_records(stream_name, [typed_record])
        tm.ok(insert_res)
        json_str = _query_scalar(
            oracle_engine,
            'SELECT json_data AS "json_data" FROM test_json WHERE id = 1',
            "json_data",
        )
        stored_data = t.json_mapping_adapter().validate_json(json_str)
        customer = stored_data.get("customer")
        customer_data = t.json_mapping_adapter().validate_python(customer)
        customer_name = customer_data.get("name")
        tm.that(customer_name, eq="Acme Corp")
        customer_address = customer_data.get("address")
        customer_address_data = t.json_mapping_adapter().validate_python(
            customer_address,
        )
        customer_city = customer_address_data.get("city")
        tm.that(customer_city, eq="objecttown")
        items = stored_data.get("items")
        items_data = t.Tests.CONTAINER_MAPPING_SEQUENCE_ADAPTER.validate_python(items)
        tm.that(len(items_data), eq=2)
        tm.ok(loader.disconnect())

    @pytest.mark.usefixtures("clean_database")
    def test_column_ordering(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
    ) -> None:
        """Test column ordering in created tables."""
        oracle_config = oracle_config.clone(
            column_ordering="alphabetical",
            column_order_rules={
                "primary_keys": 1,
                "regular_columns": 2,
                "audit_columns": 3,
                "sdc_columns": 4,
            },
        )
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "test_ordering"
        schema_message: t.JsonValue = {
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
        tm.ok(table_res)
        column_rows = _query_rows(
            oracle_engine,
            'SELECT column_name AS "column_name", column_id AS "column_id" FROM user_tab_columns WHERE table_name = :table_name ORDER BY column_id',
            {"table_name": "TEST_ORDERING"},
        )
        columns = [str(row.root["column_name"]) for row in column_rows]
        tm.that(columns[0], eq="ID")
        regular_start = 1
        tm.that(columns[regular_start], eq="ALPHA_FIELD")
        tm.that(columns[regular_start + 1], eq="ZEBRA_FIELD")
        audit_cols = [
            column for column in columns if column in {"CREATED_AT", "UPDATED_AT"}
        ]
        tm.that(len(audit_cols), eq=2)
        sdc_cols = [column for column in columns if column.startswith("_SDC_")]
        assert all(columns.index(sdc) > columns.index("UPDATED_AT") for sdc in sdc_cols)
        tm.ok(loader.disconnect())

    @pytest.mark.usefixtures("clean_database")
    def test_truncate_before_load(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
        simple_schema: t.JsonValue,
    ) -> None:
        """Test truncate table before loading data."""
        oracle_config = oracle_config.clone(truncate_before_load=True)
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "test_truncate"
        schema_dict, key_props = _schema_parts(simple_schema)
        create_res = loader.ensure_table_exists(stream_name, schema_dict, key_props)
        tm.ok(create_res)
        insert_initial = loader.insert_records(
            stream_name,
            [{"id": 1, "name": "Initial"}],
        )
        tm.ok(insert_initial)
        count = _query_scalar(
            oracle_engine,
            'SELECT COUNT(*) AS "count" FROM test_truncate',
            "count",
        )
        tm.that(int(count), eq=1)
        loader.ensure_table_exists(stream_name, schema_dict, key_props)
        count = _query_scalar(
            oracle_engine,
            'SELECT COUNT(*) AS "count" FROM test_truncate',
            "count",
        )
        tm.that(int(count), eq=0)
        tm.ok(loader.disconnect())

    @pytest.mark.usefixtures("clean_database")
    def test_custom_indexes(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
        simple_schema: t.JsonValue,
    ) -> None:
        """Test creation of custom indexes."""
        oracle_config = oracle_config.model_copy(
            update={
                "custom_indexes": {
                    "test_indexes": (
                        {
                            "name": "IDX_EMAIL_UNIQUE",
                            "columns": ["EMAIL"],
                            "unique": True,
                        },
                        {"columns": ["NAME", "CREATED_AT"]},
                    ),
                },
            },
        )
        loader = FlextTargetOracleLoader(oracle_config)
        tm.ok(loader.connect())
        stream_name = "test_indexes"
        schema_dict, key_props = _schema_parts(simple_schema)
        loader.ensure_table_exists(stream_name, schema_dict, key_props)
        index_rows = _query_rows(
            oracle_engine,
            'SELECT index_name AS "index_name", uniqueness AS "uniqueness" FROM user_indexes WHERE table_name = :table_name',
            {"table_name": "TEST_INDEXES"},
        )
        indexes = {
            str(row.root["index_name"]): str(row.root["uniqueness"])
            for row in index_rows
        }
        tm.that(indexes, has="IDX_EMAIL_UNIQUE")
        tm.that(indexes["IDX_EMAIL_UNIQUE"], eq="UNIQUE")
        composite_indexes = [
            index_name for index_name in indexes if "NAME" in index_name
        ]
        assert len(composite_indexes) > 0
        tm.ok(loader.disconnect())

    """End-to-end tests using the full FlextTargetOracle."""

    @pytest.mark.usefixtures("clean_database")
    def test_full_singer_workflow(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
        singer_messages: t.SequenceOf[t.JsonValue],
    ) -> None:
        """Test complete Singer workflow: schema -> records -> state."""
        target = FlextTargetOracle(settings=oracle_config)
        init_result = target.initialize()
        tm.ok(init_result)
        for message in singer_messages:
            result = target.execute(
                t.json_value_adapter().dump_json(message).decode("utf-8"),
            )
            tm.ok(result)
        table_count = _query_scalar(
            oracle_engine,
            "SELECT COUNT(*) AS \"count\" FROM user_tables WHERE table_name = 'USERS'",
            "count",
        )
        tm.that(int(table_count), eq=1)
        data_count = _query_scalar(
            oracle_engine,
            'SELECT COUNT(*) AS "count" FROM users',
            "count",
        )
        assert int(data_count) > 0

    @pytest.mark.usefixtures("clean_database")
    def test_column_mapping_and_filtering(
        self,
        oracle_config: FlextTargetOracleSettings,
        oracle_engine: FlextDbOracleApi,
    ) -> None:
        """Test column mapping and filtering features."""
        oracle_config = oracle_config.clone(
            column_mappings={"users": {"name": "full_name", "email": "email_address"}},
            ignored_columns=["password", "internal_id"],
        )
        target = FlextTargetOracle(settings=oracle_config)
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
        schema_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
            schema_msg,
        )
        target.execute(
            t.json_value_adapter().dump_json(schema_msg_value).decode("utf-8"),
        )
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
        record_msg_value: t.JsonValue = t.json_value_adapter().validate_python(
            record_msg,
        )
        target.execute(
            t.json_value_adapter().dump_json(record_msg_value).decode("utf-8"),
        )
        column_rows = _query_rows(
            oracle_engine,
            "SELECT column_name AS \"column_name\" FROM user_tab_columns WHERE table_name = 'USERS'",
        )
        columns = [str(row.root["column_name"]) for row in column_rows]
        tm.that(columns, has="FULL_NAME")
        tm.that(columns, has="EMAIL_ADDRESS")
        tm.that(columns, lacks="PASSWORD")
        tm.that(columns, lacks="INTERNAL_ID")
        rows = _query_rows(
            oracle_engine,
            'SELECT full_name AS "full_name", email_address AS "email_address" FROM users WHERE id = 1',
        )
        assert rows
        tm.that(rows[0].root["full_name"], eq="John Doe")
        tm.that(rows[0].root["email_address"], eq="john@example.com")
