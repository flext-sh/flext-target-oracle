# Usage Guide

Production guide for flext-target-oracle using FLEXT enterprise architecture.

## Setup

### Installation

```bash
# Development setup
make install
cp .env.example .env
# Edit .env with Oracle credentials
```

### Configuration

Create config.JSON using FLEXT patterns:

```json
{
  "oracle_config": {
    "host": "oracle.example.com",
    "port": 1521,
    "service_name": "PROD",
    "username": "etl_user",
    "password": "secure_password"
  },
  "default_target_schema": "DW",
  "batch_size": 10000,
  "load_method": "append_only"
}
```

### Running

```bash
# With Singer tap
tap-csv --config tap-config.json | target-oracle --config config.json

# Test mode
make test-integration
```

## Load Methods

### append_only (Default)

Fast bulk inserts for new data:

```json
{"load_method": "append_only"}
```

### upsert  

Oracle MERGE operations for incremental updates:

```json
{"load_method": "upsert"}
```

### overwrite

Truncate and reload:

```json
{"load_method": "overwrite"}
```

## Performance Tuning

### Batch Processing

```json
{
  "batch_size": 50000,
  "pool_size": 20
}
```

### Oracle Autonomous Database

```json
{
  "oracle_config": {
    "host": "your-adb.adb.region.oraclecloud.com",
    "port": 1522,
    "service_name": "your_service_high",
    "protocol": "tcps",
    "username": "admin",
    "password": "password",
    "wallet_location": "/path/to/wallet",
    "wallet_password": "wallet_password"
  }
}
```

## Type Mapping & Schema Management

Built-in intelligent type mapping:

- `*_ID` columns → NUMBER(38,0)
- `*_FLG` columns → NUMBER(1,0)
- `*_TS` columns → TIMESTAMP
- `*_AMOUNT` columns → NUMBER(19,4)
- JSON objects → CLOB

Tables are automatically created based on Singer schemas with proper Oracle types.

## Monitoring & Troubleshooting

### Built-in Monitoring

- flext-observability integration for structured logging
- Performance metrics and batch statistics
- Health checks for Oracle connections

### Common Issues

**Connection errors**: Verify .env configuration and Oracle connectivity
**Performance**: Adjust batch_size and pool_size based on workload
**Type errors**: Review column patterns and Oracle type mappings

### Debug Mode

```bash
# Enable detailed logging
make test-integration VERBOSE=1
```

## Production Best Practices

1. **Configuration**: Use .env for credentials, config.JSON for settings
2. **Performance**: Start with defaults, tune based on data volume
3. **Monitoring**: Use flext-observability for production monitoring
4. **Error Handling**: Implement proper retry logic in ETL pipelines
5. **Schema Management**: Use appropriate target schemas and prefixes

See `docs/ARCHITECTURE.md` for technical details on FLEXT patterns and Oracle optimizations.
