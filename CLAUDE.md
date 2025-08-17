# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Target Oracle is a **production-grade Singer target for Oracle Database data loading**, built using FLEXT ecosystem patterns and enterprise-grade reliability standards. This Python 3.13+ library integrates with the broader FLEXT data platform ecosystem, providing clean Oracle integration using established patterns from `flext-core`, `flext-meltano`, and `flext-db-oracle`.

### Current Architecture

The project follows Clean Architecture with a consolidated module structure:

```
src/flext_target_oracle/
├── __init__.py              # Public API exports and re-exports
├── target.py                # CLI interface using flext-cli patterns
├── target_client.py         # Main Target implementation and Oracle loader
├── target_config.py         # Configuration with FlextValueObject patterns
├── target_exceptions.py     # Exception hierarchy
├── target_services.py       # Service layer protocols and implementations
├── target_models.py         # Pydantic data models
├── target_observability.py  # Observability and monitoring
└── constants.py             # System constants
```

### Key Dependencies & Integration

- **flext-core**: Base patterns (FlextResult, FlextBaseConfigModel, get_logger)
- **flext-meltano**: Singer SDK integration and Target base classes 
- **flext-db-oracle**: Oracle database operations and connectivity
- **flext-cli**: Modern CLI interface patterns
- **pydantic**: Configuration validation and type safety

## Development Commands

### Core Development Workflow

```bash
# Quick setup and validation
make dev-setup               # Complete development setup with dependencies
make validate               # Project validation (uses std-validate-setup)

# Testing commands (actual available targets)
make test                   # Run all tests with Oracle Docker
make test-unit              # Unit tests only (no Docker required)
make test-integration       # Integration tests with Oracle Docker
make coverage               # Run tests with coverage report
make coverage-html          # Generate and open HTML coverage report

# Using standardized build system (std- prefix)
make std-lint               # Ruff linting
make std-format             # Format code with ruff
make std-type-check         # MyPy type checking
make std-check              # Quick health check (lint + type)
make std-build              # Build package with Poetry
make std-install            # Install dependencies
make std-install-dev        # Install with dev dependencies
```

### Oracle Docker Management

```bash
# Oracle container lifecycle
make oracle-start           # Start Oracle Docker container
make oracle-stop            # Stop Oracle container
make oracle-clean           # Stop and remove container + volumes
make oracle-logs            # Show container logs
make oracle-shell           # Open SQL*Plus shell
make oracle-status          # Check container status
```

### Testing Patterns

The project uses a comprehensive test structure:

```
tests/
├── unit/              # Unit tests (no external dependencies)
├── integration/       # Integration tests (require Oracle)
├── e2e/              # End-to-end Singer workflow tests
├── performance/      # Performance benchmarks
└── conftest.py       # Pytest fixtures and configuration
```

**Test markers available:**
```bash
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m e2e               # End-to-end tests
pytest -m performance       # Performance tests
pytest -m "not slow"        # Exclude slow tests
```

### Running Single Tests

```bash
# Run specific test file
pytest tests/unit/test_config.py -v

# Run specific test method
pytest tests/unit/test_target.py::test_target_initialization -v

# Run with coverage for specific module
pytest tests/unit/test_config.py --cov=flext_target_oracle.target_config --cov-report=term-missing

# Debug mode
pytest tests/unit/test_config.py -x --pdb
```

## Architecture & Design Patterns

### FLEXT Integration Patterns

- **FlextResult Pattern**: Railway-oriented programming for error handling
- **FlextBaseConfigModel**: Type-safe configuration with validation
- **flext-cli**: Modern CLI interface with Click integration
- **Structured Logging**: flext-core logging with correlation IDs

### Core Classes

**FlextTargetOracle** (`target_client.py`):
- Main Singer Target implementation
- Handles SCHEMA, RECORD, and STATE messages
- Uses FlextTargetOracleLoader for data operations
- Built on flext-meltano Target base class

**FlextTargetOracleLoader** (`target_client.py`):
- Oracle data loading operations
- Uses flext-db-oracle for database connectivity
- Implements batch processing and connection management
- JSON storage strategy with CLOB fields

**FlextTargetOracleConfig** (`target_config.py`):
- Extends FlextBaseConfigModel from flext-core
- Pydantic validation with custom validators
- Converts to FlextDbOracleConfig for database operations

### Configuration Example

```python
from flext_target_oracle import FlextTargetOracleConfig, LoadMethod

config = FlextTargetOracleConfig(
    oracle_host="localhost",
    oracle_port=1521,
    oracle_service="XE", 
    oracle_user="singer_user",
    oracle_password="password",
    default_target_schema="SINGER_DATA",
    load_method=LoadMethod.INSERT,
    batch_size=1000,
    use_bulk_operations=True
)
```

### Load Methods Available

```python
from flext_target_oracle import LoadMethod

LoadMethod.INSERT       # Standard INSERT statements
LoadMethod.MERGE        # MERGE/UPSERT operations  
LoadMethod.BULK_INSERT  # Bulk INSERT operations
LoadMethod.BULK_MERGE   # Bulk MERGE operations
```

## Quality Standards

### Type Safety & Linting

- **Python 3.13+** required
- **MyPy strict mode** with comprehensive type hints
- **Ruff** for linting with all rule categories enabled
- **Pydantic** for all configuration and data validation

### Coverage & Testing

- **90% minimum test coverage** required for production
- **Unit, integration, e2e, and performance** test categories
- **Pytest** with async support and comprehensive fixtures
- **Oracle Docker** integration for realistic testing

### Pre-commit Quality Gates

The project enforces quality through make targets:
```bash
make std-check          # Quick validation (lint + type)
make validate           # Full project validation
make test               # Tests with coverage requirements
```

## Environment Variables

Key environment variables for testing:

```bash
# Oracle connection (used by pytest fixtures)
FLEXT_TARGET_ORACLE_HOST=localhost
FLEXT_TARGET_ORACLE_PORT=1521
FLEXT_TARGET_ORACLE_USERNAME=system
FLEXT_TARGET_ORACLE_PASSWORD=Oracle123
FLEXT_TARGET_ORACLE_SERVICE_NAME=XE
FLEXT_TARGET_ORACLE_DEFAULT_TARGET_SCHEMA=FLEXT_TEST
```

## Singer Protocol Integration

### Message Processing

```python
# Example Singer message handling
schema_msg = {
    "type": "SCHEMA",
    "stream": "users", 
    "schema": {"type": "object", "properties": {"id": {"type": "integer"}}}
}

record_msg = {
    "type": "RECORD",
    "stream": "users",
    "record": {"id": 1, "name": "John"}
}

# Process using FlextResult pattern
result = await target.process_singer_message(schema_msg)
if result.is_failure:
    logger.error(f"Processing failed: {result.error}")
```

### CLI Interface

The target provides both programmatic and CLI interfaces:

```bash
# CLI usage (via target.py)
flext-target-oracle --config config.json < input.jsonl

# Validation and introspection
flext-target-oracle --about
flext-target-oracle --config config.json --discover
```

## Common Development Tasks

### Adding New Features

1. Follow FLEXT patterns using FlextResult and FlextBaseConfigModel
2. Add comprehensive type hints (MyPy strict mode)
3. Create unit tests with 90%+ coverage
4. Update configuration models if needed
5. Run `make validate` before committing

### Debugging Oracle Issues

```bash
# Check Oracle container status
make oracle-status

# View Oracle logs
make oracle-logs

# Access Oracle directly  
make oracle-shell

# Test connection programmatically
python -c "
from flext_target_oracle import FlextTargetOracleConfig
from flext_db_oracle import FlextDbOracleApi
config = FlextTargetOracleConfig(oracle_host='localhost', oracle_service='XE', oracle_user='system', oracle_password='Oracle123')
with FlextDbOracleApi(config.to_db_config()) as api:
    print('Connection successful!')
"
```

### Performance Testing

```bash
# Run performance benchmarks
make benchmark

# Performance tests with specific markers
pytest tests/performance/ -v --benchmark-only
```

This Oracle target is designed as a core component of the FLEXT ecosystem, emphasizing clean architecture, type safety, and production-grade reliability standards.