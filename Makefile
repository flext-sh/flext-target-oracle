# FLEXT Target Oracle - Simplified Makefile
# Simple commands for development and testing

.PHONY: help install clean test test-unit test-integration test-all lint format check validate run

# Variables
PYTHON := /home/marlonsc/flext/.venv/bin/python
PIP := /home/marlonsc/flext/.venv/bin/pip
PYTEST := /home/marlonsc/flext/.venv/bin/python -m pytest

# Default target
help: ## Show available commands
	@echo "FLEXT Target Oracle - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install     - Install package"
	@echo "  clean       - Clean build files"
	@echo ""
	@echo "Testing:"
	@echo "  test-unit   - Run unit tests (no database needed)"
	@echo "  test-integration - Run integration tests (needs Oracle)"
	@echo "  test-all    - Run all tests"
	@echo "  test        - Alias for test-all"
	@echo ""
	@echo "Quality:"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code"
	@echo "  check       - Quick check (lint + unit tests)"
	@echo "  validate    - Full validation (format + lint + all tests)"
	@echo ""
	@echo "Usage:"
	@echo "  run         - Run the target (needs .env file)"

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

# Development shortcuts
dev: install check ## Setup development environment and run checks

quick: format test-unit ## Quick development workflow

full: validate ## Full validation workflow