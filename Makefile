.PHONY: build docs gh-pages help
.DEFAULT_GOAL := help

project = uqbar
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build distribution archive
	python setup.py sdist
	python setup.py bdist_wheel --universal

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

lint: reformat ruff-lint mypy ## Run all linters

mypy: ## Run mypy
	mypy ${project}/

pytest: ## Run pytest
	pytest tests/ ${project}/

reformat: ruff-imports-fix ruff-format-fix ## Reformat codebase

ruff-format: ## Lint via ruff
	ruff format --check --diff ${formatPaths}

ruff-format-fix: ## Lint via ruff
	ruff format ${formatPaths}

ruff-imports: ## Format imports via ruff
	ruff check --select I,RUF022 ${formatPaths}

ruff-imports-fix: ## Format imports via ruff
	ruff check --select I,RUF022 --fix ${formatPaths}

ruff-lint: ## Lint via ruff
	ruff check --diff ${formatPaths}

ruff-lint-fix: ## Lint via ruff
	ruff check --fix ${formatPaths}
