# flext-target-oracle - Oracle Singer Target
PROJECT_NAME := flext-target-oracle
COV_DIR := flext_target_oracle
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: target-run test-unit test-integration build shell

target-run: ## Run target with config
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-oracle --config config.json

.DEFAULT_GOAL := help
