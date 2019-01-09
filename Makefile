.PHONY: clean test lint view-coverage upload-test

DEV_BIN     = venv/bin
PYTHON_BIN ?= python3
BROWSER    ?= firefox

test: venv
	@$(DEV_BIN)/nosetests --with-coverage --cover-html --cover-package=.

view-coverage: cover
	@$(BROWSER) cover/index.html

venv: dev_requirements.txt
	@virtualenv --python=$(PYTHON_BIN) venv
	@$(DEV_BIN)/pip install -e .
	@$(DEV_BIN)/pip install -r dev_requirements.txt

lint: venv
	@$(DEV_BIN)/pylint setup.py blizzard_api

dist: venv
	@$(DEV_BIN)/$(PYTHON_BIN) setup.py sdist bdist_wheel

upload-test:
	@$(DEV_BIN)/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload-prod:
	@$(DEV_BIN)/twine upload dist/*

clear-coverage:
	@rm -rf cover .coverage

clean: clear-coverage
	@rm -rf cache

clean-venv:
	@rm -rf venv *.egg-info build dist
