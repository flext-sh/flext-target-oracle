# FLEXT Target Oracle - Project Makefile
# =======================================
# Project-specific commands for flext-target-oracle
# Extends the standardized build system

# Include the standardized build system
include Makefile.build

.PHONY: help test test-unit test-integration test-e2e test-docker
.PHONY: oracle-start oracle-stop oracle-logs oracle-shell
.PHONY: coverage coverage-html dev-setup validate

# Default target
.DEFAULT_GOAL := help

# ============================================================================
# 🎯 PROJECT-SPECIFIC HELP
# ============================================================================

help: ## Show project-specific help
	@echo "$(CYAN)🎯 FLEXT Target Oracle - Project Commands$(RESET)"
	@echo "$(CYAN)========================================$(RESET)"
	@echo ""
	@echo "$(YELLOW)Testing Commands:$(RESET)"
	@grep -E '^(test|coverage)[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Oracle Docker Commands:$(RESET)"
	@grep -E '^oracle[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Development Commands:$(RESET)"
	@grep -E '^(dev|validate)[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Standard Commands (std-*):$(RESET)"
	@echo "Use 'make std-help' to see all standardized commands"

# ============================================================================
# 🧪 TESTING WITH ORACLE DOCKER
# ============================================================================

test: ## Run all tests with Oracle Docker
	@echo "$(BLUE)🧪 Running all tests with Oracle Docker...$(RESET)"
	@./scripts/run_tests.sh

test-unit: ## Run unit tests only (no Docker required)
	@echo "$(BLUE)🧪 Running unit tests...$(RESET)"
	@./scripts/run_tests.sh --unit

test-integration: ## Run integration tests with Docker with Oracle Docker
	@echo "$(BLUE)🧪 Running integration tests...$(RESET)"
	@./scripts/run_tests.sh --integration

test-e2e: ## Run end-to-end tests with Oracle Docker
	@echo "$(BLUE)🧪 Running end-to-end tests...$(RESET)"
	@./scripts/run_tests.sh --e2e

test-docker: oracle-start ## Run all tests keeping Docker container alive
	@echo "$(BLUE)🧪 Running tests with persistent Oracle container...$(RESET)"
	@./scripts/run_tests.sh --keep-db

test-parallel: ## Run unit tests in parallel
	@echo "$(BLUE)⚡ Running unit tests in parallel...$(RESET)"
	@./scripts/run_tests.sh --unit --parallel 4

coverage: ## Run tests with coverage report
	@echo "$(BLUE)📊 Running tests with coverage...$(RESET)"
	@poetry run pytest --cov=flext_target_oracle --cov-report=term-missing --cov-report=html

coverage-html: coverage ## Open coverage HTML report
	@echo "$(BLUE)🌐 Opening coverage report...$(RESET)"
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🐳 ORACLE DOCKER MANAGEMENT
# ============================================================================

ORACLE_COMPOSE := ../flext-db-oracle/docker-compose.oracle.yml
ORACLE_CONTAINER := flext-oracle-test

oracle-start: ## Start Oracle Docker container
	@echo "$(BLUE)🐳 Starting Oracle container...$(RESET)"
	@docker-compose -f $(ORACLE_COMPOSE) up -d oracle-xe
	@echo "$(GREEN)✅ Oracle container started$(RESET)"
	@echo "$(YELLOW)Waiting for Oracle to be ready (this may take a minute)...$(RESET)"
	@until docker exec $(ORACLE_CONTAINER) sqlplus -L system/Oracle123@//localhost:1521/XE @/dev/null >/dev/null 2>&1; do \
		printf "."; sleep 5; \
	done
	@echo ""
	@echo "$(GREEN)✅ Oracle is ready!$(RESET)"

oracle-stop: ## Stop Oracle Docker container
	@echo "$(BLUE)🛑 Stopping Oracle container...$(RESET)"
	@docker-compose -f $(ORACLE_COMPOSE) down
	@echo "$(GREEN)✅ Oracle container stopped$(RESET)"

oracle-clean: ## Stop and remove Oracle container and volumes
	@echo "$(RED)🧹 Cleaning Oracle container and data...$(RESET)"
	@docker-compose -f $(ORACLE_COMPOSE) down -v
	@echo "$(GREEN)✅ Oracle cleaned$(RESET)"

oracle-logs: ## Show Oracle container logs
	@echo "$(BLUE)📋 Oracle container logs:$(RESET)"
	@docker logs -f $(ORACLE_CONTAINER)

oracle-shell: ## Open SQL*Plus shell in Oracle container
	@echo "$(BLUE)🐚 Opening Oracle SQL*Plus...$(RESET)"
	@docker exec -it $(ORACLE_CONTAINER) sqlplus system/Oracle123@//localhost:1521/XE

oracle-status: ## Check Oracle container status
	@echo "$(BLUE)📊 Oracle container status:$(RESET)"
	@docker ps -a --filter name=$(ORACLE_CONTAINER) --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

dev-setup: std-install-dev ## Complete development setup with test dependencies
	@echo "$(BLUE)🚀 Setting up development environment...$(RESET)"
	@poetry install --all-extras
	@pip install -r requirements-test.txt
	@echo "$(GREEN)✅ Development environment ready$(RESET)"

# ============================================================================
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# ============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	@echo "$(BLUE)🔍 Running linting...$(RESET)"
	@poetry run ruff check .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	@echo "$(BLUE)🔍 Running type checking...$(RESET)"
	@PYTHONPATH=src poetry run pyrefly check .

.PHONY: security
security: ## Run security scanning
	@echo "$(BLUE)🔒 Running security scans...$(RESET)"
	@poetry run bandit -r src/
	@poetry run pip-audit

.PHONY: test
test: ## Run tests with coverage (MANDATORY)
	@echo "$(BLUE)🧪 Running tests with coverage...$(RESET)"
	@poetry run pytest --cov=flext_target_oracle --cov-report=term-missing --cov-fail-under=75

.PHONY: format
format: ## Format code
	@echo "$(BLUE)🎨 Formatting code...$(RESET)"
	@poetry run ruff format .

.PHONY: fix
fix: ## Auto-fix issues
	@echo "$(BLUE)🔧 Auto-fixing issues...$(RESET)"
	@poetry run ruff check . --fix
	@poetry run ruff format .

validate-setup: std-validate-setup ## Validate project and dependencies
	@echo "$(BLUE)🔍 Validating project setup...$(RESET)"
	@test -f pytest.ini || { echo "$(RED)❌ pytest.ini missing$(RESET)"; exit 1; }
	@test -f conftest.py || { echo "$(RED)❌ conftest.py missing$(RESET)"; exit 1; }
	@test -d tests/unit || { echo "$(YELLOW)⚠️  tests/unit/ missing$(RESET)"; }
	@test -d tests/integration || { echo "$(YELLOW)⚠️  tests/integration/ missing$(RESET)"; }
	@echo "$(GREEN)✅ Project validation passed$(RESET)"

# ============================================================================
# 🔄 CONTINUOUS INTEGRATION
# ============================================================================

ci-test: ## Run tests in CI mode
	@echo "$(BLUE)🤖 Running tests in CI mode...$(RESET)"
	@poetry run pytest \
		--cov=flext_target_oracle \
		--cov-report=xml \
		--cov-report=term \
		--junit-xml=reports/junit.xml \
		--maxfail=5 \
		-v

ci-lint: ## Run linting (ZERO TOLERANCE) in CI mode
	@echo "$(BLUE)🤖 Running linting in CI mode...$(RESET)"
	@poetry run ruff check . --output-format=github
	@poetry run pyrefly check .

# ============================================================================
# 🛠️ UTILITIES
# ============================================================================

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)👀 Running tests in watch mode...$(RESET)"
	@poetry run ptw tests/ -- -x --tb=short

test-failed: ## Re-run only failed tests
	@echo "$(BLUE)🔄 Re-running failed tests...$(RESET)"
	@poetry run pytest --lf -x

test-debug: ## Run tests with debugging enabled
	@echo "$(BLUE)🐛 Running tests with debugging...$(RESET)"
	@poetry run pytest -x --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb

benchmark: ## Run performance benchmarks
	@echo "$(BLUE)⚡ Running performance benchmarks...$(RESET)"
	@poetry run pytest tests/performance/ -v --benchmark-only

# ============================================================================
# 📦 PACKAGE SPECIFIC
# ============================================================================

example: ## Run example Singer workflow
	@echo "$(BLUE)📦 Running example Singer workflow...$(RESET)"
	@cd examples && ./run_example.sh

validate-singer: ## Validate Singer tap compatibility
	@echo "$(BLUE)🎵 Validating Singer compatibility...$(RESET)"
	@poetry run singer-tools validate-config config.json.example
	@echo "$(GREEN)✅ Singer validation passed$(RESET)"

# ============================================================================
# 🎯 COMMON ALIASES
# ============================================================================

t: test ## Alias for test
tu: test-unit ## Alias for test-unit
ti: test-integration ## Alias for test-integration
c: coverage ## Alias for coverage
l: std-lint ## Alias for lint
f: std-format ## Alias for format
# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts and cruft
	@echo "🧹 Cleaning $(PROJECT_NAME) - removing build artifacts, cache files, and cruft..."

	# Build artifacts
	rm -rf build/ dist/ *.egg-info/

	# Test artifacts
	rm -rf .pytest_cache/ htmlcov/ .coverage .coverage.* coverage.xml

	# Python cache directories
	rm -rf .mypy_cache/ .pyrefly_cache/ .ruff_cache/

	# Python bytecode
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

	# Temporary files
	find . -type f -name "*.tmp" -delete 2>/dev/null || true
	find . -type f -name "*.temp" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true

	# Log files
	find . -type f -name "*.log" -delete 2>/dev/null || true

	# Editor files
	find . -type f -name ".vscode/settings.json" -delete 2>/dev/null || true
	find . -type f -name ".idea/" -type d -exec rm -rf {} + 2>/dev/null || true

	
	# Target-specific files
	rm -rf state.json state-*.json
	rm -rf data/ output/ temp/

	@echo "✅ $(PROJECT_NAME) cleanup complete"

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

