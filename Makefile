.PHONY: clean test lint ci view-coverage

DEV_BIN     = venv/bin
PYTHON_BIN ?= python3
BROWSER    ?= firefox

test: venv
	@$(DEV_BIN)/nosetests --with-coverage --cover-html

view-coverage: cover
	@$(BROWSER) cover/index.html

venv: dev_requirements.txt
	@virtualenv --python=$(PYTHON_BIN) venv
	@$(DEV_BIN)/pip install -e .
	@$(DEV_BIN)/pip install -r dev_requirements.txt

lint: venv
	@$(DEV_BIN)/pylint --rcfile=.pylintrc setup.py blizzard_api

ci: lint test

clear-coverage:
	@rm -rf cover .coverage

clean: clear-coverage
	@rm -rf cache

clean-venv:
	@rm -rf venv *.egg-info
