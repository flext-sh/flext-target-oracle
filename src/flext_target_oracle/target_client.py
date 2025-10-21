"""Unified Oracle Target using FlextService and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-core and flext-meltano exclusively.
SOLID COMPLIANCE - Single class with single responsibility: Oracle Singer Target.
UNIFIED PATTERN - All functionality in one class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import time
from typing import ClassVar, override

from flext_core import FlextResult, FlextService
from pydantic import Field

from flext_target_oracle.config import FlextTargetOracleConfig
from flext_target_oracle.models import FlextTargetOracleModels
from flext_target_oracle.target_loader import FlextTargetOracleLoader
from flext_target_oracle.typings import FlextTargetOracleTypes


class FlextTargetOracle(
    FlextService[FlextTargetOracleTypes.SingerTarget.MessageProcessing]
):
    """Unified Oracle Singer Target using FlextService SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses flext-core, flext-meltano, and flext-db-oracle exclusively.
    SOLID COMPLIANCE - Single responsibility: Oracle Singer Target operations.
    UNIFIED PATTERN - All functionality consolidated in one class.

    Architecture:
    - Single Responsibility: Oracle Singer Target implementation
    - Open/Closed: Extensible through configuration and composition
    - Liskov Substitution: Proper FlextService inheritance
    - Interface Segregation: Focused Singer Target interface
    - Dependency Inversion: Depends on abstractions (flext-core patterns)
    """

    model_config: ClassVar = {"frozen": "False"}  # Allow field mutations

    # Pydantic fields - flext-core SOURCE OF TRUTH patterns
    name: str = Field(default="flext-oracle-target", description="Singer target name")
    config: FlextTargetOracleConfig = Field(description="Oracle target configuration")
    loader: FlextTargetOracleLoader = Field(description="Oracle data loader service")

    # Singer protocol state
    schemas: dict[str, FlextTargetOracleTypes.StreamProcessing.StreamSchema] = Field(
        default_factory=dict,
        description="Stream schemas",
    )
    state: FlextTargetOracleTypes.StreamProcessing.StreamState = Field(
        default_factory=dict,
        description="Singer state",
    )

    @override
    def __init__(
        self,
        config: FlextTargetOracleConfig | dict[str, object] | None = None,
        **_data: object,
    ) -> None:
        """Initialize Oracle Singer Target with configuration validation."""
        # Convert config if needed
        if isinstance(config, dict):
            validated_config = FlextTargetOracleConfig.model_validate(config)
        elif isinstance(config, FlextTargetOracleConfig):
            validated_config = config
        else:
            msg = (
                "Configuration is required. Provide FlextTargetOracleConfig instance "
                "or dictionary with Oracle connection parameters."
            )
            raise TypeError(msg)

        # Create loader with validated config
        loader = FlextTargetOracleLoader(validated_config)

        # Initialize FlextService
        super().__init__()

        # Set Pydantic fields as instance attributes
        self.name = "flext-oracle-target"
        self.config = validated_config
        self.loader = loader
        self.schemas = {}
        self.state = {}

        # Initialize missing attributes for testing
        self._start_time = time.time()
        self._loader = loader
        self._stream_schemas = {}
        self._ignored_columns = []

    @override
    def execute(
        self, payload: str | None = None
    ) -> FlextResult[FlextTargetOracleTypes.Core.Dict]:
        """Execute Oracle Target - implements FlextService abstract method.

        Backwards-compat: accept optional string payload (Singer message JSON). If
        payload is provided, attempt to parse and process as a single message.
        """
        # If a payload (Singer message) is provided, try to process it
        if payload is not None:
            try:
                # parse JSON string into dict
                msg = __import__("json").loads(payload)
                # Process single message if dict-like
                if isinstance(msg, dict):
                    proc = self.process_singer_message(msg)
                    return FlextResult[FlextTargetOracleTypes.Core.Dict].ok(
                        {"processed": proc.is_success},
                    )
                # If payload wasn't a dict, return a success with no-op
                return FlextResult[FlextTargetOracleTypes.Core.Dict].ok({
                    "processed": "False"
                })
            except Exception as e:
                return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                    f"Failed to process payload: {e}",
                )

        connection_result: FlextResult[object] = self.test_connection()
        if connection_result.is_failure:
            return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                f"Oracle target execution failed: {connection_result.error}",
            )

        return FlextResult[FlextTargetOracleTypes.Core.Dict].ok(
            {
                "name": self.name,
                "status": "ready",
                "oracle_host": self.config.oracle_host,
                "oracle_service": self.config.oracle_service,
                "target_schema": self.config.default_target_schema,
            },
        )

    def initialize(self: object) -> FlextResult[None]:
        """Compatibility shim for older tests: perform a connection test."""
        return self.test_connection()

    # === Core Target Operations ===

    def validate_configuration(self: object) -> FlextResult[None]:
        """Validate Oracle target configuration using domain rules."""
        return self.config.validate_domain_rules()

    def test_connection(self: object) -> FlextResult[None]:
        """Test Oracle database connectivity using loader."""
        return self.loader.test_connection()

    def discover_catalog(
        self: object,
    ) -> FlextResult[FlextTargetOracleTypes.Core.Dict]:
        """Discover available schemas and generate Singer catalog."""
        try:
            catalog: FlextTargetOracleTypes.Core.Dict = {
                "streams": [],
            }

            for stream_name in self.schemas:
                stream_entry = {
                    "tap_stream_id": "stream_name",
                    "stream": "stream_name",
                    "schema": "schema",
                    "metadata": [
                        {
                            "breadcrumb": [],
                            "metadata": {
                                "inclusion": "available",
                                "table-name": self.config.get_table_name(stream_name),
                                "schema-name": self.config.default_target_schema,
                                "forced-replication-method": "FULL_TABLE",
                            },
                        },
                    ],
                }
                streams = catalog.get("streams")
                if isinstance(streams, list):
                    streams.append(stream_entry)

            return FlextResult[FlextTargetOracleTypes.Core.Dict].ok(catalog)

        except Exception as e:
            return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                f"Failed to discover catalog: {e}",
            )

    # === Singer Protocol Operations ===

    def process_singer_messages(
        self,
        messages: list[FlextTargetOracleTypes.Core.Dict],
    ) -> FlextResult[FlextTargetOracleTypes.Core.Dict]:
        """Process Singer messages with complete statistics using standardized models."""
        try:
            # Initialize processing state using FlextTargetOracleModels
            processing_state = FlextTargetOracleModels.SingerMessageProcessing(
                processing_start_time=str(time.time()),
                message_count=len(messages),
            )

            records_processed = 0
            start_time = time.time()

            for message in messages:
                result: FlextResult[object] = self._process_single_message(message)
                if result.is_failure:
                    processing_state.error_count += 1
                    processing_state.failed_messages.append(
                        str(message.get("type", "unknown"))
                    )
                    return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                        f"Failed to process message: {result.error}",
                    )

                # Update processing statistics using models
                message_type = message.get("type")
                if message_type == "RECORD":
                    records_processed += 1
                    processing_state.record_messages += 1
                elif message_type == "SCHEMA":
                    processing_state.schema_messages += 1
                elif message_type == "STATE":
                    processing_state.state_messages += 1

            # Finalize all streams
            finalize_result: FlextResult[object] = self.loader.finalize_all_streams()
            if finalize_result.is_failure:
                processing_state.error_count += 1
                return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                    f"Failed to finalize streams: {finalize_result.error}",
                )

            # Calculate final statistics
            execution_time_ms = int((time.time() - start_time) * 1000)
            processing_state.last_processed_time = str(time.time())
            processing_state.records_per_second = (
                records_processed / (time.time() - start_time)
                if (time.time() - start_time) > 0
                else 0.0
            )

            # Use models to structure the result
            result_data = {
                "success": True,
                "records_processed": records_processed,
                "schemas_discovered": list(self.schemas.keys()),
                "execution_time_ms": execution_time_ms,
                "state_updates": self.state,
                "processing_statistics": processing_state.model_dump(),
            }

            return FlextResult[FlextTargetOracleTypes.Core.Dict].ok(result_data)

        except Exception as e:
            return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                f"Message processing failed: {e}",
            )

    def process_singer_message(
        self,
        message: FlextTargetOracleTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Process individual Singer message - compatible."""
        return self._process_single_message(message)

    def finalize(self: object) -> FlextResult[FlextTargetOracleTypes.Core.Dict]:
        """Finalize target processing and return complete statistics."""
        try:
            result: FlextResult[object] = self.loader.finalize_all_streams()
            if result.is_success:
                self.log_info("Oracle target finalization completed successfully")
                return result
            return result

        except Exception as e:
            self.log_error("Failed to finalize target", extra={"error": str(e)})
            return FlextResult[FlextTargetOracleTypes.Core.Dict].fail(
                f"Finalization failed: {e}"
            )

    # === Private Message Handlers ===

    def _process_single_message(
        self,
        message: FlextTargetOracleTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Process a single Singer message with type dispatch."""
        message_type = message.get("type")

        if message_type == "SCHEMA":
            return self._handle_schema_message(message)
        if message_type == "RECORD":
            return self._handle_record_message(message)
        if message_type == "STATE":
            return self._handle_state_message(message)
        return FlextResult[None].fail(f"Unknown message type: {message_type}")

    def _handle_schema_message(
        self,
        message: FlextTargetOracleTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Handle SCHEMA message with table creation."""
        try:
            stream_name = message.get("stream")
            schema = message.get("schema")

            if not isinstance(stream_name, str):
                return FlextResult[None].fail("Invalid stream name in schema message")

            if not isinstance(schema, dict):
                return FlextResult[None].fail("Invalid schema in schema message")

            # Store schema
            self.schemas[stream_name] = schema

            # Ensure table exists with proper type handling
            key_properties = message.get("key_properties")
            if key_properties is not None and not isinstance(key_properties, list):
                key_properties = None

            table_result = self.loader.ensure_table_exists(
                stream_name,
                schema,
                key_properties,
            )
            if table_result.is_failure:
                return FlextResult[None].fail(
                    f"Failed to ensure table exists: {table_result.error}",
                )

            self.log_info(f"Processed schema for stream {stream_name}")
            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Schema handling failed: {e}")

    def _handle_record_message(
        self,
        message: FlextTargetOracleTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Handle RECORD message with data loading."""
        try:
            stream_name = message.get("stream")
            record_data: dict[str, object] = message.get("record")

            if not isinstance(stream_name, str):
                return FlextResult[None].fail("Invalid stream name in record message")

            if not isinstance(record_data, dict):
                return FlextResult[None].fail("Invalid record data in record message")

            # Load record using loader
            result: FlextResult[object] = self.loader.load_record(
                stream_name, record_data
            )
            if result.is_failure:
                return FlextResult[None].fail(f"Failed to load record: {result.error}")

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Record handling failed: {e}")

    def _handle_state_message(
        self, message: FlextTargetOracleTypes.Core.Dict
    ) -> FlextResult[None]:
        """Handle STATE message with state persistence."""
        try:
            state_value = message.get("value")
            if isinstance(state_value, dict):
                self.state.update(state_value)

            self.log_debug(f"Updated state: {state_value}")
            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"State handling failed: {e}")

    # === Singer SDK Compatibility (if needed) ===

    def _test_connection(self: object) -> bool:
        """Singer SDK connection test compatibility."""
        result: FlextResult[object] = self.test_connection()
        return result.is_success

    def _write_record(
        self, stream_name: str, record: FlextTargetOracleTypes.Core.Dict
    ) -> None:
        """Singer SDK record writing compatibility."""
        result: FlextResult[object] = self.loader.load_record(stream_name, record)
        if result.is_failure:
            msg = f"Failed to write record: {result.error}"
            raise RuntimeError(msg)

    # === Metrics and Information ===

    def get_implementation_metrics(self: object) -> FlextTargetOracleTypes.Core.Dict:
        """Get Oracle-specific implementation metrics using standardized models."""
        # Use FlextTargetOracleModels.OraclePerformanceMetrics for structured metrics
        performance_metrics = FlextTargetOracleModels.OraclePerformanceMetrics(
            records_per_second=0.0,  # Will be calculated during actual operations
            bytes_per_second=0.0,  # Will be calculated during actual operations
            batches_per_second=0.0,  # Will be calculated during actual operations
            oracle_connections_used=1,  # Basic connection usage
            oracle_connection_pool_size=self.config.pool_max_size
            if hasattr(self.config, "pool_max_size")
            else 10,
            average_oracle_response_time=0.0,  # Will be measured during operations
            memory_usage_mb=0.0,  # Will be measured during operations
            cpu_usage_percent=0.0,  # Will be measured during operations
            success_rate=100.0,  # Default optimistic rate
            error_rate=0.0,  # Default optimistic rate
        )

        # Return complete metrics including config and performance data
        return {
            "oracle_host": self.config.oracle_host,
            "oracle_port": self.config.oracle_port,
            "default_schema": self.config.default_target_schema,
            "load_method": getattr(self.config, "load_method", {}).get(
                "value", "INSERT"
            )
            if hasattr(self.config, "load_method")
            else "INSERT",
            "use_bulk_operations": self.config.use_bulk_operations,
            "batch_size": self.config.batch_size,
            "performance_metrics": performance_metrics.model_dump(),
            "configured_schemas": list(self.schemas.keys()),
            "current_state": self.state,
        }

    def write_record(self, _record_data: str) -> FlextResult[None]:
        """Write a Singer record (stub - not implemented)."""
        return FlextResult[None].fail("write_record not implemented in stub")


__all__ = [
    "FlextTargetOracle",
]
