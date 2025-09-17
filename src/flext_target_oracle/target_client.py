"""Unified Oracle Target using FlextDomainService and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-core and flext-meltano exclusively.
SOLID COMPLIANCE - Single class with single responsibility: Oracle Singer Target.
UNIFIED PATTERN - All functionality in one class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from typing import ClassVar

from pydantic import Field

from flext_core import FlextDomainService, FlextResult, FlextTypes
from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_loader import FlextTargetOracleLoader


class FlextTargetOracle(FlextDomainService[FlextTypes.Core.Dict]):
    """Unified Oracle Singer Target using FlextDomainService SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses flext-core, flext-meltano, and flext-db-oracle exclusively.
    SOLID COMPLIANCE - Single responsibility: Oracle Singer Target operations.
    UNIFIED PATTERN - All functionality consolidated in one class.

    Architecture:
        - Single Responsibility: Oracle Singer Target implementation
        - Open/Closed: Extensible through configuration and composition
        - Liskov Substitution: Proper FlextDomainService inheritance
        - Interface Segregation: Focused Singer Target interface
        - Dependency Inversion: Depends on abstractions (flext-core patterns)
    """

    model_config: ClassVar = {"frozen": False}  # Allow field mutations

    # Pydantic fields - flext-core SOURCE OF TRUTH patterns
    name: str = Field(default="flext-oracle-target", description="Singer target name")
    config: FlextTargetOracleConfig = Field(description="Oracle target configuration")
    loader: FlextTargetOracleLoader = Field(description="Oracle data loader service")

    # Singer protocol state
    schemas: dict[str, FlextTypes.Core.Dict] = Field(
        default_factory=dict, description="Stream schemas"
    )
    state: FlextTypes.Core.Dict = Field(
        default_factory=dict, description="Singer state"
    )

    def __init__(
        self,
        config: FlextTargetOracleConfig | FlextTypes.Core.Dict | None = None,
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

        # Initialize FlextDomainService
        super().__init__()

        # Set Pydantic fields as instance attributes
        self.name = "flext-oracle-target"
        self.config = validated_config
        self.loader = loader
        self.schemas = {}
        self.state = {}

    def execute(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Execute Oracle Target - implements FlextDomainService abstract method."""
        connection_result = self.test_connection()
        if connection_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Oracle target execution failed: {connection_result.error}"
            )

        return FlextResult[FlextTypes.Core.Dict].ok(
            {
                "name": self.name,
                "status": "ready",
                "oracle_host": self.config.oracle_host,
                "oracle_service": self.config.oracle_service,
                "target_schema": self.config.default_target_schema,
            }
        )

    # === Core Target Operations ===

    def validate_configuration(self) -> FlextResult[None]:
        """Validate Oracle target configuration using domain rules."""
        return self.config.validate_domain_rules()

    def test_connection(self) -> FlextResult[None]:
        """Test Oracle database connectivity using loader."""
        return self.loader.test_connection()

    def discover_catalog(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Discover available schemas and generate Singer catalog."""
        try:
            catalog: FlextTypes.Core.Dict = {
                "streams": [],
            }

            for stream_name, schema in self.schemas.items():
                stream_entry = {
                    "tap_stream_id": stream_name,
                    "stream": stream_name,
                    "schema": schema,
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

            return FlextResult[FlextTypes.Core.Dict].ok(catalog)

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Failed to discover catalog: {e}"
            )

    # === Singer Protocol Operations ===

    def process_singer_messages(
        self, messages: list[FlextTypes.Core.Dict]
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Process Singer messages with comprehensive statistics."""
        try:
            records_processed = 0
            start_time = time.time()

            for message in messages:
                result = self._process_single_message(message)
                if result.is_failure:
                    return FlextResult[FlextTypes.Core.Dict].fail(
                        f"Failed to process message: {result.error}"
                    )

                if message.get("type") == "RECORD":
                    records_processed += 1

            # Finalize all streams
            finalize_result = self.loader.finalize_all_streams()
            if finalize_result.is_failure:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Failed to finalize streams: {finalize_result.error}"
                )

            execution_time_ms = int((time.time() - start_time) * 1000)

            result_data = {
                "success": True,
                "records_processed": records_processed,
                "schemas_discovered": list(self.schemas.keys()),
                "execution_time_ms": execution_time_ms,
                "state_updates": self.state,
            }

            return FlextResult[FlextTypes.Core.Dict].ok(result_data)

        except Exception as e:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Message processing failed: {e}"
            )

    def process_singer_message(
        self, message: FlextTypes.Core.Dict
    ) -> FlextResult[None]:
        """Process individual Singer message - async compatible."""
        return self._process_single_message(message)

    def finalize(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Finalize target processing and return comprehensive statistics."""
        try:
            result = self.loader.finalize_all_streams()
            if result.is_success:
                self.log_info("Oracle target finalization completed successfully")
                return result
            return result

        except Exception as e:
            self.log_error("Failed to finalize target", extra={"error": str(e)})
            return FlextResult[FlextTypes.Core.Dict].fail(f"Finalization failed: {e}")

    # === Private Message Handlers ===

    def _process_single_message(
        self, message: FlextTypes.Core.Dict
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
        self, message: FlextTypes.Core.Dict
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
                stream_name, schema, key_properties
            )
            if table_result.is_failure:
                return FlextResult[None].fail(
                    f"Failed to ensure table exists: {table_result.error}"
                )

            self.log_info(f"Processed schema for stream {stream_name}")
            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Schema handling failed: {e}")

    def _handle_record_message(
        self, message: FlextTypes.Core.Dict
    ) -> FlextResult[None]:
        """Handle RECORD message with data loading."""
        try:
            stream_name = message.get("stream")
            record_data = message.get("record")

            if not isinstance(stream_name, str):
                return FlextResult[None].fail("Invalid stream name in record message")

            if not isinstance(record_data, dict):
                return FlextResult[None].fail("Invalid record data in record message")

            # Load record using loader
            result = self.loader.load_record(stream_name, record_data)
            if result.is_failure:
                return FlextResult[None].fail(f"Failed to load record: {result.error}")

            return FlextResult[None].ok(None)

        except Exception as e:
            return FlextResult[None].fail(f"Record handling failed: {e}")

    def _handle_state_message(self, message: FlextTypes.Core.Dict) -> FlextResult[None]:
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

    def _test_connection(self) -> bool:
        """Singer SDK connection test compatibility."""
        result = self.test_connection()
        return result.is_success

    def _write_record(self, stream_name: str, record: FlextTypes.Core.Dict) -> None:
        """Singer SDK record writing compatibility."""
        result = self.loader.load_record(stream_name, record)
        if result.is_failure:
            msg = f"Failed to write record: {result.error}"
            raise RuntimeError(msg)

    # === Metrics and Information ===

    def get_implementation_metrics(self) -> FlextTypes.Core.Dict:
        """Get Oracle-specific implementation metrics."""
        return {
            "oracle_host": self.config.oracle_host,
            "oracle_port": self.config.oracle_port,
            "default_schema": self.config.default_target_schema,
            "load_method": self.config.load_method.value,
            "use_bulk_operations": self.config.use_bulk_operations,
            "batch_size": self.config.batch_size,
        }


# Compatibility alias
TargetOracle = FlextTargetOracle


__all__ = [
    "FlextTargetOracle",
    "TargetOracle",
]
