"""
Environmental Intelligence: Geospatial APIs SDK (ibmpairs): A Python module to 
wrap the core functionality of the Geospatial APIs component.            

Copyright 2019-2024 IBM Software: Sustainability, IBM Corp. All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

import os

# global
GLOBAL_LEGACY_ENVIRONMENT      = os.environ.get('GLOBAL_LEGACY_ENVIRONMENT', "False")
if GLOBAL_LEGACY_ENVIRONMENT.lower() in ('true', 't', 'yes', 'y', '1', 'on'):
	GLOBAL_LEGACY_ENVIRONMENT = True
else:
	GLOBAL_LEGACY_ENVIRONMENT = False

PAW_LOG_LEVEL                 = os.environ.get('PAW_LOG_LEVEL', 'INFO')
GLOBAL_JSON_REPR_INDENT       = int(os.environ.get('GLOBAL_JSON_REPR_INDENT', 4))
GLOBAL_JSON_REPR_SORT_KEYS    = os.environ.get('GLOBAL_JSON_REPR_SORT_KEYS', True)
GLOBAL_SSL_VERIFY             = True

# catalog
CATALOG_DATA_SETS_API                   = '/datasets/'
CATALOG_DATA_SETS_API_FULL              = '/datasets/full'
CATALOG_DATA_SETS_LAYERS_API            = '/datalayers'

CATALOG_DATA_LAYERS_API                 = '/datalayers/'
CATALOG_DATA_LAYERS_API_FULL            = '/datalayers/full'
CATALOG_DATA_LAYERS_API_PROPERTIES      = '/datalayer_properties'
CATALOG_DATA_LAYERS_API_DIMENSIONS      = '/datalayer_dimensions'

CATALOG_DATA_LAYER_DIMENSIONS_API       = '/datalayer_dimensions/'
CATALOG_DATA_LAYER_DIMENSION_VALUES_API = '/datalayer_dimension_values/'

CATALOG_DATA_LAYER_PROPERTIES_API       = '/datalayer_properties/'

# client
CLIENT_URL                        = os.environ.get('CLIENT_URL_V3', 'https://api.ibm.com/geospatial/run/na/core/')
CLIENT_URL_V4                     = os.environ.get('CLIENT_URL_V4', CLIENT_URL + 'v4')
CLIENT_URL_V3                     = os.environ.get('CLIENT_URL_V3', CLIENT_URL + 'v3')
CLIENT_LEGACY_URL                 = os.environ.get('CLIENT_LEGACY_URL', 'https://pairs.res.ibm.com/v2')
CLIENT_JSON_HEADER                = {"Content-Type": "application/json"}
CLIENT_PUT_AND_POST_HEADER        = {'Content-Type': 'application/json', 'Accept': 'application/json'}
CLIENT_PUT_AND_POST_HEADER_CSV    = {'Accept': 'text/csv'}
CLIENT_GET_DEFAULT_RESPONSE_TYPE  = 'json'
CLIENT_TOKEN_REFRESH_MESSAGE      = 'claim expired'
CLIENT_TOKEN_REFRESH_MESSAGE_APIC = 'Invalid-JWT-Validate'
CLIENT_TIMEOUT                    = os.environ.get('CLIENT_TIMEOUT', 3600)

UPLOAD_API                     = '/uploader/upload'
UPLOAD_STATUS_API              = '/uploader/upload/'
UPLOAD_METADATA_FILE_EXTENTION = '.meta.json'

UPLOAD_DEFAULT_WORKERS         = int(os.environ.get('UPLOAD_DEFAULT_WORKERS', 1))
UPLOAD_MAX_WORKERS             = int(os.environ.get('UPLOAD_MAX_WORKERS', 8))
UPLOAD_MIN_STATUS_INTERVAL     = int(os.environ.get('UPLOAD_MIN_STATUS_INTERVAL', 30))
UPLOAD_STATUS_CHECK_INTERVAL   = int(os.environ.get('UPLOAD_STATUS_CHECK_INTERVAL', 60))
UPLOAD_WORKER_DEBUG            = os.environ.get('UPLOAD_WORKER_DEBUG', "False")
UPLOAD_WORKER_DEBUG            = False

# woc
EIS_V2_API_URL                 = os.environ.get('EIS_V2_API_URL', 'https://foundation.agtech.ibm.com/v2')
EIS_REGISTER_QUERY             = '/layer/analytics/metadata'
EIS_REGISTER_QUERY_URL         = EIS_V2_API_URL + EIS_REGISTER_QUERY
EIS_DASHBOARD_ADD_LAYER        = '/IMAP/put-layer-config-block'

# phoenix
PHOENIX_V1_API_URL             = os.environ.get('PHOENIX_V1_API_URL', 'https://api.auth-b2b-twc.ibm.com/api/v1')
PHOENIX_ADD_DASHBOARD_LAYER    = PHOENIX_V1_API_URL  + '/IMAP/put-layer-config-block'

#query
QUERY_API                      = '/query'
QUERY_JOBS_API                 = '/queryjobs/'
QUERY_JOBS_DOWNLOAD_API        = '/download'
QUERY_JOBS_API_MERGE           = '/merge/'
QUERY_JOB_HISTORY              = '/queryhistories/full/queryjob/'
QUERY_AOI_BASE                 = '/aois/'
QUERY_AOI_GEOMETRY             = '?format='
QUERY_AOI_METADATA             = QUERY_AOI_BASE
QUERY_AOI_SEARCH               = QUERY_AOI_BASE + 'search?name='
QUERY_DATE_FORMAT              = '%Y-%m-%d'
QUERY_DEFAULT_WORKERS          = int(os.environ.get('QUERY_DEFAULT_WORKERS', 1))
QUERY_MAX_WORKERS              = int(os.environ.get('QUERY_MAX_WORKERS', 8))
QUERY_MIN_STATUS_INTERVAL      = int(os.environ.get('QUERY_MIN_STATUS_INTERVAL', 15))
QUERY_STATUS_CHECK_INTERVAL    = int(os.environ.get('QUERY_STATUS_CHECK_INTERVAL', 30))
QUERY_STATUS_RUNNING_CODES     = [0, 1, 10, 11, 12]
QUERY_STATUS_SUCCESS_CODES     = [20]
QUERY_STATUS_FAILURE_CODES     = [21, 30, 31, 40, 41]
QUERY_DOWNLOAD_DEFAULT_FOLDER  = 'download'
QUERY_WORKER_DEBUG             = os.environ.get('QUERY_WORKER_DEBUG', "False")
QUERY_WORKER_DEBUG             = False
QUERY_ID_PATTERN               = "[0-9]{10}_[0-9]{8}"

#
IBM_CLOUD_OBJECT_STORE_CONTROL_URL = 'control.cloud-object-storage.cloud.ibm.com'
IBM_CLOUD_OBJECT_STORE_ENDPOINTS   = '/v2/endpoints'

# Used for conversion from degrees to metres / vice versa, and determining levels
RASTER_DEGREE_STEPS = [268.435456,134.217728,67.108864,33.554432,16.777216,8.388608,4.194304,2.097152,1.048576,0.524288,0.262144,0.131072,0.065536,0.032768,0.016384,0.008192,0.004096,0.002048,0.001024,0.000512,0.000256,0.000128,0.000064,0.000032,0.000016,0.000008,0.000004,0.000002,0.000001]
RASTER_METRE_STEPS = [29984528.23,14992264.12,7496132.058,3748066.029,1874033.015,937016.5073,468508.2536,234254.1268,117127.0634,58563.5317,29281.76585,14640.88293,7320.441463,3660.220731,1830.110366,915.0551829,457.5275914,228.7637957,114.3818979,57.19094893,28.59547446,14.29773723,7.148868616,3.574434308,1.787217154,0.893608577,0.446804289,0.223402144,0.111701072]

# external/ibm
IBM_COS_UPLOAD_PART_SIZE = 1024 * 1024 * 50 # Set 50 MB chunks
IBM_COS_UPLOAD_FILE_THRESHOLD = 1024 * 1024 * 50 # Set threshold to 50 MB
IBM_COS_PRESIGNED_URL_EXPIRY_TIME = 3600*24
IBM_COS_DOWNLOAD_PART_SIZE = 1024 * 1024 * 50 # Set 50 MB chunks
IBM_COS_DOWNLOAD_FILE_THRESHOLD = 1024 * 1024 * 50 # Set threshold to 50 MB
