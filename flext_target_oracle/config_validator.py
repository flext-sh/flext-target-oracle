"""
Production-ready configuration validation for Oracle Target.

This module provides comprehensive validation of configuration parameters,
environment-specific validation, and production readiness checks.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text


class ConfigurationValidator:
    """Validates Oracle target configuration for production readiness."""

    def __init__(self, config: dict[str, Any]):
        """Initialize validator with configuration."""
        self.config = config
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
        except Exception as e:
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
        if not isinstance(port, int) or port < 1 or port > 65535:
            self.errors.append(f"Invalid port number: {port}")

    def _validate_connection_parameters(self) -> None:
        """Validate connection-related parameters."""
        # Protocol validation
        protocol = self.config.get("protocol", "tcp")
        if protocol not in ["tcp", "tcps"]:
            self.errors.append(f"Invalid protocol: {protocol}. Must be 'tcp' or 'tcps'")

        # TCPS-specific validation
        if (
            protocol == "tcps"
            and self.config.get("ssl_server_dn_match")
            and not self.config.get("ssl_server_cert_dn")
        ):
            self.warnings.append(
                "ssl_server_dn_match is enabled but ssl_server_cert_dn "
                "is not specified"
            )

        # Wallet validation for Autonomous Database
        wallet_location = self.config.get("wallet_location")
        if wallet_location:
            wallet_path = Path(wallet_location)
            if not wallet_path.exists():
                self.errors.append(f"Wallet location does not exist: {wallet_location}")
            elif not wallet_path.is_dir():
                self.errors.append(
                    f"Wallet location is not a directory: {wallet_location}"
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
        elif timeout < 30:
            self.warnings.append(
                "connection_timeout < 30 seconds may cause issues with slow networks"
            )

    def _validate_performance_settings(self) -> None:
        """Validate performance-related settings."""
        # Pool settings
        pool_size = self.config.get("pool_size", 10)
        max_overflow = self.config.get("max_overflow", 20)

        if not isinstance(pool_size, int) or pool_size < 1:
            self.errors.append(f"Invalid pool_size: {pool_size}")
        elif pool_size > 50:
            self.warnings.append(
                "pool_size > 50 may consume excessive database resources"
            )

        if not isinstance(max_overflow, int) or max_overflow < 0:
            self.errors.append(f"Invalid max_overflow: {max_overflow}")

        # Batch settings
        batch_size = self.config.get("batch_size", 10000)
        if not isinstance(batch_size, int) or batch_size < 1:
            self.errors.append(f"Invalid batch_size: {batch_size}")
        elif batch_size > 50000:
            self.warnings.append("batch_size > 50000 may cause memory issues")

        # Parallel settings
        parallel_degree = self.config.get("parallel_degree", 1)
        if not isinstance(parallel_degree, int) or parallel_degree < 1:
            self.errors.append(f"Invalid parallel_degree: {parallel_degree}")
        elif parallel_degree > 1 and not self.config.get(
            "oracle_is_enterprise_edition"
        ):
            self.warnings.append(
                "parallel_degree > 1 requires Oracle Enterprise Edition"
            )

        parallel_threads = self.config.get("parallel_threads", 8)
        if not isinstance(parallel_threads, int) or parallel_threads < 1:
            self.errors.append(f"Invalid parallel_threads: {parallel_threads}")
        elif parallel_threads > 32:
            self.warnings.append("parallel_threads > 32 may cause resource contention")

        # Array size for Oracle driver
        array_size = self.config.get("array_size", 1000)
        if not isinstance(array_size, int) or array_size < 1:
            self.errors.append(f"Invalid array_size: {array_size}")

    def _validate_security_settings(self) -> None:
        """Validate security-related settings."""
        # Password validation
        password = self.config.get("password", "")
        if isinstance(password, str):
            if len(password) < 8:
                self.warnings.append("Password is shorter than 8 characters")
            if password.lower() in ["password", "oracle", "admin", "welcome"]:
                self.errors.append("Password appears to be a common weak password")

        # SSL/TLS validation
        if (
            self.config.get("protocol") == "tcps"
            and not self.config.get("ssl_server_dn_match", True)
        ):
            self.warnings.append("SSL certificate verification is disabled")

        # Authentication validation
        auth_type = self.config.get("auth_type", "basic")
        if auth_type not in ["basic", "kerberos", "external"]:
            self.errors.append(f"Invalid auth_type: {auth_type}")

    def _validate_oracle_license_settings(self) -> None:
        """Validate Oracle licensing flags for compliance."""
        is_ee = self.config.get("oracle_is_enterprise_edition", False)

        # Features that require Enterprise Edition
        ee_features = {
            "parallel_degree": (lambda x: x > 1, "Parallel processing > 1"),
            "use_parallel_dml": (lambda x: x, "Parallel DML"),
            "enable_parallel_ddl": (lambda x: x, "Parallel DDL"),
            "enable_parallel_query": (lambda x: x, "Parallel Query"),
        }

        for config_key, (check_func, feature_name) in ee_features.items():
            if check_func(self.config.get(config_key, False)) and not is_ee:
                self.warnings.append(
                    f"{feature_name} requires Oracle Enterprise Edition license"
                )

        # Features that require specific options
        option_features = {
            "oracle_has_partitioning_option": {
                "enable_partitioning": "Table partitioning",
            },
            "oracle_has_compression_option": {
                "enable_compression": "Advanced compression",
                "compression_type": (
                    lambda x: x in ["advanced", "hybrid", "archive"],
                    "Advanced compression types",
                ),
            },
            "oracle_has_inmemory_option": {
                "use_inmemory": "In-Memory column store",
            },
            "oracle_has_advanced_security_option": {
                # Would include TDE, VPD, etc. if implemented
            },
        }

        for option_flag, features in option_features.items():
            has_option = self.config.get(option_flag, False)

            for config_key, feature_name in features.items():
                if isinstance(feature_name, tuple):
                    check_func, feature_name = feature_name
                    if check_func(self.config.get(config_key)) and not has_option:
                        self.warnings.append(
                            f"{feature_name} requires {option_flag} license"
                        )
                else:
                    if self.config.get(config_key, False) and not has_option:
                        self.warnings.append(
                            f"{feature_name} requires {option_flag} license"
                        )

    def _validate_production_readiness(self) -> None:
        """Validate configuration for production readiness."""
        # Logging configuration
        log_level = self.config.get("log_level", "INFO")
        if log_level == "DEBUG":
            self.warnings.append("DEBUG log level should not be used in production")

        if self.config.get("log_sql_statements", False):
            self.warnings.append(
                "SQL statement logging should be disabled in production for performance"
            )

        # Error handling
        if self.config.get("fail_fast", False):
            self.recommendations.append(
                "Consider setting fail_fast=False for production resilience"
            )

        max_retries = self.config.get("max_retries", 5)
        if max_retries < 3:
            self.recommendations.append(
                "Consider increasing max_retries for production resilience"
            )

        # Performance monitoring
        if not self.config.get("log_metrics", True):
            self.recommendations.append(
                "Enable metrics logging for production monitoring"
            )

        # Resource limits
        max_memory = self.config.get("max_memory_usage_mb", 1024)
        if max_memory < 512:
            self.warnings.append("max_memory_usage_mb < 512MB may limit performance")

        # Connection pooling
        if self.config.get("pool_pre_ping", True) is False:
            self.recommendations.append(
                "Enable pool_pre_ping for production reliability"
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
            # Build connection URL
            url = self._build_connection_url()
            engine = create_engine(url, pool_pre_ping=True)

            with engine.connect() as conn:
                # Test basic connectivity
                result = conn.execute(text("SELECT 1 FROM DUAL"))
                if result.scalar() == 1:
                    results["connection_test"] = True

                # Get Oracle version and edition
                version_result = conn.execute(
                    text(
                        "SELECT banner FROM v$version "
                        "WHERE banner LIKE 'Oracle Database%'"
                    )
                )
                version_row = version_result.fetchone()
                if version_row:
                    results["database_version"] = version_row[0]
                    results["edition_info"]["is_enterprise"] = (
                        "Enterprise Edition" in version_row[0]
                    )

                # Check for specific features
                try:
                    # Check partitioning
                    conn.execute(
                        text("SELECT COUNT(*) FROM user_part_tables WHERE ROWNUM <= 1")
                    )
                    results["edition_info"]["has_partitioning"] = True
                except Exception:
                    results["edition_info"]["has_partitioning"] = False

                # Check for Exadata/Autonomous
                try:
                    platform_result = conn.execute(
                        text("""
                        SELECT banner FROM v$version
                        WHERE banner LIKE '%Exadata%'
                        OR banner LIKE '%Autonomous%'
                        OR banner LIKE '%Cloud%'
                    """)
                    )
                    platform_row = platform_result.fetchone()
                    if platform_row:
                        results["platform_info"]["type"] = "Exadata/Autonomous/Cloud"
                        results["platform_info"]["banner"] = platform_row[0]
                        results["edition_info"]["supports_hcc"] = True
                    else:
                        results["platform_info"]["type"] = "Standard"
                        results["edition_info"]["supports_hcc"] = False
                except Exception:
                    results["platform_info"]["type"] = "Unknown"

                # Check database size and capabilities
                try:
                    size_result = conn.execute(
                        text("""
                        SELECT ROUND(SUM(bytes)/1024/1024/1024, 2) as size_gb
                        FROM dba_data_files
                    """)
                    )
                    size_row = size_result.fetchone()
                    if size_row:
                        results["platform_info"]["size_gb"] = size_row[0]
                except Exception:
                    # Might not have DBA privileges
                    pass

        except Exception as e:
            self.errors.append(f"Connection test failed: {e}")
            return results

        return results

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
        else:
            return f"oracle+oracledb://{username}:{password}@{host}:{port}/{database}"

    def _get_performance_recommendations(self) -> list[str]:
        """Generate performance recommendations based on configuration."""
        recommendations = []

        # Connection pool optimization
        pool_size = self.config.get("pool_size", 10)
        batch_size = self.config.get("batch_size", 10000)

        if pool_size < batch_size / 5000:
            recommendations.append(
                "Consider increasing pool_size for high-volume batches"
            )

        # Parallel processing recommendations
        if self.config.get("oracle_is_enterprise_edition", False):
            parallel_degree = self.config.get("parallel_degree", 1)
            if parallel_degree == 1:
                recommendations.append(
                    "Consider enabling parallel processing for better performance"
                )

        # Compression recommendations
        if (
            self.config.get("oracle_has_compression_option", False)
            and not self.config.get("enable_compression", False)
        ):
            recommendations.append(
                "Consider enabling compression for storage efficiency"
            )

        # Batch size optimization
        if batch_size < 5000:
            recommendations.append(
                "Consider increasing batch_size for better throughput"
            )
        elif batch_size > 25000:
            recommendations.append(
                "Consider reducing batch_size to avoid memory issues"
            )

        # Array size optimization
        array_size = self.config.get("array_size", 1000)
        if array_size < 500:
            recommendations.append(
                "Consider increasing array_size for better network efficiency"
            )

        # WAN optimization
        if (
            self.config.get("protocol") == "tcps"
            or "cloud" in self.config.get("host", "").lower()
        ):
            recommendations.append(
                "Consider WAN optimization settings (SDU/TDU) "
                "for cloud/remote connections"
            )

        return recommendations

    def validate_environment_variables(self) -> dict[str, Any]:
        """Validate environment-based configuration."""
        results = {
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
            "wallet_location"
        ):
            results["env_recommendations"].append(
                "Set TNS_ADMIN environment variable for wallet location"
            )

        if "NLS_LANG" not in results["env_vars_found"]:
            results["env_recommendations"].append(
                "Set NLS_LANG for consistent character encoding"
            )

        return results

    def generate_production_config_template(self) -> dict[str, Any]:
        """Generate a production-ready configuration template."""
        template = {
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

        return template
