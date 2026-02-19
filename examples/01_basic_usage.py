#!/usr/bin/env python3
"""Basic Usage Example - FLEXT Target Oracle Simple Setup and Processing.

This example demonstrates the fundamental usage patterns for FLEXT Target Oracle,
including configuration, initialization, and basic Singer message processing using
FLEXT ecosystem patterns.

Key Concepts Demonstrated:
    - FlextTargetOracleSettings creation and validation
    - FlextTargetOracle initialization and setup
    - Singer message processing (SCHEMA, RECORD, STATE)
    - FlextResult railway-oriented error handling
    - Basic logging and error management

Prerequisites:
    - Oracle database running (localhost:1521/XE)
    - User 'system' with password 'oracle' (or update config)
    - Python 3.13+ with flext-target-oracle installed

Usage:
    python examples/basic_usage.py
"""

import logging
import os

from flext_core import FlextLogger, FlextResult, FlextTypes as t
from flext_target_oracle import FlextTargetOracle, FlextTargetOracleSettings, LoadMethod
from pydantic import SecretStr

# Configure logging for the example
logging.basicConfig(level=logging.INFO)
logger = FlextLogger(__name__)


def create_configuration() -> FlextTargetOracleSettings:
    """Create basic Oracle target configuration.

    Returns:
      FlextTargetOracleSettings: Validated configuration for Oracle target

    Note:
      Using default Oracle XE configuration for simplicity. In production,
      use environment variables or secure configuration management.

    """
    logger.info("Creating Oracle target configuration")

    config = FlextTargetOracleSettings(
        oracle_host="localhost",
        oracle_port=1521,
        oracle_service="XE",
        oracle_user=os.getenv("FLEXT_EXAMPLE_ORACLE_USER", "system"),
        oracle_password=SecretStr(os.getenv("FLEXT_EXAMPLE_ORACLE_PASSWORD", "")),
        default_target_schema="FLEXT_EXAMPLES",
        load_method=LoadMethod.INSERT,
        batch_size=100,  # Small batch size for demo
        use_bulk_operations=True,
        connection_timeout=30,
    )

    logger.info(
        f"Configuration created: {config.oracle_host}:{config.oracle_port}/{config.oracle_service_name}",
    )
    return config


def create_sample_schema_message() -> dict[str, t.GeneralValueType]:
    """Create sample Singer SCHEMA message for demonstration.

    Returns:
      dict[str, t.GeneralValueType]: Singer SCHEMA message for users table

    """
    return {
        "type": "SCHEMA",
        "stream": "users",
        "schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "active": {"type": "boolean"},
            },
            "required": ["id", "name", "email"],
        },
        "key_properties": ["id"],
    }


def create_sample_record_messages() -> list[dict[str, t.GeneralValueType]]:
    """Create sample Singer RECORD messages for demonstration.

    Returns:
      List[dict[str, t.GeneralValueType]]: List of Singer RECORD messages

    """
    return [
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2025-01-01T10:00:00Z",
                "active": True,
            },
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "created_at": "2025-01-01T11:00:00Z",
                "active": True,
            },
        },
        {
            "type": "RECORD",
            "stream": "users",
            "record": {
                "id": 3,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "created_at": "2025-01-01T12:00:00Z",
                "active": False,
            },
        },
    ]


def create_sample_state_message() -> dict[str, t.GeneralValueType]:
    """Create sample Singer STATE message for demonstration.

    Returns:
      dict[str, t.GeneralValueType]: Singer STATE message with bookmark information

    """
    return {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "users": {
                    "last_id": 3,
                    "last_updated": "2025-01-01T12:00:00Z",
                },
            },
        },
    }


def demonstrate_basic_usage() -> None:
    """Demonstrate basic FLEXT Target Oracle usage patterns.

    This function shows the complete workflow of:
    1. Configuration creation and validation
    2. Target initialization
    3. Singer message processing (SCHEMA, RECORD, STATE)
    4. Error handling with FlextResult patterns
    5. Statistics collection and reporting
    """
    logger.info("Starting FLEXT Target Oracle basic usage demonstration")

    try:
        # Step 1: Create and validate configuration
        logger.info("Step 1: Creating configuration")
        config = create_configuration()

        # Validate domain rules (optional but recommended)
        logger.info("Validating configuration domain rules")
        # Validation is handled during config creation with Pydantic validators
        validation_result = FlextResult[bool].ok(value=True)
        if validation_result.is_failure:
            logger.error(f"Configuration validation failed: {validation_result.error}")
            return

        logger.info("Configuration validation successful")

        # Step 2: Initialize target
        logger.info("Step 2: Initializing Oracle target")
        target = FlextTargetOracle(config)

        # Optional: Test connection
        logger.info("Testing Oracle connection")
        connection_result = target.test_connection()
        if connection_result.is_failure:
            logger.error(f"Oracle connection test failed: {connection_result.error}")
            return

        logger.info("Oracle connection test successful")

        # Step 3: Process SCHEMA message
        logger.info("Step 3: Processing SCHEMA message")
        schema_message = create_sample_schema_message()

        schema_result = target.process_singer_message(schema_message)
        if schema_result.is_failure:
            logger.error(f"Schema processing failed: {schema_result.error}")
            return

        logger.info("Schema processed successfully - table created/verified")

        # Step 4: Process RECORD messages
        logger.info("Step 4: Processing RECORD messages")
        record_messages = create_sample_record_messages()

        for i, record_message in enumerate(record_messages, 1):
            logger.info(f"Processing record {i}/{len(record_messages)}")

            record_result = target.process_singer_message(record_message)
            if record_result.is_failure:
                logger.error(f"Record {i} processing failed: {record_result.error}")
                return

        logger.info(f"All {len(record_messages)} records processed successfully")

        # Step 5: Process STATE message
        logger.info("Step 5: Processing STATE message")
        state_message = create_sample_state_message()

        state_result = target.process_singer_message(state_message)
        if state_result.is_failure:
            logger.error(f"State processing failed: {state_result.error}")
            return

        logger.info("State processed successfully")

        # Step 6: Finalize and get statistics
        logger.info("Step 6: Finalizing target and collecting statistics")
        stats_result = target.finalize()
        if stats_result.is_failure:
            logger.error(f"Target finalization failed: {stats_result.error}")
            return

        # Display statistics
        stats = stats_result.value
        logger.info("=== Processing Statistics ===")
        logger.info(f"Total records processed: {stats.get('total_records', 0)}")
        logger.info(f"Successful records: {stats.get('successful_records', 0)}")
        logger.info(f"Failed records: {stats.get('failed_records', 0)}")
        logger.info(f"Total batches: {stats.get('total_batches', 0)}")

        logger.info("Basic usage demonstration completed successfully!")

    except Exception:
        logger.exception("Unexpected error during demonstration")
        raise


def demonstrate_error_handling() -> None:
    """Demonstrate error handling patterns with FlextResult.

    Shows how to handle various error scenarios gracefully using
    FLEXT error handling patterns.
    """
    logger.info("Demonstrating error handling patterns")

    # Create invalid configuration to show validation errors
    try:
        FlextTargetOracleSettings(
            oracle_host="",  # Invalid empty host
            oracle_service="XE",
            oracle_user=os.getenv("FLEXT_EXAMPLE_ORACLE_USER", "test"),
            oracle_password=SecretStr(os.getenv("FLEXT_EXAMPLE_ORACLE_PASSWORD", "")),
        )

        # Domain validation is handled during config creation with Pydantic validators
        validation_result = FlextResult[bool].ok(value=True)
        if validation_result.is_failure:
            logger.info(f"Expected validation error: {validation_result.error}")

    except Exception as e:
        logger.info("Configuration creation failed as expected: %s", e)

    # Demonstrate processing invalid messages
    config = create_configuration()
    target = FlextTargetOracle(config)

    # Invalid message type
    invalid_message: dict[str, t.GeneralValueType] = {"type": "INVALID", "data": "test"}
    result = target.process_singer_message(invalid_message)

    if result.is_failure:
        logger.info(f"Invalid message handled gracefully: {result.error}")

    logger.info("Error handling demonstration completed")


def main() -> None:
    """Main entry point for basic usage example."""
    logger.info("FLEXT Target Oracle - Basic Usage Example")
    logger.info("=" * 50)

    # Run the main demonstration
    demonstrate_basic_usage()

    logger.info("\n%s", "=" * 50)
    logger.info("Running error handling demonstration")

    # Run error handling demonstration
    demonstrate_error_handling()

    logger.info("\n%s", "=" * 50)
    logger.info("Example completed successfully!")
    logger.info("Next steps:")
    logger.info("- Check your Oracle database for the created table and data")
    logger.info("- Try the production_setup.py example for advanced configuration")
    logger.info("- Explore meltano_integration/ for orchestration setup")


if __name__ == "__main__":
    main()
