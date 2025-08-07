"""Oracle Data Loading Infrastructure - CORRECT Implementation.

CORRETO: Este módulo usa APENAS a API pública da flext-db-oracle,
sem duplicar funcionalidades que já existem na biblioteca abstrata.

Seguindo as regras de negócio:
1. Funcionalidades genéricas ficam em flext-db-oracle
2. API pública é usada corretamente
3. Sem código duplicado
4. Classes específicas para target Oracle apenas

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger
from flext_db_oracle import FlextDbOracleApi, FlextDbOracleConfig

from flext_target_oracle.exceptions import (
    FlextTargetOracleConnectionError,
)

if TYPE_CHECKING:
    from flext_target_oracle.config import FlextTargetOracleConfig

logger = get_logger(__name__)


class FlextTargetOracleLoader:
    """Oracle data loader - CORRETO usando apenas flext-db-oracle API pública.

    Esta implementação:
    1. Usa APENAS a API pública da flext-db-oracle
    2. Não duplica funcionalidades genéricas
    3. Mantém apenas o código específico para Singer target
    """

    def __init__(self, config: FlextTargetOracleConfig) -> None:
        """Initialize loader using flext-db-oracle correctly."""
        self.config = config

        # Use flext-db-oracle configuration
        oracle_config_dict = config.get_oracle_config()
        oracle_config_result = FlextDbOracleConfig.from_dict(
            dict(oracle_config_dict),
        )
        if oracle_config_result.is_failure:
            msg = f"Failed to create Oracle config: {oracle_config_result.error}"
            raise FlextTargetOracleConnectionError(
                msg,
                host=config.oracle_host,
                port=config.oracle_port,
                service_name=config.oracle_service,
            )

        # Initialize Oracle API - CORRETA integração
        oracle_config = oracle_config_result.data
        self.oracle_api = FlextDbOracleApi(oracle_config)

        # Simple state tracking - específico para Singer target
        self._record_buffers: dict[str, list[dict[str, object]]] = {}
        self._total_records = 0

    async def ensure_table_exists(
        self,
        stream_name: str,
        _schema: dict[str, object],
        _key_properties: list[str] | None = None,
    ) -> FlextResult[None]:
        """Ensure table exists using flext-db-oracle API."""
        try:
            table_name = self.config.get_table_name(stream_name)

            # Use flext-db-oracle context manager CORRETAMENTE
            with self.oracle_api as connected_api:
                # Check if table exists usando API
                tables_result = connected_api.get_tables(
                    schema=self.config.default_target_schema,
                )

                if tables_result.is_failure:
                    return FlextResult.fail(f"Failed to check tables: {tables_result.error}")

                existing_tables = [t.upper() for t in tables_result.data or []]
                table_exists = table_name.upper() in existing_tables

                if table_exists:
                    logger.info("Table %s already exists", table_name)
                    return FlextResult.ok(None)

                # Create simple JSON table usando API pública
                columns = [
                    {
                        "name": "DATA",
                        "type": "CLOB",
                        "nullable": True,
                    },
                    {
                        "name": "_SDC_EXTRACTED_AT",
                        "type": "TIMESTAMP",
                        "nullable": True,
                    },
                    {
                        "name": "_SDC_LOADED_AT",
                        "type": "TIMESTAMP",
                        "nullable": True,
                        "default": "CURRENT_TIMESTAMP",
                    },
                ]

                # Create and execute table DDL using flext-db-oracle API
                ddl_result = connected_api.create_table_ddl(
                    table_name=table_name,
                    columns=columns,
                    schema=self.config.default_target_schema,
                )

                if ddl_result.is_failure:
                    return FlextResult.fail(f"Failed to create DDL: {ddl_result.error}")

                # Execute DDL - handle None case and execution result together
                ddl_sql = ddl_result.data
                if ddl_sql is None:
                    return FlextResult.fail("DDL creation returned None")

                exec_result = connected_api.execute_ddl(ddl_sql)
                logger.info("Created table %s", table_name) if exec_result.is_success else None

                return (
                    FlextResult.ok(None)
                    if exec_result.is_success
                    else FlextResult.fail(f"Failed to create table: {exec_result.error}")
                )

        except Exception as e:
            logger.exception("Failed to ensure table exists")
            return FlextResult.fail(f"Table creation failed: {e}")

    async def load_record(
        self,
        stream_name: str,
        record_data: dict[str, object],
    ) -> FlextResult[None]:
        """Load record with batching."""
        try:
            # Simple buffering - específico para Singer target
            if stream_name not in self._record_buffers:
                self._record_buffers[stream_name] = []

            self._record_buffers[stream_name].append(record_data)
            self._total_records += 1

            # Auto-flush if batch is full
            if len(self._record_buffers[stream_name]) >= self.config.batch_size:
                return await self._flush_batch(stream_name)

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to load record")
            return FlextResult.fail(f"Record loading failed: {e}")

    async def finalize_all_streams(self) -> FlextResult[dict[str, object]]:
        """Finalize all streams and return stats."""
        try:
            # Flush all remaining records
            for stream_name, records in self._record_buffers.items():
                if records:
                    result = await self._flush_batch(stream_name)
                    if result.is_failure:
                        logger.error(
                            f"Failed to flush {stream_name}: {result.error}",
                        )

            stats: dict[str, object] = {
                "total_records": self._total_records,
                "streams_processed": len(self._record_buffers),
            }

            return FlextResult.ok(stats)

        except Exception as e:
            logger.exception("Failed to finalize streams")
            return FlextResult.fail(f"Finalization failed: {e}")

    async def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush batch usando flext-db-oracle API CORRETAMENTE."""
        try:
            records = self._record_buffers.get(stream_name, [])
            if not records:
                return FlextResult.ok(None)

            table_name = self.config.get_table_name(stream_name)
            loaded_at = datetime.now(UTC)

            # Use flext-db-oracle API para bulk operations
            with self.oracle_api as connected_api:
                # Prepare SQL usando API pública
                sql_result = connected_api.build_insert_statement(
                    table_name=table_name,
                    columns=["DATA", "_SDC_EXTRACTED_AT", "_SDC_LOADED_AT"],
                    schema_name=self.config.default_target_schema,
                )

                if sql_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to build INSERT: {sql_result.error}",
                    )

                # Prepare batch data with correct types
                batch_operations: list[tuple[str, dict[str, object] | None]] = []
                sql_str = sql_result.data
                if sql_str is None:
                    return FlextResult.fail("INSERT statement creation returned None")

                for record in records:
                    params: dict[str, object] = {
                        "DATA": json.dumps(record),
                        "_SDC_EXTRACTED_AT": record.get("_sdc_extracted_at", loaded_at),
                        "_SDC_LOADED_AT": loaded_at,
                    }
                    batch_operations.append((sql_str, params))

                # Execute batch usando API pública CORRETAMENTE
                result = connected_api.execute_batch(batch_operations)
                if result.is_failure:
                    return FlextResult.fail(
                        f"Batch insert failed: {result.error}",
                    )

                # Clear buffer
                self._record_buffers[stream_name] = []

                logger.info(
                    "Flushed %d records to %s", len(records), table_name,
                )
                return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to flush batch")
            return FlextResult.fail(f"Batch flush failed: {e}")
