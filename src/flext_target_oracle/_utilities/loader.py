"""Oracle Data Loader using s and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-db-oracle API exclusively.
SOLID COMPLIANCE - Single responsibility: Oracle data loading only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import (
    Sequence,
)
from datetime import UTC, datetime
from typing import ClassVar, override

from flext_db_oracle import FlextDbOracleApi, FlextDbOracleSettings
from flext_meltano import FlextMeltanoServiceBase, u
from flext_target_oracle import (
    FlextTargetOracleExceptions as e,
    FlextTargetOracleSettings,
    c,
    m,
    p,
    r,
    t,
)


class FlextTargetOracleLoader(FlextMeltanoServiceBase):
    """Oracle data loader using s and flext-db-oracle SOURCE OF TRUTH.

    ZERO DUPLICATION - Uses ONLY public flext-db-oracle API.
    SOLID COMPLIANCE - Single responsibility: Oracle data loading operations.
    """

    @staticmethod
    def _default_record_buffers() -> t.MutableMappingKV[
        str,
        t.MutableSequenceOf[t.JsonMapping],
    ]:
        """Return an empty typed buffer mapping for loader state."""
        empty_buffers: t.MutableMappingKV[
            str,
            t.MutableSequenceOf[t.JsonMapping],
        ] = {}
        return empty_buffers

    model_config: ClassVar = {"frozen": False}
    _target_config: FlextTargetOracleSettings = u.PrivateAttr()
    _oracle_api: FlextDbOracleApi = u.PrivateAttr()
    _record_buffers: t.MutableMappingKV[
        str,
        t.MutableSequenceOf[t.JsonMapping],
    ] = u.PrivateAttr(
        default_factory=_default_record_buffers,
    )
    _total_records: int = u.PrivateAttr(default_factory=lambda: 0)

    @staticmethod
    def _normalize_log_value(value: t.Scalar) -> t.JsonValue:
        """Normalize logging payloads into scalar or string values."""
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    @staticmethod
    def _loader_columns() -> t.MutableSequenceOf[t.JsonMapping]:
        """Return the canonical loader columns for db-oracle DDL generation."""
        return [
            {"name": "DATA", "data_type": "CLOB", "nullable": True},
            {
                "name": "_SDC_EXTRACTED_AT",
                "data_type": "TIMESTAMP",
                "nullable": True,
            },
            {
                "name": "_SDC_LOADED_AT",
                "data_type": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "nullable": True,
            },
        ]

    def __init__(self, settings: FlextTargetOracleSettings, **_data: t.Scalar) -> None:
        """Initialize loader with Oracle API using flext-db-oracle correctly."""
        try:
            super().__init__()
            oracle_connection = settings.get_oracle_config()
            oracle_config = FlextDbOracleSettings.model_validate({
                "host": oracle_connection.host,
                "port": oracle_connection.port,
                "service_name": oracle_connection.service_name,
                "username": oracle_connection.username,
                "password": oracle_connection.password,
            })
            oracle_api = FlextDbOracleApi(oracle_config)
            self._target_config = settings
            self._oracle_api = oracle_api
            self._record_buffers = self._default_record_buffers()
            self._total_records = 0
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            msg = f"Failed to create Oracle API: {exc}"
            raise e.OracleConnectionError(msg) from exc

    @property
    def oracle_api(self) -> FlextDbOracleApi:
        """Access Oracle API instance."""
        return self._oracle_api

    @property
    def record_buffers(
        self,
    ) -> t.MutableMappingKV[
        str,
        t.MutableSequenceOf[t.JsonMapping],
    ]:
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
    ) -> p.Result[bool]:
        try:
            if result.failure:
                return r[bool].fail(f"{operation_name} failed: {result.error}")
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            message = f"Failed to {operation_name.lower()} loader"
            self.logger.exception(message)
            self.log_error(message, error=str(exc))
            return r[bool].fail_op(operation_name.lower(), exc)

    def connect(self) -> p.Result[bool]:
        """Establish connection using underlying FlextDbOracleApi.

        Exposed for tests and parity with previous loader helpers.
        """
        return self._run_connection_operation(
            operation_name="Connect",
            result=self.oracle_api.connect(),
        )

    def disconnect(self) -> p.Result[bool]:
        """Disconnect underlying FlextDbOracleApi (exposed for tests)."""
        return self._run_connection_operation(
            operation_name="Disconnect",
            result=self.oracle_api.disconnect(),
        )

    def ensure_table_exists(
        self,
        stream_name: str,
        schema: t.JsonMapping,
        _key_properties: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Ensure table exists using flext-db-oracle API with correct table creation."""
        try:
            table_name = self.target_config.get_table_name(stream_name)
            with self.oracle_api as connected_api:
                tables_result = connected_api.fetch_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.failure:
                    return r[bool].fail(
                        f"Failed to check tables: {tables_result.error}",
                    )
                existing_tables_raw = tables_result.value or []
                existing_tables = [str(table).upper() for table in existing_tables_raw]
                table_exists = table_name.upper() in existing_tables
                if table_exists:
                    self.log_info(f"Table {table_name} already exists")
                    return r[bool].ok(value=True)
                ddl_result = self._build_create_table_statement(table_name, schema)
                if ddl_result.failure:
                    return r[bool].fail(
                        f"Failed to build create table SQL: {ddl_result.error}",
                    )
                ddl_sql = ddl_result.value
                exec_result = connected_api.execute_sql(ddl_sql)
                if exec_result.failure:
                    return r[bool].fail(f"Failed to create table: {exec_result.error}")
                self.log_info(f"Created table {table_name}")
                return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to ensure table exists", error=str(exc))
            return r[bool].fail_op("create table", exc)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute domain service - returns connection test result."""
        connection_result = self.test_connection()
        if connection_result.failure:
            return r[t.JsonMapping].fail(
                f"Oracle connection failed: {connection_result.error}",
            )
        return r[t.JsonMapping].ok({
            "status": "ready",
            "host": self.target_config.oracle_host,
            "service": self.target_config.oracle_service_name,
            "schema": self.target_config.default_target_schema,
        })

    def finalize_all_streams(self) -> p.Result[m.TargetOracle.LoaderFinalizeResult]:
        """Finalize all streams and return stats using standardized models."""
        try:
            started_at = str(datetime.now(UTC))
            records_failed = 0
            for stream_name, records in self.record_buffers.items():
                if records:
                    result = self._flush_batch(stream_name)
                    if result.failure:
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
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to finalize streams", error=str(exc))
            return r[m.TargetOracle.LoaderFinalizeResult].fail_op(
                "finalize streams", exc
            )

    def insert_records(
        self,
        stream_name: str,
        records: Sequence[t.JsonMapping],
    ) -> p.Result[bool]:
        """Insert multiple records - convenience wrapper used by tests.

        Appends records to the internal buffer via load_record and flushes the batch.
        """
        try:
            for record in records:
                load_res = self.load_record(stream_name, record)
                if load_res.failure:
                    return r[bool].fail(f"Failed to load record: {load_res.error}")
            return self._flush_batch(stream_name)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to insert records", error=str(exc))
            return r[bool].fail_op("insert records", exc)

    def load_record(
        self,
        stream_name: str,
        record_data: t.JsonMapping,
    ) -> p.Result[bool]:
        """Load record with batching."""
        try:
            if stream_name not in self.record_buffers:
                empty_records: t.MutableSequenceOf[t.JsonMapping] = []
                self.record_buffers[stream_name] = empty_records
            copied_record: t.MutableJsonMapping = {
                str(key): value for key, value in record_data.items()
            }
            self.record_buffers[stream_name].append(copied_record)
            self._total_records += 1
            if len(self.record_buffers[stream_name]) >= self.target_config.batch_size:
                return self._flush_batch(stream_name)
            return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to load record", error=str(exc))
            return r[bool].fail_op("load record", exc)

    def log_error(self, message: str, **kwargs: t.Scalar) -> None:
        """Log error message."""
        if not kwargs:
            self.logger.error(message)
            return
        details = ", ".join(
            f"{key}={self._normalize_log_value(value)}" for key, value in kwargs.items()
        )
        self.logger.error("%s | %s", message, details)

    def log_info(self, message: str, **kwargs: t.Scalar) -> None:
        """Log info message."""
        if not kwargs:
            self.logger.info(message)
            return
        details = ", ".join(
            f"{key}={self._normalize_log_value(value)}" for key, value in kwargs.items()
        )
        self.logger.info("%s | %s", message, details)

    def test_connection(self) -> p.Result[bool]:
        """Test connection to Oracle database using flext-db-oracle API."""
        try:
            with self.oracle_api as connected_api:
                tables_result = connected_api.fetch_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.failure:
                    return r[bool].fail(
                        f"Connection test failed: {tables_result.error}",
                    )
                self.log_info("Oracle connection established successfully")
                return r[bool].ok(value=True)
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to connect to Oracle", error=str(exc))
            return r[bool].fail_op("connect to Oracle", exc)

    def _build_create_table_statement(
        self,
        table_name: str,
        _schema: t.JsonMapping,
    ) -> p.Result[str]:
        """Build CREATE TABLE SQL through the db-oracle owner service."""
        return self.oracle_api.oracle_services.create_table_ddl(
            table_name,
            self._loader_columns(),
            schema=self.target_config.default_target_schema,
        )

    def _build_insert_statement(self, table_name: str) -> p.Result[str]:
        """Build INSERT SQL through the db-oracle owner service."""
        return self.oracle_api.oracle_services.build_insert_statement(
            table_name,
            ["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
            schema=self.target_config.default_target_schema,
        )

    @staticmethod
    def _build_insert_parameters(
        record: t.JsonMapping,
        loaded_at: str,
    ) -> t.JsonMapping:
        """Normalize one record into the owner-managed insert payload shape."""
        return {
            "DATA": t.TargetOracle.FLAT_CONTAINER_MAP_ADAPTER.dump_json(record).decode(
                c.DEFAULT_ENCODING,
            ),
            "_SDC_EXTRACTED_AT": str(record.get("_sdc_extracted_at", loaded_at)),
            "_SDC_LOADED_AT": loaded_at,
        }

    def _flush_batch(self, stream_name: str) -> p.Result[bool]:
        """Flush batch using flext-db-oracle API exclusively - NO direct SQLAlchemy."""
        flush_result: p.Result[bool] = r[bool].ok(value=True)
        try:
            records = self.record_buffers.get(stream_name, [])
            if records:
                table_name = self.target_config.get_table_name(stream_name)
                schema_name = self.target_config.default_target_schema
                full_table_name = f"{schema_name}.{table_name}"
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$.]*", full_table_name):
                    flush_result = r[bool].fail_op(
                        "validate Oracle table identifier",
                    )
                else:
                    loaded_at = datetime.now(UTC).isoformat()
                    with self.oracle_api as connected_api:
                        insert_sql_result = self._build_insert_statement(table_name)
                        if insert_sql_result.failure:
                            flush_result = r[bool].fail(
                                f"Failed to build insert SQL: {insert_sql_result.error}",
                            )
                        else:
                            params_list = [
                                self._build_insert_parameters(record, loaded_at)
                                for record in records
                            ]
                            result = connected_api.execute_many(
                                insert_sql_result.value,
                                params_list,
                            )
                            if result.failure:
                                flush_result = r[bool].fail(
                                    f"Batch insert failed: {result.error}",
                                )
                            else:
                                self.record_buffers[stream_name] = list[t.JsonMapping]()
                                self.log_info(
                                    f"Flushed {len(records)} records to {table_name}",
                                )
            return flush_result
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as exc:
            self.log_error("Failed to flush batch", error=str(exc))
            return r[bool].fail_op("flush batch", exc)


__all__: list[str] = ["FlextTargetOracleLoader"]
