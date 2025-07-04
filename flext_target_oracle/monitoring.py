"""Comprehensive monitoring and observability for Oracle Target.

Provides health checks, metrics collection, alerting integration,
and operational monitoring capabilities.
"""

from __future__ import annotations

import os
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Union

import psutil

# Health check thresholds
HEALTH_CPU_THRESHOLD = 90
HEALTH_MEMORY_THRESHOLD = 90
HEALTH_ERROR_RATE_THRESHOLD = 5

if TYPE_CHECKING:
    import logging
    from collections.abc import Generator

    from sqlalchemy.engine import Engine

try:
    import oracledb  # noqa: F401

    HAS_ORACLEDB = True
except ImportError:
    HAS_ORACLEDB = False

try:
    from sqlalchemy import text

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


class OracleTargetMonitor:
    """Comprehensive monitoring system for Oracle Target.

    Features:
    - System resource monitoring
    - Oracle database health checks
    - Performance metrics collection
    - Alert threshold management
    - Integration with monitoring platforms
    """

    def __init__(
        self, config: dict[str, Any], logger: logging.Logger | None = None,
    ) -> None:
        """Initialize monitoring system."""
        self.config = config
        self.logger = logger
        self.enabled = config.get("enable_monitoring", True)

        if not self.enabled:
            return

        # Monitoring configuration
        self.check_interval = config.get("monitoring_interval", 30)  # seconds
        self.health_check_timeout = config.get("health_check_timeout", 10)

        # Alert thresholds
        self.thresholds = {
            "memory_usage_percent": config.get("memory_threshold", 80),
            "cpu_usage_percent": config.get("cpu_threshold", 80),
            "connection_pool_usage": config.get("pool_threshold", 90),
            "error_rate_percent": config.get("error_rate_threshold", 5),
            "response_time_ms": config.get("response_time_threshold", 5000),
        }

        # State tracking
        self.metrics_history: list[dict[str, Any]] = []
        self.alerts_sent: set[str] = set()
        self.last_health_check: dict[str, Any] | None = None
        self._monitoring_thread: threading.Thread | None = None
        self.shutdown_event = threading.Event()

        # Initialize components
        self._initialize_monitoring()

    def _initialize_monitoring(self) -> None:
        """Initialize monitoring components."""
        if self.logger:
            self.logger.info("Initializing Oracle Target monitoring")

        # Start background monitoring if enabled
        if self.config.get("background_monitoring", False):
            self.start_background_monitoring()

    def start_background_monitoring(self) -> None:
        """Start background monitoring thread."""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            return

        self.shutdown_event.clear()
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop, name="OracleTargetMonitor", daemon=True,
        )
        self._monitoring_thread.start()

        if self.logger:
            self.logger.info("Background monitoring started")

    def stop_background_monitoring(self) -> None:
        """Stop background monitoring thread silently."""
        if (
            hasattr(self, "_monitoring_thread")
            and self._monitoring_thread
            and self._monitoring_thread.is_alive()
        ):
            self.shutdown_event.set()
            self._monitoring_thread.join(timeout=2)

        # Clear thread reference
        self._monitoring_thread = None

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while not self.shutdown_event.is_set():
            try:
                metrics = self.collect_metrics()
                self._check_thresholds(metrics)
                self._store_metrics(metrics)

            except (OSError, ValueError, AttributeError, ImportError):
                if self.logger:
                    self.logger.exception("Monitoring loop error")

            # Wait for next interval
            self.shutdown_event.wait(timeout=self.check_interval)

    def collect_metrics(self) -> dict[str, Any]:
        """Collect comprehensive metrics."""
        metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": self._collect_system_metrics(),
            "process": self._collect_process_metrics(),
            "oracle": self._collect_oracle_metrics(),
            "performance": self._collect_performance_metrics(),
        }

        if self.logger:
            self.logger.debug("Metrics collected", extra={"metrics": metrics})

        return metrics

    def _collect_system_metrics(self) -> dict[str, Any]:
        """Collect system-level metrics."""
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage("/")

            return {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent,
                },
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100,
                },
                "load_average": os.getloadavg() if hasattr(os, "getloadavg") else None,
            }
        except (OSError, ValueError, AttributeError, ImportError) as e:
            if self.logger:
                self.logger.warning("Failed to collect system metrics: %s", e)
            # Return empty dict but log the failure for debugging
            return {"error": f"Failed to collect system metrics: {e}"}

    def _collect_process_metrics(self) -> dict[str, Any]:
        """Collect process-specific metrics."""
        try:
            process = psutil.Process()

            return {
                "pid": process.pid,
                "cpu_percent": process.cpu_percent(),
                "memory_info": process.memory_info()._asdict(),
                "memory_percent": process.memory_percent(),
                "num_threads": process.num_threads(),
                "num_fds": process.num_fds() if hasattr(process, "num_fds") else None,
                "create_time": process.create_time(),
                "status": process.status(),
            }
        except (OSError, ValueError, AttributeError, ImportError) as e:
            if self.logger:
                self.logger.warning("Failed to collect process metrics: %s", e)
            # Return empty dict but log the failure for debugging
            return {"error": f"Failed to collect process metrics: {e}"}

    def _collect_oracle_metrics(self) -> dict[str, Any]:
        """Collect Oracle database metrics."""
        metrics: dict[str, Any] = {}

        # Connection pool metrics
        try:
            if hasattr(self, "_engine") and self._engine:
                pool = getattr(self._engine, "pool", None)
                if not pool:
                    return metrics
                metrics["connection_pool"] = {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                    "invalid": pool.invalid(),
                }
        except (OSError, ValueError, AttributeError, ImportError) as e:
            if self.logger:
                self.logger.debug("Could not collect pool metrics: %s", e)

        # Database session metrics (if connection available)
        try:
            db_metrics = self._collect_database_session_metrics()
            if db_metrics:
                metrics["database"] = db_metrics
        except (OSError, ValueError, AttributeError, ImportError) as e:
            if self.logger:
                self.logger.debug("Could not collect database metrics: %s", e)

        return metrics

    def _collect_database_session_metrics(self) -> dict[str, Any] | None:
        """Collect Oracle database session metrics."""
        if not hasattr(self, "_engine") or not self._engine:
            return None

        try:
            # Type ignore for dynamic engine object
            with self._engine.connect() as conn:  # type: ignore[attr-defined]
                # Session information
                result = conn.execute(
                    text(
                        """
                    SELECT
                        SID,
                        SERIAL#,
                        STATUS,
                        PROGRAM,
                        MACHINE,
                        LOGON_TIME
                    FROM V$SESSION
                    WHERE AUDSID = USERENV('SESSIONID')
                """,
                    ),
                )
                session_info = result.fetchone()

                # Memory usage
                memory_result = conn.execute(
                    text(
                        """
                    SELECT
                        NAME,
                        VALUE
                    FROM V$MYSTAT ms, V$STATNAME sn
                    WHERE ms.STATISTIC# = sn.STATISTIC#
                    AND sn.NAME IN ('session pga memory', 'session uga memory')
                """,
                    ),
                )
                memory_stats = dict(memory_result.fetchall())

                # Wait events
                wait_result = conn.execute(
                    text(
                        """
                    SELECT
                        EVENT,
                        TOTAL_WAITS,
                        TIME_WAITED
                    FROM V$SESSION_EVENT
                    WHERE SID = (SELECT SID FROM V$SESSION "
                    "WHERE AUDSID = USERENV('SESSIONID'))
                    AND TOTAL_WAITS > 0
                    ORDER BY TIME_WAITED DESC
                    FETCH FIRST 5 ROWS ONLY
                """,
                    ),
                )
                wait_events = [dict(row._asdict()) for row in wait_result.fetchall()]

                return {
                    "session": dict(session_info._asdict()) if session_info else {},
                    "memory": memory_stats,
                    "wait_events": wait_events,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

        except (OSError, ValueError, AttributeError, ImportError) as e:
            if self.logger:
                self.logger.debug("Database metrics collection failed: %s", e)
            # Return None but log the failure for debugging
            return {"error": f"Database metrics collection failed: {e}"}

    def _collect_performance_metrics(self) -> dict[str, Any]:
        """Collect performance-related metrics."""
        metrics = {}

        # Get performance data from logger if available
        if (hasattr(self, "logger") and self.logger and
                hasattr(self.logger, "performance_counters")):
            counters = self.logger.performance_counters

            session_duration = time.time() - getattr(
                self.logger, "start_time", time.time(),
            )

            metrics = {
                "session_duration": session_duration,
                "total_records": counters.get("total_records", 0),
                "total_batches": counters.get("total_batches", 0),
                "total_errors": counters.get("total_errors", 0),
                "streams_count": len(counters.get("streams_processed", set())),
            }

            # Calculate rates
            if session_duration > 0:
                metrics["records_per_second"] = (
                    metrics["total_records"] / session_duration
                )
                metrics["batches_per_second"] = (
                    metrics["total_batches"] / session_duration
                )

            # Calculate error rate
            if metrics["total_records"] > 0:
                metrics["error_rate_percent"] = (
                    metrics["total_errors"] / metrics["total_records"]
                ) * 100
            else:
                metrics["error_rate_percent"] = 0

        return metrics

    def _check_thresholds(self, metrics: dict[str, Any]) -> None:
        """Check metrics against alert thresholds."""
        alerts = []

        # Memory threshold
        memory_percent = metrics.get("system", {}).get("memory", {}).get("percent", 0)
        if memory_percent > self.thresholds["memory_usage_percent"]:
            alert_key = f"memory_high_{int(memory_percent)}"
            if alert_key not in self.alerts_sent:
                alerts.append(
                    {
                        "type": "memory_usage_high",
                        "severity": "warning",
                        "message": f"Memory usage is {memory_percent:.1f}%",
                        "value": memory_percent,
                        "threshold": self.thresholds["memory_usage_percent"],
                    },
                )
                self.alerts_sent.add(alert_key)

        # CPU threshold
        cpu_percent = metrics.get("system", {}).get("cpu", {}).get("percent", 0)
        if cpu_percent > self.thresholds["cpu_usage_percent"]:
            alert_key = f"cpu_high_{int(cpu_percent)}"
            if alert_key not in self.alerts_sent:
                alerts.append(
                    {
                        "type": "cpu_usage_high",
                        "severity": "warning",
                        "message": f"CPU usage is {cpu_percent:.1f}%",
                        "value": cpu_percent,
                        "threshold": self.thresholds["cpu_usage_percent"],
                    },
                )
                self.alerts_sent.add(alert_key)

        # Connection pool threshold
        pool_metrics = metrics.get("oracle", {}).get("connection_pool", {})
        if pool_metrics:
            pool_size = pool_metrics.get("size", 0)
            checked_out = pool_metrics.get("checked_out", 0)
            if pool_size > 0:
                pool_usage = (checked_out / pool_size) * 100
                if pool_usage > self.thresholds["connection_pool_usage"]:
                    alert_key = f"pool_high_{int(pool_usage)}"
                    if alert_key not in self.alerts_sent:
                        alerts.append(
                            {
                                "type": "connection_pool_usage_high",
                                "severity": "critical",
                                "message": (
                                    f"Connection pool usage is {pool_usage:.1f}%"
                                ),
                                "value": pool_usage,
                                "threshold": self.thresholds["connection_pool_usage"],
                            },
                        )
                        self.alerts_sent.add(alert_key)

        # Error rate threshold
        error_rate = metrics.get("performance", {}).get("error_rate_percent", 0)
        if error_rate > self.thresholds["error_rate_percent"]:
            alert_key = f"error_rate_high_{int(error_rate)}"
            if alert_key not in self.alerts_sent:
                alerts.append(
                    {
                        "type": "error_rate_high",
                        "severity": "critical",
                        "message": f"Error rate is {error_rate:.2f}%",
                        "value": error_rate,
                        "threshold": self.thresholds["error_rate_percent"],
                    },
                )
                self.alerts_sent.add(alert_key)

        # Send alerts
        for alert in alerts:
            self._send_alert(alert)

    def _send_alert(self, alert: dict[str, Any]) -> None:
        """Send alert notification."""
        alert["timestamp"] = datetime.now(timezone.utc).isoformat()

        if self.logger:
            level = "critical" if alert["severity"] == "critical" else "warning"
            getattr(self.logger, level)(
                f"ALERT: {alert['message']}", extra={"alert": alert},
            )

        # Integration with external alerting systems
        webhook_url = self.config.get("alert_webhook_url")
        if webhook_url:
            self._send_webhook_alert(webhook_url, alert)

    def _send_webhook_alert(self, webhook_url: str, alert: dict[str, Any]) -> None:
        """Send alert to webhook endpoint."""
        try:
            import requests

            payload = {
                "text": f"Oracle Target Alert: {alert['message']}",
                "alert": alert,
                "service": "flext-target-oracle",
            }

            requests.post(webhook_url, json=payload, timeout=10)

        except (OSError, ValueError, AttributeError, ImportError):
            if self.logger:
                self.logger.exception("Failed to send webhook alert")

    def _store_metrics(self, metrics: dict[str, Any]) -> None:
        """Store metrics in history."""
        self.metrics_history.append(metrics)

        # Keep only recent metrics
        max_history = self.config.get("metrics_history_size", 100)
        if len(self.metrics_history) > max_history:
            self.metrics_history = self.metrics_history[-max_history:]

    @contextmanager
    def health_check_context(self) -> Generator[dict[str, Any], None, None]:
        """Context manager for health checks."""
        start_time = time.time()
        status = "healthy"
        error = None

        try:
            context = {"start_time": start_time, "status": status}
            yield context
        except (OSError, ValueError, AttributeError, ImportError) as e:
            status = "unhealthy"
            error = str(e)
            raise
        finally:
            duration = time.time() - start_time
            self.last_health_check = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "duration": duration,
                "error": error,
            }

    def perform_health_check(self) -> dict[str, Any]:
        """Perform comprehensive health check."""
        health_status: dict[str, Any] = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "checks": {},
        }

        # System health
        try:
            with self.health_check_context():
                system_metrics = self._collect_system_metrics()
                memory_percent = system_metrics.get("memory", {}).get("percent", 0)
                cpu_percent = system_metrics.get("cpu", {}).get("percent", 0)

                health_status["checks"]["system"] = {
                    "status": (
                        "healthy"
                        if memory_percent < HEALTH_MEMORY_THRESHOLD and cpu_percent < HEALTH_CPU_THRESHOLD
                        else "degraded"
                    ),
                    "memory_percent": memory_percent,
                    "cpu_percent": cpu_percent,
                }
        except (OSError, ValueError, AttributeError, ImportError) as e:
            health_status["checks"]["system"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "unhealthy"

        # Database connectivity
        try:
            with self.health_check_context():
                db_health = self._check_database_health()
                health_status["checks"]["database"] = db_health
                if db_health["status"] != "healthy":
                    health_status["status"] = "degraded"
        except (OSError, ValueError, AttributeError, ImportError) as e:
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health_status["status"] = "unhealthy"

        # Performance check
        try:
            perf_metrics = self._collect_performance_metrics()
            error_rate = perf_metrics.get("error_rate_percent", 0)

            health_status["checks"]["performance"] = {
                "status": "healthy" if error_rate < HEALTH_ERROR_RATE_THRESHOLD else "degraded",
                "error_rate": error_rate,
                "total_records": perf_metrics.get("total_records", 0),
            }
        except (OSError, ValueError, AttributeError, ImportError) as e:
            health_status["checks"]["performance"] = {
                "status": "unknown",
                "error": str(e),
            }

        return health_status

    def _check_database_health(self) -> dict[str, Any]:
        """Check Oracle database health."""
        if not hasattr(self, "_engine") or not self._engine:
            return {
                "status": "unknown",
                "message": "No database connection available",
            }

        try:
            start_time = time.time()

            # Type ignore for dynamic engine object
            with self._engine.connect() as conn:  # type: ignore[attr-defined]
                # Simple connectivity test
                result = conn.execute(text("SELECT 1 FROM DUAL"))
                if result.scalar() != 1:
                    msg = "Invalid response from database"
                    raise Exception(msg)

                # Check database status
                status_result = conn.execute(
                    text(
                        """
                    SELECT STATUS FROM V$INSTANCE
                """,
                    ),
                )
                db_status = status_result.scalar()

                response_time = (time.time() - start_time) * 1000  # ms

                return {
                    "status": "healthy" if db_status == "OPEN" else "degraded",
                    "database_status": db_status,
                    "response_time_ms": response_time,
                    "connection_test": "passed",
                }

        except (OSError, ValueError, AttributeError, ImportError) as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection_test": "failed",
            }

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get summary of recent metrics."""
        if not self.metrics_history:
            return {"error": "No metrics available"}

        latest = self.metrics_history[-1]

        # Calculate averages from recent history
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements

        avg_memory = sum(
            m.get("system", {}).get("memory", {}).get("percent", 0)
            for m in recent_metrics
        ) / len(recent_metrics)

        avg_cpu = sum(
            m.get("system", {}).get("cpu", {}).get("percent", 0) for m in recent_metrics
        ) / len(recent_metrics)

        return {
            "timestamp": latest["timestamp"],
            "latest": latest,
            "averages": {
                "memory_percent": avg_memory,
                "cpu_percent": avg_cpu,
            },
            "history_size": len(self.metrics_history),
            "alerts_sent": len(self.alerts_sent),
        }

    def set_engine(self, engine: Union[object, Engine]) -> None:
        """Set SQLAlchemy engine for database monitoring."""
        self._engine = engine

    def cleanup(self) -> None:
        """Clean up monitoring resources silently."""
        # Stop monitoring without logging to avoid shutdown errors
        if hasattr(self, "_monitoring_thread") and self._monitoring_thread:
            if hasattr(self, "shutdown_event"):
                self.shutdown_event.set()
            if self._monitoring_thread.is_alive():
                self._monitoring_thread.join(timeout=1)

        # Clear resources without logging
        self._monitoring_thread = None


def create_monitor(
    config: dict[str, Any], logger: logging.Logger | None = None,
) -> OracleTargetMonitor:
    """Factory function to create configured monitor."""
    return OracleTargetMonitor(config, logger)
