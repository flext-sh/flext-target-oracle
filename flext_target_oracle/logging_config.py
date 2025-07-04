"""Comprehensive logging and monitoring configuration for Oracle Target.

Provides structured logging, performance metrics, operational monitoring,
and integration with observability platforms.
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

# Constants for logging configuration
MAX_SQL_LOG_LENGTH = 500

if TYPE_CHECKING:
    from collections.abc import Generator
    from types import TracebackType

    from typing_extensions import Self

try:
    import structlog

    HAS_STRUCTLOG = True
except ImportError:
    HAS_STRUCTLOG = False

try:
    from prometheus_client import (
        CollectorRegistry,
        Counter,
        Gauge,
        Histogram,
        generate_latest,
    )

    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False


class OracleTargetLogger:
    """Enhanced logging system for Oracle Target with structured logging and metrics.

    Features:
    - Structured logging with contextual information
    - Performance metrics collection
    - Error tracking and alerting
    - Integration with monitoring systems
    - Configurable log levels and outputs
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize comprehensive logging system."""
        self.config = config
        self.logger_name = "flext_target_oracle"

        # Initialize logging components
        self._setup_structured_logging()
        self._setup_metrics()
        self._setup_performance_tracking()

        # Create main logger
        self.logger = self._create_logger()

        # Session tracking
        self.session_id = self._generate_session_id()
        self.start_time = time.time()
        self.metrics: dict[str, Any] = {}

    def _setup_structured_logging(self) -> None:
        """Configure structured logging with contextual processors."""
        log_level = self.config.get("log_level", "INFO").upper()
        log_format = self.config.get("log_format", "json")

        # Configure structlog if available
        if HAS_STRUCTLOG and log_format == "json":
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.UnicodeDecoder(),
                    structlog.processors.JSONRenderer(),
                ],
                context_class=dict,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
            self.use_structured = True
        else:
            self.use_structured = False

        # Standard logging configuration
        self.log_level = getattr(logging, log_level, logging.INFO)

        # Create log directory if specified
        log_file = self.config.get("log_file")
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

    def _setup_metrics(self) -> None:
        """Initialize Prometheus metrics if available."""
        if not HAS_PROMETHEUS or not self.config.get("enable_metrics", True):
            self.prometheus_enabled = False
            return

        self.prometheus_enabled = True
        self.registry = CollectorRegistry()

        # Core metrics
        self.records_processed = Counter(
            "oracle_target_records_processed_total",
            "Total number of records processed",
            ["stream", "operation"],
            registry=self.registry,
        )

        self.processing_duration = Histogram(
            "oracle_target_processing_duration_seconds",
            "Time spent processing records",
            ["stream", "operation"],
            registry=self.registry,
        )

        self.batch_size = Histogram(
            "oracle_target_batch_size",
            "Size of processing batches",
            ["stream"],
            registry=self.registry,
        )

        self.errors_total = Counter(
            "oracle_target_errors_total",
            "Total number of errors",
            ["stream", "error_type"],
            registry=self.registry,
        )

        self.connection_pool_size = Gauge(
            "oracle_target_connection_pool_size",
            "Current connection pool size",
            registry=self.registry,
        )

        self.memory_usage_mb = Gauge(
            "oracle_target_memory_usage_mb",
            "Current memory usage in MB",
            registry=self.registry,
        )

    def _setup_performance_tracking(self) -> None:
        """Initialize performance tracking variables."""
        self.performance_counters: dict[str, Any] = {
            "total_records": 0,
            "total_batches": 0,
            "total_errors": 0,
            "total_duration": 0.0,
            "streams_processed": set(),
        }

    def _create_logger(self) -> logging.Logger:
        """Create and configure the main logger."""
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        # Clear any existing handlers
        logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)

        # File handler if configured
        log_file = self.config.get("log_file")
        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=self.config.get("log_max_bytes", 50 * 1024 * 1024),  # 50MB
                backupCount=self.config.get("log_backup_count", 5),
            )
            file_handler.setLevel(self.log_level)

            # JSON formatter for file logs
            if self.config.get("log_format") == "json":
                file_formatter = JsonFormatter()
                file_handler.setFormatter(file_formatter)
            else:
                text_formatter: logging.Formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                )
                file_handler.setFormatter(text_formatter)

            logger.addHandler(file_handler)

        # Console formatter
        console_formatter: logging.Formatter
        if self.config.get("log_format") == "json":
            console_formatter = JsonFormatter()
        else:
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
            )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        return logger

    def _generate_session_id(self) -> str:
        """Generate unique session identifier."""
        return f"oracle_target_{int(time.time())}_{os.getpid()}"

    @contextmanager
    def operation_context(
        self, operation: str, stream: str = "unknown", **kwargs: Union[str, int, bool],
    ) -> Generator[dict[str, Any], None, None]:
        """Context manager for tracking operations with metrics and logging."""
        start_time = time.time()
        operation_id = f"{operation}_{int(start_time)}"

        context: dict[str, Any] = {
            "operation": operation,
            "operation_id": operation_id,
            "stream": stream,
            "session_id": self.session_id,
            **kwargs,
        }

        self.info("Operation started", extra=context)

        try:
            yield context

            duration = time.time() - start_time
            context["duration"] = duration
            context["status"] = "success"

            # Update performance counters
            current_duration = self.performance_counters.get("total_duration", 0.0)
            self.performance_counters["total_duration"] = (
                float(current_duration) + duration
            )
            streams_set = self.performance_counters.get("streams_processed", set())
            streams_set.add(stream)
            self.performance_counters["streams_processed"] = streams_set

            # Update Prometheus metrics
            if self.prometheus_enabled:
                self.processing_duration.labels(
                    stream=stream, operation=operation,
                ).observe(duration)

            self.info("Operation completed", extra=context)

        except Exception as e:
            duration = time.time() - start_time
            context["duration"] = duration
            context["status"] = "error"
            context["error"] = str(e)
            context["error_type"] = type(e).__name__

            # Update error counters
            current_errors = self.performance_counters.get("total_errors", 0)
            self.performance_counters["total_errors"] = int(current_errors) + 1

            # Update Prometheus metrics
            if self.prometheus_enabled:
                self.errors_total.labels(
                    stream=stream, error_type=type(e).__name__,
                ).inc()
                self.processing_duration.labels(
                    stream=stream, operation=operation,
                ).observe(duration)

            self.error("Operation failed", extra=context, exc_info=True)
            raise

    def log_record_batch(
        self, stream: str, batch_size: int, operation: str = "insert",
    ) -> None:
        """Log processing of a record batch with metrics."""
        context = {
            "stream": stream,
            "batch_size": batch_size,
            "operation": operation,
            "session_id": self.session_id,
        }

        # Update performance counters
        current_records = self.performance_counters.get("total_records", 0)
        current_batches = self.performance_counters.get("total_batches", 0)
        self.performance_counters["total_records"] = int(current_records) + batch_size
        self.performance_counters["total_batches"] = int(current_batches) + 1

        # Update Prometheus metrics
        if self.prometheus_enabled:
            self.records_processed.labels(stream=stream, operation=operation).inc(
                batch_size,
            )
            self.batch_size.labels(stream=stream).observe(batch_size)

        if self.config.get("log_batch_details", True):
            self.info("Batch processed", extra=context)

    def log_performance_stats(self) -> dict[str, Any]:
        """Log comprehensive performance statistics."""
        current_time = time.time()
        session_duration = current_time - self.start_time

        total_records = self.performance_counters.get("total_records", 0)
        total_batches = self.performance_counters.get("total_batches", 0)
        total_errors = self.performance_counters.get("total_errors", 0)
        streams_processed = self.performance_counters.get("streams_processed", set())

        stats = {
            "session_id": self.session_id,
            "session_duration": session_duration,
            "total_records": total_records,
            "total_batches": total_batches,
            "total_errors": total_errors,
            "streams_count": len(streams_processed),
            "streams": list(streams_processed),
        }

        if session_duration > 0:
            stats["records_per_second"] = float(total_records) / session_duration
            stats["batches_per_second"] = float(total_batches) / session_duration

        if int(total_batches) > 0:
            stats["avg_batch_size"] = float(total_records) / float(total_batches)

        self.info("Performance statistics", extra=stats)
        return stats

    def log_oracle_connection_info(self, connection_info: dict[str, Any]) -> None:
        """Log Oracle database connection information."""
        safe_info = connection_info.copy()

        # Remove sensitive information
        sensitive_keys = ["password", "wallet_password", "token"]
        for key in sensitive_keys:
            if key in safe_info:
                safe_info[key] = "***REDACTED***"

        context = {
            "session_id": self.session_id,
            "connection_info": safe_info,
        }

        self.info("Oracle connection established", extra=context)

    def log_oracle_performance(self, metrics: dict[str, Any]) -> None:
        """Log Oracle-specific performance metrics."""
        context = {
            "session_id": self.session_id,
            "oracle_metrics": metrics,
        }

        # Update Prometheus metrics if available
        if self.prometheus_enabled:
            if "pool_size" in metrics:
                self.connection_pool_size.set(metrics["pool_size"])
            if "memory_usage_mb" in metrics:
                self.memory_usage_mb.set(metrics["memory_usage_mb"])

        self.info("Oracle performance metrics", extra=context)

    def log_sql_statement(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        duration: float | None = None,
    ) -> None:
        """Log SQL statements if enabled."""
        if not self.config.get("log_sql_statements", False):
            return

        context = {
            "session_id": self.session_id,
            "sql": (
                sql[:MAX_SQL_LOG_LENGTH] + "..."
                if len(sql) > MAX_SQL_LOG_LENGTH
                else sql
            ),
            "params_count": len(params) if params else 0,
        }

        if duration is not None:
            context["duration"] = duration

        self.debug("SQL executed", extra=context)

    def export_metrics(self) -> str:
        """Export Prometheus metrics in text format."""
        if not self.prometheus_enabled:
            return ""

        return generate_latest(self.registry).decode("utf-8")

    def get_health_status(self) -> dict[str, Any]:
        """Get current health status of the target."""
        current_time = time.time()
        session_duration = current_time - self.start_time

        total_records = self.performance_counters.get("total_records", 0)
        total_errors = self.performance_counters.get("total_errors", 0)

        return {
            "status": "healthy" if int(total_errors) == 0 else "degraded",
            "session_id": self.session_id,
            "uptime_seconds": session_duration,
            "total_records": total_records,
            "total_errors": total_errors,
            "error_rate": (
                float(total_errors) / max(1, float(total_records))
                if int(total_records) > 0
                else 0
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # Standard logging methods with context injection
    def debug(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log debug message with context."""
        self._log(logging.DEBUG, message, extra, **kwargs)

    def info(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log info message with context."""
        self._log(logging.INFO, message, extra, **kwargs)

    def warning(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log warning message with context."""
        self._log(logging.WARNING, message, extra, **kwargs)

    def error(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log error message with context."""
        self._log(logging.ERROR, message, extra, **kwargs)

    def critical(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log critical message with context."""
        self._log(logging.CRITICAL, message, extra, **kwargs)

    def exception(
        self,
        message: str,
        *args: str | float,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Log exception message with context and traceback."""
        kwargs.setdefault("exc_info", True)
        self._log(logging.ERROR, message % args if args else message, extra, **kwargs)

    def _log(
        self,
        level: int,
        message: str,
        extra: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Internal logging method with context injection."""
        try:
            # Check if logging system is still functional
            if not self.logger or not self.logger.handlers:
                return

            # Check if any handler has a closed stream
            for handler in self.logger.handlers:
                if (
                    hasattr(handler, "stream")
                    and hasattr(handler.stream, "closed")
                    and handler.stream.closed
                ):
                    return

            if extra is None:
                extra = {}

            # Add common context
            extra.setdefault("session_id", self.session_id)
            extra.setdefault("component", "oracle_target")
            extra.setdefault("timestamp", datetime.now(timezone.utc).isoformat())

            self.logger.log(level, message, extra=extra, **kwargs)
        except (ValueError, OSError) as e:
            # Logger stream is closed during shutdown - attempt emergency logging
            try:
                # Try to write to stderr as last resort
                import sys

                sys.stderr.write(f"WARNING: Logger failed during shutdown: {e}\n")
                sys.stderr.flush()
            except (OSError, AttributeError) as stderr_error:
                # If even stderr fails, then system is truly shutting down
                # Try one final fallback before giving up
                try:
                    # Attempt to write to any available file descriptor
                    import os

                    os.write(
                        2,
                        f"CRITICAL: All logging mechanisms failed: "
                        f"{stderr_error}\n".encode(),
                    )
                except OSError:
                    # Absolutely no way to log - system is completely shutting down
                    pass


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "__dict__"):
            log_entry.update({key: value for key, value in record.__dict__.items() if key not in {
                    "name",
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "lineno",
                    "funcName",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "processName",
                    "process",
                    "stack_info",
                    "exc_info",
                    "exc_text",
                }})

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class PerformanceTimer:
    """Context manager for timing operations."""

    def __init__(self, logger: OracleTargetLogger, operation: str) -> None:
        self.logger = logger
        self.operation = operation
        self.start_time: float | None = None
        self.duration: float | None = None

    def start(self) -> None:
        """Start timing."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop timing and calculate duration."""
        if self.start_time is not None:
            self.duration = time.time() - self.start_time

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.stop()
        if self.duration is not None:
            self.logger.info(
                f"{self.operation} completed",
                extra={"operation": self.operation, "duration": self.duration},
            )


def create_logger(config: dict[str, Any]) -> OracleTargetLogger:
    """Factory function to create configured logger."""
    return OracleTargetLogger(config)
