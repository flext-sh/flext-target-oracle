#!/usr/bin/env python3
"""Isolated test for exceptions hierarchy without external dependencies."""

import os
import pathlib
import sys
import traceback

sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent, "src"))

# Import directly from the exceptions module file
import importlib.util

spec = importlib.util.spec_from_file_location(
    "exceptions",
    "src/flext_target_oracle/exceptions.py",
)
exceptions_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exceptions_module)

# Import all exception classes
FlextException = exceptions_module.FlextException
FlextDomainException = exceptions_module.FlextDomainException
FlextApplicationException = exceptions_module.FlextApplicationException
FlextInfrastructureException = exceptions_module.FlextInfrastructureException
OracleTargetDomainException = exceptions_module.OracleTargetDomainException
InvalidSingerRecordException = exceptions_module.InvalidSingerRecordException
InvalidSchemaException = exceptions_module.InvalidSchemaException
TargetConfigurationException = exceptions_module.TargetConfigurationException
OracleTargetApplicationException = exceptions_module.OracleTargetApplicationException
StreamProcessingException = exceptions_module.StreamProcessingException
BatchProcessingException = exceptions_module.BatchProcessingException
LoadOperationException = exceptions_module.LoadOperationException
OracleTargetInfrastructureException = (
    exceptions_module.OracleTargetInfrastructureException
)
OracleConnectionException = exceptions_module.OracleConnectionException
OracleQueryException = exceptions_module.OracleQueryException
OracleTableException = exceptions_module.OracleTableException


def test_exception_hierarchy() -> None:
    """Test exception class hierarchy."""
    # Test FlextException is base
    assert issubclass(FlextDomainException, FlextException)
    assert issubclass(FlextApplicationException, FlextException)
    assert issubclass(FlextInfrastructureException, FlextException)

    # Test domain exception hierarchy
    assert issubclass(OracleTargetDomainException, FlextDomainException)
    assert issubclass(InvalidSingerRecordException, OracleTargetDomainException)
    assert issubclass(InvalidSchemaException, OracleTargetDomainException)
    assert issubclass(TargetConfigurationException, OracleTargetDomainException)

    # Test application exception hierarchy
    assert issubclass(OracleTargetApplicationException, FlextApplicationException)
    assert issubclass(StreamProcessingException, OracleTargetApplicationException)
    assert issubclass(BatchProcessingException, OracleTargetApplicationException)
    assert issubclass(LoadOperationException, OracleTargetApplicationException)

    # Test infrastructure exception hierarchy
    assert issubclass(OracleTargetInfrastructureException, FlextInfrastructureException)
    assert issubclass(OracleConnectionException, OracleTargetInfrastructureException)
    assert issubclass(OracleQueryException, OracleTargetInfrastructureException)
    assert issubclass(OracleTableException, OracleTargetInfrastructureException)


def test_domain_exceptions() -> None:
    """Test domain exception functionality."""
    # Test InvalidSingerRecordException
    record_data = {"type": "INVALID", "stream": "test"}
    exc = InvalidSingerRecordException(
        record_type="INVALID",
        message="Missing required field",
        record_data=record_data,
    )

    if exc.record_type != "INVALID":
        msg = f"Expected {'INVALID'}, got {exc.record_type}"
        raise AssertionError(msg)
    assert exc.record_data == record_data
    if exc.code != "INVALID_SINGER_RECORD":
        msg = f"Expected {'INVALID_SINGER_RECORD'}, got {exc.code}"
        raise AssertionError(msg)
    if "Invalid Singer record of type 'INVALID'" not in str(exc):
        msg = f"Expected {"Invalid Singer record of type 'INVALID'"} in {exc!s}"
        raise AssertionError(msg)
    if exc.context["record_type"] != "INVALID":
        msg = f"Expected {'INVALID'}, got {exc.context['record_type']}"
        raise AssertionError(msg)
    assert exc.context["record_data"] == record_data

    # Test InvalidSchemaException
    schema_data = {"type": "object", "properties": {}}
    exc = InvalidSchemaException(
        schema_name="test_schema",
        message="Empty properties",
        schema_data=schema_data,
    )

    if exc.schema_name != "test_schema":
        msg = f"Expected {'test_schema'}, got {exc.schema_name}"
        raise AssertionError(msg)
    assert exc.schema_data == schema_data
    if exc.code != "INVALID_SCHEMA":
        msg = f"Expected {'INVALID_SCHEMA'}, got {exc.code}"
        raise AssertionError(msg)
    if "Invalid schema 'test_schema'" not in str(exc):
        msg = f"Expected {"Invalid schema 'test_schema'"} in {exc!s}"
        raise AssertionError(msg)

    # Test TargetConfigurationException
    config_data = {"host": "", "port": 1521}
    exc = TargetConfigurationException(
        field="host",
        message="Cannot be empty",
        config_data=config_data,
    )

    if exc.field != "host":
        msg = f"Expected {'host'}, got {exc.field}"
        raise AssertionError(msg)
    assert exc.config_data == config_data
    if exc.code != "INVALID_TARGET_CONFIG":
        msg = f"Expected {'INVALID_TARGET_CONFIG'}, got {exc.code}"
        raise AssertionError(msg)
    if "Invalid configuration for field 'host'" not in str(exc):
        msg = f"Expected {"Invalid configuration for field 'host'"} in {exc!s}"
        raise AssertionError(msg)


def test_application_exceptions() -> None:
    """Test application exception functionality."""
    # Test StreamProcessingException
    error_details = {"error_count": 5, "failed_records": [1, 2, 3]}
    exc = StreamProcessingException(
        stream_name="test_stream",
        message="Multiple record failures",
        error_details=error_details,
    )

    if exc.stream_name != "test_stream":
        msg = f"Expected {'test_stream'}, got {exc.stream_name}"
        raise AssertionError(msg)
    assert exc.error_details == error_details
    if exc.code != "STREAM_PROCESSING_ERROR":
        msg = f"Expected {'STREAM_PROCESSING_ERROR'}, got {exc.code}"
        raise AssertionError(msg)
    if "Stream processing error for 'test_stream'" not in str(exc):
        msg = f"Expected {"Stream processing error for 'test_stream'"} in {exc!s}"
        raise AssertionError(msg)

    # Test BatchProcessingException
    batch_data = {"batch_size": 1000, "processed": 800}
    exc = BatchProcessingException(
        batch_id="batch_001",
        record_count=1000,
        message="Timeout during processing",
        batch_data=batch_data,
    )

    if exc.batch_id != "batch_001":
        msg = f"Expected {'batch_001'}, got {exc.batch_id}"
        raise AssertionError(msg)
    assert exc.record_count == 1000
    if exc.batch_data != batch_data:
        msg = f"Expected {batch_data}, got {exc.batch_data}"
        raise AssertionError(msg)
    assert exc.code == "BATCH_PROCESSING_ERROR"
    if "Batch processing error for batch 'batch_001'" not in str(exc):
        msg = f"Expected {"Batch processing error for batch 'batch_001'"} in {exc!s}"
        raise AssertionError(msg)

    # Test LoadOperationException
    operation_data = {"rows_affected": 0, "sql_state": "23000"}
    exc = LoadOperationException(
        table_name="test_table",
        operation="INSERT",
        message="Constraint violation",
        operation_data=operation_data,
    )

    if exc.table_name != "test_table":
        msg = f"Expected {'test_table'}, got {exc.table_name}"
        raise AssertionError(msg)
    assert exc.operation == "INSERT"
    if exc.operation_data != operation_data:
        msg = f"Expected {operation_data}, got {exc.operation_data}"
        raise AssertionError(msg)
    assert exc.code == "LOAD_OPERATION_ERROR"
    if "Load operation 'INSERT' failed for table 'test_table'" not in str(exc):
        msg = f"Expected {"Load operation 'INSERT' failed for table 'test_table'"} in {exc!s}"
        raise AssertionError(msg)


def test_infrastructure_exceptions() -> None:
    """Test infrastructure exception functionality."""
    # Test OracleConnectionException
    connection_details = {"timeout": 30, "ssl": False}
    exc = OracleConnectionException(
        host="localhost",
        port=1521,
        service_name="XE",
        message="Connection timeout",
        connection_details=connection_details,
    )

    if exc.host != "localhost":
        msg = f"Expected {'localhost'}, got {exc.host}"
        raise AssertionError(msg)
    assert exc.port == 1521
    if exc.service_name != "XE":
        msg = f"Expected {'XE'}, got {exc.service_name}"
        raise AssertionError(msg)
    assert exc.connection_details == connection_details
    if exc.code != "ORACLE_CONNECTION_ERROR":
        msg = f"Expected {'ORACLE_CONNECTION_ERROR'}, got {exc.code}"
        raise AssertionError(msg)
    if "Oracle connection error to localhost:1521/XE" not in str(exc):
        msg = f"Expected {'Oracle connection error to localhost:1521/XE'} in {exc!s}"
        raise AssertionError(msg)

    # Test OracleQueryException
    query = "SELECT * FROM non_existent_table"
    query_params = {"limit": 100}
    exc = OracleQueryException(
        query=query,
        message="Table does not exist",
        query_params=query_params,
    )

    if exc.query != query:
        msg = f"Expected {query}, got {exc.query}"
        raise AssertionError(msg)
    assert exc.query_params == query_params
    if exc.code != "ORACLE_QUERY_ERROR":
        msg = f"Expected {'ORACLE_QUERY_ERROR'}, got {exc.code}"
        raise AssertionError(msg)
    if "Oracle query execution error" not in str(exc):
        msg = f"Expected {'Oracle query execution error'} in {exc!s}"
        raise AssertionError(msg)

    # Test OracleTableException
    table_details = {"column_count": 10, "row_count": 1000}
    exc = OracleTableException(
        table_name="test_table",
        schema_name="test_schema",
        operation="CREATE",
        message="Table already exists",
        table_details=table_details,
    )

    if exc.table_name != "test_table":
        msg = f"Expected {'test_table'}, got {exc.table_name}"
        raise AssertionError(msg)
    assert exc.schema_name == "test_schema"
    if exc.operation != "CREATE":
        msg = f"Expected {'CREATE'}, got {exc.operation}"
        raise AssertionError(msg)
    assert exc.table_details == table_details
    if exc.code != "ORACLE_TABLE_ERROR":
        msg = f"Expected {'ORACLE_TABLE_ERROR'}, got {exc.code}"
        raise AssertionError(msg)
    if "Oracle table operation 'CREATE' failed for test_schema.test_table" not in str(
        exc,
    ):
        msg = f"Expected {"Oracle table operation 'CREATE' failed for test_schema.test_table"} in {exc!s}"
        raise AssertionError(msg)


def test_minimal_instantiation() -> None:
    """Test that exceptions can be created with minimal parameters."""
    # Test domain exceptions
    exc1 = InvalidSingerRecordException("RECORD", "Invalid format")
    if exc1.record_type != "RECORD":
        msg = f"Expected {'RECORD'}, got {exc1.record_type}"
        raise AssertionError(msg)
    assert exc1.record_data is None

    # Test application exceptions
    exc2 = StreamProcessingException("stream1", "Processing failed")
    if exc2.stream_name != "stream1":
        msg = f"Expected {'stream1'}, got {exc2.stream_name}"
        raise AssertionError(msg)
    assert exc2.error_details is None

    # Test infrastructure exceptions
    exc3 = OracleConnectionException("host", 1521, "XE", "Connection failed")
    if exc3.host != "host":
        msg = f"Expected {'host'}, got {exc3.host}"
        raise AssertionError(msg)
    assert exc3.connection_details is None


def main() -> int | None:
    """Run all tests."""
    try:
        test_exception_hierarchy()
        test_domain_exceptions()
        test_application_exceptions()
        test_infrastructure_exceptions()
        test_minimal_instantiation()

        return 0

    except (RuntimeError, ValueError, TypeError):
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
