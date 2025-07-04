# FLEXT-TARGET-ORACLE Makefile - Oracle Singer Target
# ===================================================

.PHONY: help install test clean lint format build docs dev security target-test load-test

# Variables - Use workspace venv from FLEXT standards
PYTHON := /home/marlonsc/flext/.venv/bin/python
PIP := /home/marlonsc/flext/.venv/bin/pip
PYTEST := /home/marlonsc/flext/.venv/bin/python -m pytest
POETRY := poetry

# Default target
help: ## Show this help message
	@echo "🎯 FLEXT-TARGET-ORACLE - Oracle Singer Target"
	@echo "============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-target-oracle..."
	$(POETRY) install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	$(POETRY) install --all-extras --group dev --group test --group security

# Target Operations
target-run: ## Run target with sample data
	@echo "🎯 Running flext-target-oracle with sample data..."
	$(POETRY) run target-oracle --config config.json

target-test: ## Test target functionality
	@echo "🔍 Testing target functionality..."
	$(POETRY) run pytest tests/integration/ -v -k "target"

target-schema: ## Generate target schema
	@echo "📋 Generating target schema..."
	$(POETRY) run target-oracle --discover > schema.json

target-validate: ## Validate target configuration
	@echo "✅ Validating target configuration..."
	$(POETRY) run target-oracle --config config.json --test

# Testing
test: ## Run Singer target tests
	@echo "🧪 Running target tests..."
	$(POETRY) run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	$(POETRY) run pytest tests/ --cov=flext_target_oracle --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=95

test-oracle: ## Run Oracle-specific tests
	@echo "🗄️  Running Oracle tests..."
	$(POETRY) run pytest tests/ -v -m "oracle"

test-singer: ## Run Singer protocol tests
	@echo "🎵 Running Singer protocol tests..."
	$(POETRY) run pytest tests/ -v -m "singer"

test-integration: ## Run integration tests
	@echo "🔗 Running integration tests..."
	$(POETRY) run pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests
	@echo "🌐 Running end-to-end tests..."
	$(POETRY) run pytest tests/e2e/ -v --timeout=300

test-unit: ## Run unit tests only (legacy alias)
	@echo "🧪 Running unit tests..."
	$(POETRY) run pytest tests/test_basic_functionality.py tests/test_env_validation.py -v --tb=short --disable-warnings

performance-test: ## Run performance benchmarks
	@echo "⚡ Running performance tests..."
	$(POETRY) run pytest tests/performance/ -v --benchmark-only

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for target..."
	$(POETRY) run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting target code..."
	$(POETRY) run black .
	$(POETRY) run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	$(POETRY) run mypy flext_target_oracle --strict --show-error-codes
	@echo "✅ Type checking complete"

security: ## Run security analysis
	@echo "🔒 Running security analysis for target..."
	$(POETRY) run bandit -r flext_target_oracle/ -f json -o reports/security.json || true
	$(POETRY) run bandit -r flext_target_oracle/ -f txt
	@echo "✅ Security analysis complete"

pre-commit: ## Run pre-commit hooks
	@echo "🎣 Running pre-commit hooks..."
	$(POETRY) run pre-commit run --all-files
	@echo "✅ Pre-commit checks complete"

check: lint type-check security test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-target-oracle!"

# Build & Distribution
build: ## Build the package with Poetry
	@echo "🔨 Building flext-target-oracle package..."
	$(POETRY) build
	@echo "📦 Package built successfully"

build-docker: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t flext-target-oracle:latest .
	@echo "🏗️  Docker image built successfully"

# Singer Protocol Compliance
singer-check: ## Validate Singer protocol compliance
	@echo "🎵 Checking Singer protocol compliance..."
	$(POETRY) run target-oracle --config config.json --test-connection

singer-discover: ## Run Singer discovery
	@echo "🔍 Running Singer discovery..."
	$(POETRY) run target-oracle --discover

singer-spec: ## Show Singer specification
	@echo "📖 Showing Singer specification..."
	$(POETRY) run target-oracle --about

# Database Operations
db-test: ## Test Oracle database connection
	@echo "🗄️  Testing Oracle database connection..."
	$(POETRY) run python -c "from flext_target_oracle.connectors import test_connection; result = test_connection(); print('✅ Connection successful' if result else '❌ Connection failed')"

oracle-ping: ## Ping Oracle database
	@echo "🏓 Pinging Oracle database..."
	$(POETRY) run python -c "import oracledb; from flext_target_oracle.config_validator import get_connection_string; conn = oracledb.connect(get_connection_string()); print('✅ Oracle database is reachable')"

# Development Workflow
dev-setup: install-dev ## Complete development setup
	@echo "🎯 Setting up development environment for flext-target-oracle..."
	$(POETRY) run pre-commit install
	mkdir -p reports logs data
	@echo "✅ Development setup complete!"

dev: target-run ## Alias for development target run

# Legacy aliases for backward compatibility
run: target-run ## Legacy alias for target-run
debug: ## Run with debug logging (legacy)
	@echo "🐛 Running Oracle target with debug logging..."
	@if [ ! -f .env ]; then echo "Error: .env file not found. Copy .env.example and configure."; exit 1; fi
	@FLEXT_LOG_LEVEL=DEBUG $(PYTHON) -m flext_target_oracle.target

setup: install ## Legacy alias for install
validate: check ## Legacy alias for check
quick: format test-unit ## Quick development workflow
full: check ## Full validation workflow

# Cleanup
clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf reports/ logs/ .coverage htmlcov/
	@rm -rf data/ state/ output/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@find . -name "*.state" -delete 2>/dev/null || true
	@find . -name "*.log" -delete 2>/dev/null || true

# Environment variables
export PYTHONPATH := $(PWD):$(PYTHONPATH)
export FLEXT_TARGET_ORACLE_DEV := true
export SINGER_SDK_LOG_LEVEL := DEBUG