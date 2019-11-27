.PHONY: docs build

project = uqbar
errors = E123,E203,E265,E266,E501,W503
origin := $(shell git config --get remote.origin.url)
formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/

black-check:
	black --target-version py36 --diff --check ${formatPaths}

black-reformat:
	black --target-version py36 ${formatPaths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .*cache/
	rm -Rif .tox/
	rm -Rif __pycache__
	rm -Rif build/
	rm -Rif dist/
	rm -Rif htmlcod/
	rm -Rif prof/

docs:
	make -C docs/ html 

flake8:
	flake8 --max-line-length=90 --isolated --ignore=${errors} ${formatPaths}

gh-pages:
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

isort:
	isort --multi-line 1 --recursive --trailing-comma --use-parentheses -y ${formatPaths}

mypy:
	mypy --ignore-missing-imports ${project}/

pytest:
	pytest --cov=${project}/ --cov=tests/ --cov-report=html --cov-report=term

reformat:
	make isort
	make black-reformat

release:
	make clean
	make build
	twine upload dist/*.tar.gz

test:
	make black-check
	make flake8
	make mypy
	make pytest
	make docs
