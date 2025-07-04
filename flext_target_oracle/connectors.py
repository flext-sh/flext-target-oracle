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
from sqlalchemy import create_engine, event, pool
from sqlalchemy.dialects import oracle
from sqlalchemy.engine import URL

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.interfaces import DBAPIConnection
    from sqlalchemy.pool import Pool


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

    def get_sqlalchemy_url(self, config: dict[str, Any]) -> URL:
        """Construct SQLAlchemy URL using URL.create() - SQLAlchemy 2.0 way."""
        # Use oracledb (python-oracledb) driver
        return URL.create(
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
        elif pool_size == 1:
            return pool.StaticPool  # Single connection
        else:
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
        if self.config.get("oracle_thick_mode", False):
            import oracledb

            oracledb.init_oracle_client()

        return args

    def _setup_event_listeners(self, engine: Engine) -> None:
        """Setup SQLAlchemy event listeners for Oracle optimization."""

        @event.listens_for(engine, "connect")
        def receive_connect(dbapi_conn: DBAPIConnection, _: Any) -> None:
            """Configure each new connection."""
            with dbapi_conn.cursor() as cursor:
                # Set session parameters for optimization
                if self.config.get("enable_parallel_dml", False):
                    cursor.execute("ALTER SESSION ENABLE PARALLEL DML")

                # Set NLS formats for consistency
                cursor.execute(
                    "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
                )
                cursor.execute(
                    "ALTER SESSION SET NLS_TIMESTAMP_FORMAT = "
                    "'YYYY-MM-DD HH24:MI:SS.FF6'"
                )

                # Set optimizer mode if specified
                if optimizer_mode := self.config.get("optimizer_mode"):
                    cursor.execute(
                        f"ALTER SESSION SET OPTIMIZER_MODE = {optimizer_mode}"
                    )

            # Configure connection parameters
            dbapi_conn.arraysize = self.config.get("arraysize", 1000)
            dbapi_conn.prefetchrows = self.config.get("prefetchrows", 1000)

    @property
    def connector_config(self) -> dict[str, Any]:
        """Return config for Singer SDK, hiding password."""
        config = super().connector_config.copy()
        config.pop("password", None)
        return config

    def get_column_add_ddl(
        self, _: str, column_name: str, column_type: Any
    ) -> str:
        """Use SQLAlchemy's DDL compiler for ALTER TABLE ADD."""
        from sqlalchemy import Column
        from sqlalchemy.schema import AddColumn

        # Create column for DDL
        column = Column(column_name, column_type)

        # Use SQLAlchemy's DDL compiler
        add_column = AddColumn(column)
        return str(add_column.compile(dialect=self._engine.dialect))

    def to_sql_type(self, jsonschema_type: dict[str, Any]) -> Any:
        """Convert JSON Schema types to SQLAlchemy Oracle types.

        Uses SQLAlchemy's Oracle dialect types directly.
        """

        json_type = jsonschema_type.get("type", "string")
        json_format = jsonschema_type.get("format")

        # Handle arrays (nullable types)
        if isinstance(json_type, list):
            json_type = next((t for t in json_type if t != "null"), "string")

        # Use Oracle dialect types
        if json_type == "integer":
            return oracle.NUMBER(precision=38, scale=0)

        elif json_type == "number":
            return oracle.NUMBER()

        elif json_type == "boolean":
            # Oracle doesn't have native boolean, use NUMBER(1)
            return oracle.NUMBER(precision=1, scale=0)

        elif json_type == "string":
            # Check format for specific types
            if json_format == "date":
                return oracle.DATE()
            elif json_format in ("date-time", "datetime", "time"):
                return oracle.TIMESTAMP(timezone=False)

            # String length handling
            max_length = jsonschema_type.get("maxLength", 255)
            if max_length > 4000:
                return oracle.CLOB()
            else:
                return oracle.VARCHAR2(length=max_length)

        elif json_type in ("object", "array"):
            # Store arrays as JSON in CLOB
            return oracle.CLOB()

        # Default fallback
        return oracle.VARCHAR2(length=255)

    def get_column_type(self, column_name: str, jsonschema_type: dict[str, Any]) -> Any:
        """Get SQLAlchemy column type with Oracle-specific handling.

        This method can consider column naming patterns for better type inference.
        """
        # First, get base type from JSON schema
        base_type = self.to_sql_type(jsonschema_type)

        # Apply Oracle-specific patterns if enabled
        if not self.config.get("enable_column_patterns", True):
            return base_type

        column_upper = column_name.upper()

        # ID columns
        if column_upper.endswith("_ID") or column_upper == "ID":
            return oracle.NUMBER(precision=38, scale=0)

        # Key columns
        elif column_upper.endswith("_KEY"):
            return oracle.VARCHAR2(length=255)

        # Flag/Boolean columns
        elif column_upper.endswith(("_FLG", "_FLAG", "_ENABLED", "_ACTIVE")):
            return oracle.NUMBER(precision=1, scale=0)

        # Date/Time columns
        elif any(column_upper.endswith(suffix) for suffix in ("_DATE", "_DT")):
            return oracle.DATE()
        elif any(
            column_upper.endswith(suffix)
            for suffix in ("_TIME", "_TS", "_TIMESTAMP", "_AT")
        ):
            return oracle.TIMESTAMP(timezone=False)

        # Amount/Price columns
        elif any(
            column_upper.endswith(suffix)
            for suffix in ("_AMT", "_AMOUNT", "_PRICE", "_COST")
        ):
            return oracle.NUMBER(precision=19, scale=4)

        # Percentage columns
        elif any(
            column_upper.endswith(suffix) for suffix in ("_PCT", "_PERCENT", "_RATE")
        ):
            return oracle.NUMBER(precision=5, scale=2)

        # Description/Comment columns
        elif any(
            column_upper.endswith(suffix)
            for suffix in ("_DESC", "_DESCRIPTION", "_COMMENT", "_NOTE")
        ):
            return oracle.VARCHAR2(length=4000)

        # Code columns
        elif column_upper.endswith(("_CODE", "_CD")):
            return oracle.VARCHAR2(length=50)

        # Name columns
        elif column_upper.endswith(("_NAME", "_NM")):
            return oracle.VARCHAR2(length=255)

        # Use base type from JSON schema
        return base_type

    def prepare_column_metadata(
        self, column_name: str, column_type: Any
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
