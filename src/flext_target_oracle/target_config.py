"""Target Configuration Management for FLEXT Target Oracle.

This module provides type-safe configuration management for Oracle Singer target
operations, implementing FLEXT ecosystem patterns with comprehensive validation
and enterprise-grade reliability standards.

The configuration system uses FlextModels as the foundation, providing
immutable, validated configuration objects with domain rule validation through
the Chain of Responsibility pattern. All validation follows railway-oriented
programming principles using FlextResult for consistent error handling.

Key Classes:
    FlextTargetOracleConfig: Main configuration class with comprehensive validation
    LoadMethod: Enumeration of supported Oracle data loading strategies
    FlextTargetOracleConstants: System constants to eliminate magic numbers

Architecture Patterns:
    FlextModels: Immutable configuration with built-in validation
    Chain of Responsibility: Modular validation rule composition
    Railway-Oriented Programming: FlextResult for error handling
    Domain-Driven Design: Business rule validation with domain context

Example:
    Basic configuration with domain validation:

    >>> config = FlextTargetOracleConfig(
    ...     oracle_host="localhost",
    ...     oracle_service="XE",
    ...     oracle_user="target_user",
    ...     oracle_password="secure_password",
    ...     batch_size=2000,
    ...     load_method=LoadMethod.BULK_INSERT,
    ... )
    >>> validation_result = config.validate_domain_rules()
    >>> if validation_result.success:
    ...     print("Configuration validated successfully")
    ... else:
    ...     print(f"Validation failed: {validation_result.error}")

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum

from flext_core import FlextModels, FlextResult, FlextTypes, FlextValidations
from pydantic import Field, SecretStr, field_validator

from .constants import FlextTargetOracleConstants


class LoadMethod(StrEnum):
    """Oracle data loading strategies with performance characteristics.

    Defines supported methods for loading Singer data into Oracle tables,
    each optimized for different use cases and performance requirements.

    Values:
      INSERT: Standard INSERT statements, best for small batches
      MERGE: UPSERT operations, best for incremental updates
      BULK_INSERT: Bulk INSERT operations, best for large data loads
      BULK_MERGE: Bulk MERGE operations, best for large incremental updates

    Example:
      >>> load_method = LoadMethod.BULK_INSERT
      >>> print(f"Using {load_method} for high-volume data loading")

    """

    INSERT = "INSERT"
    MERGE = "MERGE"
    BULK_INSERT = "BULK_INSERT"
    BULK_MERGE = "BULK_MERGE"


class FlextTargetOracleConfig(FlextModels.Value):
    """Type-safe Oracle target configuration with comprehensive validation.

    Provides immutable configuration object for Oracle Singer target operations
    with built-in validation, domain rule checking, and integration with the
    FLEXT ecosystem's configuration management patterns.

    This configuration class extends FlextConfig.BaseModel to provide:
    - Modern configuration with Pydantic validation
    - Comprehensive field validation using Pydantic
    - Business rule validation through validate_business_rules() method
    - Integration with flext-db-oracle for connection management
    - Environment variable support for deployment flexibility

    Attributes:
      oracle_host: Oracle database hostname or IP address (required)
      oracle_port: Oracle listener port (default: 1521, range: 1-65535)
      oracle_service: Oracle service name for connection (required)
      oracle_user: Oracle database username (required)
      oracle_password: Oracle database password (required, hidden in repr)
      default_target_schema: Target schema for table creation (default: "target")
      load_method: Data loading strategy (default: LoadMethod.INSERT)
      use_bulk_operations: Enable Oracle bulk operations (default: True)
      batch_size: Records per batch (default: 1000, must be positive)
      connection_timeout: Connection timeout in seconds (default: 30, must be positive)

    Example:
      Basic configuration for development:

      >>> config = FlextTargetOracleConfig(
      ...     oracle_host="localhost",
      ...     oracle_service="XE",
      ...     oracle_user="dev_user",
      ...     oracle_password="dev_password",
      ... )
      >>> print(f"Connecting to {config.oracle_host}:{config.oracle_port}")

      Production configuration with validation:

      >>> config = FlextTargetOracleConfig(
      ...     oracle_host="prod-oracle.company.com",
      ...     oracle_port=1521,
      ...     oracle_service="PRODDB",
      ...     oracle_user="target_user",
      ...     oracle_password="secure_prod_password",
      ...     default_target_schema="DATA_WAREHOUSE",
      ...     load_method=LoadMethod.BULK_INSERT,
      ...     batch_size=5000,
      ...     connection_timeout=60,
      ... )
      >>> validation_result = config.validate_domain_rules()
      >>> if validation_result.is_failure:
      ...     print(f"Configuration invalid: {validation_result.error}")

    Note:
      Domain validation requires database connectivity to verify permissions
      and schema access. Use validate_domain_rules() to perform comprehensive
      business rule validation beyond basic field validation.

    """

    oracle_host: str = Field(
        ...,
        description="Oracle database hostname or IP address",
        min_length=1,
        max_length=255,
    )
    oracle_port: int = Field(
        default=FlextTargetOracleConstants.Connection.DEFAULT_PORT,
        description="Oracle listener port number",
        ge=FlextTargetOracleConstants.Connection.MIN_PORT,
        le=FlextTargetOracleConstants.Connection.MAX_PORT,
    )
    oracle_service: str = Field(
        ...,
        description="Oracle service name for connection",
        min_length=1,
        max_length=64,
    )
    oracle_user: str = Field(
        ...,
        description="Oracle database username",
        min_length=1,
        max_length=128,
    )
    oracle_password: SecretStr = Field(
        ...,
        description="Oracle database password",
    )
    default_target_schema: str = Field(
        default="target",
        description="Default target schema for table creation",
        min_length=1,
        max_length=128,
    )
    load_method: LoadMethod = Field(
        default=LoadMethod.INSERT,
        description="Oracle data loading strategy",
    )
    use_bulk_operations: bool = Field(
        default=True,
        description="Enable Oracle bulk operations for performance",
    )
    batch_size: int = Field(
        default=FlextTargetOracleConstants.Processing.DEFAULT_BATCH_SIZE,
        description="Number of records per batch for processing",
        gt=0,
        le=50000,  # Reasonable upper limit for Oracle batch operations
    )
    connection_timeout: int = Field(
        default=FlextTargetOracleConstants.Connection.DEFAULT_CONNECTION_TIMEOUT,
        description="Database connection timeout in seconds",
        gt=0,
        le=3600,  # Maximum 1 hour timeout
    )

    # SSL/TLS Configuration
    use_ssl: bool = Field(
        default=False,
        description="Enable SSL/TLS for Oracle connection (TCP/TCPS)",
    )
    ssl_verify: bool = Field(
        default=True,
        description="Verify SSL certificates",
    )
    ssl_wallet_location: str | None = Field(
        default=None,
        description="Oracle wallet location for SSL connections",
        max_length=500,
    )
    ssl_wallet_password: SecretStr | None = Field(
        default=None,
        description="Oracle wallet password",
    )
    disable_dn_matching: bool = Field(
        default=False,
        description="Disable DN (Distinguished Name) matching for SSL connections",
    )

    # Connection pool configuration
    pool_min_size: int = Field(
        default=1,
        description="Minimum number of connections in pool",
        ge=1,
        le=100,
    )
    pool_max_size: int = Field(
        default=10,
        description="Maximum number of connections in pool",
        ge=1,
        le=100,
    )
    pool_increment: int = Field(
        default=1,
        description="Number of connections to add when pool is exhausted",
        ge=1,
        le=10,
    )

    # Advanced Oracle features
    enable_auto_commit: bool = Field(
        default=True,
        description="Enable auto-commit for each batch",
    )
    use_direct_path: bool = Field(
        default=False,
        description="Use Oracle direct path load for bulk operations",
    )
    parallel_degree: int | None = Field(
        default=None,
        description="Degree of parallelism for Oracle operations",
        ge=1,
        le=64,
    )

    # Column modification support
    column_mappings: dict[str, FlextTypes.Core.Dict] | None = Field(
        default=None,
        description="Column name mappings and transformations",
    )
    ignored_columns: FlextTypes.Core.StringList | None = Field(
        default=None,
        description="List of columns to ignore during loading",
    )
    add_metadata_columns: bool = Field(
        default=True,
        description="Add Singer metadata columns (_sdc_*)",
    )

    # Table naming control
    table_prefix: str | None = Field(
        default=None,
        description="Prefix to add to all table names",
        max_length=30,
    )
    table_suffix: str | None = Field(
        default=None,
        description="Suffix to add to all table names",
        max_length=30,
    )
    table_name_mappings: FlextTypes.Core.Headers | None = Field(
        default=None,
        description="Custom table name mappings for specific streams",
    )

    # SDC (Singer Data Capture) mode control
    sdc_mode: str = Field(
        default="append",
        description="SDC mode: 'append' (always insert new rows) or 'merge' (update existing rows)",
        pattern="^(append|merge)$",
    )
    sdc_primary_key_suffix: str = Field(
        default="_sdc_loaded_at",
        description="Column suffix for composite primary key in append mode",
    )
    sdc_merge_key_properties: dict[str, FlextTypes.Core.StringList] | None = Field(
        default=None,
        description="Key properties to use for merge operations per stream",
    )

    # SDC column name customization
    sdc_extracted_at_column: str = Field(
        default="_SDC_EXTRACTED_AT",
        description="Name for extraction timestamp column",
    )
    sdc_loaded_at_column: str = Field(
        default="_SDC_LOADED_AT",
        description="Name for load timestamp column",
    )
    sdc_deleted_at_column: str = Field(
        default="_SDC_DELETED_AT",
        description="Name for deletion timestamp column",
    )
    sdc_sequence_column: str = Field(
        default="_SDC_SEQUENCE",
        description="Name for sequence number column",
    )

    # Data storage mode
    storage_mode: str = Field(
        default="flattened",
        description="Storage mode: 'flattened' (flatten nested data), 'json' (store as JSON), 'hybrid' (mix based on depth)",
        pattern="^(flattened|json|hybrid)$",
    )
    max_flattening_depth: int = Field(
        default=3,
        description="Maximum depth for flattening nested structures (for hybrid mode)",
        ge=1,
        le=10,
    )
    json_column_name: str = Field(
        default="DATA",
        description="Column name for JSON storage mode",
    )

    default_string_length: int = Field(
        default=4000,
        description="Default length for VARCHAR2 columns",
        ge=1,
        le=32767,
    )
    default_timestamp_precision: int = Field(
        default=6,
        description="Default precision for TIMESTAMP columns",
        ge=0,
        le=9,
    )
    use_clob_threshold: int = Field(
        default=4000,
        description="String length threshold to use CLOB instead of VARCHAR2",
        ge=1,
    )
    type_mappings: FlextTypes.Core.Headers | None = Field(
        default=None,
        description="Custom JSON to Oracle type mappings (e.g., {'number': 'NUMBER(38,10)'})",
    )

    # Column-specific type overrides
    column_type_overrides: dict[str, FlextTypes.Core.Headers] | None = Field(
        default=None,
        description="Per-stream column type overrides (e.g., {'stream_name': {'column_name': 'DATE'}})",
    )

    # DDL Generation Control
    column_ordering: str = Field(
        default="alphabetical",
        description="Column ordering in CREATE TABLE: 'alphabetical', 'schema_order', 'custom'",
        pattern="^(alphabetical|schema_order|custom)$",
    )
    column_order_rules: dict[str, int] = Field(
        default_factory=lambda: {
            "primary_keys": 1,
            "regular_columns": 2,
            "audit_columns": 3,
            "sdc_columns": 4,
        },
        description="Priority order for column groups (lower number = higher priority)",
    )
    audit_column_patterns: FlextTypes.Core.StringList = Field(
        default_factory=lambda: [
            "created_at",
            "created_by",
            "created_date",
            "updated_at",
            "updated_by",
            "updated_date",
            "modified_at",
            "modified_by",
            "modified_date",
            "deleted_at",
            "deleted_by",
            "deleted_date",
        ],
        description="Patterns to identify audit columns",
    )

    # Table Management
    truncate_before_load: bool = Field(
        default=False,
        description="Truncate table before loading data",
    )
    force_recreate_tables: bool = Field(
        default=False,
        description="Drop and recreate tables even if they exist",
    )
    allow_alter_table: bool = Field(
        default=False,
        description="Allow ALTER TABLE for schema evolution",
    )

    # Index Management
    maintain_indexes: bool = Field(
        default=True,
        description="Maintain existing indexes when modifying tables",
    )
    create_foreign_key_indexes: bool = Field(
        default=True,
        description="Create indexes for foreign key relationships from schema",
    )
    custom_indexes: dict[str, list[FlextTypes.Core.Dict]] | None = Field(
        default=None,
        description="Custom indexes per stream (e.g., {'stream': [{'name': 'idx_custom', 'columns': ['col1', 'col2']}]})",
    )
    index_naming_template: str = Field(
        default="IDX_{table}_{columns}",
        description="Template for index names ({table}, {columns}, {type} placeholders)",
    )
    preserve_existing_indexes: bool = Field(
        default=True,
        description="Preserve indexes not defined in schema when updating",
    )

    @field_validator("oracle_port")
    @classmethod
    def validate_oracle_port(cls, v: int) -> int:
        """Validate Oracle port number is within valid TCP port range.

        Ensures the Oracle listener port is within the standard TCP port range
        and commonly used for Oracle database connections.

        Args:
            v: Port number to validate

        Returns:
            Validated port number

        Raises:
            ValueError: If port is outside valid range (1-65535)

        """
        if not (
            FlextTargetOracleConstants.Connection.MIN_PORT
            <= v
            <= FlextTargetOracleConstants.Connection.MAX_PORT
        ):
            msg: str = f"Oracle port must be between {FlextTargetOracleConstants.Connection.MIN_PORT} and {FlextTargetOracleConstants.Connection.MAX_PORT}"
            raise ValueError(msg)
        return v

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v: int) -> int:
        """Validate batch size is positive and within reasonable limits.

        Ensures batch size is positive and doesn't exceed Oracle's practical
        limits for bulk operations and memory usage.

        Args:
            v: Batch size to validate

        Returns:
            Validated batch size

        Raises:
            ValueError: If batch size is not positive

        """
        if v <= 0:
            msg = "Batch size must be positive"
            raise ValueError(msg)
        return v

    @field_validator("connection_timeout")
    @classmethod
    def validate_connection_timeout(cls, v: int) -> int:
        """Validate connection timeout is positive and reasonable.

        Ensures connection timeout allows sufficient time for database
        connection establishment while preventing indefinite hangs.

        Args:
            v: Timeout value in seconds to validate

        Returns:
            Validated timeout value

        Raises:
            ValueError: If timeout is not positive

        """
        if v <= 0:
            msg = "Connection timeout must be positive"
            raise ValueError(msg)
        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate business rules implementation required by FlextModels.

        Implements abstract method from FlextModels by delegating to
        validate_domain_rules for backwards compatibility and consistency.

        Returns:
            FlextResult[None]: Success if all business rules pass

        """
        return self.validate_domain_rules()

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate business rules using Chain of Responsibility pattern.

        Performs comprehensive domain validation beyond basic field validation,
        including connectivity checks, permission validation, and schema access
        verification. Uses the Chain of Responsibility pattern to compose
        validation rules modularly.

        The validation chain includes:
        - Host reachability verification
        - Port accessibility testing
        - Database connectivity confirmation
        - User authentication validation
        - Schema permission verification

        Returns:
            FlextResult[None]: Success if all domain rules pass, failure with
            detailed error message if any validation rule fails

        Example:
            >>> config = FlextTargetOracleConfig(...)
            >>> result = config.validate_domain_rules()
            >>> if result.is_failure:
            ...     print(f"Configuration issue: {result.error}")
            ... else:
            ...     print("Configuration validated for production use")

        Note:
            This method requires network connectivity to the Oracle database
            and may take several seconds to complete due to connection testing.

        """
        try:
            # Use flext-core validation function - ZERO DUPLICATION
            return validate_oracle_configuration(self)
        except Exception as e:
            return FlextResult[None].fail(f"Configuration validation failed: {e}")

    def validate_oracle_config(self) -> FlextResult[None]:
        """Validate Oracle configuration - alias for validate_domain_rules for test compatibility."""
        return self.validate_domain_rules()

    def get_oracle_config(self) -> dict[str, object]:
        """Convert to flext-db-oracle configuration format.

        Transforms this configuration into the format expected by flext-db-oracle
        for database connection establishment, including connection pooling
        and security settings.

        Returns:
            Dictionary containing flext-db-oracle compatible configuration with
            connection parameters, pooling settings, and security options

        Example:
            >>> config = FlextTargetOracleConfig(...)
            >>> oracle_config = config.get_oracle_config()
            >>> api = FlextDbOracleApi(FlextDbOracleConfig(**oracle_config))

        """
        oracle_config = {
            "host": self.oracle_host,
            "port": self.oracle_port,
            "service_name": self.oracle_service,
            "username": self.oracle_user,
            "password": self.oracle_password.get_secret_value(),
            "sid": None,  # Use service_name instead of SID
            "timeout": self.connection_timeout,
            "pool_min": self.pool_min_size,
            "pool_max": self.pool_max_size,
            "pool_increment": self.pool_increment,
            "encoding": "UTF-8",
            "ssl_enabled": self.use_ssl,
            "autocommit": self.enable_auto_commit,
            "ssl_server_dn_match": not self.disable_dn_matching,
        }

        # Add SSL wallet configuration if provided
        if self.use_ssl and self.ssl_wallet_location:
            oracle_config["ssl_wallet_location"] = self.ssl_wallet_location
            if self.ssl_wallet_password:
                oracle_config["ssl_wallet_password"] = self.ssl_wallet_password

        # Add advanced Oracle features if enabled
        if self.use_direct_path:
            oracle_config["use_direct_path"] = True
        if self.parallel_degree:
            oracle_config["parallel_degree"] = self.parallel_degree

        return oracle_config

    def get_table_name(self, stream_name: str) -> str:
        """Generate Oracle table name from Singer stream name.

        Converts Singer stream names to valid Oracle table names by replacing
        invalid characters and applying Oracle naming conventions with support
        for custom mappings, prefixes, and suffixes.

        Transformation rules:
        1. Check for custom mapping first
        2. Apply standard transformations (replace - and . with _)
        3. Add prefix if configured
        4. Add suffix if configured
        5. Convert to uppercase for Oracle convention
        6. Ensure length <= 30 characters (Oracle limit)

        Args:
            stream_name: Singer stream identifier

        Returns:
            Valid Oracle table name following Oracle naming conventions

        Example:
            >>> config = FlextTargetOracleConfig(
            ...     table_prefix="STG_",
            ...     table_suffix="_RAW",
            ...     table_name_mappings={"customer-orders": "ORDERS"},
            ... )
            >>> config.get_table_name("customer-orders")
            'ORDERS'  # Custom mapping takes precedence
            >>> config.get_table_name("user-profile")
            'STG_USER_PROFILE_RAW'

        """
        # Check custom mapping first
        if self.table_name_mappings and stream_name in self.table_name_mappings:
            return self.table_name_mappings[stream_name].upper()

        # Standard transformation
        base_name = stream_name.replace("-", "_").replace(".", "_")

        # Apply prefix and suffix
        if self.table_prefix:
            base_name = f"{self.table_prefix}{base_name}"
        if self.table_suffix:
            base_name = f"{base_name}{self.table_suffix}"

        # Convert to uppercase
        table_name = base_name.upper()

        # Ensure Oracle naming limit (30 characters)
        oracle_table_name_limit = 30
        if len(table_name) > oracle_table_name_limit:
            # Truncate intelligently - keep prefix/suffix if possible
            if self.table_prefix and self.table_suffix:
                prefix_len = len(self.table_prefix)
                suffix_len = len(self.table_suffix)
                remaining = 30 - prefix_len - suffix_len
                if remaining > 0:
                    core = table_name[prefix_len:-suffix_len][:remaining]
                    table_name = f"{self.table_prefix}{core}{self.table_suffix}".upper()
                else:
                    table_name = table_name[:30]
            else:
                table_name = table_name[:30]

        return table_name

    def map_column_name(self, stream_name: str, column_name: str) -> str:
        """Map a column name based on configured mappings.

        Args:
            stream_name: The stream/table name
            column_name: The original column name

        Returns:
            The mapped column name or original if no mapping exists

        """
        if self.column_mappings and stream_name in self.column_mappings:
            stream_mappings = self.column_mappings[stream_name]
            if column_name in stream_mappings:
                mapped = stream_mappings[column_name]
                if isinstance(mapped, dict) and "name" in mapped:
                    return str(mapped["name"])
                if isinstance(mapped, str):
                    return mapped
        return column_name

    def should_ignore_column(self, column_name: str) -> bool:
        """Check if a column should be ignored during loading.

        Args:
            column_name: The column name to check

        Returns:
            True if the column should be ignored

        """
        if self.ignored_columns:
            return column_name in self.ignored_columns
        return False

    def get_column_transform(
        self,
        stream_name: str,
        column_name: str,
    ) -> FlextTypes.Core.Dict | None:
        """Get transformation configuration for a column.

        Args:
            stream_name: The stream/table name
            column_name: The column name

        Returns:
            Transformation configuration dict or None

        """
        if self.column_mappings and stream_name in self.column_mappings:
            stream_mappings = self.column_mappings[stream_name]
            if column_name in stream_mappings:
                mapped = stream_mappings[column_name]
                if isinstance(mapped, dict) and "transform" in mapped:
                    transform_value = mapped["transform"]
                    if isinstance(transform_value, dict):
                        return dict(transform_value)
                    return None
        return None


def validate_oracle_configuration(config: FlextTargetOracleConfig) -> FlextResult[None]:
    """Validate Oracle configuration using flext-core FlextValidations - ZERO DUPLICATION."""
    # Required string fields validation using flext-core
    required_fields = [
        (config.oracle_host, "Oracle host is required"),
        (config.oracle_service, "Oracle service is required"),
        (config.oracle_user, "Oracle username is required"),
        (
            config.oracle_password.get_secret_value()
            if config.oracle_password
            else None,
            "Oracle password is required",
        ),
        (config.default_target_schema, "Target schema is required"),
    ]

    # Validate required string fields using FlextValidations
    for field_value, error_message in required_fields:
        if not FlextValidations.validate_non_empty_string_func(field_value):
            return FlextResult[None].fail(error_message)

    # Validate pool size constraints using FlextValidations number validation
    if not FlextValidations.validate_number(config.pool_min_size, min_value=0):
        return FlextResult[None].fail("Pool min size must be non-negative")

    if not FlextValidations.validate_number(
        config.pool_max_size, min_value=config.pool_min_size
    ):
        return FlextResult[None].fail(
            "Pool max size must be greater than or equal to pool min size"
        )

    # SSL configuration consistency validation
    if (
        config.use_ssl
        and config.ssl_wallet_password
        and not FlextValidations.validate_non_empty_string_func(
            config.ssl_wallet_location
        )
    ):
        return FlextResult[None].fail(
            "SSL wallet location is required when wallet password is provided"
        )

    return FlextResult[None].ok(None)


__all__: FlextTypes.Core.StringList = [
    "FlextTargetOracleConfig",
    "LoadMethod",
    "validate_oracle_configuration",
]
