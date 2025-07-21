"""Test observability and metrics functionality.

Tests for the metrics collection and monitoring infrastructure.
"""

import time
from unittest.mock import Mock, patch

from flext_target_oracle.monitoring import MetricsCollector, PerformanceTracker
from flext_target_oracle.observability.metrics import (
    DatabaseMetrics,
    HealthStatus,
    RecordMetrics,
)


class TestHealthStatus:
    """Test HealthStatus enum."""

    def test_health_status_values(self) -> None:
        """Test health status enum values."""
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.WARNING.value == "warning"
        assert HealthStatus.CRITICAL.value == "critical"
        assert HealthStatus.UNKNOWN.value == "unknown"


class TestDatabaseMetrics:
    """Test database metrics collection."""

    def test_database_metrics_creation(self) -> None:
        """Test database metrics object creation."""
        metrics = DatabaseMetrics(
            connections_active=5,
            connections_total=10,
            query_duration_avg=0.5,
            query_success_rate=95.5,
        )

        assert metrics.connections_active == 5
        assert metrics.connections_total == 10
        assert metrics.query_duration_avg == 0.5
        assert metrics.query_success_rate == 95.5


class TestRecordMetrics:
    """Test record processing metrics."""

    def test_record_metrics_creation(self) -> None:
        """Test record metrics object creation."""
        metrics = RecordMetrics(
            records_processed=1000,
            records_failed=5,
            processing_rate=250.0,
            batch_size_avg=100,
        )

        assert metrics.records_processed == 1000
        assert metrics.records_failed == 5
        assert metrics.processing_rate == 250.0
        assert metrics.batch_size_avg == 100


class TestMetricsCollector:
    """Test MetricsCollector functionality."""

    def test_metrics_collector_initialization(self) -> None:
        """Test metrics collector initialization."""
        collector = MetricsCollector()
        # Test initialization through public interface
        assert collector.get_all_metrics() == {}
        # Test that max_history parameter works through constructor
        collector_custom = MetricsCollector(max_history=500)
        assert collector_custom.get_all_metrics() == {}

    def test_record_metric(self) -> None:
        """Test recording a single metric."""
        collector = MetricsCollector()
        collector.record_metric("test_metric", 42.5)

        metrics = collector.get_all_metrics()
        assert "test_metric" in metrics
        assert metrics["test_metric"]["count"] == 1
        assert metrics["test_metric"]["latest"] == 42.5

    def test_multiple_metrics(self) -> None:
        """Test recording multiple metrics."""
        collector = MetricsCollector()
        collector.record_metric("metric1", 10)
        collector.record_metric("metric1", 20)
        collector.record_metric("metric2", 30)

        metrics = collector.get_all_metrics()
        assert metrics["metric1"]["count"] == 2
        assert metrics["metric1"]["avg"] == 15.0
        assert metrics["metric2"]["count"] == 1
        assert metrics["metric2"]["latest"] == 30

    def test_get_metric_stats(self) -> None:
        """Test getting statistics for a specific metric."""
        collector = MetricsCollector()
        collector.record_metric("test", 5)
        collector.record_metric("test", 10)
        collector.record_metric("test", 15)

        stats = collector.get_metric_stats("test")
        assert stats["count"] == 3
        assert stats["min"] == 5
        assert stats["max"] == 15
        assert stats["avg"] == 10.0
        assert stats["sum"] == 30

    def test_get_metric_stats_nonexistent(self) -> None:
        """Test getting stats for non-existent metric."""
        collector = MetricsCollector()
        stats = collector.get_metric_stats("nonexistent")
        assert stats == {}

    def test_history_limit(self) -> None:
        """Test that metrics history is limited."""
        collector = MetricsCollector(max_history=3)

        for i in range(5):
            collector.record_metric("test", i)

        stats = collector.get_metric_stats("test")
        assert stats["count"] == 3  # Limited to max_history
        assert stats["first"] == 2  # First value in limited history
        assert stats["latest"] == 4  # Last value recorded


class TestPerformanceTracker:
    """Test PerformanceTracker functionality."""

    def test_performance_tracker_initialization(self) -> None:
        """Test performance tracker initialization."""
        tracker = PerformanceTracker()
        assert tracker.operation_name == ""
        assert tracker.start_time is None

    def test_context_manager(self) -> None:
        """Test performance tracker as context manager."""
        with PerformanceTracker("test_operation") as tracker:
            assert tracker.operation_name == "test_operation"
            assert tracker.start_time is not None
            time.sleep(0.01)  # Small delay to measure

        # After context, duration should be available
        assert tracker.duration > 0
        assert tracker.duration < 1.0  # Should be very small

    def test_manual_start_stop(self) -> None:
        """Test manual start and stop."""
        tracker = PerformanceTracker("manual_test")
        tracker.start()
        assert tracker.start_time is not None

        time.sleep(0.01)
        tracker.stop()

        assert tracker.duration > 0
        assert tracker.duration < 1.0

    def test_get_duration_without_stop(self) -> None:
        """Test getting duration without explicit stop."""
        tracker = PerformanceTracker("test")
        tracker.start()
        time.sleep(0.01)

        duration = tracker.get_duration()
        assert duration > 0
        assert duration < 1.0

    @patch("flext_target_oracle.monitoring.logger")
    def test_logging_integration(self, mock_logger: Mock) -> None:
        """Test that performance is logged."""
        with PerformanceTracker("logged_operation"):
            time.sleep(0.01)

        # Should have logged the duration
        mock_logger.info.assert_called()
        call_args = mock_logger.info.call_args[0]
        # With f-string formatting, all info is in the single string argument
        assert len(call_args) == 1  # Single formatted string
        log_message = call_args[0]
        assert "Operation" in log_message
        assert "duration" in log_message
        assert "logged_operation" in log_message


class TestMetricsIntegration:
    """Test integration between metrics components."""

    def test_metrics_and_performance_integration(self) -> None:
        """Test metrics collection with performance tracking."""
        collector = MetricsCollector()

        with PerformanceTracker("db_operation") as tracker:
            time.sleep(0.01)

        # Record the performance metric
        collector.record_metric("operation_duration", tracker.duration)

        metrics = collector.get_all_metrics()
        assert "operation_duration" in metrics
        assert metrics["operation_duration"]["count"] == 1
        assert metrics["operation_duration"]["latest"] > 0

    def test_health_status_based_on_metrics(self) -> None:
        """Test determining health status based on metrics."""
        collector = MetricsCollector()

        # Good performance metrics
        collector.record_metric("success_rate", 99.5)
        collector.record_metric("response_time", 0.1)

        metrics = collector.get_all_metrics()
        success_rate = metrics["success_rate"]["latest"]
        response_time = metrics["response_time"]["latest"]

        # Simple health determination logic
        if success_rate > 95 and response_time < 1.0:
            status = HealthStatus.HEALTHY
        elif success_rate > 90 and response_time < 2.0:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        assert status == HealthStatus.HEALTHY
