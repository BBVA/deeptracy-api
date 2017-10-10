.DEFAULT_GOAL := help

# AutoEnv
ENV ?= .env
ENV_GEN := $(shell ./.env.gen ${ENV} .env.required)
include ${ENV}
export $(shell sed 's/=.*//' ${ENV})


# AutoDoc
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -rf build dist .eggs .cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -rf .tox .coverage htmlcov coverage-reports

.PHONY: test
test: ## run tests quickly with the default Python
	python -m unittest discover -s tests/unit

.PHONY: test-all
test-all: ## run tests on every Python version with tox
	tox

install-%:
	pip install -r $*.txt -U

.PHONY: lint
lint: ## check style with flake8
	flake8 deeptracy_api

.PHONY: coverage
coverage: ## check code coverage
	coverage run --source=deeptracy_api -m unittest  discover -s tests/unit
	coverage report -m --fail-under 80
	coverage xml -o coverage-reports/report.xml

.PHONY: docs
docs: ## generate and shows documentation
	@make -C docs html

.PHONY: run
run: ## local run the API
	./run.sh

.PHONY: behave_local
behave_local: ## run behave tests in local environment
	LOCAL_BEHAVE=True behave --no-capture --no-capture-stderr tests/acceptance/features

.PHONY: behave_only
behave_only: ## run behave tests in local environment
	LOCAL_BEHAVE=True behave --no-capture --no-capture-stderr --tags=only tests/acceptance/features

.PHONY: behave
behave: ## run behave tests in docker environment
	behave --no-capture --no-capture-stderr tests/acceptance/features
