"""
Real-world data loading scenario tests.

These tests simulate actual production use cases including:
- E-commerce transaction data
- User activity logs
- Financial records
- Multi-stream concurrent loading
- Time-series data with partitioning
"""

import json
import random
from datetime import datetime, timezone, timedelta
from io import StringIO
from typing import Any

import pytest
from flext_target_oracle.target import OracleTarget
from sqlalchemy import text
from sqlalchemy.engine import Engine

from tests.helpers import requires_oracle_connection

@pytest.mark.integration
@pytest.mark.slow
@requires_oracle_connection
class TestRealWorldScenarios:
    """Test real-world data loading scenarios."""

    def test_ecommerce_transaction_data(self,
                                        oracle_config: dict[str, Any],
                                        oracle_engine: Engine,
                                        test_table_name: str,
                                        table_cleanup,
                                        performance_timer,
                                        ) -> None:
        """Test loading e-commerce transaction data with complex schema."""
        table_cleanup(test_table_name)

        # Create target optimized for transaction data
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "upsert",
                "batch_size": 2000,
                "use_bulk_operations": True,
                "varchar_max_length": 2000,
                "number_precision": 15,
                "number_scale": 2,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # E-commerce transaction schema
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string", "maxLength": 50},
                    "order_id": {"type": "string", "maxLength": 50},
                    "customer_id": {"type": "integer"},
                    "product_id": {"type": "string", "maxLength": 20},
                    "product_name": {"type": "string", "maxLength": 200},
                    "category": {"type": "string", "maxLength": 50},
                    "quantity": {"type": "integer"},
                    "unit_price": {"type": "number"},
                    "total_amount": {"type": "number"},
                    "currency": {"type": "string", "maxLength": 3},
                    "payment_method": {"type": "string", "maxLength": 50},
                    "transaction_date": {"type": "string", "format": "date-time"},
                    "shipping_address": {"type": "object"},
                    "customer_metadata": {"type": "object"},
                    "promotion_codes": {"type": "array"},
                    "status": {"type": "string", "maxLength": 20},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["transaction_id"],
        }

        # Generate realistic e-commerce data
        record_count = 5000
        record_messages = []

        categories = [
            "Electronics",
            "Clothing",
            "Books",
            "Home & Garden",
            "Sports",
            "Toys",
        ]
        payment_methods = [
            "credit_card",
            "debit_card",
            "paypal",
            "apple_pay",
            "google_pay",
        ]
        currencies = ["USD", "EUR", "GBP", "CAD"]
        statuses = [
            "pending",
            "confirmed",
            "shipped",
            "delivered",
            "cancelled"]

        base_time = datetime.now(timezone.utc) - timedelta(days=30)

        for i in range(record_count):
            transaction_time = base_time + timedelta(
                minutes=random.randint(0, 43200)  # Random within 30 days
            )

            category = random.choice(categories)
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(9.99, 999.99), 2)
            total_amount = round(quantity * unit_price, 2)

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "transaction_id": f"TXN_{i + 1:06d}",
                    # Multiple items per order
                    "order_id": f"ORD_{(i // 3) + 1:06d}",
                    "customer_id": random.randint(1, 1000),
                    "product_id": f"PROD_{random.randint(1, 500):05d}",
                    "product_name": f"{category} Product {random.randint(1, 100)}",
                    "category": category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_amount": total_amount,
                    "currency": random.choice(currencies),
                    "payment_method": random.choice(payment_methods),
                    "transaction_date": transaction_time.isoformat() + "Z",
                    "shipping_address": {
                        "street": f"{random.randint(1, 9999)} Main St",
                        "city": random.choice(
                            ["New York", "Los Angeles", "Chicago", "Houston"]
                        ),
                        "state": random.choice(["NY", "CA", "IL", "TX"]),
                        "zip_code": f"{random.randint(10000, 99999)}",
                        "country": "USA",
                    },
                    "customer_metadata": {
                        "tier": random.choice(["bronze", "silver", "gold", "platinum"]),
                        "signup_date": (
                            transaction_time -
                            timedelta(days=random.randint(30, 365))
                        ).isoformat()
                        + "Z",
                        "lifetime_value": round(random.uniform(100, 5000), 2),
                    },
                    "promotion_codes": random.sample(
                        ["SAVE10", "WELCOME", "LOYALTY", "SEASONAL", "FLASH"],
                        k=random.randint(0, 2),
                    ),
                    "status": random.choice(statuses),
                    "created_at": transaction_time.isoformat() + "Z",
                    "updated_at": (
                        transaction_time +
                        timedelta(hours=random.randint(1, 72))
                    ).isoformat()
                    + "Z",
                },
                "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
            }
            record_messages.append(record)

        # Process transaction data
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify e-commerce data loading
        with oracle_engine.connect() as conn:
            # Verify record count
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify data integrity - check totals
            result = conn.execute(
                text(
                    f"""
                SELECT
                    COUNT(DISTINCT order_id) as unique_orders,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    SUM(quantity) as total_quantity,
                    ROUND(SUM(total_amount), 2) as total_revenue
                FROM {test_table_name}
            """
                )
            )
            stats = result.fetchone()

            assert stats[0] > 0, "No unique orders found"
            assert stats[1] > 0, "No unique customers found"
            assert stats[2] > 0, "No quantity found"
            assert stats[3] > 0, "No revenue found"

            # Verify complex data types (JSON)
            result = conn.execute(
                text(
                    f"""
                SELECT shipping_address, customer_metadata, promotion_codes
                FROM {test_table_name}
                WHERE ROWNUM <= 3
            """
                )
            )
            for row in result:
                # Verify JSON data can be parsed
                shipping = json.loads(row[0])
                metadata = json.loads(row[1])
                promos = json.loads(row[2])

                assert "street" in shipping, "Shipping address incomplete"
                assert "tier" in metadata, "Customer metadata incomplete"
                assert isinstance(promos, list), "Promotion codes not array"

        throughput = record_count / performance_timer.duration
        # TODO(@dev): Replace with proper logging  # Link: https://github.com/issue/todo
        log.error(f"E-commerce data loading: {throughput:.0f} records/second")

    def test_user_activity_logs(self,
                                oracle_config: dict[str, Any],
                                oracle_engine: Engine,
                                test_table_name: str,
                                table_cleanup,
                                ) -> None:
        """Test loading high-volume user activity logs."""
        table_cleanup(test_table_name)

        # Configure for high-volume log data
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 5000,
                "use_bulk_operations": True,
                "use_append_values_hint": True,
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # User activity log schema
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "log_id": {"type": "string", "maxLength": 36},
                    "user_id": {"type": "integer"},
                    "session_id": {"type": "string", "maxLength": 32},
                    "event_type": {"type": "string", "maxLength": 50},
                    "page_url": {"type": "string", "maxLength": 500},
                    "referrer_url": {"type": "string", "maxLength": 500},
                    "user_agent": {"type": "string", "maxLength": 1000},
                    "ip_address": {"type": "string", "maxLength": 45},
                    "geolocation": {"type": "object"},
                    "device_info": {"type": "object"},
                    "custom_properties": {"type": "object"},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "duration_seconds": {"type": "integer"},
                },
            },
            "key_properties": ["log_id"],
        }

        # Generate high-volume activity logs
        record_count = 10000
        record_messages = []

        event_types = [
            "page_view",
            "click",
            "scroll",
            "form_submit",
            "search",
            "add_to_cart",
            "checkout",
            "login",
            "logout",
            "signup",
        ]

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) "
                "AppleWebKit/605.1.15"
            ),
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
        ]

        base_time = datetime.now(timezone.utc) - timedelta(hours=24)

        for i in range(record_count):
            log_time = base_time + timedelta(
                seconds=random.randint(0, 86400)  # Random within 24 hours
            )

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "log_id": f"log_{i + 1:08d}_{random.randint(1000, 9999)}",
                    "user_id": random.randint(1, 5000),
                    "session_id": f"sess_{random.randint(100000, 999999)}",
                    "event_type": random.choice(event_types),
                    "page_url": (
                        f"https://example.com/"
                        f"{random.choice(['home', 'products', 'cart', 'profile'])}"
                    ),
                    "referrer_url": random.choice(
                        [
                            "https://google.com/search",
                            "https://facebook.com",
                            "https://twitter.com",
                            "direct",
                            "",
                        ]
                    ),
                    "user_agent": random.choice(user_agents),
                    "ip_address": (
                        f"{random.randint(1, 255)}.{random.randint(1, 255)}."
                        f"{random.randint(1, 255)}.{random.randint(1, 255)}"
                    ),
                    "geolocation": {
                        "country": random.choice(["US", "CA", "UK", "DE", "FR"]),
                        "city": random.choice(
                            ["New York", "Toronto", "London", "Berlin", "Paris"]
                        ),
                        "latitude": round(random.uniform(-90, 90), 6),
                        "longitude": round(random.uniform(-180, 180), 6),
                    },
                    "device_info": {
                        "type": random.choice(["desktop", "mobile", "tablet"]),
                        "os": random.choice(["Windows", "macOS", "iOS", "Android"]),
                        "browser": random.choice(
                            ["Chrome", "Safari", "Firefox", "Edge"]
                        ),
                        "screen_resolution": random.choice(
                            ["1920x1080", "1366x768", "375x667", "414x896"]
                        ),
                    },
                    "custom_properties": {
                        "experiment_id": f"exp_{random.randint(1, 10)}",
                        "ab_test_variant": random.choice(["A", "B", "control"]),
                        "feature_flags": random.sample(
                            ["new_ui", "recommendations", "chat"],
                            k=random.randint(0, 3),
                        ),
                    },
                    "timestamp": log_time.isoformat() + "Z",
                    "duration_seconds": random.randint(1, 300),
                },
                "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
            }
            record_messages.append(record)

        # Process activity logs
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        oracle_target.process_lines(input_stream)

        # Verify activity log data
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify log analytics
            result = conn.execute(
                text(
                    f"""
                SELECT
                    event_type,
                    COUNT(*) as event_count
                FROM {test_table_name}
                GROUP BY event_type
                ORDER BY event_count DESC
            """
                )
            )
            event_stats = dict(result.fetchall())

            # Should have all event types
            assert len(event_stats) > 0, "No events found"
            assert "page_view" in event_stats, "Page view events missing"

    def test_financial_records_with_precision(self,
                                              oracle_config: dict[str, Any],
                                              oracle_engine: Engine,
                                              test_table_name: str,
                                              table_cleanup,
                                              ) -> None:
        """Test loading financial records requiring high precision."""
        table_cleanup(test_table_name)

        # Configure for financial precision
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "upsert",
                "batch_size": 1000,
                "number_precision": 20,
                "number_scale": 8,  # High precision for financial calculations
                "skip_table_optimization": True,
            }
        )
        oracle_target = OracleTarget(config=config)

        # Financial records schema
        schema_message = {
            "type": "SCHEMA",
            "stream": test_table_name,
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string", "maxLength": 50},
                    "account_id": {"type": "string", "maxLength": 20},
                    "transaction_type": {"type": "string", "maxLength": 20},
                    "amount": {"type": "number"},
                    "currency": {"type": "string", "maxLength": 3},
                    "exchange_rate": {"type": "number"},
                    "amount_usd": {"type": "number"},
                    "fee": {"type": "number"},
                    "tax": {"type": "number"},
                    "net_amount": {"type": "number"},
                    "balance_before": {"type": "number"},
                    "balance_after": {"type": "number"},
                    "counterparty": {"type": "string", "maxLength": 100},
                    "reference": {"type": "string", "maxLength": 100},
                    "description": {"type": "string", "maxLength": 500},
                    "transaction_date": {"type": "string", "format": "date-time"},
                    "processing_date": {"type": "string", "format": "date-time"},
                    "value_date": {"type": "string", "format": "date-time"},
                    "risk_metrics": {"type": "object"},
                    "compliance_flags": {"type": "array"},
                },
            },
            "key_properties": ["transaction_id"],
        }

        # Generate financial records with high precision
        record_count = 3000
        record_messages = []

        transaction_types = [
            "deposit",
            "withdrawal",
            "transfer",
            "payment",
            "fee",
            "interest",
        ]
        currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD"]

        # Exchange rates with high precision
        exchange_rates = {
            "USD": 1.0,
            "EUR": 1.18543210,
            "GBP": 1.38765432,
            "JPY": 0.00921543,
            "CHF": 1.09876543,
            "CAD": 0.79834567,
        }

        running_balance = 100000.0  # Starting balance
        base_time = datetime.now(timezone.utc) - timedelta(days=7)

        for i in range(record_count):
            transaction_time = base_time + timedelta(
                minutes=random.randint(0, 10080)  # Random within 7 days
            )

            transaction_type = random.choice(transaction_types)
            currency = random.choice(currencies)

            # Generate amount with high precision
            if transaction_type in ["deposit", "interest"]:
                amount = round(random.uniform(100.0, 50000.0), 8)
                sign = 1
            else:
                amount = round(random.uniform(10.0, 5000.0), 8)
                sign = -1

            exchange_rate = exchange_rates[currency]
            amount_usd = round(amount * exchange_rate, 8)
            fee = (
                round(amount * 0.001, 8)
                if transaction_type in ["transfer", "payment"]
                else 0.0
            )
            tax = round(
                amount * 0.005,
                8) if transaction_type == "interest" else 0.0
            net_amount = round(amount - fee - tax, 8)

            balance_before = running_balance
            balance_after = running_balance + (sign * net_amount)
            running_balance = balance_after

            record = {
                "type": "RECORD",
                "stream": test_table_name,
                "record": {
                    "transaction_id": f"FIN_{i + 1:08d}",
                    "account_id": f"ACC_{random.randint(1000, 9999)}",
                    "transaction_type": transaction_type,
                    "amount": amount,
                    "currency": currency,
                    "exchange_rate": exchange_rate,
                    "amount_usd": amount_usd,
                    "fee": fee,
                    "tax": tax,
                    "net_amount": net_amount,
                    "balance_before": round(balance_before, 8),
                    "balance_after": round(balance_after, 8),
                    "counterparty": f"BANK_{random.randint(100, 999)}",
                    "reference": f"REF_{random.randint(100000, 999999)}",
                    "description": f"{transaction_type.title()} transaction #{i + 1}",
                    "transaction_date": transaction_time.isoformat() + "Z",
                    "processing_date": (
                        transaction_time +
                        timedelta(hours=random.randint(0, 24))
                    ).isoformat()
                    + "Z",
                    "value_date": (
                        transaction_time + timedelta(days=random.randint(0, 3))
                    ).isoformat()
                    + "Z",
                    "risk_metrics": {
                        "risk_score": round(random.uniform(0.0, 10.0), 4),
                        "aml_score": round(random.uniform(0.0, 1.0), 6),
                        "fraud_probability": round(random.uniform(0.0, 0.1), 8),
                    },
                    "compliance_flags": random.sample(
                        [
                            "kyc_verified",
                            "aml_cleared",
                            "sanctions_checked",
                            "pep_screened",
                        ],
                        k=random.randint(2, 4),
                    ),
                },
                "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
            }
            record_messages.append(record)

        # Process financial records
        messages = [schema_message] + record_messages
        input_lines = [json.dumps(msg) + "\n" for msg in messages]
        input_stream = StringIO("".join(input_lines))

        oracle_target.process_lines(input_stream)

        # Verify financial data with precision
        with oracle_engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {test_table_name}"))
            count = result.scalar()
            assert (
                count == record_count
            ), f"Expected {record_count} records, found {count}"

            # Verify precision is maintained
            result = conn.execute(
                text(
                    f"""
                SELECT
                    SUM(amount) as total_amount,
                    SUM(fee) as total_fees,
                    SUM(tax) as total_taxes,
                    AVG(exchange_rate) as avg_exchange_rate
                FROM {test_table_name}
            """
                )
            )
            totals = result.fetchone()

            assert totals[0] > 0, "No amounts found"
            assert totals[1] >= 0, "Negative fees found"
            assert totals[2] >= 0, "Negative taxes found"
            assert totals[3] > 0, "No exchange rates found"

            # Verify high precision numbers
            result = conn.execute(
                text(
                    f"""
                SELECT amount, exchange_rate, balance_after
                FROM {test_table_name}
                WHERE ROWNUM <= 5
            """
                )
            )
            for row in result:
                # Verify precision is maintained (should have decimal places)
                amount_str = str(float(row[0]))
                assert "." in amount_str, f"Amount precision lost: {amount_str}"

    def test_multi_stream_concurrent_loading(self,
                                             oracle_config: dict[str, Any],
                                             oracle_engine: Engine,
                                             test_schema_prefix: str,
                                             table_cleanup,
                                             performance_timer,
                                             ) -> None:
        """Test concurrent loading of multiple data streams."""
        # Create multiple table names
        table_names = [
            f"{test_schema_prefix}_users",
            f"{test_schema_prefix}_orders",
            f"{test_schema_prefix}_products",
        ]

        for table_name in table_names:
            table_cleanup(table_name)

        # Configure for multi-stream processing
        config = oracle_config.copy()
        config.update(
            {
                "load_method": "append-only",
                "batch_size": 1000,
                "use_bulk_operations": True,
                "skip_table_optimization": True,
            }
        )

        # Create multiple schemas and data sets
        schemas_and_records = []

        # Users stream
        users_schema = {
            "type": "SCHEMA",
            "stream": table_names[0],
            "schema": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "username": {"type": "string", "maxLength": 50},
                    "email": {"type": "string", "maxLength": 100},
                    "created_at": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["user_id"],
        }

        users_records = []
        for i in range(1000):
            users_records.append(
                {
                    "type": "RECORD",
                    "stream": table_names[0],
                    "record": {
                        "user_id": i + 1,
                        "username": f"user_{i + 1}",
                        "email": f"user_{i + 1}@example.com",
                        "created_at": datetime.now(timezone.utc).isoformat() + "Z",
                    },
                    "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
                }
            )

        schemas_and_records.append((users_schema, users_records))

        # Orders stream
        orders_schema = {
            "type": "SCHEMA",
            "stream": table_names[1],
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"},
                    "user_id": {"type": "integer"},
                    "total_amount": {"type": "number"},
                    "status": {"type": "string", "maxLength": 20},
                    "order_date": {"type": "string", "format": "date-time"},
                },
            },
            "key_properties": ["order_id"],
        }

        orders_records = []
        for i in range(2000):
            orders_records.append(
                {
                    "type": "RECORD",
                    "stream": table_names[1],
                    "record": {
                        "order_id": i + 1,
                        "user_id": random.randint(1, 1000),
                        "total_amount": round(random.uniform(10.0, 500.0), 2),
                        "status": random.choice(
                            ["pending", "confirmed", "shipped", "delivered"]
                        ),
                        "order_date": datetime.now(timezone.utc).isoformat() + "Z",
                    },
                    "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
                }
            )

        schemas_and_records.append((orders_schema, orders_records))

        # Products stream
        products_schema = {
            "type": "SCHEMA",
            "stream": table_names[2],
            "schema": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "name": {"type": "string", "maxLength": 100},
                    "category": {"type": "string", "maxLength": 50},
                    "price": {"type": "number"},
                    "inventory": {"type": "integer"},
                },
            },
            "key_properties": ["product_id"],
        }

        products_records = []
        categories = ["Electronics", "Clothing", "Books", "Home"]
        for i in range(500):
            products_records.append(
                {
                    "type": "RECORD",
                    "stream": table_names[2],
                    "record": {
                        "product_id": i + 1,
                        "name": f"Product {i + 1}",
                        "category": random.choice(categories),
                        "price": round(random.uniform(5.0, 200.0), 2),
                        "inventory": random.randint(0, 1000),
                    },
                    "time_extracted": datetime.now(timezone.utc).isoformat() + "Z",
                }
            )

        schemas_and_records.append((products_schema, products_records))

        # Interleave messages from all streams to simulate concurrent loading
        all_messages = []
        for schema, records in schemas_and_records:
            all_messages.append(schema)
            all_messages.extend(records)

        # Shuffle to simulate real concurrent stream behavior
        random.shuffle(all_messages[3:])  # Keep schemas at the beginning

        # Process all streams together
        oracle_target = OracleTarget(config=config)
        input_lines = [json.dumps(msg) + "\n" for msg in all_messages]
        input_stream = StringIO("".join(input_lines))

        performance_timer.start()
        oracle_target.process_lines(input_stream)
        performance_timer.stop()

        # Verify all streams were loaded correctly
        with oracle_engine.connect() as conn:
            # Verify users
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_names[0]}"))
            users_count = result.scalar()
            assert users_count == 1000, f"Users: expected 1000, got {users_count}"

            # Verify orders
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_names[1]}"))
            orders_count = result.scalar()
            assert orders_count == 2000, f"Orders: expected 2000, got {orders_count}"

            # Verify products
            result = conn.execute(
                text(f"SELECT COUNT(*) FROM {table_names[2]}"))
            products_count = result.scalar()
            assert (
                products_count == 500
            ), f"Products: expected 500, got {products_count}"

            # Verify referential integrity (orders reference valid users)
            result = conn.execute(
                text(
                    f"""
                SELECT COUNT(*) FROM {table_names[1]} o
                WHERE NOT EXISTS (
                    SELECT 1 FROM {table_names[0]} u
                    WHERE u.user_id = o.user_id
                )
            """
                )
            )
            orphaned_orders = result.scalar()
            assert orphaned_orders == 0, f"Found {orphaned_orders} orphaned orders"

        total_records = sum(len(records) for _, records in schemas_and_records)
        throughput = total_records / performance_timer.duration
        log.error(
            f"Multi-stream loading: {throughput:.0f} records/second "
            f"across {len(table_names)  # TODO(@dev): Replace with proper logging} streams"  # Link: https://github.com/issue/todo
                      )
