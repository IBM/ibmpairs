#########################################################
# IBM PAIRS API wrapper docker image generation         #
#########################################################
# Copyright 2019 Physical Analytics, IBM Research, IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

FROM ghcr.io/osgeo/gdal:ubuntu-full-3.7.0

MAINTAINER IBM PAIRS "pairs@us.ibm.com"
ENV PYTHONUNBUFFERED 1

# install Ubuntu packages
RUN apt-get update
RUN apt-get -y install \
    python3-pip \
    python3 

# install python, pip, virtualenv (conf)
RUN pip install --upgrade pip

# install jupyter and ibmpairs
RUN pip install jupyter
RUN pip install \
    numpy \
    Pillow \
    pandas \
    future \
    requests \
    shapely \
    fs \
    pytz \
    jsonschema \
    asyncio \
    aiodns \
    brotlipy \
    tableschema \
    ibm-cos-sdk \
    polling \
    aiohttp

# add IBM PAIRS to installation
RUN useradd -ms /bin/bash ibmpairs
USER ibmpairs
WORKDIR /home/ibmpairs
# add tutorials to the installation
COPY    tutorials/* /home/ibmpairs/
# add the IBM PAIRS open-source code
COPY    ibmpairs    /home/ibmpairs/ibmpairs/

# start python environment as Jupyter notebook

# https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini

USER root
RUN chown -R ibmpairs:ibmpairs /home/ibmpairs/*
RUN chmod +x /usr/bin/tini

USER ibmpairs
ENTRYPOINT ["/usr/bin/tini", "--"]

EXPOSE 18380:18380
CMD ["jupyter", "notebook", "--port=18380", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.token=''"]