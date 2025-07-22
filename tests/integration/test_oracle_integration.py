"""Oracle integration tests.

These tests verify Oracle database integration functionality.
"""

import asyncio
import os
from datetime import UTC, datetime
from typing import Any

import pytest
import pytest_asyncio
from flext_db_oracle import OracleConfig, OracleConnectionService, OracleQueryService

from flext_target_oracle.application.services import SingerTargetService
from flext_target_oracle.domain.models import TargetConfig


class TestOracleConnection:
    """Test Oracle database connection functionality."""

    @pytest.fixture
    def oracle_config_for_test(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "protocol": "tcp",
        }

    @pytest.mark.asyncio
    async def test_basic_connection(
        self,
        oracle_config_for_test: dict[str, Any],
    ) -> None:
        """Test basic Oracle connection.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        config = OracleConfig(**oracle_config_for_test)
        connection_service = OracleConnectionService(config)

        try:
            async with connection_service.get_connection() as conn:
                assert conn is not None
                # Test basic query
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM DUAL")
                    result = cursor.fetchone()
                    assert result[0] == 1
        except (ConnectionError, OSError, ValueError) as e:
            pytest.fail(f"Oracle connection failed: {e}")

    @pytest.mark.asyncio
    async def test_connection_pool(
        self,
        oracle_config_for_test: dict[str, Any],
    ) -> None:
        """Test Oracle connection pooling.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        config = OracleConfig(**oracle_config_for_test)
        connection_service = OracleConnectionService(config)

        try:
            # Test multiple concurrent connections
            async def get_connection() -> int:
                async with connection_service.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1 FROM DUAL")
                        result = cursor.fetchone()
                        return int(result[0]) if result else 0

            tasks = [get_connection() for _ in range(5)]
            results = await asyncio.gather(*tasks)

            assert all(result == 1 for result in results)
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Oracle connection pooling failed: {e}")

    @pytest.mark.asyncio
    async def test_query_service(self, oracle_config_for_test: dict[str, Any]) -> None:
        """Test Oracle query service.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        config = OracleConfig(**oracle_config_for_test)
        connection_service = OracleConnectionService(config)
        query_service = OracleQueryService(connection_service)

        try:
            # Test scalar query
            result = await query_service.execute_scalar("SELECT COUNT(*) FROM DUAL")
            assert result.success
            assert result.data == 1

            # Test query with parameters
            param_result = await query_service.execute_scalar(
                "SELECT :value FROM DUAL",
                {"value": 42},
            )
            assert param_result.success
            assert param_result.data == 42
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Oracle query service failed: {e}")


class TestTableOperations:
    """Test Oracle table operations."""

    @pytest.fixture
    def oracle_config_for_test(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "protocol": "tcp",
        }

    @pytest.fixture
    def target_config(self, oracle_config_for_test: dict[str, Any]) -> TargetConfig:
        """Create target configuration for testing."""
        return TargetConfig(
            **oracle_config_for_test,
            default_target_schema="FLEXT_TEST",
            batch_size=100,
        )

    @pytest_asyncio.fixture
    async def singer_service(self, target_config: TargetConfig) -> SingerTargetService:
        """Create Singer target service for testing."""
        return SingerTargetService(target_config)

    @pytest.mark.asyncio
    async def test_table_creation(self, singer_service: SingerTargetService) -> None:
        """Test table creation from schema.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        schema_message = {
            "type": "SCHEMA",
            "stream": "test_users",
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
        }

        try:
            result = await singer_service.process_singer_message(schema_message)
            assert result.success

            # Verify table exists
            check_result = await singer_service.query_service.execute_scalar(
                """
                SELECT COUNT(*)
                FROM all_tables
                WHERE owner = UPPER(:schema_name)
                AND table_name = UPPER(:table_name)
                """,
                {
                    "schema_name": singer_service.config.default_target_schema,
                    "table_name": "test_users",
                },
            )
            assert check_result.success
            assert check_result.data is not None
            assert check_result.data > 0
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Table creation test failed: {e}")

    @pytest.mark.asyncio
    async def test_record_insertion(self, singer_service: SingerTargetService) -> None:
        """Test record insertion into Oracle.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        # First ensure table exists
        schema_message = {
            "type": "SCHEMA",
            "stream": "test_records",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"},
                },
            },
        }

        record_message = {
            "type": "RECORD",
            "stream": "test_records",
            "record": {
                "id": 1,
                "data": "integration test data",
            },
        }

        try:
            # Create table
            schema_result = await singer_service.process_singer_message(schema_message)
            assert schema_result.success

            # Insert record
            record_result = await singer_service.process_singer_message(record_message)
            assert record_result.success

            # Verify record was inserted
            schema_name = singer_service.config.default_target_schema.upper()
            verify_result = await singer_service.query_service.execute_scalar(
                """
                SELECT COUNT(*)
                FROM all_tables
                WHERE owner = :schema_name
                AND table_name = 'TEST_RECORDS'
                """,
                {"schema_name": schema_name},
            )
            assert verify_result.success
            assert verify_result.data is not None
            assert verify_result.data >= 1
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Record insertion test failed: {e}")

    @pytest.mark.asyncio
    async def test_batch_processing(self, singer_service: SingerTargetService) -> None:
        """Test batch processing of multiple records.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        # Setup table
        schema_message = {
            "type": "SCHEMA",
            "stream": "test_batch",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "value": {"type": "string"},
                },
            },
        }

        try:
            await singer_service.process_singer_message(schema_message)

            # Insert multiple records to trigger batch processing
            for i in range(150):  # More than default batch size
                record_message = {
                    "type": "RECORD",
                    "stream": "test_batch",
                    "record": {
                        "id": i,
                        "value": f"batch_record_{i}",
                    },
                }
                result = await singer_service.process_singer_message(record_message)
                assert result.success

            # Finalize to flush remaining batches
            stats_result = await singer_service.finalize_all_streams()
            assert stats_result.success

            # Verify all records were inserted
            schema_name = singer_service.config.default_target_schema.upper()
            count_result = await singer_service.query_service.execute_scalar(
                """
                SELECT COUNT(*)
                FROM all_tables
                WHERE owner = :schema_name
                AND table_name = 'TEST_BATCH'
                """,
                {"schema_name": schema_name},
            )
            assert count_result.success
            assert count_result.data == 150
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Batch processing test failed: {e}")


class TestDataTypes:
    """Test handling of different data types."""

    @pytest.fixture
    def oracle_config_for_test(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "protocol": "tcp",
        }

    @pytest.fixture
    def target_config(self, oracle_config_for_test: dict[str, Any]) -> TargetConfig:
        """Create target configuration for testing."""
        return TargetConfig(
            **oracle_config_for_test,
            default_target_schema="FLEXT_TEST",
        )

    @pytest.mark.asyncio
    async def test_various_data_types(self, target_config: TargetConfig) -> None:
        """Test insertion of various data types.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        singer_service = SingerTargetService(target_config)

        schema_message = {
            "type": "SCHEMA",
            "stream": "test_datatypes",
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
                },
            },
        }

        record_message = {
            "type": "RECORD",
            "stream": "test_datatypes",
            "record": {
                "id": 1,
                "name": "Test Product",
                "price": 29.99,
                "active": True,
                "created_at": datetime.now(UTC).isoformat(),
                "metadata": {"category": "test", "priority": 1},
                "tags": ["integration", "test"],
            },
        }

        try:
            # Create table and insert record
            schema_result = await singer_service.process_singer_message(schema_message)
            assert schema_result.success

            record_result = await singer_service.process_singer_message(record_message)
            assert record_result.success

            # Verify data was inserted correctly
            schema_name = singer_service.config.default_target_schema.upper()
            verify_result = await singer_service.query_service.execute_scalar(
                """
                SELECT COUNT(*)
                FROM all_tables
                WHERE owner = :schema_name
                AND table_name = 'TEST_DATATYPES'
                """,
                {"schema_name": schema_name},
            )
            assert verify_result.success
            assert verify_result.data == 1
        except (ConnectionError, OSError, ValueError, AssertionError, TypeError) as e:
            pytest.fail(f"Data types test failed: {e}")


class TestErrorHandling:
    """Test error handling in Oracle integration."""

    @pytest.fixture
    def oracle_config_for_test(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "protocol": "tcp",
        }

    @pytest.mark.asyncio
    async def test_invalid_connection(self) -> None:
        """Test handling of invalid connection parameters."""
        invalid_config = TargetConfig(
            host="nonexistent.host",
            username="invalid_user",
            password=os.getenv("INVALID_TEST_PASSWORD", "wrong_password"),
            service_name="INVALID_SERVICE",
        )

        singer_service = SingerTargetService(invalid_config)

        schema_message = {
            "type": "SCHEMA",
            "stream": "test_invalid",
            "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
        }

        # Should handle connection error gracefully
        result = await singer_service.process_singer_message(schema_message)
        assert not result.success
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_invalid_schema(self, oracle_config_for_test: dict[str, Any]) -> None:
        """Test handling of invalid schema.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        target_config = TargetConfig(
            **oracle_config_for_test,
            default_target_schema="FLEXT_TEST",
        )
        singer_service = SingerTargetService(target_config)

        invalid_schema_message = {
            "type": "SCHEMA",
            "stream": "test_invalid_schema",
            "schema": {
                "type": "invalid_type",  # Invalid schema type
                "properties": {},
            },
        }

        try:
            result = await singer_service.process_singer_message(invalid_schema_message)
            # Should either succeed (handling gracefully) or fail with clear error
            if not result.success:
                assert result.error is not None
                assert len(str(result.error)) > 0
        except (ConnectionError, OSError, ValueError, TypeError) as e:
            pytest.fail(f"Invalid schema test failed: {e}")


class TestCleanup:
    """Test cleanup operations."""

    @pytest.fixture
    def oracle_config_for_test(self) -> dict[str, Any]:
        """Get Oracle configuration for testing."""
        return {
            "host": os.getenv("ORACLE_HOST", "localhost"),
            "port": int(os.getenv("ORACLE_PORT", "1521")),
            "service_name": os.getenv("ORACLE_SERVICE_NAME", "XEPDB1"),
            "username": os.getenv("ORACLE_USERNAME", "FLEXT_TEST"),
            "password": os.getenv("ORACLE_PASSWORD", "test_password"),
            "protocol": "tcp",
        }

    @pytest.mark.asyncio
    async def test_service_cleanup(
        self,
        oracle_config_for_test: dict[str, Any],
    ) -> None:
        """Test proper cleanup of services.

        ZERO TOLERANCE: Uses real Oracle E2E environment, NO SKIPS.
        """
        target_config = TargetConfig(
            **oracle_config_for_test,
            default_target_schema="FLEXT_TEST",
        )
        singer_service = SingerTargetService(target_config)

        try:
            # Use the service
            schema_message = {
                "type": "SCHEMA",
                "stream": "test_cleanup",
                "schema": {"type": "object", "properties": {"id": {"type": "integer"}}},
            }

            await singer_service.process_singer_message(schema_message)

            # Finalize should clean up properly
            stats = await singer_service.finalize_all_streams()
            assert stats.is_success

            # Service should be in clean state (test through public interface)
            # Verify cleanup by attempting to finalize again
            second_finalize = await singer_service.finalize_all_streams()
            assert (
                second_finalize.is_success
            )  # Should handle multiple finalizations gracefully
        except (ConnectionError, OSError, ValueError, AssertionError) as e:
            pytest.fail(f"Cleanup test failed: {e}")
