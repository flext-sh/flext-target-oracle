# flext-target-oracle

Production-grade Singer target for Oracle Database implementing FLEXT enterprise patterns.

## FLEXT Integration

Part of the comprehensive FLEXT data platform ecosystem:

- **flext-core**: Domain-driven design, ServiceResult patterns, entity modeling
- **flext-db-oracle**: Oracle-specific database operations, connection management, query optimization
- **flext-observability**: Structured logging, metrics collection, health monitoring
- **flext-meltano**: Singer/Meltano protocol standardization across FLEXT ecosystem

## Key Features

- **Enterprise Architecture**: DDD patterns with domain models, services, and repositories
- **Oracle Optimization**: MERGE upserts, bulk operations, intelligent type mapping
- **Production Ready**: Async operations, transaction management, comprehensive error handling
- **FLEXT Standards**: Consistent patterns across all FLEXT Singer implementations

## Quick Start

### FLEXT Workspace Setup

```bash
# Install in FLEXT workspace environment
make install

# Configure Oracle connection (FLEXT standard)
cp .env.example .env
# Edit with Oracle credentials following FLEXT naming conventions
```

### Usage Within FLEXT Ecosystem

```bash
# Unit tests (no Oracle required)
make test-unit

# Integration tests (Oracle via .env)
make test-integration

# Use with other FLEXT components
flext-tap-oracle | flext-target-oracle --config config.json
```

### FLEXT-Standard Configuration

```json
{
  "oracle_config": {
    "host": "localhost",
    "service_name": "XEPDB1", 
    "username": "etl_user",
    "password": "secure_password"
  },
  "default_target_schema": "FLEXT_DW",
  "batch_size": 10000,
  "load_method": "append_only"
}
```

## Configuration

### Core Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `oracle_config.host` | Oracle server hostname | required |
| `oracle_config.port` | Oracle port | 1521 |
| `oracle_config.service_name` | Oracle service name | required |
| `oracle_config.username` | Database username | required |
| `oracle_config.password` | Database password | required |
| `default_target_schema` | Target schema for tables | required |

### Performance Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `batch_size` | Records per batch | 10000 |
| `load_method` | append_only, upsert, overwrite | append_only |
| `pool_size` | Connection pool size | 10 |

### Advanced Configuration

See `.env.example` for complete configuration options including:
- Oracle Autonomous Database with wallet support
- Performance tuning parameters  
- Oracle-specific features (compression, partitioning)
- Monitoring and logging configuration

## FLEXT Architecture Implementation

### Domain-Driven Design (flext-core)

```python
# Domain entities with proper modeling
class LoadJob(DomainEntity):
    stream_name: str
    status: LoadJobStatus
    records_processed: int

# Service patterns with consistent error handling  
class SingerTargetService:
    async def process_singer_message(self, message) -> ServiceResult[None]
```

### Oracle Integration (flext-db-oracle)

- **OracleConnectionService**: Managed connections with health monitoring
- **OracleQueryService**: Parameterized queries with performance optimization
- **OracleSchemaService**: Schema operations following Oracle best practices

### Observability (flext-observability)

- **Structured Logging**: Consistent log format across FLEXT ecosystem
- **Metrics Collection**: Load statistics, performance monitoring
- **Health Checks**: Database connectivity and operational status

### Load Strategies

- **append_only**: High-performance bulk inserts (FLEXT default)
- **upsert**: Oracle MERGE with conflict resolution
- **overwrite**: Transactional table refresh

## Development (FLEXT Standards)

### FLEXT Workspace Commands

```bash
# Development setup (uses /home/marlonsc/flext/.venv)
make install
make setup

# Testing (FLEXT standard patterns)
make test-unit         # Domain logic, no dependencies
make test-integration  # Oracle integration via .env
make quality-gate      # Required before commits to FLEXT ecosystem
```

### FLEXT Requirements

- **Python 3.13**: FLEXT enterprise standard
- **FLEXT Workspace**: Located at `/home/marlonsc/flext/`
- **Oracle Database**: Any edition, including Autonomous
- **FLEXT Dependencies**: flext-core, flext-db-oracle, flext-observability

## Testing Strategy

### FLEXT Test Organization
- **Unit**: Pure domain logic testing (DDD patterns)
- **Integration**: Oracle connectivity and flext-db-oracle integration
- **E2E**: Full Singer protocol workflows

### FLEXT Compliance Testing
Tests verify compliance with FLEXT standards:
- Domain entity validation
- ServiceResult pattern usage
- Error handling consistency
- Observability integration

## FLEXT Ecosystem Integration

This target integrates seamlessly with other FLEXT components:
- **flext-tap-oracle-***: Oracle data extraction
- **flext-web**: Web interface and monitoring
- **flext-api**: REST API integration
- **flext-observability**: Centralized monitoring

See `docs/ARCHITECTURE.md` for detailed FLEXT patterns implementation.
