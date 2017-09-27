.PHONY: help clean clean-build clean-pyc clean-test
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

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -rf build dist .eggs .cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .tox .coverage htmlcov coverage-reports

install-%:
	@pip install -r $*.txt -U

lint: install-requirements_dev ## check style with flake8
	flake8 deptracy

test: install-requirements_dev ## run tests quickly with the default Python
	py.test

test-all: ## run tests on every Python version with tox
	tox

coverage: install-requirements_dev ## check code coverage quickly with the default Python
	coverage run -m pytest
	coverage report -m --fail-under 80
	coverage html

.PHONY: docs
docs: ## generate and shows documentation
	@make -C docs spelling html
	# Replace files with .md extension with .html extension
	@find ./docs/_build/ -name '*.html' -exec sed -i 's/\(\w*\)\.md\(W*\)/\1.html\2/g' {} \;
	@python -m webbrowser -t docs/_build/html/index.html

run: install-requirements ## run locally your application
	gunicorn --bind=0.0.0.0:8000 --worker-class=gevent --timeout=0 deptracy.app:app
