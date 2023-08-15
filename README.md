# IBM Environmental Intelligence Suite (EIS): Geospatial Analytics open source modules

[![Build Status](https://travis-ci.org/IBM/ibmpairs.svg?branch=master)](https://travis-ci.org/IBM/ibmpairs)
[![PyPI Package](https://badge.fury.io/py/ibmpairs.svg)](https://pypi.org/project/ibmpairs/)


This repository provides an interface to the geo-spatial big data platform
[IBM EIS: Geospatial Analytics](https://www.ibm.com/products/environmental-intelligence-suite).

E.g. the `query` module in the subdirectory `ibmpairs` serves as a wrapper employing the IBM EIS: 
Geospatial Analytics core RESTful API served through the host reachable via
[https://pairs.res.ibm.com](https://pairs.res.ibm.com/manual/api-doc/).


# General Notes

If you like to contribute, please read [CONTRIBUTING.md](https://github.com/ibm/ibmpairs/blob/master/CONTRIBUTING.md)
first. A list of maintainers is recorded in [MAINTAINERS.md](https://github.com/ibm/ibmpairs/blob/master/MAINTAINERS.md).


# Installation and Usage

If you have installed the Python package manager [PIP](https://github.com/pypa/pip),
simply run
```Bash
pip install --user ibmpairs
```
Then you can import the IBM EIS: Geospatial Analytics API wrapper modules e.g.:
```Python
import ibmpairs.client as client
import ibmpairs.query as query
```


# Getting started

Simply get your feet wet with the [tutorial](https://github.com/ibm/ibmpairs/blob/master/tutorials/IBM-EIS-Geospatial-Analytics-API-wrapper.ipynb).
Having cloned into the repo, the full API documentation you can generate by [Sphinx](https://www.sphinx-doc.org/) and the corresponding
[ReadTheDocs](https://readthedocs.org/) theme by running e.g.
```Bash
pip install sphinx sphinx_rtd_theme
```
then make the html pages,
```Bash
make docs
```
or without Make
```Bash
cd docs && make html
```
then open `docs/_build/html/index.html` with your favorite browser.


# Running in a Docker container

A self-contained environment can be built with [Docker](http://www.docker.com) using
```Bash
git clone https://github.com/ibm/ibmpairs
cd ibmpairs
make docker-build
```
then run using:
```Bash
make docker-run
```
the environment can then be accessed from the following url:
```
http://localhost:18380
```

Alternatively you can execute these steps without Make using:
```Bash
git clone https://github.com/ibm/ibmpairs
cd ibmpairs
docker build -t ibmpairs .
```
to build and
```Bash
docker run \
    -dit \
    -p 18380:18380 \
    --name ibmpairs \
    ibmpairs:latest
```
or:
```Bash
docker-compose up ibmpairs
```
to run.