# Development Guide

**FLEXT Target Oracle - Developer Documentation**

## Quick Start

### Prerequisites

- **Python 3.13+**: Required for compatibility with FLEXT ecosystem
- **Poetry**: Dependency management and packaging
- **Oracle Database**: 11g+ for testing (Docker container recommended)
- **Git**: Version control

### Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd flext-target-oracle

# Complete development setup
make setup                    # Installs dependencies + pre-commit hooks
make validate                 # Verify setup with full quality gates

# Alternative: Manual setup
poetry install --with dev,test,docs
poetry run pre-commit install
```

### Verify Installation

```bash
# Run basic health checks
make check                    # Lint + type check
make test-unit               # Unit tests only (no Oracle required)
make diagnose                # System diagnostics

# Expected output:
# ✅ All quality gates pass
# ✅ All unit tests pass
# ✅ Python 3.13+, Poetry detected
```

## Development Workflow

### Daily Development Commands

```bash
# Essential quality gates (run before every commit)
make validate                 # Complete validation pipeline
make check                   # Quick validation (lint + type)
make test                    # Full test suite with coverage

# Code maintenance
make format                  # Auto-format with ruff
make fix                     # Auto-fix linting issues
make clean                   # Remove build artifacts

# Development utilities
make shell                   # Open Python shell with project context
make deps-show              # Show dependency tree
make diagnose               # Project health check
```

### Testing Workflow

#### Unit Testing (No External Dependencies)

```bash
# Run unit tests only
make test-unit

# Run specific test file
pytest tests/test_config.py -v

# Run specific test method
pytest tests/test_target.py::test_target_initialization -v

# Run with coverage for specific module
pytest tests/test_config.py --cov=src/flext_target_oracle/config --cov-report=term-missing
```

#### Integration Testing (Requires Oracle)

```bash
# Setup Oracle test container (one-time)
docker run -d --name oracle-test \
  -p 10521:1521 \
  -e ORACLE_PWD=oracle \
  gvenzl/oracle-xe:latest

# Wait for Oracle to be ready (2-3 minutes)
docker logs -f oracle-test

# Run integration tests
make test-integration

# Or run specific integration tests
pytest tests/integration/ -v -m integration
```

#### Performance Testing

```bash
# Run performance benchmarks
make oracle-performance

# Run specific benchmark
pytest tests/performance/ --benchmark-only --benchmark-sort=mean

# Test different batch sizes
BATCH_SIZE=1000 pytest tests/performance/test_batch_performance.py
BATCH_SIZE=5000 pytest tests/performance/test_batch_performance.py
```

### Code Quality Standards

#### Zero Tolerance Quality Gates

All code must pass these checks before commit:

```bash
# Linting (ALL Ruff rules enabled)
make lint                    # Must pass with zero warnings

# Type checking (Strict MyPy mode)
make type-check             # Must pass with zero errors

# Security scanning
make security               # Bandit + pip-audit must pass

# Test coverage
make test                   # Must maintain 90%+ coverage
```

#### Code Style Guidelines

```python
# ✅ GOOD: FLEXT patterns
from flext_core import FlextResult, FlextValueObject, get_logger

def operation() -> FlextResult[Data]:
    """Clear docstring with FlextResult return type."""
    try:
        # Business logic here
        return FlextResult.ok(data)
    except Exception as e:
        logger.exception("Operation failed")
        return FlextResult.fail(f"Operation failed: {e}")

# ✅ GOOD: Configuration with validation
class Config(FlextValueObject):
    field: str = Field(..., description="Required field")

    @field_validator("field")
    @classmethod
    def validate_field(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v

# ❌ AVOID: Exceptions without context
def bad_operation():
    raise Exception("Something went wrong")  # No context!

# ❌ AVOID: Unvalidated configuration
class BadConfig:
    def __init__(self, field):
        self.field = field  # No validation!
```

## FLEXT Pattern Implementation

### FlextResult Railway Pattern

```python
# ✅ All operations return FlextResult
async def process_record(record: dict) -> FlextResult[None]:
    """Process a single record with proper error handling."""
    try:
        # Validate input
        if not record:
            return FlextResult.fail("Record cannot be empty")

        # Process record
        result = await some_operation(record)
        if result.is_failure:
            return result  # Propagate failure

        return FlextResult.ok(None)

    except Exception as e:
        logger.exception("Record processing failed")
        return FlextResult.fail(f"Processing failed: {e}")

# ✅ Chain FlextResult operations
async def process_batch(records: list[dict]) -> FlextResult[Stats]:
    """Process batch of records with early termination on failure."""
    stats = Stats()

    for record in records:
        result = await process_record(record)
        if result.is_failure:
            return FlextResult.fail(f"Batch failed on record: {result.error}")

        stats.increment()

    return FlextResult.ok(stats)
```

### Configuration Patterns

```python
# ✅ FlextValueObject with domain validation
class FlextOracleTargetConfig(FlextValueObject):
    """Type-safe configuration with business rule validation."""

    # Required fields with clear validation
    oracle_host: str = Field(..., description="Oracle host")
    oracle_port: int = Field(
        default=1521,
        ge=1,
        le=65535,
        description="Oracle port"
    )

    # Custom validation
    @field_validator("oracle_host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        if not v or v.isspace():
            raise ValueError("Oracle host is required")
        return v.strip()

    # Domain rule validation
    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate business rules using Chain of Responsibility."""
        validator = ConfigurationValidator()
        return validator.validate(self)
```

### Logging Patterns

```python
# ✅ Structured logging with context
from flext_core import get_logger

logger = get_logger(__name__)

def process_with_logging(stream_name: str, batch_size: int):
    """Example of proper logging with context."""

    # Structured logging with extra context
    logger.info(
        "Starting batch processing",
        extra={
            "stream_name": stream_name,
            "batch_size": batch_size,
            "operation": "batch_processing"
        }
    )

    try:
        # Process batch
        result = process_batch()

        logger.info(
            "Batch processing completed",
            extra={
                "stream_name": stream_name,
                "records_processed": result.count,
                "duration_ms": result.duration
            }
        )

    except Exception as e:
        logger.exception(
            "Batch processing failed",
            extra={
                "stream_name": stream_name,
                "error_type": type(e).__name__
            }
        )
        raise
```

## Oracle Integration Development

### Database Connection Testing

```python # Test Oracle connectivity manually
from flext_target_oracle import FlextOracleTargetConfig
from flext_target_oracle.loader import FlextOracleTargetLoader

# Create test configuration
config = FlextOracleTargetConfig(
    oracle_host="localhost",
    oracle_port=10521,
    oracle_service="XE",
    oracle_user="system",
    oracle_password="oracle",
    default_target_schema="TEST_SCHEMA"
)

# Test connection
loader = FlextOracleTargetLoader(config)

# Verify with context manager
with loader.oracle_api as connected_api:
    tables_result = connected_api.get_tables("TEST_SCHEMA")
    if tables_result.success:
        print(f"Connected! Found {len(tables_result.data)} tables")
    else:
        print(f"Connection failed: {tables_result.error}")
```

### Table Management Development

```python
# Test table creation and schema evolution
async def test_table_management():
    """Test table operations during development."""

    # Schema definition
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }

    # Ensure table exists
    result = await loader.ensure_table_exists("test_stream", schema)
    if result.is_failure:
        print(f"Table creation failed: {result.error}")
        return

    # Test record insertion
    test_record = {
        "id": 1,
        "name": "Test Record",
        "created_at": "2025-08-04T10:00:00Z"
    }

    result = await loader.load_record("test_stream", test_record)
    if result.success:
        print("Record loaded successfully")
    else:
        print(f"Record loading failed: {result.error}")
```

## Debugging and Troubleshooting

### Common Development Issues

#### 1. Oracle Connection Issues

```bash
# Check Oracle container status
docker ps | grep oracle
docker logs oracle-test

# Test connectivity
make oracle-connect

# Debug with Python
PYTHONPATH=src python -c "
from flext_target_oracle import FlextOracleTargetConfig
from flext_target_oracle.loader import FlextOracleTargetLoader
import logging
logging.basicConfig(level=logging.DEBUG)
config = FlextOracleTargetConfig(
    oracle_host='localhost',
    oracle_port=10521,
    oracle_service='XE',
    oracle_user='system',
    oracle_password='oracle'
)
loader = FlextOracleTargetLoader(config)
print('Config created successfully')
"
```

#### 2. Import Errors

```python
# ❌ Common import issue
from flext_target_oracle import something_that_doesnt_exist

# ✅ Check available imports
from flext_target_oracle import (
    FlextOracleTarget,
    FlextOracleTargetConfig,
    LoadMethod,
    FlextResult  # Re-exported from flext-core
)

# ✅ Debug imports
python -c "from flext_target_oracle import *; print(dir())"
```

#### 3. Configuration Validation Errors

```python
# ❌ Invalid configuration
config = FlextOracleTargetConfig(
    oracle_host="",  # Empty host will fail validation
    oracle_port=70000,  # Port too high
    batch_size=-1  # Negative batch size
)

# ✅ Valid configuration with proper validation
try:
    config = FlextOracleTargetConfig(
        oracle_host="localhost",
        oracle_port=1521,
        oracle_service="XE",
        oracle_user="system",
        oracle_password="oracle"
    )

    # Test domain rules
    validation_result = config.validate_domain_rules()
    if validation_result.is_failure:
        print(f"Validation failed: {validation_result.error}")

except ValidationError as e:
    print(f"Configuration error: {e}")
```

### Debugging Tools

#### 1. Enhanced Logging

```python
# Enable debug logging for development
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# FLEXT modules will automatically use debug logging
```

#### 2. Interactive Development

```bash
# Open Python shell with project context
make shell

# In shell:
>>> from flext_target_oracle import *
>>> config = FlextOracleTargetConfig(...)
>>> # Interactive testing
```

#### 3. Performance Profiling

```python
# Profile batch processing performance
import cProfile
import pstats

def profile_batch_processing():
    """Profile batch processing for performance optimization."""

    pr = cProfile.Profile()
    pr.enable()

    # Your batch processing code here
    result = process_large_batch(records)

    pr.disable()

    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions by time
```

## Testing Development

### Writing New Tests

#### Unit Test Template

```python
"""Test template for new functionality."""
import pytest
from flext_target_oracle import FlextOracleTargetConfig, FlextResult

class TestNewFeature:
    """Test suite for new feature."""

    def test_success_case(self):
        """Test successful operation."""
        # Arrange
        config = FlextOracleTargetConfig(...)

        # Act
        result = new_feature_operation(config)

        # Assert
        assert result.success
        assert result.data == expected_value

    def test_failure_case(self):
        """Test failure handling."""
        # Arrange
        invalid_config = FlextOracleTargetConfig(...)

        # Act
        result = new_feature_operation(invalid_config)

        # Assert
        assert result.is_failure
        assert "expected error message" in result.error

    @pytest.mark.parametrize("input_value,expected", [
        ("valid_input", "expected_output"),
        ("another_input", "another_output"),
    ])
    def test_parametrized(self, input_value, expected):
        """Test multiple input scenarios."""
        result = operation(input_value)
        assert result == expected
```

#### Integration Test Template

```python
"""Integration test template."""
import pytest
from flext_target_oracle import FlextOracleTarget

@pytest.mark.integration
class TestOracleIntegration:
    """Integration tests requiring Oracle database."""

    @pytest.fixture
    def oracle_target(self, sample_config):
        """Create target with Oracle connection."""
        return FlextOracleTarget(sample_config)

    async def test_end_to_end_processing(self, oracle_target):
        """Test complete Singer message processing."""
        # Schema message
        schema_msg = {...}
        result = await oracle_target.process_singer_message(schema_msg)
        assert result.success

        # Record messages
        record_msg = {...}
        result = await oracle_target.process_singer_message(record_msg)
        assert result.success

        # Finalization
        stats_result = await oracle_target.finalize()
        assert stats_result.success
        assert stats_result.data["total_records"] > 0
```

### Test Data Management

```python
# Test fixtures for consistent test data
@pytest.fixture
def sample_schema():
    """Standard test schema."""
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        }
    }

@pytest.fixture
def sample_records():
    """Standard test records."""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    ]
```

## Performance Development

### Batch Size Optimization

```python
# Test different batch sizes for optimal performance
import time
from typing import List

async def benchmark_batch_sizes(records: List[dict]):
    """Benchmark different batch sizes."""

    batch_sizes = [100, 500, 1000, 2000, 5000]
    results = {}

    for batch_size in batch_sizes:
        config = FlextOracleTargetConfig(
            # ... other config
            batch_size=batch_size
        )

        target = FlextOracleTarget(config)

        start_time = time.time()

        # Process all records
        for record in records:
            await target.process_singer_message({
                "type": "RECORD",
                "stream": "test_stream",
                "record": record
            })

        await target.finalize()

        duration = time.time() - start_time
        results[batch_size] = {
            "duration": duration,
            "records_per_second": len(records) / duration
        }

    # Print results
    for batch_size, stats in results.items():
        print(f"Batch size {batch_size}: "
              f"{stats['records_per_second']:.1f} records/sec")
```

### Memory Usage Monitoring

```python
import psutil
import os

def monitor_memory_usage():
    """Monitor memory usage during processing."""

    process = psutil.Process(os.getpid())

    def get_memory_mb():
        return process.memory_info().rss / 1024 / 1024

    print(f"Initial memory: {get_memory_mb():.1f} MB")

    # Your processing code here
    # ...

    print(f"Final memory: {get_memory_mb():.1f} MB")
```

## Contributing Guidelines

### Pull Request Checklist

Before submitting a pull request:

- [ ] **Code Quality**: `make validate` passes with zero issues
- [ ] **Tests**: All existing tests pass, new tests added for new functionality
- [ ] **Documentation**: Updated relevant documentation (architecture, API)
- [ ] **Security**: No new security vulnerabilities introduced
- [ ] **FLEXT Patterns**: Follows established FLEXT ecosystem patterns
- [ ] **Backward Compatibility**: No breaking changes without major version bump

### Commit Message Format

```
type(scope): brief description

Detailed explanation of changes made, why they were necessary,
and any breaking changes introduced.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`

### Review Process

1. **Automated Checks**: CI/CD pipeline runs quality gates
2. **Architecture Review**: Ensure FLEXT pattern compliance
3. **Security Review**: Check for vulnerabilities
4. **Performance Review**: Validate no performance regressions
5. **Documentation Review**: Ensure documentation is updated

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-04  
**Next Review**: 2025-08-11
