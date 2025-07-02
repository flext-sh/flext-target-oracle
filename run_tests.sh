#!/bin/bash
# Test runner for FLEXT Target Oracle

echo "=== FLEXT Target Oracle Test Runner ==="
echo

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your Oracle database connection."
    exit 1
fi

# Show current edition configuration
echo "Current Oracle Edition Configuration:"
grep -E "ORACLE_IS_ENTERPRISE_EDITION|ORACLE_HAS_.*_OPTION" .env 2>/dev/null || echo "No edition settings found (defaults to Standard Edition)"
echo

# Parse command line arguments
TEST_TYPE=${1:-all}

case $TEST_TYPE in
    unit)
        echo "Running unit tests (no database required)..."
        pytest -m unit -v
        ;;
    basic)
        echo "Running basic integration tests (work on all editions)..."
        pytest tests/test_basic_functionality.py tests/test_configuration.py -v
        ;;
    integration)
        echo "Running integration tests (database required)..."
        pytest -m integration -v
        ;;
    ee)
        echo "Running Enterprise Edition tests..."
        echo "Note: These tests will be skipped if not on Enterprise Edition"
        pytest tests/test_enterprise_features.py -v
        ;;
    performance)
        echo "Running performance benchmarks..."
        pytest -m performance -v
        ;;
    all)
        echo "Running all tests..."
        pytest -v
        ;;
    *)
        echo "Usage: $0 [unit|basic|integration|ee|performance|all]"
        echo
        echo "Test types:"
        echo "  unit        - Unit tests (no database needed)"
        echo "  basic       - Basic functionality tests"
        echo "  integration - Integration tests (database required)"
        echo "  ee          - Enterprise Edition specific tests"
        echo "  performance - Performance benchmarks"
        echo "  all         - All tests (default)"
        exit 1
        ;;
esac

echo
echo "Test run complete!"

# Show coverage if pytest-cov is installed
if command -v coverage &> /dev/null; then
    echo
    echo "To generate coverage report, run:"
    echo "  pytest --cov=flext_target_oracle --cov-report=html"
fi