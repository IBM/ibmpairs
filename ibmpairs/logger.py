"""
Environmental Intelligence: Geospatial APIs SDK (ibmpairs): A Python module to 
wrap the core functionality of the Geospatial APIs component.            

Copyright 2019-2024 IBM Software: Sustainability, IBM Corp. All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

import logging
from logging.config import dictConfig
from ibmpairs.config import LOGGING

dictConfig(LOGGING)
logger = logging.getLogger('paw')
