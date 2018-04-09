.PHONY: docs build

build:
	python setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm -Rif
	find . -name '*egg-info' | xargs rm -Rif
	find . -name __pycache__ | xargs rm -Rif
	rm -Rif dist/
	rm -Rif build/

docs:
	make -C docs/ html 

release:
	make clean
	make build
	twine upload dist/uqbar*.tar.gz
