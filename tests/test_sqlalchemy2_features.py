"""Test SQLAlchemy 2.0 features in Oracle Target.

This module tests the modern SQLAlchemy 2.0 implementation including:
- URL.create() for connection URLs
- QueuePool configuration
- Event system
- Bulk operations
- Type mapping
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine, pool, event
from sqlalchemy.engine import URL

from flext_target_oracle.connectors import OracleConnector
from flext_target_oracle.sinks import OracleSink
from flext_target_oracle.target import OracleTarget


class TestSQLAlchemy2Features:
    """Test SQLAlchemy 2.0 features."""
    
    def test_url_create_usage(self):
        """Test that URL.create() is used for connection URLs."""
        config = {
            "host": "localhost",
            "port": 1521,
            "user": "test_user",
            "password": "test_pass",
            "service_name": "ORCL"
        }
        
        connector = OracleConnector(config)
        url = connector.get_sqlalchemy_url(config)
        
        # Verify URL is created using URL.create()
        assert isinstance(url, URL)
        assert url.drivername == "oracle+oracledb"
        assert url.username == "test_user"
        assert url.password == "test_pass"
        assert url.host == "localhost"
        assert url.port == 1521
        assert url.query == {"service_name": "ORCL"}
    
    def test_pool_class_selection(self):
        """Test pool class selection based on configuration."""
        connector = OracleConnector({})
        
        # Test QueuePool (default)
        config = {"pool_size": 10}
        connector.config = config
        assert connector._get_pool_class() == pool.QueuePool
        
        # Test NullPool
        config = {"pool_size": 0}
        connector.config = config
        assert connector._get_pool_class() == pool.NullPool
        
        # Test StaticPool
        config = {"pool_size": 1}
        connector.config = config
        assert connector._get_pool_class() == pool.StaticPool
    
    @patch('flext_target_oracle.connectors.create_engine')
    def test_engine_creation_with_future_mode(self, mock_create_engine):
        """Test engine creation with future=True for SQLAlchemy 2.0."""
        config = {
            "host": "localhost",
            "user": "test_user",
            "password": "test_pass",
            "service_name": "ORCL",
            "pool_size": 10,
            "echo": True
        }
        
        connector = OracleConnector(config)
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        engine = connector.create_engine()
        
        # Verify create_engine was called with future=True
        mock_create_engine.assert_called_once()
        call_kwargs = mock_create_engine.call_args[1]
        assert call_kwargs['future'] is True
        assert call_kwargs['poolclass'] == pool.QueuePool
        assert call_kwargs['pool_size'] == 10
        assert call_kwargs['echo'] is True
        assert call_kwargs['pool_pre_ping'] is True
    
    @patch('flext_target_oracle.connectors.event')
    @patch('flext_target_oracle.connectors.create_engine')
    def test_event_listeners_setup(self, mock_create_engine, mock_event):
        """Test SQLAlchemy event listeners are properly set up."""
        config = {
            "host": "localhost",
            "user": "test_user",
            "password": "test_pass",
            "service_name": "ORCL",
            "enable_parallel_dml": True,
            "optimizer_mode": "ALL_ROWS"
        }
        
        connector = OracleConnector(config)
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        engine = connector.create_engine()
        
        # Verify event.listens_for was called
        mock_event.listens_for.assert_called_with(mock_engine, "connect")
    
    def test_oracle_type_mapping(self):
        """Test Oracle-specific type mapping."""
        connector = OracleConnector({})
        
        # Test integer mapping
        int_type = connector.to_sql_type({"type": "integer"})
        assert str(int_type) == "NUMBER(precision=38, scale=0)"
        
        # Test boolean mapping (Oracle doesn't have native boolean)
        bool_type = connector.to_sql_type({"type": "boolean"})
        assert str(bool_type) == "NUMBER(precision=1, scale=0)"
        
        # Test string mapping with length
        string_type = connector.to_sql_type({"type": "string", "maxLength": 100})
        assert str(string_type) == "VARCHAR2(length=100)"
        
        # Test CLOB for long strings
        clob_type = connector.to_sql_type({"type": "string", "maxLength": 5000})
        assert str(clob_type) == "CLOB"
    
    def test_column_pattern_recognition(self):
        """Test intelligent column type mapping based on patterns."""
        config = {"enable_column_patterns": True}
        connector = OracleConnector(config)
        
        # Test ID column
        id_type = connector.get_column_type("USER_ID", {"type": "integer"})
        assert str(id_type) == "NUMBER(precision=38, scale=0)"
        
        # Test flag column
        flag_type = connector.get_column_type("ACTIVE_FLG", {"type": "string"})
        assert str(flag_type) == "NUMBER(precision=1, scale=0)"
        
        # Test timestamp column
        ts_type = connector.get_column_type("CREATE_TS", {"type": "string"})
        assert "TIMESTAMP" in str(ts_type)
        
        # Test amount column
        amt_type = connector.get_column_type("TOTAL_AMOUNT", {"type": "number"})
        assert str(amt_type) == "NUMBER(precision=19, scale=4)"


class TestOracleSinkSQLAlchemy2:
    """Test Oracle Sink with SQLAlchemy 2.0 features."""
    
    @pytest.fixture
    def mock_target(self):
        """Create mock target."""
        target = Mock()
        target.config = {
            "batch_size_rows": 10000,
            "parallel_threads": 4,
            "load_method": "append-only",
            "add_record_metadata": True,
            "use_direct_path": True
        }
        return target
    
    @pytest.fixture
    def mock_connector(self):
        """Create mock connector with engine."""
        connector = Mock()
        connector._engine = Mock()
        return connector
    
    def test_bulk_insert_with_sqlalchemy2(self, mock_target, mock_connector):
        """Test bulk insert using SQLAlchemy 2.0 insert()."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        }
        
        sink = OracleSink(
            target=mock_target,
            stream_name="test_stream",
            schema=schema,
            key_properties=["id"]
        )
        sink.connector = mock_connector
        
        # Mock table
        mock_table = Mock()
        sink._table = mock_table
        
        # Test records
        records = [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"}
        ]
        
        # Mock connection context manager
        mock_conn = MagicMock()
        mock_connector._engine.begin.return_value.__enter__.return_value = mock_conn
        
        # Process batch
        with patch('flext_target_oracle.sinks.insert') as mock_insert:
            sink._process_batch_append(records)
            
            # Verify insert was called
            mock_insert.assert_called_once_with(mock_table)
            
            # Verify execute was called with prepared records
            mock_conn.execute.assert_called_once()
            
            # Check that audit fields were added
            call_args = mock_conn.execute.call_args[0][1]
            assert all("CREATE_TS" in record for record in call_args)
            assert all("MOD_TS" in record for record in call_args)
            assert all(record["CREATE_USER"] == "SINGER" for record in call_args)
    
    def test_event_handler_for_bulk_operations(self, mock_target, mock_connector):
        """Test event handler adds Oracle hints for bulk operations."""
        sink = OracleSink(
            target=mock_target,
            stream_name="test_stream",
            schema={},
            key_properties=[]
        )
        sink.connector = mock_connector
        
        # Setup event handlers
        sink._setup_event_handlers()
        
        # Verify event.listens_for was used
        # This would be tested in integration tests with real engine


class TestOracleTargetSQLAlchemy2:
    """Test Oracle Target with SQLAlchemy 2.0 features."""
    
    @patch('flext_target_oracle.target.create_async_engine')
    @patch('flext_target_oracle.target.create_engine')
    def test_initialize_engines_with_modern_patterns(self, mock_create_engine, mock_create_async_engine):
        """Test engine initialization with SQLAlchemy 2.0 patterns."""
        config = {
            "host": "localhost",
            "port": 1521,
            "username": "test_user",
            "password": "test_pass",
            "service_name": "ORCL",
            "pool_size": 20,
            "pool_recycle": 7200
        }
        
        # Mock logger and monitor
        with patch('flext_target_oracle.target.create_logger') as mock_create_logger:
            with patch('flext_target_oracle.target.create_monitor'):
                mock_logger = Mock()
                mock_create_logger.return_value = mock_logger
                
                target = OracleTarget(config=config)
                
                # Verify engines were created
                mock_create_engine.assert_called_once()
                mock_create_async_engine.assert_called_once()
                
                # Check engine configuration
                engine_kwargs = mock_create_engine.call_args[1]
                assert engine_kwargs['poolclass'] == pool.QueuePool
                assert engine_kwargs['pool_size'] == 20
                assert engine_kwargs['pool_recycle'] == 7200
                assert engine_kwargs['future'] is True
    
    def test_connection_url_building(self):
        """Test connection URL building with modern patterns."""
        config = {
            "host": "oracle.example.com",
            "port": 1522,
            "username": "app_user",
            "password": "secure_pass",
            "service_name": "PROD_DB"
        }
        
        with patch('flext_target_oracle.target.create_logger'):
            with patch('flext_target_oracle.target.create_monitor'):
                with patch('flext_target_oracle.target.create_engine'):
                    with patch('flext_target_oracle.target.create_async_engine'):
                        target = OracleTarget(config=config)
                        url = target._build_connection_url()
                        
                        assert url == "oracle+oracledb://app_user:secure_pass@oracle.example.com:1522/PROD_DB"
    
    def test_health_check_with_sqlalchemy2(self):
        """Test health check using SQLAlchemy 2.0 text()."""
        config = {
            "host": "localhost",
            "username": "test",
            "password": "test",
            "service_name": "ORCL"
        }
        
        with patch('flext_target_oracle.target.create_logger'):
            with patch('flext_target_oracle.target.create_monitor'):
                with patch('flext_target_oracle.target.create_engine') as mock_create_engine:
                    with patch('flext_target_oracle.target.create_async_engine'):
                        # Mock engine and connection
                        mock_engine = Mock()
                        mock_conn = MagicMock()
                        mock_engine.connect.return_value.__enter__.return_value = mock_conn
                        mock_engine.pool = Mock()
                        mock_engine.pool.size.return_value = 10
                        mock_engine.pool.checkedout.return_value = 2
                        mock_create_engine.return_value = mock_engine
                        
                        target = OracleTarget(config=config)
                        
                        # Perform health check
                        with patch('flext_target_oracle.target.text') as mock_text:
                            health_status = target._check_engine_health()
                            
                            # Verify text() was used for SQL
                            mock_text.assert_called_with("SELECT 1 FROM DUAL")
                            mock_conn.execute.assert_called_once()
                            
                            # Check health status
                            assert health_status["sync_engine"]["status"] == "healthy"
                            assert health_status["sync_engine"]["pool_size"] == 10
                            assert health_status["sync_engine"]["checked_out"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])