"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

import logging
from logging.config import dictConfig
from ibmpairs.config import LOGGING

dictConfig(LOGGING)
logger = logging.getLogger('paw')
