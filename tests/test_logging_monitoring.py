"""
Tests for comprehensive logging and monitoring system.

These tests validate the logging configuration, monitoring capabilities,
metrics collection, and observability features.
"""

from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from flext_target_oracle.logging_config import (
    JsonFormatter,
    PerformanceTimer,
    create_logger,
)
from flext_target_oracle.monitoring import create_monitor


@pytest.mark.unit
class TestLoggingConfiguration:
    """Test logging configuration and functionality."""

    def test_logger_initialization(self):
        """Test logger initialization with various configurations."""
        # Basic configuration
        config = {
            "log_level": "INFO",
            "log_format": "json",
            "enable_metrics": True,
        }

        logger = create_logger(config)

        assert logger is not None
        assert logger.logger_name == "flext_target_oracle"
        assert logger.log_level == 20  # INFO level
        assert logger.session_id is not None
        assert logger.start_time > 0

    def test_logger_with_file_output(self):
        """Test logger with file output configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"

            config = {
                "log_level": "DEBUG",
                "log_format": "json",
                "log_file": str(log_file),
                "log_max_bytes": 1024 * 1024,
                "log_backup_count": 3,
            }

            logger = create_logger(config)
            logger.info("Test log message", extra={"test_key": "test_value"})

            # Verify log file was created and contains message
            assert log_file.exists()

            with open(log_file) as f:
                log_content = f.read()
                assert "Test log message" in log_content
                assert "test_key" in log_content

    def test_structured_logging_context(self):
        """Test structured logging with operation context."""
        config = {
            "log_level": "INFO",
            "log_format": "json",
            "enable_metrics": True,
        }

        logger = create_logger(config)

        # Test operation context
        with logger.operation_context(
            "test_operation", stream="test_stream", batch_size=100
        ) as context:
            assert context["operation"] == "test_operation"
            assert context["stream"] == "test_stream"
            assert context["batch_size"] == 100
            assert "operation_id" in context
            assert "session_id" in context

    def test_logging_levels_and_methods(self):
        """Test all logging levels and methods."""
        config = {"log_level": "DEBUG"}
        logger = create_logger(config)

        # Capture log output
        with patch.object(logger.logger, "log") as mock_log:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")

            # Verify all levels were called
            assert mock_log.call_count == 5

    def test_record_batch_logging(self):
        """Test batch processing logging with metrics."""
        config = {"enable_metrics": True}
        logger = create_logger(config)

        # Log several batches
        logger.log_record_batch("test_stream", 1000, "insert")
        logger.log_record_batch("test_stream", 2000, "upsert")
        logger.log_record_batch("other_stream", 500, "insert")

        # Verify performance counters
        assert logger.performance_counters["total_records"] == 3500
        assert logger.performance_counters["total_batches"] == 3
        assert len(logger.performance_counters["streams_processed"]) == 2

    def test_performance_statistics(self):
        """Test performance statistics collection."""
        config = {"enable_metrics": True}
        logger = create_logger(config)

        # Simulate some activity
        time.sleep(0.1)  # Ensure session duration > 0
        logger.log_record_batch("stream1", 1000)
        logger.log_record_batch("stream2", 2000)

        stats = logger.log_performance_stats()

        assert stats["session_id"] == logger.session_id
        assert stats["total_records"] == 3000
        assert stats["total_batches"] == 2
        assert stats["streams_count"] == 2
        assert "records_per_second" in stats
        assert stats["records_per_second"] > 0

    def test_oracle_connection_logging(self):
        """Test Oracle connection information logging."""
        config = {}
        logger = create_logger(config)

        connection_info = {
            "host": "localhost",
            "port": 1521,
            "service_name": "XE",
            "username": "test_user",
            "password": "secret_password",  # Should be redacted
            "wallet_password": "secret_wallet",  # Should be redacted
        }

        with patch.object(logger.logger, "info") as mock_info:
            logger.log_oracle_connection_info(connection_info)

            # Verify sensitive info was redacted
            call_args = mock_info.call_args
            extra_data = call_args.kwargs["extra"]
            connection_data = extra_data["connection_info"]

            assert connection_data["password"] == "***REDACTED***"
            assert connection_data["wallet_password"] == "***REDACTED***"
            assert connection_data["username"] == "test_user"  # Not sensitive

    def test_sql_statement_logging(self):
        """Test SQL statement logging functionality."""
        config = {"log_sql_statements": True}
        logger = create_logger(config)

        with patch.object(logger.logger, "debug") as mock_debug:
            logger.log_sql_statement(
                "SELECT * FROM test_table WHERE id = :id",
                params={"id": 123},
                duration=0.045,
            )

            call_args = mock_debug.call_args
            extra_data = call_args.kwargs["extra"]

            assert "sql" in extra_data
            assert extra_data["params_count"] == 1
            assert extra_data["duration"] == 0.045

    def test_json_formatter(self):
        """Test JSON log formatter."""
        formatter = JsonFormatter()

        # Create a mock log record
        import logging

        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Add extra fields
        record.custom_field = "custom_value"
        record.session_id = "test_session"

        formatted = formatter.format(record)
        log_data = json.loads(formatted)

        assert log_data["message"] == "Test message"
        assert log_data["level"] == "INFO"
        assert log_data["custom_field"] == "custom_value"
        assert log_data["session_id"] == "test_session"
        assert "timestamp" in log_data

    def test_performance_timer(self):
        """Test performance timer functionality."""
        config = {}
        logger = create_logger(config)

        # Test as context manager
        with PerformanceTimer(logger, "test_operation") as timer:
            time.sleep(0.01)  # Small delay

        assert timer.duration is not None
        assert timer.duration > 0.005  # Should be at least 5ms

        # Test manual start/stop
        timer2 = PerformanceTimer(logger, "manual_test")
        timer2.start()
        time.sleep(0.01)
        timer2.stop()

        assert timer2.duration is not None
        assert timer2.duration > 0.005


@pytest.mark.unit
class TestMonitoringSystem:
    """Test monitoring system functionality."""

    def test_monitor_initialization(self):
        """Test monitor initialization."""
        config = {
            "enable_monitoring": True,
            "monitoring_interval": 10,
            "memory_threshold": 80,
            "cpu_threshold": 75,
        }

        monitor = create_monitor(config)

        assert monitor.enabled is True
        assert monitor.check_interval == 10
        assert monitor.thresholds["memory_usage_percent"] == 80
        assert monitor.thresholds["cpu_usage_percent"] == 75

    def test_monitor_disabled(self):
        """Test monitor when disabled."""
        config = {"enable_monitoring": False}
        monitor = create_monitor(config)

        assert monitor.enabled is False

    def test_system_metrics_collection(self):
        """Test system metrics collection."""
        config = {"enable_monitoring": True}
        monitor = create_monitor(config)

        metrics = monitor._collect_system_metrics()

        assert "memory" in metrics
        assert "cpu" in metrics
        assert "disk" in metrics

        # Memory metrics
        memory = metrics["memory"]
        assert "total" in memory
        assert "used" in memory
        assert "percent" in memory
        assert isinstance(memory["percent"], (int, float))

        # CPU metrics
        cpu = metrics["cpu"]
        assert "percent" in cpu
        assert "count" in cpu

    def test_process_metrics_collection(self):
        """Test process-specific metrics collection."""
        config = {"enable_monitoring": True}
        monitor = create_monitor(config)

        metrics = monitor._collect_process_metrics()

        assert "pid" in metrics
        assert "memory_info" in metrics
        assert "cpu_percent" in metrics
        assert "num_threads" in metrics
        assert "status" in metrics

    def test_performance_metrics_collection(self):
        """Test performance metrics collection."""
        config = {"enable_monitoring": True}
        logger = create_logger({"enable_metrics": True})
        monitor = create_monitor(config, logger)

        # Simulate some activity
        logger.log_record_batch("test_stream", 1000)
        logger.log_record_batch("test_stream", 2000)

        metrics = monitor._collect_performance_metrics()

        assert "total_records" in metrics
        assert "total_batches" in metrics
        assert "streams_count" in metrics
        assert metrics["total_records"] == 3000
        assert metrics["total_batches"] == 2

    def test_health_check(self):
        """Test comprehensive health check."""
        config = {"enable_monitoring": True}
        monitor = create_monitor(config)

        health = monitor.perform_health_check()

        assert "status" in health
        assert "timestamp" in health
        assert "checks" in health

        checks = health["checks"]
        assert "system" in checks
        assert "performance" in checks

        # System check should have status
        system_check = checks["system"]
        assert "status" in system_check

    def test_threshold_checking(self):
        """Test alert threshold checking."""
        config = {
            "enable_monitoring": True,
            "memory_threshold": 50,  # Low threshold for testing
            "cpu_threshold": 50,
        }

        logger = create_logger({"enable_metrics": True})
        monitor = create_monitor(config, logger)

        # Mock high resource usage
        high_usage_metrics = {
            "system": {
                "memory": {"percent": 75},  # Above threshold
                "cpu": {"percent": 60},  # Above threshold
            },
            "performance": {
                "error_rate_percent": 2,  # Below threshold
            },
        }

        with patch.object(monitor, "_send_alert") as mock_alert:
            monitor._check_thresholds(high_usage_metrics)

            # Should send alerts for memory and CPU
            assert mock_alert.call_count >= 1

    def test_metrics_history_management(self):
        """Test metrics history storage and management."""
        config = {
            "enable_monitoring": True,
            "metrics_history_size": 5,  # Small size for testing
        }

        monitor = create_monitor(config)

        # Add more metrics than the history size
        for i in range(10):
            metrics = {"timestamp": f"time_{i}", "value": i}
            monitor._store_metrics(metrics)

        # Should only keep the latest 5
        assert len(monitor.metrics_history) == 5
        assert monitor.metrics_history[-1]["value"] == 9  # Latest
        assert monitor.metrics_history[0]["value"] == 5  # Oldest kept

    def test_background_monitoring(self):
        """Test background monitoring thread."""
        config = {
            "enable_monitoring": True,
            "monitoring_interval": 0.1,  # Fast interval for testing
            "background_monitoring": True,
        }

        monitor = create_monitor(config)

        # Start background monitoring
        monitor.start_background_monitoring()

        # Verify thread is running
        assert monitor.monitoring_thread is not None
        assert monitor.monitoring_thread.is_alive()

        # Wait a bit for some metrics collection
        time.sleep(0.2)

        # Stop monitoring
        monitor.stop_background_monitoring()

        # Verify thread stopped
        assert not monitor.monitoring_thread.is_alive()

        # Should have collected some metrics
        assert len(monitor.metrics_history) > 0

    def test_webhook_alert_integration(self):
        """Test webhook alert integration."""
        config = {
            "enable_monitoring": True,
            "alert_webhook_url": "https://hooks.example.com/webhook",
        }

        monitor = create_monitor(config)

        alert = {
            "type": "test_alert",
            "severity": "warning",
            "message": "Test alert message",
            "value": 85,
            "threshold": 80,
        }

        with patch("requests.post") as mock_post:
            monitor._send_webhook_alert(config["alert_webhook_url"], alert)

            # Verify webhook was called
            mock_post.assert_called_once()
            call_args = mock_post.call_args

            assert call_args[0][0] == config["alert_webhook_url"]
            payload = call_args.kwargs["json"]
            assert "alert" in payload
            assert payload["service"] == "flext-target-oracle"


@pytest.mark.integration
class TestLoggingMonitoringIntegration:
    """Test integration between logging and monitoring systems."""

    def test_logger_monitor_integration(self):
        """Test integration between logger and monitor."""
        config = {
            "enable_monitoring": True,
            "enable_metrics": True,
            "log_level": "INFO",
        }

        logger = create_logger(config)
        monitor = create_monitor(config, logger)

        # Simulate activity
        with logger.operation_context("test_operation", stream="test_stream"):
            logger.log_record_batch("test_stream", 1000)
            time.sleep(0.01)

        # Monitor should be able to collect performance metrics from logger
        metrics = monitor._collect_performance_metrics()

        assert metrics["total_records"] == 1000
        assert metrics["total_batches"] == 1
        assert "records_per_second" in metrics

    def test_full_observability_stack(self):
        """Test complete observability stack."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "oracle_target.log"

            config = {
                "enable_monitoring": True,
                "enable_metrics": True,
                "log_level": "INFO",
                "log_format": "json",
                "log_file": str(log_file),
                "monitoring_interval": 0.1,
                "memory_threshold": 50,
            }

            logger = create_logger(config)
            monitor = create_monitor(config, logger)

            # Simulate Oracle target activity
            with logger.operation_context("data_loading", stream="orders"):
                logger.log_record_batch("orders", 5000, "insert")
                logger.log_oracle_performance(
                    {
                        "pool_size": 10,
                        "memory_usage_mb": 256,
                    }
                )

                # Collect monitoring metrics
                metrics = monitor.collect_metrics()

                # Verify comprehensive metrics
                assert "system" in metrics
                assert "process" in metrics
                assert "performance" in metrics

                # Verify performance data
                perf_metrics = metrics["performance"]
                assert perf_metrics["total_records"] == 5000
                assert perf_metrics["total_batches"] == 1

            # Verify log file contains structured data
            assert log_file.exists()
            with open(log_file) as f:
                log_lines = f.readlines()

            # Parse JSON logs
            log_entries = [json.loads(line) for line in log_lines if line.strip()]

            # Should have operation start, batch log, performance log, and operation end
            assert len(log_entries) >= 3

            # Verify structured logging data
            operation_logs = [entry for entry in log_entries if "operation" in entry]
            assert len(operation_logs) >= 2  # Start and end

    def test_health_check_with_logging(self):
        """Test health check with comprehensive logging."""
        config = {
            "enable_monitoring": True,
            "log_level": "DEBUG",
        }

        logger = create_logger(config)
        monitor = create_monitor(config, logger)

        with patch.object(logger, "info"):
            health = monitor.perform_health_check()

            # Health check should log results
            assert health["status"] in ["healthy", "degraded", "unhealthy"]
            assert "checks" in health

    def test_error_tracking_integration(self):
        """Test error tracking between logging and monitoring."""
        config = {
            "enable_monitoring": True,
            "enable_metrics": True,
            "error_rate_threshold": 1,  # Low threshold for testing
        }

        logger = create_logger(config)
        monitor = create_monitor(config, logger)

        # Simulate errors
        logger.performance_counters["total_records"] = 100
        logger.performance_counters["total_errors"] = 5  # 5% error rate

        metrics = monitor.collect_metrics()

        # Should detect high error rate
        error_rate = metrics["performance"]["error_rate_percent"]
        assert error_rate == 5.0

        # Should trigger alert
        with patch.object(monitor, "_send_alert") as mock_alert:
            monitor._check_thresholds(metrics)

            # Should send error rate alert
            assert mock_alert.call_count >= 1
