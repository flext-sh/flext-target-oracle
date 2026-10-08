"""Basic Usage Example - FLEXT Target Oracle Simple Setup and Processing.

This example demonstrates the fundamental usage patterns for FLEXT Target Oracle,
including configuration, initialization, and basic Singer message processing using
FLEXT ecosystem patterns.

Key Concepts Demonstrated:
    - FlextTargetOracleSettings creation and validation
    - FlextTargetOracle initialization and setup
    - Singer message processing (SCHEMA, RECORD, STATE)
    - r railway-oriented error handling
    - Basic logging and error management

Prerequisites:
    - Oracle database running (localhost:1521/XE)
    - User 'system' with password 'oracle' (or update settings)
    - Python 3.13+ with flext-target-oracle installed

Usage:
    python examples/basic_usage.py

Copyright (c) 2026 FLEXT Team. All rights reserved.
examples/01_basic_usage
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import logging
import os

from flext_cli import u as cli_u

from flext_target_oracle import FlextTargetOracleSettings, m, r, t, u
from flext_target_oracle.utilities import FlextTargetOracle

logging.basicConfig(level=logging.INFO)
logger = u.fetch_logger(__name__)


def create_configuration() -> FlextTargetOracleSettings:
    """Create basic Oracle target configuration.

    Returns:
      FlextTargetOracleSettings: Validated configuration for Oracle target

    Note:
      Using default Oracle XE configuration for simplicity. In production,
      use environment variables or secure configuration management.

    """
    logger.info("Creating Oracle target configuration")
    # ADR-005: project settings live under the TargetOracle namespace.
    settings = FlextTargetOracleSettings.model_validate({
        "TargetOracle": {
            "oracle_host": "localhost",
            "oracle_port": 1521,
            "oracle_service_name": "XE",
            "oracle_user": os.getenv("FLEXT_EXAMPLE_ORACLE_USER", "system"),
            "oracle_password": os.getenv("FLEXT_EXAMPLE_ORACLE_PASSWORD", ""),
            "default_target_schema": "FLEXT_EXAMPLES",
            "batch_size": 100,
            "use_bulk_operations": True,
            "transaction_timeout": 30,
        },
    })
    logger.info(
        "Configuration created: %s:%s/%s",
        settings.TargetOracle.oracle_host,
        settings.TargetOracle.oracle_port,
        settings.TargetOracle.oracle_service_name,
    )
    return settings


def create_sample_schema_message() -> m.Meltano.SingerSchemaMessage:
    """Create sample Singer SCHEMA message for demonstration.

    Returns:
      t.JsonMapping: Singer SCHEMA message for users table

    """
    schema_message: m.Meltano.SingerSchemaMessage = (
        m.Meltano.SingerSchemaMessage.model_validate({
            "type": "SCHEMA",
            "stream": "users",
            "schema": {
                "type": "object",
                "properties": cli_u.Cli.json_dumps({
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "active": {"type": "boolean"},
                }).unwrap(),
                "required": cli_u.Cli.json_dumps(["id", "name", "email"]).unwrap(),
            },
            "key_properties": ["id"],
        })
    )
    return schema_message


def create_sample_record_messages() -> t.SequenceOf[m.Meltano.SingerRecordMessage]:
    """Create sample Singer RECORD messages for demonstration.

    Returns:
      List[t.JsonMapping]: List of Singer RECORD messages

    """
    return [
        m.Meltano.SingerRecordMessage.model_validate({
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2025-01-01T10:00:00Z",
                "active": True,
            },
        }),
        m.Meltano.SingerRecordMessage.model_validate({
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "created_at": "2025-01-01T11:00:00Z",
                "active": True,
            },
        }),
        m.Meltano.SingerRecordMessage.model_validate({
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "created_at": "2025-01-01T12:00:00Z",
                "active": False,
            },
        }),
    ]


def create_sample_state_message() -> m.Meltano.SingerStateMessage:
    """Create sample Singer STATE message for demonstration.

    Returns:
      t.JsonMapping: Singer STATE message with bookmark information

    """
    state_message: m.Meltano.SingerStateMessage = (
        m.Meltano.SingerStateMessage.model_validate({
            "type": "STATE",
            "value": {
                "bookmarks": {
                    "users": {"last_id": 3, "last_updated": "2025-01-01T12:00:00Z"},
                },
            },
        })
    )
    return state_message


def _process_record_messages(
    target: FlextTargetOracle,
    record_messages: t.SequenceOf[t.JsonValue],
) -> None:
    """Process RECORD messages through the target, failing fast on error.

    Raises:
        SystemExit: If any record processing fails.
    """
    for i, record_message in enumerate(record_messages, 1):
        logger.info("Processing record %s/%s", i, len(record_messages))
        record_result = target.process_singer_message(record_message)
        if record_result.failure:
            logger.error("Record %s processing failed: %s", i, record_result.error)
            raise SystemExit(1)
    logger.info("All %s records processed successfully", len(record_messages))


def _log_processing_statistics(stats: object) -> None:
    """Log the final processing statistics summary."""
    logger.info("=== Processing Statistics ===")
    logger.info("Total records processed: %s", stats.total_records)
    logger.info("Successful records: %s", stats.loading_operation.records_loaded)
    logger.info("Failed records: %s", stats.loading_operation.records_failed)
    logger.info("Total batches: %s", stats.streams_processed)


def demonstrate_basic_usage() -> None:
    """Demonstrate basic FLEXT Target Oracle usage patterns.

    This function shows the complete workflow of:
    1. Configuration creation and validation
    2. Target initialization
    3. Singer message processing (SCHEMA, RECORD, STATE)
    4. Error handling with r patterns
    5. Statistics collection and reporting

    Raises:
        SystemExit: If ``validation_result.failure``; or if
            ``connection_result.failure``; or if ``schema_result.failure``; or if
            ``state_result.failure``; or if ``stats_result.failure``; or if
            ``record_result.failure``.
    """
    logger.info("Starting FLEXT Target Oracle basic usage demonstration")
    logger.info("Step 1: Creating configuration")
    settings = create_configuration()
    logger.info("Validating configuration domain rules")
    validation_result = r[bool].ok(value=True)
    if validation_result.failure:
        logger.error("Configuration validation failed: %s", validation_result.error)
        raise SystemExit(1)
    logger.info("Configuration validation successful")
    logger.info("Step 2: Initializing Oracle target")
    target = FlextTargetOracle(settings)
    logger.info("Testing Oracle connection")
    connection_result = target.test_connection()
    if connection_result.failure:
        logger.error("Oracle connection test failed: %s", connection_result.error)
        raise SystemExit(1)
    logger.info("Oracle connection test successful")
    logger.info("Step 3: Processing SCHEMA message")
    schema_message = create_sample_schema_message()
    schema_result = target.process_singer_message(schema_message)
    if schema_result.failure:
        logger.error("Schema processing failed: %s", schema_result.error)
        raise SystemExit(1)
    logger.info("Schema processed successfully - table created/verified")
    logger.info("Step 4: Processing RECORD messages")
    record_messages = create_sample_record_messages()
    _process_record_messages(target, record_messages)
    logger.info("Step 5: Processing STATE message")
    state_message = create_sample_state_message()
    state_result = target.process_singer_message(state_message)
    if state_result.failure:
        logger.error("State processing failed: %s", state_result.error)
        raise SystemExit(1)
    logger.info("State processed successfully")
    logger.info("Step 6: Finalizing target and collecting statistics")
    stats_result = target.finalize()
    if stats_result.failure:
        logger.error("Target finalization failed: %s", stats_result.error)
        raise SystemExit(1)
    _log_processing_statistics(stats_result.value)
    logger.info("Basic usage demonstration completed successfully!")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling patterns with r.

    Shows how to handle various error scenarios gracefully using
    FLEXT error handling patterns.
    """
    logger.info("Demonstrating error handling patterns")
    try:
        # ADR-005: invalid nested values (port 0 violates ge=1) must raise.
        FlextTargetOracleSettings.model_validate({
            "TargetOracle": {
                "oracle_port": 0,
                "oracle_service_name": "XE",
                "oracle_user": os.getenv("FLEXT_EXAMPLE_ORACLE_USER", "test"),
                "oracle_password": os.getenv("FLEXT_EXAMPLE_ORACLE_PASSWORD", ""),
            },
        })
        validation_result = r[bool].ok(value=True)
        if validation_result.failure:
            logger.info("Expected validation error: %s", validation_result.error)
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ) as e:
        logger.info("Configuration creation failed as expected", error=str(e))
    settings = create_configuration()
    target = FlextTargetOracle(settings)
    invalid_message = '{"type": "INVALID", "data": "test"}'
    result = target.write_record(invalid_message)
    if result.failure:
        logger.info("Invalid message handled gracefully: %s", result.error)
    logger.info("Error handling demonstration completed")


def main() -> None:
    """Run the basic usage example."""
    logger.info("FLEXT Target Oracle - Basic Usage Example")
    logger.info("=" * 50)
    demonstrate_basic_usage()
    logger.info("\n%s", "=" * 50)
    logger.info("Running error handling demonstration")
    demonstrate_error_handling()
    logger.info("\n%s", "=" * 50)
    logger.info("Example completed successfully!")
    logger.info("Next steps:")
    logger.info("- Check your Oracle database for the created table and data")
    logger.info("- Try the production_setup.py example for advanced configuration")
    logger.info("- Explore meltano_integration/ for orchestration setup")


if __name__ == "__main__":
    main()
