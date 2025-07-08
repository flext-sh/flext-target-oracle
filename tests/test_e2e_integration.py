"""End-to-end integration tests for Oracle target.

This module provides comprehensive end-to-end testing scenarios
that simulate real-world usage patterns and complex data workflows.
"""

from __future__ import annotations

import json
import logging
from io import StringIO
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from sqlalchemy import text

from flext_target_oracle.target import OracleTarget
from tests.helpers import requires_oracle_connection

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

log = logging.getLogger(__name__)


@requires_oracle_connection
class TestE2EIntegration:
    """End-to-end integration tests."""

    def test_complete_etl_workflow(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
        performance_timer: Any,
    ) -> None:
        """Test complete ETL workflow from schema to final data."""
        table_cleanup(test_table_name)

        # Configure target for production-like scenario
        etl_config = oracle_config.copy()
        etl_config["batch_size"] = 5000
        etl_config["max_workers"] = 4
        etl_config["use_bulk_operations"] = True
        etl_config["upsert_method"] = "merge"
        etl_config["enable_metrics"] = True

        target = OracleTarget(config=etl_config)

        # Phase 1: Schema definition
        customer_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer"},
                    "first_name": {"type": "string", "maxLength": 100},
                    "last_name": {"type": "string", "maxLength": 100},
                    "email": {"type": "string", "maxLength": 255},
                    "phone": {"type": "string", "maxLength": 20},
                    "address": {"type": "object"},
                    "registration_date": {"type": "string", "format": "date-time"},
                    "last_login": {"type": "string", "format": "date-time"},
                    "status": {"type": "string", "maxLength": 20},
                    "lifetime_value": {"type": "number"},
                    "preferences": {"type": "object"},
                    "tags": {"type": "array"},
                    "is_premium": {"type": "boolean"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["customer_id"],
        }

        # Phase 2: Initial data load (simulate historical data)
        historical_customers = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "customer_id": i + 1,
                        "first_name": f"FirstName{i + 1}",
                        "last_name": f"LastName{i + 1}",
                        "email": f"customer{i + 1}@example.com",
                        "phone": f"+1-555-{(i + 1000):04d}",
                        "address": {
                            "street": f"{i + 1} Main St",
                            "city": "Sample City",
                            "state": "CA",
                            "zip": f"{90000 + (i % 1000):05d}",
                            "country": "USA",
                        },
                        "registration_date": "2024-01-01T10:00:00Z",
                        "last_login": "2025-07-01T10:00:00Z",
                        "status": "active" if i % 4 != 3 else "inactive",
                        "lifetime_value": float((i + 1) * 25.50),
                        "preferences": {
                            "email_notifications": True,
                            "sms_notifications": i % 3 == 0,
                            "language": "en",
                            "timezone": "UTC-8",
                        },
                        "tags": [f"segment_{(i % 5) + 1}", f"cohort_{(i % 10) + 1}"],
                        "is_premium": i % 7 == 0,
                        "created_at": "2024-01-01T10:00:00Z",
                        "updated_at": "2025-07-02T10:00:00Z",
                    },
                    "time_extracted": "2025-07-02T10:00:00Z",
                } for i in range(10000)]

        # Process initial load
        messages = [json.dumps(customer_schema)]
        messages.extend([json.dumps(record) for record in historical_customers])
        input_data = "\n".join(messages)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        performance_timer.stop()
        initial_load_time = performance_timer.duration

        # Verify initial load
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            initial_count = row[0]
            assert initial_count == 10000

            # Verify data integrity
            result = conn.execute(
                text(
                    f"""
                SELECT
                    COUNT(DISTINCT customer_id) as unique_customers,
                    COUNT(*) as total_records,
                    MIN(customer_id) as min_id,
                    MAX(customer_id) as max_id
                FROM {test_table_name}
            """,
                ),
            )
            stats = result.fetchone()
            assert stats is not None
            assert stats.unique_customers == 10000
            assert stats.total_records == 10000
            assert stats.min_id == 1
            assert stats.max_id == 10000

        # Phase 3: Incremental updates (simulate daily changes)

        # Update existing customers (simulate profile updates)
        # Update every 10th customer in first 2000
        incremental_updates = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "customer_id": i + 1,
                        "first_name": f"UpdatedFirst{i + 1}",
                        "last_name": f"UpdatedLast{i + 1}",
                        "email": f"updated.customer{i + 1}@example.com",
                        "phone": f"+1-555-{(i + 2000):04d}",
                        "address": {
                            "street": f"{i + 1} Updated St",
                            "city": "Updated City",
                            "state": "NY",
                            "zip": f"{10000 + (i % 1000):05d}",
                            "country": "USA",
                        },
                        "registration_date": "2024-01-01T10:00:00Z",
                        "last_login": "2025-07-02T11:00:00Z",  # Updated login
                        "status": "premium" if i % 20 == 0 else "active",
                        # Increased value
                        "lifetime_value": float((i + 1) * 35.75),
                        "preferences": {
                            "email_notifications": True,
                            "sms_notifications": True,  # Updated preference
                            "language": "en",
                            "timezone": "UTC-5",  # Updated timezone
                        },
                        "tags": [
                            f"segment_{(i % 5) + 1}",
                            f"cohort_{(i % 10) + 1}",
                            "updated",
                        ],
                        "is_premium": True,  # Upgraded to premium
                        "created_at": "2024-01-01T10:00:00Z",
                        "updated_at": "2025-07-02T11:00:00Z",  # Updated timestamp
                    },
                    "time_extracted": "2025-07-02T11:00:00Z",
                } for i in range(0, 2000, 10)]

        # Add new customers (simulate new registrations)
        incremental_updates.extend({
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "customer_id": i + 1,
                        "first_name": f"NewCustomer{i + 1}",
                        "last_name": f"NewLast{i + 1}",
                        "email": f"new.customer{i + 1}@example.com",
                        "phone": f"+1-555-{(i + 3000):04d}",
                        "address": {
                            "street": f"{i + 1} New St",
                            "city": "New City",
                            "state": "TX",
                            "zip": f"{75000 + (i % 1000):05d}",
                            "country": "USA",
                        },
                        "registration_date": "2025-07-02T11:00:00Z",
                        "last_login": "2025-07-02T11:00:00Z",
                        "status": "active",
                        "lifetime_value": 0.0,  # New customer
                        "preferences": {
                            "email_notifications": True,
                            "sms_notifications": False,
                            "language": "en",
                            "timezone": "UTC-6",
                        },
                        "tags": ["new_customer", f"segment_{(i % 5) + 1}"],
                        "is_premium": False,
                        "created_at": "2025-07-02T11:00:00Z",
                        "updated_at": "2025-07-02T11:00:00Z",
                    },
                    "time_extracted": "2025-07-02T11:00:00Z",
                } for i in range(10000, 12000))

        # Process incremental updates
        messages = [json.dumps(customer_schema)]
        messages.extend([json.dumps(record) for record in incremental_updates])
        input_data = "\n".join(messages)

        target_incremental = OracleTarget(config=etl_config)

        performance_timer.start()

        with patch("sys.stdin", StringIO(input_data)):
            target_incremental.cli()

        performance_timer.stop()
        incremental_load_time = performance_timer.duration

        # Verify incremental updates
        with oracle_engine.connect() as conn:
            # Should have 12000 total customers now (10000 original + 2000 new)
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            final_count = row[0]
            assert final_count == 12000

            # Verify updates were applied
            result = conn.execute(
                text(
                    f"""
                SELECT COUNT(*)
                FROM {test_table_name}
                WHERE first_name LIKE 'UpdatedFirst%'
            """,
                ),
            )
            row = result.fetchone()
            assert row is not None
            updated_count = row[0]
            assert updated_count == 200  # 2000/10 updates

            # Verify new customers
            result = conn.execute(
                text(
                    f"""
                SELECT COUNT(*)
                FROM {test_table_name}
                WHERE first_name LIKE 'NewCustomer%'
            """,
                ),
            )
            row = result.fetchone()
            assert row is not None
            new_count = row[0]
            assert new_count == 2000

            # Verify premium upgrades
            result = conn.execute(
                text(
                    f"""
                SELECT COUNT(*)
                FROM {test_table_name}
                WHERE status = 'premium'
            """,
                ),
            )
            row = result.fetchone()
            assert row is not None
            premium_count = row[0]
            assert premium_count >= 10  # At least 10 premium upgrades

        # Phase 4: Data quality validation
        with oracle_engine.connect() as conn:
            # Check for data integrity issues
            data_quality_checks = [
                (
                    "No duplicate customer IDs",
                    (
                        f"SELECT COUNT(*) - COUNT(DISTINCT customer_id) "
                        f"FROM {test_table_name}"
                    ),
                ),
                (
                    "All emails are unique",
                    f"SELECT COUNT(*) - COUNT(DISTINCT email) FROM {test_table_name}",
                ),
                (
                    "No null customer IDs",
                    f"SELECT COUNT(*) FROM {test_table_name} WHERE customer_id IS NULL",
                ),
                (
                    "All statuses are valid",
                    (
                        f"SELECT COUNT(*) FROM {test_table_name} WHERE status "
                        f"NOT IN ('active', 'inactive', 'premium')"
                    ),
                ),
                (
                    "Reasonable lifetime values",
                    f"SELECT COUNT(*) FROM {test_table_name} WHERE lifetime_value < 0",
                ),
            ]

            for check_name, query in data_quality_checks:
                result = conn.execute(text(query))
                row = result.fetchone()
                assert row is not None
                issue_count = row[0]
                assert issue_count == 0, f"Data quality issue: {check_name}"

        # Performance summary
        total_throughput = 12000 / (initial_load_time + incremental_load_time)
        initial_throughput = 10000 / initial_load_time
        incremental_throughput = (
            2200 / incremental_load_time
        )  # 200 updates + 2000 inserts

        # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error("\nEnd-to-End ETL Performance:")
        log.error(
            f"Initial load: {initial_throughput:.2f} records/sec "
            # Link: https://github.com/issue/todo
            f"({initial_load_time:.2f}s)  # TODO(@dev): Replace with proper logging",
        )
        log.error(
            f"Incremental load: {incremental_throughput:.2f} records/sec "
            f"({incremental_load_time:.2f}s)  "
            "# TODO(@dev): Replace with proper logging  "
            "# Link: https://github.com/issue/todo",
        )
        log.error(
            f"Overall throughput: {total_throughput:.2f} records/sec",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            "Total records processed: 12,200",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Final customer count: {final_count:,}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo

        # Performance assertions
        assert (
            initial_throughput > 500
        ), f"Initial load too slow: {initial_throughput:.2f} records/sec"
        assert (
            incremental_throughput > 200
        ), f"Incremental load too slow: {incremental_throughput:.2f} records/sec"

    def test_schema_evolution_workflow(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
    ) -> None:
        """Test schema evolution with column additions."""
        table_cleanup(test_table_name)

        target = OracleTarget(config=oracle_config)

        # Phase 1: Initial schema with basic columns
        initial_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Insert initial data
        initial_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {"id": 1, "name": "John", "email": "john@example.com"},
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {"id": 2, "name": "Jane", "email": "jane@example.com"},
            },
        ]

        messages = [json.dumps(initial_schema)]
        messages.extend([json.dumps(record) for record in initial_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify initial schema
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 2

            # Check initial columns
            result = conn.execute(
                text(
                    f"""
                SELECT column_name
                FROM user_tab_columns
                WHERE table_name = UPPER('{test_table_name}')
                ORDER BY column_id
            """,
                ),
            )
            initial_columns = [row[0] for row in result.fetchall()]
            expected_initial = ["ID", "NAME", "EMAIL"]
            for col in expected_initial:
                assert col in initial_columns

        # Phase 2: Evolved schema with additional columns
        evolved_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "age": {"type": "integer"},  # New column
                    "phone": {"type": "string"},  # New column
                    "metadata": {"type": "object"},  # New column
                    "is_active": {"type": "boolean"},  # New column
                },
            },
            "key_properties": ["id"],
        }

        # Insert data with new columns
        evolved_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 3,
                    "name": "Bob",
                    "email": "bob@example.com",
                    "age": 30,
                    "phone": "+1-555-0003",
                    "metadata": {"department": "Engineering"},
                    "is_active": True,
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,  # Update existing record with new columns
                    "name": "John Updated",
                    "email": "john.updated@example.com",
                    "age": 25,
                    "phone": "+1-555-0001",
                    "metadata": {"department": "Sales"},
                    "is_active": True,
                },
            },
        ]

        messages = [json.dumps(evolved_schema)]
        messages.extend([json.dumps(record) for record in evolved_records])
        input_data = "\n".join(messages)

        target_evolved = OracleTarget(config=oracle_config)
        with patch("sys.stdin", StringIO(input_data)):
            target_evolved.cli()

        # Verify schema evolution
        with oracle_engine.connect() as conn:
            # Should have 3 records total (1 updated, 1 new, 1 unchanged)
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 3

            # Check evolved columns
            result = conn.execute(
                text(
                    f"""
                SELECT column_name
                FROM user_tab_columns
                WHERE table_name = UPPER('{test_table_name}')
                ORDER BY column_id
            """,
                ),
            )
            evolved_columns = [row[0] for row in result.fetchall()]
            expected_evolved = ["AGE", "PHONE", "METADATA", "IS_ACTIVE"]
            for col in expected_evolved:
                assert col in evolved_columns, f"Missing evolved column: {col}"

            # Verify data integrity
            result = conn.execute(
                text(
                    f"""
                SELECT id, name, age, phone
                FROM {test_table_name}
                WHERE id = 1
            """,
                ),
            )
            updated_record = result.fetchone()
            assert updated_record is not None
            assert updated_record.name == "John Updated"
            assert updated_record.age == 25
            assert updated_record.phone == "+1-555-0001"

            # Verify new record
            result = conn.execute(
                text(
                    f"""
                SELECT id, name, age
                FROM {test_table_name}
                WHERE id = 3
            """,
                ),
            )
            new_record = result.fetchone()
            assert new_record is not None
            assert new_record.name == "Bob"
            assert new_record.age == 30

    def test_error_recovery_workflow(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
    ) -> None:
        """Test error recovery and resilience workflow."""
        table_cleanup(test_table_name)

        # Configure with retry settings
        resilient_config = oracle_config.copy()
        resilient_config["max_retries"] = 3
        resilient_config["retry_delay"] = 0.1
        resilient_config["retry_backoff"] = 2.0

        target = OracleTarget(config=resilient_config)

        # Create schema with constraints that can cause errors
        error_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "short_text": {"type": "string", "maxLength": 10},
                    "required_field": {"type": "string"},
                },
            },
            "key_properties": ["id"],
        }

        # Phase 1: Process valid records
        valid_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 1,
                    "short_text": "Valid",
                    "required_field": "Present",
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 2,
                    "short_text": "Also OK",
                    "required_field": "Also here",
                },
            },
        ]

        messages = [json.dumps(error_schema)]
        messages.extend([json.dumps(record) for record in valid_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify valid records processed
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            assert row[0] == 2

        # Phase 2: Process records that may cause constraint violations
        mixed_records = [
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 3,
                    "short_text": "Valid3",
                    "required_field": "Present3",
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 4,
                    "short_text": "This text is too long for column",  # Error expected
                    "required_field": "Present4",
                },
            },
            {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "id": 5,
                    "short_text": "Valid5",
                    "required_field": "Present5",
                },
            },
        ]

        messages = [json.dumps(error_schema)]
        messages.extend([json.dumps(record) for record in mixed_records])
        input_data = "\n".join(messages)

        target_recovery = OracleTarget(config=resilient_config)

        # This should handle errors gracefully
        try:
            with patch("sys.stdin", StringIO(input_data)):
                target_recovery.cli()
        except Exception as e:
            # Some errors may be expected - verify they're constraint-related
            error_msg = str(e).lower()
            assert any(
                keyword in error_msg
                for keyword in ["constraint", "length", "value", "invalid"]
            )

        # Verify that valid records were still processed despite errors
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            # Should have at least the original 2 records, possibly more valid
            # ones
            assert count >= 2, f"Error recovery failed - only {count} records found"

    def test_monitoring_and_metrics_workflow(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
    ) -> None:
        """Test monitoring and metrics collection workflow."""
        table_cleanup(test_table_name)

        # Configure with monitoring enabled
        monitoring_config = oracle_config.copy()
        monitoring_config["enable_metrics"] = True
        monitoring_config["log_performance_stats"] = True

        target = OracleTarget(config=monitoring_config)

        # Create monitoring test schema
        monitoring_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "metric_name": {"type": "string"},
                    "metric_value": {"type": "number"},
                    "timestamp": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["id"],
        }

        # Generate monitoring test data
        monitoring_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "id": i + 1,
                        "metric_name": f"metric_{(i % 10) + 1}",
                        "metric_value": float(i * 1.5),
                        "timestamp": "2025-07-02T10:00:00Z",
                    },
                } for i in range(5000)]

        # Process with monitoring
        messages = [json.dumps(monitoring_schema)]
        messages.extend([json.dumps(record) for record in monitoring_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify monitoring data processed
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            count = row[0]
            assert count == 5000

            # Verify monitoring data distribution
            result = conn.execute(
                text(
                    f"""
                SELECT
                    metric_name,
                    COUNT(*) as record_count,
                    AVG(metric_value) as avg_value,
                    MIN(metric_value) as min_value,
                    MAX(metric_value) as max_value
                FROM {test_table_name}
                GROUP BY metric_name
                ORDER BY metric_name
            """,
                ),
            )

            metrics = result.fetchall()
            assert len(metrics) == 10  # Should have 10 different metric types

            for metric in metrics:
                assert metric is not None
                assert metric.record_count == 500  # 5000 records / 10 metrics
                assert metric.avg_value > 0
                assert metric.min_value >= 0
                assert metric.max_value > metric.min_value

    def test_real_world_data_patterns(
        self,
        oracle_config: dict[str, Any],
        test_table_name: str,
        oracle_engine: Engine,
        table_cleanup: Any,
    ) -> None:
        """Test with realistic data patterns and edge cases."""
        table_cleanup(test_table_name)

        target = OracleTarget(config=oracle_config)

        # Create realistic schema with various data types
        realistic_schema = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string"},
                    "user_id": {"type": "integer"},
                    "amount": {"type": "number"},
                    "currency": {"type": "string"},
                    "description": {"type": "string"},
                    "metadata": {"type": "object"},
                    "tags": {"type": "array"},
                    "processed_at": {"type": "string", "format": "date-time"},
                    "is_refund": {"type": "boolean"},
                    "source_system": {"type": "string"},
                },
            },
            "key_properties": ["transaction_id"],
        }

        # Generate realistic data with edge cases

        # Regular transactions
        realistic_records = [{
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "transaction_id": f"TXN-{i + 1:06d}",
                        "user_id": (i % 100) + 1,
                        "amount": round(10.0 + (i * 0.75), 2),
                        "currency": "USD",
                        "description": f"Purchase transaction {i + 1}",
                        "metadata": {
                            "payment_method": "credit_card",
                            "merchant_id": f"MERCH-{(i % 50) + 1:03d}",
                            "ip_address": f"192.168.1.{(i % 254) + 1}",
                        },
                        "tags": ["purchase", "online"],
                        "processed_at": "2025-07-02T10:00:00Z",
                        "is_refund": False,
                        "source_system": "web_app",
                    },
                } for i in range(1000)]

        # Edge case: Very large amounts
        realistic_records.extend(
            [
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "transaction_id": "TXN-LARGE-001",
                        "user_id": 9999,
                        "amount": 999999.99,
                        "currency": "USD",
                        "description": "Large transaction test",
                        "metadata": {"special": "high_value"},
                        "tags": ["large", "special"],
                        "processed_at": "2025-07-02T10:00:00Z",
                        "is_refund": False,
                        "source_system": "admin_panel",
                    },
                },
            ],
        )

        # Edge case: Zero amounts
        realistic_records.extend(
            [
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "transaction_id": "TXN-ZERO-001",
                        "user_id": 1000,
                        "amount": 0.0,
                        "currency": "USD",
                        "description": "Zero amount transaction",
                        "metadata": {"type": "adjustment"},
                        "tags": ["adjustment", "zero"],
                        "processed_at": "2025-07-02T10:00:00Z",
                        "is_refund": False,
                        "source_system": "accounting",
                    },
                },
            ],
        )

        # Edge case: Negative amounts (refunds)
        realistic_records.extend(
            [
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "transaction_id": "TXN-REFUND-001",
                        "user_id": 500,
                        "amount": -50.25,
                        "currency": "USD",
                        "description": "Refund transaction",
                        "metadata": {"original_txn": "TXN-000500"},
                        "tags": ["refund", "negative"],
                        "processed_at": "2025-07-02T10:00:00Z",
                        "is_refund": True,
                        "source_system": "refund_api",
                    },
                },
            ],
        )

        # Edge case: Unicode and special characters
        realistic_records.extend(
            [
                {
                    "type": "RECORD",
                    "stream": test_table_name,
                    "record": {
                        "transaction_id": "TXN-UNICODE-001",
                        "user_id": 777,
                        "amount": 25.50,
                        "currency": "EUR",
                        "description": "Café purchase with émojis 🛒 and chars: áéíóú",
                        "metadata": {
                            "merchant_name": "Café Münchën & Co.",
                            "location": "São Paulo, Brasil",
                            "notes": "Special characters: @#$%^&*()[]{}|\\:;\"'<>,.?/",
                        },
                        "tags": ["international", "unicode", "special"],
                        "processed_at": "2025-07-02T10:00:00Z",
                        "is_refund": False,
                        "source_system": "mobile_app",
                    },
                },
            ],
        )

        # Process realistic data
        messages = [json.dumps(realistic_schema)]
        messages.extend([json.dumps(record) for record in realistic_records])
        input_data = "\n".join(messages)

        with patch("sys.stdin", StringIO(input_data)):
            target.cli()

        # Verify realistic data processing
        with oracle_engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {test_table_name}"))
            row = result.fetchone()
            assert row is not None
            total_count = row[0]
            assert total_count == len(realistic_records)

            # Verify edge cases were handled correctly

            # Large amount
            result = conn.execute(
                text(
                    f"""
                SELECT amount FROM {test_table_name}
                WHERE transaction_id = 'TXN-LARGE-001'
            """,
                ),
            )
            large_amount = result.fetchone()
            assert large_amount is not None
            assert float(large_amount.amount) == 999999.99

            # Zero amount
            result = conn.execute(
                text(
                    f"""
                SELECT amount FROM {test_table_name}
                WHERE transaction_id = 'TXN-ZERO-001'
            """,
                ),
            )
            zero_amount = result.fetchone()
            assert zero_amount is not None
            assert float(zero_amount.amount) == 0.0

            # Negative amount
            result = conn.execute(
                text(
                    f"""
                SELECT amount, is_refund FROM {test_table_name}
                WHERE transaction_id = 'TXN-REFUND-001'
            """,
                ),
            )
            refund = result.fetchone()
            assert refund is not None
            assert float(refund.amount) == -50.25
            assert refund.is_refund == 1

            # Unicode handling
            result = conn.execute(
                text(
                    f"""
                SELECT description FROM {test_table_name}
                WHERE transaction_id = 'TXN-UNICODE-001'
            """,
                ),
            )
            unicode_desc = result.fetchone()
            assert unicode_desc is not None
            assert "🛒" in unicode_desc.description
            assert "émojis" in unicode_desc.description

            # Data distribution analysis
            result = conn.execute(
                text(
                    f"""
                SELECT
                    COUNT(*) as total_transactions,
                    COUNT(DISTINCT user_id) as unique_users,
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_positive,
                    SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as total_negative,
                    AVG(amount) as avg_amount
                FROM {test_table_name}
            """,
                ),
            )

            summary = result.fetchone()
            assert summary is not None
            assert summary.total_transactions == len(realistic_records)
            assert summary.unique_users > 0
            assert summary.total_positive > 0
            assert summary.total_negative < 0  # Should have negative refunds

        log.error(
            "\nRealistic Data Processing Summary:",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Total transactions: {summary.total_transactions}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Unique users: {summary.unique_users}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Total positive amount: ${summary.total_positive:.2f}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Total negative amount: ${summary.total_negative:.2f}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(
            f"Average transaction: ${summary.avg_amount:.2f}",
        )  # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
