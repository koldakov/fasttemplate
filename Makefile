SHELL = /bin/bash
PYTHON = python3.12
ARGS = $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

help: # Display this message
	@sed -ne '/@sed/!s/# //p' $(MAKEFILE_LIST)

install: # Install Environ and dependencies
	@echo "Installing poetry"
	@$(PYTHON) -m pip install poetry
	@echo "Installing dependencies"
	@$(PYTHON) -m poetry install
	@echo "Initiating pre-commit"
	@$(PYTHON) -m poetry run pre-commit install

activate: # Activate virtual environment
	@$(PYTHON) -m poetry shell

test: # Run tests
	@$(PYTHON) -m poetry run pytest
