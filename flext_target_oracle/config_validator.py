"""Production-ready configuration validation for Oracle Target.

This module provides comprehensive validation of configuration parameters,
environment-specific validation, and production readiness checks.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from sqlalchemy import create_engine, text

if TYPE_CHECKING:
    import logging

# Configuration constants
MAX_PORT_NUMBER = 65535
MIN_CONNECTION_TIMEOUT = 30
MAX_POOL_SIZE = 50
MAX_BATCH_SIZE = 50000
MAX_PARALLEL_THREADS = 32
MIN_PASSWORD_LENGTH = 8
MIN_RETRIES = 3
MIN_MEMORY_MB = 512
MIN_BATCH_SIZE_PERF = 5000
MAX_BATCH_SIZE_PERF = 25000
MIN_ARRAY_SIZE_PERF = 500


class ConfigurationValidator:
    """Validates Oracle target configuration for production readiness."""

    def __init__(
        self, config: dict[str, Any], logger: logging.Logger | None = None,
    ) -> None:
        """Initialize validator with configuration."""
        self.config = config
        self.logger = logger
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.recommendations: list[str] = []

    def validate_all(self) -> dict[str, Any]:
        """Perform comprehensive configuration validation."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": [],
            "connection_test": False,
            "edition_info": {},
            "performance_recommendations": [],
        }

        # Basic configuration validation
        self._validate_required_fields()
        self._validate_connection_parameters()
        self._validate_performance_settings()
        self._validate_security_settings()
        self._validate_oracle_license_settings()
        self._validate_production_readiness()

        # Test actual connection if possible
        try:
            connection_results = self._test_connection()
            results.update(connection_results)
        except (OSError, ValueError, RuntimeError) as e:
            self.errors.append(f"Connection test failed: {e}")

        # Compile results
        results["errors"] = self.errors
        results["warnings"] = self.warnings
        results["recommendations"] = self.recommendations
        results["valid"] = len(self.errors) == 0

        if results["valid"]:
            results["performance_recommendations"] = (
                self._get_performance_recommendations()
            )

        return results

    def _validate_required_fields(self) -> None:
        """Validate required configuration fields."""
        required_fields = ["host", "username", "password"]

        for field in required_fields:
            if not self.config.get(field):
                self.errors.append(f"Required field '{field}' is missing or empty")

        # Either service_name or database must be provided
        if not self.config.get("service_name") and not self.config.get("database"):
            self.errors.append("Either 'service_name' or 'database' must be provided")

        # Validate port
        port = self.config.get("port", 1521)
        if not isinstance(port, int) or port < 1 or port > MAX_PORT_NUMBER:
            self.errors.append(f"Invalid port number: {port}")

    def _validate_connection_parameters(self) -> None:
        """Validate connection-related parameters."""
        # Protocol validation
        protocol = self.config.get("protocol", "tcp")
        if protocol not in {"tcp", "tcps"}:
            self.errors.append(f"Invalid protocol: {protocol}. Must be 'tcp' or 'tcps'")

        # TCPS-specific validation
        if (
            protocol == "tcps"
            and self.config.get("ssl_server_dn_match")
            and not self.config.get("ssl_server_cert_dn")
        ):
            self.warnings.append(
                "ssl_server_dn_match is enabled but ssl_server_cert_dn "
                "is not specified",
            )

        # Wallet validation for Autonomous Database
        wallet_location = self.config.get("wallet_location")
        if wallet_location:
            wallet_path = Path(wallet_location)
            if not wallet_path.exists():
                self.errors.append(f"Wallet location does not exist: {wallet_location}")
            elif not wallet_path.is_dir():
                self.errors.append(
                    f"Wallet location is not a directory: {wallet_location}",
                )
            else:
                # Check for required wallet files
                required_files = ["cwallet.sso", "tnsnames.ora", "sqlnet.ora"]
                missing_files = [
                    f for f in required_files if not (wallet_path / f).exists()
                ]
                if missing_files:
                    self.warnings.append(f"Missing wallet files: {missing_files}")

        # Connection timeout validation
        timeout = self.config.get("connection_timeout", 60)
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            self.errors.append(f"Invalid connection_timeout: {timeout}")
        elif timeout < MIN_CONNECTION_TIMEOUT:
            self.warnings.append(
                "connection_timeout < 30 seconds may cause issues with slow networks",
            )

    def _validate_performance_settings(self) -> None:
        """Validate performance-related settings."""
        self._validate_pool_settings()
        self._validate_batch_settings()
        self._validate_parallel_settings()
        self._validate_array_settings()

    def _validate_pool_settings(self) -> None:
        """Validate connection pool settings."""
        pool_size = self.config.get("pool_size", 10)
        max_overflow = self.config.get("max_overflow", 20)

        if not isinstance(pool_size, int) or pool_size < 1:
            self.errors.append(f"Invalid pool_size: {pool_size}")
        elif pool_size > MAX_POOL_SIZE:
            self.warnings.append(
                "pool_size > 50 may consume excessive database resources",
            )

        if not isinstance(max_overflow, int) or max_overflow < 0:
            self.errors.append(f"Invalid max_overflow: {max_overflow}")

    def _validate_batch_settings(self) -> None:
        """Validate batch processing settings."""
        batch_size = self.config.get("batch_size", 10000)
        if not isinstance(batch_size, int) or batch_size < 1:
            self.errors.append(f"Invalid batch_size: {batch_size}")
        elif batch_size > MAX_BATCH_SIZE:
            self.warnings.append("batch_size > 50000 may cause memory issues")

    def _validate_parallel_settings(self) -> None:
        """Validate parallel processing settings."""
        parallel_degree = self.config.get("parallel_degree", 1)
        if not isinstance(parallel_degree, int) or parallel_degree < 1:
            self.errors.append(f"Invalid parallel_degree: {parallel_degree}")
        elif parallel_degree > 1 and not self.config.get(
            "oracle_is_enterprise_edition",
        ):
            self.warnings.append(
                "parallel_degree > 1 requires Oracle Enterprise Edition",
            )

        parallel_threads = self.config.get("parallel_threads", 8)
        if not isinstance(parallel_threads, int) or parallel_threads < 1:
            self.errors.append(f"Invalid parallel_threads: {parallel_threads}")
        elif parallel_threads > MAX_PARALLEL_THREADS:
            self.warnings.append("parallel_threads > 32 may cause resource contention")

    def _validate_array_settings(self) -> None:
        """Validate Oracle array size settings."""
        array_size = self.config.get("array_size", 1000)
        if not isinstance(array_size, int) or array_size < 1:
            self.errors.append(f"Invalid array_size: {array_size}")

    def _validate_security_settings(self) -> None:
        """Validate security-related settings."""
        # Password validation
        password = self.config.get("password", "")
        if isinstance(password, str):
            if len(password) < MIN_PASSWORD_LENGTH:
                self.warnings.append("Password is shorter than 8 characters")
            if password.lower() in {"password", "oracle", "admin", "welcome"}:
                self.errors.append("Password appears to be a common weak password")

        # SSL/TLS validation
        if self.config.get("protocol") == "tcps" and not self.config.get(
            "ssl_server_dn_match", True,
        ):
            self.warnings.append("SSL certificate verification is disabled")

        # Authentication validation
        auth_type = self.config.get("auth_type", "basic")
        if auth_type not in {"basic", "kerberos", "external"}:
            self.errors.append(f"Invalid auth_type: {auth_type}")

    def _validate_oracle_license_settings(self) -> None:
        """Validate Oracle licensing flags for compliance."""
        self._validate_enterprise_edition_features()
        self._validate_option_based_features()

    def _validate_enterprise_edition_features(self) -> None:
        """Validate features that require Enterprise Edition."""
        is_ee = self.config.get("oracle_is_enterprise_edition", False)

        if is_ee:
            return

        # Check parallel processing
        parallel_degree = self.config.get("parallel_degree", 1)
        if parallel_degree > 1:
            self.warnings.append(
                "Parallel processing > 1 requires Oracle Enterprise Edition license",
            )

        # Check parallel features
        parallel_features = {
            "use_parallel_dml": "Parallel DML",
            "enable_parallel_ddl": "Parallel DDL",
            "enable_parallel_query": "Parallel Query",
        }

        for config_key, feature_name in parallel_features.items():
            if self.config.get(config_key, False):
                self.warnings.append(
                    f"{feature_name} requires Oracle Enterprise Edition license",
                )

    def _validate_option_based_features(self) -> None:
        """Validate features that require specific Oracle options."""
        self._validate_partitioning_option()
        self._validate_compression_option()
        self._validate_inmemory_option()

    def _validate_partitioning_option(self) -> None:
        """Validate partitioning option features."""
        has_option = self.config.get("oracle_has_partitioning_option", False)
        if self.config.get("enable_partitioning", False) and not has_option:
            self.warnings.append(
                "Table partitioning requires oracle_has_partitioning_option license",
            )

    def _validate_compression_option(self) -> None:
        """Validate compression option features."""
        has_option = self.config.get("oracle_has_compression_option", False)

        if self.config.get("enable_compression", False) and not has_option:
            self.warnings.append(
                "Advanced compression requires oracle_has_compression_option license",
            )

        compression_type = self.config.get("compression_type", "")
        if (compression_type in {"advanced", "hybrid", "archive"}
            and not has_option):
            self.warnings.append(
                "Advanced compression types require "
                "oracle_has_compression_option license",
            )

    def _validate_inmemory_option(self) -> None:
        """Validate in-memory option features."""
        has_option = self.config.get("oracle_has_inmemory_option", False)
        if self.config.get("use_inmemory", False) and not has_option:
            self.warnings.append(
                "In-Memory column store requires oracle_has_inmemory_option license",
            )

    def _validate_production_readiness(self) -> None:
        """Validate configuration for production readiness."""
        # Logging configuration
        log_level = self.config.get("log_level", "INFO")
        if log_level == "DEBUG":
            self.warnings.append("DEBUG log level should not be used in production")

        if self.config.get("log_sql_statements", False):
            self.warnings.append(
                "SQL statement logging should be disabled in production for "
                "performance",
            )

        # Error handling
        if self.config.get("fail_fast", False):
            self.recommendations.append(
                "Consider setting fail_fast=False for production resilience",
            )

        max_retries = self.config.get("max_retries", 5)
        if max_retries < MIN_RETRIES:
            self.recommendations.append(
                "Consider increasing max_retries for production resilience",
            )

        # Performance monitoring
        if not self.config.get("log_metrics", True):
            self.recommendations.append(
                "Enable metrics logging for production monitoring",
            )

        # Resource limits
        max_memory = self.config.get("max_memory_usage_mb", 1024)
        if max_memory < MIN_MEMORY_MB:
            self.warnings.append("max_memory_usage_mb < 512MB may limit performance")

        # Connection pooling
        if self.config.get("pool_pre_ping", True) is False:
            self.recommendations.append(
                "Enable pool_pre_ping for production reliability",
            )

    def _test_connection(self) -> dict[str, Any]:
        """Test actual database connection and gather environment info."""
        results = {
            "connection_test": False,
            "edition_info": {},
            "database_version": None,
            "platform_info": {},
        }

        try:
            url = self._build_connection_url()
            engine = create_engine(url, pool_pre_ping=True)

            with engine.connect() as conn:
                self._test_basic_connectivity(conn, results)
                self._detect_oracle_version_and_edition(conn, results)
                self._check_oracle_features(conn, results)
                self._detect_platform_type(conn, results)
                self._check_database_size(conn, results)

        except (OSError, ValueError, RuntimeError) as e:
            self.errors.append(f"Connection test failed: {e}")

        return results

    def _test_basic_connectivity(
        self, conn: object, results: dict[str, Any],
    ) -> None:
        """Test basic database connectivity."""
        result = conn.execute(text("SELECT 1 FROM DUAL"))
        if result.scalar() == 1:
            results["connection_test"] = True

    def _detect_oracle_version_and_edition(
        self, conn: object, results: dict[str, Any],
    ) -> None:
        """Detect Oracle database version and edition."""
        version_result = conn.execute(
            text(
                "SELECT banner FROM v$version "
                "WHERE banner LIKE 'Oracle Database%'",
            ),
        )
        version_row = version_result.fetchone()
        if version_row:
            version_str = str(version_row[0])
            results["database_version"] = version_str
            edition_info = results["edition_info"]
            if isinstance(edition_info, dict):
                edition_info["is_enterprise"] = (
                    "Enterprise Edition" in version_str
                )

    def _check_oracle_features(
        self, conn: object, results: dict[str, Any],
    ) -> None:
        """Check for specific Oracle features availability."""
        try:
            conn.execute(
                text("SELECT COUNT(*) FROM user_part_tables WHERE ROWNUM <= 1"),
            )
            edition_info = results["edition_info"]
            if isinstance(edition_info, dict):
                edition_info["has_partitioning"] = True
        except (OSError, ValueError, RuntimeError) as e:
            edition_info = results["edition_info"]
            if isinstance(edition_info, dict):
                edition_info["has_partitioning"] = False
            if self.logger:
                self.logger.debug(
                    "Partitioning check failed (normal for SE): %s", e,
                )

    def _detect_platform_type(
        self, conn: object, results: dict[str, Any],
    ) -> None:
        """Detect Oracle platform type (Exadata/Autonomous/Cloud)."""
        try:
            platform_result = conn.execute(
                text(
                    """
                SELECT banner FROM v$version
                WHERE banner LIKE '%Exadata%'
                OR banner LIKE '%Autonomous%'
                OR banner LIKE '%Cloud%'
            """,
                ),
            )
            platform_row = platform_result.fetchone()
            if platform_row:
                platform_info = results["platform_info"]
                if isinstance(platform_info, dict):
                    platform_info["type"] = "Exadata/Autonomous/Cloud"
                    platform_info["banner"] = str(platform_row[0])
                edition_info = results["edition_info"]
                if isinstance(edition_info, dict):
                    edition_info["supports_hcc"] = True
            else:
                platform_info = results["platform_info"]
                if isinstance(platform_info, dict):
                    platform_info["type"] = "Standard"
                edition_info = results["edition_info"]
                if isinstance(edition_info, dict):
                    edition_info["supports_hcc"] = False
        except (OSError, ValueError, RuntimeError) as e:
            platform_info = results["platform_info"]
            if isinstance(platform_info, dict):
                platform_info["type"] = "Unknown"
            if self.logger:
                self.logger.debug("Platform detection failed: %s", e)

    def _check_database_size(
        self, conn: object, results: dict[str, Any],
    ) -> None:
        """Check database size and capabilities."""
        try:
            size_result = conn.execute(
                text(
                    """
                SELECT ROUND(SUM(bytes)/1024/1024/1024, 2) as size_gb
                FROM dba_data_files
            """,
                ),
            )
            size_row = size_result.fetchone()
            if size_row:
                platform_info = results["platform_info"]
                if isinstance(platform_info, dict):
                    platform_info["size_gb"] = (
                        float(size_row[0]) if size_row[0] is not None else 0.0
                    )
        except (OSError, ValueError, RuntimeError) as e:
            if self.logger:
                self.logger.debug(
                    "Database size check failed (may need DBA privileges): %s",
                    e,
                )

    def _build_connection_url(self) -> str:
        """Build SQLAlchemy connection URL for testing."""
        username = self.config["username"]
        password = str(self.config["password"])
        host = self.config["host"]
        port = self.config.get("port", 1521)

        if self.config.get("service_name"):
            database = self.config["service_name"]
        else:
            database = self.config.get("database", "XE")

        if self.config.get("protocol") == "tcps":
            # For TCPS, use connect_args approach
            return "oracle+oracledb://@"
        return f"oracle+oracledb://{username}:{password}@{host}:{port}/{database}"

    def _get_performance_recommendations(self) -> list[str]:
        """Generate performance recommendations based on configuration."""
        recommendations = []

        # Connection pool optimization
        pool_size = self.config.get("pool_size", 10)
        batch_size = self.config.get("batch_size", 10000)

        if pool_size < batch_size / 5000:
            recommendations.append(
                "Consider increasing pool_size for high-volume batches",
            )

        # Parallel processing recommendations
        if self.config.get("oracle_is_enterprise_edition", False):
            parallel_degree = self.config.get("parallel_degree", 1)
            if parallel_degree == 1:
                recommendations.append(
                    "Consider enabling parallel processing for better performance",
                )

        # Compression recommendations
        if self.config.get(
            "oracle_has_compression_option", False,
        ) and not self.config.get("enable_compression", False):
            recommendations.append(
                "Consider enabling compression for storage efficiency",
            )

        # Batch size optimization
        if batch_size < MIN_BATCH_SIZE_PERF:
            recommendations.append(
                "Consider increasing batch_size for better throughput",
            )
        elif batch_size > MAX_BATCH_SIZE_PERF:
            recommendations.append(
                "Consider reducing batch_size to avoid memory issues",
            )

        # Array size optimization
        array_size = self.config.get("array_size", 1000)
        if array_size < MIN_ARRAY_SIZE_PERF:
            recommendations.append(
                "Consider increasing array_size for better network efficiency",
            )

        # WAN optimization
        if (
            self.config.get("protocol") == "tcps"
            or "cloud" in self.config.get("host", "").lower()
        ):
            recommendations.append(
                "Consider WAN optimization settings (SDU/TDU) "
                "for cloud/remote connections",
            )

        return recommendations

    def validate_environment_variables(self) -> dict[str, Any]:
        """Validate environment-based configuration."""
        results: dict[str, Any] = {
            "env_vars_found": [],
            "env_vars_missing": [],
            "env_recommendations": [],
        }

        # Check for common Oracle environment variables
        oracle_env_vars = [
            "ORACLE_HOME",
            "ORACLE_SID",
            "TNS_ADMIN",
            "NLS_LANG",
            "ORA_TZFILE",
        ]

        for var in oracle_env_vars:
            if os.getenv(var):
                results["env_vars_found"].append(var)
            else:
                results["env_vars_missing"].append(var)

        # Environment-specific recommendations
        if "TNS_ADMIN" not in results["env_vars_found"] and self.config.get(
            "wallet_location",
        ):
            results["env_recommendations"].append(
                "Set TNS_ADMIN environment variable for wallet location",
            )

        if "NLS_LANG" not in results["env_vars_found"]:
            results["env_recommendations"].append(
                "Set NLS_LANG for consistent character encoding",
            )

        return results

    def generate_production_config_template(self) -> dict[str, Any]:
        """Generate a production-ready configuration template."""
        return {
            # Connection settings
            "host": "your-oracle-host",
            "port": 1521,
            "service_name": "your-service-name",
            "username": "your-username",
            "password": "your-secure-password",
            "protocol": "tcps",  # Use encrypted connections
            # Performance settings
            "batch_size": 10000,
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "parallel_threads": 8,
            "array_size": 1000,
            "prefetch_rows": 100,
            # Oracle Enterprise Edition features (set based on your licenses)
            "oracle_is_enterprise_edition": False,
            "oracle_has_partitioning_option": False,
            "oracle_has_compression_option": False,
            "oracle_has_inmemory_option": False,
            "oracle_has_advanced_security_option": False,
            # Production settings
            "load_method": "upsert",
            "max_retries": 5,
            "retry_delay": 1.0,
            "retry_backoff": 2.0,
            "fail_fast": False,
            "log_level": "INFO",
            "log_sql_statements": False,
            "log_metrics": True,
            "validate_records": True,
            # Optimization settings
            "use_bulk_operations": True,
            "use_merge_statements": True,
            "gather_statistics": True,
            "create_table_indexes": True,
            "enable_result_cache": True,
            # Resource management
            "max_memory_usage_mb": 1024,
            "connection_timeout": 60,
            "varchar_max_length": 4000,
            "number_precision": 38,
            "number_scale": 10,
        }
