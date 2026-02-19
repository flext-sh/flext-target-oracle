# FLEXT Target Oracle - Test Suite

<!-- TOC START -->

- [📁 Test Structure](#-test-structure)
- [🚀 Running Tests](#-running-tests)
  - [Quick Start](#quick-start)
  - [Using the Test Script](#using-the-test-script)
- [🐳 Oracle Docker Management](#-oracle-docker-management)
  - [Manual Container Management](#manual-container-management)
- [🧪 Test Categories](#-test-categories)
  - [Unit Tests (`tests/unit/`)](#unit-tests-testsunit)
  - [Integration Tests (`tests/integration/`)](#integration-tests-testsintegration)
  - [End-to-End Tests (`tests/e2e/`)](#end-to-end-tests-testse2e)
- [📊 Test Configuration](#-test-configuration)
  - [Environment Variables](#environment-variables)
  - [Keeping Test Database](#keeping-test-database)
- [🔧 Key Fixtures](#-key-fixtures)
  - [Database Fixtures](#database-fixtures)
  - [Data Fixtures](#data-fixtures)
  - [Mock Fixtures](#mock-fixtures)
- [📈 Coverage Requirements](#-coverage-requirements)
- [🛠️ Development Workflow](#-development-workflow)
- [🐛 Debugging Tests](#-debugging-tests)
- [📝 Writing New Tests](#-writing-new-tests)
  - [Unit Test Example](#unit-test-example)
  - [Integration Test Example](#integration-test-example)
- [🎯 Best Practices](#-best-practices)
- [🚨 Troubleshooting](#-troubleshooting)
  - [Oracle Container Issues](#oracle-container-issues)
  - [Test Failures](#test-failures)
  - [Performance Issues](#performance-issues)

<!-- TOC END -->

This directory contains the comprehensive test suite for the FLEXT Oracle Target, organized following pytest best practices with automatic Oracle Docker container management.

## 📁 Test Structure

```
tests/
├── conftest.py          # Pytest configuration and shared fixtures
├── pytest.ini           # Pytest settings
├── README.md           # This file
├── unit/               # Unit tests (no database required)
├── integration/        # Integration tests (requires Oracle)
├── e2e/               # End-to-end tests
├── performance/       # Performance benchmarks
└── artifacts/         # Test outputs and reports
```

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests (automatically starts Oracle if needed)
make test

# Run only unit tests (no Docker required)
make test-unit

# Run integration tests
make test-integration

# Run with coverage
make coverage
```

### Using the Test Script

The `scripts/run_tests.sh` script provides fine-grained control:

```bash
# Run all tests
./scripts/run_tests.sh

# Run only unit tests
./scripts/run_tests.sh --unit

# Run integration tests with verbose output
./scripts/run_tests.sh --integration -v

# Keep Oracle container running after tests
./scripts/run_tests.sh --keep-db

# Run unit tests in parallel
./scripts/run_tests.sh --unit --parallel 4
```

## 🐳 Oracle Docker Management

Tests automatically manage an Oracle XE container using Docker Compose:

- **Automatic Start**: Container starts automatically when running integration/e2e tests
- **Health Checks**: Tests wait for Oracle to be fully ready
- **Test Schema**: Creates `FLEXT_TEST` schema with proper permissions
- **Cleanup**: Container stops after tests (unless `--keep-db` is used)

### Manual Container Management

```bash
# Start Oracle container
make oracle-start

# Stop Oracle container
make oracle-stop

# View Oracle logs
make oracle-logs

# Open SQL*Plus shell
make oracle-shell
```

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)

- No external dependencies
- Mock all database operations
- Fast execution
- Run with: `pytest -m unit`

### Integration Tests (`tests/integration/`)

- Require real Oracle database
- Test actual SQL execution
- Verify DDL/DML operations
- Run with: `pytest -m integration`

### End-to-End Tests (`tests/e2e/`)

- Complete Singer workflows
- Full data pipeline testing
- Performance validation
- Run with: `pytest -m e2e`

## 📊 Test Configuration

### Environment Variables

Tests use these environment variables (automatically set by fixtures):

```bash
FLEXT_TARGET_ORACLE_HOST=localhost
FLEXT_TARGET_ORACLE_PORT=1521
FLEXT_TARGET_ORACLE_SERVICE=XE
FLEXT_TARGET_ORACLE_USER=FLEXT_TEST
FLEXT_TARGET_ORACLE_PASSWORD=test_password
FLEXT_TARGET_ORACLE_DEFAULT_TARGET_SCHEMA=FLEXT_TEST
```

### Keeping Test Database

To keep the Oracle container running after tests:

```bash
# Using environment variable
KEEP_TEST_DB=true pytest

# Using make
make test-docker

# Using script
./scripts/run_tests.sh --keep-db
```

## 🔧 Key Fixtures

### Database Fixtures

- `oracle_container`: Session-scoped Oracle container lifecycle
- `oracle_engine`: SQLAlchemy engine for direct DB access
- `oracle_config`: Configured FlextOracleTargetSettings
- `oracle_loader`: Connected OracleLoader instance
- `clean_database`: Cleans all tables before each test

### Data Fixtures

- `simple_schema`: Basic Singer schema
- `nested_schema`: Complex nested schema
- `sample_record`: Single record
- `batch_records`: 100 records for bulk testing
- `singer_messages`: Complete message stream

### Mock Fixtures

- `mock_oracle_api`: Mocked FlextDbOracleApi
- `mock_loader`: Mocked OracleLoader

## 📈 Coverage Requirements

- Minimum coverage: 80%
- Coverage reports: HTML, JSON, and terminal
- View HTML report: `make coverage-html`

## 🛠️ Development Workflow

1. **Write tests first** (TDD approach)
1. **Run unit tests** during development: `make test-unit`
1. **Run integration tests** before commit: `make test-integration`
1. **Check coverage**: `make coverage`
1. **Run all tests** before push: `make test`

## 🐛 Debugging Tests

```bash
# Run with debugger on failure
pytest --pdb

# Run specific test with verbose output
pytest tests/unit/test_loader.py::TestOracleLoaderConnection::test_connect_success -vv

# Re-run only failed tests
pytest --lf

# Run tests in watch mode
make test-watch
```

## 📝 Writing New Tests

### Unit Test Example

```python
@pytest.mark.unit
class TestNewFeature:
    def test_feature_behavior(self, mock_oracle_api):
        """Test description."""
        # Arrange
        loader = OracleLoader(config)

        # Act
        result = loader.some_method()

        # Assert
        assert result.is_success
        mock_oracle_api.some_call.assert_called_once()
```

### Integration Test Example

```python
@pytest.mark.integration
@pytest.mark.oracle
def test_real_database_operation(oracle_loader, oracle_engine):
    """Test with real Oracle database."""
    # Create table
    oracle_loader.ensure_table_exists("test", schema, keys)

    # Insert data
    oracle_loader.insert_records("test", records)

    # Verify in database
    with oracle_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM test")).scalar()
        assert count == len(records)
```

## 🎯 Best Practices

1. **Isolation**: Each test should be independent
1. **Cleanup**: Use `clean_database` fixture for integration tests
1. **Mocking**: Mock external dependencies in unit tests
1. **Assertions**: Use specific assertions with clear messages
1. **Naming**: Descriptive test names that explain the scenario
1. **Markers**: Use appropriate pytest markers
1. **Performance**: Keep unit tests fast (< 1 second each)

## 🚨 Troubleshooting

### Oracle Container Issues

```bash
# Check container status
docker ps -a | grep flext-oracle

# View container logs
docker logs flext-oracle-test

# Restart container
make oracle-clean && make oracle-start
```

### Test Failures

1. Check Oracle container is running
1. Verify network connectivity
1. Check test database permissions
1. Review test logs in `reports/`

### Performance Issues

- Use `--keep-db` to avoid container restarts
- Run unit tests in parallel
- Use smaller datasets for integration tests
- Profile slow tests with `--durations=10`
