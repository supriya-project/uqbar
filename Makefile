.PHONY: build docs gh-pages help
.DEFAULT_GOAL := help

project = uqbar
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

black-check:  ## Run black formatting check
	black --diff --check ${formatPaths}

black-reformat:  ## Reformat via black
	black ${formatPaths}

build:  ## Build distribution archive
	python setup.py sdist
	python setup.py bdist_wheel --universal

clean:  ## Remove transitory files
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/
	rm -Rif wheelhouse/

docs:  ## Build the docs
	make -C docs/ html 

docs-clean: ## Build documentation from scratch
	make -C docs/ clean html

flake8:  ## Run flake8
	flake8 ${formatPaths}

gh-pages:  ## Upload docs to GitHub pages
	rm -Rf gh-pages/
	git clone $(origin) gh-pages/
	cd gh-pages/ && \
		git checkout gh-pages || git checkout --orphan gh-pages
	rsync -rtv --del --exclude=.git docs/build/html/ gh-pages/
	cd gh-pages && \
		touch .nojekyll && \
		git add --all . && \
		git commit --allow-empty -m "Update docs" && \
		git push -u origin gh-pages
	rm -Rf gh-pages/

isort:  ## Reformat via isort
	isort ${formatPaths}

mypy:  ## Run mypy
	mypy ${project}/

pytest:  ## Run pytest
	pytest tests/ ${project}/

reformat:
	make isort
	make black-reformat

release:
	make clean
	make build
	make docs
	twine upload dist/*.tar.gz
	make gh-pages

test:
	make black-check
	make flake8
	make mypy
	make pytest
	make docs
