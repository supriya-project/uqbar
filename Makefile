.PHONY: docs gh-pages help
.DEFAULT_GOAL := help

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Remove transitory files
	find . -name '*.pyc' | xargs rm
	find . -name '.ipynb_checkpoints' | xargs rm -Rf
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/
	rm -Rif wheelhouse/

docs: ## Build the docs
	make -C docs/ html

docs-clean: ## Build documentation from scratch
	make -C docs/ clean html

mypy: ## Run mypy
	mypy src/

pytest: ## Run pytest
	pytest tests/ src/
