# Modern Singer SDK Architecture Design for flext-target-oracle

## Overview

This document outlines the modernized architecture for flext-target-oracle using Singer SDK with SOLID, KISS, and DRY principles for a completely generic and professional Oracle target.

## Core Design Principles

### 1. SOLID Principles

#### Single Responsibility (SRP)
- **OracleTarget**: Only handles target initialization and configuration
- **OracleSink**: Only manages data persistence to Oracle
- **OracleConnector**: Only manages database connections
- **TypeMapper**: Only handles type conversions
- **BatchProcessor**: Only manages batch operations
- **PerformanceOptimizer**: Only handles performance tuning

#### Open/Closed (OCP)
- Base classes for extension without modification
- Strategy pattern for different load methods
- Plugin architecture for custom type mappings

#### Liskov Substitution (LSP)
- All sinks properly extend Singer SDK's SQLSink
- Type mappers implement consistent interfaces

#### Interface Segregation (ISP)
- Separate interfaces for:
  - ITypeMapper
  - IBatchProcessor
  - IPerformanceOptimizer
  - IConnectionManager

#### Dependency Inversion (DIP)
- Depend on abstractions (interfaces) not concrete classes
- Inject dependencies through constructors

### 2. KISS (Keep It Simple, Stupid)
- Remove complex inheritance chains
- Use composition over inheritance
- Clear, descriptive naming
- Minimal configuration with sensible defaults

### 3. DRY (Don't Repeat Yourself)
- Centralized type mapping rules
- Shared utilities module
- Reusable batch processing logic
- Common error handling patterns

## Architecture Components

### Core Modules

```
flext_target_oracle/
├── __init__.py
├── target.py          # Main target class (minimal)
├── sink.py            # Oracle sink implementation
├── connector.py       # Database connection management
├── core/
│   ├── __init__.py
│   ├── interfaces.py  # Abstract interfaces
│   ├── exceptions.py  # Custom exceptions
│   └── constants.py   # Shared constants
├── typing/
│   ├── __init__.py
│   ├── mapper.py      # Type mapping logic
│   ├── rules.py       # Type mapping rules
│   └── validators.py  # Type validation
├── batch/
│   ├── __init__.py
│   ├── processor.py   # Batch processing logic
│   ├── strategies.py  # Load strategies (append, upsert, etc)
│   └── optimizer.py   # Performance optimization
├── utils/
│   ├── __init__.py
│   ├── retry.py       # Retry logic
│   ├── monitoring.py  # Metrics and monitoring
│   └── logging.py     # Structured logging
└── cli.py             # CLI entry point
```

### Core Features

1. **Intelligent Type Mapping**
   - Configurable type mapping rules
   - Pattern-based type detection
   - JSON schema to Oracle type conversion
   - Support for custom type mappings

2. **Advanced Table Management**
   - Configurable table creation strategies
   - Support for various primary key patterns
   - Optional audit field addition
   - Intelligent index creation

3. **Performance Optimization**
   - Lazy connection pattern
   - Configurable batch sizes
   - Parallel processing support
   - Direct path loading options
   - Advanced connection pooling

4. **Data Type Handling**
   - Null value handling
   - Timezone support
   - Large text handling (VARCHAR2/CLOB)
   - Boolean mapping options

## Implementation Plan

### Phase 1: Core Structure
1. Create interface definitions
2. Implement type mapping system
3. Build connection management
4. Create base sink class

### Phase 2: Core Logic
1. Implement configurable type mapping
2. Create flexible table management
3. Add batch processing system
4. Implement multiple load strategies

### Phase 3: Performance
1. Add lazy connection pattern
2. Implement parallel processing
3. Add performance optimizations
4. Create monitoring system

### Phase 4: Testing & Validation
1. Unit tests for each component
2. Integration tests with Oracle
3. Performance benchmarks
4. Business logic validation

## Configuration Schema

```python
config_schema = {
    # Connection
    "host": {"type": "string", "required": True},
    "port": {"type": "integer", "default": 1521},
    "service_name": {"type": "string"},
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": True, "secret": True},
    "schema": {"type": "string"},
    
    # Performance
    "batch_size": {"type": "integer", "default": 50000},
    "parallel_threads": {"type": "integer", "default": 8},
    "connection_pool_size": {"type": "integer", "default": 10},
    
    # Load Method
    "load_method": {
        "type": "string", 
        "enum": ["append-only", "upsert", "overwrite"],
        "default": "append-only"
    },
    
    # Type Mapping
    "type_mapping_rules": {"type": "object"},
    "enable_smart_typing": {"type": "boolean", "default": True},
    
    # Oracle Features
    "use_direct_path": {"type": "boolean", "default": True},
    "enable_compression": {"type": "boolean", "default": False},
    "enable_partitioning": {"type": "boolean", "default": False}
}
```

## Benefits of This Architecture

1. **Maintainability**: Clear separation of concerns
2. **Testability**: Each component can be tested independently
3. **Extensibility**: Easy to add new features without breaking existing code
4. **Performance**: Optimized for high-volume data loads
5. **Reliability**: Robust error handling and retry logic