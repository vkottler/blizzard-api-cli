.PHONY: clean test lint

DEV_BIN     = venv/bin
PYTHON_BIN ?= python3

test: venv
	@$(DEV_BIN)/$(PYTHON_BIN) api_client.py

venv:
	@virtualenv --python=$(PYTHON_BIN) venv
	@$(DEV_BIN)/pip install -r requirements.txt
	@$(DEV_BIN)/pip install -r dev_requirements.txt

lint:
	@$(DEV_BIN)/pylint api_client.py py

clean:
	@rm -rf cache

clean-venv:
	@rm -rf venv
