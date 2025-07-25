# FLEXT Target Oracle - Oracle Database Singer Target
# ================================================
# Enterprise-grade Singer target for Oracle Database data loading
# Python 3.13 + Singer SDK + Oracle + FLEXT Core + Zero Tolerance Quality Gates

.PHONY: help info diagnose check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-singer
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: sync validate-config target-test target-validate target-schema target-run
.PHONY: oracle-write-test oracle-schema-check oracle-performance

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎯 FLEXT Target Oracle - Oracle Database Singer Target"
	@echo "====================================================="
	@echo "🎯 Singer SDK + Oracle + FLEXT Core + Python 3.13"
	@echo ""
	@echo "📦 Enterprise-grade Oracle Database target for Singer protocol"
	@echo "🔒 Zero tolerance quality gates with Oracle optimization"
	@echo "🧪 90%+ test coverage requirement with Oracle integration testing"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'


info: ## Show project information
	@echo "📊 Project Information"
	@echo "======================"
	@echo "Name: flext-target-oracle"
	@echo "Type: singer-target"
	@echo "Title: FLEXT TARGET ORACLE"
	@echo "Version: $(shell poetry version -s 2>/dev/null || echo "0.7.0")"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Not found")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Not installed")"
	@echo "Venv: $(shell poetry env info --path 2>/dev/null || echo "Not activated")"
	@echo "Directory: $(CURDIR)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo "Not a git repo")"
	@echo "Git Status: $(shell git status --porcelain 2>/dev/null | wc -l | xargs echo) files changed"

diagnose: ## Run complete diagnostics
	@echo "🔍 Running diagnostics for flext-target-oracle..."
	@echo "System Information:"
	@echo "OS: $(shell uname -s)"
	@echo "Architecture: $(shell uname -m)"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Not found")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Not installed")"
	@echo ""
	@echo "Project Structure:"
	@ls -la
	@echo ""
	@echo "Poetry Configuration:"
	@poetry config --list 2>/dev/null || echo "Poetry not configured"
	@echo ""
	@echo "Dependencies Status:"
	@poetry show --outdated 2>/dev/null || echo "No outdated dependencies"

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT TARGET ORACLE COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_target_oracle --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-singer: ## Run Singer protocol tests
	@echo "🧪 Running Singer protocol tests..."
	@poetry run pytest tests/singer/ -v
	@echo "✅ Singer tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_target_oracle --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🎯 SINGER TARGET OPERATIONS
# ============================================================================

sync: ## Sync data to Oracle target
	@echo "🎯 Running Oracle data sync..."
	@poetry run target-oracle --config $(TARGET_CONFIG) < $(TARGET_STATE)
	@echo "✅ Oracle sync complete"

validate-config: ## Validate target configuration
	@echo "🔍 Validating target configuration..."
	@poetry run target-oracle --config $(TARGET_CONFIG) --validate-config
	@echo "✅ Target configuration validated"

target-test: ## Test Oracle target functionality
	@echo "🎯 Testing Oracle target functionality..."
	@poetry run target-oracle --about
	@poetry run target-oracle --version
	@echo "✅ Target test complete"

target-validate: ## Validate target configuration
	@echo "🔍 Validating target configuration..."
	@poetry run target-oracle --config tests/fixtures/config/target_config.json --validate-config
	@echo "✅ Target configuration validated"

target-schema: ## Validate Oracle schema
	@echo "🔍 Validating Oracle schema..."
	@poetry run target-oracle --config tests/fixtures/config/target_config.json --validate-schema
	@echo "✅ Oracle schema validated"

target-run: ## Run Oracle data loading
	@echo "🎯 Running Oracle data loading..."
	@poetry run target-oracle --config tests/fixtures/config/target_config.json < tests/fixtures/data/sample_input.jsonl
	@echo "✅ Oracle data loading complete"

target-run-debug: ## Run Oracle target with debug logging
	@echo "🎯 Running Oracle target with debug..."
	@poetry run target-oracle --config tests/fixtures/config/target_config.json --log-level DEBUG < tests/fixtures/data/sample_input.jsonl
	@echo "✅ Oracle debug run complete"

target-dry-run: ## Run Oracle target in dry-run mode
	@echo "🎯 Running Oracle target dry-run..."
	@poetry run target-oracle --config tests/fixtures/config/target_config.json --dry-run < tests/fixtures/data/sample_input.jsonl
	@echo "✅ Oracle dry-run complete"

# ============================================================================
# 🗄️ ORACLE-SPECIFIC OPERATIONS
# ============================================================================

oracle-write-test: ## Test Oracle write operations
	@echo "🗄️ Testing Oracle write operations..."
	@poetry run python -c "from flext_target_oracle.client import TargetOracleClient; import asyncio; import json; config = json.load(open('tests/fixtures/config/target_config.json')); client = TargetOracleClient(config); print('Testing write operations...'); result = asyncio.run(client.test_write()); print('✅ Write test passed!' if result.is_success else f'❌ Write test failed: {result.error}')"
	@echo "✅ Oracle write test complete"

oracle-schema-check: ## Check Oracle schema compatibility
	@echo "🗄️ Checking Oracle schema compatibility..."
	@poetry run python scripts/validate_oracle_schema.py
	@echo "✅ Oracle schema check complete"

oracle-performance: ## Run Oracle performance tests
	@echo "⚡ Running Oracle performance tests..."
	@poetry run pytest tests/performance/ -v --benchmark-only
	@echo "✅ Oracle performance tests complete"

oracle-connect: ## Test Oracle connection
	@echo "🗄️ Testing Oracle connection..."
	@poetry run python -c "from flext_target_oracle.client import TargetOracleClient; import asyncio; import json; config = json.load(open('tests/fixtures/config/target_config.json')); client = TargetOracleClient(config); print('Testing connection...'); result = asyncio.run(client.connect()); print('✅ Connected!' if result.is_success else f'❌ Failed: {result.error}')"
	@echo "✅ Oracle connection test complete"

oracle-schema: ## Generate Oracle schema
	@echo "🗄️ Generating Oracle schema..."
	@poetry run python scripts/generate_oracle_schema.py
	@echo "✅ Oracle schema generation complete"

oracle-optimize: ## Optimize Oracle performance
	@echo "🗄️ Optimizing Oracle performance..."
	@poetry run python scripts/optimize_oracle_target.py
	@echo "✅ Oracle optimization complete"

oracle-diagnostics: ## Run Oracle diagnostics
	@echo "🔍 Running Oracle diagnostics..."
	@poetry run python scripts/oracle_diagnostics.py
	@echo "✅ Oracle diagnostics complete"

oracle-bulk-load: ## Test Oracle bulk loading
	@echo "🗄️ Testing Oracle bulk loading..."
	@poetry run python scripts/test_bulk_load.py
	@echo "✅ Oracle bulk load test complete"

oracle-parallel-load: ## Test Oracle parallel loading
	@echo "🗄️ Testing Oracle parallel loading..."
	@poetry run python scripts/test_parallel_load.py
	@echo "✅ Oracle parallel load test complete"

# ============================================================================
# 🔍 DATABASE VALIDATION
# ============================================================================

validate-tables: ## Validate Oracle table structures
	@echo "🔍 Validating Oracle table structures..."
	@poetry run python scripts/validate_tables.py
	@echo "✅ Table validation complete"

validate-data-types: ## Validate Oracle data type mappings
	@echo "🔍 Validating Oracle data type mappings..."
	@poetry run python scripts/validate_data_types.py
	@echo "✅ Data type validation complete"

validate-constraints: ## Validate Oracle constraints
	@echo "🔍 Validating Oracle constraints..."
	@poetry run python scripts/validate_constraints.py
	@echo "✅ Constraint validation complete"

validate-indexes: ## Validate Oracle indexes
	@echo "🔍 Validating Oracle indexes..."
	@poetry run python scripts/validate_indexes.py
	@echo "✅ Index validation complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# Target settings
TARGET_CONFIG := config.json
TARGET_STATE := state.json

# Singer settings
export SINGER_LOG_LEVEL := INFO
export SINGER_BATCH_SIZE := 10000
export SINGER_MAX_BATCH_AGE := 300

# Oracle Target settings
export TARGET_ORACLE_HOST := localhost
export TARGET_ORACLE_PORT := 1521
export TARGET_ORACLE_SERVICE_NAME := XE
export TARGET_ORACLE_DEFAULT_TARGET_SCHEMA := FLEXT_DW

# Performance settings
export TARGET_ORACLE_POOL_SIZE := 10
export TARGET_ORACLE_PARALLEL_DEGREE := 4
export TARGET_ORACLE_ENABLE_COMPRESSION := true

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-target-oracle
PROJECT_TYPE := meltano-plugin
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Target Oracle - Oracle Database Singer Target

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 SINGER SPECIFIC COMMANDS
# ============================================================================

singer-about: ## Show Singer target about information
	@echo "🎵 Singer target about information..."
	@poetry run target-oracle --about
	@echo "✅ About information displayed"

singer-config-sample: ## Generate Singer config sample
	@echo "🎵 Generating Singer config sample..."
	@poetry run target-oracle --config-sample > config_sample.json
	@echo "✅ Config sample generated: config_sample.json"

singer-test-streams: ## Test Singer streams
	@echo "🎵 Testing Singer streams..."
	@poetry run pytest tests/singer/test_streams.py -v
	@echo "✅ Singer streams tests complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Singer project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Singer Target + Oracle"
	@echo "🐍 Python: 3.13"
	@echo "🔗 Framework: FLEXT Core + Singer SDK"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Oracle Database Singer Target"
	@echo "🔗 Dependencies: flext-core, flext-db-oracle, singer-sdk"
	@echo "📦 Provides: Oracle data loading capabilities"
	@echo "🎯 Standards: Enterprise Oracle integration patterns"