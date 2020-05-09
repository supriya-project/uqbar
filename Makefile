.PHONY: build docs gh-pages help
.DEFAULT_GOAL := help

project = uqbar
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

black-check:  ## Run black formatting check
	black --target-version py36 --diff --check ${formatPaths}

black-reformat:  ## Reformat via black
	black --target-version py36 ${formatPaths}

build:  ## Build distribution archive
	python setup.py sdist

clean:  ## Remove transitory files
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcov/
	rm -Rif prof/

docs:  ## Build the docs
	make -C docs/ html 

flake8:  ## Run flake8
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${formatPaths}

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
	isort \
		--case-sensitive \
		--multi-line 3 \
		--recursive \
		--trailing-comma \
		--use-parentheses \
		-y \
		${formatPaths}

mypy:  ## Run mypy
	mypy --ignore-missing-imports ${project}/

pytest:  ## Run pytest
	pytest --cov=${project}/ --cov=tests/ --cov-report=html --cov-report=term

reformat:
	make isort
	make black-reformat

release:
	make clean
	make build
	twine upload dist/*.tar.gz
	make docs
	make gh-pages

test:
	make black-check
	make flake8
	make mypy
	make pytest
	make docs
