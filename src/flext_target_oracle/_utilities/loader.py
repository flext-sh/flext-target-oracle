"""Oracle Data Loader using s and SOURCE OF TRUTH patterns.

ZERO DUPLICATION - Uses flext-db-oracle API exclusively.
SOLID COMPLIANCE - Single responsibility: Oracle data loading only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import (
    Mapping,
    Sequence,
)
from datetime import UTC, datetime
from operator import itemgetter
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
    _stream_columns: dict[str, tuple[m.DbOracle.Column, ...]] = u.PrivateAttr(
        default_factory=dict,
    )
    _stream_field_mappings: dict[str, tuple[tuple[str, str], ...]] = u.PrivateAttr(
        default_factory=dict,
    )
    _stream_key_columns: dict[str, tuple[str, ...]] = u.PrivateAttr(
        default_factory=dict,
    )
    _total_records: int = u.PrivateAttr(default_factory=lambda: 0)

    @staticmethod
    def _normalize_log_value(value: t.Scalar) -> t.JsonValue:
        """Normalize logging payloads into scalar or string values."""
        if isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    def _loader_columns(
        self,
        stream_name: str,
        schema: t.JsonMapping,
        key_properties: t.StrSequence | None,
    ) -> p.Result[tuple[m.DbOracle.Column, ...]]:
        """Build and cache Oracle column metadata for one Singer stream."""
        try:
            properties_value = schema.get("properties", {})
            properties = (
                t.json_mapping_adapter().validate_json(properties_value)
                if isinstance(properties_value, str)
                else t.json_mapping_adapter().validate_python(properties_value)
            )
            normalized_schema = t.json_mapping_adapter().validate_python({
                "properties": properties,
            })
            type_mapping_result = self.oracle_api.oracle_services.map_singer_schema(
                normalized_schema,
            )
            if type_mapping_result.failure or type_mapping_result.value is None:
                return r[tuple[m.DbOracle.Column, ...]].fail(
                    type_mapping_result.error
                    or "Failed to map Singer schema to Oracle",
                )
            stream_mappings = t.TargetOracle.STR_MAP_ADAPTER.validate_python(
                self.target_config.column_mappings.get(stream_name, {}),
            )
            ignored_columns = frozenset(self.target_config.ignored_columns)
            key_columns_list: list[str] = []
            for key_name in key_properties or ():
                if key_name in ignored_columns:
                    continue
                key_columns_list.append(
                    (stream_mappings.get(key_name) or key_name).upper(),
                )
            key_columns = tuple(key_columns_list)
            json_storage_enabled = self.target_config.storage_mode in {
                c.TargetOracle.STORAGE_MODE_JSON,
                c.TargetOracle.STORAGE_MODE_HYBRID,
            }
            field_mappings: list[tuple[str, str]] = []
            columns: list[m.DbOracle.Column] = []
            for source_name, definition_value in properties.items():
                if source_name in ignored_columns:
                    continue
                definition = (
                    t.json_mapping_adapter().validate_python(definition_value)
                    if isinstance(definition_value, Mapping)
                    else t.json_mapping_adapter().validate_python({})
                )
                field_type_value = definition.get("type", "string")
                if isinstance(field_type_value, str):
                    field_type = field_type_value
                elif isinstance(field_type_value, Sequence) and field_type_value:
                    field_type = next(
                        (
                            str(item)
                            for item in field_type_value
                            if str(item).lower() != "null"
                        ),
                        "string",
                    )
                else:
                    field_type = "string"
                if json_storage_enabled and field_type in {"array", "object"}:
                    continue
                target_name = stream_mappings.get(source_name) or source_name
                field_mappings.append((source_name, target_name))
                column_name = target_name.upper()
                columns.append(
                    m.DbOracle.Column(
                        name=column_name,
                        data_type=(
                            type_mapping_result.value.mapping.get(
                                source_name,
                                c.DbOracle.DEFAULT_VARCHAR_TYPE,
                            )
                        ),
                        nullable=column_name not in key_columns,
                        primary_key=column_name in key_columns,
                    ),
                )
            if json_storage_enabled:
                columns.append(
                    m.DbOracle.Column(
                        name=self.target_config.json_column_name.upper(),
                        data_type=c.DbOracle.DataType.CLOB.value,
                        nullable=True,
                    ),
                )
            columns.extend([
                m.DbOracle.Column(
                    name="_SDC_EXTRACTED_AT",
                    data_type=c.DbOracle.DataType.TIMESTAMP.value,
                    nullable=True,
                ),
                m.DbOracle.Column(
                    name="_SDC_LOADED_AT",
                    data_type=(
                        f"{c.DbOracle.DataType.TIMESTAMP.value} DEFAULT CURRENT_TIMESTAMP"
                    ),
                    nullable=True,
                ),
            ])
            if self.target_config.column_ordering == "alphabetical":
                order_rules = {
                    "primary_keys": 1,
                    "regular_columns": 2,
                    "audit_columns": 3,
                    "sdc_columns": 4,
                }
                order_rules.update(self.target_config.column_order_rules)
                primary_columns = sorted(
                    [column for column in columns if column.primary_key],
                    key=lambda column: column.name,
                )
                sdc_columns = sorted(
                    [column for column in columns if column.name.startswith("_SDC_")],
                    key=lambda column: column.name,
                )
                primary_names = frozenset(column.name for column in primary_columns)
                sdc_names = frozenset(column.name for column in sdc_columns)
                audit_columns = sorted(
                    [
                        column
                        for column in columns
                        if column.name not in primary_names
                        and column.name not in sdc_names
                        and (
                            column.data_type.startswith(
                                c.DbOracle.DataType.TIMESTAMP.value,
                            )
                            or column.name.endswith("_AT")
                        )
                    ],
                    key=lambda column: column.name,
                )
                audit_names = frozenset(column.name for column in audit_columns)
                regular_columns = sorted(
                    [
                        column
                        for column in columns
                        if column.name not in primary_names
                        and column.name not in sdc_names
                        and column.name not in audit_names
                    ],
                    key=lambda column: column.name,
                )
                grouped_columns = {
                    "primary_keys": primary_columns,
                    "regular_columns": regular_columns,
                    "audit_columns": audit_columns,
                    "sdc_columns": sdc_columns,
                }
                columns = [
                    column
                    for group_name, _priority in sorted(
                        order_rules.items(),
                        key=itemgetter(1),
                    )
                    for column in grouped_columns.get(group_name, ())
                ]
            cached_columns = tuple(columns)
            self._stream_columns[stream_name] = cached_columns
            self._stream_field_mappings[stream_name] = tuple(field_mappings)
            self._stream_key_columns[stream_name] = key_columns
            return r[tuple[m.DbOracle.Column, ...]].ok(cached_columns)
        except c.ValidationError as exc:
            return r[tuple[m.DbOracle.Column, ...]].fail(
                f"Invalid Singer schema for {stream_name}: {exc}",
            )

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
            self._stream_columns = {}
            self._stream_field_mappings = {}
            self._stream_key_columns = {}
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
        key_properties: t.StrSequence | None = None,
    ) -> p.Result[bool]:
        """Ensure table exists using flext-db-oracle API with correct table creation."""
        try:
            table_name = self.target_config.get_table_name(stream_name)
            stream_columns_result = self._loader_columns(
                stream_name,
                schema,
                key_properties,
            )
            if stream_columns_result.failure:
                return r[bool].fail(
                    stream_columns_result.error or "Failed to derive Oracle columns",
                )
            with self.oracle_api as connected_api:
                tables_result = connected_api.fetch_tables(
                    schema=self.target_config.default_target_schema,
                )
                if tables_result.failure:
                    return r[bool].fail(
                        f"Failed to check tables: {tables_result.error}",
                    )
                existing_tables_raw = tables_result.value or []
                existing_tables = [table.upper() for table in existing_tables_raw]
                table_exists = table_name.upper() in existing_tables
                if table_exists:
                    if self.target_config.truncate_before_load:
                        truncate_sql = f"TRUNCATE TABLE {self.target_config.default_target_schema}.{table_name}"
                        truncate_result = connected_api.execute_sql(truncate_sql)
                        if truncate_result.failure:
                            return r[bool].fail(
                                f"Failed to truncate table: {truncate_result.error}",
                            )
                        self.log_info(f"Truncated table {table_name}")
                    self.log_info(f"Table {table_name} already exists")
                    return r[bool].ok(value=True)
                ddl_result = connected_api.oracle_services.create_table_ddl(
                    table_name,
                    stream_columns_result.value,
                    schema=self.target_config.default_target_schema,
                )
                if ddl_result.failure:
                    return r[bool].fail(
                        f"Failed to build create table SQL: {ddl_result.error}",
                    )
                ddl_sql = ddl_result.value
                exec_result = connected_api.execute_sql(ddl_sql)
                if exec_result.failure:
                    return r[bool].fail(f"Failed to create table: {exec_result.error}")
                for raw_index in self.target_config.custom_indexes.get(stream_name, ()):
                    columns_value = raw_index.get("columns", ())
                    if isinstance(columns_value, str) or not isinstance(
                        columns_value,
                        Sequence,
                    ):
                        return r[bool].fail(
                            f"Custom index columns must be a sequence for {stream_name}",
                        )
                    index_columns = [str(column).upper() for column in columns_value]
                    if not index_columns:
                        return r[bool].fail(
                            f"Custom index requires at least one column for {stream_name}",
                        )
                    raw_index_name = raw_index.get("name") or raw_index.get(
                        "index_name"
                    )
                    index_name = str(
                        raw_index_name or f"{table_name}_{index_columns[0]}_IDX",
                    )[:30]
                    index_payload = t.json_mapping_adapter().validate_python({
                        "table_name": table_name,
                        "index_name": index_name,
                        "columns": index_columns,
                        "unique": bool(raw_index.get("unique", False)),
                        "schema_name": self.target_config.default_target_schema,
                    })
                    index_sql_result = (
                        connected_api.oracle_services.build_create_index_statement(
                            index_payload,
                        )
                    )
                    if index_sql_result.failure:
                        return r[bool].fail(
                            f"Failed to build create index SQL: {index_sql_result.error}",
                        )
                    index_exec_result = connected_api.execute_sql(
                        index_sql_result.value
                    )
                    if index_exec_result.failure:
                        return r[bool].fail(
                            f"Failed to create index: {index_exec_result.error}",
                        )
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
            copied_record: t.MutableJsonMapping = dict(record_data.items())
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

    def _build_insert_parameters(
        self,
        stream_name: str,
        record: t.JsonMapping,
        loaded_at: str,
    ) -> p.Result[t.JsonMapping]:
        """Normalize one record into the owner-managed insert payload shape."""
        try:
            stream_columns = self._stream_columns.get(stream_name, ())
            if not stream_columns:
                return r[t.JsonMapping].fail(
                    f"No registered schema for stream {stream_name}",
                )
            column_names = frozenset(column.name for column in stream_columns)
            params: t.MutableJsonMapping = {
                column.name: None
                for column in stream_columns
                if not column.name.startswith("_SDC_")
            }
            for source_name, target_name in self._stream_field_mappings.get(
                stream_name,
                (),
            ):
                column_name = target_name.upper()
                if column_name not in column_names:
                    continue
                params[column_name] = record.get(target_name, record.get(source_name))
            if self.target_config.storage_mode in {
                c.TargetOracle.STORAGE_MODE_JSON,
                c.TargetOracle.STORAGE_MODE_HYBRID,
            }:
                params[self.target_config.json_column_name.upper()] = (
                    t.TargetOracle.FLAT_CONTAINER_MAP_ADAPTER.dump_json(record).decode(
                        c.DEFAULT_ENCODING,
                    )
                )
            params["_SDC_EXTRACTED_AT"] = str(
                record.get("_sdc_extracted_at", loaded_at),
            )
            params["_SDC_LOADED_AT"] = loaded_at
            return r[t.JsonMapping].ok(
                t.json_mapping_adapter().validate_python(params),
            )
        except c.ValidationError as exc:
            return r[t.JsonMapping].fail(
                f"Invalid insert parameters for {stream_name}: {exc}",
            )

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
                        stream_columns = self._stream_columns.get(stream_name, ())
                        if not stream_columns:
                            return r[bool].fail(
                                f"No registered schema for stream {stream_name}"
                            )
                        insert_sql_result = (
                            connected_api.oracle_services.build_insert_statement(
                                table_name,
                                [column.name for column in stream_columns],
                                schema=schema_name,
                            )
                        )
                        if insert_sql_result.failure:
                            flush_result = r[bool].fail(
                                f"Failed to build insert SQL: {insert_sql_result.error}",
                            )
                        else:
                            params_list: list[t.JsonMapping] = []
                            for record in records:
                                params_result = self._build_insert_parameters(
                                    stream_name,
                                    record,
                                    loaded_at,
                                )
                                if params_result.failure:
                                    return r[bool].fail(
                                        params_result.error
                                        or "Failed to build insert parameters",
                                    )
                                params_list.append(params_result.value)
                            merge_enabled = (
                                self.target_config.sdc_mode.lower()
                                == c.TargetOracle.LOAD_METHOD_MERGE.lower()
                                or self.target_config.load_method
                                in {
                                    c.TargetOracle.LOAD_METHOD_MERGE,
                                    c.TargetOracle.LOAD_METHOD_BULK_MERGE,
                                }
                            )
                            if merge_enabled and self._stream_key_columns.get(
                                stream_name
                            ):
                                delete_sql_result = connected_api.oracle_services.build_delete_statement(
                                    table_name,
                                    self._stream_key_columns[stream_name],
                                    schema=schema_name,
                                )
                                if delete_sql_result.failure:
                                    return r[bool].fail(
                                        f"Failed to build merge delete SQL: {delete_sql_result.error}",
                                    )
                                for params in params_list:
                                    delete_params = (
                                        t.json_mapping_adapter().validate_python({
                                            key: params[key]
                                            for key in self._stream_key_columns[
                                                stream_name
                                            ]
                                        })
                                    )
                                    delete_result = connected_api.execute_sql(
                                        delete_sql_result.value,
                                        delete_params,
                                    )
                                    if delete_result.failure:
                                        return r[bool].fail(
                                            f"Merge delete failed: {delete_result.error}",
                                        )
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
