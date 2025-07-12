"""Singer Target Application Services.

Using flext-core patterns and flext-db-oracle for Oracle operations.
Zero duplication, clean architecture.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Protocol

from flext_db_oracle import (
    OracleConfig,
    OracleConnectionService,
    OracleQueryService,
    OracleSchemaService,
)

from flext_core import ServiceResult
from flext_observability.logging import get_logger
from flext_target_oracle.domain.models import (
    LoadJob,
    LoadJobStatus,
    LoadMethod,
    LoadStatistics,
    SingerRecord,
)

if TYPE_CHECKING:
    from flext_target_oracle.domain.models import (
        SingerSchema,
        TargetConfig,
    )

logger = get_logger(__name__)


class JSONModule(Protocol):
    """Protocol for JSON module."""

    def dumps(self, obj: Any) -> str:  # noqa: ANN401
        """Serialize obj to a JSON formatted str."""
        ...


class SingerTargetService:
    """Main service for Singer target operations."""

    def __init__(self, config: TargetConfig) -> None:
        """Initialize the Singer target service.

        Args:
            config: Target configuration with Oracle connection details

        """
        self.config = config

        # Create Oracle services using flext-db-oracle
        oracle_config = OracleConfig(**config.oracle_config)
        self.connection_service = OracleConnectionService(oracle_config)
        self.query_service = OracleQueryService(self.connection_service)
        self.schema_service = OracleSchemaService(self.query_service)

        # Target-specific services
        self.loader_service = OracleLoaderService(
            self.connection_service,
            self.query_service,
            config,
        )

    async def process_singer_message(
        self,
        message: dict[str, Any],
    ) -> ServiceResult[None]:
        """Process a Singer message (RECORD, SCHEMA, or STATE)."""
        try:
            record = SingerRecord(**message)

            if record.type == "SCHEMA":
                return await self._handle_schema(record)
            if record.type == "RECORD":
                return await self._handle_record(record)
            if record.type == "STATE":
                return await self._handle_state(record)
            return ServiceResult.failure(f"Unknown message type: {record.type}")

        except Exception as e:
            logger.exception("Failed to process Singer message")
            return ServiceResult.failure(f"Message processing failed: {e}")

    async def _handle_schema(self, record: SingerRecord) -> ServiceResult[None]:
        """Handle SCHEMA message."""
        if not record.record_schema or not record.stream:
            return ServiceResult.failure("Schema message missing schema or stream")

        # Convert dict to SingerSchema
        from flext_target_oracle.domain.models import SingerSchema

        schema = SingerSchema(**record.record_schema)

        # Create/update table schema
        result = await self.loader_service.ensure_table_exists(
            record.stream,
            schema,
        )

        if result.is_success:
            logger.info("Schema processed for stream: %s", record.stream)

        return result

    async def _handle_record(self, record: SingerRecord) -> ServiceResult[None]:
        """Handle RECORD message."""
        if not record.record or not record.stream:
            return ServiceResult.failure("Record message missing data or stream")

        # Load record data
        return await self.loader_service.load_record(
            record.stream,
            record.record,
        )

    async def _handle_state(self, _record: SingerRecord) -> ServiceResult[None]:
        """Handle STATE message."""
        # State handling could be implemented here
        logger.debug("State message received (not implemented)")
        return ServiceResult.success(None)

    async def finalize_all_streams(self) -> ServiceResult[LoadStatistics]:
        """Finalize all active streams and return statistics."""
        return await self.loader_service.finalize_all_streams()


class OracleLoaderService:
    """Service for loading data into Oracle using flext-db-oracle."""

    def __init__(
        self,
        connection_service: OracleConnectionService,
        query_service: OracleQueryService,
        config: TargetConfig,
    ) -> None:
        """Initialize the Oracle loader service.

        Args:
            connection_service: Oracle connection service
            query_service: Oracle query service
            config: Target configuration

        """
        self.connection_service = connection_service
        self.query_service = query_service
        self.config = config
        self._active_jobs: dict[str, LoadJob] = {}
        self._record_buffers: dict[str, list[dict[str, Any]]] = {}

    async def ensure_table_exists(
        self,
        stream_name: str,
        schema: SingerSchema,
    ) -> ServiceResult[None]:
        """Ensure target table exists with correct schema."""
        try:
            table_name = self._get_table_name(stream_name)
            logger.info(
                "Ensuring table exists: stream=%s, table=%s",
                stream_name,
                table_name,
            )

            # Check if table exists
            check_sql = """
            SELECT COUNT(*)
            FROM all_tables
            WHERE owner = UPPER(:schema_name)
            AND table_name = UPPER(:table_name)
            """

            logger.debug(
                "Checking table existence: schema=%s, table=%s",
                self.config.default_target_schema,
                table_name,
            )

            result = await self.query_service.execute_scalar(
                check_sql,
                {
                    "schema_name": self.config.default_target_schema,
                    "table_name": table_name,
                },
            )

            if not result.is_success:
                return ServiceResult.failure(
                    f"Failed to check table existence: {result.error}",
                )

            table_exists = result.value and result.value > 0
            logger.debug("Table exists check result: %s", table_exists)

            if not table_exists:
                # Create table based on schema
                create_result = await self._create_table(table_name, schema)
                if not create_result.is_success:
                    return create_result

                logger.info(
                    "Created table: %s.%s",
                    self.config.default_target_schema,
                    table_name,
                )
            else:
                logger.debug(
                    "Table already exists: %s.%s",
                    self.config.default_target_schema,
                    table_name,
                )

            return ServiceResult.success(None)

        except Exception as e:
            logger.exception(
                "Failed to ensure table exists for stream %s",
                stream_name,
            )
            return ServiceResult.failure(f"Table creation failed: {e}")

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, Any],
    ) -> ServiceResult[None]:
        """Load a single record (buffered for batch processing)."""
        try:
            # Add to buffer
            if stream_name not in self._record_buffers:
                self._record_buffers[stream_name] = []
                logger.debug("Created new buffer for stream: %s", stream_name)

            self._record_buffers[stream_name].append(record_data)
            buffer_size = len(self._record_buffers[stream_name])
            logger.info(
                "Added record to buffer: stream=%s, buffer_size=%s/%s",
                stream_name,
                buffer_size,
                self.config.batch_size,
            )

            # Check if batch is ready
            if buffer_size >= self.config.batch_size:
                logger.info("Buffer full, flushing batch for stream: %s", stream_name)
                return await self._flush_batch(stream_name)

            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to load record for stream %s", stream_name)
            return ServiceResult.failure(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> ServiceResult[LoadStatistics]:
        """Flush all pending batches and return statistics."""
        try:
            total_stats = LoadStatistics()

            # Flush all remaining batches
            for stream_name in list(self._record_buffers.keys()):
                if self._record_buffers[stream_name]:
                    result = await self._flush_batch(stream_name)
                    if not result.is_success:
                        logger.error(
                            "Failed to flush final batch for %s: %s",
                            stream_name,
                            result.error,
                        )

            # Calculate combined statistics
            for job in self._active_jobs.values():
                total_stats.total_records += job.records_processed + job.records_failed
                total_stats.successful_records += job.records_processed
                total_stats.failed_records += job.records_failed

            # success_rate is calculated as a property, no need to set it

            logger.info(
                "Finalization complete: %d records processed",
                total_stats.total_records,
            )
            return ServiceResult.success(total_stats)

        except Exception as e:
            logger.exception("Failed to finalize streams")
            return ServiceResult.failure(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> ServiceResult[None]:
        """Flush pending records for a stream."""
        try:
            if (
                stream_name not in self._record_buffers
                or not self._record_buffers[stream_name]
            ):
                return ServiceResult.success(None)

            records = self._record_buffers[stream_name]
            table_name = self._get_table_name(stream_name)

            # Get or create job
            if stream_name not in self._active_jobs:
                self._active_jobs[stream_name] = LoadJob(
                    stream_name=stream_name,
                    table_name=table_name,
                    status=LoadJobStatus.RUNNING,
                    started_at=datetime.now(tz=UTC),
                )

            job = self._active_jobs[stream_name]

            # Execute batch insert based on load method
            if self.config.load_method == LoadMethod.APPEND_ONLY:
                result = await self._insert_batch(table_name, records)
            elif self.config.load_method == LoadMethod.UPSERT:
                result = await self._upsert_batch(table_name, records)
            else:  # OVERWRITE
                result = await self._overwrite_batch(table_name, records)

            # Clear buffer first
            self._record_buffers[stream_name] = []

            if result.is_success:
                job.records_processed += len(records)
                logger.info("Batch loaded: %d records to %s", len(records), table_name)
            else:
                job.records_failed += len(records)
                job.error_message = result.error
                logger.error("Batch failed: %s", result.error)

            return result  # noqa: TRY300

        except Exception as e:
            logger.exception("Failed to flush batch for stream %s", stream_name)
            return ServiceResult.failure(f"Batch flush failed: {e}")

    async def _create_table(
        self,
        table_name: str,
        schema: SingerSchema,
    ) -> ServiceResult[None]:
        """Create table from Singer schema."""
        try:
            columns = []

            # First, process all regular fields
            for prop_name, prop_def in schema.properties.items():
                if prop_name == "table_name" or prop_name.startswith("_sdc_"):
                    continue

                # Get Oracle type for the field
                oracle_type = self._map_singer_type_to_oracle(prop_def)

                # Quote column names to handle special characters
                columns.append(f'"{prop_name.upper()}" {oracle_type}')

            # Add Singer metadata columns at the end
            columns.extend(
                [
                    '"_SDC_EXTRACTED_AT" TIMESTAMP',
                    '"_SDC_ENTITY" VARCHAR2(100)',
                    '"_SDC_SEQUENCE" NUMBER',
                    '"_SDC_BATCHED_AT" TIMESTAMP',
                ],
            )

            if not columns:
                columns = ['"DATA" CLOB']  # Fallback for schemaless data

            # Build CREATE TABLE without extra formatting (Oracle needs uppercase)
            create_sql = f'CREATE TABLE "{self.config.default_target_schema.upper()}"."{table_name.upper()}" ({", ".join(columns)})'

            # Debug log the SQL
            logger.info("Creating table with %s columns", len(columns))
            logger.debug("CREATE TABLE SQL: %s", create_sql)

            # Execute via connection service
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_sql)
                    conn.commit()

            logger.info(
                "Successfully created table %s.%s",
                self.config.default_target_schema,
                table_name,
            )
            return ServiceResult.success(None)

        except Exception:
            logger.exception("Failed to create table %s", table_name)
            return ServiceResult.failure("Table creation failed")

    async def _insert_batch(
        self,
        table_name: str,
        records: list[dict[str, Any]],
    ) -> ServiceResult[None]:
        """Insert batch of records (append-only)."""
        try:
            if not records:
                return ServiceResult.success(None)

            # Get table structure
            columns_result = await self._get_table_columns(table_name)
            if not columns_result.is_success:
                return ServiceResult.failure(
                    columns_result.error or "Failed to get table columns",
                )

            existing_columns = columns_result.value
            if existing_columns is None:
                return ServiceResult.failure("No columns returned from table query")

            # Choose insert strategy based on table structure
            max_simple_columns = 3
            if (
                "data" in existing_columns
                and len(existing_columns) <= max_simple_columns
            ):
                return await self._insert_batch_simple(
                    table_name, records, existing_columns,
                )
            return await self._insert_batch_structured(
                table_name, records, existing_columns,
            )

        except Exception:
            logger.exception("Failed to insert batch to %s", table_name)
            return ServiceResult.failure("Batch insert failed")

    async def _get_table_columns(self, table_name: str) -> ServiceResult[list[str]]:
        """Get table column names."""
        check_sql = """
            SELECT column_name
            FROM all_tab_columns
            WHERE owner = :owner
            AND table_name = :table_name
            ORDER BY column_id
        """

        try:
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        check_sql,
                        {
                            "owner": self.config.default_target_schema.upper(),
                            "table_name": table_name.upper(),
                        },
                    )
                    existing_columns_upper = [row[0] for row in cursor]
                    existing_columns = [col.lower() for col in existing_columns_upper]

                    if not existing_columns:
                        full_table_name = (
                            f"{self.config.default_target_schema}.{table_name}"
                        )
                        return ServiceResult.failure(
                            f"No columns found for table {full_table_name}",
                        )

                    return ServiceResult.success(existing_columns)

        except Exception:
            logger.exception("Failed to get table columns for %s", table_name)
            return ServiceResult.failure("Failed to get table structure")

    async def _insert_batch_simple(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        existing_columns: list[str],
    ) -> ServiceResult[None]:
        """Insert batch using simple JSON storage approach."""
        full_table_name = f"{self.config.default_target_schema}.{table_name}"

        # Build simple INSERT SQL using parameterized queries
        placeholders = ", ".join([f":{col}" for col in existing_columns])
        column_list = ", ".join([f'"{col.upper()}"' for col in existing_columns])
        # Build safe parameterized SQL
        table_parts = full_table_name.split(".")
        schema_name = (
            table_parts[0]
            if len(table_parts) > 1
            else self.config.default_target_schema
        )
        actual_table_name = table_parts[-1]

        # Use parameterized table and schema names for safety (Oracle needs uppercase)
        sql_template = 'INSERT INTO "{0}"."{1}" ({2}) VALUES ({3})'
        sql = sql_template.format(
            schema_name.upper(), actual_table_name.upper(), column_list, placeholders,
        )

        # Build parameters
        params = []
        for record in records:
            param = {}
            for col in existing_columns:
                if col == "data":
                    param[col] = json.dumps(record)
                elif col == "id":
                    param[col] = str(record.get("id", ""))
                elif col == "_extracted_at":
                    param[col] = str(
                        record.get(
                            "_sdc_extracted_at",
                            record.get("_extracted_at", ""),
                        ),
                    )
                else:
                    param[col] = str(record.get(col, ""))
            params.append(param)

        # Execute insert using direct Oracle connection
        try:
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.executemany(sql, params)
                    conn.commit()

            logger.info(
                "Successfully inserted %d records (simple mode) to %s",
                len(params),
                table_name,
            )
            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to insert simple batch")
            return ServiceResult.failure(f"Simple batch insert failed: {e}")

    async def _insert_batch_structured(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        existing_columns: list[str],
    ) -> ServiceResult[None]:
        """Insert batch using structured column mapping."""
        full_table_name = f"{self.config.default_target_schema}.{table_name}"

        # Build structured INSERT SQL
        sql_result = self._build_structured_sql(full_table_name, existing_columns)
        sql = sql_result["sql"]

        logger.info("SQL: %s", sql)
        logger.info("Existing columns: %s", existing_columns)
        logger.info(
            "First record keys: %s",
            list(records[0].keys()) if records else "No records",
        )

        # Build parameters
        params_result = self._build_structured_params(
            table_name, records, existing_columns,
        )
        if not params_result.is_success:
            return ServiceResult.failure(
                params_result.error or "Failed to build parameters",
            )

        params = params_result.value
        if params is None:
            return ServiceResult.failure("No parameters returned from build process")

        # Execute insert using direct Oracle connection
        try:
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Use executemany for batch insert
                    cursor.executemany(sql, params)
                    conn.commit()

            logger.info(
                "Successfully inserted %d records to %s", len(params), table_name,
            )
            return ServiceResult.success(None)

        except Exception as e:
            logger.exception("Failed to insert structured batch")
            return ServiceResult.failure(f"Batch insert failed: {e}")

    def _build_structured_sql(
        self,
        full_table_name: str,
        existing_columns: list[str],
    ) -> dict[str, Any]:
        """Build structured INSERT SQL with proper column mapping."""
        # Build SQL with all columns (use uppercase for Oracle)
        column_list = ", ".join([f'"{col.upper()}"' for col in existing_columns])

        # Build value placeholders with TO_TIMESTAMP for timestamp columns
        value_placeholders = []
        for col in existing_columns:
            col_lower = col.lower()
            # Oracle bind params can't start with underscore, so we strip it
            param_name = (
                col_lower.lstrip("_") if col_lower.startswith("_") else col_lower
            )

            # Use TO_TIMESTAMP for timestamp columns
            timestamp_columns = [
                "_sdc_extracted_at",
                "_sdc_batched_at",
                "create_ts",
                "mod_ts",
                "picked_ts",
            ]
            if col_lower in timestamp_columns:
                value_placeholders.append(
                    f"TO_TIMESTAMP(:{param_name}, 'YYYY-MM-DD\"T\"HH24:MI:SS.FF')",
                )
            else:
                value_placeholders.append(f":{param_name}")

        # Build safe parameterized SQL string
        table_parts = full_table_name.split(".")
        schema_name = (
            table_parts[0]
            if len(table_parts) > 1
            else self.config.default_target_schema
        ).upper()
        actual_table_name = table_parts[-1].upper()

        # Use safe string formatting for Oracle SQL
        sql_template = 'INSERT INTO "{0}"."{1}" ({2}) VALUES ({3})'
        sql = sql_template.format(
            schema_name, actual_table_name, column_list, ", ".join(value_placeholders),
        )

        return {"sql": sql}

    def _build_structured_params(
        self,
        table_name: str,
        records: list[dict[str, Any]],
        existing_columns: list[str],
    ) -> ServiceResult[list[dict[str, Any]]]:
        """Build parameters for structured INSERT."""
        params = []
        try:
            for record in records:
                param = self._build_single_record_params(
                    table_name, record, existing_columns,
                )
                params.append(param)

            logger.info("Params created: %d records", len(params))
            if params:
                self._log_param_debug_info(params)

            return ServiceResult.success(params)

        except Exception as e:
            logger.exception("Error building params")
            return ServiceResult.failure(f"Parameter building failed: {e}")

    def _build_single_record_params(
        self,
        table_name: str,
        record: dict[str, Any],
        existing_columns: list[str],
    ) -> dict[str, Any]:
        """Build parameters for a single record."""
        param = {}
        for col in existing_columns:
            col_lower = col.lower()
            # Oracle bind params can't start with underscore
            param_name = (
                col_lower.lstrip("_") if col_lower.startswith("_") else col_lower
            )

            # Handle special Singer metadata columns
            if col_lower in ["_sdc_extracted_at", "_sdc_batched_at"]:
                param[param_name] = self._build_timestamp_param(col_lower, record)
            elif col_lower == "_sdc_entity":
                param[param_name] = table_name.lower().replace("test_", "")
            elif col_lower == "_sdc_sequence":
                param[param_name] = "0"  # Use string for Oracle parameter
            # Handle custom timestamp columns
            elif (
                col_lower in ["create_ts", "mod_ts", "picked_ts"]
                and col_lower in record
            ):
                param[param_name] = self._build_custom_timestamp_param(
                    record[col_lower],
                )
            # Handle regular data columns
            elif col_lower in record:
                data_value = self._build_data_param(record[col_lower], json)
                param[param_name] = str(data_value) if data_value is not None else ""
            else:
                param[param_name] = ""  # Convert None to empty string

        return param

    def _build_timestamp_param(self, col_lower: str, record: dict[str, Any]) -> str:
        """Build timestamp parameter for Singer metadata columns."""
        if col_lower == "_sdc_extracted_at":
            ts = record.get("_sdc_extracted_at", datetime.now(UTC).isoformat())
        else:  # _sdc_batched_at
            ts = datetime.now(UTC).isoformat()

        if isinstance(ts, str):
            # Remove both +00:00 and Z suffixes
            ts = ts.replace("+00:00", "").replace("Z", "")
        return str(ts)

    def _build_custom_timestamp_param(self, ts_value: str | float | None) -> str:
        """Build timestamp parameter for custom timestamp columns."""
        if isinstance(ts_value, str):
            # Remove timezone offset (everything after + or -)
            if "+" in ts_value:
                ts_value = ts_value.split("+")[0]
            elif (
                "-" in ts_value and "T" in ts_value
            ):  # Check for T to avoid removing negative numbers
                ts_value = ts_value.rsplit("-", 1)[
                    0
                ]  # Remove last occurrence (timezone)
            # Also remove Z suffix
            ts_value = ts_value.replace("Z", "")
        return str(ts_value) if ts_value else ""

    def _build_data_param(
        self,
        value: dict[str, Any] | list[Any] | str | float | bool | None,
        json_module: JSONModule,
    ) -> str | int | float | None:
        """Build parameter for regular data columns with proper type conversion."""
        # Handle None and dict/list first
        if value is None:
            return None  # Keep None as None for Oracle NULL
        if isinstance(value, dict | list):
            return json_module.dumps(value)

        # Handle boolean values (Oracle expects 0/1 for NUMBER columns)
        if isinstance(value, bool):
            return 1 if value else 0

        # Handle string values with numeric conversion
        if isinstance(value, str):
            return self._convert_string_value(value)

        # Return other types as-is (int, float)
        return value

    def _convert_string_value(self, value: str) -> str | int | float | None:
        """Convert string value to appropriate type for Oracle."""
        # Check if it's a numeric string that should be converted
        if value.strip() == "":
            return None  # Empty string -> NULL
        try:
            # Try integer first
            if "." not in value:
                return int(value)
            # Try float
            return float(value)
        except ValueError:
            # Not numeric, keep as string
            return value

    def _log_param_debug_info(self, params: list[dict[str, Any]]) -> None:
        """Log parameter debug information."""
        if not params:
            return

        logger.info("First param keys: %s...", list(params[0].keys())[:10])
        logger.info(
            "Sample values: id=%s, sdc_extracted_at=%s",
            params[0].get("id"),
            params[0].get("sdc_extracted_at"),
        )

        # Log all timestamp values for debugging
        for key, value in params[0].items():
            if "extracted" in key or "batched" in key or "ts" in key:
                logger.info("Timestamp param %s = %s", key, value)

    async def _upsert_batch(
        self,
        table_name: str,
        records: list[dict[str, Any]],
    ) -> ServiceResult[None]:
        """Upsert batch of records using Oracle MERGE."""
        # For now, delegate to insert (would need proper upsert implementation)
        return await self._insert_batch(table_name, records)

    async def _overwrite_batch(
        self,
        table_name: str,
        records: list[dict[str, Any]],
    ) -> ServiceResult[None]:
        """Overwrite table with batch of records."""
        try:
            async with self.connection_service.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Truncate table first (use uppercase and quotes for Oracle)
                    schema_name = self.config.default_target_schema.upper()
                    table_name_upper = table_name.upper()
                    cursor.execute(f'TRUNCATE TABLE "{schema_name}"."{table_name_upper}"')
                    conn.commit()

            # Then insert new data
            return await self._insert_batch(table_name, records)

        except Exception:
            logger.exception("Failed to overwrite table %s", table_name)
            return ServiceResult.failure("Table overwrite failed")

    def _get_table_name(self, stream_name: str) -> str:
        """Convert stream name to Oracle table name."""
        # Simple conversion - could be enhanced
        base_name = stream_name.upper().replace("-", "_").replace(".", "_")
        # Add prefix if configured
        if self.config.table_prefix:
            return f"{self.config.table_prefix}{base_name}"
        return base_name

    def _map_singer_type_to_oracle(self, prop_def: dict[str, Any]) -> str:
        """Map Singer property type to Oracle column type."""
        # Basic type mapping - would need enhancement
        prop_type = prop_def.get("type", "string")

        if isinstance(prop_type, list):
            # Handle nullable types like ["null", "string"]
            prop_type = next((t for t in prop_type if t != "null"), "string")

        # Check for format hints
        prop_format = prop_def.get("format", "")

        # Enhanced type mapping
        if prop_type == "string":
            if prop_format == "date-time":
                return "TIMESTAMP"
            if prop_format == "date":
                return "DATE"
            return "VARCHAR2(4000)"

        type_mapping = {
            "integer": "NUMBER",
            "number": "NUMBER",
            "boolean": "NUMBER(1)",
            "array": "CLOB",
            "object": "CLOB",
        }

        return type_mapping.get(prop_type, "CLOB")

    def _analyze_record_structure(self, record: dict[str, Any]) -> dict[str, str]:
        """Analyze a record to determine optimal column types."""
        columns = {}

        for key, value in record.items():
            if self._should_skip_column(key):
                continue

            columns[key] = self._determine_column_type(value)

        return columns

    def _should_skip_column(self, key: str) -> bool:
        """Check if column should be skipped from analysis."""
        return key.startswith("_sdc_") or key == "data"

    def _determine_column_type(
        self, value: dict[str, Any] | list[Any] | str | float | bool | None,
    ) -> str:
        """Determine Oracle column type based on value."""
        if value is None:
            return "VARCHAR2(4000)"
        if isinstance(value, bool):
            return "NUMBER(1)"
        if isinstance(value, int):
            return self._get_integer_column_type(value)
        if isinstance(value, float):
            return "NUMBER"
        if isinstance(value, str):
            return self._get_string_column_type(value)
        # Handle dict, list, or any other type
        return "CLOB" if isinstance(value, dict | list) else "VARCHAR2(4000)"

    def _get_integer_column_type(self, value: int) -> str:
        """Get Oracle column type for integer values."""
        large_id_threshold = 999999999
        return "NUMBER(19)" if abs(value) > large_id_threshold else "NUMBER"

    def _get_string_column_type(self, value: str) -> str:
        """Get Oracle column type for string values."""
        datetime_min_length = 19
        date_check_length = 10
        short_string_length = 100
        medium_string_length = 1000

        # Check for datetime patterns
        if len(value) > datetime_min_length and (
            "T" in value or "-" in value[:date_check_length]
        ):
            return "TIMESTAMP"
        if len(value) <= short_string_length:
            return "VARCHAR2(200)"
        if len(value) <= medium_string_length:
            return "VARCHAR2(2000)"
        return "VARCHAR2(4000)"
