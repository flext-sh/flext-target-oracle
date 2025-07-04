"""Oracle performance optimizer.

Implements Oracle-specific optimizations for high-performance data loading.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...core.models.config import CompressionType, LoadMethod

if TYPE_CHECKING:
    from ...core.models.config import OracleConfig, PerformanceConfig

logger = logging.getLogger(__name__)


class OracleOptimizer:
    """Oracle-specific performance optimizer."""

    def __init__(self, config: OracleConfig, performance_config: PerformanceConfig) -> None:
        """Initialize optimizer with configuration."""
        self._config = config
        self._performance = performance_config

    def get_table_options(self, table_name: str) -> dict[str, Any]:
        """Get Oracle table creation options for performance."""
        options = {}
        
        # Compression settings
        if self._performance.compression_type != CompressionType.NONE:
            options["compress"] = self._get_compression_clause()
        
        # Parallel settings
        if self._performance.enable_parallel_dml:
            options["parallel"] = f"PARALLEL {self._performance.parallel_threads}"
        
        # In-memory settings (requires Oracle In-Memory option)
        if self._performance.in_memory and self._config.oracle_is_enterprise_edition:
            options["inmemory"] = self._get_inmemory_clause()
        
        # NOLOGGING for bulk operations
        if self._performance.nologging:
            options["logging"] = "NOLOGGING"
        
        return options

    def get_insert_hints(self, batch_size: int) -> list[str]:
        """Get Oracle hints for insert operations."""
        hints = []
        
        # Direct path insert for large batches
        if self._performance.use_direct_path and batch_size > 1000:
            if self._performance.append_values_hint:
                hints.append("APPEND_VALUES")
            else:
                hints.append("APPEND")
        
        # Parallel DML hint
        if self._performance.enable_parallel_dml:
            hints.append(f"PARALLEL({self._performance.parallel_threads})")
        
        # Cache hint for small lookups
        if batch_size < 100:
            hints.append("CACHE")
        
        return hints

    def get_session_parameters(self) -> dict[str, str]:
        """Get Oracle session parameters for optimization."""
        params = {}
        
        # Enable parallel DML
        if self._performance.enable_parallel_dml:
            params["PARALLEL_DML_MODE"] = "ENABLED"
            params["PARALLEL_DEGREE_POLICY"] = "AUTO"
            params["PARALLEL_MIN_SERVERS"] = str(self._performance.parallel_threads)
        
        # Optimize for bulk operations
        if self._config.load_method == LoadMethod.APPEND_ONLY:
            params["OPTIMIZER_MODE"] = "ALL_ROWS"
            params["_OPTIMIZER_BATCH_TABLE_ACCESS_BY_ROWID"] = "TRUE"
        
        # Memory settings
        params["WORKAREA_SIZE_POLICY"] = "AUTO"
        params["PGA_AGGREGATE_TARGET"] = "2G"  # Adjust based on available memory
        
        # Direct path settings
        if self._performance.use_direct_path:
            params["_DIRECT_PATH_INSERT_MODE"] = "TRUE"
        
        return params

    def get_bulk_load_sql(self, table_name: str, columns: list[str], batch_size: int) -> str:
        """Generate optimized bulk load SQL."""
        hints = self.get_insert_hints(batch_size)
        hint_clause = f"/*+ {' '.join(hints)} */" if hints else ""
        
        placeholders = [f":{col}" for col in columns]
        
        sql = f"""
        INSERT {hint_clause} INTO {table_name} (
            {', '.join(columns)}
        ) VALUES (
            {', '.join(placeholders)}
        )
        """
        
        return sql.strip()

    def get_merge_sql(self, table_name: str, columns: list[str], key_columns: list[str]) -> str:
        """Generate optimized merge SQL."""
        # Build merge conditions
        merge_conditions = [f"target.{col} = source.{col}" for col in key_columns]
        
        # Build update set clause (exclude key columns)
        update_columns = [col for col in columns if col not in key_columns]
        update_set = [f"target.{col} = source.{col}" for col in update_columns]
        
        # Build source columns
        source_columns = [f":{col} AS {col}" for col in columns]
        
        sql = f"""
        MERGE /*+ PARALLEL({self._performance.parallel_threads}) */ 
        INTO {table_name} target
        USING (
            SELECT {', '.join(source_columns)}
            FROM dual
        ) source
        ON ({' AND '.join(merge_conditions)})
        WHEN MATCHED THEN
            UPDATE SET {', '.join(update_set)}
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(columns)})
            VALUES ({', '.join([f'source.{col}' for col in columns])})
        """
        
        return sql.strip()

    def optimize_connection_parameters(self, connection: Any) -> None:
        """Apply optimizations to database connection."""
        # Set array size for bulk fetches
        connection.arraysize = 1000
        
        # Set prefetch rows
        connection.prefetchrows = 1000
        
        # Disable autocommit for batch operations
        connection.autocommit = False
        
        # Set statement cache size
        connection.stmtcachesize = 50

    def get_index_recommendations(self, table_name: str, columns: list[str], key_columns: list[str]) -> list[str]:
        """Get index creation recommendations."""
        indexes = []
        
        # Primary key index (handled by constraint)
        if key_columns:
            # Additional indexes for foreign key lookups
            for col in columns:
                if col.endswith("_ID") and col not in key_columns:
                    indexes.append(f"CREATE INDEX IX_{table_name}_{col} ON {table_name}({col})")
        
        # Timestamp indexes for incremental loads
        for col in columns:
            if col in ["MOD_TS", "CREATE_TS", "UPDATED_AT", "CREATED_AT"]:
                indexes.append(f"CREATE INDEX IX_{table_name}_{col} ON {table_name}({col})")
        
        # Composite indexes for common queries
        if "COMPANY_CODE" in columns and "FACILITY_CODE" in columns:
            indexes.append(
                f"CREATE INDEX IX_{table_name}_COMP_FAC ON {table_name}(COMPANY_CODE, FACILITY_CODE)"
            )
        
        return indexes

    def _get_compression_clause(self) -> str:
        """Get Oracle compression clause."""
        compression_map = {
            CompressionType.BASIC: "COMPRESS BASIC",
            CompressionType.ADVANCED: "COMPRESS FOR OLTP",
            CompressionType.QUERY_HIGH: "COMPRESS FOR QUERY HIGH",
            CompressionType.QUERY_LOW: "COMPRESS FOR QUERY LOW",
            CompressionType.ARCHIVE_HIGH: "COMPRESS FOR ARCHIVE HIGH",
            CompressionType.ARCHIVE_LOW: "COMPRESS FOR ARCHIVE LOW",
        }
        
        clause = compression_map.get(self._performance.compression_type, "")
        
        # Validate license compliance
        if self._performance.compression_type in [
            CompressionType.ADVANCED,
            CompressionType.QUERY_HIGH,
            CompressionType.QUERY_LOW,
            CompressionType.ARCHIVE_HIGH,
            CompressionType.ARCHIVE_LOW,
        ]:
            if not self._config.oracle_has_advanced_compression:
                logger.warning(
                    f"Advanced compression type '{self._performance.compression_type}' "
                    "requires Oracle Advanced Compression option"
                )
                return "COMPRESS BASIC"  # Fallback to basic
        
        return clause

    def _get_inmemory_clause(self) -> str:
        """Get Oracle in-memory clause."""
        priority_map = {
            "none": "INMEMORY NO PRIORITY",
            "low": "INMEMORY PRIORITY LOW",
            "medium": "INMEMORY PRIORITY MEDIUM",
            "high": "INMEMORY PRIORITY HIGH",
            "critical": "INMEMORY PRIORITY CRITICAL",
        }
        
        return priority_map.get(
            self._performance.in_memory_priority.lower(),
            "INMEMORY"
        )

    def estimate_memory_requirements(self, row_count: int, avg_row_size: int) -> dict[str, float]:
        """Estimate memory requirements for operations."""
        # Base memory per row (bytes)
        memory_per_row = avg_row_size
        
        # Add overhead for indexes (20% estimate)
        index_overhead = memory_per_row * 0.2
        
        # Sort memory (for ORDER BY, GROUP BY)
        sort_memory = row_count * (memory_per_row + index_overhead) * 0.1
        
        # Hash memory (for joins, aggregations)
        hash_memory = row_count * memory_per_row * 0.15
        
        # PGA memory recommendation
        pga_memory = max(
            sort_memory + hash_memory,
            100 * 1024 * 1024  # Minimum 100MB
        )
        
        # Buffer cache recommendation
        buffer_cache = row_count * memory_per_row * 0.25
        
        return {
            "pga_memory_mb": pga_memory / (1024 * 1024),
            "buffer_cache_mb": buffer_cache / (1024 * 1024),
            "total_memory_mb": (pga_memory + buffer_cache) / (1024 * 1024),
        }