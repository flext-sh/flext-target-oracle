"""Oracle Target Service using FlextCore.Service and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-core and flext-meltano SOURCE OF TRUTH.
SOLID COMPLIANCE - Single responsibility: Singer Target operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from typing import ClassVar, override

from flext_core import FlextCore
from pydantic import Field

from flext_target_oracle.config import FlextTargetOracleConfig
from flext_target_oracle.target_loader import FlextTargetOracleLoader


class FlextTargetOracleService(FlextCore.Service[FlextCore.Types.Dict]):
    """Oracle Singer Target service using FlextCore.Service SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses FlextMeltanoTarget and FlextTargetOracleLoader.
    SOLID COMPLIANCE - Single responsibility: Singer protocol operations.
    """

    model_config: ClassVar = {"frozen": "False"}  # Allow field mutations

    # Pydantic fields for service configuration
    name: str = Field(default="flext-oracle-target", description="Target name")
    config: FlextTargetOracleConfig = Field(description="Oracle target configuration")
    loader: FlextTargetOracleLoader = Field(description="Oracle data loader")

    # Internal state
    _schemas: FlextCore.Types.NestedDict = Field(
        default_factory=dict,
        description="Stream schemas",
    )
    _state: FlextCore.Types.Dict = Field(
        default_factory=dict,
        description="Singer state",
    )

    @override
    def __init__(self, config: FlextTargetOracleConfig, **_data: object) -> None:
        """Initialize Oracle Target service with configuration validation."""
        # Create loader instance
        loader = FlextTargetOracleLoader(config)

        # Initialize FlextCore.Service
        super().__init__()

        # Set Pydantic fields as instance attributes
        self.name = "flext-oracle-target"
        self.config: FlextCore.Types.Dict = config
        self.loader = loader
        self._schemas = {}
        self._state = {}

    @override
    def execute(self: object) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Execute domain service - test connection and return status."""
        connection_result: FlextCore.Result[object] = self.loader.test_connection()
        if connection_result.is_failure:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Oracle target service connection failed: {connection_result.error}",
            )

        return FlextCore.Result[FlextCore.Types.Dict].ok(
            {
                "name": self.name,
                "status": "ready",
                "config_valid": "True",
                "connection_tested": "True",
            },
        )

    def validate_configuration(self: object) -> FlextCore.Result[None]:
        """Validate the current configuration."""
        return self.config.validate_domain_rules()

    def test_connection(self: object) -> FlextCore.Result[None]:
        """Test Oracle database connectivity."""
        return self.loader.test_connection()

    def discover_catalog(self: object) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Discover available schemas and generate Singer catalog."""
        try:
            streams_list: list[FlextCore.Types.Dict] = []
            catalog: FlextCore.Types.Dict = {
                "streams": "streams_list",
            }

            for stream_name in self._schemas:
                stream_entry: FlextCore.Types.Dict = {
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
                streams_list.append(stream_entry)

            return FlextCore.Result[FlextCore.Types.Dict].ok(catalog)

        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Failed to discover catalog: {e}",
            )

    def process_singer_messages(
        self,
        messages: list[FlextCore.Types.Dict],
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Process Singer messages (SCHEMA, RECORD, STATE)."""
        try:
            records_processed = 0
            start_time = time.time()

            for message in messages:
                result: FlextCore.Result[object] = self._process_single_message(message)
                if result.is_failure:
                    return FlextCore.Result[FlextCore.Types.Dict].fail(
                        f"Failed to process message: {result.error}",
                    )

                if message.get("type") == "RECORD":
                    records_processed += 1

            # Finalize all streams
            finalize_result: FlextCore.Result[object] = (
                self.loader.finalize_all_streams()
            )
            if finalize_result.is_failure:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    f"Failed to finalize streams: {finalize_result.error}",
                )

            int((time.time() - start_time) * 1000)

            result_data = {
                "success": "True",
                "records_processed": "records_processed",
                "schemas_discovered": list(self._schemas.keys()),
                "execution_time_ms": "execution_time_ms",
                "state_updates": self._state,
            }

            return FlextCore.Result[FlextCore.Types.Dict].ok(result_data)

        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Message processing failed: {e}",
            )

    def _process_single_message(
        self,
        message: FlextCore.Types.Dict,
    ) -> FlextCore.Result[None]:
        """Process a single Singer message."""
        message_type = message.get("type")

        if message_type == "SCHEMA":
            return self._handle_schema(message)
        if message_type == "RECORD":
            return self._handle_record(message)
        if message_type == "STATE":
            return self._handle_state(message)
        return FlextCore.Result[None].fail(f"Unknown message type: {message_type}")

    def _handle_schema(self, message: FlextCore.Types.Dict) -> FlextCore.Result[None]:
        """Handle SCHEMA message."""
        try:
            stream_name = message.get("stream")
            schema = message.get("schema")

            if not isinstance(stream_name, str):
                return FlextCore.Result[None].fail(
                    "Invalid stream name in schema message"
                )

            if not isinstance(schema, dict):
                return FlextCore.Result[None].fail("Invalid schema in schema message")

            # Store schema
            self._schemas[stream_name] = schema

            # Ensure table exists
            key_properties = message.get("key_properties")
            key_properties_list: FlextCore.Types.StringList | None = (
                key_properties if isinstance(key_properties, list) else None
            )
            table_result = self.loader.ensure_table_exists(
                stream_name,
                schema,
                key_properties_list,
            )
            if table_result.is_failure:
                return FlextCore.Result[None].fail(
                    f"Failed to ensure table exists: {table_result.error}",
                )

            self.log_info(f"Processed schema for stream {stream_name}")
            return FlextCore.Result[None].ok(None)

        except Exception as e:
            return FlextCore.Result[None].fail(f"Schema handling failed: {e}")

    def _handle_record(self, message: FlextCore.Types.Dict) -> FlextCore.Result[None]:
        """Handle RECORD message."""
        try:
            stream_name = message.get("stream")
            record_data: FlextCore.Types.Dict = message.get("record")

            if not isinstance(stream_name, str):
                return FlextCore.Result[None].fail(
                    "Invalid stream name in record message"
                )

            if not isinstance(record_data, dict):
                return FlextCore.Result[None].fail(
                    "Invalid record data in record message"
                )

            # Load record using loader
            result: FlextCore.Result[object] = self.loader.load_record(
                stream_name, record_data
            )
            if result.is_failure:
                return FlextCore.Result[None].fail(
                    f"Failed to load record: {result.error}"
                )

            return FlextCore.Result[None].ok(None)

        except Exception as e:
            return FlextCore.Result[None].fail(f"Record handling failed: {e}")

    def _handle_state(self, message: FlextCore.Types.Dict) -> FlextCore.Result[None]:
        """Handle STATE message."""
        try:
            state_value = message.get("value")
            if isinstance(state_value, dict):
                self._state.update(state_value)

            self.log_debug(f"Updated state: {state_value}")
            return FlextCore.Result[None].ok(None)

        except Exception as e:
            return FlextCore.Result[None].fail(f"State handling failed: {e}")

    def finalize(self: object) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Finalize target processing and return comprehensive statistics."""
        try:
            result: FlextCore.Result[object] = self.loader.finalize_all_streams()
            if result.is_success:
                self.log_info("Target finalization completed successfully")
                return result
            return result

        except Exception as e:
            self.log_error("Failed to finalize target", extra={"error": str(e)})
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Finalization failed: {e}"
            )

    def get_implementation_metrics(self: object) -> FlextCore.Types.Dict:
        """Get Oracle-specific implementation metrics."""
        return {
            "oracle_host": self.config.oracle_host,
            "oracle_port": self.config.oracle_port,
            "default_schema": self.config.default_target_schema,
            "load_method": self.config.load_method.value,
            "use_bulk_operations": self.config.use_bulk_operations,
            "batch_size": self.config.batch_size,
        }


__all__ = [
    "FlextTargetOracleService",
]
