.PHONY: clean-pyc clean-build docs clean doctest wc complexity maintability sloc

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "doctest - run doctest"
	@echo "wc - count lines"
	@echo "complexity - calculate complexity"
	@echo "maintability - calculate maintability index"
	@echo "sloc - count sloc"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 pyqp tests

test:
	nosetests tests/

test-all:
	tox

coverage:
	nosetests pyqp/ tests/ --with-doctest --with-coverage --cover-tests --cover-inclusive --cover-package=pyqp

docs:
	rm -f docs/pyqp.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/pyqp
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

doctest:
	nosetests pyqp/ --with-doctest

sloc:
	radon raw -s pyqp/

complexity:
	radon cc -a pyqp/

maintability:
	radon mi pyqp/

wc:
	wc -l pyqp/*.py pyqp/*/*.py | sort -nr
