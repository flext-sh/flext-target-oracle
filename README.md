# flext-target-oracle

A high-performance [Singer](https://singer.io) target for Oracle Database, built with the modern [Singer SDK](https://sdk.meltano.com) and optimized for enterprise workloads.

## Features

### 🚀 Performance
- **Parallel Processing**: Multi-threaded batch processing for maximum throughput
- **Direct Path Loading**: Oracle direct path inserts for bulk operations
- **Intelligent Batching**: Configurable batch sizes with automatic optimization
- **Connection Pooling**: Advanced connection management for high concurrency
- **Lazy Connections**: No database connection until data arrives

### 🎯 Type Mapping
- **Intelligent Type Detection**: Pattern-based column type mapping
- **Configurable Rules**: Custom type mapping via configuration
- **JSON Schema Support**: Full JSON schema to Oracle type conversion
- **Large Text Handling**: Automatic VARCHAR2/CLOB selection

### 🔧 Enterprise Features
- **Historical Versioning**: Optional time-series data support
- **Audit Fields**: Configurable audit column addition
- **Compression Support**: Table and index compression options
- **Partitioning**: Automatic partition management
- **Performance Monitoring**: Built-in metrics and logging

### 🔒 Reliability
- **Transaction Management**: ACID compliance with rollback support
- **Error Handling**: Detailed error reporting and recovery
- **Schema Evolution**: Automatic schema updates
- **Data Validation**: Input validation and type checking

## Quick Start

### Installation

```bash
# Setup development environment
make install

# Copy and configure environment
cp .env.example .env
# Edit .env with your Oracle database credentials
```

### Basic Usage

```bash
# Run unit tests (no database needed)
make test-unit

# Run integration tests (needs Oracle)
make test-integration

# Run the target
make run
```

### Configuration

Create a `config.json`:

```json
{
  "host": "localhost",
  "port": 1521,
  "service_name": "XEPDB1",
  "username": "target_user",
  "password": "secure_password",
  "schema": "TARGET_SCHEMA"
}
```

### Oracle Autonomous Database

```json
{
  "host": "your-adb.adb.region.oraclecloud.com",
  "port": 1522,
  "service_name": "your_service_high",
  "protocol": "tcps",
  "username": "your_user",
  "password": "your_password",
  "wallet_location": "/path/to/wallet",
  "wallet_password": "wallet_password"
}
```

## Configuration Reference

### Essential Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | string | **required** | Oracle host |
| `port` | integer | 1521 | Oracle port |
| `service_name` | string | | Oracle service name |
| `database` | string | | Oracle SID (alternative) |
| `username` | string | **required** | Username |
| `password` | string | **required** | Password |
| `schema` | string | | Default schema |

### Performance Optimization

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `batch_config.batch_size` | integer | 10000 | Records per batch |
| `pool_size` | integer | 10 | Connection pool size |
| `use_bulk_operations` | boolean | true | Use bulk operations |
| `use_merge_statements` | boolean | true | Use MERGE for upserts |
| `parallel_degree` | integer | 1 | Oracle parallel degree |

### Advanced Features

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `load_method` | string | append-only | Load method: append-only, upsert, overwrite |
| `enable_compression` | boolean | false | Enable table compression |
| `compression_type` | string | basic | Compression: basic, advanced, hybrid |
| `create_table_indexes` | boolean | true | Create indexes on keys |
| `add_record_metadata` | boolean | true | Add Singer metadata |

## Advanced Usage

### High-Performance Configuration

```json
{
  "host": "oracle-server",
  "port": 1521,
  "service_name": "PROD",
  "username": "etl_user",
  "password": "secure_password",
  
  "batch_config": {
    "batch_size": 50000,
    "batch_wait_limit_seconds": 30
  },
  
  "pool_size": 20,
  "max_overflow": 40,
  "use_bulk_operations": true,
  "use_merge_statements": true,
  "parallel_degree": 4,
  
  "enable_compression": true,
  "compression_type": "advanced",
  "use_direct_path": true,
  
  "load_method": "upsert"
}
```

### All Configuration Parameters

The target supports 100+ configuration parameters. Key categories:

- **Connection**: host, port, service_name, protocol, wallet settings
- **SQLAlchemy Engine**: pool settings, echo, isolation level
- **Oracle Driver**: array_size, prefetch_rows, statement cache
- **Singer SDK**: batch_config, stream_maps, flattening
- **Performance**: parallel processing, compression, direct path
- **Data Types**: varchar length, number precision, JSON storage
- **Error Handling**: retries, backoff, error tolerance
- **Table Management**: prefixes, indexes, statistics
- **Monitoring**: logging, metrics, profiling

See `config.json.example` for a complete example.

## Oracle-Specific Features

### MERGE Operations

Automatically uses Oracle MERGE for upserts when `load_method` is "upsert":

```sql
MERGE INTO target_table
USING (SELECT :id, :name, :email FROM dual) source
ON (target_table.id = source.id)
WHEN MATCHED THEN UPDATE SET name = source.name, email = source.email
WHEN NOT MATCHED THEN INSERT (id, name, email) VALUES (source.id, source.name, source.email)
```

### Compression

Enable table compression for storage efficiency:

```json
{
  "enable_compression": true,
  "compression_type": "advanced"
}
```

### Parallel Processing

Utilize Oracle parallel processing:

```json
{
  "parallel_degree": 4,
  "use_parallel_dml": true
}
```

## Development

### Available Commands

```bash
# Setup
make install         # Install package
make clean          # Clean build files

# Testing  
make test-unit      # Unit tests (no database)
make test-integration # Integration tests (needs Oracle)
make test-all       # All tests
make test           # Alias for test-all

# Quality
make lint           # Code linting
make format         # Code formatting
make check          # Quick check (lint + unit tests)
make validate       # Full validation (format + lint + all tests)

# Usage
make run            # Run the target (needs .env)

# Shortcuts
make dev            # Setup + check
make quick          # Format + unit tests
make full           # Complete validation
```

### Requirements

- Python 3.9+
- Oracle Database (any edition)
- Virtual environment at `/home/marlonsc/flext/.venv`

## Testing

### Unit Tests
No Oracle database required. Tests configuration, type mapping, and basic functionality.

```bash
make test-unit
```

### Integration Tests  
Requires Oracle database connection configured in `.env`.

```bash
make test-integration
```

### Complete Test Suite
Runs all tests including performance and enterprise features.

```bash
make test-all
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run code quality checks
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Issues: [GitHub Issues](https://github.com/flext/flext-target-oracle/issues)
- Documentation: [Singer SDK Docs](https://sdk.meltano.com/)
- Oracle Docs: [Oracle Database Documentation](https://docs.oracle.com/en/database/)

## Credits

Built with:
- [Singer SDK](https://sdk.meltano.com/) - The best way to build Singer taps and targets
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL toolkit
- [oracledb](https://oracle.github.io/python-oracledb/) - Python driver for Oracle Database