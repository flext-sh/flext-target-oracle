# Development Guide

<!-- TOC START -->

- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Verify Installation](#verify-installation)
- [Development Workflow](#development-workflow)
  - [Daily Development Commands](#daily-development-commands)
  - [Testing Workflow](#testing-workflow)
  - [Code Quality Standards](#code-quality-standards)

<!-- TOC END -->

**FLEXT Target Oracle - Developer Documentation**

## Quick Start

Run from the active workspace/worktree root. For a standalone checkout, this is
the repository root. In a physical FLEXT workspace, stay at the workspace root;
use `ALL=Y` with test verbs when the run must include every governed member.

The package root exports `FlextTargetOracleSettings` and the `target_oracle`
facade. The loader examples later in this guide concern the implementation
layer in `application/loader.py`; that class is not a package-root export.

### Prerequisites

- **Python 3.13+**: Required for compatibility with FLEXT ecosystem
- **Oracle Database**: 11g+ for testing (Docker container recommended)
- **Git**: Version control

### Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd flext-target-oracle  # Standalone checkout; use the workspace root for a member

# Complete development setup
make setup                    # Installs dependencies + pre-commit hooks
make check CHECK_PHASE=complete  # Verify setup with complete quality gates
```

### Verify Installation

```bash
# Run basic health checks
make check CHECK_PHASE=complete  # Complete configured validation
make tests                      # Native incremental Testmon selection

# Expected output:
# ✅ All quality gates pass
# ✅ Selected tests pass
# ✅ Python 3.13+
```

## Development Workflow

### Daily Development Commands

```bash
# Essential quality gates (run before every commit)
# Generation, repair, formatting, and complete validation
make check CHECK_PHASE=complete
make clean               # Remove build artifacts
```

### Testing Workflow

#### Test Suite

```bash
# Native incremental selection through the persistent Testmon cache
make tests
```

Use a separate complete-inventory run when explicit qualification requires every
selected test, including the configuration and target cases:

```bash
make tests-full
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

# For explicit integration qualification after Oracle prerequisites are available
make tests-full
```

#### Performance Testing

```bash
# For explicit performance qualification through the complete native inventory
make tests-full
```

### Code Quality Standards

#### Zero Tolerance Quality Gates

All code must pass these checks before commit:

```bash
# Lint, typing, security, documentation, and the configured complete gates
make check CHECK_PHASE=complete

# Native incremental behavioral validation through the persistent Testmon cache
make tests
```

#### Code Style Guidelines

```python
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

# ✅ GOOD: FLEXT patterns
from flext_cli import u


def operation() -> p.Result[Data]:
    """Clear docstring with r return type."""
    try:
        # Business logic here
        return r[bool].ok(data)
    except Exception as e:
        logger.exception("Operation failed")
        return r[bool].fail(f"Operation failed: {e}")


# ✅ GOOD: Configuration with validation
class Config(m.Value):
    field: str = u.Field(..., description="Required field")

    @m.field_validator("field")
    @classmethod
    def validate_field(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("u.Field cannot be empty")
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

### r Railway Pattern

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_core import m, p, r


# ✅ All operations return r[T]
def process_record(record: dict) -> p.Result[bool]:
    """Process a single record with proper error handling."""
    if not record:
        return r[bool].fail("Record cannot be empty")

    result = some_operation(record)
    if result.failure:
        return result  # Propagate failure

    return r[bool].ok(value=True)


# ✅ Chain r[T] operations
def process_batch(records: list[p.Dict]) -> p.Result[bool]:
    """Process batch of records with early termination on failure."""
    for record in records:
        result = process_record(record)
        if result.failure:
            return r[bool].fail(f"Batch failed on record: {result.error}")

    return r[bool].ok(value=True)
```
### Configuration Patterns

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_core import m, p, u


# ✅ m.Value with domain validation
class FlextTargetOracleSettings(m.Value):
    """Type-safe configuration with business rule validation."""

    # Required fields with clear validation
    oracle_host: str = u.Field(..., description="Oracle host")
    oracle_port: int = u.Field(default=1521, ge=1, le=65535, description="Oracle port")

    # Custom validation
    @m.field_validator("oracle_host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        if not v or v.isspace():
            raise ValueError("Oracle host is required")
        return v.strip()

    # Domain rule validation
    def validate_domain_rules(self) -> p.Result[bool]:
        """Validate business rules using a validator."""
        validator = ConfigurationValidator()
        return validator.validate(self)
```
### Logging Patterns

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import logging

logger = logging.getLogger(__name__)


def process_with_logging(stream_name: str, batch_size: int):
    """Example of proper logging with context."""
    # Structured logging with extra context
    logger.info(
        "Starting batch processing",
        extra={
            "stream_name": stream_name,
            "batch_size": batch_size,
            c.ContextScope.OPERATION: "batch_processing",
        },
    )

    try:
        # Process batch
        result = process_batch()

        logger.info(
            "Batch processing completed",
            extra={
                "stream_name": stream_name,
                "records_processed": result.count,
                "duration_ms": result.duration,
            },
        )

    except Exception as e:
        logger.exception(
            "Batch processing failed",
            extra={"stream_name": stream_name, "error_type": type(e).__name__},
        )
        raise
```
## Oracle Integration Development

### Database Connection Testing

```text
# Test Oracle connectivity manually
from flext_core import u
from flext_target_oracle.application.loader import FlextTargetOracleLoader

# Create test configuration
loader = FlextTargetOracleLoader(...)

# Verify connection
result = loader.test_connection()
if result.success:
    u.Cli.print("Connected successfully")
else:
    u.Cli.print(f"Connection failed: {result.error}")
```
### Table Management Development

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)


# Test table creation and schema evolution
def test_table_management():
    """Test table operations during development."""
    # Schema definition
    schema = {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
    }

    # Ensure table exists
    result = loader.ensure_table_exists("test_stream", schema)
    if result.failure:
        u.Cli.print(f"Table creation failed: {result.error}")
        return

    # Test record insertion
    test_record = {"id": 1, "name": "Test Record"}

    result = loader.load_record("test_stream", test_record)
    if result.success:
        u.Cli.print("Record loaded successfully")
    else:
        u.Cli.print(f"Record loading failed: {result.error}")
```
## Debugging and Troubleshooting

### Common Development Issues

#### 1. Oracle Connection Issues

```bash
# Check Oracle container status
docker ps -a --filter oracle
docker logs oracle-test

# Verify the installed public facade in the provisioned environment
python -c "from flext_target_oracle import target_oracle; assert target_oracle.target_name == 'target-oracle'"
```
#### 2. Import Errors

```text
# ❌ Common import issue

# ✅ Check available imports
```

```bash
# ✅ Debug imports
python -c "from flext_target_oracle import FlextTargetOracleSettings, target_oracle"
```
#### 3. Configuration Validation Errors

```text
# ❌ Invalid configuration
try:
    loader = FlextTargetOracleLoader(...)  # Invalid config will raise
except Exception as e:
    u.Cli.print(f"Configuration error: {e}")

# ✅ Valid configuration
loader = FlextTargetOracleLoader(...)

# Test connection
result = loader.test_connection()
if result.failure:
    u.Cli.print(f"Validation failed: {result.error}")
```
### Debugging Tools

#### 1. Enhanced Logging

```text
# Enable debug logging for development
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FLEXT modules will automatically use debug logging
```
#### 2. Interactive Development

```bash
# Open Python shell with project context
python -m flext_core.tools.cli

# In shell:
>>> from flext_target_oracle import *
>>> # Interactive testing
```
#### 3. Performance Profiling

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

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
    stats.sort_stats("cumulative")
    stats.print_stats(20)  # Top 20 functions by time
```
## Testing Development

### Writing New Tests

#### Unit Test Template

```text
"""Test template for new functionality."""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import pytest

from flext_target_oracle.application.loader import FlextTargetOracleLoader
from tests import c, p, r, tm


class TestNewFeature:
    """Test suite for new feature."""

    def test_success_case(self):
        """Test successful operation."""
        # Arrange
        loader = FlextTargetOracleLoader(...)

        # Act
        result = new_feature_operation(loader)

        # Assert
        tm.ok(result.success)
        tm.that(result.value, eq=expected_value)

    def test_failure_case(self):
        """Test failure handling."""
        # Arrange
        invalid_loader = FlextTargetOracleLoader(...)

        # Act
        result = new_feature_operation(invalid_loader)

        # Assert
        tm.fail(result)
        assert "expected error message" in result.error

    @c.Tests.MARK.parametrize(
        "input_value,expected",
        [("valid_input", "expected_output"), ("another_input", "another_output")],
    )
    def test_parametrized(self, input_value, expected):
        """Test multiple input scenarios."""
        result = operation(input_value)
        tm.that(result, eq=expected)
```
#### Integration Test Template

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

"""Integration test template."""

import pytest

from flext_target_oracle.application.loader import FlextTargetOracleLoader


class TestOracleIntegration:
    """Integration tests requiring Oracle database."""

    @pytest.fixture
    def oracle_loader(self, sample_config):
        """Create loader with Oracle connection."""
        return FlextTargetOracleLoader(...)

    def test_end_to_end_processing(self, oracle_loader):
        """Test complete Singer message processing."""
        # Load record
        result = oracle_loader.load_record("test_stream", {...})
        tm.ok(result.success)
```
### Test Data Management

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)


# Test fixtures for consistent test data
@pytest.fixture
def sample_schema():
    """Standard test schema."""
    return {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
        },
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

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

# Test different batch sizes for optimal performance
import time

from flext_core import m, p
from flext_target_oracle.application.loader import FlextTargetOracleLoader


def benchmark_batch_sizes(records: list[p.Dict]):
    """Benchmark different batch sizes."""
    batch_sizes = [100, 500, 1000, 2000, 5000]
    results = {}

    for batch_size in batch_sizes:
        loader = FlextTargetOracleLoader(...)

        start_time = time.time()

        # Process all records
        for record in records:
            loader.load_record("test_stream", record)

        duration = time.time() - start_time
        results[batch_size] = {
            "duration": duration,
            "records_per_second": len(records) / duration,
        }

    # Print results
    for batch_size, stats in results.items():
        u.Cli.print(
            f"Batch size {batch_size}: {stats['records_per_second']:.1f} records/sec"
        )
```
### Memory Usage Monitoring

```text
from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import os

import psutil


def monitor_memory_usage():
    """Monitor memory usage during processing."""
    process = psutil.Process(os.getpid())

    def get_memory_mb():
        return process.memory_info().rss / 1024 / 1024

    u.Cli.print(f"Initial memory: {get_memory_mb():.1f} MB")

    # Your processing code here
    # ...

    u.Cli.print(f"Final memory: {get_memory_mb():.1f} MB")
```
## Contributing Guidelines

### Pull Request Checklist

Before submitting a pull request:

- [ ] **Code Quality**: `make check CHECK_PHASE=complete` passes with zero issues
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
1. **Architecture Review**: Ensure FLEXT pattern compliance
1. **Security Review**: Check for vulnerabilities
1. **Performance Review**: Validate no performance regressions
1. **Documentation Review**: Ensure documentation is updated

______________________________________________________________________

**Document Version**: 1.1\
**Reviewed**: 2026-11-28\
**Author**: Marlon Costa <marlon.costa@datacosmos.com.br>.

Historical metadata: version 1.0 was last updated on 2025-08-04 and recorded
2025-08-11 as its next-review date.
