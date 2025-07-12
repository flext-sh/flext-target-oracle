# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `flext-target-oracle`, a high-performance Singer target for Oracle Database built with the modern Singer SDK and optimized for enterprise workloads. The project uses SQLAlchemy 2.0, supports parallel processing, direct path loading, and Oracle-specific optimizations.

## Essential Development Commands

### Environment Setup

```bash
# Use workspace virtual environment (required by FLEXT standards)
source /home/marlonsc/flext/.venv/bin/activate

# Install dependencies
make install          # Runtime dependencies only
make install-dev      # All development dependencies
make setup           # Complete development setup
```

### Testing

```bash
# Unit tests (no database required)
make test-unit
pytest -m unit

# Integration tests (requires Oracle database)
make test-integration
pytest -m integration

# All tests
make test-all

# Specific test categories
make test-oracle      # Oracle-specific tests
make test-singer      # Singer protocol tests
make test-e2e         # End-to-end tests
make test-performance # Performance benchmarks

# Run specific test files or functions
pytest tests/test_oracle_connection.py -v
pytest tests/test_target_functionality.py::test_specific_function -v

# Skip slow tests
pytest -m "not slow"
```

### Code Quality

```bash
# Format code
make format
make fix

# Lint code with Ruff (160+ rules)
make lint

# Type checking with MyPy
make type-check

# Security analysis
make security

# All quality checks (must pass 100%)
make check
make quality-gate
```

### Development Workflow

```bash
# Quick development cycle
make quick           # Format + unit tests
make dev-test        # Quick test validation

# Full validation
make full            # All checks + all tests
make workflow        # Complete development workflow

# CI pipeline locally
make ci             # Run full CI pipeline
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

1. **OracleTarget** (`target.py`) - Main Singer target class orchestrating data loading
2. **OracleSink** (`sinks.py`) - Handles data transformation, batching, and Oracle-specific operations
3. **OracleConnector** (`connectors.py`) - Manages database connections and SQLAlchemy engine lifecycle
4. **OracleConfig** (`config.py`) - Configuration management with flat and nested format support

### Domain-Driven Structure

```
src/flext_target_oracle/
├── application/         # Application services layer
│   └── services/       # Business logic services
├── domain/             # Domain models and entities
│   ├── models/        # Domain models
│   └── repositories/  # Repository interfaces
├── cli.py             # CLI interface
├── config.py          # Configuration management
├── connectors.py      # Database connectivity
├── sinks.py           # Data processing
└── target.py          # Main target class
```

### Key Design Patterns

- **Factory Pattern**: Dynamic pool class selection based on configuration
- **Strategy Pattern**: Different load methods (append-only, upsert, overwrite)
- **Facade Pattern**: Legacy compatibility with delegation to flext-meltano SDK
- **Template Method**: Singer SDK base classes extended with Oracle specifics
- **Observer Pattern**: SQLAlchemy event system for lifecycle management

### Enterprise Features

- **Performance**: Parallel processing, connection pooling, direct path loading, intelligent batching
- **Oracle-Specific**: MERGE operations for upserts, compression support, parallel DML, partitioning
- **Reliability**: Transaction management, error categorization, schema evolution, retry logic
- **Monitoring**: Built-in metrics, structured logging, performance profiling, observability integration

## Configuration

### Required Environment

- Python 3.13 (FLEXT enterprise standard)
- Oracle Database (any edition including Autonomous)
- Environment file `.env` with Oracle credentials

### Key Configuration Parameters

```python
# Connection settings
host, port, service_name     # Oracle connection details
protocol                      # tcp or tcps (SSL)
wallet_location              # For Oracle Autonomous Database

# Performance settings
batch_config.batch_size      # Records per batch (default: 10000)
pool_size                    # Connection pool size (default: 10)
parallel_degree              # Oracle parallel processing
use_bulk_operations          # Enable Oracle bulk operations

# Load behavior
load_method                  # append-only, upsert, overwrite
primary_keys                 # Keys for upsert operations
```

### Environment Variables

```bash
# Required Oracle connection
DATABASE__HOST=localhost
DATABASE__PORT=1521
DATABASE__SERVICE_NAME=XEPDB1
DATABASE__USERNAME=system
DATABASE__PASSWORD=oracle

# Optional Oracle features
ORACLE_IS_ENTERPRISE_EDITION=false
ORACLE_HAS_PARTITIONING_OPTION=false
ORACLE_HAS_COMPRESSION_OPTION=false
```

## Testing Strategy

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── helpers.py               # Test utilities and mock data generators
├── test_*.py               # Test modules organized by functionality
├── unit/                   # Pure unit tests (no external dependencies)
├── integration/            # Integration tests (require Oracle)
├── e2e/                   # End-to-end scenario tests
└── README.md              # Test documentation
```

### Test Markers

- `@pytest.mark.unit` - Unit tests with no external dependencies
- `@pytest.mark.integration` - Integration tests requiring Oracle
- `@pytest.mark.oracle` - Oracle-specific feature tests
- `@pytest.mark.singer` - Singer protocol compliance tests
- `@pytest.mark.performance` - Performance benchmarks
- `@pytest.mark.slow` - Long-running tests (excluded by default)
- `@pytest.mark.e2e` - End-to-end workflow tests

### Key Test Files

- `test_oracle_connection.py` - Connection establishment, TCPS/SSL, Autonomous DB
- `test_target_functionality.py` - Core Singer target functionality
- `test_oracle_features.py` - Oracle-specific features (MERGE, bulk operations)
- `test_performance_benchmarks.py` - Throughput and scalability tests
- `test_sqlalchemy2_features.py` - SQLAlchemy 2.0 specific features
- `test_error_handling.py` - Error recovery and retry logic

## Legacy Compatibility

The project maintains backward compatibility through a facade pattern. The current implementation delegates to `flext-meltano` enterprise SDK for unified Singer target protocols while preserving the original API.

**Preferred Pattern** (uses enterprise SDK):

```python
from flext_meltano.singer_sdk_integration import FlextSingerSDKIntegration
```

**Legacy Compatibility** (for existing integrations):

```python
from flext_target_oracle.target import OracleTarget
```

## Development Standards

### Code Quality Gates

- **Ruff**: Maximum strictness with ALL rules enabled (160+ rules)
- **MyPy**: Strict type checking with no implicit Any
- **Black**: Code formatting with 88-character line length
- **Bandit**: Security vulnerability scanning
- **Coverage**: 90% minimum test coverage requirement
- **Pre-commit**: Automated checks before commits

### SOLID Principles Applied

- **SRP**: Each component has single, well-defined responsibility
- **OCP**: Extensible through configuration without modifying core
- **LSP**: Maintains Singer SDK contracts in all extensions
- **ISP**: Clean, minimal interfaces between components
- **DIP**: Depends on abstractions (Singer SDK, SQLAlchemy interfaces)

### CI/CD Pipeline

- Multi-OS testing (Ubuntu, Windows, macOS)
- Security scanning with Trivy and Semgrep
- Automated semantic versioning
- Coverage reporting with Codecov
- Documentation validation
- Package publishing to PyPI

## Important Notes

- Uses workspace virtual environment at `/home/marlonsc/flext/.venv` (FLEXT workspace standard)
- Requires Oracle database for integration tests (Docker Compose provided)
- Supports Oracle Autonomous Database with wallet configuration
- Built for enterprise workloads with high-performance optimizations
- Follows Singer specification for data integration pipelines
- Integrates with FLEXT observability for monitoring and metrics
