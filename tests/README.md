# Tests - FLEXT Target Oracle

## Test Structure

```
tests/
├── unit/               # Unit tests (mocked dependencies)
├── integration/        # Integration tests (real Oracle)
├── e2e/               # End-to-end tests (full pipeline)
├── test_config.py     # Configuration validation tests
├── test_target.py     # Singer Target implementation tests
├── test_loader.py     # Oracle data loading tests
├── test_exceptions.py # Exception hierarchy tests
└── conftest.py        # Pytest fixtures and configuration
```

## Running Tests

```bash
# All tests with coverage
make test

# Unit tests only (fast)
make test-unit
pytest -m "not integration"

# Integration tests (requires Oracle)
make test-integration
pytest -m integration

# Specific test file
pytest tests/test_config.py -v

# With debug output
pytest tests/test_loader.py -v -s
```

## Test Categories

- **Unit Tests**: Fast tests with mocked dependencies
- **Integration Tests**: Tests with real Oracle database
- **E2E Tests**: Full pipeline tests with Singer messages
- **Performance Tests**: Benchmarking and load testing

## Oracle Setup for Integration Tests

```bash
# Environment variables for Oracle connection
export FLEXT_TARGET_ORACLE_HOST=localhost
export FLEXT_TARGET_ORACLE_PORT=1521
export FLEXT_TARGET_ORACLE_SERVICE_NAME=XE
export FLEXT_TARGET_ORACLE_USERNAME=system
export FLEXT_TARGET_ORACLE_PASSWORD=oracle
```

## Current Coverage

- **Configuration**: 100% covered with comprehensive validation tests
- **Target Implementation**: Basic coverage with core functionality
- **Loader Operations**: Partial coverage, needs more integration tests
- **Exception Handling**: Basic exception creation tests

## Known Issues

- Some integration tests require actual Oracle database
- SQL injection vulnerability tests needed (security)
- Performance benchmarking tests incomplete
- E2E tests with real Singer ecosystem pending