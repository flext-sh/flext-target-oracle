# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Target Oracle is a production-grade Singer target for Oracle Database data loading, built using FLEXT ecosystem patterns. This is a Python 3.13+ library that integrates with the broader FLEXT data platform ecosystem, providing clean Oracle integration using established patterns from `flext-core`, `flext-meltano`, and `flext-db-oracle`.

## Architecture

### Clean Structure Architecture
The project follows a simplified, clean architecture after migrating from a complex domain/application layer structure:

```
src/flext_target_oracle/
├── __init__.py          # Main exports and exceptions
├── config.py            # Configuration (FlextOracleTargetConfig)  
├── target.py            # Main target (inherits from flext-meltano Target)
├── loader.py            # Oracle loader (uses flext-db-oracle)
├── exceptions.py        # Oracle-specific exceptions
├── domain.bak/          # Legacy domain models (backup)
├── application.bak/     # Legacy services (backup)
└── target.py.bak        # Legacy target implementation (backup)
```

### Key Dependencies
- **flext-core**: Base patterns, FlextResult, logging, FlextValueObject
- **flext-meltano**: Singer SDK integration and Target base class
- **flext-db-oracle**: Oracle database operations and connectivity
- **pydantic**: Configuration validation and type safety

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Oracle DB Integration Optimization
**Status**: ALTO - Integration com flext-db-oracle pode ser optimized
**Problema**:
- Loader implementation pode não fully leverage flext-db-oracle capabilities
- Connection management patterns podem be optimized
- Oracle-specific features podem não be fully utilized

**TODO**:
- [ ] Optimize integration com flext-db-oracle para performance
- [ ] Leverage advanced Oracle features via DB library
- [ ] Consolidate connection management patterns
- [ ] Document Oracle optimization strategies

### 🚨 GAP 2: Legacy Architecture Cleanup
**Status**: ALTO - Legacy backup files indicate architectural transition
**Problema**:
- domain.bak/ e application.bak/ indicate incomplete refactoring
- Target.py.bak suggests architectural changes in progress
- Legacy patterns podem still be referenced

**TODO**:
- [ ] Complete architectural migration cleanup
- [ ] Remove legacy backup files após validation
- [ ] Document architectural decisions e migration rationale
- [ ] Ensure no references to legacy patterns

### 🚨 GAP 3: Singer Target Data Loading Patterns
**Status**: ALTO - Oracle data loading patterns podem não be optimal
**Problema**:
- Bulk loading strategies não documented
- Oracle-specific loading optimizations podem be missing
- Error handling para data loading failures pode be incomplete

**TODO**:
- [ ] Implement Oracle bulk loading optimizations
- [ ] Add comprehensive error handling para loading failures
- [ ] Document data loading performance patterns
- [ ] Add data validation e quality checks

### 🚨 GAP 4: Oracle WMS Integration Opportunity
**Status**: MEDIUM - Oracle target pode leverage WMS capabilities
**Problema**:
- Oracle target não integrated com flext-oracle-wms capabilities
- WMS-specific loading patterns podem be beneficial
- Integration opportunities com WMS ecosystem podem be missed

**TODO**:
- [ ] Evaluate integration opportunities com flext-oracle-wms
- [ ] Document WMS-specific Oracle loading patterns
- [ ] Consider WMS data validation patterns
- [ ] Align com broader Oracle WMS ecosystem

### Design Patterns
- **Inherits from flext-meltano Target**: Uses established Singer patterns
- **FlextResult Pattern**: Railway-oriented programming for error handling
- **FlextValueObject**: Configuration with built-in validation
- **Clean Error Hierarchy**: Specific exceptions for different failure modes

## Development Commands

### Core Quality Gates (Zero Tolerance)
```bash
make validate           # Complete validation (lint + type + security + test)
make check             # Essential checks (lint + type + test)
make lint              # Ruff linting (ALL rules enabled)
make type-check        # MyPy strict mode type checking
make security          # Security scans (bandit + pip-audit + secrets)
make test              # Run tests with 90% coverage minimum
make format            # Format code with ruff
make fix               # Auto-fix all issues (format + lint)
```

### Testing Commands
```bash
make test              # All tests with 90% coverage requirement
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make test-singer       # Singer protocol tests
make coverage          # Generate detailed coverage report
make coverage-html     # Generate HTML coverage report
```

### Singer Target Operations
```bash
make singer-about            # Show Singer target information
make singer-config-sample    # Generate config sample
make target-test            # Test target functionality
make target-validate        # Validate configuration
make target-schema          # Validate Oracle schema
make target-run             # Run data loading
make target-run-debug       # Run with debug logging
make target-dry-run         # Run in dry-run mode
```

### Oracle-Specific Operations
```bash
make oracle-connect         # Test Oracle connection
make oracle-write-test      # Test write operations
make oracle-schema-check    # Check schema compatibility
make oracle-performance     # Run performance tests
make oracle-bulk-load       # Test bulk loading
make oracle-parallel-load   # Test parallel loading
make oracle-diagnostics     # Run diagnostics
```

### Development Setup
```bash
make setup              # Complete development setup
make install            # Install dependencies with Poetry  
make dev-install        # Install in development mode
make pre-commit         # Setup pre-commit hooks
make build              # Build distribution packages
make clean              # Remove all artifacts
```

### Dependency Management
```bash
make deps-update        # Update all dependencies
make deps-audit         # Audit for vulnerabilities
make deps-tree          # Show dependency tree
make deps-outdated      # Show outdated dependencies
```

## Configuration

### Core Configuration Class
The `FlextOracleTargetConfig` class extends `FlextValueObject` and provides:

```python
from flext_target_oracle import FlextOracleTargetConfig, LoadMethod

config = FlextOracleTargetConfig(
    oracle_host="localhost",
    oracle_port=1521,
    oracle_service="XE", 
    oracle_user="singer_user",
    oracle_password="password",
    default_target_schema="SINGER_DATA",
    load_method=LoadMethod.BULK_INSERT,
    batch_size=10000
)
```

### Environment Variables
Key environment variables for development and testing:
```bash
TARGET_ORACLE_HOST=localhost
TARGET_ORACLE_PORT=1521
TARGET_ORACLE_SERVICE_NAME=XE
TARGET_ORACLE_DEFAULT_TARGET_SCHEMA=FLEXT_DW
TARGET_ORACLE_POOL_SIZE=10
TARGET_ORACLE_PARALLEL_DEGREE=4
TARGET_ORACLE_ENABLE_COMPRESSION=true
```

## Testing Strategy

### Test Structure
```
tests/
├── unit/              # Unit tests (no external dependencies)
├── integration/       # Integration tests (with Oracle)
├── e2e/              # End-to-end tests
├── performance/       # Performance benchmarks
├── artifacts/         # Test configuration and data
│   ├── config.json   # Test Oracle configuration
│   └── oracle-init/  # Oracle schema setup scripts
└── conftest.py       # Pytest configuration
```

### Test Markers
```bash
pytest -m unit                    # Unit tests only
pytest -m integration            # Integration tests only
pytest -m "not slow"             # Exclude slow tests
pytest -m e2e                    # End-to-end tests
pytest -m performance            # Performance tests
```

### Coverage Requirements
- **Minimum 90% test coverage required**
- HTML coverage reports generated in `htmlcov/`
- Coverage enforcement in CI/CD pipeline

## Code Quality Standards

### Zero Tolerance Quality Gates
1. **Ruff Linting**: ALL rule categories enabled, comprehensive checks
2. **MyPy Type Checking**: Strict mode with zero errors tolerated
3. **Security Scanning**: bandit + pip-audit + detect-secrets
4. **Test Coverage**: 90% minimum coverage requirement
5. **Pre-commit Hooks**: Automated quality checks on every commit

### Python Requirements
- **Python 3.13+**: Required version for compatibility
- **Type Hints**: All code must include comprehensive type annotations
- **Pydantic Models**: Use for all configuration and data validation
- **FlextResult Pattern**: Use for all operations that can fail

## Integration Patterns

### FLEXT Ecosystem Integration
- **flext-core**: Use FlextResult, FlextValueObject, get_logger
- **flext-meltano**: Inherit from Target base class for Singer integration
- **flext-db-oracle**: Use for all Oracle database operations

### Singer Protocol Compliance
- Implements standard Singer target interface
- Handles SCHEMA, RECORD, and STATE messages
- Supports Singer configuration and discovery patterns
- Compatible with Meltano orchestration

### Oracle Integration
- **Connection Management**: Uses flext-db-oracle connection patterns
- **Batch Processing**: Configurable batch sizes for performance
- **Load Methods**: INSERT, MERGE, BULK_INSERT, BULK_MERGE options
- **Performance Options**: Compression, parallel degree, bulk operations

## Error Handling

### Exception Hierarchy
```python
FlextOracleTargetError                    # Base exception
├── FlextOracleTargetConnectionError      # Connection issues
├── FlextOracleTargetAuthenticationError  # Authentication failures
├── FlextOracleTargetSchemaError         # Schema-related errors
└── FlextOracleTargetProcessingError     # Data processing errors
```

### FlextResult Pattern
All operations return FlextResult for consistent error handling:
```python
result = await target.process_batch(records)
if result.is_failure:
    logger.error(f"Batch processing failed: {result.error}")
    return result
```

## Performance Considerations

### Oracle-Specific Optimizations
- **Bulk Operations**: Use Oracle bulk insert capabilities
- **Parallel Processing**: Configurable parallel degree
- **Connection Pooling**: Efficient connection management
- **Compression**: Optional Oracle compression support
- **Batch Sizing**: Tunable batch sizes for optimal throughput

### Monitoring and Observability
- Structured logging with correlation IDs
- Performance metrics and benchmarking
- Health check endpoints
- Integration with FLEXT observability stack

## Migration Notes

### Legacy Architecture
The project was migrated from a complex domain/application layer architecture to a simplified structure. Legacy code is preserved in `.bak` directories for reference:

- `domain.bak/`: Original domain models and entities
- `application.bak/`: Original service layer  
- `target.py.bak`: Original target implementation

### Key Changes in Migration
1. **Simplified Structure**: Removed complex layering
2. **Base Class Inheritance**: Now inherits from flext-meltano Target
3. **External Dependencies**: Uses flext-db-oracle for Oracle operations
4. **Standardized Configuration**: Uses FlextValueObject patterns
5. **Clean Public API**: Simplified interface for consumers

## Common Development Workflows

### Adding New Features
1. Follow existing patterns from flext-core and flext-meltano
2. Use FlextResult for error handling
3. Add comprehensive unit and integration tests
4. Update configuration if needed
5. Run full validation suite before committing

### Debugging Oracle Issues
1. Use `make oracle-diagnostics` for system checks
2. Test connection with `make oracle-connect`
3. Enable debug logging with `make target-run-debug`
4. Check Oracle schema compatibility with `make oracle-schema-check`

### Performance Testing
1. Run benchmarks with `make oracle-performance`
2. Test bulk operations with `make oracle-bulk-load`
3. Test parallel loading with `make oracle-parallel-load`
4. Profile using built-in pytest-benchmark integration

This Oracle target is designed to be a reliable, production-ready component in the FLEXT ecosystem while maintaining clean architecture and high code quality standards.