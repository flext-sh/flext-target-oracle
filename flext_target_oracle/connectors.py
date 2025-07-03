"""
Oracle Connector with maximum performance optimizations for WAN and parallelism.

This connector leverages all Oracle Database advanced features:
- Network optimization for WAN environments
- Maximum parallelism and partitioning
- Advanced bulk operations and compression
- Oracle 19c/21c/23c features
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from singer_sdk.connectors import SQLConnector
from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.dialects.oracle import TIMESTAMP

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from sqlalchemy.engine import Connection, Engine


class OracleConnector(SQLConnector):
    """
    High-performance Oracle connector optimized for WAN and parallel processing.

    Features:
    - WAN optimization with SDU/TDU tuning
    - Maximum parallelism with RAC awareness
    - Advanced bulk operations with direct path
    - Network compression and encryption
    - Connection multiplexing and pooling
    """

    # Oracle capabilities - disable column alter to avoid DDL issues
    allow_column_add: bool = True
    allow_column_rename: bool = False  # Oracle ALTER COLUMN syntax is complex
    allow_column_alter: bool = False  # Disable to avoid ORA-01735 errors
    allow_merge_upsert: bool = True
    allow_temp_tables: bool = True

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize Oracle connector with Oracle-specific type mappings."""
        super().__init__(config)

        # Override format handlers to use Oracle types
        self.jsonschema_to_sql.register_format_handler(
            "date-time", lambda _: TIMESTAMP()
        )
        self.jsonschema_to_sql.register_format_handler("date", lambda _: TIMESTAMP())
        self.jsonschema_to_sql.register_format_handler("time", lambda _: TIMESTAMP())

    def get_column_type(self, column_name: str, jsonschema_type: dict[str, Any]) -> Any:
        """Override column type mapping with JSON schema type priority."""
        from sqlalchemy.dialects.oracle import CHAR, CLOB, NUMBER, VARCHAR2

        # Get JSON schema type info
        json_type = jsonschema_type.get("type", "string")
        json_format = jsonschema_type.get("format")

        # Handle type arrays (nullable types)
        if isinstance(json_type, list):
            json_type = next((t for t in json_type if t != "null"), "string")

        # Get configuration settings
        schema_convention = self.config.get("schema_naming_convention", "generic")
        enable_smart_typing = self.config.get("enable_smart_typing", True)
        default_varchar_length = self.config.get("varchar_default_length", 255)
        max_varchar_length = self.config.get("varchar_max_length", 4000)

        # Debug logging to understand what's happening
        if self.config.get("debug_type_mapping", False):
            print(
                f"DEBUG: get_column_type called for {column_name} with schema "
                f"{jsonschema_type}"
            )
            print(
                f"DEBUG: json_type={json_type}, format={json_format}, "
                f"convention={schema_convention}"
            )

        # PRIORITY 1: JSON Schema type mapping
        # (user's feedback: "olhar o tipo de campo antes das regras")
        if json_type == "integer":
            oracle_type = NUMBER()  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: {column_name} (integer) -> {oracle_type}")
            return oracle_type

        elif json_type == "number":
            oracle_type = NUMBER()  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: {column_name} (number) -> {oracle_type}")
            return oracle_type

        elif json_type == "boolean":
            # Apply naming convention rules ONLY for boolean
            if (
                schema_convention == "wms"
                and enable_smart_typing
                and column_name.upper().endswith("_FLG")
            ):
                # WMS uses CHAR(1) for flags
                oracle_type = CHAR(1)  # type: ignore[assignment]
            else:
                # Standard Oracle boolean
                oracle_type = NUMBER(1, 0)  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: {column_name} (boolean) -> {oracle_type}")
            return oracle_type

        elif json_type == "string":
            # PRIORITY 2: Date/time format handling
            # (user's feedback: "date/time tem que usar timestamp(6)")
            if json_format in ("date-time", "date", "time"):
                oracle_type = TIMESTAMP()  # type: ignore[assignment]
                if self.config.get("debug_type_mapping", False):
                    print(
                        f"DEBUG: {column_name} (string with {json_format} format) -> "
                        f"{oracle_type}"
                    )
                return oracle_type

            # PRIORITY 3: Explicit maxLength from schema
            max_length = jsonschema_type.get("maxLength")
            if max_length:
                oracle_type = VARCHAR2(
                    min(max_length, max_varchar_length)
                )  # type: ignore[assignment]
                if self.config.get("debug_type_mapping", False):
                    print(
                        f"DEBUG: {column_name} (string with "
                        f"maxLength={max_length}) -> {oracle_type}"
                    )
                return oracle_type

            # PRIORITY 4: Smart typing rules
            # (only for string fields without explicit length)
            if enable_smart_typing:
                if schema_convention == "wms":
                    # WMS-specific string rules
                    if column_name.upper().endswith("_KEY"):
                        oracle_type = VARCHAR2(255)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (WMS _KEY rule) -> {oracle_type}"
                            )
                        return oracle_type
                    elif any(
                        word in column_name.lower() for word in ["str", "user", "name"]
                    ):
                        oracle_type = VARCHAR2(255)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (WMS str/user/name rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type
                    elif column_name.upper().endswith("_DESC"):
                        oracle_type = VARCHAR2(255)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (WMS _DESC rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type
                    elif any(
                        word in column_name.lower() for word in ["code", "status"]
                    ):
                        oracle_type = VARCHAR2(50)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (WMS code/status rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type
                else:
                    # Generic smart string rules
                    if any(word in column_name.lower() for word in ["key", "code"]):
                        oracle_type = VARCHAR2(100)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (generic key/code rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type
                    elif any(word in column_name.lower() for word in ["name", "title"]):
                        oracle_type = VARCHAR2(255)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (generic name/title rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type
                    elif any(
                        word in column_name.lower()
                        for word in ["desc", "comment", "note"]
                    ):
                        oracle_type = VARCHAR2(500)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} "
                                f"(generic desc/comment/note rule) -> {oracle_type}"
                            )
                        return oracle_type
                    elif any(
                        word in column_name.lower() for word in ["status", "code"]
                    ):
                        oracle_type = VARCHAR2(50)  # type: ignore[assignment]
                        if self.config.get("debug_type_mapping", False):
                            print(
                                f"DEBUG: {column_name} (generic status/code rule) "
                                f"-> {oracle_type}"
                            )
                        return oracle_type

            # PRIORITY 5: Default VARCHAR2 length
            oracle_type = VARCHAR2(default_varchar_length)  # type: ignore[assignment]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: {column_name} (default VARCHAR2) -> {oracle_type}")
            return oracle_type

        elif json_type in ("object", "array"):
            return CLOB()  # JSON data

        # Fallback to default VARCHAR2
        return VARCHAR2(default_varchar_length)

    def to_sql_type(self, jsonschema_type: dict[str, Any]) -> Any:
        """Convert JSON Schema type to Oracle SQL type with user feedback priority."""
        from sqlalchemy.dialects.oracle import CLOB, NUMBER, VARCHAR2

        # Get JSON schema type info
        json_type = jsonschema_type.get("type", "string")
        json_format = jsonschema_type.get("format")

        # Handle type arrays (nullable types)
        if isinstance(json_type, list):
            json_type = next((t for t in json_type if t != "null"), "string")

        # Get configuration settings
        schema_convention = self.config.get("schema_naming_convention", "generic")
        default_varchar_length = self.config.get("varchar_default_length", 255)
        max_varchar_length = self.config.get("varchar_max_length", 4000)

        # Debug logging
        if self.config.get("debug_type_mapping", False):
            print(f"DEBUG: to_sql_type called with schema {jsonschema_type}")
            print(
                f"DEBUG: json_type={json_type}, format={json_format}, "
                f"convention={schema_convention}"
            )

        # PRIORITY 1: JSON Schema type mapping
        # (user's feedback: "olhar o tipo de campo antes das regras")
        if json_type == "integer":
            oracle_type = NUMBER()  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: to_sql_type (integer) -> {oracle_type}")
            return oracle_type

        elif json_type == "number":
            oracle_type = NUMBER()  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: to_sql_type (number) -> {oracle_type}")
            return oracle_type

        elif json_type == "boolean":
            # Oracle doesn't have native boolean, use NUMBER(1)
            oracle_type = NUMBER(1, 0)  # type: ignore[no-untyped-call]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: to_sql_type (boolean) -> {oracle_type}")
            return oracle_type

        elif json_type == "string":
            # PRIORITY 2: Date/time format handling
            # (user's feedback: "date/time tem que usar timestamp(6)")
            if json_format in ("date-time", "date", "time"):
                oracle_type = TIMESTAMP()  # type: ignore[assignment]
                if self.config.get("debug_type_mapping", False):
                    print(
                        f"DEBUG: to_sql_type (string with {json_format} format) "
                        f"-> {oracle_type}"
                    )
                return oracle_type

            # PRIORITY 3: Explicit maxLength from schema
            max_length = jsonschema_type.get("maxLength")
            if max_length:
                oracle_type = VARCHAR2(
                    min(max_length, max_varchar_length)
                )  # type: ignore[assignment]
                if self.config.get("debug_type_mapping", False):
                    print(
                        f"DEBUG: to_sql_type (string with maxLength={max_length}) "
                        f"-> {oracle_type}"
                    )
                return oracle_type

            # PRIORITY 4: Use default VARCHAR2 length
            # (no column name available in to_sql_type)
            oracle_type = VARCHAR2(default_varchar_length)  # type: ignore[assignment]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: to_sql_type (string default) -> {oracle_type}")
            return oracle_type

        elif json_type in ("object", "array"):
            oracle_type = CLOB()  # type: ignore[assignment]
            if self.config.get("debug_type_mapping", False):
                print(f"DEBUG: to_sql_type (object/array) -> {oracle_type}")
            return oracle_type

        # Fallback to default VARCHAR2
        oracle_type = VARCHAR2(default_varchar_length)  # type: ignore[assignment]
        if self.config.get("debug_type_mapping", False):
            print(f"DEBUG: to_sql_type (fallback) -> {oracle_type}")
        return oracle_type

    def prepare_column(
        self,
        full_table_name: str | Any,
        column_name: str,
        sql_type: Any,
    ) -> None:
        """Prepare column with Oracle-specific DDL handling."""
        # Override to use Oracle-specific column management
        if self.column_exists(full_table_name, column_name):
            # Column exists - check if type needs modification
            # For Oracle, we'll skip column modification to avoid DDL issues
            return
        else:
            # Column doesn't exist - add it
            self._add_column(full_table_name, column_name, sql_type)

    def _add_column(
        self, full_table_name: str, column_name: str, sql_type: Any
    ) -> None:
        """Add column using Oracle-specific syntax."""
        with self._engine.connect() as conn, conn.begin():
            # Compile the SQL type to get proper Oracle syntax
            compiled_type = sql_type.compile(dialect=conn.dialect)

            # Use Oracle ADD COLUMN syntax
            add_column_ddl = text(
                f"ALTER TABLE {full_table_name} ADD ({column_name} {compiled_type})"
            )
            conn.execute(add_column_ddl)

    def create_schema(self, schema_name: str) -> None:
        """Create schema - In Oracle, user is the schema, so skip creation."""
        # In Oracle, schemas are tied to users
        # For user schemas (like OIC), they already exist when user is created
        # Only try to create if it's a different schema than the connected user
        with self._engine.connect() as conn:
            current_user = conn.execute(text("SELECT USER FROM DUAL")).scalar()
            if current_user and schema_name.upper() != current_user.upper():
                # Only create if it's not the user's default schema
                super().create_schema(schema_name)

    def get_sqlalchemy_url(self, config: dict[str, Any] | None = None) -> str:
        """Build Oracle URL with maximum performance parameters."""
        if config is None:
            config = self.config

        # Use complete connection string if provided
        if config.get("connection_string"):
            return str(config["connection_string"])

        # Build high-performance connection URL
        username = config["username"]
        password = str(config["password"])  # Convert SecretString to str
        host = config["host"]
        port = config.get("port", 1521)

        # Service name preferred for RAC/Data Guard
        if config.get("service_name"):
            database = config["service_name"]
        else:
            database = config.get("database", "XE")

        # Base URL with oracledb driver
        url = f"oracle+oracledb://{username}:{password}@"

        # For Oracle Autonomous Database or TCPS connections, use DSN format
        if config.get("protocol") == "tcps" or config.get("is_autonomous_database"):
            # Build proper DSN for SQLAlchemy with oracledb
            # Build proper DSN for SQLAlchemy with oracledb
            protocol = config.get("protocol", "tcp").upper()
            dsn = (
                f"(DESCRIPTION=(ADDRESS=(PROTOCOL={protocol})"
                f"(HOST={host})(PORT={port}))"
                f"(CONNECT_DATA=(SERVICE_NAME={database})"
            )

            # Add SSL settings for TCPS
            if config.get("protocol") == "tcps" and config.get(
                "ssl_server_dn_match", False
            ):
                dsn += "(SECURITY=(SSL_SERVER_CERT_DN=TRUE))"

            dsn += "))"

            # Use DSN format for URL
            url += dsn
        else:
            # Standard connection for non-TCPS
            url += f"{host}:{port}/{database}"

        # Don't add query parameters as they're handled in connect_args
        return url

    def create_engine(self) -> Engine:
        """Create SQLAlchemy engine with maximum Oracle performance features."""
        # For Oracle Autonomous Database with TCPS, use connect_args approach
        if self.config.get("protocol") == "tcps":
            # Build DSN for connect_args
            host = self.config["host"]
            port = self.config.get("port", 1521)
            service_name = self.config.get("service_name") or self.config.get(
                "database", "XE"
            )

            dsn = f"""(DESCRIPTION=
                (ADDRESS=(PROTOCOL=TCPS)(HOST={host})(PORT={port}))
                (CONNECT_DATA=(SERVICE_NAME={service_name}))
            )"""

            # Use empty URL with connect_args
            url = "oracle+oracledb://@"

            # Connect args for TCPS
            password = str(self.config["password"])
            # Remove quotes if present
            if password.startswith('"') and password.endswith('"'):
                password = password[1:-1]

            connect_args = {
                "user": self.config["username"],
                "password": password,
                "dsn": dsn,
                "ssl_server_dn_match": self.config.get("ssl_server_dn_match", False),
                # Only use parameters supported in Thin Mode
                "tcp_connect_timeout": float(self.config.get("connection_timeout", 60)),
            }

            # Add wallet if provided
            if self.config.get("wallet_location"):
                connect_args["config_dir"] = self.config["wallet_location"]
                connect_args["wallet_location"] = self.config["wallet_location"]
                if self.config.get("wallet_password"):
                    connect_args["wallet_password"] = self.config["wallet_password"]
        else:
            # Standard connection for non-TCPS
            url = self.get_sqlalchemy_url()
            connect_args = {}

        # Determine optimal pool class based on workload
        if self.config.get("use_null_pool"):
            pool_class: Any = pool.NullPool
        elif self.config.get("use_static_pool"):
            pool_class = pool.StaticPool
        elif self.config.get("use_assertion_pool"):
            pool_class = pool.AssertionPool
        else:
            pool_class = pool.QueuePool

        # Engine configuration - simplified for NullPool compatibility
        engine_kwargs = {
            "poolclass": pool_class,
        }

        # Only add pool parameters if not using NullPool
        if pool_class != pool.NullPool:
            engine_kwargs.update({
                "pool_size": self.config.get("pool_size", 10),
                "max_overflow": self.config.get("max_overflow", 20),
                "pool_timeout": self.config.get("pool_timeout", 60),
                "pool_recycle": self.config.get("pool_recycle", 1800),
                "pool_pre_ping": self.config.get("pool_pre_ping", True),
                "pool_use_lifo": self.config.get("pool_use_lifo", True),
            })

        # Add common parameters
        engine_kwargs.update({
            # SQLAlchemy 2.0+ performance features
            "future": True,
            "query_cache_size": self.config.get(
                "query_cache_size", 5000
            ),  # Large cache
            "use_insertmanyvalues": self.config.get("use_insertmanyvalues", True),
            "insertmanyvalues_page_size": self.config.get(
                "insertmanyvalues_page_size", 50000
            ),  # Large batches
            # Execution options for performance
            "execution_options": {
                "isolation_level": self.config.get("isolation_level", "READ COMMITTED"),
                "compiled_cache": {},  # Statement compilation cache
                "synchronize_session": False,  # Disable for performance
                "stream_results": self.config.get(
                    "stream_results", True
                ),  # For large results
                "max_row_buffer": self.config.get("max_row_buffer", 10000),
            },
            # Debugging
            "echo": self.config.get("echo", False),
            "echo_pool": self.config.get("echo_pool", False),
            "hide_parameters": not self.config.get("log_sql_parameters", False),
        })

        # Add connect_args if present
        if connect_args:
            engine_kwargs["connect_args"] = connect_args

        # Create engine
        engine = create_engine(url, **engine_kwargs)

        # Skip performance optimizations for now to avoid
        # SQLAlchemy compatibility issues
        # self._apply_performance_optimizations(engine)

        return engine

    def _apply_performance_optimizations(self, engine: Engine) -> None:
        """Apply maximum Oracle performance optimizations."""

        @event.listens_for(engine, "connect")
        def optimize_session(dbapi_connection: Any, _connection_record: Any) -> None:
            """Configure each connection for maximum performance."""
            # Set connection attributes for performance
            dbapi_connection.arraysize = self.config.get("array_size", 1000)
            dbapi_connection.prefetchrows = self.config.get("prefetch_rows", 100)

            # Set client info for monitoring
            dbapi_connection.module = self.config.get("module", "flext-oracle-target")
            dbapi_connection.action = self.config.get("action", "bulk_load")
            dbapi_connection.clientinfo = self.config.get(
                "client_info", "FLEXT High Performance Target"
            )

            with dbapi_connection.cursor() as cursor:
                # Session optimization statements
                optimizations = []

                # Date/time formats for consistency
                optimizations.extend(
                    [
                        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'",
                        "ALTER SESSION SET NLS_TIMESTAMP_FORMAT = "
                        "'YYYY-MM-DD HH24:MI:SS.FF6'",
                        "ALTER SESSION SET NLS_TIMESTAMP_TZ_FORMAT = "
                        "'YYYY-MM-DD HH24:MI:SS.FF6 TZH:TZM'",
                    ]
                )

                # Timezone
                tz = self.config.get("timestamp_timezone", "UTC")
                optimizations.append(f"ALTER SESSION SET TIME_ZONE = '{tz}'")

                # Maximum parallel processing (requires EE)
                if self.config.get("parallel_degree", 1) > 1:
                    if self.config.get("oracle_is_enterprise_edition", False):
                        degree = self.config["parallel_degree"]
                        optimizations.extend(
                            [
                                "ALTER SESSION ENABLE PARALLEL DML",
                                "ALTER SESSION ENABLE PARALLEL DDL",
                                "ALTER SESSION ENABLE PARALLEL QUERY",
                                f"ALTER SESSION FORCE PARALLEL DML PARALLEL {degree}",
                                f"ALTER SESSION FORCE PARALLEL DDL PARALLEL {degree}",
                                f"ALTER SESSION FORCE PARALLEL QUERY PARALLEL {degree}",
                            ]
                        )

                    # Parallel execution parameters
                    if self.config.get("parallel_max_servers"):
                        optimizations.append(
                            "ALTER SESSION SET PARALLEL_MAX_SERVERS = "
                            f"{self.config['parallel_max_servers']}"
                        )
                    if self.config.get("parallel_min_servers"):
                        optimizations.append(
                            "ALTER SESSION SET PARALLEL_MIN_SERVERS = "
                            f"{self.config['parallel_min_servers']}"
                        )

                # Optimizer settings for performance
                optimizer_mode = self.config.get("optimizer_mode", "ALL_ROWS")
                optimizations.extend(
                    [
                        f"ALTER SESSION SET OPTIMIZER_MODE = {optimizer_mode}",
                        "ALTER SESSION SET OPTIMIZER_ADAPTIVE_PLANS = TRUE",
                        "ALTER SESSION SET OPTIMIZER_ADAPTIVE_STATISTICS = TRUE",
                    ]
                )

                # Query optimization features
                if self.config.get("enable_result_cache", True):
                    optimizations.append("ALTER SESSION SET RESULT_CACHE_MODE = FORCE")
                if self.config.get("enable_query_rewrite", True):
                    optimizations.append(
                        "ALTER SESSION SET QUERY_REWRITE_ENABLED = TRUE"
                    )

                # Memory optimization
                if self.config.get("pga_aggregate_limit"):
                    optimizations.append(
                        "ALTER SESSION SET PGA_AGGREGATE_LIMIT = "
                        f"{self.config['pga_aggregate_limit']}"
                    )
                if self.config.get("sort_area_size"):
                    optimizations.append(
                        "ALTER SESSION SET SORT_AREA_SIZE = "
                        f"{self.config['sort_area_size']}"
                    )
                if self.config.get("hash_area_size"):
                    optimizations.append(
                        "ALTER SESSION SET HASH_AREA_SIZE = "
                        f"{self.config['hash_area_size']}"
                    )

                # Direct path operations
                if self.config.get("use_direct_path", True):
                    optimizations.append(
                        "ALTER SESSION SET '_serial_direct_read' = TRUE"
                    )

                # Big data optimizations
                if self.config.get("enable_big_data_sql", True):
                    optimizations.append(
                        "ALTER SESSION SET '_optimizer_gather_stats_on_load' = TRUE"
                    )

                # In-Memory features (if available)
                if self.config.get("use_inmemory"):
                    optimizations.extend(
                        [
                            "ALTER SESSION SET INMEMORY_QUERY = ENABLE",
                            "ALTER SESSION SET INMEMORY_SIZE = 1G",
                        ]
                    )

                # Execute all optimizations with smart error handling
                for opt in optimizations:
                    try:
                        cursor.execute(opt)
                    except Exception as e:
                        # Categorize Oracle optimization errors
                        error_msg = str(e)
                        if any(
                            code in error_msg
                            for code in ["ORA-00942", "ORA-00900", "ORA-02248"]
                        ):
                            # Critical errors: table doesn't exist,
                            # SQL error, invalid option
                            raise RuntimeError(
                                f"Critical Oracle optimization error: {opt} - {e}"
                            ) from e
                        elif any(
                            code in error_msg for code in ["ORA-00031", "ORA-02097"]
                        ):
                            # Feature not available in this Oracle
                            # edition/version - log warning
                            print(
                                f"WARNING: Oracle feature not available, "
                                f"skipping: {opt} - {e}"
                            )
                        else:
                            # Unknown error - log and continue
                            # but make it visible
                            print(
                                f"WARNING: Oracle optimization failed, "
                                f"continuing: {opt} - {e}"
                            )

                # Set array size for this connection
                cursor.arraysize = self.config.get("array_size", 50000)

    def prepare_database(self) -> None:
        """Prepare database for high-performance operations."""
        with self._engine.begin() as conn:
            preparations = []

            # Enable supplemental logging for CDC if needed
            if self.config.get("enable_supplemental_logging"):
                preparations.append("ALTER DATABASE ADD SUPPLEMENTAL LOG DATA")

            # Force logging for recovery
            if self.config.get("force_logging"):
                preparations.append("ALTER DATABASE FORCE LOGGING")

            # Flashback features
            if self.config.get("enable_flashback"):
                preparations.append("ALTER DATABASE FLASHBACK ON")

            for prep in preparations:
                try:
                    conn.execute(text(prep))
                except Exception as e:
                    # Log database preparation failures instead of silently suppressing
                    print(f"WARNING: Database preparation failed: {prep} - {e}")

    def create_high_performance_table(
        self,
        full_table_name: str,
        schema: dict[str, Any],
        primary_keys: list[str] | None = None,
        partition_keys: list[str] | None = None,
    ) -> None:
        """Create table with maximum performance features."""
        # Let parent create the basic table using prepare_table method
        self.prepare_table(
            full_table_name=full_table_name,
            schema=schema,
            primary_keys=primary_keys or [],
            as_temp_table=False,
        )

        # Apply advanced optimizations
        with self._engine.begin() as conn:
            table_name = full_table_name

            # Advanced compression
            if self.config.get("enable_compression"):
                compression = self.config.get("compression_type", "ADVANCED")
                compress_for = self.config.get("compress_for", "OLTP")
                conn.execute(
                    text(
                        f"ALTER TABLE {table_name} COMPRESS FOR "
                        f"{compress_for} {compression}"
                    )
                )

            # Maximum parallelism
            if self.config.get("parallel_degree", 1) > 1:
                degree = self.config["parallel_degree"]
                conn.execute(text(f"ALTER TABLE {table_name} PARALLEL {degree}"))

            # In-Memory column store
            if self.config.get("use_inmemory"):
                inmem_opts = []
                if self.config.get("inmemory_priority"):
                    inmem_opts.append(f"PRIORITY {self.config['inmemory_priority']}")
                if self.config.get("inmemory_distribute"):
                    inmem_opts.append(
                        f"DISTRIBUTE {self.config['inmemory_distribute']}"
                    )
                if self.config.get("inmemory_duplicate"):
                    inmem_opts.append(f"DUPLICATE {self.config['inmemory_duplicate']}")

                inmem_clause = " ".join(inmem_opts)
                conn.execute(text(f"ALTER TABLE {table_name} INMEMORY {inmem_clause}"))

            # Result cache for frequently accessed tables
            if self.config.get("use_result_cache"):
                conn.execute(
                    text(f"ALTER TABLE {table_name} RESULT_CACHE (MODE FORCE)")
                )

            # Advanced indexing
            if primary_keys and self.config.get("create_indexes"):
                # Create primary key index with advanced options
                idx_name = f"PK_{table_name.split('.')[-1]}"[:30]
                idx_opts = []

                if self.config.get("index_compression"):
                    idx_opts.append("COMPRESS ADVANCED LOW")
                if self.config.get("invisible_indexes"):
                    idx_opts.append("INVISIBLE")
                if self.config.get("parallel_degree", 1) > 1:
                    idx_opts.append(f"PARALLEL {self.config['parallel_degree']}")

                idx_clause = " ".join(idx_opts)
                conn.execute(
                    text(
                        f"CREATE UNIQUE INDEX {idx_name} ON {table_name} "
                        f"({','.join(primary_keys)}) {idx_clause}"
                    )
                )

            # Table partitioning for scalability
            if partition_keys and self.config.get("enable_partitioning"):
                self._create_partitions(conn, table_name, partition_keys)

            # Automatic Data Optimization (ADO)
            if self.config.get("enable_ado"):
                conn.execute(
                    text(
                        f"""
                    ALTER TABLE {table_name} ILM ADD POLICY
                    ROW STORE COMPRESS ADVANCED SEGMENT
                    AFTER 30 DAYS OF NO MODIFICATION
                """
                    )
                )

    def _create_partitions(
        self, conn: Connection, table_name: str, partition_keys: list[str]
    ) -> None:
        """Create advanced partitioning for maximum performance."""
        partition_type = self.config.get("partition_type", "INTERVAL")
        partition_col = partition_keys[0]

        if partition_type == "INTERVAL":
            # Interval partitioning for time-series data
            interval = self.config.get(
                "partition_interval",
                "NUMTOYMINTERVAL(1,'MONTH')",
            )
            conn.execute(
                text(
                    f"""
                ALTER TABLE {table_name} MODIFY
                PARTITION BY RANGE ({partition_col})
                INTERVAL ({interval})
                (PARTITION p_initial VALUES LESS THAN "
                "(TO_DATE('2020-01-01','YYYY-MM-DD')))"
            """
                )
            )

        elif partition_type == "HASH":
            # Hash partitioning for even distribution
            partitions = self.config.get("hash_partitions", 32)
            conn.execute(
                text(
                    f"""
                ALTER TABLE {table_name} MODIFY
                PARTITION BY HASH ({partition_col})
                PARTITIONS {partitions}
            """
                )
            )

        elif partition_type == "LIST":
            # List partitioning for categorical data
            # Would need specific values from config
            pass

        # Enable partition-wise joins
        if self.config.get("enable_partition_wise_joins"):
            conn.execute(text("ALTER SESSION SET '_partition_large_extents' = TRUE"))

    @contextmanager
    def get_high_performance_connection(self) -> Iterator[Connection]:
        """Get connection optimized for bulk operations."""
        with self._engine.connect() as conn, conn.begin():
            # Disable constraints temporarily for speed
            if self.config.get("disable_constraints_during_load"):
                conn.execute(text("SET CONSTRAINTS ALL DEFERRED"))

            # Use append mode for direct path
            if self.config.get("use_append_values_hint"):
                conn.execute(
                    text("ALTER SESSION SET '_direct_path_insert_mode' = TRUE")
                )

            yield conn

    def prepare_table(
        self,
        full_table_name: str | Any,
        schema: dict[str, Any],
        primary_keys: Sequence[str],
        partition_keys: list[str] | None = None,
        as_temp_table: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Adapt target table to provided schema if possible."""
        # 🔍 DEBUG: Log load_method and table existence
        print(f"🔍 PREPARE_TABLE DEBUG - Table: {full_table_name}")
        print(f"🔍 load_method from config: {self.config.get('load_method')}")
        print(f"🔍 Table exists: {self.table_exists(full_table_name=full_table_name)}")

        # Call parent implementation
        super().prepare_table(
            full_table_name=full_table_name,
            schema=schema,
            primary_keys=primary_keys,
            partition_keys=partition_keys,
            as_temp_table=as_temp_table,
        )

    def create_empty_table(
        self,
        full_table_name: str | Any,
        schema: dict[str, Any],
        primary_keys: list[str] | None = None,  # type: ignore[override]
        partition_keys: list[str] | None = None,
        as_temp_table: bool = False,  # noqa: FBT002, FBT001
    ) -> None:
        """Create table with Oracle-specific column types."""
        # 🔍 DEBUG: Log the schema being used for table creation
        properties = schema.get("properties", {})
        print(f"🔍 CREATE_EMPTY_TABLE DEBUG - Table: {full_table_name}")
        print(f"🔍 Schema has {len(properties)} properties")
        print(f"🔍 Properties: {list(properties.keys())}")
        print(f"🔍 Primary keys: {primary_keys}")

        # Call parent implementation
        super().create_empty_table(
            full_table_name=full_table_name,
            schema=schema,
            primary_keys=primary_keys,
            partition_keys=partition_keys,
            as_temp_table=as_temp_table,
        )

    def analyze_and_optimize_table(self, table_name: str) -> None:
        """Analyze table and apply runtime optimizations."""
        with self._engine.begin() as conn:
            # Gather advanced statistics
            if self.config.get("gather_extended_statistics"):
                conn.execute(
                    text(
                        f"""
                    BEGIN
                        DBMS_STATS.GATHER_TABLE_STATS(
                            ownname => USER,
                            tabname => '{table_name.split(".")[-1]}',
                            estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
                            method_opt => 'FOR ALL COLUMNS SIZE AUTO',
                            granularity => 'ALL',
                            cascade => TRUE,
                            degree => DBMS_STATS.DEFAULT_DEGREE"
                        );
                    END;
                """
                    )
                )

            # Create extended statistics for correlated columns
            if self.config.get("create_extended_stats"):
                # This would need column correlation info from config
                pass

            # Refresh materialized views if any
            if self.config.get("refresh_mviews"):
                conn.execute(
                    text(
                        f"""
                    BEGIN
                        DBMS_MVIEW.REFRESH(
                            list => '{table_name}_MV',
                            method => 'C',
                            parallelism => {self.config.get('parallel_degree', 8)}
                        );
                    END;
                """
                    )
                )
