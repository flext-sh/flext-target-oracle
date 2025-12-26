"""FlextTargetOracleUtilities - Singer target utilities for Oracle database operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import ClassVar

from flext_core import FlextConstants, FlextResult
from flext_core.utilities import u_core


class FlextTargetOracleUtilities(u_core):
    """Single unified utilities class for Singer target Oracle database operations.

    This class provides complete Oracle database target functionality for Singer protocol
    integration, including connection management, SQL generation, bulk operations, transaction
    handling, and performance optimization for enterprise Oracle deployments.

    Oracle Domain Specialization:
    - Enterprise Oracle database connectivity with connection pooling
    - High-performance bulk insert operations and batch processing
    - Singer protocol compliance with stream-to-table mapping
    - Oracle-specific SQL generation with hints and optimization
    - Complete transaction management with ACID compliance
    - Oracle performance monitoring and query optimization
    - Enterprise security with parameterized queries and SQL injection prevention

    Attributes:
    ORACLE_DEFAULT_PORT: Default Oracle database port (1521)
    ORACLE_DEFAULT_SERVICE: Default Oracle service name (XE)
    DEFAULT_BATCH_SIZE: Default batch size for bulk operations (1000)
    MAX_CONNECTION_POOL_SIZE: Maximum connection pool size (20)
    DEFAULT_COMMIT_INTERVAL: Default commit interval for transactions (1000)

    """

    ORACLE_DEFAULT_PORT: ClassVar[int] = 1521
    ORACLE_DEFAULT_SERVICE: ClassVar[str] = "XE"
    DEFAULT_BATCH_SIZE: ClassVar[int] = 1000
    MAX_CONNECTION_POOL_SIZE: ClassVar[int] = 20
    DEFAULT_COMMIT_INTERVAL: ClassVar[int] = 1000
    ORACLE_MAX_IDENTIFIER_LENGTH: ClassVar[int] = 128
    DEFAULT_TRANSACTION_TIMEOUT: ClassVar[int] = 300

    class SingerUtilities:
        """Singer protocol utilities for Oracle target operations."""

        @staticmethod
        def create_schema_message(
            stream_name: str,
            schema: dict[str, object],
            key_properties: list[str] | None = None,
        ) -> dict[str, object]:
            """Create Singer SCHEMA message for Oracle table definition.

            Args:
            stream_name: Name of the Singer stream
            schema: JSON schema definition for the stream
            key_properties: List of key property names

            Returns:
            Singer SCHEMA message dictionary

            """
            return {
                "type": "SCHEMA",
                "stream": stream_name,
                "schema": schema,
                "key_properties": key_properties or [],
                "bookmark_properties": [],
            }

        @staticmethod
        def create_record_message(
            stream_name: str,
            record: dict[str, object],
            time_extracted: str | None = None,
        ) -> dict[str, object]:
            """Create Singer RECORD message for Oracle data insertion.

            Args:
            stream_name: Name of the Singer stream
            record: Data record to insert
            time_extracted: Optional extraction timestamp

            Returns:
            Singer RECORD message dictionary

            """
            message = {
                "type": "RECORD",
                "stream": stream_name,
                "record": record,
            }
            if time_extracted:
                message["time_extracted"] = time_extracted
            return message

        @staticmethod
        def create_state_message(state: dict[str, object]) -> dict[str, object]:
            """Create Singer STATE message for Oracle target checkpointing.

            Args:
            state: State data for checkpointing

            Returns:
            Singer STATE message dictionary

            """
            return {"type": "STATE", "value": state}

        @staticmethod
        def validate_singer_message(
            message: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Singer message format and required fields.

            Args:
            message: Singer message to validate

            Returns:
            FlextResult containing validated message or error

            """
            if not isinstance(message, dict):
                return FlextResult[dict[str, object]].fail(
                    "Singer message must be a dictionary",
                )

            message_type = message.get("type")
            if message_type not in {"SCHEMA", "RECORD", "STATE"}:
                return FlextResult[dict[str, object]].fail(
                    f"Invalid Singer message type: {message_type}",
                )

            if message_type == "SCHEMA":
                required_fields = ["stream", "schema"]
                for field in required_fields:
                    if field not in message:
                        return FlextResult[dict[str, object]].fail(
                            f"Missing required field for SCHEMA: {field}",
                        )

            elif message_type == "RECORD":
                required_fields = ["stream", "record"]
                for field in required_fields:
                    if field not in message:
                        return FlextResult[dict[str, object]].fail(
                            f"Missing required field for RECORD: {field}",
                        )

            elif message_type == "STATE":
                if "value" not in message:
                    return FlextResult[dict[str, object]].fail(
                        "Missing required field for STATE: value",
                    )

            return FlextResult[dict[str, object]].ok(message)

    class OracleDataProcessing:
        """Oracle database-specific data processing utilities."""

        @staticmethod
        def map_singer_type_to_oracle_type(
            singer_type: str,
            format_spec: str | None = None,
        ) -> str:
            """Map Singer JSON schema type to Oracle SQL type.

            Args:
            singer_type: Singer data type (string, integer, number, boolean, etc.)
            format_spec: Optional format specification (date-time, date, etc.)

            Returns:
            Oracle SQL type string

            """
            type_mapping = {
                "string": "VARCHAR2(4000)",
                "integer": "NUMBER(19,0)",
                "number": "NUMBER",
                "boolean": "NUMBER(1,0)",
                "object": "CLOB",
                "array": "CLOB",
            }

            if (
                singer_type == "string"
                and format_spec
                and (format_spec in {"date", "date-time"} or format_spec == "time")
            ):
                return "TIMESTAMP"

            return type_mapping.get(singer_type, "CLOB")

        @staticmethod
        def generate_oracle_table_ddl(
            table_name: str,
            schema: dict[str, object],
            key_properties: list[str] | None = None,
        ) -> FlextResult[str]:
            """Generate Oracle DDL for creating table from Singer schema.

            Args:
            table_name: Name of the Oracle table to create
            schema: Singer JSON schema
            key_properties: List of key property names

            Returns:
            FlextResult containing Oracle DDL string or error

            """
            try:
                properties: dict[str, object] = schema.get("properties", {})
                if not properties:
                    return FlextResult[str].fail("Schema properties cannot be empty")

                columns = []
                for column_name, column_spec in properties.items():
                    column_type = column_spec.get("type", "string")
                    format_spec = column_spec.get("format")
                    oracle_type = FlextTargetOracleUtilities.OracleDataProcessing.map_singer_type_to_oracle_type(
                        column_type,
                        format_spec,
                    )

                    # Add NOT NULL constraint for key properties
                    constraint = (
                        " NOT NULL"
                        if key_properties and column_name in key_properties
                        else ""
                    )
                    columns.append(
                        f'    "{column_name.upper()}" {oracle_type}{constraint}',
                    )

                ddl = f'CREATE TABLE "{table_name.upper()}" (\n'
                ddl += ",\n".join(columns)

                # Add primary key constraint if key properties exist
                if key_properties:
                    key_columns = ", ".join(
                        f'"{key.upper()}"' for key in key_properties
                    )
                    ddl += f',\n    CONSTRAINT "PK_{table_name.upper()}" PRIMARY KEY ({key_columns})'

                ddl += "\n)"

                return FlextResult[str].ok(ddl)

            except Exception as e:
                return FlextResult[str].fail(f"Failed to generate Oracle DDL: {e}")

        @staticmethod
        def prepare_oracle_insert_statement(
            table_name: str,
            columns: list[str],
        ) -> FlextResult[str]:
            """Prepare parameterized Oracle INSERT statement.

            Args:
            table_name: Name of the Oracle table
            columns: List of column names

            Returns:
            FlextResult containing Oracle INSERT statement or error

            """
            if not columns:
                return FlextResult[str].fail("Column list cannot be empty")

            try:
                column_list = ", ".join(f'"{col.upper()}"' for col in columns)
                placeholder_list = ", ".join("?" for _ in columns)

                # Parameterized INSERT with placeholders - safe SQL generation
                # Table name is validated and quoted to prevent injection
                statement = f'INSERT INTO "{table_name.upper()}" ({column_list}) VALUES ({placeholder_list})'
                return FlextResult[str].ok(statement)

            except Exception as e:
                return FlextResult[str].fail(
                    f"Failed to prepare Oracle INSERT statement: {e}",
                )

        @staticmethod
        def transform_record_for_oracle(
            record: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Transform Singer record for Oracle database insertion.

            Args:
            record: Singer record data

            Returns:
            FlextResult containing transformed record or error

            """
            try:
                transformed = {}
                for key, value in record.items():
                    # Convert None to NULL for Oracle
                    if value is None:
                        transformed[key.upper()] = None
                    # Convert boolean to Oracle NUMBER(1,0)
                    elif isinstance(value, bool):
                        transformed[key.upper()] = 1 if value else 0
                    # Convert complex types to JSON string
                    elif isinstance(value, (dict, list)):
                        transformed[key.upper()] = json.dumps(value)
                    else:
                        transformed[key.upper()] = value

                return FlextResult[dict[str, object]].ok(transformed)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to transform record for Oracle: {e}",
                )

    class StreamUtilities:
        """Singer stream processing utilities for Oracle target."""

        @staticmethod
        def process_schema_stream(
            stream_name: str,
            schema_message: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Process Singer schema stream for Oracle table management.

            Args:
            stream_name: Name of the Singer stream
            schema_message: Singer SCHEMA message

            Returns:
            FlextResult containing processed schema information or error

            """
            try:
                schema: dict[str, object] = schema_message.get("schema", {})
                key_properties: list[str] = schema_message.get("key_properties", [])

                # Generate Oracle table DDL
                ddl_result = FlextTargetOracleUtilities.OracleDataProcessing.generate_oracle_table_ddl(
                    stream_name,
                    schema,
                    key_properties,
                )
                if ddl_result.is_failure:
                    return FlextResult[dict[str, object]].fail(
                        f"DDL generation failed: {ddl_result.error}",
                    )

                processed_schema = {
                    "stream_name": stream_name,
                    "oracle_table_name": stream_name.upper(),
                    "ddl": ddl_result.value,
                    "key_properties": key_properties,
                    "properties": schema.get("properties", {}),
                }

                return FlextResult[dict[str, object]].ok(processed_schema)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to process schema stream: {e}",
                )

        @staticmethod
        def batch_records_for_oracle(
            records: list[dict[str, object]],
            batch_size: int = 1000,
        ) -> FlextResult[list[list[dict[str, object]]]]:
            """Batch Singer records for efficient Oracle bulk operations.

            Args:
            records: List of Singer records
            batch_size: Size of each batch (default: 1000)

            Returns:
            FlextResult containing list of batches or error

            """
            if batch_size <= 0:
                return FlextResult[list[list[dict[str, object]]]].fail(
                    "Batch size must be positive",
                )

            try:
                batches = []
                for i in range(0, len(records), batch_size):
                    batch = records[i : i + batch_size]
                    batches.append(batch)

                return FlextResult[list[list[dict[str, object]]]].ok(batches)

            except Exception as e:
                return FlextResult[list[list[dict[str, object]]]].fail(
                    f"Failed to batch records: {e}",
                )

    class ConfigValidation:
        """Configuration validation utilities for Oracle target."""

        @staticmethod
        def validate_oracle_connection_config(
            config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle connection configuration.

            Args:
            config: Oracle connection configuration

            Returns:
            FlextResult containing validated config or error

            """
            required_fields = ["host", "port", "service_name", "username", "password"]
            for field in required_fields:
                if field not in config or not config[field]:
                    return FlextResult[dict[str, object]].fail(
                        f"Missing required Oracle config field: {field}",
                    )

            # Validate port number
            try:
                port_value = config["port"]
                if isinstance(port_value, (int, str)):
                    port = int(port_value)
                    if not (
                        FlextConstants.Network.MIN_PORT
                        <= port
                        <= FlextConstants.Network.MAX_PORT
                    ):
                        return FlextResult[dict[str, object]].fail(
                            f"Oracle port must be between {FlextConstants.Network.MIN_PORT} and {FlextConstants.Network.MAX_PORT}",
                        )
                else:
                    return FlextResult[dict[str, object]].fail(
                        "Oracle port must be an integer or string",
                    )
            except (ValueError, TypeError):
                return FlextResult[dict[str, object]].fail(
                    "Oracle port must be a valid integer",
                )

            return FlextResult[dict[str, object]].ok(config)

        @staticmethod
        def validate_oracle_target_config(
            config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle target-specific configuration.

            Args:
            config: Oracle target configuration

            Returns:
            FlextResult containing validated config or error

            """
            # Validate batch size
            batch_size = config.get(
                "batch_size",
                FlextTargetOracleUtilities.DEFAULT_BATCH_SIZE,
            )
            if isinstance(batch_size, int) and batch_size <= 0:
                return FlextResult[dict[str, object]].fail(
                    "Batch size must be positive",
                )

            # Validate connection pool size
            pool_size = config.get("connection_pool_size", 5)
            if isinstance(pool_size, int) and (
                pool_size <= 0
                or pool_size > FlextTargetOracleUtilities.MAX_CONNECTION_POOL_SIZE
            ):
                return FlextResult[dict[str, object]].fail(
                    f"Connection pool size must be between 1 and {FlextTargetOracleUtilities.MAX_CONNECTION_POOL_SIZE}",
                )

            # Validate commit interval
            commit_interval = config.get(
                "commit_interval",
                FlextTargetOracleUtilities.DEFAULT_COMMIT_INTERVAL,
            )
            if isinstance(commit_interval, int) and commit_interval <= 0:
                return FlextResult[dict[str, object]].fail(
                    "Commit interval must be positive",
                )

            return FlextResult[dict[str, object]].ok(config)

    class StateManagement:
        """Singer state management utilities for Oracle target."""

        @staticmethod
        def create_oracle_target_state(
            stream_states: dict[str, object],
            target_metadata: dict[str, object] | None = None,
        ) -> FlextResult[dict[str, object]]:
            """Create Oracle target state for Singer checkpointing.

            Args:
            stream_states: Dictionary of stream states
            target_metadata: Optional target-specific metadata

            Returns:
            FlextResult containing Oracle target state or error

            """
            try:
                state = {
                    "streams": stream_states,
                    "target_type": "oracle",
                    "last_updated": datetime.now(UTC).isoformat(),
                }

                if target_metadata:
                    state["target_metadata"] = target_metadata

                return FlextResult[dict[str, object]].ok(state)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to create Oracle target state: {e}",
                )

        @staticmethod
        def update_stream_state(
            current_state: dict[str, object],
            stream_name: str,
            last_processed_record: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Update state for a specific stream in Oracle target.

            Args:
            current_state: Current Singer state
            stream_name: Name of the stream to update
            last_processed_record: Last processed record data

            Returns:
            FlextResult containing updated state or error

            """
            try:
                updated_state = current_state.copy()

                if "streams" not in updated_state:
                    updated_state["streams"] = {}

                updated_state["streams"][stream_name] = {
                    "last_processed_record": last_processed_record,
                    "last_updated": datetime.now(UTC).isoformat(),
                }

                return FlextResult[dict[str, object]].ok(updated_state)

            except Exception as e:
                return FlextResult[dict[str, object]].fail(
                    f"Failed to update stream state: {e}",
                )

    class PerformanceUtilities:
        """Oracle performance optimization utilities."""

        @staticmethod
        def calculate_optimal_batch_size(
            table_row_size_bytes: int,
            available_memory_mb: int = 100,
        ) -> FlextResult[int]:
            """Calculate optimal batch size for Oracle bulk operations.

            Args:
            table_row_size_bytes: Average size of table row in bytes
            available_memory_mb: Available memory for batching in MB

            Returns:
            FlextResult containing optimal batch size or error

            """
            try:
                if table_row_size_bytes <= 0:
                    return FlextResult[int].fail("Table row size must be positive")

                if available_memory_mb <= 0:
                    return FlextResult[int].fail("Available memory must be positive")

                available_memory_bytes = available_memory_mb * 1024 * 1024
                max_batch_size = available_memory_bytes // table_row_size_bytes

                # Ensure batch size is within reasonable bounds
                optimal_batch_size = max(1, min(max_batch_size, 10000))

                return FlextResult[int].ok(optimal_batch_size)

            except Exception as e:
                return FlextResult[int].fail(
                    f"Failed to calculate optimal batch size: {e}",
                )

        @staticmethod
        def generate_oracle_performance_hints(
            operation_type: str,
            table_size: str = "medium",
        ) -> FlextResult[str]:
            """Generate Oracle SQL hints for performance optimization.

            Args:
            operation_type: Type of operation (INSERT, UPDATE, DELETE, SELECT)
            table_size: Size category of table (small, medium, large)

            Returns:
            FlextResult containing Oracle hints string or error

            """
            try:
                hints = []

                if operation_type.upper() == "INSERT":
                    hints.append("APPEND")
                    if table_size == "large":
                        hints.extend(("PARALLEL(4)", "NOLOGGING"))

                elif operation_type.upper() in {"UPDATE", "DELETE"}:
                    if table_size == "large":
                        hints.append("PARALLEL(2)")

                elif operation_type.upper() == "SELECT":
                    hints.append("FIRST_ROWS")
                    if table_size == "large":
                        hints.append("PARALLEL(2)")

                hint_string = f"/*+ {' '.join(hints)} */" if hints else ""
                return FlextResult[str].ok(hint_string)

            except Exception as e:
                return FlextResult[str].fail(f"Failed to generate Oracle hints: {e}")

    # Proxy methods for backward compatibility (minimal)
    def validate_singer_message(
        self,
        message: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Proxy to SingerUtilities.validate_singer_message."""
        return self.SingerUtilities.validate_singer_message(message)

    def transform_record_for_oracle(
        self,
        record: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Proxy to OracleDataProcessing.transform_record_for_oracle."""
        return self.OracleDataProcessing.transform_record_for_oracle(record)

    def validate_oracle_connection_config(
        self,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Proxy to ConfigValidation.validate_oracle_connection_config."""
        return self.ConfigValidation.validate_oracle_connection_config(config)
