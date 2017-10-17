# Project documentation

## Requirements

The following Python packages need to be installed:

- `sphinx`
- `sphinx-autobuild`
- `sphinx_rtd_theme`
- `sphinxcontrib-httpdomain`

## How to generate auto-documentation from Python docstrings of the project

Run the following command from the `docs` folder:

`sphinx-apidoc -o source/modules ../deeptracy_api`

## How to generate the HTML documentation

Run:

`make html`

