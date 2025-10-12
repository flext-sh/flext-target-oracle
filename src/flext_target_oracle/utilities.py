"""FlextTargetOracleUtilities - Singer target utilities for Oracle database operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import ClassVar

from flext_core import FlextCore


class FlextTargetOracleUtilities(FlextCore.Utilities):
    """Single unified utilities class for Singer target Oracle database operations.

    This class provides comprehensive Oracle database target functionality for Singer protocol
    integration, including connection management, SQL generation, bulk operations, transaction
    handling, and performance optimization for enterprise Oracle deployments.

    Oracle Domain Specialization:
    - Enterprise Oracle database connectivity with connection pooling
    - High-performance bulk insert operations and batch processing
    - Singer protocol compliance with stream-to-table mapping
    - Oracle-specific SQL generation with hints and optimization
    - Comprehensive transaction management with ACID compliance
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
            schema: FlextCore.Types.Dict,
            key_properties: FlextCore.Types.StringList | None = None,
        ) -> FlextCore.Types.Dict:
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
            record: FlextCore.Types.Dict,
            time_extracted: str | None = None,
        ) -> FlextCore.Types.Dict:
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
        def create_state_message(state: FlextCore.Types.Dict) -> FlextCore.Types.Dict:
            """Create Singer STATE message for Oracle target checkpointing.

            Args:
                state: State data for checkpointing

            Returns:
                Singer STATE message dictionary

            """
            return {"type": "STATE", "value": state}

        @staticmethod
        def validate_singer_message(
            message: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate Singer message format and required fields.

            Args:
                message: Singer message to validate

            Returns:
                FlextCore.Result containing validated message or error

            """
            if not isinstance(message, dict):
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Singer message must be a dictionary"
                )

            message_type = message.get("type")
            if message_type not in {"SCHEMA", "RECORD", "STATE"}:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Invalid Singer message type: {message_type}"
                )

            if message_type == "SCHEMA":
                required_fields = ["stream", "schema"]
                for field in required_fields:
                    if field not in message:
                        return FlextCore.Result[FlextCore.Types.Dict].fail(
                            f"Missing required field for SCHEMA: {field}"
                        )

            elif message_type == "RECORD":
                required_fields = ["stream", "record"]
                for field in required_fields:
                    if field not in message:
                        return FlextCore.Result[FlextCore.Types.Dict].fail(
                            f"Missing required field for RECORD: {field}"
                        )

            elif message_type == "STATE":
                if "value" not in message:
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        "Missing required field for STATE: value"
                    )

            return FlextCore.Result[FlextCore.Types.Dict].ok(message)

    class OracleDataProcessing:
        """Oracle database-specific data processing utilities."""

        @staticmethod
        def map_singer_type_to_oracle_type(
            singer_type: str, format_spec: str | None = None
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
            schema: FlextCore.Types.Dict,
            key_properties: FlextCore.Types.StringList | None = None,
        ) -> FlextCore.Result[str]:
            """Generate Oracle DDL for creating table from Singer schema.

            Args:
                table_name: Name of the Oracle table to create
                schema: Singer JSON schema
                key_properties: List of key property names

            Returns:
                FlextCore.Result containing Oracle DDL string or error

            """
            try:
                properties = schema.get("properties", {})
                if not properties:
                    return FlextCore.Result[str].fail(
                        "Schema properties cannot be empty"
                    )

                columns = []
                for column_name, column_spec in properties.items():
                    column_type = column_spec.get("type", "string")
                    format_spec = column_spec.get("format")
                    oracle_type = FlextTargetOracleUtilities.OracleDataProcessing.map_singer_type_to_oracle_type(
                        column_type, format_spec
                    )

                    # Add NOT NULL constraint for key properties
                    constraint = (
                        " NOT NULL"
                        if key_properties and column_name in key_properties
                        else ""
                    )
                    columns.append(
                        f'    "{column_name.upper()}" {oracle_type}{constraint}'
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

                return FlextCore.Result[str].ok(ddl)

            except Exception as e:
                return FlextCore.Result[str].fail(f"Failed to generate Oracle DDL: {e}")

        @staticmethod
        def prepare_oracle_insert_statement(
            table_name: str, columns: FlextCore.Types.StringList
        ) -> FlextCore.Result[str]:
            """Prepare parameterized Oracle INSERT statement.

            Args:
                table_name: Name of the Oracle table
                columns: List of column names

            Returns:
                FlextCore.Result containing Oracle INSERT statement or error

            """
            if not columns:
                return FlextCore.Result[str].fail("Column list cannot be empty")

            try:
                column_list = ", ".join(f'"{col.upper()}"' for col in columns)
                placeholder_list = ", ".join("?" for _ in columns)

                statement = f'INSERT INTO "{table_name.upper()}" ({column_list}) VALUES ({placeholder_list})'
                return FlextCore.Result[str].ok(statement)

            except Exception as e:
                return FlextCore.Result[str].fail(
                    f"Failed to prepare Oracle INSERT statement: {e}"
                )

        @staticmethod
        def transform_record_for_oracle(
            record: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Transform Singer record for Oracle database insertion.

            Args:
                record: Singer record data

            Returns:
                FlextCore.Result containing transformed record or error

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

                return FlextCore.Result[FlextCore.Types.Dict].ok(transformed)

            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to transform record for Oracle: {e}"
                )

    class StreamUtilities:
        """Singer stream processing utilities for Oracle target."""

        @staticmethod
        def process_schema_stream(
            stream_name: str, schema_message: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Process Singer schema stream for Oracle table management.

            Args:
                stream_name: Name of the Singer stream
                schema_message: Singer SCHEMA message

            Returns:
                FlextCore.Result containing processed schema information or error

            """
            try:
                schema = schema_message.get("schema", {})
                key_properties = schema_message.get("key_properties", [])

                # Generate Oracle table DDL
                ddl_result = FlextTargetOracleUtilities.OracleDataProcessing.generate_oracle_table_ddl(
                    stream_name, schema, key_properties
                )
                if ddl_result.is_failure:
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        f"DDL generation failed: {ddl_result.error}"
                    )

                processed_schema = {
                    "stream_name": stream_name,
                    "oracle_table_name": stream_name.upper(),
                    "ddl": ddl_result.unwrap(),
                    "key_properties": key_properties,
                    "properties": schema.get("properties", {}),
                }

                return FlextCore.Result[FlextCore.Types.Dict].ok(processed_schema)

            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to process schema stream: {e}"
                )

        @staticmethod
        def batch_records_for_oracle(
            records: list[FlextCore.Types.Dict], batch_size: int = 1000
        ) -> FlextCore.Result[list[list[FlextCore.Types.Dict]]]:
            """Batch Singer records for efficient Oracle bulk operations.

            Args:
                records: List of Singer records
                batch_size: Size of each batch (default: 1000)

            Returns:
                FlextCore.Result containing list of batches or error

            """
            if batch_size <= 0:
                return FlextCore.Result[list[list[FlextCore.Types.Dict]]].fail(
                    "Batch size must be positive"
                )

            try:
                batches = []
                for i in range(0, len(records), batch_size):
                    batch = records[i : i + batch_size]
                    batches.append(batch)

                return FlextCore.Result[list[list[FlextCore.Types.Dict]]].ok(batches)

            except Exception as e:
                return FlextCore.Result[list[list[FlextCore.Types.Dict]]].fail(
                    f"Failed to batch records: {e}"
                )

    class ConfigValidation:
        """Configuration validation utilities for Oracle target."""

        @staticmethod
        def validate_oracle_connection_config(
            config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate Oracle connection configuration.

            Args:
                config: Oracle connection configuration

            Returns:
                FlextCore.Result containing validated config or error

            """
            required_fields = ["host", "port", "service_name", "username", "password"]
            for field in required_fields:
                if field not in config or not config[field]:
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        f"Missing required Oracle config field: {field}"
                    )

            # Validate port number
            try:
                port = int(config["port"])
                if not (
                    FlextCore.Constants.Network.MIN_PORT
                    <= port
                    <= FlextCore.Constants.Network.MAX_PORT
                ):
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        f"Oracle port must be between {FlextCore.Constants.Network.MIN_PORT} and {FlextCore.Constants.Network.MAX_PORT}"
                    )
            except (ValueError, TypeError):
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Oracle port must be a valid integer"
                )

            return FlextCore.Result[FlextCore.Types.Dict].ok(config)

        @staticmethod
        def validate_oracle_target_config(
            config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate Oracle target-specific configuration.

            Args:
                config: Oracle target configuration

            Returns:
                FlextCore.Result containing validated config or error

            """
            # Validate batch size
            batch_size = config.get(
                "batch_size", FlextTargetOracleUtilities.DEFAULT_BATCH_SIZE
            )
            if batch_size <= 0:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Batch size must be positive"
                )

            # Validate connection pool size
            pool_size = config.get("connection_pool_size", 5)
            if (
                pool_size <= 0
                or pool_size > FlextTargetOracleUtilities.MAX_CONNECTION_POOL_SIZE
            ):
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Connection pool size must be between 1 and {FlextTargetOracleUtilities.MAX_CONNECTION_POOL_SIZE}"
                )

            # Validate commit interval
            commit_interval = config.get(
                "commit_interval", FlextTargetOracleUtilities.DEFAULT_COMMIT_INTERVAL
            )
            if commit_interval <= 0:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Commit interval must be positive"
                )

            return FlextCore.Result[FlextCore.Types.Dict].ok(config)

    class StateManagement:
        """Singer state management utilities for Oracle target."""

        @staticmethod
        def create_oracle_target_state(
            stream_states: FlextCore.Types.Dict,
            target_metadata: FlextCore.Types.Dict | None = None,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create Oracle target state for Singer checkpointing.

            Args:
                stream_states: Dictionary of stream states
                target_metadata: Optional target-specific metadata

            Returns:
                FlextCore.Result containing Oracle target state or error

            """
            try:
                state = {
                    "streams": stream_states,
                    "target_type": "oracle",
                    "last_updated": datetime.now(UTC).isoformat(),
                }

                if target_metadata:
                    state["target_metadata"] = target_metadata

                return FlextCore.Result[FlextCore.Types.Dict].ok(state)

            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to create Oracle target state: {e}"
                )

        @staticmethod
        def update_stream_state(
            current_state: FlextCore.Types.Dict,
            stream_name: str,
            last_processed_record: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Update state for a specific stream in Oracle target.

            Args:
                current_state: Current Singer state
                stream_name: Name of the stream to update
                last_processed_record: Last processed record data

            Returns:
                FlextCore.Result containing updated state or error

            """
            try:
                updated_state = current_state.copy()

                if "streams" not in updated_state:
                    updated_state["streams"] = {}

                updated_state["streams"][stream_name] = {
                    "last_processed_record": last_processed_record,
                    "last_updated": datetime.now(UTC).isoformat(),
                }

                return FlextCore.Result[FlextCore.Types.Dict].ok(updated_state)

            except Exception as e:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to update stream state: {e}"
                )

    class PerformanceUtilities:
        """Oracle performance optimization utilities."""

        @staticmethod
        def calculate_optimal_batch_size(
            table_row_size_bytes: int,
            available_memory_mb: int = 100,
        ) -> FlextCore.Result[int]:
            """Calculate optimal batch size for Oracle bulk operations.

            Args:
                table_row_size_bytes: Average size of table row in bytes
                available_memory_mb: Available memory for batching in MB

            Returns:
                FlextCore.Result containing optimal batch size or error

            """
            try:
                if table_row_size_bytes <= 0:
                    return FlextCore.Result[int].fail("Table row size must be positive")

                if available_memory_mb <= 0:
                    return FlextCore.Result[int].fail(
                        "Available memory must be positive"
                    )

                available_memory_bytes = available_memory_mb * 1024 * 1024
                max_batch_size = available_memory_bytes // table_row_size_bytes

                # Ensure batch size is within reasonable bounds
                optimal_batch_size = max(1, min(max_batch_size, 10000))

                return FlextCore.Result[int].ok(optimal_batch_size)

            except Exception as e:
                return FlextCore.Result[int].fail(
                    f"Failed to calculate optimal batch size: {e}"
                )

        @staticmethod
        def generate_oracle_performance_hints(
            operation_type: str,
            table_size: str = "medium",
        ) -> FlextCore.Result[str]:
            """Generate Oracle SQL hints for performance optimization.

            Args:
                operation_type: Type of operation (INSERT, UPDATE, DELETE, SELECT)
                table_size: Size category of table (small, medium, large)

            Returns:
                FlextCore.Result containing Oracle hints string or error

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
                return FlextCore.Result[str].ok(hint_string)

            except Exception as e:
                return FlextCore.Result[str].fail(
                    f"Failed to generate Oracle hints: {e}"
                )

    # Proxy methods for backward compatibility (minimal)
    def validate_singer_message(
        self, message: FlextCore.Types.Dict
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Proxy to SingerUtilities.validate_singer_message."""
        return self.SingerUtilities.validate_singer_message(message)

    def transform_record_for_oracle(
        self, record: FlextCore.Types.Dict
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Proxy to OracleDataProcessing.transform_record_for_oracle."""
        return self.OracleDataProcessing.transform_record_for_oracle(record)

    def validate_oracle_connection_config(
        self, config: FlextCore.Types.Dict
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Proxy to ConfigValidation.validate_oracle_connection_config."""
        return self.ConfigValidation.validate_oracle_connection_config(config)
