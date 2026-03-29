"""Oracle Data Loader using FlextService and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-db-oracle API exclusively.
SOLID COMPLIANCE - Single responsibility: Oracle data loading only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import ClassVar, override

from flext_core import FlextLogger, FlextService, r
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleSettings
from pydantic import PrivateAttr, TypeAdapter

from flext_target_oracle import (
    FlextTargetOracleSettings,
    c,
    m,
    p,
    t,
)
from flext_target_oracle._utilities.errors import FlextTargetOracleExceptions

_FLAT_CONTAINER_MAP_ADAPTER: TypeAdapter[t.FlatContainerMapping] = TypeAdapter(
    t.FlatContainerMapping,
)

logger = FlextLogger(__name__)


def _default_record_buffers() -> dict[str, list[t.FlatContainerMapping]]:
    return {}


def _normalize_log_value(value: t.ContainerValue) -> t.NormalizedValue:
    if isinstance(value, (str, int, float, bool, datetime)):
        return value
    return str(value)


class FlextTargetOracleLoader(FlextService[m.TargetOracle.LoaderReadyResult]):
    """Oracle data loader using FlextService and flext-db-oracle SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses ONLY public flext-db-oracle API.
    SOLID COMPLIANCE - Single responsibility: Oracle data loading operations.
    """

    model_config: ClassVar = {"frozen": False}
    _target_config: FlextTargetOracleSettings = PrivateAttr()
    _oracle_api: FlextDbOracleApi = PrivateAttr()
    _record_buffers: dict[str, list[t.FlatContainerMapping]] = PrivateAttr(
        default_factory=_default_record_buffers,
    )
    _total_records: int = PrivateAttr(default=0)

    def __init__(self, config: FlextTargetOracleSettings, **_data: t.Scalar) -> None:
        """Initialize loader with Oracle API using flext-db-oracle correctly."""
        try:
            super().__init__()
            oracle_connection = config.get_oracle_config()
            oracle_config = FlextDbOracleSettings.model_validate({
                "host": oracle_connection.host,
                "port": oracle_connection.port,
                "service_name": oracle_connection.service_name,
                "username": oracle_connection.username,
                "password": oracle_connection.password,
            })
            oracle_api = FlextDbOracleApi(oracle_config)
            self._target_config = config
            self._oracle_api = oracle_api
            self._record_buffers = dict[str, list[t.FlatContainerMapping]]()
            self._total_records = 0
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            msg = f"Failed to create Oracle API: {e}"
            raise FlextTargetOracleExceptions.OracleConnectionError(msg) from e

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Access Oracle API instance."""
        return self._oracle_api

    @property
    def record_buffers(
        self,
    ) -> dict[str, list[t.FlatContainerMapping]]:
        """Access record buffers."""
        return self._record_buffers

    @property
    def target_config(self) -> FlextTargetOracleSettings:
        """Access target configuration."""
        return self._target_config

    @property
    def total_records(self) -> int:
        """Access total records count."""
        return self._total_records

    def _run_connection_operation(
        self,
        *,
        operation_name: str,
        result: p.TargetOracle.ConnectionOperationResult,
    ) -> r[bool]:
        try:
            if result.is_failure:
                return r[bool].fail(f"{operation_name} failed: {result.error}")
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            message = f"Failed to {operation_name.lower()} loader"
            logger.exception(message)
            self.log_error(message, error=str(e))
            return r[bool].fail(f"{operation_name} failed: {e}")

    def connect(self) -> r[bool]:
        """Establish connection using underlying FlextDbOracleApi.

        Exposed for tests and parity with previous loader helpers.
        """
        return self._run_connection_operation(
            operation_name="Connect",
            result=self.oracle_api.connect(),
        )

    def disconnect(self) -> r[bool]:
        """Disconnect underlying FlextDbOracleApi (exposed for tests)."""
        return self._run_connection_operation(
            operation_name="Disconnect",
            result=self.oracle_api.disconnect(),
        )

    def ensure_table_exists(
        self,
        stream_name: str,
        schema: t.FlatContainerMapping,
        _key_properties: Sequence[str] | None = None,
    ) -> r[bool]:
        """Ensure table exists using flext-db-oracle API with correct table creation."""
        try:
            table_name = self.target_config.get_table_name(stream_name)
            with self.oracle_api as connected_api:
                tables_result = connected_api.get_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.is_failure:
                    return r[bool].fail(
                        f"Failed to check tables: {tables_result.error}",
                    )
                existing_tables_raw = tables_result.value or []
                existing_tables = [str(table).upper() for table in existing_tables_raw]
                table_exists = table_name.upper() in existing_tables
                if table_exists:
                    self.log_info(f"Table {table_name} already exists")
                    return r[bool].ok(value=True)
                ddl_sql = self._build_create_table_sql(table_name, schema)
                exec_result = connected_api.execute_sql(ddl_sql)
                if exec_result.is_failure:
                    return r[bool].fail(f"Failed to create table: {exec_result.error}")
                self.log_info(f"Created table {table_name}")
                return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to ensure table exists", error=str(e))
            return r[bool].fail(f"Table creation failed: {e}")

    @override
    def execute(self) -> r[m.TargetOracle.LoaderReadyResult]:
        """Execute domain service - returns connection test result."""
        connection_result = self.test_connection()
        if connection_result.is_failure:
            return r[m.TargetOracle.LoaderReadyResult].fail(
                f"Oracle connection failed: {connection_result.error}",
            )
        return r[m.TargetOracle.LoaderReadyResult].ok(
            m.TargetOracle.LoaderReadyResult.model_validate({
                "status": "ready",
                "host": self.target_config.oracle_host,
                "service": self.target_config.oracle_service_name,
                "schema": self.target_config.default_target_schema,
            }),
        )

    def finalize_all_streams(self) -> r[m.TargetOracle.LoaderFinalizeResult]:
        """Finalize all streams and return stats using standardized models."""
        try:
            started_at = str(datetime.now(UTC))
            records_failed = 0
            for stream_name, records in self.record_buffers.items():
                if records:
                    result = self._flush_batch(stream_name)
                    if result.is_failure:
                        records_failed += len(records)
                        self.log_error(f"Failed to flush {stream_name}: {result.error}")
            return r[m.TargetOracle.LoaderFinalizeResult].ok(
                m.TargetOracle.LoaderFinalizeResult(
                    total_records=self.total_records,
                    streams_processed=len(self.record_buffers),
                    status="completed",
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
                ),
            )
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to finalize streams", error=str(e))
            return r[m.TargetOracle.LoaderFinalizeResult].fail(
                f"Finalization failed: {e}",
            )

    def insert_records(
        self,
        stream_name: str,
        records: Sequence[t.ConfigurationMapping],
    ) -> r[bool]:
        """Insert multiple records - convenience wrapper used by tests.

        Appends records to the internal buffer via load_record and flushes the batch.
        """
        try:
            for record in records:
                load_res = self.load_record(stream_name, record)
                if load_res.is_failure:
                    return r[bool].fail(f"Failed to load record: {load_res.error}")
            return self._flush_batch(stream_name)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to insert records", error=str(e))
            return r[bool].fail(f"Insert records failed: {e}")

    def load_record(
        self,
        stream_name: str,
        record_data: t.FlatContainerMapping,
    ) -> r[bool]:
        """Load record with batching."""
        try:
            if stream_name not in self.record_buffers:
                self.record_buffers[stream_name] = list[t.FlatContainerMapping]()
            self.record_buffers[stream_name].append(dict(record_data))
            self._total_records += 1
            if len(self.record_buffers[stream_name]) >= self.target_config.batch_size:
                return self._flush_batch(stream_name)
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to load record", error=str(e))
            return r[bool].fail(f"Record loading failed: {e}")

    def log_error(self, message: str, **kwargs: t.Scalar) -> None:
        """Log error message."""
        if not kwargs:
            logger.error(message)
            return
        details = ", ".join(
            f"{key}={_normalize_log_value(value)}" for key, value in kwargs.items()
        )
        logger.error("%s | %s", message, details)

    def log_info(self, message: str, **kwargs: t.Scalar) -> None:
        """Log info message."""
        if not kwargs:
            logger.info(message)
            return
        details = ", ".join(
            f"{key}={_normalize_log_value(value)}" for key, value in kwargs.items()
        )
        logger.info("%s | %s", message, details)

    def test_connection(self) -> r[bool]:
        """Test connection to Oracle database using flext-db-oracle API."""
        try:
            with self.oracle_api as connected_api:
                tables_result = connected_api.get_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.is_failure:
                    return r[bool].fail(
                        f"Connection test failed: {tables_result.error}",
                    )
                self.log_info("Oracle connection established successfully")
                return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to connect to Oracle", error=str(e))
            return r[bool].fail(f"Connection failed: {e}")

    def _build_create_table_sql(
        self,
        table_name: str,
        _schema: t.FlatContainerMapping,
    ) -> str:
        """Build CREATE TABLE SQL statement."""
        schema_name = self.target_config.default_target_schema
        full_table_name = f"{schema_name}.{table_name}"
        sql = (
            "\n CREATE TABLE "
            + full_table_name
            + " (\n DATA CLOB,\n _SDC_EXTRACTED_AT TIMESTAMP,\n _SDC_LOADED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n )\n "
        )
        return sql.strip()

    def _flush_batch(self, stream_name: str) -> r[bool]:
        """Flush batch using flext-db-oracle API exclusively - NO direct SQLAlchemy."""
        try:
            records = self.record_buffers.get(stream_name, [])
            if not records:
                return r[bool].ok(value=True)
            table_name = self.target_config.get_table_name(stream_name)
            schema_name = self.target_config.default_target_schema
            full_table_name = f"{schema_name}.{table_name}"
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$.]*", full_table_name):
                return r[bool].fail("Invalid Oracle table identifier")
            loaded_at = datetime.now(UTC).isoformat()
            with self.oracle_api as connected_api:
                for record in records:
                    insert_sql = f"INSERT INTO {full_table_name} (DATA, _SDC_EXTRACTED_AT, _SDC_LOADED_AT) VALUES (:data, :extracted_at, :loaded_at)"  # nosec B608  # table name validated by re.fullmatch above
                    params: t.ConfigurationMapping = {
                        "data": _FLAT_CONTAINER_MAP_ADAPTER.dump_json(record).decode(
                            "utf-8",
                        ),
                        "extracted_at": str(record.get("_sdc_extracted_at", loaded_at)),
                        "loaded_at": loaded_at,
                    }
                    result = connected_api.execute_sql(insert_sql, parameters=params)
                    if result.is_failure:
                        return r[bool].fail(f"Batch insert failed: {result.error}")
                self.record_buffers[stream_name] = list[t.FlatContainerMapping]()
                self.log_info(f"Flushed {len(records)} records to {table_name}")
                return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.log_error("Failed to flush batch", error=str(e))
            return r[bool].fail(f"Batch flush failed: {e}")


__all__ = ["FlextTargetOracleLoader"]
