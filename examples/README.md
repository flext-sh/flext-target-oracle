# FLEXT Target Oracle - Practical Examples

<!-- TOC START -->

- [Quick Navigation](#quick-navigation)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
- [Examples Overview](#examples-overview)
  - [1. Basic Usage](#1-basic-usage)
  - [2. Meltano Integration](#2-meltano-integration)
  - [3. Production Setup](#3-production-setup)
  - [4. Performance Tuning](#4-performance-tuning)
  - [5. Error Handling](#5-error-handling)
- [Running Examples](#running-examples)
- [Common Patterns](#common-patterns)
  - [FlextResult Error Handling](#flextresult-error-handling)
  - [Configuration Management](#configuration-management)
  - [FLEXT Ecosystem Integration](#flext-ecosystem-integration)
- [Testing Examples](#testing-examples)
- [Contributing Examples](#contributing-examples)
- [Security Notes](#security-notes)

<!-- TOC END -->

**Comprehensive examples for Oracle Singer target implementation and usage**

## Quick Navigation

| Example                                     | Use Case                                     | Complexity   |
| ------------------------------------------- | -------------------------------------------- | ------------ |
| [Basic Usage](basic_usage.py)               | Simple target setup and record processing    | Beginner     |
| [Meltano Integration](meltano_integration/) | Complete Meltano project configuration       | Intermediate |
| [Production Setup](production_setup.py)     | Enterprise configuration with error handling | Advanced     |
| [Performance Tuning](performance_tuning.py) | Batch optimization and monitoring            | Advanced     |
| [Error Handling](error_handling.py)         | Comprehensive error scenarios                | Intermediate |

## Getting Started

### Prerequisites

```bash
# Install FLEXT Target Oracle
pip install -e .

# Set up Oracle database (for testing)
docker run -d \
  --name oracle-xe \
  -p 1521:1521 \
  -e ORACLE_PASSWORD=oracle \
  gvenzl/oracle-xe:21-slim
```

### Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your Oracle credentials
export ORACLE_HOST=localhost
export ORACLE_PORT=1521
export ORACLE_SERVICE=XE
export ORACLE_USER=system
export ORACLE_PASSWORD=oracle
```

## Examples Overview

### 1. Basic Usage

Simple target initialization and Singer message processing with FLEXT patterns.

### 2. Meltano Integration

Complete Meltano project setup with target configuration and pipeline execution.

### 3. Production Setup

Enterprise-grade configuration with comprehensive error handling, monitoring, and security considerations.

### 4. Performance Tuning

Optimization techniques for high-volume data loading with batch tuning and connection management.

### 5. Error Handling

Comprehensive error scenarios and recovery strategies using FLEXT error patterns.

## Running Examples

```bash
# Basic usage example
python examples/basic_usage.py

# Production setup with configuration validation
python examples/production_setup.py

# Performance tuning with benchmarks
python examples/performance_tuning.py
```

## Common Patterns

### FlextResult Error Handling

All examples demonstrate railway-oriented programming with FlextResult patterns:

```python
result = target.process_singer_message(message)
if result.is_failure:
    logger.error(f"Processing failed: {result.error}")
    return result
```

### Configuration Management

Type-safe configuration with domain validation:

```python
config = FlextOracleTargetSettings(
    oracle_host="localhost",
    oracle_service="XE",
    oracle_user="target_user",
    oracle_password="secure_password"
)

validation_result = config.validate_domain_rules()
if validation_result.is_failure:
    raise ValueError(f"Invalid configuration: {validation_result.error}")
```

### FLEXT Ecosystem Integration

Integration with FLEXT core patterns and flext-db-oracle:

```python
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u
from flext_target_oracle import FlextOracleTarget, FlextOracleTargetSettings

logger = FlextLogger(__name__)
```

## Testing Examples

```bash
# Run example tests
pytest examples/tests/

# Test with actual Oracle connection
pytest examples/tests/ -m integration
```

## Contributing Examples

1. **Follow FLEXT Patterns**: Use FlextResult, m.Value, and structured logging
1. **Document Thoroughly**: Include comprehensive docstrings and comments
1. **Test Coverage**: Add corresponding tests in examples/tests/
1. **Security Awareness**: Highlight security considerations and best practices
1. **Production Ready**: Examples should be suitable for adaptation in production

## Security Notes

⚠️ **Important**: These examples include placeholder credentials for demonstration purposes.
**Never** use default credentials in production environments.

- Use environment variables for sensitive configuration
- Implement proper credential management
- Review security considerations in each example
- Follow FLEXT security best practices

______________________________________________________________________

**Next Steps**: Start with [Basic Usage](basic_usage.py) for a simple introduction to FLEXT Target Oracle.
