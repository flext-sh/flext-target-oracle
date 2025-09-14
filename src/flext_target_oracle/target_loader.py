"""Oracle Data Loader using FlextDomainService and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-db-oracle API exclusively.
SOLID COMPLIANCE - Single responsibility: Oracle data loading only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from flext_core import FlextDomainService, FlextResult, FlextTypes
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig
from pydantic import Field, SecretStr

from flext_target_oracle.target_config import FlextTargetOracleConfig
from flext_target_oracle.target_exceptions import (
    FlextTargetOracleConnectionError,
)


class FlextTargetOracleLoader(FlextDomainService[FlextTypes.Core.Dict]):
    """Oracle data loader using FlextDomainService and flext-db-oracle SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses ONLY public flext-db-oracle API.
    SOLID COMPLIANCE - Single responsibility: Oracle data loading operations.
    """

    # Pydantic fields for configuration and state
    config: FlextTargetOracleConfig = Field(description="Oracle target configuration")
    oracle_api: FlextDbOracleApi = Field(description="Oracle API instance")

    # Internal state fields (without underscore for Pydantic)
    record_buffers: dict[str, list[FlextTypes.Core.Dict]] = Field(
        default_factory=dict, description="Record buffers by stream"
    )
    total_records: int = Field(default=0, description="Total records processed")

    def __init__(self, config: FlextTargetOracleConfig, **data: object) -> None:
        """Initialize loader with Oracle API using flext-db-oracle correctly."""
        try:
            # Create Oracle API configuration from target config
            oracle_config = FlextDbOracleConfig(
                host=config.oracle_host,
                port=config.oracle_port,
                service_name=config.oracle_service,
                database=config.oracle_service,  # Required field - same as service_name
                username=config.oracle_user,
                password=SecretStr(
                    config.oracle_password.get_secret_value()
                    if hasattr(config.oracle_password, "get_secret_value")
                    else str(config.oracle_password)
                ),
            )

            # Initialize Oracle API
            oracle_api = FlextDbOracleApi(oracle_config)

            # Initialize FlextDomainService with Pydantic fields
            super().__init__(
                config=config,
                oracle_api=oracle_api,
                record_buffers={},
                total_records=0,
                **data,
            )

        except Exception as e:
            msg = f"Failed to create Oracle API: {e}"
            raise FlextTargetOracleConnectionError(msg) from e

    def execute(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Execute domain service - returns connection test result."""
        connection_result = self.test_connection()
        if connection_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Oracle connection failed: {connection_result.error}"
            )

        return FlextResult[FlextTypes.Core.Dict].ok(
            {
                "status": "ready",
                "host": self.config.oracle_host,
                "service": self.config.oracle_service,
                "schema": self.config.default_target_schema,
            }
        )

    def test_connection(self) -> FlextResult[None]:
        """Test connection to Oracle database using flext-db-oracle API."""
        try:
            # Use Oracle API context manager correctly
            with self.oracle_api as connected_api:
                # Test connection by getting tables
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema
                )
                if tables_result.is_failure:
                    return FlextResult[None].fail(
                        f"Connection test failed: {tables_result.error}"
                    )

                self.log_info("Oracle connection established successfully")
                return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error("Failed to connect to Oracle", extra={"error": str(e)})
            return FlextResult[None].fail(f"Connection failed: {e}")

    def ensure_table_exists(
        self,
        stream_name: str,
        schema: FlextTypes.Core.Dict,
        _key_properties: FlextTypes.Core.StringList | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists using flext-db-oracle API with correct table creation."""
        try:
            table_name = self.config.get_table_name(stream_name)

            with self.oracle_api as connected_api:
                # Check if table exists
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema
                )

                if tables_result.is_failure:
                    return FlextResult[None].fail(
                        f"Failed to check tables: {tables_result.error}"
                    )

                # Handle case where tables_result.data might be None
                existing_tables_raw = tables_result.data
                if existing_tables_raw is None:
                    existing_tables = []
                elif isinstance(existing_tables_raw, list):
                    existing_tables = [str(t).upper() for t in existing_tables_raw]
                else:
                    existing_tables = []

                table_exists = table_name.upper() in existing_tables

                if table_exists:
                    self.log_info(f"Table {table_name} already exists")
                    return FlextResult[None].ok(None)

                # Create table using SQL execution (since create_table_ddl doesn't exist)
                ddl_sql = self._build_create_table_sql(table_name, schema)

                # Execute DDL using execute method
                exec_result = connected_api.execute(ddl_sql)
                if exec_result.is_failure:
                    return FlextResult[None].fail(
                        f"Failed to create table: {exec_result.error}"
                    )

                self.log_info(f"Created table {table_name}")
                return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error("Failed to ensure table exists", extra={"error": str(e)})
            return FlextResult[None].fail(f"Table creation failed: {e}")

    def load_record(
        self,
        stream_name: str,
        record_data: FlextTypes.Core.Dict,
    ) -> FlextResult[None]:
        """Load record with batching."""
        try:
            if stream_name not in self.record_buffers:
                self.record_buffers[stream_name] = []

            self.record_buffers[stream_name].append(record_data)
            self.total_records += 1

            # Auto-flush if batch is full
            if len(self.record_buffers[stream_name]) >= self.config.batch_size:
                return self._flush_batch(stream_name)

            return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error("Failed to load record", extra={"error": str(e)})
            return FlextResult[None].fail(f"Record loading failed: {e}")

    def finalize_all_streams(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Finalize all streams and return stats."""
        try:
            # Flush all remaining records
            for stream_name, records in self.record_buffers.items():
                if records:
                    result = self._flush_batch(stream_name)
                    if result.is_failure:
                        self.log_error(f"Failed to flush {stream_name}: {result.error}")

            stats: FlextTypes.Core.Dict = {
                "total_records": self.total_records,
                "streams_processed": len(self.record_buffers),
                "status": "completed",
            }

            return FlextResult[FlextTypes.Core.Dict].ok(stats)

        except Exception as e:
            self.log_error("Failed to finalize streams", extra={"error": str(e)})
            return FlextResult[FlextTypes.Core.Dict].fail(f"Finalization failed: {e}")

    def _build_create_table_sql(
        self, table_name: str, _schema: FlextTypes.Core.Dict
    ) -> str:
        """Build CREATE TABLE SQL statement."""
        schema_name = self.config.default_target_schema
        full_table_name = f"{schema_name}.{table_name}"

        # Create simple JSON table for Singer data
        sql = f"""
        CREATE TABLE {full_table_name} (
            DATA CLOB,
            _SDC_EXTRACTED_AT TIMESTAMP,
            _SDC_LOADED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        return sql.strip()

    def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush batch using direct SQL execution."""
        try:
            records = self.record_buffers.get(stream_name, [])
            if not records:
                return FlextResult[None].ok(None)

            table_name = self.config.get_table_name(stream_name)
            schema_name = self.config.default_target_schema
            full_table_name = f"{schema_name}.{table_name}"
            loaded_at = datetime.now(UTC)

            with self.oracle_api as connected_api:
                # Use parameterized query with table name validation
                # Validate table name contains only safe characters
                if not all(c.isalnum() or c in '._' for c in full_table_name):
                    return FlextResult[None].fail("Invalid table name characters")
                
                # Build INSERT SQL with validated table name
                insert_sql = (
                    f"INSERT INTO {full_table_name} "
                    "(DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) "
                    "VALUES (:data, :extracted_at, :loaded_at)"
                )

                # Execute batch using multiple execute calls
                for record in records:
                    params = {
                        "data": json.dumps(record),
                        "extracted_at": record.get("_sdc_extracted_at", loaded_at),
                        "loaded_at": loaded_at,
                    }

                    result = connected_api.execute(insert_sql, params)
                    if result.is_failure:
                        return FlextResult[None].fail(
                            f"Batch insert failed: {result.error}"
                        )

                # Clear buffer
                self.record_buffers[stream_name] = []

                self.log_info(f"Flushed {len(records)} records to {table_name}")
                return FlextResult[None].ok(None)

        except Exception as e:
            self.log_error("Failed to flush batch", extra={"error": str(e)})
            return FlextResult[None].fail(f"Batch flush failed: {e}")


__all__ = [
    "FlextTargetOracleLoader",
]
