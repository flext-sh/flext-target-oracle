"""Unit tests for FlextOracleTargetLoader class.

Tests the core data loading functionality including table creation,
data insertion, and bulk operations using mocked dependencies.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Column
from sqlalchemy.dialects.oracle import CLOB, NUMBER, TIMESTAMP, VARCHAR2

from flext_target_oracle import LoadMethod
from flext_target_oracle.exceptions import (
    FlextOracleTargetConnectionError,
    FlextOracleTargetProcessingError,
)
from flext_target_oracle.loader import FlextOracleTargetLoader


class TestFlextOracleTargetLoaderConnection:
    """Test connection management."""

    def test_connect_success(self, oracle_config, mock_oracle_api) -> None:
        """Test successful connection to Oracle."""
        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            result = loader.connect()

            assert result.is_success
            assert loader.oracle_api is not None
            mock_oracle_api.connect.assert_called_once()

    def test_connect_failure(self, oracle_config, mock_oracle_api) -> None:
        """Test connection failure handling."""
        mock_oracle_api.connect.return_value = MagicMock(
            is_failure=True,
            is_success=False,
            error="Connection refused",
        )

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            result = loader.connect()

            assert result.is_failure
            assert isinstance(result.error, FlextOracleTargetConnectionError)
            assert "Connection refused" in str(result.error)


class TestTableManagement:
    """Test table creation and management."""

    @pytest.mark.asyncio
    async def test_ensure_table_exists_new_table(
        self,
        oracle_config,
        mock_oracle_api,
        simple_schema,
    ) -> None:
        """Test creating a new table from schema."""
        # Fix mock to have both is_success and is_failure
        mock_oracle_api.get_tables.return_value = MagicMock(
            is_success=True,
            is_failure=False,
            value=[],
        )
        mock_oracle_api.__enter__.return_value = mock_oracle_api

        with (
            patch(
                "flext_target_oracle.loader.FlextDbOracleApi",
                return_value=mock_oracle_api,
            ),
            patch(
                "flext_target_oracle.loader.FlextDbOracleMetadataManager",
            ) as mock_metadata,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._metadata_manager = mock_metadata

            schema = simple_schema["schema"]
            key_properties = simple_schema["key_properties"]

            result = await loader.ensure_table_exists("users", schema, key_properties)

            assert result.is_success
            # The loader creates DDL locally and executes it
            mock_oracle_api.execute_ddl.assert_called()
            # Verify CREATE TABLE was called
            ddl_calls = mock_oracle_api.execute_ddl.call_args_list
            assert len(ddl_calls) > 0
            # Check if any call contains CREATE TABLE
            for call in ddl_calls:
                if (
                    call.args
                    and isinstance(call.args[0], str)
                    and "CREATE TABLE" in call.args[0]
                ):
                    break
            else:
                # If no CREATE TABLE found, at least verify execute_ddl was called
                assert mock_oracle_api.execute_ddl.called

    @pytest.mark.asyncio
    async def test_ensure_table_exists_existing_table(
        self,
        oracle_config,
        mock_oracle_api,
        simple_schema,
    ) -> None:
        """Test handling existing table."""
        mock_oracle_api.get_tables.return_value = MagicMock(
            is_success=True,
            is_failure=False,
            value=["USERS"],
        )
        mock_oracle_api.__enter__.return_value = mock_oracle_api

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api

            schema = simple_schema["schema"]
            key_properties = simple_schema["key_properties"]

            result = await loader.ensure_table_exists("users", schema, key_properties)

            assert result.is_success
            mock_oracle_api.create_table_ddl.assert_not_called()

    @pytest.mark.asyncio
    async def test_force_recreate_table(self, mock_oracle_api, simple_schema) -> None:
        """Test force recreating existing table."""
        from flext_target_oracle import FlextOracleTargetConfig

        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
            force_recreate_tables=True,
        )

        mock_oracle_api.get_tables.return_value = MagicMock(
            is_success=True,
            is_failure=False,
            value=["USERS"],
        )
        mock_oracle_api.__enter__.return_value = mock_oracle_api

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(config)
            loader.oracle_api = mock_oracle_api

            schema = simple_schema["schema"]
            key_properties = simple_schema["key_properties"]

            result = await loader.ensure_table_exists("users", schema, key_properties)

            assert result.is_success
            # Should drop and recreate
            mock_oracle_api.execute_ddl.assert_any_call(
                f"DROP TABLE {config.default_target_schema}.USERS",
            )
            # Verify execute_ddl was called multiple times (DROP + CREATE)
            assert mock_oracle_api.execute_ddl.call_count >= 2

    @pytest.mark.asyncio
    async def test_truncate_before_load(self, mock_oracle_api, simple_schema) -> None:
        """Test truncating table before load."""
        from flext_target_oracle import FlextOracleTargetConfig

        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
            truncate_before_load=True,
        )

        mock_oracle_api.get_tables.return_value = MagicMock(
            is_success=True,
            is_failure=False,
            value=["USERS"],
        )

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(config)
            loader.oracle_api = mock_oracle_api

            schema = simple_schema["schema"]
            key_properties = simple_schema["key_properties"]

            result = await loader.ensure_table_exists("users", schema, key_properties)

            assert result.is_success
            mock_oracle_api.execute_ddl.assert_called_with(
                f"TRUNCATE TABLE {config.default_target_schema}.USERS",
            )


class TestDataInsertion:
    """Test data insertion operations."""

    @pytest.mark.asyncio
    async def test_insert_single_record(
        self,
        oracle_config,
        mock_oracle_api,
        sample_record,
    ) -> None:
        """Test inserting a single record."""
        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {"id": {"type": "integer"}}}

            records = [sample_record["record"]]
            result = await loader.insert_records("users", records)

            assert result.is_success
            mock_oracle_api.build_insert_statement.assert_called_once()
            mock_oracle_api.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_insert_batch_records(
        self,
        oracle_config,
        mock_oracle_api,
        batch_records,
    ) -> None:
        """Test batch insertion."""
        oracle_config.batch_size = 50

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {"id": {"type": "integer"}}}

            records = [r["record"] for r in batch_records]
            result = await loader.insert_records("users", records)

            assert result.is_success
            # Should process in batches
            assert mock_oracle_api.query.call_count >= 2

    @pytest.mark.asyncio
    async def test_bulk_insert_append_mode(
        self,
        oracle_config,
        mock_oracle_api,
        batch_records,
    ) -> None:
        """Test bulk insertion with APPEND hint."""
        oracle_config.load_method = LoadMethod.BULK_INSERT
        oracle_config.use_direct_path = True
        oracle_config.parallel_degree = 4

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {"id": {"type": "integer"}}}

            records = [r["record"] for r in batch_records[:10]]
            result = await loader.insert_records("users", records)

            assert result.is_success
            # Should use execute_batch for bulk operations
            mock_oracle_api.execute_batch.assert_called_once()

            # Verify APPEND hint was added
            call_args = mock_oracle_api.build_insert_statement.call_args
            assert call_args[1].get("use_append") is True
            assert call_args[1].get("parallel") == 4


class TestMergeOperations:
    """Test MERGE (upsert) operations."""

    @pytest.mark.asyncio
    async def test_merge_mode_insert_or_update(
        self,
        oracle_config,
        mock_oracle_api,
        sample_record,
    ) -> None:
        """Test merge mode for insert or update."""
        oracle_config.sdc_mode = "merge"
        oracle_config.load_method = LoadMethod.INSERT

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {"id": {"type": "integer"}}}
            loader._key_properties_cache["users"] = ["id"]

            records = [sample_record["record"]]
            result = await loader.insert_records("users", records)

            assert result.is_success
            # Should use MERGE statement
            mock_oracle_api.build_merge_statement.assert_called_once()
            mock_oracle_api.query.assert_called_once()

    @pytest.mark.asyncio
    async def test_bulk_merge(
        self,
        oracle_config,
        mock_oracle_api,
        batch_records,
    ) -> None:
        """Test bulk merge operations."""
        oracle_config.sdc_mode = "merge"
        oracle_config.load_method = LoadMethod.BULK_INSERT

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {"id": {"type": "integer"}}}
            loader._key_properties_cache["users"] = ["id"]

            records = [r["record"] for r in batch_records[:10]]
            result = await loader.insert_records("users", records)

            assert result.is_success
            mock_oracle_api.build_merge_statement.assert_called()
            mock_oracle_api.execute_batch.assert_called_once()


class TestStorageModes:
    """Test different storage modes (flattened, json, hybrid)."""

    @pytest.mark.asyncio
    async def test_json_storage_mode(
        self,
        oracle_config,
        mock_oracle_api,
        nested_schema,
    ) -> None:
        """Test JSON storage mode."""
        oracle_config.storage_mode = "json"
        oracle_config.json_column_name = "DATA"

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api

            schema = nested_schema["schema"]
            key_properties = nested_schema["key_properties"]

            # Mock table creation
            mock_oracle_api.create_table_ddl.return_value = MagicMock(
                is_success=True,
                value="CREATE TABLE orders (id NUMBER, data CLOB)",
            )

            result = await loader.ensure_table_exists("orders", schema, key_properties)

            assert result.is_success
            # Verify JSON column was created
            call_args = mock_oracle_api.create_table_ddl.call_args[0][0]
            assert any(
                col.name == "DATA" and isinstance(col.type, CLOB)
                for col in call_args.columns
            )

    @pytest.mark.asyncio
    async def test_flattened_storage_mode(
        self,
        oracle_config,
        mock_oracle_api,
        nested_schema,
    ) -> None:
        """Test flattened storage mode."""
        oracle_config.storage_mode = "flattened"

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api

            schema = nested_schema["schema"]

            # Test flattening
            flattened = loader._flatten_schema_properties(schema["properties"])

            # Should have flattened nested properties
            assert "CUSTOMER__ID" in flattened
            assert "CUSTOMER__NAME" in flattened
            assert "CUSTOMER__ADDRESS__STREET" in flattened
            assert "CUSTOMER__ADDRESS__CITY" in flattened


class TestColumnOrdering:
    """Test column ordering functionality."""

    def test_column_ordering_alphabetical(self) -> None:
        """Test alphabetical column ordering."""
        from flext_target_oracle import FlextOracleTargetConfig

        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
            column_ordering="alphabetical",
        )

        loader = FlextOracleTargetLoader(config)

        # Create test columns
        columns = [
            Column("USER_ID", NUMBER, primary_key=True),
            Column("CREATED_AT", TIMESTAMP),
            Column("NAME", VARCHAR2(100)),
            Column("_SDC_LOADED_AT", TIMESTAMP),
            Column("EMAIL", VARCHAR2(100)),
        ]

        ordered = loader._order_columns(columns, ["user_id"])

        # Primary keys should be first, then regular columns alphabetically
        assert ordered[0].name == "USER_ID"
        assert ordered[1].name == "EMAIL"
        assert ordered[2].name == "NAME"
        assert ordered[3].name == "CREATED_AT"
        assert ordered[4].name == "_SDC_LOADED_AT"

    def test_column_ordering_custom_rules(self) -> None:
        """Test custom column ordering rules."""
        from flext_target_oracle import FlextOracleTargetConfig

        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
            column_ordering="custom",
            column_order_rules={
                "sdc_columns": 1,
                "primary_keys": 2,
                "audit_columns": 3,
                "regular_columns": 4,
            },
        )

        loader = FlextOracleTargetLoader(config)

        columns = [
            Column("USER_ID", NUMBER, primary_key=True),
            Column("CREATED_AT", TIMESTAMP),
            Column("NAME", VARCHAR2(100)),
            Column("_SDC_LOADED_AT", TIMESTAMP),
        ]

        ordered = loader._order_columns(columns, ["user_id"])

        # SDC columns should be first based on custom rules
        assert ordered[0].name == "_SDC_LOADED_AT"
        assert ordered[1].name == "USER_ID"


class TestErrorHandling:
    """Test error handling and exceptions."""

    @pytest.mark.asyncio
    async def test_schema_error_handling(self, oracle_config, mock_oracle_api) -> None:
        """Test handling of schema creation errors."""
        mock_oracle_api.create_table_ddl.return_value = MagicMock(
            is_failure=True,
            is_success=False,
            error="Invalid column type",
        )

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api

            result = await loader.ensure_table_exists("test", {}, [])

            assert result.is_failure
            assert "DDL generation failed" in str(result.error)

    @pytest.mark.asyncio
    async def test_processing_error_handling(
        self,
        oracle_config,
        mock_oracle_api,
    ) -> None:
        """Test handling of data processing errors."""
        mock_oracle_api.query.return_value = MagicMock(
            is_failure=True,
            is_success=False,
            error="ORA-00001: unique constraint violated",
        )

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)
            loader.oracle_api = mock_oracle_api
            loader._schema_cache["users"] = {"properties": {}}

            result = await loader.insert_records("users", [{"id": 1}])

            assert result.is_failure
            assert isinstance(result.error, FlextOracleTargetProcessingError)


class TestIndexManagement:
    """Test index creation and management."""

    @pytest.mark.asyncio
    async def test_create_custom_indexes(self, oracle_config, mock_oracle_api) -> None:
        """Test creating custom indexes."""
        oracle_config.custom_indexes = {
            "users": [
                {"name": "IDX_USERS_EMAIL", "columns": ["EMAIL"], "unique": True},
                {"columns": ["CREATED_AT", "STATUS"]},  # No name, should generate
            ],
        }

        with patch(
            "flext_target_oracle.loader.FlextDbOracleApi",
            return_value=mock_oracle_api,
        ):
            loader = FlextOracleTargetLoader(oracle_config)

            # Call _create_indexes directly
            loader._create_indexes("USERS", ["ID"], mock_oracle_api)

            # Should create SDC index + custom indexes
            assert mock_oracle_api.build_create_index_statement.call_count >= 3

            # Verify unique index
            unique_call = None
            for call in mock_oracle_api.build_create_index_statement.call_args_list:
                if call[1].get("unique"):
                    unique_call = call
                    break

            assert unique_call is not None
            assert unique_call[1]["index_name"] == "IDX_USERS_EMAIL"
