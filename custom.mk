.PHONY: target-run test-unit test-integration build shell
target-run: ## Run target with config
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-oracle --config config.json
.DEFAULT_GOAL := help
