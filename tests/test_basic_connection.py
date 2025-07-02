"""
Basic connection test for Oracle Target.

This test validates basic connectivity without testing licensed features.
"""

from flext_target_oracle import OracleTarget

from .helpers import (
    get_test_config,
    requires_oracle_connection,
)


class TestBasicConnection:
    """Test basic Oracle connectivity."""

    @requires_oracle_connection
    def test_connection_and_simple_query(self):
        """Test basic connection and simple query execution."""
        config = get_test_config(include_licensed_features=False)
        target = OracleTarget(config=config)

        # Create a sink to establish connection
        # Need to provide a schema for Singer SDK
        test_schema = {"type": "object", "properties": {"id": {"type": "integer"}}}
        sink = target.get_sink("test_connection", schema=test_schema)

        # Test basic query
        from sqlalchemy import text

        with sink.connector._engine.connect() as conn:
            # Simple query that works on all Oracle editions
            result = conn.execute(text("SELECT 1 FROM DUAL")).scalar()
            assert result == 1

            # Test table exists
            version = conn.execute(
                text("SELECT BANNER FROM v$version WHERE ROWNUM = 1")
            ).scalar()
            print(f"Oracle version: {version}")

            # Check user and schema
            user = conn.execute(text("SELECT USER FROM DUAL")).scalar()
            print(f"Connected as: {user}")

            # Check if we're on Enterprise Edition
            is_ee = (
                conn.execute(
                    text("""
                SELECT COUNT(*) FROM v$version
                WHERE BANNER LIKE '%Enterprise Edition%'
            """)
                ).scalar()
                > 0
            )
            print(f"Is Enterprise Edition: {is_ee}")

            # Verify table was created
            table_count = conn.execute(
                text("""
                SELECT COUNT(*) FROM user_tables
                WHERE table_name = 'TEST_CONNECTION'
            """)
            ).scalar()
            assert table_count == 1
            print("Table created successfully")

            # Check column types are Oracle-compatible
            column_types = conn.execute(
                text("""
                SELECT column_name, data_type
                FROM user_tab_columns
                WHERE table_name = 'TEST_CONNECTION'
                ORDER BY column_name
            """)
            ).fetchall()
            print("Column types:")
            for col_name, data_type in column_types:
                print(f"  {col_name}: {data_type}")

            # Clean up
            conn.execute(text("DROP TABLE test_connection"))

    @requires_oracle_connection
    def test_basic_table_operations(self):
        """Test basic table operations available in all editions."""
        config = get_test_config(include_licensed_features=False)
        # Ensure we're using basic features only
        config["enable_compression"] = False
        config["enable_partitioning"] = False
        config["use_inmemory"] = False
        config["parallel_degree"] = 1

        target = OracleTarget(config=config)

        # Test schema and record
        schema = {
            "type": "SCHEMA",
            "stream": "test_basic",
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

        record = {
            "type": "RECORD",
            "stream": "test_basic",
            "record": {"id": 1, "name": "Test Record", "value": 100.50},
        }

        # Process messages
        import json
        from io import StringIO

        from sqlalchemy import text

        messages = [schema, record]
        input_data = "\n".join(json.dumps(msg) for msg in messages)

        target.listen(file_input=StringIO(input_data))

        # Verify data
        sink = target.get_sink("test_basic")
        with sink.connector._engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {sink.full_table_name}")
            ).scalar()
            assert result == 1

            # Clean up
            conn.execute(text(f"DROP TABLE {sink.full_table_name}"))

    @requires_oracle_connection
    def test_merge_statement(self):
        """Test MERGE statement (available in all editions)."""
        config = get_test_config(include_licensed_features=False)
        config["load_method"] = "upsert"
        config["use_merge_statements"] = True

        target = OracleTarget(config=config)

        schema = {
            "type": "SCHEMA",
            "stream": "test_merge",
            "schema": {
                "type": "object",
                "properties": {"id": {"type": "integer"}, "status": {"type": "string"}},
            },
            "key_properties": ["id"],
        }

        # Initial record
        messages = [
            schema,
            {
                "type": "RECORD",
                "stream": "test_merge",
                "record": {"id": 1, "status": "initial"},
            },
        ]

        import json
        from io import StringIO

        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Update record
        messages = [
            schema,
            {
                "type": "RECORD",
                "stream": "test_merge",
                "record": {"id": 1, "status": "updated"},
            },
        ]

        from sqlalchemy import text as sql_text

        input_data = "\n".join(json.dumps(msg) for msg in messages)
        target.listen(file_input=StringIO(input_data))

        # Verify update
        sink = target.get_sink("test_merge")
        with sink.connector._engine.connect() as conn:
            result = conn.execute(
                sql_text(f"SELECT status FROM {sink.full_table_name} WHERE id = 1")
            ).scalar()
            assert result == "updated"

            # Should still have only 1 record
            count = conn.execute(
                sql_text(f"SELECT COUNT(*) FROM {sink.full_table_name}")
            ).scalar()
            assert count == 1

            # Clean up
            conn.execute(sql_text(f"DROP TABLE {sink.full_table_name}"))
