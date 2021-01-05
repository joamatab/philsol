help:
	@echo 'make install:          Install package and hooks'
	@echo 'make test:             Run tests with pytest'
	@echo 'make test-force:       Rebuilds regression test'

install:
	pre-commit install
	pip install .


test:
	pytest

mypy:
	mypy . --ignore-missing-imports

lint:
	tox -e flake8

pylint:
	pylint --rcfile .pylintrc philsol

lintdocs:
	flake8 --select RST

lintdocs2:
	pydocstyle philsol

doc8:
	doc8 docs/

autopep8:
	autopep8 --in-place --aggressive --aggressive **/*.py

codestyle:
	pycodestyle --max-line-length=88
