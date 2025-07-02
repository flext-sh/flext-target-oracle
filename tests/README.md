# FLEXT Target Oracle - Test Suite

Comprehensive test suite for the FLEXT Oracle target implementation using Oracle Autonomous Database with TCPS connections.

## 🧪 Test Structure

### Test Categories

#### **Connection Tests** (`test_oracle_connection.py`)
- TCPS/SSL connection validation
- Oracle Autonomous Database features
- Connection pooling and health checks
- Character set and Unicode support
- Database version compatibility

#### **Core Functionality** (`test_target_functionality.py`)
- Singer SDK message processing
- Schema and record handling
- Batch processing and parallelization
- Data type mappings and transformations
- Configuration validation
- Error handling and recovery

#### **Oracle Features** (`test_oracle_features.py`)
- Oracle MERGE operations
- Bulk operations and array processing
- Parallel processing configuration
- Table compression and partitioning
- Connection pooling behavior
- Oracle-specific error handling

#### **Performance Benchmarks** (`test_performance_benchmarks.py`)
- High-throughput ingestion testing
- Bulk vs individual operation comparison
- Parallel degree scaling analysis
- Memory usage optimization
- Connection pool performance
- Large record handling

#### **End-to-End Integration** (`test_e2e_integration.py`)
- Complete ETL workflow simulation
- Schema evolution scenarios
- Error recovery workflows
- Monitoring and metrics collection
- Real-world data patterns

## 🏃 Running Tests

### Prerequisites

1. **Oracle Autonomous Database** access with TCPS connection
2. **Environment configuration** in `.env` file:
   ```env
   DATABASE__HOST=your-autonomous-db.adb.region.oraclecloud.com
   DATABASE__PORT=1522
   DATABASE__SERVICE_NAME=your_service_name
   DATABASE__USERNAME=your_username
   DATABASE__PASSWORD=your_password
   DATABASE__PROTOCOL=tcps
   DATABASE__SCHEMA=your_schema
   ```

3. **Python dependencies** installed:
   ```bash
   pip install -e .
   pip install pytest pytest-cov pytest-timeout pytest-benchmark
   ```

### Test Execution

#### **All Tests**
```bash
# Run complete test suite
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=flext_target_oracle --cov-report=html
```

#### **By Category**
```bash
# Connection tests only
pytest tests/test_oracle_connection.py -v

# Core functionality
pytest tests/test_target_functionality.py -v

# Oracle-specific features
pytest tests/test_oracle_features.py -v

# Performance benchmarks
pytest tests/test_performance_benchmarks.py -v

# End-to-end integration
pytest tests/test_e2e_integration.py -v
```

#### **By Markers**
```bash
# Integration tests (require database)
pytest -m integration

# Performance benchmarks
pytest -m performance

# Unit tests only (no database required)
pytest -m unit

# Slow tests
pytest -m slow

# Connection-specific tests
pytest -m connection
```

#### **Specific Test Functions**
```bash
# Test TCPS connection
pytest tests/test_oracle_connection.py::TestOracleConnection::test_tcps_connection_details -v

# Test bulk operations
pytest tests/test_oracle_features.py::TestOracleSpecificFeatures::test_bulk_operations -v

# Test complete ETL workflow
pytest tests/test_e2e_integration.py::TestE2EIntegration::test_complete_etl_workflow -v

# Test high-throughput performance
pytest tests/test_performance_benchmarks.py::TestPerformanceBenchmarks::test_high_throughput_ingestion -v
```

### Test Configuration

#### **Pytest Configuration** (`pytest.ini`)
- Test discovery patterns
- Marker definitions
- Output formatting
- Timeout settings
- Logging configuration

#### **Test Fixtures** (`conftest.py`)
- Oracle connection management
- Test data generation
- Configuration loading
- Performance timing utilities
- Table cleanup automation

## 📊 Test Coverage

### **Functional Coverage**
- ✅ **Connection Management**: TCPS, pooling, failover
- ✅ **Data Processing**: All Singer message types
- ✅ **Oracle Features**: MERGE, bulk ops, compression
- ✅ **Performance**: Throughput, scalability, optimization
- ✅ **Error Handling**: Retries, recovery, resilience
- ✅ **Schema Evolution**: Dynamic schema changes
- ✅ **Data Types**: Complete Oracle type mapping

### **Test Data Patterns**
- **Small datasets**: 100-1,000 records for functional testing
- **Medium datasets**: 5,000-10,000 records for integration
- **Large datasets**: 20,000-50,000 records for performance
- **Edge cases**: Unicode, special characters, extreme values
- **Real-world patterns**: Transaction data, user profiles

### **Performance Baselines**

| Test Scenario | Expected Throughput | Timeout |
|---------------|-------------------|---------|
| Basic ingestion | >1,000 records/sec | 60s |
| Bulk operations | >2,000 records/sec | 120s |
| High-throughput | >1,000 records/sec | 180s |
| Large records (~10KB) | >50 records/sec | 300s |
| Parallel processing | 2x+ baseline | 180s |

## 🔧 Test Configuration

### **Environment Variables**
```bash
# Test execution
ORACLE_TARGET_LOG_LEVEL=DEBUG
ORACLE_TARGET_TEST_MODE=true
PYTHONPATH=.

# Database connection (from .env)
DATABASE__HOST=...
DATABASE__PORT=1522
DATABASE__SERVICE_NAME=...
DATABASE__USERNAME=...
DATABASE__PASSWORD=...
DATABASE__PROTOCOL=tcps
```

### **Target Configuration for Tests**
```json
{
  "batch_size": 5000,
  "max_workers": 4,
  "pool_size": 10,
  "max_overflow": 20,
  "use_bulk_operations": true,
  "upsert_method": "merge",
  "enable_metrics": true,
  "max_retries": 3,
  "retry_delay": 1.0,
  "parallel_degree": 2
}
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Connection Failures**
```bash
# Verify .env file exists and has correct values
cat .env

# Test basic connection
python -c "
import os
from flext_target_oracle.connectors import OracleConnector
config = {...}  # Load from .env
connector = OracleConnector(config=config)
engine = connector.create_sqlalchemy_engine()
print('Connection successful')
"
```

#### **Test Failures**
```bash
# Run specific failing test with maximum verbosity
pytest tests/test_oracle_connection.py::test_basic_connection -vvv -s

# Check test logs
tail -f tests/pytest.log

# Run with debugging
pytest --pdb tests/test_target_functionality.py::test_schema_message_processing
```

#### **Performance Issues**
```bash
# Run performance tests individually
pytest tests/test_performance_benchmarks.py::test_high_throughput_ingestion -v --durations=0

# Monitor database during tests
# (Oracle performance views, connection counts, etc.)
```

### **Database Cleanup**
Tests automatically clean up tables, but manual cleanup may be needed:

```sql
-- List test tables
SELECT table_name FROM user_tables WHERE table_name LIKE 'TEST_%';

-- Drop test tables
DROP TABLE test_table_name CASCADE CONSTRAINTS;
```

## 📈 Continuous Integration

### **GitHub Actions**
```yaml
name: Oracle Target Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov
      - name: Run tests
        env:
          DATABASE__HOST: ${{ secrets.ORACLE_HOST }}
          DATABASE__PORT: 1522
          DATABASE__SERVICE_NAME: ${{ secrets.ORACLE_SERVICE }}
          DATABASE__USERNAME: ${{ secrets.ORACLE_USER }}
          DATABASE__PASSWORD: ${{ secrets.ORACLE_PASSWORD }}
          DATABASE__PROTOCOL: tcps
        run: pytest --cov=flext_target_oracle --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### **Test Reports**
- **Coverage**: HTML and XML reports
- **Performance**: Benchmark results
- **JUnit**: XML output for CI integration
- **Logs**: Detailed execution logs

## 🎯 Test Development

### **Adding New Tests**

1. **Choose appropriate test file** based on test category
2. **Follow naming conventions**: `test_*` functions
3. **Use appropriate markers**: `@pytest.mark.integration`
4. **Include table cleanup**: Use `table_cleanup` fixture
5. **Add performance timing**: Use `performance_timer` fixture
6. **Document test purpose**: Clear docstrings

### **Test Template**
```python
def test_new_feature(
    oracle_config: Dict[str, Any],
    test_table_name: str,
    oracle_engine: Engine,
    table_cleanup,
    performance_timer
):
    """Test description with expected behavior."""
    table_cleanup(test_table_name)
    
    # Setup
    target = OracleTarget(config=oracle_config)
    
    # Test execution
    performance_timer.start()
    # ... test logic ...
    performance_timer.stop()
    
    # Verification
    with oracle_engine.connect() as conn:
        # ... verify results ...
        pass
    
    # Assertions
    assert condition, "Error message"
```

### **Best Practices**
- **Isolated tests**: Each test should be independent
- **Meaningful assertions**: Clear success/failure criteria
- **Performance expectations**: Include throughput requirements
- **Error scenarios**: Test both success and failure paths
- **Data variety**: Use different data patterns and sizes

## 📚 Documentation

- **Test Results**: Available in `tests/` directory
- **Coverage Reports**: Generated in `htmlcov/`
- **Performance Data**: Logged during benchmark tests
- **CI Integration**: Test status in pull requests