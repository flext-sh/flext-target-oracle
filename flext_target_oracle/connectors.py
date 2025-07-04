"""Oracle Connector using SQLAlchemy 2.0 modern features.

This connector leverages SQLAlchemy 2.0's advanced capabilities:
- Modern connection pooling with QueuePool
- Event system for connection optimization
- Oracle dialect with full type support
- Async-ready architecture
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from singer_sdk.connectors import SQLConnector
from sqlalchemy import Column, create_engine, event, pool
from sqlalchemy.dialects import oracle
from sqlalchemy.engine import URL
from sqlalchemy.schema import CreateColumn

try:
    import oracledb
except ImportError:
    oracledb = None

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.interfaces import DBAPIConnection
    from sqlalchemy.pool import Pool
    from sqlalchemy.types import TypeEngine

# Oracle VARCHAR2 maximum length before using CLOB
MAX_VARCHAR2_LENGTH = 4000


class OracleConnector(SQLConnector):
    """Modern Oracle connector using SQLAlchemy 2.0.

    Leverages SQLAlchemy's built-in features without reimplementation:
    - Connection pooling
    - Type mapping
    - Event system
    - Oracle dialect optimizations
    """

    # Let SQLAlchemy handle these capabilities
    allow_column_add: bool = True
    allow_column_rename: bool = True
    allow_column_alter: bool = True
    allow_merge_upsert: bool = True
    allow_temp_tables: bool = True

    def get_sqlalchemy_url(self, config: dict[str, Any]) -> str:
        """Construct SQLAlchemy URL using URL.create() - SQLAlchemy 2.0 way."""
        # Use oracledb (python-oracledb) driver
        url = URL.create(
            drivername="oracle+oracledb",
            username=config.get("user", config.get("username")),
            password=config["password"],
            host=config["host"],
            port=config.get("port", 1521),
            query=(
                {"service_name": config["service_name"]}
                if "service_name" in config
                else {}
            ),
        )
        return str(url)

    def create_engine(self) -> Engine:
        """Create SQLAlchemy 2.0 engine with Oracle optimizations."""
        # Let SQLAlchemy handle pool configuration
        pool_class = self._get_pool_class()

        engine = create_engine(
            self.get_sqlalchemy_url(self.config),
            # Use SQLAlchemy 2.0 features
            future=True,
            echo=self.config.get("echo", False),
            # Pool configuration
            poolclass=pool_class,
            pool_size=self.config.get("pool_size", 10),
            max_overflow=self.config.get("pool_max_overflow", 10),
            pool_timeout=self.config.get("pool_timeout", 30),
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_pre_ping=True,  # Verify connections before use
            # Oracle-specific via connect_args
            connect_args=self._get_connect_args(),
        )

        # Use SQLAlchemy's event system for optimization
        self._setup_event_listeners(engine)

        return engine

    def _get_pool_class(self) -> type[Pool]:
        """Select appropriate SQLAlchemy pool class."""
        pool_size = self.config.get("pool_size", 10)

        if pool_size == 0:
            return pool.NullPool  # No pooling
        if pool_size == 1:
            return pool.StaticPool  # Single connection
        return pool.QueuePool  # Default pooling

    def _get_connect_args(self) -> dict[str, Any]:
        """Get Oracle-specific connection arguments."""
        args = {
            "encoding": "UTF-8",
            "nencoding": "UTF-8",
            "threaded": True,  # Thread-safe mode
            "events": True,  # Enable event notifications
        }

        # Add thick mode if needed (for certain Oracle features)
        if self.config.get("oracle_thick_mode", False) and oracledb is not None:
            oracledb.init_oracle_client()

        return args

    def _setup_event_listeners(self, engine: Engine) -> None:
        """Setup SQLAlchemy event listeners for Oracle optimization."""

        @event.listens_for(engine, "connect")
        def receive_connect(dbapi_conn: DBAPIConnection, _: object) -> None:
            """Configure each new connection."""
            cursor = dbapi_conn.cursor()
            try:
                # Set session parameters for optimization
                if self.config.get("enable_parallel_dml", False):
                    cursor.execute("ALTER SESSION ENABLE PARALLEL DML")

                # Set NLS formats for consistency
                cursor.execute(
                    "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'",
                )
                cursor.execute(
                    "ALTER SESSION SET NLS_TIMESTAMP_FORMAT = "
                    "'YYYY-MM-DD HH24:MI:SS.FF6'",
                )

                # Set optimizer mode if specified
                if optimizer_mode := self.config.get("optimizer_mode"):
                    cursor.execute(
                        f"ALTER SESSION SET OPTIMIZER_MODE = {optimizer_mode}",
                    )
            finally:
                cursor.close()

            # Configure connection parameters (Oracle-specific)
            if hasattr(dbapi_conn, "arraysize"):
                dbapi_conn.arraysize = self.config.get("arraysize", 1000)
            if hasattr(dbapi_conn, "prefetchrows"):
                dbapi_conn.prefetchrows = self.config.get("prefetchrows", 1000)

    @property
    def connector_config(self) -> dict[str, Any]:
        """Return config for Singer SDK, hiding password."""
        config = dict(self.config)
        config.pop("password", None)
        return config

    def get_column_add_ddl(  # type: ignore[override]
        self, _: str, column_name: str, column_type: TypeEngine[Any],
    ) -> str:
        """Use SQLAlchemy's DDL compiler for ALTER TABLE ADD."""
        # Create column for DDL
        column: Column[Any] = Column(column_name, column_type)

        # Use SQLAlchemy's DDL compiler
        add_column_ddl = CreateColumn(column)
        compiled_ddl = add_column_ddl.compile(dialect=self._engine.dialect)
        return f"ALTER TABLE {{table_name}} ADD {compiled_ddl}"

    def to_sql_type(self, jsonschema_type: dict[str, Any]) -> TypeEngine[Any]:
        """Convert JSON Schema types to SQLAlchemy Oracle types.

        Uses SQLAlchemy's Oracle dialect types directly.
        """
        json_type = jsonschema_type.get("type", "string")
        json_format = jsonschema_type.get("format")

        # Handle arrays (nullable types)
        if isinstance(json_type, list):
            json_type = next((t for t in json_type if t != "null"), "string")

        # Map types to Oracle types
        type_mapping = {
            "integer": oracle.NUMBER(precision=38, scale=0),  # type: ignore[no-untyped-call]
            "number": oracle.NUMBER(),  # type: ignore[no-untyped-call]
            "boolean": oracle.NUMBER(precision=1, scale=0),  # type: ignore[no-untyped-call]
        }

        if json_type in type_mapping:
            return type_mapping[json_type]

        if json_type == "string":
            return self._get_string_type(json_format, jsonschema_type)

        if json_type in {"object", "array"}:
            return oracle.CLOB()

        # Default fallback
        return oracle.VARCHAR2(length=255)

    def _get_string_type(
        self, json_format: str | None, jsonschema_type: dict[str, Any],
    ) -> TypeEngine[Any]:
        """Get Oracle type for string fields based on format."""
        if json_format == "date":
            return oracle.DATE()
        if json_format in {"date-time", "datetime", "time"}:
            return oracle.TIMESTAMP(timezone=False)

        # String length handling
        max_length = jsonschema_type.get("maxLength", 255)
        if max_length > MAX_VARCHAR2_LENGTH:
            return oracle.CLOB()
        return oracle.VARCHAR2(length=max_length)

    def get_column_type(
        self, column_name: str, jsonschema_type: dict[str, Any],
    ) -> TypeEngine[Any]:
        """Get SQLAlchemy column type with Oracle-specific handling.

        This method can consider column naming patterns for better type inference.
        """
        # First, get base type from JSON schema
        base_type = self.to_sql_type(jsonschema_type)

        # Apply Oracle-specific patterns if enabled
        if not self.config.get("enable_column_patterns", True):
            return base_type

        column_upper = column_name.upper()

        # Use pattern matching for better maintainability
        pattern_type = self._get_column_type_by_pattern(column_upper)
        return pattern_type if pattern_type else base_type

    def _get_column_type_by_pattern(self, column_upper: str) -> TypeEngine[Any] | None:
        """Get Oracle type based on column naming patterns."""
        # Define pattern mappings
        pattern_mappings = [
            # ID columns
            (lambda col: col.endswith("_ID") or col == "ID",
             oracle.NUMBER(precision=38, scale=0)),  # type: ignore[no-untyped-call]

            # Key columns
            (lambda col: col.endswith("_KEY"),
             oracle.VARCHAR2(length=255)),

            # Flag/Boolean columns
            (lambda col: col.endswith(("_FLG", "_FLAG", "_ENABLED", "_ACTIVE")),
             oracle.NUMBER(precision=1, scale=0)),  # type: ignore[no-untyped-call]

            # Date columns
            (lambda col: any(col.endswith(suffix) for suffix in ("_DATE", "_DT")),
             oracle.DATE()),

            # Timestamp columns
            (lambda col: any(col.endswith(suffix)
                           for suffix in ("_TIME", "_TS", "_TIMESTAMP", "_AT")),
             oracle.TIMESTAMP(timezone=False)),

            # Amount/Price columns
            (lambda col: any(col.endswith(suffix)
                           for suffix in ("_AMT", "_AMOUNT", "_PRICE", "_COST")),
             oracle.NUMBER(precision=19, scale=4)),  # type: ignore[no-untyped-call]

            # Percentage columns
            (lambda col: any(col.endswith(suffix)
                           for suffix in ("_PCT", "_PERCENT", "_RATE")),
             oracle.NUMBER(precision=5, scale=2)),  # type: ignore[no-untyped-call]

            # Description/Comment columns
            (lambda col: any(col.endswith(suffix)
                           for suffix in ("_DESC", "_DESCRIPTION", "_COMMENT", "_NOTE")),
             oracle.VARCHAR2(length=4000)),

            # Code columns
            (lambda col: col.endswith(("_CODE", "_CD")),
             oracle.VARCHAR2(length=50)),

            # Name columns
            (lambda col: col.endswith(("_NAME", "_NM")),
             oracle.VARCHAR2(length=255)),
        ]

        # Check patterns and return first match
        for pattern_check, oracle_type in pattern_mappings:
            if pattern_check(column_upper):
                return oracle_type

        return None

    def prepare_column_metadata(
        self, column_name: str, column_type: TypeEngine[Any],
    ) -> dict[str, Any]:
        """Prepare column metadata for SQLAlchemy table creation."""
        # Create column with proper attributes
        metadata = {
            "name": column_name,
            "type": column_type,
            "nullable": True,  # Default to nullable
            "primary_key": column_name.upper() == "ID",
        }

        # Add Oracle-specific attributes if needed
        if hasattr(column_type, "length") and column_type.length:
            metadata["length"] = column_type.length

        return metadata
