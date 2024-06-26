"""
Environmental Intelligence: Geospatial APIs SDK (ibmpairs): A Python module to 
wrap the core functionality of the Geospatial APIs component.            

Copyright 2019-2024 IBM Software: Sustainability, IBM Corp. All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# general messages
ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED = 'The json input type \'{}\' for {} is not recognized, the type must be in [\'str\', \'dict\'].'
ERROR_NO_RASTERIO = 'rasterio is not available on your system, please install rasterio to use this method.'

# authentication messages
INFO_AUTHENTICATION_API_KEY_NOT_FOUND_IN_FILE = 'The api key for the user \'{}\' in file \'{}\' could not be found or set for the host \'{}\'.'
INFO_AUTHENTICATION_PASSWORD_NOT_FOUND_IN_FILE = 'The password for the user \'{}\' in file \'{}\' could not be found or set for the host \'{}\'.'
INFO_AUTHENTICATION_COULD_NOT_GET_AUTH_TOKEN = 'The authentication failed with the provided auth token, exception: \'{}\''
ERROR_AUTHENTICATION_FAILED = 'AUTHENTICATION FAILED: A {} could not be gathered from the provided attributes.'
ERROR_AUTHENTICATION_COULD_NOT_FIND_API_KEY_FILE = 'The api key file \'{}\' could not be found.'
ERROR_AUTHENTICATION_NO_API_KEY_OR_CLIENT_ID = 'The OAuth2 Authentication type requires an api_key and client_id to be set.'
ERROR_AUTHENTICATION_NO_REFRESH_TOKEN_OR_CLIENT_ID = 'The OAuth2 Authentication refresh_auth_token() call requires a oauth2_response.refresh_token and client_id to be set. The method is intended to be called once a user has already authenticated but the jwt token has expired, try executing the get_auth_token() method.'
ERROR_AUTHENTICATION_RETURN_NOT_OAUTH2RETURN = 'The json returned by the {} service was not of type OAuth2Return. The returned json is: \'{}\', the exception: \'{}\''
ERROR_AUTHENTICATION_NOT_SUCCESSFUL = 'The call to the {} service was not successful, the status code is: \'{}\''
ERROR_AUTHENTICATION_NOT_SUCCESSFUL_API_CONNECT = 'The call to the {} service was not successful, the status code is: \'{}\', message: \'{}\''
ERROR_AUTHENTICATION_200_RETURN_ERROR = 'The call to the {} service was successful but produced an error \'{}\', perhaps the api_key value is incorrect.'
ERROR_AUTHENTICATION_REFRESH_200_RETURN_ERROR = 'The call to the {} service was successful but produced an error \'{}\', perhaps the refresh_token value is incorrect or a temporary issue with the authentication system prevented the procurement of an authentication token.'
INFO_AUTHENTICATION_TOKEN_REFRESH = 'Attempting to refresh authentication token.'
INFO_AUTHENTICATION_TOKEN_REFRESH_SUCCESS = 'The token was successfully refreshed.'
ERROR_AUTHENTICATION_TYPE_NOT_RECOGNIZED = 'The authentication type {} was not recognized.'
ERROR_AUTHENTICATION_IAM_NO_API_KEY_OR_CLIENT_ID = 'The OAuth2 Authentication type, when using API Connect, requires an api_key, client_id and org_id to be set.'
ERROR_AUTHENTICATION_NO_ACCESS_TOKEN = 'An access_token from {} the return could not be found, response \'{}\'.'
INFO_BOTH_CLIENT_ID_AND_TENANT_ID = 'The client_id {} and the tenant_id {} have both been specified; the tenant_id entry will be derived from client_id.'
ERROR_NO_CLIENT_OR_TENANT_ID = 'A client_id or tenant_id must be specified in order to authenticate via IBM API Connect.'
ERROR_NO_ORG_ID = 'An org_id must be specified in order to authenticate via IBM API Connect.'
INFO_STARTS_WITH_GEOSPATIAL = 'The string starts with geospatial, where it should start with saascore; correcting.'
INFO_STARTS_WITH_SAASCORE = 'The string starts with saascore, where it should start with geospatial; correcting.'
INFO_API_CONNECT_POSSIBLE_TENANT_ID_IN_CLIENT_ID_FIELD = 'It might be that a tenant_id is declared in the client_id field, attempting to auth with \'saascore-\' prefixed.'
INFO_AUTHENTICATION_SUCCESSFUL = 'Authentication success.'
INFO_AUTHENTICATION_API_KEY_TYPE = 'The authentication api key type is assumed to be {}, because the api key prefix \'PHX\' {} present.'
INFO_AUTHENTICATION_TYPE_API_KEY_REFRESH = 'The authentication api key type is assumed to be {}, because the api key prefix \'PHX\' {} present; trying to refresh.'
ERROR_AUTHENTICATION_VERSION_UNKNOWN = 'The host version specified {} is invalid, version must be in (2,3,4): default 3.'
INFO_AUTHENTICATION_TWO_IS_LEGACY = 'The specified host version is 2, which is synonymous with LEGACY=True; altered LEGACY=TRUE.'

# catalog messages
ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
INFO_CATALOG_RESPOSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE = 'There was no error message produced in the output of the failed call.'

ERROR_CATALOG_DATA_SET_ID = 'The DataSet object has no ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_DATA_SET_ID = 'The DataLayer object has no Data Set ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_DIMENSION_ID = 'The DataLayerDimension object has no ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_PROPERTY_ID = 'The DataLayerProperty object has no ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_DIMENSION_DATA_LAYER_ID = 'The DataLayerDimensions object has no Data Layer ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_DIMENSIONS_DATA_LAYER_ID = 'The DataLayerDimensions object has no Data Layer ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_PROPERTY_DATA_LAYER_ID = 'The DataLayerProperty object has no Data Layer ID set and none was provided.'
ERROR_CATALOG_DATA_LAYER_PROPERTIES_DATA_LAYER_ID = 'The DataLayerProperties object has no Data Layer ID set and none was provided.'
ERROR_CATALOG_DATA_SET_CREATE = 'The DataSet creation was not successful, error code: {}, message: {}.'
INFO_CATALOG_DATA_SET_CREATE_SUCCESS = 'The Data Set creation was successful, the new Data Set ID is: {}.'
ERROR_CATALOG_DATA_SET_UPDATE = 'The DataSet update was not successful, error code: {}, message: {}.'
INFO_CATALOG_DATA_SET_UPDATE_SUCCESS = 'The DataSet update was successful, the Data Set ID is: {}.'
INFO_CATALOG_DATA_SET_DELETE_SUCCESS = 'The DataSet \'{}\' was deleted successfully.'

ERROR_CATALOG_DATA_SETS_UNKNOWN = 'The DataSets from_dict method only takes a dict or list, the type \'{}\' is not accepted.'
ERROR_CATALOG_DATA_SETS_MULTIPLE_IDENTICAL_NAMES = 'The data_sets attribute has multiple sets with the name \'{}\'- this name should be unique.'
ERROR_CATALOG_DATA_SETS_NO_DATA_SET = 'The data_sets attribute does not contain a DataSet with the name attribute {}.'
ERROR_CATALOG_DATA_SETS_TYPE_UNKNOWN = 'The data_sets list can only be searched by int (positional) or a valid str, not {}.'
WARN_CATALOG_DATA_SETS_DATA_SET_OBJECT_NO_NAME = 'A data set in the data_sets object has no name and therefore cannot be searched.'

ERROR_CATALOG_DATA_LAYER_ID = 'The DataLayer object has no ID set and none was provided.'
ERROR_CATALOG_SET_DATA_LAYER_ID = 'The data layer id \'{}\' is neither an integer or a list of integers.'
INFO_CATALOG_DATA_LAYER_UPDATE_SUCCESS = 'The data layer update was successful, the data layer id is: \'{}\'.'
ERROR_CATALOG_DATA_LAYERS_NO_GROUP = 'The DataLayers.create method requires a group name to be set in the group attribute, please provide this into the method call as create(data_layer_group = \'<data_layer_group_name>\') or add to the object data_layers_object.group = \'<data_layer_group_name>\'.'
ERROR_CATALOG_DATA_LAYERS_SET_ID = 'The DataLayers object has no Data Set ID set and none was provided.'
ERROR_CATALOG_DATA_LAYERS_SET_LAYER_TYPE = 'The DataLayers object has no data layer type set.'
ERROR_CATALOG_DATA_LAYERS_TYPE_UNKNOWN = 'The data layers Type \'{}\' is not in [\'VectorPoint\',\'VectorPolygon\',\'Raster\']'
INFO_CATALOG_DATA_LAYERS_CREATE_SUCCESS = 'The data layers creation was successful, the new data layer ids are: {}.'
ERROR_CATALOG_DATA_LAYERS_UNKNOWN = 'The DataLayer from_dict method only takes a dict or list, the type {} is not accepted.'
ERROR_CATALOG_DATA_LAYERS_DATA_LAYER_COULD_NOT_SET_ATTR = 'The DataLayer \'{}\' value \'{}\' could not be set on the \'{}\' attribute.'
ERROR_CATALOG_DATA_LAYERS_DATA_LAYER_NAME_NOT_FOUND = 'The data layer \'{}\' could not be found in the DataLayers attribute data_layers.'
INFO_CATALOG_DATA_LAYERS_DATA_LAYER_ATTR_SET = 'The data layer \'{}\' had the value \'{}\' set on the attribute \'{}\'.'
ERROR_CATALOG_DATA_LAYERS_FILTER_DATA_LAYER_BY_ATTRIBUTE = 'No layers in self._data_layers could be found with the attribute \'{}\' value \'{}\' according to the regex \'{}\''
ERROR_CATALOG_DATA_LAYERS_MULTIPLE_IDENTICAL_NAMES = 'The DataLayers object has multiple layers with the name \'{}\'- this name should be unique.'
ERROR_CATALOG_DATA_LAYERS_NO_DATA_SET = 'The data_layers attribute does not contain a DataLayer with the full_name attribute {}.'
ERROR_CATALOG_DATA_LAYERS_TYPE_UNKNOWN = 'The data_layers list can only be searched by int (positional) or a valid str, not {}.'
ERROR_CATALOG_DATA_LAYERS_NO_DATA_SET = 'The data_layers attribute does not contain a DataLayers with the name attribute {}.'
ERROR_CATALOG_DATA_LAYERS_UNKNOWN = 'The data_layers list can only be searched by int (positional) or a valid str, not {}.'
WARN_CATALOG_DATA_LAYERS_DATA_LAYER_OBJECT_NO_NAME = 'A data layer in the data_layers object has no name and therefore cannot be searched.'
INFO_CATALOG_DATA_LAYER_DELETE_SUCCESS = 'The data layer \'{}\' was deleted successfully.'

WARN_CATALOG_DATA_LAYER_DIMENSIONS_OBJECT_NO_NAME = 'A data layer dimensions in the data_layer_dimensions object has no name and therefore cannot be searched.'
ERROR_CATALOG_DATA_LAYER_DIMENSIONS_MULTIPLE_IDENTICAL_NAMES = 'The data_layer_dimensions object has multiple dimensions with the name \'{}\'- this name should be unique.'
ERROR_CATALOG_DATA_LAYER_DIMENSIONS_UNKNOWN = 'The DataLayerDimension.from_dict() method only takes a dict or list, the type {} is not accepted.'
ERROR_CATALOG_DATA_LAYER_DIMENSIONS_NO_DATA_SET = 'The data_layer_dimensions attribute does not contain a DataLayerDimension with the full_name attribute {}.'
ERROR_CATALOG_DATA_LAYER_DIMENSIONS_TYPE_UNKNOWN = 'The data_layer_dimensions list can only be searched by int (positional) or a valid str, not {}.'
INFO_CATALOG_DATA_LAYER_DIMENSIONS_CREATE_SUCCESS = 'The Data Layer Dimension creation was successful, the new Data Layer Dimension is: {}.'

WARN_CATALOG_DATA_LAYER_PROPERTIES_OBJECT_NO_NAME = 'A data layer property in the data_layer_properties object has no name and therefore cannot be searched.'
ERROR_CATALOG_DATA_LAYER_PROPERTIES_MULTIPLE_IDENTICAL_NAMES = 'The data_layer_properties object has multiple properties with the name \'{}\'- this name should be unique.'
ERROR_CATALOG_DATA_LAYER_PROPERTIES_UNKNOWN = 'The DataLayerDimension.from_dict() method only takes a dict or list, the type {} is not accepted.'
ERROR_CATALOG_DATA_LAYER_PROPERTIES_NO_DATA_SET = 'The data_layer_properties attribute does not contain a DataLayerProperty with the full_name attribute {}.'
ERROR_CATALOG_DATA_LAYER_PROPERTIES_TYPE_UNKNOWN = 'The data_layer_properties list can only be searched by int (positional) or a valid str, not {}.'
INFO_CATALOG_DATA_LAYER_PROPERTY_CREATE_SUCCESS = 'The Data Layer Property creation was successful, the new Data Layer Property is: {}.'

ERROR_CATALOG_VECTOR_DATA_LAYER_FROM_FILE_NOT_FOUND = 'The vector data layer definition file \'{}\' was not found.'

# client messages
DEBUG_CLIENT_POST_BASIC = 'POSTing {} to url {} using basic auth.'
DEBUG_CLIENT_POST_OAUTH = 'POSTing {} to url {} using oauth.'
DEBUG_CLIENT_DELETE_BASIC = 'DELETE of {} using basic auth.'
DEBUG_CLIENT_DELETE_OAUTH = 'DELETE of {} using oauth.'
ERROR_CLIENT_AUTHENTICATION_MECHANISM = 'The authentication mechanism {} was not recognized.'
DEBUG_CLIENT_SET_HEADERS = 'The headers for the client set to {}.'
DEBUG_CLIENT_SET_AUTHENTICATION = 'The authentication for the client was set to {}.'

ERROR_CLIENT_UNSPECIFIED_ERROR = 'The {} {} to {} encountered an unspecified error contacting the server; the request was unsuccessful, error message: {}'
INFO_BASIC_AUTH_ASSUMPTION = 'The client authentication method is assumed to be Basic auth as password, or password file was specified.'
INFO_0AUTH2_AUTH_ASSUMPTION = 'The client authentication method is assumed to be OAuth2.'

# common messages
INFO_COMMON_CHECK_BOOL_CONVERSION = 'The \'{}\' value \'{}\' was converted to a boolean \'{}\'.'

ERROR_COMMON_FROM_LIST = 'The input method \'{}\' could not be executed against the \'{}\' list.'
ERROR_COMMON_CLASS_TO_DICT = 'The \'{}\' input object of type \'{}\' could not be cast to dict.'
ERROR_COMMON_CHECK_BOOL = 'The type \'{}\' of \'{}\' is invalid, the type should be in [\'bool\', \'str\', \'int\'].'
ERROR_COMMON_CHECK_BOOL_STRING_NOT_BOOL = 'The value \'{}\' is a string, but is not \'true\' or \'false\' (when converted to lower case) and therefore cannot be set to bool.';
ERROR_COMMON_CHECK_BOOL_INT_NOT_BOOL = 'The value \'{}\' is an integer, but is not \'1\' or \'0\' and therefore cannot be set to bool.';
ERROR_COMMON_CHECK_CLASS = 'The type \'{}\' is not an instance of class \'{}\''
ERROR_COMMON_CHECK_WRONG_TYPE = 'The type \'{}\' of \'{}\' is invalid, the type should be \'{}\'.'
ERROR_COMMON_CHECK_STR = 'The type \'{}\' of \'{}\' is invalid, the type should be in [\'str\', \'int\'].'
ERROR_COMMON_CHECK_INT = 'The type \'{}\' of \'{}\' is invalid, the type should be in [\'int\', \'str\'].'
ERROR_COMMON_CHECK_FLOAT = 'The type \'{}\' of \'{}\' is invalid, the type should be in [\'float\', \'str\', \'int\'].'
ERROR_COMMON_STR_TO_INT = 'The value \'{}\' is a string rather than an int and cannot be cast to int.'
ERROR_COMMON_STR_TO_FLOAT = 'The value \'{}\' is a string rather than a float and cannot be cast to float.'
ERROR_COMMON_INT_TO_STR = 'The value \'{}\' is an int rather than a string and cannot be cast to string.'
ERROR_COMMON_FLOAT_TO_STR = 'The value \'{}\' is a float rather than a string and cannot be cast to string.'
ERROR_COMMON_INT_TO_FLOAT = 'The value \'{}\' is an int rather than a float and cannot be cast to float.'
ERROR_NO_CLIENT = 'An ibmpairs client was not provided in the method or object init and a client has not been set in the environment. Please try setting a client.Client() object in your environment or provide a client argument.'
DEBUG_CLIENT_PROVIDED_FOUND = 'A client was provided in the method or object init and will be used.'
DEBUG_CLIENT_IN_OBJECT_FOUND = 'A client was found in the object and will be used.'
DEBUG_CLIENT_GLOBAL_FOUND = 'A global client was found in the environment and will be used.'

# project messages
WARN_NO_PROJECT_ON_IMPORT = 'The Watson Studio project lib could not be imported. This function is intended to take a file from the attached cos storage and copy locally into a notebook. Are you operating a notebook on a Watson Studio instance?'

# query messages
ERROR_QUERY_MERGE_BASE_ID_MISSING = 'The base_job_id was not specified and the object id is not present. Has this query been run? If not, execute Query.submit(). If so, update the object id as follows Query.id = \'<your_id>\''
ERROR_QUERY_MERGE_OTHER_ID_MISSING = 'The other_job_id was not specified.'
ERROR_QUERY_MERGE_ID_NOT_RECOGNIZED = 'The provided {}_job_id type is invalid, the type should be in [\'Query\', \'str\', \'int\'].'
INFO_QUERY_MERGE_SUCCESS = 'The merge of other job {} into base job {} was successful.'
ERROR_QUERY_MERGE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_CATALOG_RESPOSE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_QUERY_RESPOSE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_FAVORITE_STATUS_NOT_SUCCESSFUL = 'The {} {} to {} was not successful, the favorite status was not updated, the error code was: {}.'
WARN_QUERY_MULTIPLE_IDENTICAL_NAMES = 'The LatestQueries object has multiple queries with the name \'{}\'- the result that will be returned will be the latest.'
INFO_QUERY_NO_NAME = 'A query in the LatestQueries object has no name and therefore cannot be referred to by name for search.'
INFO_QUERY_NO_DATES_INPUT = 'The replace_dates function was called, however, no start and end dates were input, therefore no action will be taken.'
INFO_QUERY_RESPONSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE = 'There was no error message produced in the output of the failed call.'
INFO_REAL_TIME_POINT_QUERY_STATUS_SKIP = 'A real time point query is returned at the time of executing the Query.submit() method. The status is therefore complete. Skipping.'
INFO_REAL_TIME_POINT_QUERY_NO_DATA = 'A real time point query is returned at the time of executing the Query.submit() method. A download (save to disk) has been indicated, however there is no returned data to save from the Query.submit_response attribute. Skipping.'
INFO_REAL_TIME_POINT_QUERY_DOWNLOAD_SKIP = 'A real time point query is returned at the time of executing the Query.submit() method. There is nothing further to download. Skipping.'
INFO_FAVORITE_STATUS_SUCCESS = 'The favorite status of query {} was updated to {}.'
INFO_QUERY_SUBMIT_SUCCESS = 'The query was successfully submitted with the id: {}.'
INFO_QUERY_SUCCESS = 'The query {} was successful after checking the status.'
ERROR_QUERY_FAILED = 'The query {} failed, error {} {}'
INFO_QUERY_STATUS = 'The query {} has the status {}.'
ERROR_QUERY_UNKNOWN_STATE = 'The query {} completed with the unknown status_code {}.'
ERROR_QUERY_STATUS_HTTP_RESPONSE_CODE = 'Unable to check query status - HTTP response code {}.'
ERROR_QUERY_DELETED = 'The query {} has been deleted and therefore cannot be downloaded.'
INFO_QUERY_DOWNLOAD_PATH_SET = 'The query download folder is set to the path {}.'
WARN_QUERY_DOWNLOAD_PATH_CREATE = 'The query download folder {} was not present on the operating system as either a fixed or relative path. Attempting to create.'
INFO_QUERY_DOWNLOAD_PATH_CREATED = 'The query download folder {} was successfully created.'
ERROR_QUERY_DOWNLOAD_PATH_CREATED = 'The query download folder {} could not be created.'
INFO_QUERY_FORMAT = 'The query {} is a {}.'
INFO_QUERY_DOWNLOAD_FILE_SAVE = 'The query file for {} will be downloaded to the following path {}.'
INFO_QUERY_DOWNLOAD_FILE_SAVED = 'The query file for {} was successfully downloaded to {}.'
INFO_POINT_QUERY_DOWNLOAD_FILE_SAVED = 'The online point query output was successfully saved to {}.'
ERROR_QUERY_DOWNLOAD_UNSUCCESSFUL = 'The query file for {} could not be downloaded to {}, the operation failed.'
ERROR_POINT_QUERY_DOWNLOAD_UNSUCCESSFUL = 'The online point query could not be saved to {}, the operation failed.'
INFO_QUERY_DOWNLOAD_FILE_UNZIP = 'The query zip {} will be unzipped to the following path {}.'
INFO_QUERY_DOWNLOAD_FILE_UNZIPPED = 'The query zip {} was successfully unzipped to {}.'
ERROR_QUERY_DOWNLOAD_UNSUCCESSFUL_UNZIP = 'The query zip {} could not be unzipped to {}, the operation failed.'
ERROR_QUERY_DOWNLOAD_REQUEST_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_QUERY_EXCEED_MAX_WORKERS = 'The number of workers specified \'{}\' is greater than the maxmimum value\'{}\', please decrease.'
ERROR_QUERY_STATUS_INTERVAL = 'The status_interval specified \'{}\' is less than the minimum value \'{}\', please increase.'
INFO_QUERY_RUNNER_MUST_CHECK_STATUS = 'The status must be checked in order to query and download.'
ERROR_QUERY_RUNNER_CHOICE_INVALID = 'The choice of submit: {}, status: {} and download {} is invalid.'
ERROR_QUERY_JOB_LAYERS_UNKNOWN = 'The QueryJobLayers from_dict method only takes a dict or list, the type \'{}\' is not accepted.'
ERROR_QUERY_STATUS_ID_NOT_PRESENT = 'The query id was not present in the query object.'
ERROR_QUERY_MERGE_UNAUTHORIZED = 'Unauthorized: The user may not be the owner of both jobs (master and other).'
ERROR_QUERY_MERGE_NOT_FOUND = 'Not Found: It may be that one, or both, of the jobs (master and other) have failed.'
ERROR_QUERY_MERGE_PRECONDITION = 'Precondition Failed: It may be that the master and other jobs have different bounding boxes.'
ERROR_QUERY_JOB_LIST_UNKNOWN = 'The QueryJobList from_dict method only takes a dict or list, the type \'{}\' is not accepted.'
INFO_STARTING_EVENT_LOOP = 'No running async event loop detected; performing asyncio.run() to start a new event loop.'
DEBUG_FOUND_EVENT_LOOP = 'An already running async event loop was found; starting event loop in new thread.'
INFO_FOUND_EVENT_LOOP_STARTING_TASK = 'TASK: {} STARTING.'
INFO_FOUND_EVENT_LOOP_COMPLETED_TASK = 'TASK: {} COMPLETED.'
ERROR_QUERY_FAVORITE_NO_ID = 'The favorite or unfavorite call was not provided a query id and no id already exists in the object.'
ERROR_QUERY_HISTORY_NO_ID = 'The query history call was not provided a query id and no id already exists in the object.'
ERROR_LATEST_QUERIES_FAILED_TO_RETRIEVE_QUERIES = 'The queries in the latest queries list could not be retrieved, exception: {}.'
ERROR_QUERY_HISTORY_GET_FAILED = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_QUERY_LATEST_QUERIES_MULTIPLE_IDENTICAL_NAMES = 'The latest_queries attribute has multiple queries with the name \'{}\'- this name should be unique to use this search functionality, please refer to the query positionally instead (e.g. object.latest_queries[0]).'
ERROR_QUERY_LATEST_QUERIES_NO_QUERY = 'The latest_queries attribute does not contain a query with the name attribute {}.'
ERROR_QUERY_LATEST_QUERIES_TYPE_UNKNOWN = 'The latest_queries list can only be searched by int (positional) or a valid str, not {}.'
WARN_QUERY_LATEST_QUERIES_QUERY_OBJECT_NO_NAME = 'A query in the latest_queries object has no name and therefore cannot be searched.'
ERROR_QUERY_COULD_NOT_LOAD_POINT_QUERY = 'Unable to load point data into dataframe: {}.'
ERROR_QUERY_NO_POINT_DATA = 'There is no point data in the Query object at Query.submit_response.data available to load/return.'
INFO_QUERY_AOI_SUCCESSFUL = 'The AOI metadata for {} was retreived.'
ERROR_QUERY_NO_AOI_ID = 'The AOI object has no ID set and none was provided.'
ERROR_QUERY_NO_GEOJSON = 'Sorry, the GeoJSON Python module (e.g. via `pip install geojson`) is required for AOI.get() to operate. Please install and try again.'
WARN_QUERY_AOI_OBJECT_NO_ID = 'An AOI in the AOIs object has no id and therefore cannot be searched.'
ERROR_QUERY_AOI_NO_AOI = 'The aois attribute does not contain an AOI with the id attribute {}.'
ERROR_QUERY_AOI_MULTIPLE_IDENTICAL_IDS = 'The aois object has multiple properties with the id \'{}\'- this id should be unique.'
ERROR_QUERY_AOI_ID_TYPE_UNKNOWN = 'The aois list can only be searched by an int id no, not {}.'
ERROR_QUERY_AOI_UNKNOWN = 'The AOIs.from_dict() method only takes a dict or list, the type {} is not accepted.'
ERROR_QUERY_AOI_RESPOSE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
WARN_QUERY_INTERACTIVE_ALREADY_PERFORMED = 'The query.submit_response object has a data value already present; skipping action as it appears this is an online query and the gathering of data has already been performed.'
ERROR_QUERY_CANNOT_LOAD_GEOJSON = 'The provided geojson {} was invalid, unable to load.'
ERROR_QUERY_CANNOT_CONVERT_GEOJSON_TO_DICT = 'The Query.Spatial.geojson had an error converting to dict.'
ERROR_QUERY_CANNOT_LOAD_GEOJSON_TYPE_UNKNOWN = 'The provided geojson is an unknown type, please provide as a str, dict, geojson.feature.Feature or geojson.feature.FeatureCollection.'

# woc messages
ERROR_QUERY_TYPE_NOT_RECOGNIZED = 'The query input type {} is not recognized, should be in [\'query.Query\',\'dict\',\'str\']'

# external/ibm messages
INFO_IBM_COS_BUCKET_NO_ENDPOINT = 'The endpoint url could not be determined from the endpoint reference {}.'
ERROR_IBM_CLOUD_OBJECT_STORE_CONTROL_FAIL = 'The Cloud Object Store Endpoints url {} could not be reached, the error status code was {}.'
ERROR_IBM_INTERFACE_NOT_RECOGNIZED = 'The specified interface {} is not in [\'public\', \'private\', \'direct\'].'
ERROR_IBM_CLOUD_OBJECT_AUTH_ENDPOINT_NOT_FOUND = 'The Cloud Object Store Endpoints response did not contain an auth endpoint entry. Please see {} for valid endpoints.'
ERROR_IBM_COS_BUCKET_UNKNOWN_SERVICE_CREDENTIALS_FORMAT = 'The ibm_cos_service_credentials object was of type {} but could not be converted to an authentication.IBMCOSServiceCredentials object.'
ERROR_IBM_COS_BUCKET_UNKNOWN_COS_FILE_FORMAT = 'The ibm_cos_file object was of type {} but could not be converted to an authentication.IBMCOSFile object.'
ERROR_IBM_COS_RESOURCE_COULD_NOT_BE_CREATED = 'Cannot create IBM COS resource. Exception: {}.'
ERROR_IBM_COS_CLIENT_COULD_NOT_BE_CREATED = 'Cannot create IBM COS client.'
ERROR_IBM_COS_UPLOAD_CLIENT_ERROR = 'The upload of the file {} to IBM COS attempt encountered an IBM Client error: {}.'
ERROR_IBM_COS_UPLOAD_ERROR = 'The multi-part upload of the file {} to IBM COS encountered an error: {}.'
ERROR_IBM_COS_DOWNLOAD_CLIENT_ERROR = 'The download of the IBM COS file {} from bucket {} to {}{} locally, encountered an IBM Client error: {}.'
ERROR_IBM_COS_DOWNLOAD_ERROR = 'The multi-part download of the IBM COS file {} from bucket {} to {}{} locally, encountered an error: {}.'
ERROR_NO_IBM_COS_RESOURCE = 'The IBMCOSBucket object has self._resource (ibm_boto3 resource) object, please provide an api_key, resource_instance_id, ibm_auth_endpoint and endpoint when initialising the IBMCOSBucket object or execute the method IBMCOSBucket.set_resource(api_key, resource_instance_id, ibm_auth_endpoint, endpoint).'
ERROR_NO_IBM_COS_CLIENT = 'The IBMCOSBucket object has self._resource (ibm_boto3 resource) object, please provide an access_key_id, secret_access_key, resource_instance_id, ibm_auth_endpoint and endpoint when initialising the IBMCOSBucket object or execute the method IBMCOSBucket.set_client(access_key_id, secret_access_key, resource_instance_id, ibm_auth_endpoint, endpoint).'
DEBUG_IBM_COS_UPLOADING = 'The file {} will be uploaded to {} in the IBM COS bucket {}.'
DEBUG_IBM_COS_UPLOAD_SUCCESS = 'The file {} was successfully uploaded to {} in IBM COS bucket {}.'
DEBUG_IBM_COS_DELETING = 'The file {} will be deleted from the IBM COS bucket {}.'
DEBUG_IBM_COS_DELETE_SUCCESS = 'The file {} was successfully deleted from IBM COS bucket {}.'
DEBUG_IBM_COS_CREATING_DIRECTORY = 'The directory {} will be created.'
DEBUG_IBM_COS_DOWNLOADING = 'The IBM COS file {} in bucket {} will be downloaded locally to {}{}.'
DEBUG_IBM_COS_DOWNLOAD_SUCCESS = 'The IBM COS file {} from bucket {} was successfully uploaded to {}{}.'
ERROR_IBM_COS_ERROR = 'The {} call to {} for {} failed with exception: {}.'

# upload
ERROR_UPLOAD_LOCATION_NOT_RECOGNISED = 'The upload location: {}, was not recognized.'
ERROR_UPLOAD_STORAGE_NOT_RECOGNISED = 'The upload storage mechanism: {}, was not recognized, please provide an external.ibm.IBMCOSBucket object.'
ERROR_UPLOAD_RESPOSE_NOT_SUCCESSFUL = 'The {} {} call to {} failed with status code: {}, message: {}.'
ERROR_UPLOAD_URL_CANNOT_BE_REACHED = 'The url: {} could not be reached.'
ERROR_UPLOAD_STORAGE_METADATA_COULD_NOT_BE_LOADED = 'The contents of the metadata file {} in {} {} {} `{}` could not be converted to valid json.'
ERROR_UPLOAD_STATUS_INCORRECT_TRACKING_ID = 'Unable to track upload - invalid tracking ID.'
ERROR_UPLOAD_STATUS_NOT_AUTHORIZED = 'Unable to track upload - no authentication or unauthorized.'
ERROR_UPLOAD_STATUS_HTTP_RESPONSE_CODE = 'Unable to track upload - HTTP response code {}.'
ERROR_WORKER_UPLOAD_CONVERSION_FAILED = 'The {} operation failed to convert upload input type {}.'
ERROR_WORKER_MAX_EXCEEDED = 'The maximum number of workers is {}.'
ERROR_UPLOAD_STATUS_INTERVAL = 'The status_interval specified \'{}\' is less than the minimum value \'{}\', please increase.'
ERROR_UPLOAD_EXCEED_MAX_WORKERS = 'The number of workers specified \'{}\' is greater than the maxmimum value\'{}\', please decrease.'
INFO_UPLOAD_RESPONSE_NOT_SUCCESSFUL_NO_ERROR_MESSAGE = 'There was no error message produced in the output of the failed call.'
INFO_UPLOAD_SUBMIT_SUCCESS = 'The upload request was successfully submitted, tracking_id: {}.'
INFO_UPLOAD_STORAGE_NOT_PRESENT = 'There was no storage attached to the submit, therefore the url parameter should be reachable.'
INFO_UPLOAD_SUCCESS = 'The upload of {} to IBM PAIRS was a success.'
ERROR_UPLOAD_FAILED = 'The upload of {} to IBM PAIRS failed, error: {}.'
INFO_UPLOAD_STATUS = 'The upload of {} to IBM PAIRS has the status \'{}\'.'
INFO_WORKER_UPLOAD_TYPE = 'The worker upload type is Upload.'
INFO_WORKER_UPLOAD_TYPE_NOT_UPLOAD = 'The worker upload type is {}, attempting {}.'
DEBUG_WORKER_STARTING_EXECUTION = 'The upload worker execution will commence.'
DEBUG_UPLOAD_SUBMIT_SEARCH_METADATA = 'Searching for {} within the storage mechanism'
DEBUG_UPLOAD_SUBMIT_FOUND_METADATA = 'Found {} within the storage mechanism, the upload will use the metadata: {}.'
DEBUG_UPLOAD_SUBMIT_NO_METADATA_IN_STORAGE = 'Could not find {} within the storage mechanism or it could not be converted, assuming the metadata is within the object structure: {}.'
ERROR_UPLOAD_TYPE_NOT_RECOGNIZED = 'The upload input type {} is not recognized, should be in [\'ibmpairs.upload.Upload\']'
