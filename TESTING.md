# Testing Guide for FLEXT Target Oracle

## Overview

The test suite is designed to work with both Oracle Standard Edition and Enterprise Edition databases. Tests for licensed features are automatically skipped when those features are not available.

## Quick Start

1. **Setup Environment**
   ```bash
   # Copy example configuration
   cp .env.example .env
   
   # Edit .env with your database credentials
   # Make sure to set oracle edition flags correctly
   ```

2. **Run Tests**
   ```bash
   # Run all tests
   pytest
   
   # Run only unit tests (no database needed)
   pytest -m unit
   
   # Run basic tests (work on all editions)
   ./run_tests.sh basic
   
   # Run Enterprise Edition tests
   ./run_tests.sh ee
   ```

## Oracle Edition Configuration

In your `.env` file, set these flags based on your Oracle Database:

### Standard Edition (SE2)
```env
DATABASE__ORACLE_IS_ENTERPRISE_EDITION=false
# Don't set any option flags - they default to false
```

### Enterprise Edition (EE)
```env
DATABASE__ORACLE_IS_ENTERPRISE_EDITION=true
# Only set these if you have the licenses:
DATABASE__ORACLE_HAS_PARTITIONING_OPTION=true
DATABASE__ORACLE_HAS_COMPRESSION_OPTION=true
DATABASE__ORACLE_HAS_INMEMORY_OPTION=true
```

## Test Categories

### 1. Unit Tests (No Database Required)
- Configuration validation
- Type mapping
- Basic functionality
- Run with: `pytest -m unit`

### 2. Basic Integration Tests (All Editions)
- Connection testing
- Basic CRUD operations
- Bulk inserts
- MERGE statements
- Run with: `pytest tests/test_basic_functionality.py`

### 3. Enterprise Edition Tests
- Parallel DML (EE only)
- Advanced compression (requires license)
- Partitioning (requires license)
- In-Memory features (requires license)
- Run with: `pytest tests/test_enterprise_features.py`

### 4. Performance Tests
- Throughput benchmarks
- Parallel processing tests
- Large dataset handling
- Run with: `pytest -m performance`

## Features by Oracle Edition

### Available in All Editions:
- ✅ Basic table operations
- ✅ Bulk INSERT/UPDATE/DELETE
- ✅ MERGE statements
- ✅ Basic compression
- ✅ Standard indexing
- ✅ Connection pooling
- ✅ JSON support (as CLOB)

### Enterprise Edition Only:
- ⚠️ Parallel DML (degree > 1)
- ⚠️ Result cache
- ⚠️ Adaptive query optimization

### Requires Additional License:
- 💰 Partitioning Option
- 💰 Advanced Compression Option
- 💰 In-Memory Option
- 💰 Advanced Security Option

## Running Specific Tests

```bash
# Test connection only
pytest tests/test_oracle_connection.py::test_basic_connection

# Test without licensed features
pytest -k "not partitioning and not compression and not inmemory"

# Test with verbose output
pytest -vv tests/test_enterprise_features.py

# Test with specific markers
pytest -m "integration and not slow"
```

## Conditional Test Execution

Tests automatically skip when:
1. `.env` file is missing
2. Database connection fails
3. Required Oracle edition/option is not available
4. Specific feature is not licensed

Example skip messages:
- "Parallel degree > 1 requires Oracle Enterprise Edition"
- "Advanced compression requires Oracle Advanced Compression option"
- "In-Memory feature requires Oracle In-Memory option"

## Environment Detection

The test suite can detect your Oracle edition in two ways:

1. **Explicit Configuration** (Recommended):
   Set `DATABASE__ORACLE_IS_ENTERPRISE_EDITION` in `.env`

2. **Automatic Detection**:
   If not set, tests query `V$VERSION` to detect edition

## Test Database Requirements

### Minimum Permissions:
- CREATE TABLE
- CREATE INDEX
- SELECT on V$ views (for edition detection)
- DML operations (INSERT, UPDATE, DELETE, MERGE)

### Recommended Setup:
```sql
-- Create test user
CREATE USER test_user IDENTIFIED BY password;
GRANT CONNECT, RESOURCE TO test_user;
GRANT CREATE SESSION TO test_user;
GRANT UNLIMITED TABLESPACE TO test_user;

-- For edition detection
GRANT SELECT ON V_$VERSION TO test_user;
GRANT SELECT ON V_$PARAMETER TO test_user;
```

## Troubleshooting

### All EE tests are skipped
- Check `DATABASE__ORACLE_IS_ENTERPRISE_EDITION=true` in `.env`
- Verify you're actually connected to an EE database

### Connection failures
- Verify database credentials in `.env`
- Check network connectivity
- For TCPS, ensure `DATABASE__PROTOCOL=tcps`

### Permission errors
- Ensure test user has required grants
- Check tablespace quotas

## CI/CD Integration

For automated testing:

```yaml
# GitHub Actions example
- name: Run tests
  env:
    DATABASE__HOST: ${{ secrets.ORACLE_HOST }}
    DATABASE__USERNAME: ${{ secrets.ORACLE_USER }}
    DATABASE__PASSWORD: ${{ secrets.ORACLE_PASS }}
    DATABASE__ORACLE_IS_ENTERPRISE_EDITION: ${{ vars.IS_EE }}
  run: |
    # Run only tests appropriate for the edition
    if [ "$DATABASE__ORACLE_IS_ENTERPRISE_EDITION" = "true" ]; then
      pytest
    else
      pytest -k "not enterprise"
    fi
```