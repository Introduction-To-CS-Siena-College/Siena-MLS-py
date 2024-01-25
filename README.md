# Siena-MLS : Multimedia Library for Students

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/siena-mls)
[![PyPI - Version](https://img.shields.io/pypi/v/siena_mls)
](https://pypi.org/project/siena-mls/)

The project is a development platform designed for [Media Computation](http://web.eecs.umich.edu/~mjguz/mediacomp/mediaComp-teach/). It offers a pure Python implementation of [gatech-csl/jes](https://github.com/gatech-csl/jes), aiming to ensure consistent API functionality across both implementations. Notable enhancements beyond the foundational versions are detailed in subsequent sections. This package is compatible with any Python3.10^ version, allowing students to utilize the Python programming language to manipulate multimedia components, including images, sounds, and videos over online repl providers. The current API documentation aligns with the JES usage described in the reference book, and the functions implemented to date are provided here.

This library was developed for the Introduction to Computer Science (CSIS 110) course at Siena College, as well as the college's affiliated high school computer science programs.

## Usage

To install the package in your projects, use pip / poetry / upm etc. The best way is to add the following to your pyproject.toml file:

```toml
[tool.poetry.dependencies]
python = ">=3.10.0,<3.11"
siena_mls = ">18" # This is the MLS Version ( check with the latest one )
```

If you just want to use this on a script, this will install it in your python environment.

```bash
pip install siena_mls
```

*Finaly* in the first line of your main file:

```python
from siena_mls import *
```

## Contributin and Deploying

The project is configured to auto deploy to PyPi on project release. Here is a possible sequence of actions that may help.

### Contributions

1. Use github codespaces / local VSCode to make changes.
2. Contribute any changes, test things out in `playground.py`.
3. Add files and Commit then push.
4. **Version Update:** : Increment Version in `pyproject.toml`.
5. **Pre-Release Deployment:** Create a pre-release in GitHub to push to `test.pypi.org`. Just confirm that the Actions ran and the version is avaliable over test.pypi
6. **Release Deployment:** Create a release in GitHub to push to `pypi.org`.

Refer to comamnds in Annex if you need to manually build / test / publish.

## Support & Grants

[![Siena College](https://badgen.net/static/Supported%20By/Siena%20College?color=006747)](https://siena.edu)

## Contributions

_-Robin Flatland & Ninad Chaudhari (Siena College)_

## Annexture

<details>
<summary>Alternate: not using pyTest</summary>
The same can be acheved without using pytest

```poetry run coverage run -m unittest discover```\
```poetry run coverage html```
</details>

## Installing dependencies

`pip install .` can parse `pyproject.toml` and install all deps in current python environment.

## Project Commands & Scripts

This project utilizes [Poetry](https://python-poetry.org/) for efficient package & dependencies management. Below is a quick guide to the most commonly used commands:

1. **Install Dependencies:** `poetry install`
2. **Build Project:** `poetry build`
3. **Test:** `poetry run pytest`
