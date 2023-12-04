# Siena-MLS : Multimedia Library for Students

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/siena-mls)
[![PyPI - Version](https://img.shields.io/pypi/v/siena-mls)
](https://pypi.org/project/siena-mls/)

The project is a development platform designed for [Media Computation](http://web.eecs.umich.edu/~mjguz/mediacomp/mediaComp-teach/). It offers a pure Python implementation of [gatech-csl/jes](https://github.com/gatech-csl/jes), aiming to ensure consistent API functionality across both implementations. Notable enhancements beyond the foundational versions are detailed in subsequent sections. This package is compatible with any Python3.10^ version, allowing students to utilize the Python programming language to manipulate multimedia components, including images, sounds, and videos over online repl providers. The current API documentation aligns with the JES usage described in the reference book, and the functions implemented to date are provided here.

This library was developed for the Introduction to Computer Science (CSIS 110) course at Siena College, as well as the college's affiliated high school computer science programs.

## Project Commands & Scripts

This project utilizes [Poetry](https://python-poetry.org/) for efficient package & dependencies management. Below is a quick guide to the most commonly used commands:

### Installation
To install all dependencies, run:
```bash
poetry install
```

### Build
Build the project with:
```bash
poetry build
```

### Testing
Execute tests using pytest:
```bash
poetry run pytest
```

---

### Deploying to PyPi

**Version Update:** Before deploying, remember to update the version number in `pyproject.toml`.

**GitHub Actions Workflow:**
- **Pre-Release Deployment:** Create a pre-release in GitHub to push to `test.pypi.org`.
- **Release Deployment:** Create a release in GitHub to push to `pypi.org`.


## Support & Grants

[![Siena College](https://badgen.net/static/Supported%20By/Siena%20College?color=006747)](https://siena.edu)

## Contributions

_-Robin Flatland & Ninad Chaudhari (Siena College)_
# lab-python-unit-testing

## Annexture
<detail>
<summary>Alternate: not using pyTest</summary>
The same can be acheved without using pytest

```poetry run coverage run -m unittest discover```\
```poetry run coverage html```
</detail>
