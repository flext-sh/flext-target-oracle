.PHONY: target-run test-unit test-integration build shell
target-run: ## Run target with settings
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run target-oracle --settings settings.json
.DEFAULT_GOAL := help
