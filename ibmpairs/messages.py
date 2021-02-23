"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# authentication messages
INFO_AUTHENTICATION_API_KEY_NOT_FOUND_IN_FILE = 'The api key for the user \'{}\' in file \'{}\' could not be found or set for the host \'{}\'.'
INFO_AUTHENTICATION_COULD_NOT_GET_AUTH_TOKEN = 'The authentication failed with auth token \'{}\', exception: \'{}\''
ERROR_AUTHENTICATION_COULD_NOT_FIND_API_KEY_FILE = 'The api key file \'{}\' could not be found.'
ERROR_AUTHENTICATION_NO_API_KEY_OR_CLIENT_ID = 'The OAuth2 Authentication type requires an api_key and client_id to be set.'
ERROR_AUTHENTICATION_NO_REFRESH_TOKEN_OR_CLIENT_ID = 'The OAuth2 Authentication refresh_auth_token() call requires a oauth2_response.refresh_token and client_id to be set. The method is intended to be called once a user has already authenticated but the jwt token has expired, try executing the get_auth_token() method.'
ERROR_AUTHENTICATION_PHOENIX_RETURN_NOT_OAUTH2RETURN = 'The json returned by the Phoenix GetBearerForClient service was not of type OAuth2Return. The returned json is: \'{}\', the exception: \'{}\''
ERROR_AUTHENTICATION_PHOENIX_NOT_SUCCESSFUL = 'The call to the Phoenix GetBearerForClient service was not successful, the status code is: \'{}\''
ERROR_AUTHENTICATION_PHOENIX_200_RETURN_ERROR = 'The call to the Phoenix GetBearerForClient service was successful but produced an error \'{}\', perhaps the api_key value is incorrect.'
ERROR_AUTHENTICATION_PHOENIX_REFRESH_200_RETURN_ERROR = 'The call to the Phoenix GetBearerForClient service was successful but produced an error \'{}\', perhaps the refresh_token value is incorrect.'

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
ERROR_COMMON_INT_TO_FLOAT = 'The value \'{}\' is an int rather than a float and cannot be cast to float.'
