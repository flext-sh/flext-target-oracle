# FLEXT Target Oracle - Enterprise Oracle Database Loading

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Singer SDK](https://img.shields.io/badge/singer--sdk-compliant-brightgreen.svg)](https://sdk.meltano.com/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture%20%2B%20DDD-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Coverage](https://img.shields.io/badge/coverage-90%25+-brightgreen.svg)](https://pytest.org)

Singer-compliant target for loading data into Oracle databases. Built with Python 3.13+, Clean Architecture, and Domain-Driven Design patterns as part of the FLEXT enterprise data integration platform.

## Overview

FLEXT Target Oracle provides enterprise-grade data loading capabilities for Oracle databases, implementing the Singer specification for standardized data integration workflows. The target leverages the FLEXT ecosystem's layered architecture for robust Oracle connectivity and optimal performance.

### Key Features

- **Oracle Database Loading**: Comprehensive data loading into Oracle 11g, 12c, 18c, 19c, 21c, and 23c
- **Singer Protocol Compliance**: Full Singer SDK implementation with stream processing
- **Layered Architecture**: Clean separation leveraging FLEXT ecosystem libraries
- **Performance Optimization**: Oracle-specific optimizations and bulk operations
- **Clean Architecture**: Domain-driven design with flext-core integration
- **Zero Tolerance Quality**: 90% test coverage with comprehensive quality gates

This target provides a streamlined Oracle database loader for Singer pipelines, built on top of:

- **flext-core**: Core patterns and utilities
- **flext-meltano**: Singer SDK integration and base classes  
- **flext-db-oracle**: Oracle database operations

## 🏗️ Architecture

### Clean Structure

```
src/flext_target_oracle/
├── __init__.py          # Main exports
├── config.py            # Configuration (inherits from FlextBaseConfig)
├── target.py            # Main target (inherits from FlextBatchTarget)
├── loader.py            # Oracle loader (uses flext-db-oracle)
├── exceptions.py        # Oracle-specific exceptions
├── domain.bak/          # Legacy domain models (backup)
├── application.bak/     # Legacy services (backup)
└── target.py.bak        # Legacy target implementation (backup)
```

### Key Features

- ✅ **Inherits from FlextBatchTarget**: Uses flext-meltano base classes
- ✅ **Uses FlextBaseConfig**: Standardized configuration management
- ✅ **Leverages flext-db-oracle**: Oracle operations via established library
- ✅ **Singer Bridge Integration**: Uses FlextSingerBridge for message handling
- ✅ **Clean Error Handling**: FlextResult patterns throughout
- ✅ **Batch Processing**: Efficient record buffering and batch inserts
- ✅ **JSON Storage**: Simple CLOB-based storage for flexibility

## 🚀 Usage

### Basic Configuration

```python
from flext_target_oracle import OracleTarget, OracleTargetConfig

config = OracleTargetConfig(
    host="localhost",
    port=1521,
    service_name="XE",
    username="singer_user",
    password="password",
    default_target_schema="SINGER_DATA",
    batch_size=10000
)

target = OracleTarget(config)
```

### Processing Messages

```python
# Schema message
schema_msg = {
    "type": "SCHEMA",
    "stream": "users",
    "schema": {"type": "object", "properties": {...}}
}

# Record message  
record_msg = {
    "type": "RECORD",
    "stream": "users", 
    "record": {"id": 1, "name": "John"}
}

# Process messages
await target.process_singer_message(schema_msg)
await target.process_singer_message(record_msg)
await target.finalize()
```

## 📋 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `host` | str | - | Oracle host |
| `port` | int | 1521 | Oracle port |
| `service_name` | str | - | Oracle service name |
| `sid` | str | - | Oracle SID (alternative to service_name) |
| `username` | str | - | Oracle username |
| `password` | str | - | Oracle password |
| `protocol` | str | "tcp" | Connection protocol |
| `default_target_schema` | str | "SINGER_DATA" | Target schema for tables |
| `table_prefix` | str | "" | Prefix for table names |
| `load_method` | LoadMethod | APPEND_ONLY | Data loading strategy |
| `batch_size` | int | 10000 | Records per batch |
| `use_bulk_operations` | bool | True | Enable Oracle bulk operations |
| `compression` | bool | False | Enable Oracle compression |
| `parallel_degree` | int | 1 | Oracle parallel processing degree |

## 🔧 Development

### Testing Structure

```bash
# Test basic structure (without external dependencies)
python test_structure.py

# Test with full dependencies
python test_simple.py
```

### Dependencies

- flext-core: Core patterns and utilities
- flext-meltano: Singer SDK integration
- flext-db-oracle: Oracle database operations

## 📦 Migration from Legacy

The legacy implementation has been preserved in `.bak` files:

- `domain.bak/`: Original domain models and entities
- `application.bak/`: Original service layer
- `target.py.bak`: Original target implementation

### Key Changes

1. **Simplified Architecture**: Removed complex domain/application layers
2. **Base Class Inheritance**: Now inherits from FlextBatchTarget
3. **Standardized Config**: Uses FlextBaseConfig pattern
4. **External Dependencies**: Leverages flext-db-oracle for Oracle operations
5. **Clean APIs**: Simplified public interface

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Follow flext-core patterns and conventions
2. Use flext-meltano base classes when possible
3. Leverage flext-db-oracle for Oracle operations
4. Maintain clean, simple, and testable code
5. Preserve backward compatibility where possible
