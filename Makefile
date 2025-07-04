# FLEXT Target Oracle - Development Makefile
# Complete development automation for target-oracle

.PHONY: help install setup clean test test-unit test-integration test-all lint format check validate run build package debug

# Variables
PYTHON := /home/marlonsc/flext/.venv/bin/python
PIP := /home/marlonsc/flext/.venv/bin/pip
PYTEST := /home/marlonsc/flext/.venv/bin/python -m pytest
RUFF := /home/marlonsc/flext/.venv/bin/ruff
MYPY := /home/marlonsc/flext/.venv/bin/mypy

# Default target
help: ## Show available commands
	@echo "FLEXT Target Oracle - Available Commands"
	@echo ""
	@echo "Setup & Build:"
	@echo "  install     - Install package in development mode"
	@echo "  setup       - Complete setup (install + check environment)"
	@echo "  build       - Build distribution packages"
	@echo "  package     - Create release package"
	@echo "  clean       - Clean all build artifacts"
	@echo ""
	@echo "Testing:"
	@echo "  test        - Run all tests (alias for test-all)"
	@echo "  test-unit   - Run unit tests only (no database)"
	@echo "  test-integration - Run integration tests (requires Oracle)"
	@echo "  test-all    - Run complete test suite"
	@echo ""
	@echo "Quality:"
	@echo "  lint        - Run code linting (ruff + mypy)"
	@echo "  format      - Auto-format code"
	@echo "  check       - Quick check (lint + unit tests)"
	@echo "  validate    - Full validation (format + lint + all tests)"
	@echo ""
	@echo "Development:"
	@echo "  run         - Run the target (requires .env file)"
	@echo "  debug       - Run with debug logging enabled"
	@echo "  dev         - Setup dev environment and run checks"
	@echo "  quick       - Quick dev cycle (format + unit tests)"
	@echo "  full        - Full validation workflow"

# Setup commands
install: ## Install package and dependencies
	@echo "Installing package..."
	@$(PIP) install -e ".[dev,test]"
	@echo "Installation complete"

clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete"

# Testing commands
test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	@$(PYTEST) tests/test_basic_functionality.py tests/test_env_validation.py -v --tb=short --disable-warnings
	@echo "Unit tests complete"

test-integration: ## Run integration tests
	@echo "Running integration tests..."
	@if [ ! -f .env ]; then echo "Error: .env file not found. Copy .env.example and configure."; exit 1; fi
	@$(PYTEST) tests/test_connection.py -v --tb=short --disable-warnings
	@echo "Integration tests complete"

test-all: ## Run all tests
	@echo "Running all tests..."
	@if [ ! -f .env ]; then echo "Error: .env file not found. Copy .env.example and configure."; exit 1; fi
	@$(PYTEST) tests/ -v --tb=short --disable-warnings
	@echo "All tests complete"

test: test-all ## Alias for test-all

# Quality commands
lint: ## Run code linting
	@echo "Running linting..."
	@$(PYTHON) -m ruff check flext_target_oracle/ tests/ || true
	@$(PYTHON) -m mypy flext_target_oracle/ || true
	@echo "Linting complete"

format: ## Format code
	@echo "Formatting code..."
	@$(PYTHON) -m ruff format flext_target_oracle/ tests/
	@$(PYTHON) -m ruff check --fix flext_target_oracle/ tests/ || true
	@echo "Formatting complete"

check: ## Quick quality check
	@echo "Running quick check..."
	@$(MAKE) lint
	@$(MAKE) test-unit
	@echo "Quick check complete"

validate: ## Complete validation
	@echo "Running complete validation..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test-all
	@echo "Validation complete"

# Usage commands
run: ## Run the Oracle target
	@echo "Running Oracle target..."
	@if [ ! -f .env ]; then echo "Error: .env file not found. Copy .env.example and configure."; exit 1; fi
	@$(PYTHON) -m flext_target_oracle.target

debug: ## Run with debug logging
	@echo "Running Oracle target with debug logging..."
	@if [ ! -f .env ]; then echo "Error: .env file not found. Copy .env.example and configure."; exit 1; fi
	@FLEXT_LOG_LEVEL=DEBUG $(PYTHON) -m flext_target_oracle.target

# Build commands
build: clean ## Build distribution packages
	@echo "Building distribution packages..."
	@$(PYTHON) -m pip install --upgrade build
	@$(PYTHON) -m build
	@echo "Build complete. Check dist/ directory."

package: build ## Create release package
	@echo "Creating release package..."
	@ls -la dist/
	@echo "Package ready for distribution"

# Setup commands
setup: install ## Complete setup with environment check
	@echo "Setting up development environment..."
	@$(MAKE) install
	@echo "Checking environment..."
	@$(PYTHON) -c "import flext_target_oracle; print(f'Package installed: {flext_target_oracle.__version__}')"
	@echo "Setup complete"

# Development shortcuts
dev: setup check ## Setup development environment and run checks

quick: format test-unit ## Quick development workflow

full: validate ## Full validation workflow