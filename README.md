# IBM Environmental Intelligence (EI): Geospatial APIs SDK

[![PyPI Package](https://badge.fury.io/py/ibmpairs.svg)](https://pypi.org/project/ibmpairs/)

This repository provides an interface to the IBM EI: Geospatial APIs component:
[IBM EI: Geospatial APIs](https://www.ibm.com/products/environmental-intelligence).

E.g. the `query` module in the subdirectory `ibmpairs` serves as a wrapper employing the IBM EI: 
Geospatial APIs served through the RESTful host reachable via
[https://api.ibm.com/geospatial/run/na/core/v3/](https://developer.ibm.com/apis/catalog/envintelsuite--ibm-environmental-intelligence).

Sample applications that use `ibmpairs` can be located in the [Environmental-Intelligence](https://github.com/IBM/Environmental-Intelligence/tree/main) project.


# General Notes

If you like to contribute, please read [CONTRIBUTING.md](https://github.com/ibm/ibmpairs/blob/master/CONTRIBUTING.md)
first. A list of maintainers is recorded in [MAINTAINERS.md](https://github.com/ibm/ibmpairs/blob/master/MAINTAINERS.md).


# Installation and Usage

If you have installed the Python package manager [PIP](https://github.com/pypa/pip),
simply run
```Bash
pip install --user ibmpairs
```
Then you can import the IBM EI: Geospatial APIs SDK wrapper modules e.g.:
```Python
import ibmpairs.client as client
import ibmpairs.query as query
```


# Getting started

See the documentation [here](https://ibm.github.io/ibmpairs/) and try our tutorials.


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
