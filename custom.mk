.PHONY: target-run test-unit test-integration build shell
target-run: ## Run target with settings
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-oracle --config settings.json
.DEFAULT_GOAL := help
