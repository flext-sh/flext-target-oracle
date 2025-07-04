"""
High-Performance Oracle Sink with WAN and parallelism optimizations.

Maximizes Oracle Database performance for:
- WAN environments with large latencies
- Parallel processing for massive throughput
- Direct path operations for bulk loads
- Advanced compression and partitioning
"""

from __future__ import annotations

import asyncio
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any

import sqlalchemy
from singer_sdk.sinks import SQLSink
from sqlalchemy import Column, insert, select, update
from sqlalchemy.dialects.oracle import CLOB, NUMBER, TIMESTAMP, VARCHAR2
from sqlalchemy.orm import Mapped, mapped_column

from .connectors import OracleConnector, OracleConnectorBase

if TYPE_CHECKING:
    import datetime

    from singer_sdk.target_base import Target


class OracleTargetTable(OracleConnectorBase):
    """SQLAlchemy 2.x ORM model for Oracle target tables with typed mappings."""

    __abstract__ = True  # This is a base class

    # Standard audit fields with typed mappings
    create_user: Mapped[str | None] = mapped_column(VARCHAR2(255), nullable=True)
    create_ts: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    mod_user: Mapped[str | None] = mapped_column(VARCHAR2(255), nullable=True)
    mod_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=False), nullable=False
    )
    tk_date: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=sqlalchemy.func.current_timestamp(),
        nullable=False
    )

    # Singer SDK metadata fields with typed mappings
    sdc_extracted_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    sdc_received_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    sdc_batched_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    sdc_sequence: Mapped[int | None] = mapped_column(NUMBER(), nullable=True)  # type: ignore[no-untyped-call]
    sdc_table_version: Mapped[int | None] = mapped_column(NUMBER(), nullable=True)  # type: ignore[no-untyped-call]


class OracleSink(SQLSink[OracleConnector]):
    """
    High-performance Oracle sink optimized for WAN and parallel processing.

    Features:
    - Parallel batch processing with configurable threads
    - Direct path inserts with APPEND_VALUES hint
    - Array DML for maximum bulk throughput
    - WAN-optimized chunking and compression
    - Advanced Oracle features (partitioning, in-memory, etc.)
    """

    connector_class = OracleConnector

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize high-performance Oracle sink."""
        super().__init__(target, stream_name, schema, key_properties)

        # Performance configuration
        self._batch_size = self.config.get("batch_size_rows", 50000)
        self._parallel_threads = self.config.get("parallel_threads", 8)
        self._chunk_size = self.config.get("chunk_size", 10000)

        # Thread pool for parallel processing
        if self._parallel_threads > 1:
            self._executor: ThreadPoolExecutor | None = ThreadPoolExecutor(
                max_workers=self._parallel_threads
            )
        else:
            self._executor = None

        # Historical versioning support for time-series data
        self._enable_versioning = self.config.get("enable_historical_versioning", False)
        self._versioning_column = self.config.get(
            "historical_versioning_column", "mod_ts"
        )
        self._original_key_properties = key_properties

        # Logging and monitoring (will be set by target)
        self._logger = None
        self._monitor = None

        # Enhanced statistics tracking
        self._stream_stats: dict[str, Any] = {
            "total_records_received": 0,
            "total_batches_processed": 0,
            "total_records_inserted": 0,
            "total_records_updated": 0,
            "total_records_failed": 0,
            "total_processing_time": 0.0,
            "last_batch_time": None,
            "first_batch_time": None,
            "largest_batch_size": 0,
            "smallest_batch_size": float("inf"),
            "failed_batches": [],
            "successful_operations": 0,
            "database_operations": {
                "inserts": 0,
                "updates": 0,
                "merges": 0,
                "rows_affected": 0,
            },
        }

        # LAZY CONNECTION: Don't connect until we actually need to
        self._schema_prepared = False
        self._connection_established = False

    @property
    def key_properties(self) -> list[str]:
        """Return primary key properties with historical versioning support."""
        if (
            self._enable_versioning
            and self._versioning_column in self.schema.get("properties", {})
            and self._original_key_properties
            and self._versioning_column not in self._original_key_properties
        ):
            # Return composite key: original_keys + versioning_column
            return list(self._original_key_properties) + [self._versioning_column]
        return self._original_key_properties or []

    @property
    def full_table_name(self) -> Any:
        """Return the fully qualified table name with proper prefix handling."""
        # Build table name properly handling ALL naming options
        stream_name = self.stream_name
        schema_name = self.config.get("default_target_schema", "")

        # Apply stream_name_prefix
        if self.config.get("stream_name_prefix"):
            stream_name = f"{self.config['stream_name_prefix']}{stream_name}"

        # Apply table_prefix (standard Singer SDK config name)
        if self.config.get("table_prefix"):
            stream_name = f"{self.config['table_prefix']}{stream_name.upper()}"

        # Handle stream_maps for table name transformation
        stream_maps = self.config.get("stream_maps", {})
        if stream_maps and self.stream_name in stream_maps:
            stream_map = stream_maps[self.stream_name]
            if isinstance(stream_map, dict) and "table_name" in stream_map:
                stream_name = stream_map["table_name"]
                # Apply stream_name_prefix to mapped name too
                if self.config.get("stream_name_prefix"):
                    stream_name = f"{self.config['stream_name_prefix']}{stream_name}"

        # Build full table name
        table = f"{schema_name}.{stream_name}" if schema_name else stream_name

        # Apply Oracle naming constraints (30 chars max for older versions)
        if self.config.get("max_identifier_length", 128) == 30:
            schema_part, table_part = self._parse_full_table_name(table)
            if schema_part:
                table_part = table_part[:30]
                table = f"{schema_part}.{table_part}"
            else:
                table = table[:30]

        return table

    def setup(self) -> None:
        """Set up the sink with LAZY Oracle connection - no DB connection until data."""
        # 🔍 DEBUG: Log schema details before setup
        schema_props = self.schema.get("properties", {})
        self.logger.info(
            (
                "🔍 LAZY SINK SETUP - Stream: %s - Schema properties: %d "
                "(NO DB CONNECTION YET)"
            ),
            self.stream_name,
            len(schema_props),
            extra={
                "stream_name": self.stream_name,
                "schema_properties_count": len(schema_props),
                "schema_properties": list(schema_props.keys())[:20],  # First 20
                "full_schema": (
                    self.schema if len(schema_props) <= 10 else None
                ),  # Full schema only if small
            },
        )

        # 🔍 DEBUG: Check what conform_schema does (no DB connection needed)
        conformed = self.conform_schema(self.schema)
        conformed_props = conformed.get("properties", {})
        self.logger.info(
            "🔍 LAZY SETUP - After conform_schema - Stream: %s - Properties: %d",
            self.stream_name,
            len(conformed_props),
            extra={
                "stream_name": self.stream_name,
                "conformed_properties_count": len(conformed_props),
                "conformed_properties": list(conformed_props.keys())[:20],
            },
        )

        # LAZY SETUP: DON'T call super().setup() here - it tries to connect!
        # Instead, defer all DB operations until first batch arrives

        # Store basic info without DB connection
        self._setup_schema_info()

        # DON'T mark schema as prepared yet - wait for lazy connection

        # 🔍 DEBUG: Log lazy setup completion
        self.logger.info(
            (
                "🔍 LAZY SETUP COMPLETE - Stream: %s - Table will be: %s "
                "(connection deferred)"
            ),
            self.stream_name,
            self.full_table_name,
            extra={
                "stream_name": self.stream_name,
                "table_name": self.full_table_name,
                "lazy_setup_completed": True,
                "connection_deferred": True,
            },
        )

    def _setup_schema_info(self) -> None:
        """Setup schema information without database connection."""
        # This method stores schema info needed later
        # No DB connection required

    def _ensure_connection_and_table(self) -> None:
        """Ensure database connection and table exist - called lazily."""
        if self._connection_established:
            return

        if self._logger:
            self._logger.info(
                (
                    f"🔗 LAZY CONNECTION - Establishing Oracle connection "
                    f"for {self.stream_name}"
                ),
                extra={
                    "stream_name": self.stream_name,
                    "table_name": self.full_table_name,
                    "lazy_connection_trigger": "first_batch_processing",
                },
            )

        try:
            # CUSTOM SETUP: Don't use super().setup() - use our own DDL instead
            self._setup_custom_oracle_table()
            self._connection_established = True

            if self._logger:
                self._logger.info(
                    (
                        f"✅ CUSTOM TABLE CREATION SUCCESSFUL - {self.stream_name} "
                        f"with correct field order and types"
                    ),
                    extra={
                        "stream_name": self.stream_name,
                        "table_name": self.full_table_name,
                        "connection_status": "established",
                    },
                )

        except Exception as e:
            if self._logger:
                self._logger.error(
                    f"❌ CUSTOM TABLE CREATION FAILED - {self.stream_name}: {e}",
                    extra={
                        "stream_name": self.stream_name,
                        "table_name": self.full_table_name,
                        "error": str(e),
                        "connection_status": "failed",
                    },
                    exc_info=True,
                )
            raise

    def _setup_custom_oracle_table(self) -> None:
        """Setup Oracle table using our custom DDL instead of Singer SDK SQLAlchemy."""
        # Step 1: Initialize connection (without table creation)
        if not self.connector._engine:
            # Initialize SQLAlchemy engine by accessing the URL property
            _ = self.connector.sqlalchemy_url

        # Step 2: Create table using our custom DDL
        self._create_oracle_table()

        # Step 3: Setup other Singer SDK components manually
        self._setup_schema_info()

    def _create_oracle_table(self) -> None:
        """Create table with Oracle-compatible column types using SQLAlchemy schema."""
        with self.connector._engine.begin() as conn:
            # Create table using SQLAlchemy Table definition instead of raw DDL
            table_def = self._build_sqlalchemy_table()

            if self._logger:
                self._logger.info(
                    f"Creating Oracle table with SQLAlchemy schema: "
                    f"{self.full_table_name}"
                )

            try:
                # Drop table first if it exists, then create
                table_def.drop(conn, checkfirst=True)
                table_def.create(conn, checkfirst=False)

                if self._logger:
                    self._logger.info(
                        f"✅ Table {self.full_table_name} created successfully "
                        f"with unified rules via SQLAlchemy"
                    )

            except Exception as e:
                if self._logger:
                    self._logger.error(
                        f"❌ Failed to create table {self.full_table_name}: {e}"
                    )
                raise

    def _build_sqlalchemy_table(self) -> sqlalchemy.Table:
        """Build SQLAlchemy Table definition with Oracle types and field order."""
        from sqlalchemy import Column, MetaData, PrimaryKeyConstraint, Table
        from sqlalchemy.dialects.oracle import TIMESTAMP, VARCHAR2

        schema_name, table_name = self._parse_full_table_name(self.full_table_name)
        schema_properties = self.schema.get("properties", {})

        metadata = MetaData()
        columns: list[Column[Any]] = []

        # STEP 1: Find primary key field (prioritize simple 'id' over complex ones)
        primary_key_field = None
        id_fields = [
            name
            for name in schema_properties
            if (
                name.upper() == "ID"
                or (
                    name.upper().endswith("_ID") and not name.upper().endswith("_ID_ID")
                )
            )
        ]

        if id_fields:
            if "id" in [f.lower() for f in id_fields]:
                primary_key_field = next(f for f in id_fields if f.lower() == "id")
            else:
                primary_key_field = id_fields[0]

        # STEP 2: Add PRIMARY KEY first
        if primary_key_field:
            oracle_type = self._get_sqlalchemy_oracle_type(
                primary_key_field, schema_properties[primary_key_field]
            )
            columns.append(
                Column(primary_key_field.upper(), oracle_type, nullable=False)
            )

        # STEP 3: Add OTHER FIELDS (sorted, excluding audit, TK_DATE, and URL fields)
        other_fields = []
        for prop_name in sorted(schema_properties.keys()):
            prop_upper = prop_name.upper()
            if (
                prop_name != primary_key_field
                and prop_upper != "URL"  # Exclude URL fields
                and not prop_upper.endswith("_URL")  # Exclude _URL fields
                and not prop_upper.endswith("_ID_ID")  # Exclude malformed IDs
                and not prop_upper.endswith("_ID_KEY")  # Exclude key fields
                and not prop_upper.endswith("_ID_URL")  # Exclude URL ID fields
                and prop_upper
                not in ["TK_DATE", "CREATE_USER", "CREATE_TS", "MOD_USER", "MOD_TS"]
            ):
                other_fields.append(prop_name)

        for prop_name in other_fields:
            oracle_type = self._get_sqlalchemy_oracle_type(
                prop_name, schema_properties[prop_name]
            )
            columns.append(Column(prop_name.upper(), oracle_type, nullable=True))

        # STEP 4: Add MANDATORY AUDIT FIELDS at the end
        columns.extend(
            [
                Column("CREATE_USER", VARCHAR2(255), nullable=True),
                Column("CREATE_TS", TIMESTAMP(timezone=False), nullable=True),
                Column("MOD_USER", VARCHAR2(255), nullable=True),
                Column("MOD_TS", TIMESTAMP(timezone=False), nullable=False),
            ]
        )

        # STEP 5: Add TK_DATE field (ALWAYS, not conditional)
        columns.append(
            Column(
                "TK_DATE",
                TIMESTAMP(timezone=False),
                server_default=sqlalchemy.func.current_timestamp(),
                nullable=False,
            )
        )

        # Create table with composite primary key
        table = Table(
            table_name.upper(),
            metadata,
            *columns,
            schema=schema_name.upper() if schema_name else None,
        )

        # Add composite primary key constraint
        if primary_key_field:
            table.append_constraint(
                PrimaryKeyConstraint(
                    primary_key_field.upper(), "MOD_TS", name=f"PK_{table_name.upper()}"
                )
            )

        return table

    def _get_sqlalchemy_oracle_type(
        self, column_name: str, column_schema: dict[str, Any]
    ) -> Any:
        """Convert column to SQLAlchemy Oracle type using intelligent mapping.

        This method provides generic type mapping that works for any Oracle database.
        """
        from sqlalchemy.dialects.oracle import CLOB, DATE, NUMBER, TIMESTAMP, VARCHAR2

        # Get type mapping rules (from config or built-in)
        rules = self._get_type_mapping_rules()

        # Convert to Oracle type string using intelligent mapping
        oracle_type_str = self._convert_to_oracle_type(
            column_name, column_schema, rules
        )

        # Convert string type to SQLAlchemy type
        if oracle_type_str == "NUMBER":
            return NUMBER()  # type: ignore[no-untyped-call]
        elif oracle_type_str == "NUMBER(1,0)":
            return NUMBER(1, 0)  # type: ignore[no-untyped-call]
        elif oracle_type_str.startswith("NUMBER("):
            # Parse NUMBER(precision,scale)
            params = oracle_type_str[7:-1].split(",")
            if len(params) == 2:
                return NUMBER(int(params[0]), int(params[1]))  # type: ignore[no-untyped-call]
            elif len(params) == 1:
                return NUMBER(int(params[0]), 0)  # type: ignore[no-untyped-call]
            else:
                return NUMBER()  # type: ignore[no-untyped-call]
        elif oracle_type_str.startswith("VARCHAR2"):
            # Extract length from VARCHAR2(255 CHAR) format
            if "(" in oracle_type_str:
                length_part = oracle_type_str.split("(")[1].split(")")[0]
                length = int(length_part.split()[0])  # Get number before CHAR
                return VARCHAR2(length)
            return VARCHAR2(255)
        elif oracle_type_str.startswith("TIMESTAMP"):
            return TIMESTAMP(timezone=False)
        elif oracle_type_str == "DATE":
            return DATE()
        elif oracle_type_str == "CLOB":
            return CLOB()
        else:
            # Default to VARCHAR2 with configured default length
            default_length = self.config.get("varchar_default_length", 255)
            return VARCHAR2(default_length)

    def _generate_oracle_ddl(self) -> Any:
        """Generate Oracle DDL with CORRECT field order following table_creator.py."""
        schema_name, table_name = self._parse_full_table_name(self.full_table_name)
        schema_properties = self.schema.get("properties", {})

        # STEP 1: Organize columns in CORRECT ORDER (like table_creator.py)
        columns: list[str] = []
        primary_key_field = None

        # 1.1 Find primary key field (prioritize simple 'id' over complex ones)
        id_fields = [
            name
            for name in schema_properties
            if (
                name.upper() == "ID"
                or (
                    name.upper().endswith("_ID") and not name.upper().endswith("_ID_ID")
                )
            )
        ]

        if id_fields:
            if "id" in [f.lower() for f in id_fields]:
                primary_key_field = next(f for f in id_fields if f.lower() == "id")
            else:
                primary_key_field = id_fields[0]

        # 1.2 Add PRIMARY KEY first
        if primary_key_field:
            oracle_type = self._convert_to_oracle_type(
                primary_key_field, schema_properties[primary_key_field], {}
            )
            columns.append(
                f'    "{primary_key_field.upper()}" {oracle_type} NOT NULL ENABLE'
            )

        # 1.3 Add OTHER FIELDS (sorted, excluding URLs and complex nested objects)
        other_fields = []
        for prop_name in sorted(schema_properties.keys()):
            # Skip URLs and system fields
            prop_upper = prop_name.upper()
            if (
                prop_name != primary_key_field
                and prop_upper != "URL"
                and not prop_upper.endswith("_URL")
                and not prop_upper.endswith("_ID_ID")
                and not prop_upper.endswith("_ID_KEY")
                and not prop_upper.endswith("_ID_URL")
                and prop_upper
                not in ["TK_DATE", "CREATE_USER", "CREATE_TS", "MOD_USER", "MOD_TS"]
            ):
                other_fields.append(prop_name)

        for prop_name in other_fields:
            oracle_type = self._convert_to_oracle_type(
                prop_name, schema_properties[prop_name], {}
            )
            # Add collation for VARCHAR2 types
            collation = ' COLLATE "USING_NLS_COMP"' if "VARCHAR2" in oracle_type else ""
            columns.append(f'    "{prop_name.upper()}" {oracle_type}{collation}')

        # 1.4 Add COMPLEX FOREIGN KEY fields (_ID_KEY, _ID_URL, etc.)
        fk_fields = [
            name
            for name in schema_properties
            if "_ID_" in name.upper() and not name.upper().endswith("_URL")
        ]
        for prop_name in sorted(fk_fields):
            if not prop_name.upper().endswith("_URL"):
                oracle_type = self._convert_to_oracle_type(
                    prop_name, schema_properties[prop_name], {}
                )
                collation = (
                    ' COLLATE "USING_NLS_COMP"' if "VARCHAR2" in oracle_type else ""
                )
                columns.append(f'    "{prop_name.upper()}" {oracle_type}{collation}')

        # 1.5 Add MANDATORY AUDIT FIELDS at the end
        audit_fields = [
            ("CREATE_USER", "VARCHAR2(255 CHAR)", ""),
            ("CREATE_TS", "TIMESTAMP (6)", ""),
            ("MOD_USER", "VARCHAR2(255 CHAR)", ""),
            ("MOD_TS", "TIMESTAMP (6)", " NOT NULL ENABLE"),
        ]

        for field_name, field_type, constraints in audit_fields:
            collation = ' COLLATE "USING_NLS_COMP"' if "VARCHAR2" in field_type else ""
            columns.append(f'    "{field_name}" {field_type}{collation}{constraints}')

        # 1.6 Add TK_DATE field (ALWAYS, not conditional)
        columns.append(
            '    "TK_DATE" TIMESTAMP (6) DEFAULT CURRENT_TIMESTAMP NOT NULL ENABLE'
        )

        # STEP 2: Create PRIMARY KEY constraint with MOD_TS
        pk_constraint = ""
        if primary_key_field:
            pk_name = f"PK_{table_name.upper()}"
            pk_cols = f'"{primary_key_field.upper()}", "MOD_TS"'
            pk_constraint = f',\n    CONSTRAINT "{pk_name}" PRIMARY KEY ({pk_cols})'

        # STEP 3: Build full DDL
        if schema_name:
            full_table_name = f'"{schema_name.upper()}"."{table_name.upper()}"'
        else:
            full_table_name = f'"{table_name.upper()}"'

        # columns_sql = ",\n".join(columns)  # Not used

        # Build DDL line by line to avoid any formatting issues
        ddl_lines = [
            "-- Oracle table created with unified rules from table_creator.py",
            f"-- Generated for stream: {self.stream_name}",
            "-- CORRECT field order: PK -> fields -> audit -> TK_DATE",
            f"DROP TABLE {full_table_name} CASCADE CONSTRAINTS;",
            "",
            f"CREATE TABLE {full_table_name}",
            "  (",
        ]

        # Add column definitions
        for i, col in enumerate(columns):
            if i == len(columns) - 1:
                # Last column: add comma only if there's a PK constraint coming
                if pk_constraint:
                    ddl_lines.append(f"    {col},")
                else:
                    ddl_lines.append(f"    {col}")
            else:
                # Not last column: always add comma
                ddl_lines.append(f"    {col},")

        # Add primary key constraint if present
        if pk_constraint:
            constraint_clean = pk_constraint.strip().lstrip(",").strip()
            ddl_lines.append(f"    {constraint_clean}")

        # Close table definition
        ddl_lines.extend([" );", ""])

        # Join lines and ensure clean formatting
        ddl = "\n".join(ddl_lines).strip()

        return ddl

    def _get_type_mapping_rules(self) -> dict[str, Any]:
        """Get type mapping rules from configuration or intelligent defaults.

        This method provides a professional type mapping system that:
        1. Allows custom rules via configuration
        2. Provides intelligent built-in defaults
        3. Supports extensibility without code changes
        """
        # Check for custom rules in configuration
        if "custom_type_rules" in self.config:
            return self.config["custom_type_rules"]

        # Use intelligent built-in rules
        return self._get_intelligent_type_mapping_rules()

    def _get_intelligent_type_mapping_rules(self) -> dict[str, Any]:
        """Get intelligent type mapping rules for Oracle.

        These rules are based on common database naming conventions
        and provide optimal Oracle types for various data patterns.
        """
        return {
            "FIELD_PATTERNS_TO_ORACLE": {
                "id_patterns": "NUMBER",
                "key_patterns": "VARCHAR2(255 CHAR)",
                "qty_patterns": "NUMBER",
                "price_patterns": "NUMBER",
                "weight_patterns": "NUMBER",
                "date_patterns": "TIMESTAMP(6)",
                "flag_patterns": "NUMBER(1,0)",
                "desc_patterns": "VARCHAR2(500 CHAR)",
                "code_patterns": "VARCHAR2(50 CHAR)",
                "name_patterns": "VARCHAR2(255 CHAR)",
                "addr_patterns": "VARCHAR2(500 CHAR)",
                "decimal_patterns": "NUMBER",
                "set_patterns": "VARCHAR2(4000 CHAR)",
            },
            "FIELD_PATTERN_RULES": {
                "id_patterns": ["*_id", "id"],
                "key_patterns": ["*_key"],
                "qty_patterns": [
                    "*_qty",
                    "*_quantity",
                    "*_count",
                    "*_amount",
                    "*_number",
                    "*_total",
                ],
                "price_patterns": [
                    "*_price",
                    "*_cost",
                    "*_rate",
                    "*_percent",
                    "*_value",
                    "*_amount",
                    "price",
                    "cost",
                    "rate",
                ],
                "weight_patterns": [
                    "*_weight",
                    "*_volume",
                    "*_length",
                    "*_width",
                    "*_height",
                ],
                "date_patterns": [
                    "*_date",
                    "*_time",
                    "*_ts",
                    "*_timestamp",
                    "*_datetime",
                    "*_at",
                    "created_*",
                    "updated_*",
                    "modified_*",
                ],
                "flag_patterns": ["*_flg", "*_flag", "*_enabled", "*_active"],
                "desc_patterns": ["*_desc", "*_description", "*_note", "*_comment"],
                "code_patterns": ["*_code", "*_status", "*_type"],
                "name_patterns": ["*_name", "*_title"],
                "addr_patterns": ["*_addr", "*_address"],
                "decimal_patterns": [
                    "*_decimal",
                    "*_numeric",
                    "*_float",
                    "*_double",
                    "*_real",
                ],
                "set_patterns": ["*_set"],
            },
        }

    def _convert_to_oracle_type(
        self, column_name: str, column_schema: dict[str, Any], rules: dict[str, Any]
    ) -> Any:
        """Convert column to Oracle type using intelligent mapping rules.

        This method implements a professional type mapping system that:
        1. Respects explicit type hints in schema
        2. Uses pattern matching for common naming conventions
        3. Falls back to JSON schema type mapping
        """
        # Priority 1: Check for explicit Oracle type hint in schema
        if "sql_type" in column_schema or "oracle_type" in column_schema:
            return column_schema.get("oracle_type", column_schema.get("sql_type"))

        # Priority 2: Apply intelligent pattern-based mapping
        pattern_type = self._apply_pattern_based_mapping(
            column_name, column_schema, rules
        )
        if pattern_type:
            return pattern_type

        # Priority 3: Use JSON schema type mapping
        return self._map_json_schema_to_oracle_type(column_schema)

    def _apply_pattern_based_mapping(
        self, column_name: str, _column_schema: dict[str, Any], rules: dict[str, Any]
    ) -> str | None:
        """Apply pattern-based type mapping using intelligent rules.

        Returns None if no pattern matches, allowing fallback to other methods.
        """
        column_lower = column_name.lower()

        # Priority 1: Field name patterns (same logic as table_creator.py)
        field_patterns = rules["FIELD_PATTERNS_TO_ORACLE"]
        field_rules = rules["FIELD_PATTERN_RULES"]

        for pattern_key, patterns in field_rules.items():
            for pattern in patterns:
                # Handle wildcard patterns
                if "*" in pattern:
                    pattern_clean = pattern.replace("*", "")
                    if (
                        pattern.startswith("*_")
                        and column_lower.endswith(pattern_clean)
                    ) or (
                        pattern.endswith("_*")
                        and column_lower.startswith(pattern_clean)
                    ):
                        oracle_type = field_patterns[pattern_key]
                        # Force 4000 CHAR for _set fields regardless of max_length
                        if pattern_key == "set_patterns":
                            return "VARCHAR2(4000 CHAR)"
                        return oracle_type
                # Exact match
                elif pattern == column_lower:
                    oracle_type = field_patterns[pattern_key]
                    # Force 4000 CHAR for _set fields regardless of max_length
                    if pattern_key == "set_patterns":
                        return "VARCHAR2(4000 CHAR)"
                    return oracle_type

        # No pattern matched
        return None

    def _map_json_schema_to_oracle_type(self, column_schema: dict[str, Any]) -> str:
        """Map JSON schema types to Oracle types.

        This provides intelligent default mappings for standard JSON schema types.
        """
        # Extract base type from schema
        schema_type = column_schema.get("type", "string")
        if isinstance(schema_type, list):
            # Handle nullable types like ["string", "null"]
            schema_type = next((t for t in schema_type if t != "null"), "string")

        # Integer types
        if schema_type == "integer":
            # Check for specific integer constraints
            if "minimum" in column_schema and column_schema["minimum"] >= 0:
                # Unsigned integer
                max_val = column_schema.get("maximum", 999999999999)
                if max_val <= 999:
                    return "NUMBER(3,0)"
                elif max_val <= 999999:
                    return "NUMBER(6,0)"
                elif max_val <= 999999999:
                    return "NUMBER(9,0)"
            return "NUMBER"

        # Number/float types
        elif schema_type == "number":
            # Check for decimal places
            if "multipleOf" in column_schema:
                # Determine precision from multipleOf
                multiple = str(column_schema["multipleOf"])
                if "." in multiple:
                    scale = len(multiple.split(".")[1])
                    return f"NUMBER(38,{min(scale, 10)})"
            return "NUMBER"

        # Boolean type
        elif schema_type == "boolean":
            return "NUMBER(1,0)"

        # String types
        elif schema_type == "string":
            # Check for date/time formats
            format_type = column_schema.get("format")
            if format_type in ["date-time", "datetime"]:
                return "TIMESTAMP(6)"
            elif format_type == "date":
                return "DATE"
            elif format_type == "time":
                return "TIMESTAMP(6)"

            # Check for enum constraints (use appropriate size)
            if "enum" in column_schema:
                max_enum_length = max(len(str(e)) for e in column_schema["enum"])
                return f"VARCHAR2({min(max_enum_length * 2, 4000)} CHAR)"

            # Use maxLength if specified
            max_length = column_schema.get("maxLength")
            if max_length:
                return f"VARCHAR2({min(max_length, 4000)} CHAR)"

            # Check for content hints
            if (
                "contentEncoding" in column_schema
                and column_schema["contentEncoding"] == "base64"
            ):
                return "CLOB"  # Base64 data can be large

            # Default string size based on config
            default_size = self.config.get("varchar_default_length", 255)
            return f"VARCHAR2({default_size} CHAR)"

        # Array and object types
        elif schema_type in ["array", "object"]:
            # Use CLOB for complex types
            return "CLOB"

        # Default fallback
        return "VARCHAR2(255 CHAR)"

    def _ensure_metadata_columns(self, conn: Any) -> None:
        """Ensure Singer metadata columns have correct types.

        This method ensures that standard Singer metadata columns
        are properly typed for Oracle.
        """
        # Get table parts
        schema_name, table_name = self._parse_full_table_name(self.full_table_name)

        # Define standard Singer metadata columns with optimal Oracle types
        metadata_columns = [
            ("_sdc_extracted_at", "TIMESTAMP(6)"),
            ("_sdc_received_at", "TIMESTAMP(6)"),
            ("_sdc_batched_at", "TIMESTAMP(6)"),
            ("_sdc_deleted_at", "TIMESTAMP(6)"),
            ("_sdc_sequence", "NUMBER"),
            ("_sdc_table_version", "NUMBER"),
            ("_sdc_sync_started_at", "TIMESTAMP(6)"),
        ]

        # Only process if metadata columns are enabled
        if not self.config.get("add_record_metadata", True):
            return

        # Try to alter columns - some may not exist yet
        for col_name, oracle_type in metadata_columns:
            try:
                if schema_name:
                    full_name = f'"{schema_name}"."{table_name}"'
                else:
                    full_name = f'"{table_name}"'

                # Check if column exists first
                check_sql = f"""
                    SELECT COUNT(*) FROM user_tab_columns
                    WHERE table_name = '{table_name.upper()}'
                    AND column_name = '{col_name.upper()}'
                """
                result = conn.execute(sqlalchemy.text(check_sql)).scalar()

                if result > 0:
                    # Column exists, try to modify it
                    alter_sql = (
                        f'ALTER TABLE {full_name} MODIFY ("{col_name}" {oracle_type})'
                    )
                    conn.execute(sqlalchemy.text(alter_sql))
                else:
                    # Column doesn't exist, add it
                    add_sql = (
                        f'ALTER TABLE {full_name} ADD ("{col_name}" {oracle_type})'
                    )
                    conn.execute(sqlalchemy.text(add_sql))

            except Exception as e:
                # DO NOT MASK CRITICAL DDL ERRORS
                self.logger.error(
                    f"CRITICAL: Column modification FAILED for {col_name}: {e}"
                )
                raise RuntimeError(
                    f"Column modification failed for {col_name}: {e}"
                ) from e

    def _parse_full_table_name(self, full_name: str) -> tuple[str | None, str]:
        """Parse schema.table into schema and table parts."""
        if "." in full_name:
            parts = full_name.split(".")
            schema = parts[0].strip('"')
            table = parts[1].strip('"')
            return schema, table
        else:
            return None, full_name.strip('"')

    def _get_oracle_column(self, name: str, json_schema: dict[str, Any]) -> Column[Any]:
        """Convert JSON schema property to Oracle column."""
        json_type = json_schema.get("type", "string")

        if json_type == "integer" or json_type == "number":
            return Column(
                name, NUMBER(), nullable=True  # type: ignore[no-untyped-call]
            )
        elif json_type == "boolean":
            return Column(
                name, NUMBER(1), nullable=True  # type: ignore[no-untyped-call]
            )
        elif json_type == "string":
            # Check for format hints
            format_type = json_schema.get("format")
            if format_type in ("date-time", "date", "time"):
                return Column(name, TIMESTAMP(), nullable=True)
            else:
                max_length = json_schema.get("maxLength", 4000)
                if max_length > 4000:
                    return Column(name, CLOB(), nullable=True)
                else:
                    return Column(name, VARCHAR2(max_length), nullable=True)
        elif json_type in ("object", "array"):
            return Column(name, CLOB(), nullable=True)
        else:
            # Default to VARCHAR2
            return Column(name, VARCHAR2(4000), nullable=True)

    def _apply_oracle_optimizations(self) -> None:
        """Apply maximum Oracle performance optimizations."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name
            optimizations = []

            # Check if we're on Enterprise Edition
            is_ee = self.config.get("oracle_is_enterprise_edition", False)

            # Advanced compression for WAN efficiency
            if self.config.get("enable_compression"):
                compression = self.config.get("compression_type", "ADVANCED").upper()
                compress_for = self.config.get("compress_for", "OLTP")

                # Only use advanced compression if licensed
                if compression != "BASIC" and not self.config.get(
                    "oracle_has_compression_option"
                ):
                    self.logger.warning(
                        f"Compression type {compression} requires Oracle "
                        f"Advanced Compression option. Using BASIC instead."
                    )
                    compression = "BASIC"
                    compress_for = "OLTP"

                optimizations.append(
                    f"ALTER TABLE {table_name} COMPRESS FOR "
                    f"{compress_for} {compression}"
                )

            # Maximum parallelism (requires EE)
            if self.config.get("parallel_degree", 1) > 1:
                if not is_ee:
                    self.logger.warning(
                        "Parallel degree > 1 requires Oracle Enterprise "
                        "Edition. Skipping."
                    )
                else:
                    degree = self.config["parallel_degree"]
                    optimizations.append(f"ALTER TABLE {table_name} PARALLEL {degree}")

            # Direct path operations
            if self.config.get("use_direct_path"):
                optimizations.append(f"ALTER TABLE {table_name} NOLOGGING")

            # In-Memory column store for ultra-fast access
            if self.config.get("use_inmemory"):
                if not self.config.get("oracle_has_inmemory_option"):
                    self.logger.warning(
                        "In-Memory feature requires Oracle In-Memory option. Skipping."
                    )
                else:
                    priority = self.config.get("inmemory_priority", "HIGH")
                    distribute = self.config.get("inmemory_distribute", "AUTO")
                    duplicate = self.config.get("inmemory_duplicate", "NO DUPLICATE")
                    optimizations.append(
                        f"ALTER TABLE {table_name} INMEMORY PRIORITY {priority} "
                        f"DISTRIBUTE {distribute} {duplicate}"
                    )

            # Result cache for read-heavy workloads
            if self.config.get("use_result_cache"):
                optimizations.append(
                    f"ALTER TABLE {table_name} RESULT_CACHE (MODE FORCE)"
                )

            # Execute all optimizations - REPORT ALL ERRORS
            for opt in optimizations:
                try:
                    conn.execute(sqlalchemy.text(opt))
                    self.logger.info(f"Applied Oracle optimization: {opt}")
                except Exception as e:
                    # DO NOT MASK ERRORS - Log them clearly
                    self.logger.error(f"Oracle optimization FAILED: {opt} - Error: {e}")
                    raise RuntimeError(f"Oracle optimization failed: {opt}") from e

            # Create high-performance indexes
            if self.key_properties and self.config.get("create_table_indexes"):
                self._create_performance_indexes(conn, table_name)

    def _create_performance_indexes(self, conn: Any, table_name: str) -> None:
        """Create indexes with maximum performance options."""
        for i, key in enumerate(self.key_properties):
            idx_name = f"IDX_{table_name.split('.')[-1]}_{i}"[:30]

            # Build index with performance options
            idx_opts = []
            if self.config.get("index_compression"):
                idx_opts.append("COMPRESS ADVANCED LOW")
            if self.config.get("parallel_degree", 1) > 1:
                idx_opts.append(f"PARALLEL {self.config['parallel_degree']}")
            if self.config.get("index_logging") is False:
                idx_opts.append("NOLOGGING")

            idx_clause = " ".join(idx_opts)

            try:
                conn.execute(
                    sqlalchemy.text(
                        f"CREATE INDEX {idx_name} ON {table_name} ({key}) {idx_clause}"
                    )
                )
                self.logger.info(f"Created index: {idx_name}")
            except Exception as e:
                # Check for expected errors vs real problems
                error_msg = str(e)
                if "ORA-00955" in error_msg:  # Name already used - acceptable
                    self.logger.info(f"Index {idx_name} already exists - skipping")
                elif (
                    "ORA-00942" in error_msg
                ):  # Table doesn't exist - acceptable during setup
                    self.logger.info(f"Table not ready for index {idx_name} - skipping")
                else:
                    # Real error - DO NOT MASK
                    self.logger.error(f"Index creation FAILED: {idx_name} - Error: {e}")
                    raise RuntimeError(f"Index creation failed: {idx_name}: {e}") from e

    def set_logger(self, logger: Any) -> None:
        """Set logger for sink operations."""
        self._logger = logger

    def set_monitor(self, monitor: Any) -> None:
        """Set monitor for sink operations."""
        self._monitor = monitor
        # Pass engine to monitor for database metrics
        try:
            if hasattr(self.connector, "_engine") and self.connector._engine:
                monitor.set_engine(self.connector._engine)
        except Exception as e:
            # Engine may not be available yet - log warning but continue
            if self.logger:
                self.logger.warning(
                    f"Monitor engine setup failed (will retry later): {e}"
                )
            else:
                print(f"WARNING: Monitor engine setup failed (will retry later): {e}")

    def process_batch(self, context: dict[str, Any]) -> None:
        """Process batch with comprehensive Oracle insertion tracking and statistics."""
        import time

        batch_start_time = time.time()

        records = context.get("records", [])
        if not records:
            if self._logger:
                self._logger.warning(
                    f"⚠️ EMPTY BATCH for stream {self.stream_name} - No records"
                )
            return

        # Update statistics - records received
        self._stream_stats["total_records_received"] = int(
            self._stream_stats["total_records_received"]
        ) + len(records)
        self._stream_stats["total_batches_processed"] = (
            int(self._stream_stats["total_batches_processed"]) + 1
        )

        # Track batch size statistics
        batch_size = len(records)
        if batch_size > int(self._stream_stats["largest_batch_size"]):
            self._stream_stats["largest_batch_size"] = batch_size
        smallest_batch = self._stream_stats["smallest_batch_size"]
        if isinstance(smallest_batch, (int, float)) and batch_size < smallest_batch:
            self._stream_stats["smallest_batch_size"] = batch_size

        # Track timing
        if self._stream_stats["first_batch_time"] is None:
            self._stream_stats["first_batch_time"] = batch_start_time
        self._stream_stats["last_batch_time"] = batch_start_time

        # Detailed batch analysis with enhanced statistics
        if self._logger:
            self._logger.info(
                f"📦 BATCH #{self._stream_stats['total_batches_processed']} STARTING",
                extra={
                    "stream_name": self.stream_name,
                    "batch_number": self._stream_stats["total_batches_processed"],
                    "batch_size": batch_size,
                    "cumulative_records": self._stream_stats["total_records_received"],
                    "load_method": self.config.get("load_method", "append-only"),
                    "table_name": self.full_table_name,
                    "key_properties": self.key_properties,
                    "first_record_keys": list(records[0].keys()) if records else [],
                    "sample_record_preview": (
                        {k: str(v)[:50] for k, v in list(records[0].items())[:5]}
                        if records
                        else {}
                    ),
                    "avg_batch_size": (
                        self._stream_stats["total_records_received"]
                        / self._stream_stats["total_batches_processed"]
                    ),
                    "largest_batch": self._stream_stats["largest_batch_size"],
                    "smallest_batch": (
                        self._stream_stats["smallest_batch_size"]
                        if self._stream_stats["smallest_batch_size"] != float("inf")
                        else batch_size
                    ),
                },
            )

            # Log batch processing
            self._logger.log_record_batch(
                stream=self.stream_name,
                batch_size=len(records),
                operation=self.config.get("load_method", "append-only"),
            )

        # Use operation context for monitoring if available
        operation_context = None
        if self._logger:
            operation_context = self._logger.operation_context(
                "process_batch",
                stream=self.stream_name,
                batch_size=len(records),
                load_method=self.config.get("load_method", "append-only"),
            )

        try:
            if operation_context:
                with operation_context:
                    self._process_batch_internal(records)
            else:
                self._process_batch_internal(records)

            # Mark successful processing
            self._stream_stats["successful_operations"] = (
                int(self._stream_stats["successful_operations"]) + 1
            )
            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time
            self._stream_stats["total_processing_time"] = (
                float(self._stream_stats["total_processing_time"]) + batch_duration
            )

            # Log successful batch completion with performance metrics
            if self._logger:
                avg_processing_time = float(
                    self._stream_stats["total_processing_time"]
                ) / int(self._stream_stats["successful_operations"])
                records_per_second = (
                    batch_size / batch_duration if batch_duration > 0 else 0
                )

                self._logger.info(
                    (
                        f"✅ ORACLE SINK - BATCH "
                        f"#{self._stream_stats['total_batches_processed']} COMPLETED"
                    ),
                    extra={
                        "stream_name": self.stream_name,
                        "batch_number": self._stream_stats["total_batches_processed"],
                        "batch_size": batch_size,
                        "processing_time_seconds": round(batch_duration, 3),
                        "records_per_second": round(records_per_second, 2),
                        "avg_processing_time": round(avg_processing_time, 3),
                        "total_records_processed": self._stream_stats[
                            "total_records_received"
                        ],
                        "successful_batches": self._stream_stats[
                            "successful_operations"
                        ],
                        "failed_batches": len(self._stream_stats["failed_batches"]),
                        "total_inserts": self._stream_stats["database_operations"][
                            "inserts"
                        ],
                        "total_updates": self._stream_stats["database_operations"][
                            "updates"
                        ],
                        "total_rows_affected": self._stream_stats[
                            "database_operations"
                        ]["rows_affected"],
                    },
                )

        except Exception as e:
            # Track failed batch
            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time

            failure_info = {
                "batch_number": self._stream_stats["total_batches_processed"],
                "batch_size": batch_size,
                "error": str(e),
                "processing_time": batch_duration,
                "timestamp": batch_start_time,
            }
            failed_batches = list(self._stream_stats["failed_batches"])
            failed_batches.append(failure_info)
            self._stream_stats["failed_batches"] = failed_batches
            self._stream_stats["total_records_failed"] = (
                int(self._stream_stats["total_records_failed"]) + batch_size
            )

            if self._logger:
                self._logger.error(
                    (
                        f"❌ ORACLE SINK - BATCH "
                        f"#{self._stream_stats['total_batches_processed']} FAILED"
                    ),
                    extra={
                        "stream": self.stream_name,
                        "batch_number": self._stream_stats["total_batches_processed"],
                        "batch_size": batch_size,
                        "error": str(e),
                        "processing_time_seconds": round(batch_duration, 3),
                        "total_failed_records": self._stream_stats[
                            "total_records_failed"
                        ],
                        "total_failed_batches": len(
                            self._stream_stats["failed_batches"]
                        ),
                        "failure_rate": round(
                            (
                                self._stream_stats["total_records_failed"]
                                / self._stream_stats["total_records_received"]
                            )
                            * 100,
                            2,
                        ),
                    },
                    exc_info=True,
                )
            raise

    def _process_batch_internal(self, records: list[dict[str, Any]]) -> None:
        """Internal batch processing logic with detailed SQL execution tracking."""
        # LAZY CONNECTION: Ensure Oracle connection exists before processing
        self._ensure_connection_and_table()

        if self._logger:
            self._logger.info(
                "🔧 INTERNAL BATCH PROCESSING",
                extra={
                    "stream_name": self.stream_name,
                    "records_count": len(records),
                    "load_method": self.config.get("load_method", "append-only"),
                    "has_key_properties": bool(self.key_properties),
                    "key_properties": self.key_properties,
                    "connection_established": self._connection_established,
                },
            )

        # Check load method
        load_method = self.config.get("load_method", "append-only")

        # Handle overwrite mode - truncate before insert
        if load_method == "overwrite" and not hasattr(self, "_overwrite_done"):
            if self._logger:
                self._logger.info(
                    f"🗑️ OVERWRITE MODE - Truncating table " f"{self.full_table_name}"
                )
            try:
                with self.connector._engine.connect() as conn:
                    # Check if table exists and get correct name
                    schema_name = self.config.get(
                        "default_target_schema", self.config.get("schema", "")
                    )
                    table_base_name = self.stream_name.upper()

                    # Try to find the table - it might be with or without prefix
                    check_sql = f"""
                    SELECT table_name
                    FROM all_tables
                    WHERE owner = '{schema_name.upper()}'
                    AND (table_name = '{table_base_name}' OR
                         table_name = 'WMS_{table_base_name}')
                    """
                    result = conn.execute(sqlalchemy.text(check_sql)).fetchone()

                    if result:
                        actual_table_name = result[0]
                        truncate_sql = (
                            f'TRUNCATE TABLE "{schema_name.upper()}"'
                            f'."{actual_table_name}"'
                        )
                        if self._logger:
                            self._logger.info(
                                f"Truncating existing table: {truncate_sql}"
                            )
                        conn.execute(sqlalchemy.text(truncate_sql))
                        conn.commit()
                    else:
                        # Table doesn't exist yet, will be created by Singer SDK
                        if self._logger:
                            self._logger.info(
                                f"Table doesn't exist yet, will be created: "
                                f"{self.full_table_name}"
                            )
                self._overwrite_done = True
                if self._logger:
                    self._logger.info(
                        f"✅ Table {self.full_table_name} truncated successfully"
                    )
            except Exception as e:
                if self._logger:
                    self._logger.error(f"❌ Failed to truncate table: {e}")
                raise

        # Check if this is an upsert scenario
        if load_method == "upsert" and self.key_properties and len(records) > 0:
            if self._logger:
                self._logger.info(
                    f"🔄 USING UPSERT MODE for {self.stream_name}",
                    extra={"key_properties": self.key_properties},
                )
            self._process_batch_upsert(records)
        else:
            # Use Singer SDK's standard batch processing for append-only and overwrite
            if self._logger:
                self._logger.info(
                    f"➕ USING {load_method.upper()} MODE for {self.stream_name}"
                )
            context = {"records": records}
            super().process_batch(context)

    def _process_batch_upsert(self, records: list[dict[str, Any]]) -> None:
        """Process batch using Oracle MERGE for upsert operations."""
        if not self.key_properties:
            raise ValueError("Upsert requires key_properties to be defined")

        # Build MERGE statement
        merge_sql = self._build_oracle_merge_statement()

        # Conform records
        prepared_records = [self._conform_record(record) for record in records]

        # Execute MERGE in batches
        batch_size = self.config.get("merge_batch_size", 1000)

        with self.connector._engine.connect() as conn, conn.begin():
            for i in range(0, len(prepared_records), batch_size):
                batch = prepared_records[i : i + batch_size]
                for record in batch:
                    conn.execute(sqlalchemy.text(merge_sql), record)

    def _build_oracle_merge_statement(self) -> Any:
        """Build Oracle-specific MERGE statement."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())
        key_columns = self.key_properties or []

        # Add Singer metadata columns that may exist
        metadata_columns = [
            "_sdc_extracted_at",
            "_sdc_received_at",
            "_sdc_batched_at",
            "_sdc_deleted_at",
            "_sdc_sequence",
            "_sdc_table_version",
            "_sdc_sync_started_at",
        ]

        # Check which metadata columns actually exist in the table
        all_columns = columns + metadata_columns
        non_key_columns = [col for col in all_columns if col not in key_columns]

        # Build MERGE statement
        merge_sql = f"""
        MERGE INTO {table_name} target
        USING (
            SELECT {', '.join(f':{col} AS {col}' for col in all_columns)}
            FROM dual
        ) source
        ON ({' AND '.join(f'target.{col} = source.{col}' for col in key_columns)})
        """

        # Add UPDATE clause if there are non-key columns
        if non_key_columns:
            merge_sql += f"""
        WHEN MATCHED THEN
            UPDATE SET {', '.join(f'{col} = source.{col}' for col in non_key_columns)}
            """

        # Add INSERT clause
        merge_sql += f"""
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(all_columns)})
            VALUES ({', '.join(f'source.{col}' for col in all_columns)})
        """

        return merge_sql

    def _process_batch_parallel(self, records: list[dict[str, Any]]) -> None:
        """Process batch in parallel chunks for maximum throughput."""
        # Split into chunks
        chunks = []
        for i in range(0, len(records), self._chunk_size):
            chunks.append(records[i : i + self._chunk_size])

        # Process chunks in parallel
        futures = []
        if self._executor:
            for chunk in chunks:
                future = self._executor.submit(self._process_chunk, chunk)
                futures.append(future)

            # Wait for completion - DO NOT MASK PARALLEL PROCESSING ERRORS
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    # Log the specific chunk processing error
                    if self._logger:
                        self._logger.error(f"Parallel chunk processing failed: {e}")
                    # Always raise - parallel processing errors indicate serious issues
                    raise
        else:
            # Use async processing if available
            if self.config.get("enable_async", False):
                asyncio.run(self._process_chunks_async(chunks))
            else:
                # Fallback to sequential processing
                for chunk in chunks:
                    self._process_chunk(chunk)

    async def _process_chunks_async(self, chunks: list[list[dict[str, Any]]]) -> None:
        """Process chunks asynchronously with SQLAlchemy 2.x patterns."""
        tasks = []
        for chunk in chunks:
            if self.key_properties:
                task = self._execute_merge_batch_async(chunk)
            else:
                task = self._execute_insert_batch_async(chunk)
            tasks.append(task)

        await asyncio.gather(*tasks)

    def _process_chunk(self, records: list[dict[str, Any]]) -> None:
        """Process a single chunk of records."""
        if self.key_properties:
            self._execute_merge_batch(records)
        else:
            self._execute_insert_batch(records)

    def _process_batch_direct_path(self, records: list[dict[str, Any]]) -> None:
        """Process using Oracle direct path for maximum speed."""
        insert_sql = self._build_direct_path_insert()
        prepared = [self._conform_record(r) for r in records]

        with self.connector._engine.connect() as conn, conn.begin():
            conn.execute(sqlalchemy.text(insert_sql), prepared)

    def _process_batch_bulk_insert(self, records: list[dict[str, Any]]) -> None:
        """Process using optimized bulk insert."""
        self._execute_insert_batch(records)

    def _process_batch_with_merge(self, context: dict[str, Any]) -> None:
        """Process batch using high-performance Oracle MERGE."""
        records = context.get("records", [])
        if not records:
            return

        self._execute_merge_batch(records)

    async def _execute_insert_batch_async(self, records: list[dict[str, Any]]) -> None:
        """Execute async bulk insert with SQLAlchemy 2.x patterns."""
        if not self.connector._async_engine:
            # Fallback to sync processing
            return self._execute_insert_batch(records)

        async with self.connector.get_async_session() as session:
            # Use modern SQLAlchemy 2.x insert patterns
            stmt = insert(self._get_table_model())
            prepared_records = [self._conform_record(r) for r in records]

            await session.execute(stmt, prepared_records)
            await session.commit()

            # Update statistics
            self._stream_stats["total_records_inserted"] += len(prepared_records)

    def _execute_insert_batch(self, records: list[dict[str, Any]]) -> None:
        """Execute high-performance bulk insert with comprehensive tracking."""
        import time

        operation_start = time.time()

        if self._logger:
            self._logger.info(
                "💽 EXECUTING INSERT BATCH",
                extra={
                    "stream_name": self.stream_name,
                    "records_count": len(records),
                    "table_name": self.full_table_name,
                    "operation_type": "INSERT",
                },
            )

        insert_sql = self._build_bulk_insert_statement()
        prepared = [self._conform_record(r) for r in records]

        if self._logger:
            self._logger.info(
                "📝 SQL INSERT STATEMENT",
                extra={
                    "stream_name": self.stream_name,
                    "sql_statement": (
                        insert_sql[:500] + "..."
                        if len(insert_sql) > 500
                        else insert_sql
                    ),
                    "prepared_records_count": len(prepared),
                    "sample_prepared_record": prepared[0] if prepared else {},
                },
            )

        try:
            with self.connector._engine.connect() as conn, conn.begin():
                result = conn.execute(sqlalchemy.text(insert_sql), prepared)
                rows_affected = getattr(result, "rowcount", len(prepared))

                # Update statistics
                self._stream_stats["total_records_inserted"] = int(
                    self._stream_stats["total_records_inserted"]
                ) + len(prepared)
                db_ops = dict(self._stream_stats["database_operations"])
                db_ops["inserts"] = int(db_ops["inserts"]) + 1
                db_ops["rows_affected"] = int(db_ops["rows_affected"]) + rows_affected
                self._stream_stats["database_operations"] = db_ops

                operation_end = time.time()
                operation_duration = operation_end - operation_start

                # Verify actual insertion by querying the database
                verification_query = f"SELECT COUNT(*) FROM {self.full_table_name}"
                try:
                    count_result = conn.execute(sqlalchemy.text(verification_query))
                    total_rows_in_table = count_result.scalar()
                except Exception as verification_error:
                    # DO NOT SILENCE VERIFICATION ERRORS - Log them clearly
                    total_rows_in_table = "verification_failed"
                    if self._logger:
                        self._logger.error(
                            (
                                f"❌ VERIFICATION QUERY FAILED after INSERT: "
                                f"{verification_error}"
                            ),
                            extra={
                                "stream_name": self.stream_name,
                                "verification_query": verification_query,
                                "error_type": type(verification_error).__name__,
                                "error_details": str(verification_error),
                            },
                        )

                if self._logger:
                    self._logger.info(
                        "✅ INSERT OPERATION SUCCESSFUL",
                        extra={
                            "stream_name": self.stream_name,
                            "operation_type": "INSERT",
                            "records_sent": len(prepared),
                            "rows_affected": rows_affected,
                            "table_name": self.full_table_name,
                            "operation_duration": round(operation_duration, 3),
                            "records_per_second": round(
                                (
                                    len(prepared) / operation_duration
                                    if operation_duration > 0
                                    else 0
                                ),
                                2,
                            ),
                            "total_rows_in_table": total_rows_in_table,
                            "cumulative_inserts": self._stream_stats[
                                "total_records_inserted"
                            ],
                            "total_db_operations": self._stream_stats[
                                "database_operations"
                            ]["inserts"],
                            "total_rows_affected": self._stream_stats[
                                "database_operations"
                            ]["rows_affected"],
                        },
                    )

        except Exception as e:
            operation_end = time.time()
            operation_duration = operation_end - operation_start

            if self._logger:
                self._logger.error(
                    "❌ INSERT OPERATION FAILED",
                    extra={
                        "stream_name": self.stream_name,
                        "operation_type": "INSERT",
                        "error": str(e),
                        "sql_statement": (
                            insert_sql[:200] + "..."
                            if len(insert_sql) > 200
                            else insert_sql
                        ),
                        "records_attempted": len(prepared),
                        "operation_duration": round(operation_duration, 3),
                        "table_name": self.full_table_name,
                        "sample_record": prepared[0] if prepared else {},
                    },
                    exc_info=True,
                )
            raise

    async def _execute_merge_batch_async(self, records: list[dict[str, Any]]) -> None:
        """Execute async MERGE with modern SQLAlchemy 2.x patterns."""
        if not self.connector._async_engine:
            # Fallback to sync processing
            return self._execute_merge_batch(records)

        async with self.connector.get_async_session() as session:
            table_model = self._get_table_model()

            for record in records:
                conformed = self._conform_record(record)
                key_values = {
                    k: conformed[k] for k in self.key_properties if k in conformed
                }

                # Try to find existing record
                stmt = select(table_model).where(
                    *[getattr(table_model, k) == v for k, v in key_values.items()]
                )
                existing = await session.execute(stmt)
                row = existing.scalar_one_or_none()

                if row:
                    # Update existing record
                    update_stmt = update(table_model).where(
                        *[getattr(table_model, k) == v for k, v in key_values.items()]
                    ).values(**conformed)
                    await session.execute(update_stmt)
                    self._stream_stats["total_records_updated"] += 1
                else:
                    # Insert new record
                    insert_stmt = insert(table_model).values(**conformed)
                    await session.execute(insert_stmt)
                    self._stream_stats["total_records_inserted"] += 1

            await session.commit()

    def _get_table_model(self) -> type[OracleTargetTable]:
        """Get or create SQLAlchemy 2.x ORM model for this table."""
        # This would dynamically create a table model based on schema
        # For now, return the base class
        return OracleTargetTable

    def _execute_merge_batch(self, records: list[dict[str, Any]]) -> None:
        """Execute high-performance MERGE operation with comprehensive tracking."""
        import time

        operation_start = time.time()

        if self._logger:
            self._logger.info(
                "🔄 EXECUTING MERGE BATCH",
                extra={
                    "stream_name": self.stream_name,
                    "records_count": len(records),
                    "table_name": self.full_table_name,
                    "operation_type": "MERGE",
                },
            )

        merge_sql = self._build_merge_statement()
        prepared = [self._conform_record(r) for r in records]

        if self._logger:
            self._logger.info(
                "📝 SQL MERGE STATEMENT",
                extra={
                    "stream_name": self.stream_name,
                    "sql_statement": (
                        merge_sql[:500] + "..." if len(merge_sql) > 500 else merge_sql
                    ),
                    "prepared_records_count": len(prepared),
                },
            )

        try:
            with self.connector._engine.connect() as conn, conn.begin():
                # Get initial row count for comparison
                verification_query = f"SELECT COUNT(*) FROM {self.full_table_name}"
                try:
                    initial_count_result = conn.execute(
                        sqlalchemy.text(verification_query)
                    )
                    initial_row_count = initial_count_result.scalar()
                except Exception as initial_count_error:
                    # DO NOT SILENCE INITIAL COUNT ERRORS - Log them
                    initial_row_count = "count_failed"
                    if self._logger:
                        self._logger.error(
                            (
                                f"❌ INITIAL COUNT QUERY FAILED for MERGE: "
                                f"{initial_count_error}"
                            ),
                            extra={
                                "stream_name": self.stream_name,
                                "verification_query": verification_query,
                                "error_type": type(initial_count_error).__name__,
                                "error_details": str(initial_count_error),
                            },
                        )

                # Process in optimal batch sizes
                batch_size = self.config.get("merge_batch_size", 5000)
                total_affected = 0
                total_sub_batches = 0

                for i in range(0, len(prepared), batch_size):
                    batch = prepared[i : i + batch_size]
                    result = conn.execute(sqlalchemy.text(merge_sql), batch)
                    batch_affected = getattr(result, "rowcount", 0)
                    total_affected += batch_affected
                    total_sub_batches += 1

                    if self._logger:
                        self._logger.info(
                            "🔄 MERGE SUB-BATCH PROCESSED",
                            extra={
                                "stream_name": self.stream_name,
                                "sub_batch_number": (i // batch_size) + 1,
                                "sub_batch_size": len(batch),
                                "rows_affected": batch_affected,
                                "cumulative_affected": total_affected,
                            },
                        )

                # Get final row count
                try:
                    final_count_result = conn.execute(
                        sqlalchemy.text(verification_query)
                    )
                    final_row_count = final_count_result.scalar()
                    net_change = (
                        final_row_count - initial_row_count
                        if (
                            isinstance(initial_row_count, int)
                            and isinstance(final_row_count, int)
                        )
                        else "unknown"
                    )
                except Exception as final_count_error:
                    # DO NOT SILENCE FINAL COUNT ERRORS - Log them
                    final_row_count = "count_failed"
                    net_change = "count_failed"
                    if self._logger:
                        self._logger.error(
                            (
                                f"❌ FINAL COUNT QUERY FAILED for MERGE: "
                                f"{final_count_error}"
                            ),
                            extra={
                                "stream_name": self.stream_name,
                                "verification_query": verification_query,
                                "error_type": type(final_count_error).__name__,
                                "error_details": str(final_count_error),
                            },
                        )

                # Update statistics
                db_ops = dict(self._stream_stats["database_operations"])
                db_ops["merges"] = int(db_ops["merges"]) + 1
                db_ops["rows_affected"] = int(db_ops["rows_affected"]) + total_affected
                self._stream_stats["database_operations"] = db_ops

                # Estimate inserts vs updates (rough calculation)
                if isinstance(net_change, int) and net_change >= 0:
                    estimated_inserts = net_change
                    estimated_updates = len(prepared) - estimated_inserts
                    self._stream_stats["total_records_inserted"] = (
                        int(self._stream_stats["total_records_inserted"])
                        + estimated_inserts
                    )
                    self._stream_stats["total_records_updated"] = (
                        int(self._stream_stats["total_records_updated"])
                        + estimated_updates
                    )
                else:
                    # Fallback: assume all records were processed
                    self._stream_stats["total_records_updated"] = int(
                        self._stream_stats["total_records_updated"]
                    ) + len(prepared)

                operation_end = time.time()
                operation_duration = operation_end - operation_start

                if self._logger:
                    self._logger.info(
                        "✅ MERGE OPERATION SUCCESSFUL",
                        extra={
                            "stream_name": self.stream_name,
                            "operation_type": "MERGE",
                            "records_sent": len(prepared),
                            "total_rows_affected": total_affected,
                            "sub_batches_processed": total_sub_batches,
                            "table_name": self.full_table_name,
                            "operation_duration": round(operation_duration, 3),
                            "records_per_second": round(
                                (
                                    len(prepared) / operation_duration
                                    if operation_duration > 0
                                    else 0
                                ),
                                2,
                            ),
                            "initial_table_rows": initial_row_count,
                            "final_table_rows": final_row_count,
                            "net_row_change": net_change,
                            "estimated_inserts": (
                                net_change
                                if isinstance(net_change, int) and net_change >= 0
                                else "unknown"
                            ),
                            "estimated_updates": (
                                len(prepared) - net_change
                                if isinstance(net_change, int) and net_change >= 0
                                else "unknown"
                            ),
                            "cumulative_inserts": self._stream_stats[
                                "total_records_inserted"
                            ],
                            "cumulative_updates": self._stream_stats[
                                "total_records_updated"
                            ],
                            "total_db_operations": self._stream_stats[
                                "database_operations"
                            ]["merges"],
                            "total_rows_affected_cumulative": self._stream_stats[
                                "database_operations"
                            ]["rows_affected"],
                        },
                    )

        except Exception as e:
            operation_end = time.time()
            operation_duration = operation_end - operation_start

            if self._logger:
                self._logger.error(
                    "❌ MERGE OPERATION FAILED",
                    extra={
                        "stream_name": self.stream_name,
                        "operation_type": "MERGE",
                        "error": str(e),
                        "sql_statement": (
                            merge_sql[:200] + "..."
                            if len(merge_sql) > 200
                            else merge_sql
                        ),
                        "records_attempted": len(prepared),
                        "operation_duration": round(operation_duration, 3),
                        "table_name": self.full_table_name,
                        "sample_record": prepared[0] if prepared else {},
                    },
                    exc_info=True,
                )
            raise

    def _build_direct_path_insert(self) -> Any:
        """Build INSERT with APPEND_VALUES hint for direct path."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())

        # Don't add metadata columns here - Singer SDK handles this

        columns_str = ", ".join(columns)
        placeholders = ", ".join(f":{col}" for col in columns)

        # Direct path with parallel hint
        return f"""
        INSERT /*+ APPEND_VALUES "
        f"PARALLEL({table_name},{self.config.get('parallel_degree', 8)}) */
        INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        """

    def _build_bulk_insert_statement(self) -> Any:
        """Build optimized INSERT with performance hints."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())

        # Don't add metadata columns here - Singer SDK handles this

        columns_str = ", ".join(columns)
        placeholders = ", ".join(f":{col}" for col in columns)

        # Performance hints
        hints = []
        if self.config.get("use_parallel_dml"):
            hints.append(
                f"PARALLEL({table_name},{self.config.get('parallel_degree', 8)})"
            )
        if self.config.get("use_append_hint"):
            hints.append("APPEND")

        hint_str = f"/*+ {' '.join(hints)} */" if hints else ""

        return (
            f"INSERT {hint_str} INTO {table_name} ({columns_str}) "
            f"VALUES ({placeholders})"
        )

    def _build_merge_statement(self) -> Any:
        """Build high-performance MERGE with hints."""
        table_name = self.full_table_name
        columns = list(self.schema["properties"].keys())
        key_cols = self.key_properties or []

        # Performance hints
        hints = []
        if self.config.get("use_parallel_dml"):
            hints.append(
                f"PARALLEL({table_name},{self.config.get('parallel_degree', 8)})"
            )
        if self.config.get("use_merge_hint"):
            hints.append("USE_MERGE")

        hint_str = f"/*+ {' '.join(hints)} */" if hints else ""

        # Build columns
        all_cols = columns
        update_cols = [col for col in all_cols if col not in key_cols]

        # Build MERGE
        merge_sql = f"""
        MERGE {hint_str} INTO {table_name} target
        USING (
            SELECT {', '.join(f':{col} AS {col}' for col in all_cols)}
            FROM dual
        ) source
        ON ({' AND '.join(f'target.{col} = source.{col}' for col in key_cols)})
        """

        if update_cols:
            merge_sql += f"""
        WHEN MATCHED THEN
            UPDATE SET {', '.join(f'{col} = source.{col}' for col in update_cols)}
            """

        merge_sql += f"""
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(all_cols)})
            VALUES ({', '.join(f'source.{col}' for col in all_cols)})
        """

        return merge_sql

    def _singer_sdk_to_oracle_type(
        self, singer_type: dict[str, Any]
    ) -> sqlalchemy.types.TypeEngine[Any]:
        """Map Singer SDK types to Oracle types using SQLAlchemy."""
        type_str = singer_type.get("type", "string")

        # Handle type arrays
        if isinstance(type_str, list):
            type_str = next((t for t in type_str if t != "null"), "string")

        # Get format for date/time types
        format_str = singer_type.get("format", "")

        # Map to Oracle types
        if type_str == "string":
            max_length = singer_type.get(
                "maxLength", self.config.get("varchar_max_length", 4000)
            )
            if max_length > 4000:
                # Use CLOB for long strings
                return sqlalchemy.dialects.oracle.CLOB()
            elif self.config.get("use_nvarchar"):
                return sqlalchemy.dialects.oracle.NVARCHAR2(max_length)
            else:
                return sqlalchemy.dialects.oracle.VARCHAR2(max_length)

        elif type_str == "integer":
            return sqlalchemy.dialects.oracle.NUMBER(  # type: ignore[no-untyped-call]
                precision=self.config.get("number_precision", 38), scale=0
            )

        elif type_str == "number":
            return sqlalchemy.dialects.oracle.NUMBER(  # type: ignore[no-untyped-call]
                precision=self.config.get("number_precision", 38),
                scale=self.config.get("number_scale", 10),
            )

        elif type_str == "boolean":
            # Oracle doesn't have native boolean
            if self.config.get("supports_native_boolean"):
                return sqlalchemy.BOOLEAN()
            else:
                return sqlalchemy.dialects.oracle.NUMBER(
                    1, 0
                )  # type: ignore[no-untyped-call]

        elif type_str == "object" or type_str == "array":
            # Store JSON as CLOB or native JSON type
            json_type = self.config.get("json_column_type", "CLOB")
            if json_type == "JSON" and hasattr(sqlalchemy.dialects.oracle, "JSON"):
                return sqlalchemy.dialects.oracle.JSON()  # type: ignore[no-any-return]
            else:
                return sqlalchemy.dialects.oracle.CLOB()

        elif format_str == "date":
            return sqlalchemy.dialects.oracle.DATE()

        elif format_str == "time":
            return sqlalchemy.dialects.oracle.TIMESTAMP()

        elif format_str == "date-time" or type_str == "date-time":
            return sqlalchemy.dialects.oracle.TIMESTAMP(timezone=True)

        # Default to VARCHAR2
        return sqlalchemy.dialects.oracle.VARCHAR2(255)

    def activate_version(self, new_version: int) -> None:
        """Activate version using Singer SDK pattern."""
        # Let Singer SDK handle version activation
        super().activate_version(new_version)

    def clean_up(self) -> None:
        """Clean up with comprehensive final statistics reporting."""
        if self._logger:
            self._logger.info(f"🧹 Starting cleanup for stream {self.stream_name}")

        # Generate comprehensive final statistics report
        self._generate_final_statistics_report()

        try:
            # Gather advanced statistics
            if self.config.get("gather_statistics"):
                if self._logger:
                    self._logger.info("Gathering table statistics")

                with self.connector._engine.connect() as conn:
                    table_name = self.full_table_name.split(".")[-1]
                    conn.execute(
                        sqlalchemy.text(
                            f"""
                        BEGIN
                            DBMS_STATS.GATHER_TABLE_STATS(
                                ownname => USER,
                                tabname => '{table_name}',
                                estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
                                method_opt => 'FOR ALL COLUMNS SIZE AUTO',
                                granularity => 'ALL',
                                cascade => TRUE,
                                degree => {self.config.get(
                                    'parallel_degree', 'DBMS_STATS.DEFAULT_DEGREE'
                                )}"
                            );
                        END;
                    """
                        )
                    )

            # Rebuild indexes for optimal performance
            if self.config.get("rebuild_indexes_after_load"):
                if self._logger:
                    self._logger.info("Rebuilding indexes")
                self._rebuild_indexes()

            # Refresh materialized views if configured
            if self.config.get("refresh_mviews"):
                if self._logger:
                    self._logger.info("Refreshing materialized views")
                self._refresh_materialized_views()

            # Log Oracle performance metrics if available
            if self._logger and self._monitor:
                try:
                    oracle_metrics = {
                        "pool_size": getattr(
                            self.connector._engine.pool, "size", lambda: 0
                        )(),
                        "checked_out": getattr(
                            self.connector._engine.pool, "checkedout", lambda: 0
                        )(),
                        "overflow": getattr(
                            self.connector._engine.pool, "overflow", lambda: 0
                        )(),
                    }
                    self._logger.log_oracle_performance(oracle_metrics)
                except Exception as e:
                    self._logger.debug(f"Could not log Oracle metrics: {e}")

        except Exception as e:
            if self._logger:
                self._logger.error(f"Error during cleanup: {e}")
            raise
        finally:
            # Shutdown thread pool
            if self._executor:
                if self._logger:
                    self._logger.debug("Shutting down thread pool")
                self._executor.shutdown(wait=True)

        if self._logger:
            self._logger.info(f"Cleanup completed for stream {self.stream_name}")

        # Let Singer SDK handle cleanup
        super().clean_up()

    def _rebuild_indexes(self) -> None:
        """Rebuild indexes with parallel processing after bulk load."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name.split(".")[-1]

            # Get all indexes
            result = conn.execute(
                sqlalchemy.text(
                    f"""
                SELECT index_name FROM user_indexes
                WHERE table_name = '{table_name}' AND index_type != 'LOB'
            """
                )
            )

            for row in result:
                idx_name = row[0]
                try:
                    conn.execute(
                        sqlalchemy.text(
                            f"""
                        ALTER INDEX {idx_name} REBUILD
                        PARALLEL {self.config.get('parallel_degree', 8)}
                        NOLOGGING
                    """
                        )
                    )
                    if self._logger:
                        self._logger.info(f"Successfully rebuilt index: {idx_name}")
                except Exception as e:
                    # Log rebuild failures instead of silently suppressing
                    if self._logger:
                        self._logger.warning(
                            f"Index rebuild failed for {idx_name}: {e}"
                        )
                    # Don't raise - this is optimization, not critical

    def _refresh_materialized_views(self) -> None:
        """Refresh any materialized views on the table."""
        with self.connector._engine.connect() as conn:
            table_name = self.full_table_name
            try:
                conn.execute(
                    sqlalchemy.text(
                        f"""
                    BEGIN
                        DBMS_MVIEW.REFRESH_DEPENDENT(
                            number_of_failures => :failures,
                            list => '{table_name}',
                            method => 'C',
                            parallelism => {self.config.get('parallel_degree', 8)}
                        );
                    END;
                """
                    ),
                    {"failures": 0},
                )
                if self._logger:
                    self._logger.info(
                        f"Successfully refreshed materialized views for {table_name}"
                    )
            except Exception as e:
                # Log MView refresh failures instead of silently suppressing
                if self._logger:
                    self._logger.warning(
                        f"Materialized view refresh failed for {table_name}: {e}"
                    )
                # Don't raise - this is optimization, not critical

    def _conform_record(self, record: dict[str, Any]) -> dict[str, Any]:
        """Conform record to Oracle requirements using Singer SDK patterns."""
        conformed: dict[str, Any] = {}

        # Process each field according to schema
        for key, value in record.items():
            # Skip URL fields completely during record processing
            key_upper = key.upper()
            if (
                key_upper == "URL"
                or key_upper.endswith("_URL")
                or key_upper.endswith("_ID_URL")
                or key_upper.endswith("_ID_KEY")
                or key_upper.endswith("_ID_ID")
            ):
                # Skip URL and problematic fields completely
                continue
            if key in self.schema.get("properties", {}):
                prop_schema = self.schema["properties"][key]
                prop_type = prop_schema.get("type", "string")

                # Handle type arrays (nullable types)
                if isinstance(prop_type, list):
                    if value is None and "null" in prop_type:
                        conformed[key] = None
                        continue
                    prop_type = next((t for t in prop_type if t != "null"), "string")

                # Apply type-specific conversions
                if value is not None:
                    if prop_type == "boolean":
                        if self.config.get("supports_native_boolean"):
                            conformed[key] = value
                        else:
                            # Handle both string and integer boolean values
                            true_val = self.config.get("boolean_true_value", "1")
                            false_val = self.config.get("boolean_false_value", "0")
                            # Convert to int if the default values are being used
                            if true_val == "1" and false_val == "0":
                                conformed[key] = 1 if value else 0
                            else:
                                conformed[key] = true_val if value else false_val
                    elif prop_type in ("object", "array"):
                        # Serialize to JSON
                        conformed[key] = json.dumps(value)
                    else:
                        conformed[key] = value
                else:
                    conformed[key] = None
            else:
                # Pass through fields not in schema (except URL fields)
                conformed[key] = value

        # Don't add Singer metadata here - Singer SDK handles this automatically

        return conformed

    def conform_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Override schema conforming to filter out URL fields."""
        conformed_schema = schema.copy()

        # Filter URL fields from schema properties
        if "properties" in conformed_schema:
            filtered_properties = {}
            for prop_name, prop_schema in conformed_schema["properties"].items():
                prop_upper = prop_name.upper()
                # Skip URL fields completely from schema
                if not (
                    prop_upper == "URL"
                    or prop_upper.endswith("_URL")
                    or prop_upper.endswith("_ID_URL")
                    or prop_upper.endswith("_ID_KEY")
                    or prop_upper.endswith("_ID_ID")
                ):
                    filtered_properties[prop_name] = prop_schema

            conformed_schema["properties"] = filtered_properties

            # Log the filtering result
            original_count = len(schema.get("properties", {}))
            filtered_count = len(filtered_properties)
            if self.logger:
                self.logger.info(
                    f"🔍 SCHEMA FILTERED - Stream: {self.stream_name} - "
                    f"Original: {original_count} fields - "
                    f"Filtered: {filtered_count} fields - "
                    f"Removed: {original_count - filtered_count} URL fields"
                )

        return super().conform_schema(conformed_schema)

    def _generate_final_statistics_report(self) -> None:
        """Generate comprehensive final statistics report for the stream."""
        import time

        if not self._logger:
            return

        # Calculate final metrics
        total_duration = 0.0
        if (
            self._stream_stats["first_batch_time"]
            and self._stream_stats["last_batch_time"]
        ):
            total_duration = (
                self._stream_stats["last_batch_time"]
                - self._stream_stats["first_batch_time"]
            )

        avg_processing_time = (
            self._stream_stats["total_processing_time"]
            / self._stream_stats["successful_operations"]
            if self._stream_stats["successful_operations"] > 0
            else 0
        )

        overall_records_per_second = (
            self._stream_stats["total_records_received"] / total_duration
            if total_duration > 0
            else 0
        )

        success_rate = (
            (
                self._stream_stats["successful_operations"]
                / self._stream_stats["total_batches_processed"]
            )
            * 100
            if self._stream_stats["total_batches_processed"] > 0
            else 0
        )

        failure_rate = (
            (
                self._stream_stats["total_records_failed"]
                / self._stream_stats["total_records_received"]
            )
            * 100
            if self._stream_stats["total_records_received"] > 0
            else 0
        )

        # Get final table row count
        final_table_count = "unknown"
        try:
            with self.connector._engine.connect() as conn:
                verification_query = f"SELECT COUNT(*) FROM {self.full_table_name}"
                count_result = conn.execute(sqlalchemy.text(verification_query))
                final_table_count = count_result.scalar()
        except Exception as final_stats_error:
            # DO NOT SILENCE FINAL STATISTICS ERRORS - Log them
            final_table_count = "statistics_query_failed"
            if self._logger:
                self._logger.error(
                    f"❌ FINAL STATISTICS QUERY FAILED: {final_stats_error}",
                    extra={
                        "stream_name": self.stream_name,
                        "verification_query": verification_query,
                        "error_type": type(final_stats_error).__name__,
                        "error_details": str(final_stats_error),
                        "context": "final_statistics_generation",
                    },
                )

        self._logger.info(
            f"📊 FINAL STATISTICS REPORT - STREAM: {self.stream_name}",
            extra={
                "=== STREAM PROCESSING SUMMARY ===": True,
                "stream_name": self.stream_name,
                "table_name": self.full_table_name,
                "load_method": self.config.get("load_method", "append-only"),
                "=== RECORD PROCESSING STATS ===": True,
                "total_records_received": self._stream_stats["total_records_received"],
                "total_batches_processed": self._stream_stats[
                    "total_batches_processed"
                ],
                "successful_batches": self._stream_stats["successful_operations"],
                "failed_batches": len(self._stream_stats["failed_batches"]),
                "success_rate_percent": round(success_rate, 2),
                "failure_rate_percent": round(failure_rate, 2),
                "=== DATABASE OPERATIONS ===": True,
                "total_records_inserted": self._stream_stats["total_records_inserted"],
                "total_records_updated": self._stream_stats["total_records_updated"],
                "total_records_failed": self._stream_stats["total_records_failed"],
                "insert_operations": self._stream_stats["database_operations"][
                    "inserts"
                ],
                "merge_operations": self._stream_stats["database_operations"]["merges"],
                "total_rows_affected": self._stream_stats["database_operations"][
                    "rows_affected"
                ],
                "final_table_row_count": final_table_count,
                "=== PERFORMANCE METRICS ===": True,
                "total_processing_duration": round(total_duration, 3),
                "avg_batch_processing_time": round(avg_processing_time, 3),
                "overall_records_per_second": round(overall_records_per_second, 2),
                "largest_batch_size": self._stream_stats["largest_batch_size"],
                "smallest_batch_size": (
                    self._stream_stats["smallest_batch_size"]
                    if self._stream_stats["smallest_batch_size"] != float("inf")
                    else 0
                ),
                "avg_batch_size": (
                    round(
                        self._stream_stats["total_records_received"]
                        / self._stream_stats["total_batches_processed"],
                        2,
                    )
                    if self._stream_stats["total_batches_processed"] > 0
                    else 0
                ),
                "=== FAILURE ANALYSIS ===": True,
                "failed_batch_details": (
                    self._stream_stats["failed_batches"][-5:]
                    if self._stream_stats["failed_batches"]
                    else "No failures"
                ),
                "total_failed_records": self._stream_stats["total_records_failed"],
                "=== TIMING INFO ===": True,
                "first_batch_timestamp": (
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime(self._stream_stats["first_batch_time"]),
                    )
                    if self._stream_stats["first_batch_time"]
                    else "N/A"
                ),
                "last_batch_timestamp": (
                    time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime(self._stream_stats["last_batch_time"]),
                    )
                    if self._stream_stats["last_batch_time"]
                    else "N/A"
                ),
                "total_session_duration": round(total_duration, 3),
            },
        )

        # Additional summary log for quick reference
        self._logger.info(
            f"🎯 QUICK SUMMARY - {self.stream_name}: "
            f"{self._stream_stats['total_records_received']} records → "
            f"{self._stream_stats['total_records_inserted']} inserted, "
            f"{self._stream_stats['total_records_updated']} updated, "
            f"{self._stream_stats['total_records_failed']} failed | "
            f"Final table count: {final_table_count} | "
            f"Success rate: {round(success_rate, 1)}% | "
            f"Avg speed: {round(overall_records_per_second, 1)} rec/sec"
        )
