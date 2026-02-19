# flext-target-oracle - Oracle Singer Target
PROJECT_NAME := flext-target-oracle
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: target-run test-unit test-integration build shell

target-run: ## Run target with config
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-oracle --config config.json

.DEFAULT_GOAL := help
