"""Oracle Data Loader using FlextService and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-db-oracle API exclusively.
SOLID COMPLIANCE - Single responsibility: Oracle data loading only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import ClassVar

from flext_core import FlextLogger, FlextResult, FlextService, t
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleSettings
from pydantic import Field

from .models import m
from .settings import FlextTargetOracleSettings
from .target_exceptions import (
    FlextTargetOracleConnectionError,
)

logger = FlextLogger(__name__)


class FlextTargetOracleLoader(FlextService[m.TargetOracle.LoaderReadyResult]):
    """Oracle data loader using FlextService and flext-db-oracle SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses ONLY public flext-db-oracle API.
    SOLID COMPLIANCE - Single responsibility: Oracle data loading operations.
    """

    model_config: ClassVar = {"frozen": False}

    # Pydantic fields for configuration and state
    target_config: FlextTargetOracleSettings = Field(
        description="Oracle target configuration"
    )
    oracle_api: FlextDbOracleApi = Field(description="Oracle API instance")

    # Internal state fields (without underscore for Pydantic)
    record_buffers: dict[str, list[dict[str, t.JsonValue]]] = Field(
        default_factory=dict,
        description="Record buffers by stream",
    )
    total_records: int = Field(default=0, description="Total records processed")

    def log_info(self, message: str) -> None:
        """Log informational loader events."""
        logger.info(message)

    def log_error(
        self,
        message: str,
        *,
        extra: Mapping[str, str] | None = None,
    ) -> None:
        """Log loader errors with optional metadata."""
        if extra is None:
            logger.error(message)
            return
        logger.error(message, extra=extra)

    def __init__(self, config: FlextTargetOracleSettings, **_data: object) -> None:
        """Initialize loader with Oracle API using flext-db-oracle correctly."""
        try:
            # Create Oracle API configuration from target config
            oracle_connection = config.get_oracle_config()
            oracle_config = FlextDbOracleSettings(
                host=oracle_connection.host,
                port=oracle_connection.port,
                service_name=oracle_connection.service_name,
                username=oracle_connection.username,
                password=oracle_connection.password,
            )

            # Initialize Oracle API
            oracle_api = FlextDbOracleApi(oracle_config)

            # Initialize FlextService
            super().__init__()

            # Set Pydantic fields as instance attributes
            self.target_config = config
            self.oracle_api = oracle_api
            self.record_buffers = {}
            self.total_records = 0

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            msg = f"Failed to create Oracle API: {e}"
            raise FlextTargetOracleConnectionError(msg) from e

    def execute(self) -> FlextResult[m.TargetOracle.LoaderReadyResult]:
        """Execute domain service - returns connection test result."""
        connection_result = self.test_connection()
        if connection_result.is_failure:
            return FlextResult[m.TargetOracle.LoaderReadyResult].fail(
                f"Oracle connection failed: {connection_result.error}",
            )

        return FlextResult[m.TargetOracle.LoaderReadyResult].ok(
            m.TargetOracle.LoaderReadyResult(
                host=self.target_config.oracle_host,
                service=self.target_config.oracle_service_name,
                schema=self.target_config.default_target_schema,
            )
        )

    def test_connection(self) -> FlextResult[bool]:
        """Test connection to Oracle database using flext-db-oracle API."""
        try:
            # Use Oracle API context manager correctly
            with self.oracle_api as connected_api:
                # Test connection by getting tables
                tables_result = connected_api.get_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.is_failure:
                    return FlextResult[bool].fail(
                        f"Connection test failed: {tables_result.error}",
                    )

                self.log_info("Oracle connection established successfully")
                return FlextResult[bool].ok(value=True)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to connect to Oracle", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Connection failed: {e}")

    def connect(self) -> FlextResult[bool]:
        """Establish connection using underlying FlextDbOracleApi.

        Exposed for tests and parity with previous loader helpers.
        """
        try:
            result = self.oracle_api.connect()
            if bool(result.is_failure if hasattr(result, "is_failure") else False):
                return FlextResult[bool].fail(
                    f"Connect failed: {result.error if hasattr(result, 'error') else None}",
                )

            return FlextResult[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Failed to connect loader")
            self.log_error("Failed to connect loader", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Connect failed: {e}")

    def disconnect(self) -> FlextResult[bool]:
        """Disconnect underlying FlextDbOracleApi (exposed for tests)."""
        try:
            result = self.oracle_api.disconnect()
            if bool(result.is_failure if hasattr(result, "is_failure") else False):
                return FlextResult[bool].fail(
                    f"Disconnect failed: {result.error if hasattr(result, 'error') else None}",
                )

            return FlextResult[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Failed to disconnect loader")
            self.log_error("Failed to disconnect loader", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Disconnect failed: {e}")

    def insert_records(
        self,
        stream_name: str,
        records: list[Mapping[str, t.JsonValue]],
    ) -> FlextResult[bool]:
        """Insert multiple records - convenience wrapper used by tests.

        Appends records to the internal buffer via load_record and flushes the batch.
        """
        try:
            for record in records:
                # Use existing load_record logic which handles buffering and auto-flush
                load_res = self.load_record(stream_name, record)
                if load_res.is_failure:
                    return FlextResult[bool].fail(
                        f"Failed to load record: {load_res.error}",
                    )

            # Ensure remaining records are flushed
            return self._flush_batch(stream_name)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to insert records", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Insert records failed: {e}")

    def ensure_table_exists(
        self,
        stream_name: str,
        schema: Mapping[str, t.JsonValue],
        _key_properties: list[str] | None = None,
    ) -> FlextResult[bool]:
        """Ensure table exists using flext-db-oracle API with correct table creation."""
        try:
            table_name = self.target_config.get_table_name(stream_name)

            with self.oracle_api as connected_api:
                # Check if table exists
                tables_result = connected_api.get_tables(
                    schema=self.target_config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult[bool].fail(
                        f"Failed to check tables: {tables_result.error}",
                    )

                existing_tables_raw = tables_result.value or []
                existing_tables = [str(table).upper() for table in existing_tables_raw]

                table_exists = table_name.upper() in existing_tables

                if table_exists:
                    self.log_info(f"Table {table_name} already exists")
                    return FlextResult[bool].ok(value=True)

                # Create table using SQL execution (since create_table_ddl doesn't exist)
                ddl_sql = self._build_create_table_sql(table_name, schema)

                # Execute DDL using execute method
                exec_result = connected_api.execute_sql(ddl_sql)
                if exec_result.is_failure:
                    return FlextResult[bool].fail(
                        f"Failed to create table: {exec_result.error}",
                    )

                self.log_info(f"Created table {table_name}")
                return FlextResult[bool].ok(value=True)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to ensure table exists", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Table creation failed: {e}")

    def load_record(
        self,
        stream_name: str,
        record_data: Mapping[str, t.JsonValue],
    ) -> FlextResult[bool]:
        """Load record with batching."""
        try:
            if stream_name not in self.record_buffers:
                self.record_buffers[stream_name] = []

            self.record_buffers[stream_name].append(dict(record_data))
            self.total_records += 1

            # Auto-flush if batch is full
            if len(self.record_buffers[stream_name]) >= self.target_config.batch_size:
                return self._flush_batch(stream_name)

            return FlextResult[bool].ok(value=True)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to load record", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Record loading failed: {e}")

    def finalize_all_streams(
        self,
    ) -> FlextResult[m.TargetOracle.LoaderFinalizeResult]:
        """Finalize all streams and return stats using standardized models."""
        try:
            started_at = str(datetime.now(UTC))
            records_failed = 0

            # Flush all remaining records
            for stream_name, records in self.record_buffers.items():
                if records:
                    result = self._flush_batch(stream_name)
                    if result.is_failure:
                        records_failed += len(records)
                        self.log_error(f"Failed to flush {stream_name}: {result.error}")

            return FlextResult[m.TargetOracle.LoaderFinalizeResult].ok(
                m.TargetOracle.LoaderFinalizeResult(
                    total_records=self.total_records,
                    streams_processed=len(self.record_buffers),
                    loading_operation=m.TargetOracle.LoaderOperation(
                        stream_name="all_streams",
                        started_at=started_at,
                        completed_at=str(datetime.now(UTC)),
                        records_loaded=self.total_records,
                        records_failed=records_failed,
                    ),
                    buffer_status={
                        stream: len(records)
                        for stream, records in self.record_buffers.items()
                    },
                )
            )

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to finalize streams", extra={"error": str(e)})
            return FlextResult[m.TargetOracle.LoaderFinalizeResult].fail(
                f"Finalization failed: {e}"
            )

    def _build_create_table_sql(
        self,
        table_name: str,
        _schema: Mapping[str, t.JsonValue],
    ) -> str:
        """Build CREATE TABLE SQL statement."""
        schema_name = self.target_config.default_target_schema
        full_table_name = f"{schema_name}.{table_name}"

        # Create simple JSON table for Singer data
        sql = (
            """
 CREATE TABLE """
            + full_table_name
            + """ (
 DATA CLOB,
 _SDC_EXTRACTED_AT TIMESTAMP,
 _SDC_LOADED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 )
 """
        )

        return sql.strip()

    def _flush_batch(self, stream_name: str) -> FlextResult[bool]:
        """Flush batch using flext-db-oracle API exclusively - NO direct SQLAlchemy."""
        try:
            records = self.record_buffers.get(stream_name, [])
            if not records:
                return FlextResult[bool].ok(value=True)

            table_name = self.target_config.get_table_name(stream_name)
            schema_name = self.target_config.default_target_schema
            full_table_name = f"{schema_name}.{table_name}"
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$.]*", full_table_name):
                return FlextResult[bool].fail("Invalid Oracle table identifier")
            loaded_at = datetime.now(UTC).isoformat()

            with self.oracle_api as connected_api:
                # Use flext-db-oracle API for all SQL operations - ZERO direct SQLAlchemy
                for record in records:
                    insert_sql = f"INSERT INTO {full_table_name} (DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) VALUES (:data, :extracted_at, :loaded_at)"  # nosec B608

                    # Execute parameterized query through flext-db-oracle
                    params: dict[str, t.JsonValue] = {
                        "data": json.dumps(record),
                        "extracted_at": str(record.get("_sdc_extracted_at", loaded_at)),
                        "loaded_at": loaded_at,
                    }

                    result = connected_api.execute_sql(
                        insert_sql,
                        parameters=params,
                    )
                    if result.is_failure:
                        return FlextResult[bool].fail(
                            f"Batch insert failed: {result.error}",
                        )

                # Clear buffer
                self.record_buffers[stream_name] = []

                self.log_info(f"Flushed {len(records)} records to {table_name}")
                return FlextResult[bool].ok(value=True)

        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.log_error("Failed to flush batch", extra={"error": str(e)})
            return FlextResult[bool].fail(f"Batch flush failed: {e}")


__all__ = [
    "FlextTargetOracleLoader",
]
