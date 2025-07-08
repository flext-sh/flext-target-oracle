# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `flext-target-oracle`, a high-performance Singer target for Oracle Database built with the modern Singer SDK and optimized for enterprise workloads. The project uses SQLAlchemy 2.0, supports parallel processing, direct path loading, and Oracle-specific optimizations.

## Essential Development Commands

### Environment Setup
```bash
# Use workspace virtual environment
source /home/marlonsc/flext/.venv/bin/activate

# Install dependencies  
make install
# Or with dev dependencies
make install-dev
```

### Testing
```bash
# Unit tests (no database required)
make test-unit

# Integration tests (requires Oracle database)
make test-integration

# All tests
make test-all

# Specific test categories
make test-oracle      # Oracle-specific tests
make test-singer      # Singer protocol tests
make test-e2e         # End-to-end tests
```

### Code Quality
```bash
# Lint code with Ruff
make lint

# Format code
make format

# Type checking with MyPy
make type-check

# Security analysis
make security

# All quality checks
make check
```

### Development Workflow
```bash
# Quick development workflow
make quick           # Format + unit tests

# Full validation
make full           # All checks + all tests

# Development setup
make dev-setup      # Complete dev environment
```

### Database Operations
```bash
# Test Oracle connection
make db-test

# Run target with configuration
make target-run

# Validate configuration
make target-validate
```

## Architecture Overview

### Core Components

1. **OracleTarget** (`flext_target_oracle/target.py`) - Main Singer target class that orchestrates data loading
2. **OracleSink** (`flext_target_oracle/sinks.py`) - Handles data transformation and batch processing 
3. **OracleConnector** (`flext_target_oracle/connectors.py`) - Manages database connections and SQLAlchemy engine lifecycle

### Key Design Patterns

- **Factory Pattern**: Pool class selection based on configuration
- **Strategy Pattern**: Different load methods (append-only, upsert, overwrite)
- **Facade Pattern**: Legacy compatibility with delegation to flext-meltano SDK
- **Template Method**: Singer SDK base classes extended with Oracle specifics

### Enterprise Features

- **Performance**: Parallel processing, connection pooling, direct path loading, intelligent batching
- **Oracle-Specific**: MERGE operations for upserts, compression support, parallel DML
- **Reliability**: Transaction management, error categorization, schema evolution
- **Monitoring**: Built-in metrics, structured logging, performance profiling

## Configuration

### Required Environment
- Python 3.13 (specified in pyproject.toml)
- Oracle Database (any edition including Autonomous)
- Environment file `.env` with Oracle credentials

### Key Configuration Parameters
- `host`, `port`, `service_name` - Oracle connection
- `batch_config.batch_size` - Records per batch (default: 10000)
- `pool_size` - Connection pool size (default: 10)
- `load_method` - append-only, upsert, overwrite
- `use_bulk_operations` - Enable Oracle bulk operations
- `parallel_degree` - Oracle parallel processing

## Testing Strategy

### Test Organization
- **Unit Tests**: Fast tests with no external dependencies (`tests/test_basic_functionality.py`, `tests/test_env_validation.py`)
- **Integration Tests**: Require Oracle database connection (`tests/integration/`)
- **E2E Tests**: End-to-end scenarios (`tests/e2e/`)
- **Performance Tests**: Benchmarks and load testing (`tests/test_performance_benchmarks.py`)

### Test Markers
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.oracle` - Oracle-specific tests
- `@pytest.mark.singer` - Singer protocol tests
- `@pytest.mark.performance` - Performance benchmarks

### Running Specific Tests
```bash
# Unit tests only
pytest -m "unit"

# Integration tests only  
pytest -m "integration"

# Oracle-specific tests
pytest -m "oracle"

# Exclude slow tests
pytest -m "not slow"
```

## Legacy Compatibility

The project maintains backward compatibility through a facade pattern. The current implementation delegates to `flext-meltano` enterprise SDK for unified Singer target protocols while preserving the original API.

**Preferred Pattern**:
```python
from flext_meltano.singer_sdk_integration import FlextSingerSDKIntegration
```

**Legacy Compatibility**:
```python
from flext_target_oracle.target import OracleTarget
```

## Development Standards

### Code Quality
- **Ruff**: Maximum strictness linting with 160+ rules
- **MyPy**: Strict type checking enabled
- **Black**: Code formatting with 88-character line length
- **Bandit**: Security analysis for vulnerabilities
- **Coverage**: 95% minimum test coverage requirement

### SOLID Principles Applied
- **SRP**: Each component has single responsibility
- **OCP**: Extensible through configuration without core changes
- **LSP**: Inherits from Singer SDK maintaining expected behaviors
- **ISP**: Clean interfaces between components
- **DIP**: Depends on abstractions (Singer SDK, SQLAlchemy)

## Important Notes

- Uses workspace virtual environment at `/home/marlonsc/flext/.venv` (FLEXT workspace standard)
- Requires Oracle database for integration tests
- Supports Oracle Autonomous Database with wallet configuration
- Built for enterprise workloads with high-performance optimizations
- Follows Singer specification for data integration pipelines