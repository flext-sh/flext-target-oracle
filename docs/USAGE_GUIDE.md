# Oracle Target Usage Guide

## Quick Start

### Installation

```bash
pip install flext-target-oracle
```

### Basic Configuration

Create a `config.json` file:

```json
{
  "host": "oracle.example.com",
  "port": 1521,
  "user": "your_username",
  "password": "your_password",
  "service_name": "ORCL"
}
```

### Running the Target

```bash
# From a tap
tap-csv | target-oracle --config config.json

# From a file
target-oracle --config config.json < messages.jsonl

# With state
tap-salesforce --state state.json | target-oracle --config config.json
```

## Configuration Examples

### Minimal Configuration

```json
{
  "host": "localhost",
  "user": "scott",
  "password": "tiger",
  "service_name": "ORCL"
}
```

### Production Configuration

```json
{
  "host": "oracle-prod.company.com",
  "port": 1521,
  "user": "etl_user",
  "password": "${ORACLE_PASSWORD}",
  "service_name": "PRODDB",

  "default_target_schema": "DW",
  "table_prefix": "SINGER_",

  "batch_size_rows": 50000,
  "parallel_threads": 8,
  "pool_size": 20,
  "pool_recycle": 3600,

  "load_method": "append-only",
  "add_record_metadata": true,
  "use_direct_path": true,
  "enable_parallel_dml": true
}
```

### High-Performance Configuration

```json
{
  "host": "oracle-cluster.company.com",
  "user": "bulk_loader",
  "password": "${ORACLE_PASSWORD}",
  "service_name": "DW",

  "batch_size_rows": 100000,
  "parallel_threads": 16,
  "pool_size": 50,

  "use_direct_path": true,
  "enable_parallel_dml": true,
  "optimizer_mode": "ALL_ROWS",

  "alter_session": [
    "ALTER SESSION SET PARALLEL_DEGREE_POLICY = AUTO",
    "ALTER SESSION SET PARALLEL_MIN_TIME_THRESHOLD = 1"
  ]
}
```

## Load Methods

### Append-Only (Default)

Fastest method, always inserts new records:

```json
{
  "load_method": "append-only"
}
```

**Use when:**

- Loading to staging tables
- Processing immutable event streams
- Performance is critical

### Upsert

Updates existing records, inserts new ones:

```json
{
  "load_method": "upsert"
}
```

**Use when:**

- Loading dimension tables
- Syncing master data
- Need latest version of records

**Note:** Requires key properties in the stream schema.

### Overwrite

Truncates table before loading:

```json
{
  "load_method": "overwrite"
}
```

**Use when:**

- Full refreshes
- Small reference tables
- Testing environments

## Performance Tuning

### Batch Size

Adjust based on available memory:

```json
{
  "batch_size_rows": 10000 // Default, good for most cases
}
```

**Guidelines:**

- Small records: 50,000-100,000
- Large records: 5,000-10,000
- Limited memory: 1,000-5,000

### Parallel Processing

Enable for large datasets:

```json
{
  "parallel_threads": 8,
  "batch_size_rows": 50000
}
```

**Guidelines:**

- CPU cores × 2 = good starting point
- Monitor CPU usage and adjust
- Diminishing returns above 16 threads

### Connection Pooling

Configure based on parallelism:

```json
{
  "pool_size": 20,
  "pool_recycle": 3600,
  "pool_timeout": 30
}
```

**Guidelines:**

- pool_size = parallel_threads × 2
- pool_recycle prevents stale connections
- pool_timeout prevents hanging

### Direct Path Loading

Enable for bulk loads:

```json
{
  "use_direct_path": true,
  "batch_size_rows": 100000
}
```

**Benefits:**

- Bypasses buffer cache
- Faster for large batches
- Less redo log generation

**Limitations:**

- No triggers fired
- No foreign key checks during load
- Exclusive table lock

## Schema Management

### Automatic Table Creation

Tables are created automatically based on stream schema:

```json
{
  "default_target_schema": "ETL",
  "table_prefix": "RAW_"
}
```

Results in tables like: `ETL.RAW_CUSTOMERS`

### Column Type Optimization

Enable pattern recognition for better types:

```json
{
  "enable_column_patterns": true
}
```

Automatically maps:

- `customer_id` → NUMBER(38,0)
- `active_flg` → NUMBER(1,0)
- `created_ts` → TIMESTAMP WITH TIME ZONE
- `total_amount` → NUMBER(19,4)

### Audit Fields

Automatically added when enabled:

```json
{
  "add_record_metadata": true
}
```

Adds columns:

- `CREATE_USER`: Who created the record
- `CREATE_TS`: When created
- `MOD_USER`: Who last modified
- `MOD_TS`: When last modified

## Error Handling

### Connection Errors

The target automatically retries on connection errors:

```json
{
  "retry_count": 3,
  "retry_delay": 5
}
```

### Batch Failures

Failed batches are logged with details:

```
ERROR: Batch processing failed: ORA-01400: cannot insert NULL
Failed batch size: 1000 records
Stream: customers
```

### Data Type Errors

Automatic type conversion with fallbacks:

```python
# String to number conversion
"123.45" → 123.45

# Boolean to number
true → 1
false → 0

# Date parsing
"2024-01-15T10:30:00Z" → TIMESTAMP
```

## Monitoring

### Logging

Enable detailed logging:

```json
{
  "echo": true, // Log SQL statements
  "log_level": "DEBUG"
}
```

### Performance Metrics

Monitor key metrics in logs:

```
INFO: Processed batch of 50000 records in 2.34s (21,368 records/sec)
INFO: Stream customers complete: 1000000 records in 47.2s
```

### Health Checks

Built-in health monitoring:

```python
# Check connection health
health = target._check_engine_health()
print(health)
# {
#   "sync_engine": {
#     "status": "healthy",
#     "pool_size": 20,
#     "checked_out": 5
#   }
# }
```

## Best Practices

### 1. Start Simple

Begin with default settings:

```json
{
  "host": "oracle.example.com",
  "user": "username",
  "password": "password",
  "service_name": "ORCL"
}
```

### 2. Test Load Methods

Try different methods on sample data:

```bash
# Test append
target-oracle --config append-config.json < sample.jsonl

# Test upsert
target-oracle --config upsert-config.json < sample.jsonl
```

### 3. Monitor and Adjust

Watch performance metrics and tune:

1. Start with default batch size
2. Increase if memory allows
3. Enable parallelism for large datasets
4. Use direct path for bulk loads

### 4. Use Schemas

Always specify target schema:

```json
{
  "default_target_schema": "STAGE",
  "table_prefix": "${TAP_NAME}_"
}
```

### 5. Handle Failures

Implement proper error handling:

```bash
#!/bin/bash
tap-source | target-oracle --config config.json || {
  echo "Pipeline failed"
  # Send alert
  exit 1
}
```

## Troubleshooting

### Connection Issues

**Error:** `ORA-12154: TNS:could not resolve the connect identifier`

**Solution:** Check service_name or use full DSN:

```json
{
  "dsn": "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL)))"
}
```

### Performance Issues

**Symptom:** Slow loading

**Solutions:**

1. Increase batch size
2. Enable parallel processing
3. Use direct path loading
4. Check network latency

### Memory Issues

**Error:** `MemoryError`

**Solutions:**

1. Reduce batch size
2. Disable parallelism
3. Process streams separately

### Type Conversion Errors

**Error:** `ORA-01722: invalid number`

**Solutions:**

1. Check source data quality
2. Enable type validation
3. Use CLOB for mixed types

## Advanced Usage

### Custom Session Parameters

Set Oracle session parameters:

```json
{
  "alter_session": [
    "ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD'",
    "ALTER SESSION SET TIME_ZONE='UTC'",
    "ALTER SESSION SET WORKAREA_SIZE_POLICY=MANUAL",
    "ALTER SESSION SET SORT_AREA_SIZE=100000000"
  ]
}
```

### Environment Variables

Use environment variables for sensitive data:

```json
{
  "host": "${ORACLE_HOST}",
  "user": "${ORACLE_USER}",
  "password": "${ORACLE_PASSWORD}",
  "service_name": "${ORACLE_SERVICE}"
}
```

### Dynamic Table Names

Use Singer metadata for custom table names:

```json
{
  "stream_maps": {
    "customers": {
      "destination_table": "CUSTOMER_MASTER"
    }
  }
}
```

### Conditional Loading

Skip certain streams:

```json
{
  "exclude_streams": ["temp_*", "test_*"],
  "include_streams": ["customers", "orders", "products"]
}
```
