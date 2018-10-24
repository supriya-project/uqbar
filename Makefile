.PHONY: docs build test

black:
	black --py36 --diff uqbar/ test/

black-check:
	black --py36 --diff --check uqbar/ test/

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

mypy:
	mypy uqbar/

release:
	make clean
	make build
	twine upload dist/*.tar.gz

test:
	pytest
