"""Production Setup Example - Enterprise-Grade Oracle Target Configuration.

This example demonstrates production-ready configuration and deployment patterns
for FLEXT Target Oracle, including comprehensive error handling, monitoring,
security considerations, and performance optimization.

"""

from __future__ import annotations

import datetime
import json
import logging
import os
import signal
import sys
import time
from collections.abc import Sequence
from datetime import UTC
from types import FrameType
from typing import cast

from pydantic import BaseModel, Field

from flext_target_oracle import (
    FlextTargetOracle,
    FlextTargetOracleSettings,
    c,
    m,
    r,
    t,
    u,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("flext_target_oracle.log")],
)
logger = u.fetch_logger(__name__)
type SingerMessage = (
    m.TargetOracle.SingerSchemaMessage
    | m.TargetOracle.SingerRecordMessage
    | m.TargetOracle.SingerStateMessage
    | m.TargetOracle.SingerActivateVersionMessage
)


class HealthStatus(BaseModel):
    """Runtime health snapshot used by health checks."""

    timestamp: float
    status: str = "healthy"
    checks: t.MutableContainerMapping = Field(default_factory=dict)
    metrics: t.MutableContainerMapping = Field(default_factory=dict)
    error: str | None = None


class ProcessingStats(BaseModel):
    """In-memory counters for Singer stream processing."""

    processing_start_time: float
    processing_end_time: float | None = None
    processing_duration_seconds: float = 0.0
    messages_processed: int = 0
    schemas_processed: int = 0
    records_processed: int = 0
    states_processed: int = 0
    errors_encountered: int = 0


class ProductionConfig:
    """Production configuration management with environment variables."""

    @staticmethod
    def create_from_environment() -> FlextTargetOracleSettings:
        """Create production configuration from environment variables.

        Returns:
            FlextTargetOracleSettings: Production-ready configuration

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
        oracle_port = int(os.getenv("ORACLE_PORT", "1521"))
        default_target_schema = os.getenv("DEFAULT_TARGET_SCHEMA", "ENTERPRISE_DW")
        batch_size = int(os.getenv("BATCH_SIZE", "5000"))
        connection_timeout = int(os.getenv("CONNECTION_TIMEOUT", "60"))
        load_method_str = os.getenv("LOAD_METHOD", "BULK_INSERT").upper()
        load_method = getattr(
            c.TargetOracle,
            f"LOAD_METHOD_{load_method_str}",
            c.TargetOracle.LOAD_METHOD_BULK_INSERT,
        )
        _ = load_method  # reserved for future use
        config = FlextTargetOracleSettings.model_validate({
            "oracle_host": oracle_host,
            "oracle_port": oracle_port,
            "oracle_service_name": oracle_service,
            "oracle_user": oracle_user,
            "oracle_password": oracle_password,
            "default_target_schema": default_target_schema,
            "batch_size": batch_size,
            "use_bulk_operations": True,
            "transaction_timeout": connection_timeout,
        })
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

    def __init__(self, config: FlextTargetOracleSettings) -> None:
        """Initialize production target manager.

        Args:
            config: Validated Oracle target configuration

        """
        self.config = config
        self.target: FlextTargetOracle | None = None
        self.shutdown_requested = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def health_check(self) -> r[t.ContainerMapping]:
        """Perform comprehensive health check for monitoring systems.

        Returns:
            r with health status and metrics

        """
        logger.debug("Performing health check")
        health_status = HealthStatus(timestamp=time.time())
        try:
            checks = health_status.checks
            if not self.target:
                health_status.status = "unhealthy"
                checks["target_initialized"] = False
            else:
                checks["target_initialized"] = True
            if self.target:
                try:
                    connectivity_result = self.target.test_connection()
                    checks["oracle_connectivity"] = connectivity_result.success
                    if not connectivity_result.success:
                        health_status.status = "degraded"
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                    RuntimeError,
                    ImportError,
                ) as e:
                    checks["oracle_connectivity"] = False
                    checks["oracle_error"] = str(e)
                    health_status.status = "unhealthy"
            metrics = health_status.metrics
            if self.target:
                target_metrics = self.target.get_implementation_metrics()
                metrics.update(target_metrics.model_dump())
            logger.debug("Health check completed: %s", health_status.status)
            return r[t.ContainerMapping].ok(health_status.model_dump())
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Health check failed")
            health_status.status = "unhealthy"
            health_status.error = str(e)
            return r[t.ContainerMapping].fail(f"Health check error: {e}")

    def initialize(self) -> r[bool]:
        """Initialize target with comprehensive validation.

        Returns:
            r[bool]: Success if initialization complete, failure with error details

        """
        logger.info("Initializing production Oracle target")
        try:
            logger.info("Validating configuration domain rules")
            validation_result = r[bool].ok(value=True)
            if validation_result.failure:
                return r[bool].fail(
                    f"Configuration validation failed: {validation_result.error}",
                )
            logger.info("Creating Oracle target instance")
            self.target = FlextTargetOracle(self.config)
            logger.info("Testing Oracle database connectivity")
            connection_result = self.target.test_connection()
            if connection_result.failure:
                return r[bool].fail("Oracle connectivity test failed")
            logger.info("Production target initialized successfully")
            return r[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Failed to initialize production target")
            return r[bool].fail(f"Initialization error: {e}")

    def process_singer_stream(
        self,
        messages: Sequence[SingerMessage],
    ) -> r[t.ContainerMapping]:
        """Process complete Singer message stream with comprehensive error handling.

        Args:
            messages: List of Singer messages (SCHEMA, RECORD, STATE)

        Returns:
            r with processing statistics and status

        """
        if not self.target:
            return r[t.ContainerMapping].fail("Target not initialized")
        logger.info("Processing Singer stream with %d messages", len(messages))
        stats = ProcessingStats(processing_start_time=time.time())
        try:
            for i, message in enumerate(messages):
                if self.shutdown_requested:
                    logger.info("Shutdown requested, stopping message processing")
                    break
                message_type = "UNKNOWN"
                if isinstance(message, m.TargetOracle.SingerSchemaMessage):
                    message_type = "SCHEMA"
                elif isinstance(message, m.TargetOracle.SingerRecordMessage):
                    message_type = "RECORD"
                elif isinstance(message, m.TargetOracle.SingerStateMessage):
                    message_type = "STATE"
                logger.debug(
                    "Processing message %d/%d: %s",
                    i + 1,
                    len(messages),
                    message_type,
                )
                if not self.target:
                    return r[t.ContainerMapping].fail("Target not initialized")
                result = self.target.process_singer_message(message)
                if result.success:
                    stats.messages_processed += 1
                    if message_type == "SCHEMA":
                        stats.schemas_processed += 1
                    elif message_type == "RECORD":
                        stats.records_processed += 1
                    elif message_type == "STATE":
                        stats.states_processed += 1
                else:
                    stats.errors_encountered += 1
                    logger.error(
                        "Message %d processing failed: %s",
                        i + 1,
                        result.error,
                    )
                if (i + 1) % 1000 == 0:
                    logger.info("Processed %d/%d messages", i + 1, len(messages))
            logger.info("Finalizing target operations")
            finalize_result = self.target.finalize()
            if finalize_result.success:
                final_stats = finalize_result.value
                stats.messages_processed += final_stats.total_records
                logger.info("Target finalization completed successfully")
            else:
                logger.error("Target finalization failed: %s", finalize_result.error)
                stats.errors_encountered += 1
            stats.processing_end_time = time.time()
            processing_duration = (
                stats.processing_end_time - stats.processing_start_time
            )
            stats.processing_duration_seconds = processing_duration
            logger.info(
                "Stream processing completed in %.2f seconds",
                processing_duration,
            )
            return r[t.ContainerMapping].ok(stats.model_dump())
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Unexpected error during stream processing")
            stats.processing_end_time = time.time()
            stats.errors_encountered += 1
            return r[t.ContainerMapping].fail(f"Stream processing error: {e}")

    def shutdown(self) -> r[bool]:
        """Graceful shutdown with resource cleanup.

        Returns:
            r[bool]: Success if shutdown completed cleanly

        """
        logger.info("Starting graceful shutdown")
        try:
            if self.target:
                logger.info("Finalizing pending operations")
                self.target.finalize()
                logger.info("Cleaning up target resources")
                self.target = None
            logger.info("Graceful shutdown completed")
            return r[bool].ok(value=True)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            logger.exception("Error during shutdown")
            return r[bool].fail(f"Shutdown error: {e}")

    def _signal_handler(self, signum: int, _frame: FrameType | None) -> None:
        """Handle shutdown signals gracefully."""
        logger.info("Received signal %d, initiating graceful shutdown", signum)
        self.shutdown_requested = True


def demonstrate_production_setup() -> None:
    """Demonstrate production setup and processing patterns."""
    logger.info("Starting production setup demonstration")
    try:
        logger.info("Step 1: Creating production configuration")
        config = ProductionConfig.create_from_environment()
        logger.info("Step 2: Initializing production target manager")
        manager = ProductionTargetManager(config)
        init_result = manager.initialize()
        if init_result.failure:
            logger.error("Production initialization failed: %s", init_result.error)
            return
        logger.info("Step 3: Performing initial health check")
        health_result = manager.health_check()
        if health_result.success:
            health_data = health_result.value
            if isinstance(health_data, dict):
                logger.info(
                    "Health check status",
                    status=str(health_data.get("status", "unknown")),
                )
                checks_obj: t.NormalizedValue = health_data.get("checks")
                checks: t.ContainerMapping = (
                    cast("t.ContainerMapping", checks_obj)
                    if isinstance(checks_obj, dict)
                    else {}
                )
                if checks:
                    logger.info(
                        "Oracle connectivity",
                        connectivity=str(checks.get("oracle_connectivity", "unknown")),
                    )
        else:
            logger.warning("Health check failed: %s", health_result.error)
        logger.info("Step 4: Creating sample production data stream")
        messages = create_production_sample_stream()
        logger.info("Step 5: Processing production data stream")
        processing_result = manager.process_singer_stream(messages)
        if processing_result.success:
            stats = processing_result.value
            logger.info("=== Production Processing Statistics ===")
            logger.info(
                "Processing stats",
                messages_processed=str(stats.get("messages_processed", 0)),
                records_processed=str(stats.get("records_processed", 0)),
                processing_duration_seconds=str(
                    stats.get("processing_duration_seconds", 0),
                ),
                errors_encountered=str(stats.get("errors_encountered", 0)),
            )
            if stats.get("total_records"):
                logger.info(
                    "Load stats",
                    total_records=str(stats.get("total_records", 0)),
                    successful_records=str(stats.get("successful_records", 0)),
                    failed_records=str(stats.get("failed_records", 0)),
                )
        else:
            logger.error("Production processing failed: %s", processing_result.error)
        logger.info("Step 6: Performing final health check")
        final_health = manager.health_check()
        if final_health.success and isinstance(final_health.value, dict):
            logger.info(
                "Final health status",
                status=str(final_health.value.get("status", "unknown")),
            )
        logger.info("Step 7: Performing graceful shutdown")
        shutdown_result = manager.shutdown()
        if shutdown_result.success:
            logger.info("Production shutdown completed successfully")
        else:
            logger.error("Shutdown issues: %s", shutdown_result.error)
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ):
        logger.exception("Production demonstration failed")
        raise


def create_production_sample_stream() -> Sequence[SingerMessage]:
    """Create a realistic production data stream for demonstration.

    Returns:
      List of Singer messages representing a production workload

    """
    messages: t.MutableSequenceOf[SingerMessage] = []
    schema_message = m.TargetOracle.SingerSchemaMessage.model_validate({
        "type": "SCHEMA",
        "stream": "customer_orders",
        "schema": {
            "type": "t.NormalizedValue",
            "properties": json.dumps({
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
            }),
            "required": json.dumps(["order_id", "customer_id", "order_date"]),
        },
        "key_properties": ["order_id"],
    })
    messages.append(schema_message)
    base_date = datetime.datetime(2025, 1, 1, tzinfo=UTC)
    for i in range(1, 101):
        record_message = m.TargetOracle.SingerRecordMessage.model_validate({
            "type": "RECORD",
            "stream": "customer_orders",
            "record": {
                "order_id": i,
                "customer_id": i % 20 + 1,
                "order_date": (base_date + datetime.timedelta(hours=i)).isoformat()
                + "Z",
                "product_sku": f"SKU-{i % 10 + 1:03d}",
                "quantity": i % 5 + 1,
                "unit_price": round(19.99 + i % 100, 2),
                "total_amount": round((19.99 + i % 100) * (i % 5 + 1), 2),
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
        })
        messages.append(record_message)
    state_message = m.TargetOracle.SingerStateMessage.model_validate({
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
    })
    messages.append(state_message)
    return messages


def main() -> None:
    """Main entry point for production setup example."""
    logger.info("FLEXT Target Oracle - Production Setup Example")
    logger.info("=" * 60)
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
    except (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
    ):
        logger.exception("Production setup example failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
