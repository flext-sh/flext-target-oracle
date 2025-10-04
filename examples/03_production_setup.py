#!/usr/bin/env python3
"""Production Setup Example - Enterprise-Grade Oracle Target Configuration.

This example demonstrates production-ready configuration and deployment patterns
for FLEXT Target Oracle, including comprehensive error handling, monitoring,
security considerations, and performance optimization.

"""

import datetime
import logging
import os
import signal
import sys
import time
from datetime import UTC
from typing import cast

from flext_core import FlextLogger, FlextResult, FlextTypes
from pydantic import SecretStr

from flext_target_oracle import FlextTargetOracle, FlextTargetOracleConfig, LoadMethod

# Configure production-grade logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("flext_target_oracle.log")],
)

logger = FlextLogger(__name__)


class ProductionConfig:
    """Production configuration management with environment variables."""

    @staticmethod
    def create_from_environment() -> FlextTargetOracleConfig:
        """Create production configuration from environment variables.

        Returns:
            FlextTargetOracleConfig: Production-ready configuration

        Raises:
            ValueError: If required environment variables are missing

        Environment Variables:
            ORACLE_HOST: Oracle database hostname (required)
            ORACLE_PORT: Oracle database port (default: 1521)
            ORACLE_SERVICE: Oracle service name (required)
            ORACLE_USER: Oracle username (required)
            ORACLE_PASSWORD: Oracle password (required)
            DEFAULT_TARGET_SCHEMA: Default schema (default: ENTERPRISE_DW)
            BATCH_SIZE: Batch size for processing (default: 5000)
            CONNECTION_TIMEOUT: Connection timeout (default: 60)
            LOAD_METHOD: Loading method (default: BULK_INSERT)

        """
        logger.info("Creating production configuration from environment")

        # Required parameters
        oracle_host = os.getenv("ORACLE_HOST")
        oracle_service = os.getenv("ORACLE_SERVICE")
        oracle_user = os.getenv("ORACLE_USER")
        oracle_password = os.getenv("ORACLE_PASSWORD")

        if not all([oracle_host, oracle_service, oracle_user, oracle_password]):
            missing = [
                var
                for var, val in [
                    ("ORACLE_HOST", oracle_host),
                    ("ORACLE_SERVICE", oracle_service),
                    ("ORACLE_USER", oracle_user),
                    ("ORACLE_PASSWORD", oracle_password),
                ]
                if not val
            ]
            msg = f"Missing required environment variables: {', '.join(missing)}"
            raise ValueError(msg)

        # Type guards to help MyPy understand these are non-None after validation
        if oracle_host is None:
            msg = "ORACLE_HOST environment variable is required"
            raise ValueError(msg)
        if oracle_service is None:
            msg = "ORACLE_SERVICE environment variable is required"
            raise ValueError(msg)
        if oracle_user is None:
            msg = "ORACLE_USER environment variable is required"
            raise ValueError(msg)
        if oracle_password is None:
            msg = "ORACLE_PASSWORD environment variable is required"
            raise ValueError(msg)

        # Optional parameters with production defaults
        oracle_port = int(os.getenv("ORACLE_PORT", "1521"))
        default_target_schema = os.getenv("DEFAULT_TARGET_SCHEMA", "ENTERPRISE_DW")
        batch_size = int(os.getenv("BATCH_SIZE", "5000"))
        connection_timeout = int(os.getenv("CONNECTION_TIMEOUT", "60"))

        # Parse load method
        load_method_str = os.getenv("LOAD_METHOD", "BULK_INSERT").upper()
        load_method = getattr(LoadMethod, load_method_str, LoadMethod.BULK_INSERT)

        config = FlextTargetOracleConfig(
            oracle_host=oracle_host,
            oracle_port=oracle_port,
            oracle_service=oracle_service,
            oracle_user=oracle_user,
            oracle_password=SecretStr(oracle_password),
            default_target_schema=default_target_schema,
            load_method=load_method,
            batch_size=batch_size,
            use_bulk_operations=True,
            connection_timeout=connection_timeout,
        )

        logger.info(
            "Production configuration created: %s:%s/%s",
            oracle_host,
            oracle_port,
            oracle_service,
        )
        logger.info(
            "Target schema: %s, Batch size: %s",
            default_target_schema,
            batch_size,
        )
        logger.info(
            "Load method: %s, Connection timeout: %ss",
            load_method,
            connection_timeout,
        )

        return config


class ProductionTargetManager:
    """Production-grade target manager with comprehensive error handling."""

    def __init__(self, config: FlextTargetOracleConfig) -> None:
        """Initialize production target manager.

        Args:
            config: Validated Oracle target configuration

        """
        self.config = config
        self.target: FlextTargetOracle | None = None
        self.shutdown_requested = False

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum: int, _frame: object) -> None:
        """Handle shutdown signals gracefully."""
        logger.info("Received signal %d, initiating graceful shutdown", signum)
        self.shutdown_requested = True

    def initialize(self) -> FlextResult[None]:
        """Initialize target with comprehensive validation.

        Returns:
            FlextResult[None]: Success if initialization complete, failure with error details

        """
        logger.info("Initializing production Oracle target")

        try:
            # Step 1: Validate configuration domain rules
            logger.info("Validating configuration domain rules")
            # Domain validation is handled during config creation with Pydantic validators
            validation_result = FlextResult[None].ok(None)
            if validation_result.is_failure:
                return FlextResult[None].fail(
                    f"Configuration validation failed: {validation_result.error}",
                )

            # Step 2: Initialize target
            logger.info("Creating Oracle target instance")
            self.target = FlextTargetOracle(self.config)

            # Step 3: Test connectivity
            logger.info("Testing Oracle database connectivity")
            connection_result = self.target.test_connection()
            if connection_result.is_failure:
                return FlextResult[None].fail("Oracle connectivity test failed")

            logger.info("Production target initialized successfully")
            return FlextResult[None].ok(None)

        except Exception as e:
            logger.exception("Failed to initialize production target")
            return FlextResult[None].fail(f"Initialization error: {e}")

    def process_singer_stream(
        self,
        messages: FlextTypes.List,
    ) -> FlextResult[FlextTypes.Dict]:
        """Process complete Singer message stream with comprehensive error handling.

        Args:
            messages: List of Singer messages (SCHEMA, RECORD, STATE)

        Returns:
            FlextResult with processing statistics and status

        """
        if not self.target:
            return FlextResult[FlextTypes.Dict].fail("Target not initialized")

        logger.info("Processing Singer stream with %d messages", len(messages))

        stats: FlextTypes.Dict = {
            "messages_processed": 0,
            "schemas_processed": 0,
            "records_processed": 0,
            "states_processed": 0,
            "errors_encountered": 0,
            "processing_start_time": 0.0,
            "processing_end_time": 0.0,
        }

        stats["processing_start_time"] = time.time()

        try:
            for i, message in enumerate(messages):
                # Check for shutdown signal
                if self.shutdown_requested:
                    logger.info("Shutdown requested, stopping message processing")
                    break

                message_type = (
                    message.get("type", "UNKNOWN")
                    if isinstance(message, dict)
                    else "UNKNOWN"
                )
                logger.debug(
                    "Processing message %d/%d: %s",
                    i + 1,
                    len(messages),
                    message_type,
                )

                # Process message with error handling
                if not self.target:
                    return FlextResult[FlextTypes.Dict].fail("Target not initialized")
                # Type assertion since we checked above that target is not None
                assert self.target is not None
                result = self.target.process_singer_message(
                    message if isinstance(message, dict) else {}
                )

                if result.success:
                    # Update counters (values are already int, just increment)
                    messages_processed = stats["messages_processed"]
                    if isinstance(messages_processed, int):
                        stats["messages_processed"] = messages_processed + 1

                    # Update type-specific counters
                    if message_type == "SCHEMA":
                        schemas_processed = stats["schemas_processed"]
                        if isinstance(schemas_processed, int):
                            stats["schemas_processed"] = schemas_processed + 1
                    elif message_type == "RECORD":
                        records_processed = stats["records_processed"]
                        if isinstance(records_processed, int):
                            stats["records_processed"] = records_processed + 1
                    elif message_type == "STATE":
                        states_processed = stats["states_processed"]
                        if isinstance(states_processed, int):
                            stats["states_processed"] = states_processed + 1

                else:
                    errors_encountered = stats["errors_encountered"]
                    if isinstance(errors_encountered, int):
                        stats["errors_encountered"] = errors_encountered + 1
                    logger.error(
                        "Message %d processing failed: %s",
                        i + 1,
                        result.error,
                    )

                    # In production, you might want to decide whether to continue or stop
                    # For this example, we continue processing

                # Progress logging for long streams
                if (i + 1) % 1000 == 0:
                    logger.info("Processed %d/%d messages", i + 1, len(messages))

            # Finalize target
            logger.info("Finalizing target operations")
            finalize_result = self.target.finalize()

            if finalize_result.success:
                # Merge finalization stats
                final_stats = finalize_result.data
                if isinstance(final_stats, dict):
                    # Cast to ensure type compatibility
                    final_stats_typed = dict(final_stats)
                    stats.update(final_stats_typed)
                logger.info("Target finalization completed successfully")
            else:
                logger.error("Target finalization failed: %s", finalize_result.error)
                current_errors = stats.get("errors_encountered", 0)
                assert isinstance(current_errors, int)
                stats["errors_encountered"] = current_errors + 1

            stats["processing_end_time"] = time.time()
            end_time = stats.get("processing_end_time", 0.0)
            start_time = stats.get("processing_start_time", 0.0)
            assert isinstance(end_time, (int, float))
            assert isinstance(start_time, (int, float))
            processing_duration = end_time - start_time
            stats["processing_duration_seconds"] = processing_duration

            logger.info(
                "Stream processing completed in %.2f seconds",
                processing_duration,
            )
            return FlextResult[FlextTypes.Dict].ok(dict(stats))

        except Exception as e:
            logger.exception("Unexpected error during stream processing")
            stats["processing_end_time"] = time.time()
            current_errors = stats.get("errors_encountered", 0)
            assert isinstance(current_errors, int)
            stats["errors_encountered"] = current_errors + 1
            return FlextResult[FlextTypes.Dict].fail(f"Stream processing error: {e}")

    def health_check(self) -> FlextResult[FlextTypes.Dict]:
        """Perform comprehensive health check for monitoring systems.

        Returns:
            FlextResult with health status and metrics

        """
        logger.debug("Performing health check")

        health_status: FlextTypes.Dict = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {},  # Will be populated with check results
            "metrics": {},  # Will be populated with metrics
        }

        try:
            # Check 1: Target initialization
            checks = health_status["checks"]
            assert isinstance(checks, dict)
            if not self.target:
                health_status["status"] = "unhealthy"
                checks["target_initialized"] = False
            else:
                checks["target_initialized"] = True

            # Check 2: Oracle connectivity
            if self.target:
                try:
                    connectivity_result = self.target.test_connection()
                    checks["oracle_connectivity"] = connectivity_result
                    if not connectivity_result:
                        health_status["status"] = "degraded"
                except Exception as e:
                    checks["oracle_connectivity"] = False
                    checks["oracle_error"] = str(e)
                    health_status["status"] = "unhealthy"

            # Add configuration metrics
            metrics = health_status["metrics"]
            assert isinstance(metrics, dict)
            if self.target:
                target_metrics = self.target.get_implementation_metrics()
                if isinstance(target_metrics, dict):
                    metrics.update(target_metrics)

            logger.debug("Health check completed: %s", health_status["status"])
            return FlextResult[FlextTypes.Dict].ok(dict(health_status))

        except Exception as e:
            logger.exception("Health check failed")
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)
            return FlextResult[FlextTypes.Dict].fail(f"Health check error: {e}")

    def shutdown(self) -> FlextResult[None]:
        """Graceful shutdown with resource cleanup.

        Returns:
            FlextResult[None]: Success if shutdown completed cleanly

        """
        logger.info("Starting graceful shutdown")

        try:
            if self.target:
                # Finalize any pending operations
                logger.info("Finalizing pending operations")
                self.target.finalize()

                # Clean up resources (if needed)
                logger.info("Cleaning up target resources")
                self.target = None

            logger.info("Graceful shutdown completed")
            return FlextResult[None].ok(None)

        except Exception as e:
            logger.exception("Error during shutdown")
            return FlextResult[None].fail(f"Shutdown error: {e}")


def demonstrate_production_setup() -> None:
    """Demonstrate production setup and processing patterns."""
    logger.info("Starting production setup demonstration")

    try:
        # Step 1: Create production configuration
        logger.info("Step 1: Creating production configuration")
        config = ProductionConfig.create_from_environment()

        # Step 2: Initialize production target manager
        logger.info("Step 2: Initializing production target manager")
        manager = ProductionTargetManager(config)

        init_result = manager.initialize()
        if init_result.is_failure:
            logger.error("Production initialization failed: %s", init_result.error)
            return

        # Step 3: Perform health check
        logger.info("Step 3: Performing initial health check")
        health_result = manager.health_check()
        if health_result.success:
            health_data = health_result.data
            if isinstance(health_data, dict):
                logger.info(
                    "Health check status: %s", health_data.get("status", "unknown")
                )
                checks = health_data.get("checks")
                if isinstance(checks, dict):
                    logger.info(
                        "Oracle connectivity: %s",
                        checks.get("oracle_connectivity", "unknown"),
                    )
        else:
            logger.warning("Health check failed: %s", health_result.error)

        # Step 4: Create sample production data stream
        logger.info("Step 4: Creating sample production data stream")
        messages = create_production_sample_stream()

        # Step 5: Process the stream
        logger.info("Step 5: Processing production data stream")
        processing_result = manager.process_singer_stream(messages)

        if processing_result.success:
            stats = processing_result.data
            logger.info("=== Production Processing Statistics ===")
            logger.info("Messages processed: %d", stats.get("messages_processed", 0))
            logger.info("Records processed: %d", stats.get("records_processed", 0))
            logger.info(
                "Processing duration: %.2fs",
                stats.get("processing_duration_seconds", 0),
            )
            logger.info("Errors encountered: %d", stats.get("errors_encountered", 0))

            if stats.get("total_records"):
                logger.info("Total records loaded: %s", stats["total_records"])
                logger.info(
                    "Successful records: %d",
                    stats.get("successful_records", 0),
                )
                logger.info("Failed records: %d", stats.get("failed_records", 0))
        else:
            logger.error("Production processing failed: %s", processing_result.error)

        # Step 6: Final health check
        logger.info("Step 6: Performing final health check")
        final_health = manager.health_check()
        if final_health.success:
            logger.info("Final health status: %s", final_health.data["status"])

        # Step 7: Graceful shutdown
        logger.info("Step 7: Performing graceful shutdown")
        shutdown_result = manager.shutdown()
        if shutdown_result.success:
            logger.info("Production shutdown completed successfully")
        else:
            logger.error("Shutdown issues: %s", shutdown_result.error)

    except Exception:
        logger.exception("Production demonstration failed")
        raise


def create_production_sample_stream() -> FlextTypes.List:
    """Create a realistic production data stream for demonstration.

    Returns:
      List of Singer messages representing a production workload

    """
    messages: FlextTypes.List = []  # Flexible list for various message types

    # Schema message for customer orders
    schema_message = {
        "type": "SCHEMA",
        "stream": "customer_orders",
        "schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "integer"},
                "customer_id": {"type": "integer"},
                "order_date": {"type": "string", "format": "date-time"},
                "product_sku": {"type": "string"},
                "quantity": {"type": "integer"},
                "unit_price": {"type": "number"},
                "total_amount": {"type": "number"},
                "order_status": {"type": "string"},
                "shipping_address": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
            "required": ["order_id", "customer_id", "order_date"],
        },
        "key_properties": ["order_id"],
    }
    messages.append(cast("object", schema_message))

    # Generate sample records (simulate production volume)
    base_date = datetime.datetime(2025, 1, 1, tzinfo=UTC)

    for i in range(1, 101):  # 100 sample orders
        record_message = {
            "type": "RECORD",
            "stream": "customer_orders",
            "record": {
                "order_id": i,
                "customer_id": (i % 20) + 1,  # 20 customers
                "order_date": (base_date + datetime.timedelta(hours=i)).isoformat()
                + "Z",
                "product_sku": f"SKU-{(i % 10) + 1:03d}",
                "quantity": (i % 5) + 1,
                "unit_price": round(19.99 + (i % 100), 2),
                "total_amount": round((19.99 + (i % 100)) * ((i % 5) + 1), 2),
                "order_status": ["pending", "processing", "shipped", "delivered"][
                    i % 4
                ],
                "shipping_address": f"{i} Main St, City {i % 10}, State",
                "created_at": (base_date + datetime.timedelta(hours=i)).isoformat()
                + "Z",
                "updated_at": (
                    base_date + datetime.timedelta(hours=i, minutes=30)
                ).isoformat()
                + "Z",
            },
        }
        messages.append(cast("object", record_message))

    # State message
    state_message = {
        "type": "STATE",
        "value": {
            "bookmarks": {
                "customer_orders": {
                    "last_order_id": 100,
                    "last_updated": (
                        base_date + datetime.timedelta(hours=100)
                    ).isoformat()
                    + "Z",
                },
            },
        },
    }
    messages.append(state_message)

    return messages


def main() -> None:
    """Main entry point for production setup example."""
    logger.info("FLEXT Target Oracle - Production Setup Example")
    logger.info("=" * 60)

    # Check for required environment variables
    required_vars = ["ORACLE_HOST", "ORACLE_SERVICE", "ORACLE_USER", "ORACLE_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(
            "Missing required environment variables: %s",
            ", ".join(missing_vars),
        )
        logger.error("Please set the following environment variables:")
        for var in required_vars:
            logger.error("  export %s=<value>", var)
        sys.exit(1)

    try:
        # Run production demonstration
        demonstrate_production_setup()

        logger.info("\n%s", "=" * 60)
        logger.info("Production setup example completed successfully!")
        logger.info("\nProduction Checklist:")
        logger.info("✓ Environment-based configuration")
        logger.info("✓ Comprehensive validation and error handling")
        logger.info("✓ Health checks and monitoring integration")
        logger.info("✓ Graceful shutdown and resource cleanup")
        logger.info("✓ Production-grade logging and statistics")

    except KeyboardInterrupt:
        logger.info("Example interrupted by user")
    except Exception:
        logger.exception("Production setup example failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
