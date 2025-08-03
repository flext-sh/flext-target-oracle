"""Unit tests for Oracle Loader using flext-db-oracle."""

from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_target_oracle.config import FlextOracleTargetConfig, LoadMethod
from flext_target_oracle.loader import FlextOracleTargetLoader

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3


class TestFlextOracleTargetLoader:
    """Test Oracle Loader implementation."""

    @pytest.fixture
    def sample_config(self) -> FlextOracleTargetConfig:
        """Sample configuration for testing."""
        return FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service="XE",
            oracle_user="test_user",
            oracle_password="test_pass",
            default_target_schema="TEST_SCHEMA",
            batch_size=1000,
            load_method=LoadMethod.INSERT,
        )

    @pytest.fixture
    def mock_loader(
        self,
        sample_config: FlextOracleTargetConfig,
    ) -> FlextOracleTargetLoader:
        """Mock loader with mocked Oracle services."""
        # Since flext-db-oracle imports are commented out, we don't need to mock them
        return FlextOracleTargetLoader(sample_config)

    @pytest.mark.asyncio
    async def test_loader_initialization(
        self,
        sample_config: FlextOracleTargetConfig,
    ) -> None:
        """Test loader initialization."""
        # Since flext-db-oracle imports are commented out, we just test basic initialization
        loader = FlextOracleTargetLoader(sample_config)

        # Verify buffers are initialized
        if loader._record_buffers != {}:
            msg = f"Expected {{}}, got {loader._record_buffers}"
            raise AssertionError(msg)
        assert loader._total_records == 0
        if loader.config != sample_config:
            msg = f"Expected {sample_config}, got {loader.config}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_ensure_table_exists_success(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test ensure_table_exists when table already exists."""
        stream_name = "users"
        schema = {"type": "object", "properties": {"id": {"type": "integer"}}}

        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.get_tables = Mock(return_value=FlextResult.ok(["USERS"]))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader.ensure_table_exists(stream_name, schema)

        assert result.is_success

    @pytest.mark.asyncio
    async def test_load_record_buffering(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test record loading with buffering."""
        result = await mock_loader.load_record("users", {"id": 1, "name": "John"})

        assert result.is_success
        if "users" not in mock_loader._record_buffers:
            msg = f"Expected {'users'} in {mock_loader._record_buffers}"
            raise AssertionError(msg)
        if len(mock_loader._record_buffers["users"]) != 1:
            msg = f"Expected {1}, got {len(mock_loader._record_buffers['users'])}"
            raise AssertionError(msg)
        assert mock_loader._record_buffers["users"][0] == {"id": 1, "name": "John"}

    @pytest.mark.asyncio
    async def test_load_record_batch_flush(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test record loading that triggers batch flush."""
        # Set batch size to 1 to trigger immediate flush
        # Cannot modify batch_size as it's read-only, create new config
        new_config = FlextOracleTargetConfig(
            oracle_host=mock_loader.config.oracle_host,
            oracle_port=mock_loader.config.oracle_port,
            oracle_service=mock_loader.config.oracle_service,
            oracle_user=mock_loader.config.oracle_user,
            oracle_password=mock_loader.config.oracle_password,
            batch_size=1,
        )
        mock_loader.config = new_config

        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.execute_ddl = Mock(return_value=FlextResult.ok(None))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader.load_record("users", {"id": 1, "name": "John"})

        assert result.is_success
        # Buffer should be empty after flush
        if mock_loader._record_buffers["users"] != []:
            msg = f"Expected {[]}, got {mock_loader._record_buffers['users']}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_finalize_all_streams_success(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test successful finalization of all streams."""
        # Add some records to buffers
        mock_loader._record_buffers["users"] = [{"id": 1}, {"id": 2}]
        mock_loader._record_buffers["products"] = [{"id": 1}]

        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.execute_ddl = Mock(return_value=FlextResult.ok(None))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader.finalize_all_streams()

        assert result.is_success
        # Check result.data is not None before indexing
        assert result.data is not None, "Result data should not be None"
        if result.data["total_records"] != EXPECTED_DATA_COUNT:
            msg = f"Expected {3}, got {result.data['total_records']}"
            raise AssertionError(msg)
        assert result.data["successful_records"] == EXPECTED_DATA_COUNT
        if result.data["failed_records"] != 0:
            msg = f"Expected {0}, got {result.data['failed_records']}"
            raise AssertionError(msg)

    @pytest.mark.asyncio
    async def test_flush_batch_empty_buffer(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test flushing empty buffer."""
        result = await mock_loader._flush_batch("users")

        assert result.is_success

    @pytest.mark.asyncio
    async def test_flush_batch_success(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test successful batch flush."""
        # Add records to buffer
        mock_loader._record_buffers["users"] = [{"id": 1}, {"id": 2}]

        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.execute_ddl = Mock(return_value=FlextResult.ok(None))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader._flush_batch("users")

        assert result.is_success
        if mock_loader._total_records != EXPECTED_BULK_SIZE:
            msg = f"Expected {2}, got {mock_loader._total_records}"
            raise AssertionError(msg)
        assert mock_loader._record_buffers["users"] == []  # Buffer cleared

    @pytest.mark.asyncio
    async def test_insert_batch_success(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test successful batch insert."""
        records = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]

        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.execute_ddl = Mock(return_value=FlextResult.ok(None))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader._insert_batch("users", records)

        assert result.is_success

    @pytest.mark.asyncio
    async def test_insert_batch_empty_records(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test batch insert with empty records."""
        result = await mock_loader._insert_batch("users", [])

        assert result.is_success

    @pytest.mark.asyncio
    async def test_create_table_success(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test successful table creation."""
        # Mock the Oracle API completely for unit test
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=None)
        mock_api.execute_ddl = Mock(return_value=FlextResult.ok(None))

        with patch.object(mock_loader, "oracle_api", mock_api):
            result = await mock_loader._create_table("users")

        assert result.is_success
        mock_api.execute_ddl.assert_called_once()

    def test_get_table_name_basic(self, mock_loader: FlextOracleTargetLoader) -> None:
        """Test basic table name generation."""
        table_name = mock_loader.config.get_table_name("users")
        if table_name != "USERS":
            msg = f"Expected {'USERS'}, got {table_name}"
            raise AssertionError(msg)

    def test_get_table_name_with_prefix(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test table name generation with prefix."""
        # table_prefix doesn't exist in real API - test standard behavior
        table_name = mock_loader.config.get_table_name("users")
        if table_name != "USERS":
            msg = f"Expected {'USERS'}, got {table_name}"
            raise AssertionError(msg)

    def test_get_table_name_special_chars(
        self,
        mock_loader: FlextOracleTargetLoader,
    ) -> None:
        """Test table name generation with special characters."""
        table_name = mock_loader.config.get_table_name("user-profiles")
        if table_name != "USER_PROFILES":
            msg = f"Expected {'USER_PROFILES'}, got {table_name}"
            raise AssertionError(msg)

        table_name = mock_loader.config.get_table_name("orders.items")
        if table_name != "ORDERS_ITEMS":
            msg = f"Expected {'ORDERS_ITEMS'}, got {table_name}"
            raise AssertionError(msg)
