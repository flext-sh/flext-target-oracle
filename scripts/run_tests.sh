#!/bin/bash

# Script to run tests for flext-target-oracle with Docker Oracle support

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="all"
KEEP_DB=false
COVERAGE=true
VERBOSE=false
WORKERS=1

# Parse command line arguments
while [[ $# -gt 0 ]]; do
	case $1 in
	--unit)
		TEST_TYPE="unit"
		shift
		;;
	--integration)
		TEST_TYPE="integration"
		shift
		;;
	--e2e)
		TEST_TYPE="e2e"
		shift
		;;
	--keep-db)
		KEEP_DB=true
		shift
		;;
	--no-coverage)
		COVERAGE=false
		shift
		;;
	--verbose | -v)
		VERBOSE=true
		shift
		;;
	--parallel | -n)
		WORKERS="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: $0 [options]"
		echo ""
		echo "Options:"
		echo "  --unit          Run only unit tests (no database required)"
		echo "  --integration   Run only integration tests (requires Oracle)"
		echo "  --e2e           Run only end-to-end tests (requires Oracle)"
		echo "  --keep-db       Keep Oracle container running after tests"
		echo "  --no-coverage   Disable coverage reporting"
		echo "  --verbose, -v   Enable verbose output"
		echo "  --parallel N    Run tests in parallel with N workers (unit tests only)"
		echo "  --help, -h      Show this help message"
		echo ""
		echo "Examples:"
		echo "  $0                    # Run all tests"
		echo "  $0 --unit            # Run only unit tests"
		echo "  $0 --integration -v  # Run integration tests with verbose output"
		echo "  $0 --keep-db         # Keep Oracle container after tests"
		exit 0
		;;
	*)
		echo -e "${RED}Unknown option: $1${NC}"
		exit 1
		;;
	esac
done

# Setup environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Export keep database flag
if [ "$KEEP_DB" = true ]; then
	export KEEP_TEST_DB=true
fi

# Build pytest command
PYTEST_CMD="pytest"

# Add test markers
case $TEST_TYPE in
unit)
	PYTEST_CMD="$PYTEST_CMD -m unit"
	echo -e "${GREEN}Running unit tests...${NC}"
	;;
integration)
	PYTEST_CMD="$PYTEST_CMD -m integration"
	echo -e "${GREEN}Running integration tests (requires Oracle)...${NC}"
	;;
e2e)
	PYTEST_CMD="$PYTEST_CMD -m e2e"
	echo -e "${GREEN}Running end-to-end tests (requires Oracle)...${NC}"
	;;
all)
	echo -e "${GREEN}Running all tests...${NC}"
	;;
esac

# Add parallel execution for unit tests
if [ "$TEST_TYPE" = "unit" ] && [ "$WORKERS" != "1" ]; then
	PYTEST_CMD="$PYTEST_CMD -n $WORKERS"
fi

# Add verbose flag
if [ "$VERBOSE" = true ]; then
	PYTEST_CMD="$PYTEST_CMD -vv"
fi

# Disable coverage if requested
if [ "$COVERAGE" = false ]; then
	PYTEST_CMD="$PYTEST_CMD --no-cov"
fi

# Check if we need Oracle container
if [ "$TEST_TYPE" != "unit" ]; then
	echo -e "${YELLOW}Checking Oracle container...${NC}"

	# Check if docker-compose is available
	if ! command -v docker-compose &>/dev/null; then
		echo -e "${RED}docker-compose is required for integration tests${NC}"
		exit 1
	fi

	# Check if Oracle container is running
	if ! docker ps | grep -q "flext-oracle-test"; then
		echo -e "${YELLOW}Oracle container not running. It will be started automatically by pytest.${NC}"
	else
		echo -e "${GREEN}Oracle container is already running.${NC}"
	fi
fi

# Create necessary directories
mkdir -p reports
mkdir -p htmlcov
mkdir -p .pytest_cache

# Run tests
echo -e "${YELLOW}Executing: $PYTEST_CMD${NC}"
echo ""

if $PYTEST_CMD; then
	echo ""
	echo -e "${GREEN}✓ Tests passed successfully!${NC}"

	if [ "$COVERAGE" = true ]; then
		echo ""
		echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
	fi

	exit 0
else
	echo ""
	echo -e "${RED}✗ Tests failed!${NC}"
	exit 1
fi
