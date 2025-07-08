# FLEXT-TARGET-ORACLE Makefile - Data Integration Pipeline
# ===========================================================

.PHONY: help install test clean lint format build docs dev security type-check pre-commit

# Default target
help: ## Show this help message
	@echo "🏗️  Flext Target Oracle - Data Integration Pipeline"
	@echo "================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-target-oracle..."
	poetry install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	poetry install --all-extras --group dev --group test --group security

# Testing
test: ## Run tests
	@echo "🧪 Running tests for flext-target-oracle..."
	@if [ -d tests ]; then \
		python -m pytest tests/ -v; \
	else \
		echo "No tests directory found"; \
	fi

test-coverage: ## Run tests with coverage
	@echo "🧪 Running tests with coverage for flext-target-oracle..."
	@python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for flext-target-oracle..."
	poetry run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting code with strict standards..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	poetry run mypy src/flext_target_oracle --strict --show-error-codes
	@echo "✅ Type checking complete"

security: ## Run security analysis
	@echo "🔒 Running security analysis..."
	poetry run bandit -r src/ -f json -o reports/security.json || true
	poetry run bandit -r src/ -f txt
	@echo "✅ Security analysis complete"

pre-commit: ## Run pre-commit hooks
	@echo "🎣 Running pre-commit hooks..."
	poetry run pre-commit run --all-files
	@echo "✅ Pre-commit checks complete"

check: lint type-check security test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-target-oracle!"

# Build & Distribution
build: ## Build the package with Poetry
	@echo "🔨 Building flext-target-oracle package..."
	poetry build
	@echo "📦 Package built successfully"

build-clean: clean build ## Clean then build
	@echo "🔄 Clean build for flext-target-oracle..."

publish-test: build ## Publish to TestPyPI
	@echo "🚀 Publishing to TestPyPI..."
	poetry publish --repository testpypi

publish: build ## Publish to PyPI
	@echo "🚀 Publishing flext-target-oracle to PyPI..."
	poetry publish

# Documentation
docs: ## Generate documentation
	@echo "📚 Generating documentation for flext-target-oracle..."
	@if [ -f docs/conf.py ]; then \
		cd docs && make html; \
	else \
		echo "No docs configuration found"; \
	fi

# Cleanup
clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts for flext-target-oracle..."
	@rm -rf build/ dist/ *.egg-info/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true

# Development Workflow
dev-setup: install-dev ## Complete development setup
	@echo "🎯 Setting up development environment for flext-target-oracle..."
	poetry run pre-commit install
	mkdir -p reports
	@echo "✅ Development setup complete!"

dev: ## Run in development mode
	@echo "🔧 Starting flext-target-oracle in development mode..."
	PYTHONPATH=src poetry run python -m flext_target_oracle --debug

dev-test: ## Quick development test cycle
	@echo "⚡ Quick test cycle for development..."
	poetry run pytest tests/ -v --tb=short

# Environment variables
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export FLEXT_TARGET_ORACLE_DEV := true

# Data Integration commands
validate-schema: ## Validate data schemas
	@echo "🔍 Validating data schemas..."
	PYTHONPATH=src poetry run python -m {project_name.replace('-', '_')}.validate

test-connection: ## Test data source connection
	@echo "🔌 Testing data source connection..."
	PYTHONPATH=src poetry run python -m {project_name.replace('-', '_')}.test_connection
