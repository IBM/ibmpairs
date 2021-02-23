"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
import os

# Dict corresponding to https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': os.getenv('PAW_LOG_MSG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            'datefmt': os.getenv('PAW_LOG_DATE_FORMAT', '%Y-%m-%d %H:%M:%S'),
        },
    },
    'handlers': {
        'default': {
            'level': os.getenv('PAW_LOG_LEVEL', 'DEBUG'),
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            "stream": "ext://sys.stdout"

        },
    },
    'loggers': {
        'paw': {
            'handlers': ['default'],
            'level': os.getenv('PAW_LOG_LEVEL', 'DEBUG'),
            'propagate': False
        }
    }
}
