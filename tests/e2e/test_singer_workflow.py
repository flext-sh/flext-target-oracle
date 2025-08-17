"""End-to-end tests for complete Singer workflows.

These tests validate the full data pipeline from Singer tap through
the Oracle target, including schema evolution, state management, and
complex data transformations.
"""

import asyncio
import json
import time
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from sqlalchemy import text

from flext_target_oracle import FlextOracleTarget, FlextOracleTargetConfig, LoadMethod


@pytest.mark.e2e
@pytest.mark.oracle
@pytest.mark.slow
class TestSingerWorkflowE2E:
    """Complete Singer workflow end-to-end tests."""

    @pytest.mark.asyncio
    async def test_complete_ecommerce_workflow(
      self,
      oracle_config: FlextOracleTargetConfig,
      oracle_engine,
      clean_database,
    ) -> None:
      """Test complete e-commerce data workflow with multiple streams."""
      # Configure for realistic scenario
      oracle_config.batch_size = 500
      oracle_config.load_method = LoadMethod.BULK_INSERT
      oracle_config.sdc_mode = "merge"
      oracle_config.storage_mode = "flattened"
      oracle_config.column_ordering = "alphabetical"
      oracle_config.create_foreign_key_indexes = True

      target = FlextOracleTarget(config=oracle_config)
      await target.initialize()

      # Stream 1: Customers
      customer_schema = {
          "type": "SCHEMA",
          "stream": "customers",
          "schema": {
              "type": "object",
              "properties": {
                  "customer_id": {"type": "integer"},
                  "email": {"type": "string", "format": "email"},
                  "name": {"type": "string"},
                  "created_at": {"type": "string", "format": "date-time"},
                  "updated_at": {"type": "string", "format": "date-time"},
                  "address": {
                      "type": "object",
                      "properties": {
                          "street": {"type": "string"},
                          "city": {"type": "string"},
                          "state": {"type": "string"},
                          "zip": {"type": "string"},
                      },
                  },
                  "preferences": {
                      "type": "object",
                      "properties": {
                          "newsletter": {"type": "boolean"},
                          "sms_alerts": {"type": "boolean"},
                      },
                  },
              },
          },
          "key_properties": ["customer_id"],
          "bookmark_properties": ["updated_at"],
      }

      # Stream 2: Products
      product_schema = {
          "type": "SCHEMA",
          "stream": "products",
          "schema": {
              "type": "object",
              "properties": {
                  "product_id": {"type": "integer"},
                  "sku": {"type": "string"},
                  "name": {"type": "string"},
                  "category": {"type": "string"},
                  "price": {"type": "number"},
                  "cost": {"type": "number"},
                  "created_at": {"type": "string", "format": "date-time"},
                  "updated_at": {"type": "string", "format": "date-time"},
              },
          },
          "key_properties": ["product_id"],
          "bookmark_properties": ["updated_at"],
      }

      # Stream 3: Orders
      order_schema = {
          "type": "SCHEMA",
          "stream": "orders",
          "schema": {
              "type": "object",
              "properties": {
                  "order_id": {"type": "integer"},
                  "customer_id": {
                      "type": "integer",
                      "foreign_key": "customers.customer_id",
                  },
                  "order_date": {"type": "string", "format": "date-time"},
                  "status": {"type": "string"},
                  "total_amount": {"type": "number"},
                  "created_at": {"type": "string", "format": "date-time"},
                  "updated_at": {"type": "string", "format": "date-time"},
              },
          },
          "key_properties": ["order_id"],
          "bookmark_properties": ["updated_at"],
      }

      # Stream 4: Order Items
      order_item_schema = {
          "type": "SCHEMA",
          "stream": "order_items",
          "schema": {
              "type": "object",
              "properties": {
                  "order_item_id": {"type": "integer"},
                  "order_id": {"type": "integer", "foreign_key": "orders.order_id"},
                  "product_id": {
                      "type": "integer",
                      "foreign_key": "products.product_id",
                  },
                  "quantity": {"type": "integer"},
                  "unit_price": {"type": "number"},
                  "discount": {"type": "number"},
                  "created_at": {"type": "string", "format": "date-time"},
              },
          },
          "key_properties": ["order_item_id"],
      }

      # Process schemas
      for schema in [
          customer_schema,
          product_schema,
          order_schema,
          order_item_schema,
      ]:
          result = await target.execute(json.dumps(schema))
          assert result.is_success

      # Generate test data
      now = datetime.now(UTC).isoformat()

      # Insert customers
      customers = []
      for i in range(1, 101):  # 100 customers
          customer = {
              "type": "RECORD",
              "stream": "customers",
              "record": {
                  "customer_id": i,
                  "email": f"customer{i}@example.com",
                  "name": f"Customer {i}",
                  "created_at": now,
                  "updated_at": now,
                  "address": {
                      "street": f"{i} Main St",
                      "city": "Anytown",
                      "state": "CA",
                      "zip": f"{90000 + i:05d}",
                  },
                  "preferences": {
                      "newsletter": i % 2 == 0,
                      "sms_alerts": i % 3 == 0,
                  },
              },
              "time_extracted": now,
          }
          customers.append(customer)
          result = await target.execute(json.dumps(customer))
          assert result.is_success

      # Insert products
      products = []
      categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
      for i in range(1, 51):  # 50 products
          product = {
              "type": "RECORD",
              "stream": "products",
              "record": {
                  "product_id": i,
                  "sku": f"SKU-{i:05d}",
                  "name": f"Product {i}",
                  "category": categories[i % len(categories)],
                  "price": float(
                      Decimal(str(10 + i * 5.99)).quantize(Decimal("0.01")),
                  ),
                  "cost": float(Decimal(str(5 + i * 2.99)).quantize(Decimal("0.01"))),
                  "created_at": now,
                  "updated_at": now,
              },
              "time_extracted": now,
          }
          products.append(product)
          result = await target.execute(json.dumps(product))
          assert result.is_success

      # Insert orders with items
      order_id = 1
      order_item_id = 1
      statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

      for customer_id in range(1, 26):  # First 25 customers make orders
          for _ in range(2):  # 2 orders per customer
              order = {
                  "type": "RECORD",
                  "stream": "orders",
                  "record": {
                      "order_id": order_id,
                      "customer_id": customer_id,
                      "order_date": now,
                      "status": statuses[order_id % len(statuses)],
                      "total_amount": 0.0,  # Will calculate
                      "created_at": now,
                      "updated_at": now,
                  },
                  "time_extracted": now,
              }

              # Add 1-5 items per order
              order_total = 0.0
              for _ in range((order_id % 5) + 1):
                  product_id = (order_item_id % 50) + 1
                  quantity = (order_item_id % 3) + 1
                  unit_price = products[product_id - 1]["record"]["price"]
                  discount = 0.1 if order_item_id % 10 == 0 else 0.0

                  item_total = quantity * unit_price * (1 - discount)
                  order_total += item_total

                  order_item = {
                      "type": "RECORD",
                      "stream": "order_items",
                      "record": {
                          "order_item_id": order_item_id,
                          "order_id": order_id,
                          "product_id": product_id,
                          "quantity": quantity,
                          "unit_price": unit_price,
                          "discount": discount,
                          "created_at": now,
                      },
                      "time_extracted": now,
                  }

                  result = await target.execute(json.dumps(order_item))
                  assert result.is_success
                  order_item_id += 1

              # Update order with total
              order["record"]["total_amount"] = round(order_total, 2)
              result = await target.execute(json.dumps(order))
              assert result.is_success
              order_id += 1

      # Send state message
      state = {
          "type": "STATE",
          "value": {
              "bookmarks": {
                  "customers": {
                      "replication_key": "updated_at",
                      "replication_key_value": now,
                      "version": 1,
                  },
                  "products": {
                      "replication_key": "updated_at",
                      "replication_key_value": now,
                      "version": 1,
                  },
                  "orders": {
                      "replication_key": "updated_at",
                      "replication_key_value": now,
                      "version": 1,
                  },
              },
          },
      }
      result = await target.execute(json.dumps(state))
      assert result.is_success

      # Verify data in Oracle
      with oracle_engine.connect() as conn:
          # Check tables created
          tables = conn.execute(
              text(
                  """
                  SELECT table_name
                  FROM user_tables
                  WHERE table_name IN ('CUSTOMERS', 'PRODUCTS', 'ORDERS', 'ORDER_ITEMS')
                  ORDER BY table_name
                  """,
              ),
          ).fetchall()
          assert len(tables) == 4

          # Verify customer data with flattened address
          customer_count = conn.execute(
              text("SELECT COUNT(*) FROM customers"),
          ).scalar()
          assert customer_count == 100

          # Check flattened columns exist
          columns = conn.execute(
              text(
                  """
                  SELECT column_name
                  FROM user_tab_columns
                  WHERE table_name = 'CUSTOMERS'
                  AND column_name LIKE 'ADDRESS__%'
                  ORDER BY column_name
                  """,
              ),
          ).fetchall()
          assert len(columns) == 4  # street, city, state, zip

          # Verify foreign key indexes were created
          indexes = conn.execute(
              text(
                  """
                  SELECT index_name, table_name
                  FROM user_indexes
                  WHERE table_name IN ('ORDERS', 'ORDER_ITEMS')
                  AND index_name LIKE '%FK%'
                  """,
              ),
          ).fetchall()
          assert (
              len(indexes) >= 2
          )  # At least FK indexes for customer_id and product_id

          # Test complex query with joins
          result = conn.execute(
              text(
                  """
                  SELECT
                      c.name as customer_name,
                      COUNT(DISTINCT o.order_id) as order_count,
                      SUM(o.total_amount) as total_spent
                  FROM customers c
                  JOIN orders o ON c.customer_id = o.customer_id
                  WHERE o.status = 'delivered'
                  GROUP BY c.name
                  HAVING COUNT(DISTINCT o.order_id) > 0
                  ORDER BY total_spent DESC
                  FETCH FIRST 10 ROWS ONLY
                  """,
              ),
          ).fetchall()
          assert len(result) > 0

    @pytest.mark.asyncio
    async def test_schema_evolution_workflow(
      self,
      oracle_config: FlextOracleTargetConfig,
      oracle_engine,
      clean_database,
    ) -> None:
      """Test schema evolution with ALTER TABLE support."""
      oracle_config.allow_alter_table = True
      oracle_config.sdc_mode = "merge"

      target = FlextOracleTarget(config=oracle_config)
      await target.initialize()

      # Initial schema
      schema_v1 = {
          "type": "SCHEMA",
          "stream": "evolving_table",
          "schema": {
              "type": "object",
              "properties": {
                  "id": {"type": "integer"},
                  "name": {"type": "string"},
                  "created_at": {"type": "string", "format": "date-time"},
              },
          },
          "key_properties": ["id"],
      }

      # Create table with initial schema
      result = await target.execute(json.dumps(schema_v1))
      assert result.is_success

      # Insert initial data
      record_v1 = {
          "type": "RECORD",
          "stream": "evolving_table",
          "record": {
              "id": 1,
              "name": "Initial Record",
              "created_at": datetime.now(UTC).isoformat(),
          },
      }
      result = await target.execute(json.dumps(record_v1))
      assert result.is_success

      # Evolved schema - add new columns
      schema_v2 = {
          "type": "SCHEMA",
          "stream": "evolving_table",
          "schema": {
              "type": "object",
              "properties": {
                  "id": {"type": "integer"},
                  "name": {"type": "string"},
                  "email": {"type": "string", "format": "email"},  # New
                  "age": {"type": "integer"},  # New
                  "is_active": {"type": "boolean"},  # New
                  "metadata": {  # New nested object
                      "type": "object",
                      "properties": {
                          "source": {"type": "string"},
                          "version": {"type": "string"},
                      },
                  },
                  "created_at": {"type": "string", "format": "date-time"},
                  "updated_at": {"type": "string", "format": "date-time"},  # New
              },
          },
          "key_properties": ["id"],
      }

      # Apply evolved schema
      result = await target.execute(json.dumps(schema_v2))
      assert result.is_success

      # Insert data with new columns
      record_v2 = {
          "type": "RECORD",
          "stream": "evolving_table",
          "record": {
              "id": 2,
              "name": "Evolved Record",
              "email": "evolved@example.com",
              "age": 30,
              "is_active": True,
              "metadata": {
                  "source": "api",
                  "version": "2.0",
              },
              "created_at": datetime.now(UTC).isoformat(),
              "updated_at": datetime.now(UTC).isoformat(),
          },
      }
      result = await target.execute(json.dumps(record_v2))
      assert result.is_success

      # Update existing record with new fields
      record_v1_updated = {
          "type": "RECORD",
          "stream": "evolving_table",
          "record": {
              "id": 1,
              "name": "Initial Record Updated",
              "email": "initial@example.com",
              "age": 25,
              "is_active": True,
              "metadata": {
                  "source": "manual",
                  "version": "1.0",
              },
              "created_at": record_v1["record"]["created_at"],
              "updated_at": datetime.now(UTC).isoformat(),
          },
      }
      result = await target.execute(json.dumps(record_v1_updated))
      assert result.is_success

      # Verify schema evolution in database
      with oracle_engine.connect() as conn:
          # Check all columns exist
          columns = conn.execute(
              text(
                  """
                  SELECT column_name, data_type
                  FROM user_tab_columns
                  WHERE table_name = 'EVOLVING_TABLE'
                  ORDER BY column_id
                  """,
              ),
          ).fetchall()

          column_names = [col[0] for col in columns]
          assert "EMAIL" in column_names
          assert "AGE" in column_names
          assert "IS_ACTIVE" in column_names
          assert "METADATA__SOURCE" in column_names
          assert "METADATA__VERSION" in column_names
          assert "UPDATED_AT" in column_names

          # Verify data integrity
          records = conn.execute(
              text(
                  """
                  SELECT id, name, email, age, is_active
                  FROM evolving_table
                  ORDER BY id
                  """,
              ),
          ).fetchall()

          assert len(records) == 2
          assert records[0][2] == "initial@example.com"  # First record updated
          assert records[1][2] == "evolved@example.com"  # Second record

    @pytest.mark.asyncio
    async def test_high_volume_streaming(
      self,
      oracle_config: FlextOracleTargetConfig,
      oracle_engine,
      clean_database,
    ) -> None:
      """Test high-volume data streaming with performance metrics."""
      # Configure for performance
      oracle_config.batch_size = 10000
      oracle_config.load_method = LoadMethod.BULK_INSERT
      oracle_config.use_direct_path = True
      oracle_config.parallel_degree = 4
      oracle_config.sdc_mode = "append"  # Faster for bulk loads

      target = FlextOracleTarget(config=oracle_config)
      await target.initialize()

      # Schema for high-volume events
      schema = {
          "type": "SCHEMA",
          "stream": "events",
          "schema": {
              "type": "object",
              "properties": {
                  "event_id": {"type": "string"},
                  "event_type": {"type": "string"},
                  "user_id": {"type": "integer"},
                  "timestamp": {"type": "string", "format": "date-time"},
                  "properties": {"type": "object"},
                  "context": {
                      "type": "object",
                      "properties": {
                          "ip": {"type": "string"},
                          "user_agent": {"type": "string"},
                          "page": {"type": "string"},
                      },
                  },
              },
          },
          "key_properties": ["event_id"],
      }

      result = await target.execute(json.dumps(schema))
      assert result.is_success

      # Generate and stream large volume of events
      start_time = time.time()
      event_types = ["page_view", "click", "purchase", "signup", "logout"]
      total_events = 100000  # 100k events

      # Process in batches to simulate streaming
      batch_size = 5000
      for batch_start in range(0, total_events, batch_size):
          batch_end = min(batch_start + batch_size, total_events)

          for i in range(batch_start, batch_end):
              event = {
                  "type": "RECORD",
                  "stream": "events",
                  "record": {
                      "event_id": f"evt_{i:08d}",
                      "event_type": event_types[i % len(event_types)],
                      "user_id": (i % 10000) + 1,
                      "timestamp": datetime.now(UTC).isoformat(),
                      "properties": {
                          "value": i * 0.01,
                          "category": f"cat_{i % 100}",
                      },
                      "context": {
                          "ip": f"192.168.{i % 256}.{(i // 256) % 256}",
                          "user_agent": f"Mozilla/5.0 (Test {i % 10})",
                          "page": f"/page/{i % 1000}",
                      },
                  },
              }
              result = await target.execute(json.dumps(event))
              assert result.is_success

          # Small delay between batches to simulate real streaming
          await asyncio.sleep(0.1)

      end_time = time.time()
      elapsed = end_time - start_time

      # Verify performance and data integrity
      with oracle_engine.connect() as conn:
          # Check record count
          count = conn.execute(text("SELECT COUNT(*) FROM events")).scalar()
          assert count == total_events

          # Calculate throughput
          records_per_second = total_events / elapsed

          # Performance assertion
          assert records_per_second > 1000  # Should handle > 1k records/sec

          # Verify data distribution
          distribution = conn.execute(
              text(
                  """
                  SELECT event_type, COUNT(*) as cnt
                  FROM events
                  GROUP BY event_type
                  ORDER BY event_type
                  """,
              ),
          ).fetchall()

          assert len(distribution) == len(event_types)
          for row in distribution:
              assert row[1] == total_events // len(event_types)
