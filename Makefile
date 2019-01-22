.PHONY: docs build test

paths = uqbar/ tests/ *.py
errors = E123,E203,E265,E266,E501,W503

black-check:
	black --py36 --diff --check ${paths}

black-reformat:
	black --py36 ${paths}

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm -Rif
	find . -name '*egg-info' | xargs rm -Rif
	find . -name '.*_cache' | xargs rm -Rif
	find . -name .coverage | xargs rm -Rif
	find . -name __pycache__ | xargs rm -Rif
	rm -Rif build/
	rm -Rif dist/

docs:
	make -C docs/ html 

flake8:
	flake8 --max-line-length=90 --ignore=${errors} uqbar/ tests/

isort:
	isort --multi-line 1 --recursive --trailing-comma --use-parentheses -y ${paths}

mypy:
	mypy ${paths}

pytest:
	pytest --cov=uqbar/ --cov=tests/ --cov-report=html --cov-report=term

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
