"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
import os
import re
from typing import Any
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.constants as constants
import ibmpairs.common as common
from ibmpairs.logger import logger
import ibmpairs.messages as messages
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import requests
#}}}

# fold: String Literals {{{
PAIRS_DEFAULT_PASSWORD_FILE_NAME    = u'auth/basic.txt'
PAIRS_PASSWORD_FILE_COMMENT_REG_EX  = re.compile(r'^\s*#')
#}}}

# fold: Basic Class {{{
class Basic:
    #_host: str
    #_username: str
    #_password: str
    #_password_file: str
    
    """
    An object to represent basic credentials and recovery from a file.

    :param host:             IBM PAIRS host, defaults to https://pairs.res.ibm.com
    :type host:              str
    :param username:         IBM PAIRS username
    :type username:          str
    :param password:         IBM PAIRS password
    :type password:          str
    :param password_file:    IBM PAIRS password file, defaults to auth/basic.txt
    :type password_file:     str
    :raises Exception:       if username and password are not present
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns: A string representation of the internal class structure.
        :rtype:   str
        """
        
        return_dict = self.to_dict()
        
        if "password" in return_dict:
            return_dict["password"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns: A dict representation of the internal class structure.
        :rtype:   dict
        """
      
        return_dict = self.to_dict()
        
        if "password" in return_dict:
            return_dict["password"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    #
    def __init__(self,
                 host: str          = constants.CLIENT_PAIRS_URL,
                 username: str      = None,
                 password: str      = None,
                 password_file: str = "auth/basic.txt"
                ):
        self._host          = common.strip_protocol(host)
        self._username      = username
        self._password      = password
        self._password_file = password_file
        
        if ((self._password is None) and (self._username is not None)):
            try:
                self.set_credentials_from_file(self._username, self._password_file, self._host)
            except Exception as e:
                msg = messages.INFO_AUTHENTICATION_PASSWORD_NOT_FOUND_IN_FILE.format(self._username, self._password_file, self._host)
                logger.info(msg)
        
        if (self._password is None) or (self._username is None):
            msg = messages.ERROR_AUTHENTICATION_FAILED.format('username and password')
            logger.error(msg)
            raise common.PAWException(msg)
            

    #
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.check_str(common.strip_protocol(host))
        
    #    
    def del_host(self): 
        del self._host

    #    
    host = property(get_host, set_host, del_host)

    #
    def get_username(self):
        return self._username
    
    #
    def set_username(self, username):
        self._username = common.check_str(username)
        
    #    
    def del_username(self): 
        del self._username

    #    
    username = property(get_username, set_username, del_username)

    #
    def get_password(self):
        return self._password

    #
    def set_password(self, password):
        self._password = common.check_str(password)
        
    #    
    def del_password(self): 
        del self._password

    #    
    password = property(get_password, set_password, del_password)
    
    #
    def get_password_file(self):
        return self._password_file

    #
    def set_password_file(self, password_file):
        if os.path.isfile(os.path.join(os.getcwd(), password_file)):
            self._password_file = os.path.join(os.getcwd(), password_file)
        elif os.path.isfile(password_file):
            self._password_file = common.check_str(password_file)
        else:
            raise ValueError(
                "The file '{}' could not be found.".format(
                    password_file
                )
            )
        
    #    
    def del_password_file(self): 
        del self._password_file

    #    
    password_file = property(get_password_file, set_password_file, del_password_file)

    #
    def set_credentials(self, username, password):
        self.set_username(username)
        self.set_password(password)
        
    #
    def set_credentials_from_file(self, username, password_file, host):
        
        """
        Set credentials attributes from a file, calls get_password_from_file.

        :param username:      The username string.
        :type username:       str
        :param password_file: The password_file string.
        :type password_file:  str
        :param host:          The host string.
        :type host:           str
        :raises Exception:    if password file does not exist,
                              if password was not found
        """ 
      
        self.set_username(username)
        self.set_password_file(password_file)
        self.set_host(host)
        self.set_password(get_password_from_file(server   = self._host,
                                                 user     = self._username,
                                                 passFile = self._password_file
                                                )
                         )

    #
    def get_credentials(self):
        return (self.get_username(), self.get_password())
    
    #
    def get_credentials_from_file(self, username, password_file, host):
      
        """
        Gets username and password credentials from a file, calls get_password_from_file.

        :param username:      The username string.
        :type username:       str
        :param password_file: The password_file string.
        :type password_file:  str
        :param host:          The host string.
        :type host:           str
        :returns:             Username and password.
        :rtype:               tuple
        :raises Exception:    if password file does not exist,
                              if password was not found.
        """ 
        
        self.set_username(username)
        self.set_password_file(password_file)
        self.set_host(host)
        self.set_password(get_password_from_file(server   = self._host,
                                                 user     = self._username,
                                                 passFile = self._password_file
                                                )
                         )
        return (self.get_username(), self.get_password())
            
    def from_dict(authentication_dict: Any):
        
        """
        Create a Basic authentication object from a dictionary.
        
        :param authentication_dict: A dictionary that contains the keys of a Basic object.
        :type authentication_dict:  Any             
        :rtype:                     ibmpairs.authentication.Basic
        :raises Exception:          if not a dictionary.
        """
        
        username = None
        password = None
        password_file = None
        host = None
        
        common.check_dict(authentication_dict)
        if "host" in authentication_dict:
            host = common.check_str(authentication_dict.get("host"))
        if "username" in authentication_dict:
            username = common.check_str(authentication_dict.get("username"))
        if "password" in authentication_dict:
            password = common.check_str(authentication_dict.get("password"))
        if "password_file" in authentication_dict:
            password_file = common.check_str(authentication_dict.get("password_file"))
            
        return Basic(host          = host,
                     username      = username,
                     password      = password,
                     password_file = password_file
                    )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.  
            
        :rtype: dict
        """
        
        authentication_dict: dict = {}
        if self._host is not None:
            authentication_dict["host"] = self._host
        if self._username is not None:
            authentication_dict["username"] = self._username
        if self._password is not None:
            authentication_dict["password"] = self._password
        if self._password_file is not None:
            authentication_dict["password_file"] = self._password_file
        return authentication_dict
    
    #
    def from_json(basic_json: Any):

        """
        Create an Basic object from json (dictonary or str).
        
        :param basic_dict: A json dictionary that contains the keys of an Basic or a string representation of a json dictionary.
        :type basic_dict:  Any             
        :rtype:            ibmpairs.authentication.Basic
        :raises Exception: if not a dictionary or a string.
        """

        if isinstance(basic_json, dict):
            basic = Basic.from_dict(basic_json)
        elif isinstance(basic_json, str):
            basic_dict = json.loads(basic_json)
            basic = Basic.from_dict(basic_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(basic_json), "basic_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return basic
    
    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure.   
           
        :rtype: string
        """

        return json.dumps(self.to_dict())
        
#fold: OAuth2Return Class {{{
class OAuth2Return:
    #_access_token: str
    #_expires_in: int
    #_token_type: str
    #_refresh_token: str
    #_scope: str
    #_error: str
    
    """
    An object to represent the return provided by a Phoenix OAuth2 call.

    :param access_token:     An access_token (JWT)
    :type access_token:      str
    :param expires_in:       An expiration time (seconds)
    :type expires_in:        int
    :param token_type:       The token type
    :type token_type:        str
    :param refresh_token:    A refresh token
    :type refresh_token:     str
    :param scope:            The scope of the token
    :type scope:             str
    :param error:            An error message
    :type error:             str
    :raises Exception:       if username and password are not present
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns: A string representation of the internal class structure.
        :rtype:   str
        """
        
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
        
    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns: A dict representation of the internal class structure.
        :rtype:   dict
        """
      
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
    
    def __init__(self,
                 access_token: str  = None,
                 expires_in: int    = None,
                 token_type: str    = None,
                 refresh_token: str = None,
                 scope: str         = None,
                 error: str         = None
                ):
        self._access_token  = access_token
        self._expires_in    = expires_in
        self._token_type    = token_type
        self._refresh_token = refresh_token
        self._scope         = scope
        self._error         = error
        
    #
    def get_access_token(self):
        return self._access_token

    #
    def set_access_token(self, access_token):
        self._access_token = common.check_str(access_token)
        
    #    
    def del_access_token(self): 
        del self._access_token

    #    
    access_token = property(get_access_token, set_access_token, del_access_token)
    
    #
    def get_expires_in(self):
        return self._expires_in

    #
    def set_expires_in(self, expires_in):
        self._expires_in = common.check_int(expires_in)
        
    #    
    def del_expires_in(self): 
        del self._expires_in

    #    
    expires_in = property(get_expires_in, set_expires_in, del_expires_in)
    
    #
    def get_token_type(self):
        return self._token_type

    #
    def set_token_type(self, token_type):
        self._token_type = common.check_str(token_type)
        
    #    
    def del_token_type(self): 
        del self._token_type

    #    
    token_type = property(get_token_type, set_token_type, del_token_type)
    
    #
    def get_refresh_token(self):
        return self._refresh_token

    #
    def set_refresh_token(self, refresh_token):
        self._refresh_token = common.check_str(refresh_token)
        
    #    
    def del_refresh_token(self): 
        del self._refresh_token

    #    
    refresh_token = property(get_refresh_token, set_refresh_token, del_refresh_token)
    
    #
    def get_scope(self):
        return self._scope

    #
    def set_scope(self, scope):
        self._scope = common.check_str(scope)
        
    #    
    def del_scope(self): 
        del self._scope

    #    
    scope = property(get_scope, set_scope, del_scope)
    
    #
    def get_error(self):
        return self._error

    #
    def set_error(self, error):
        self._error = common.check_str(error)
        
    #    
    def del_error(self): 
        del self._error

    #    
    error = property(get_error, set_error, del_error)
    
    #
    def from_dict(oauth2_return_dict: Any):
        
        """
        Create an OAuth2Return object from a dictionary.
        
        :param oauth2_return_dict: A dictionary that contains the keys of an OAuth2Return object.
        :type oauth2_return_dict:  Any             
        :rtype:                    ibmpairs.authentication.OAuth2Return
        :raises Exception:         if not a dictionary.
        """
        
        access_token  = None
        expires_in    = None
        token_type    = None
        refresh_token = None
        scope         = None
        error         = None
        
        common.check_dict(oauth2_return_dict)
        if "access_token" in oauth2_return_dict:
            if oauth2_return_dict.get("access_token") is not None:
                access_token = common.check_str(oauth2_return_dict.get("access_token"))
        if "expires_in" in oauth2_return_dict:
            if oauth2_return_dict.get("expires_in") is not None:
                expires_in = common.check_int(oauth2_return_dict.get("expires_in"))
        if "token_type" in oauth2_return_dict:
            if oauth2_return_dict.get("token_type") is not None:
                token_type = common.check_str(oauth2_return_dict.get("token_type"))
        if "refresh_token" in oauth2_return_dict:
            if oauth2_return_dict.get("refresh_token") is not None:
                refresh_token = common.check_str(oauth2_return_dict.get("refresh_token"))
        if "scope" in oauth2_return_dict:
            if oauth2_return_dict.get("scope") is not None:
                scope = common.check_str(oauth2_return_dict.get("scope"))
        if "error" in oauth2_return_dict:
            if oauth2_return_dict.get("error") is not None:
                error = common.check_str(oauth2_return_dict.get("error"))
            
        return OAuth2Return(access_token  = access_token,
                            expires_in    = expires_in,
                            token_type    = token_type,
                            refresh_token = refresh_token,
                            scope         = scope,
                            error         = error
                           )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure. 
                   
        :rtype: dict
        """
        
        oauth2_return_dict: dict = {}
        if self._access_token is not None:
            oauth2_return_dict["access_token"] = self._access_token
        if self._expires_in is not None:
            oauth2_return_dict["expires_in"] = self._expires_in
        if self._token_type is not None:
            oauth2_return_dict["token_type"] = self._token_type
        if self._refresh_token is not None:
            oauth2_return_dict["refresh_token"] = self._refresh_token
        if self._scope is not None:
            oauth2_return_dict["scope"] = self._scope
        if self._error is not None:
            oauth2_return_dict["error"] = self._error
        return oauth2_return_dict
        
    #
    def from_json(oauth2_return_json: Any):

        """
        Create an OAuth2Return object from json (dictonary or str).
        
        :param oauth2_return_dict: A json dictionary that contains the keys of an OAuth2Return or a string representation of a json dictionary.
        :type oauth2_return_dict:  Any             
        :rtype:                    ibmpairs.authentication.OAuth2Return
        :raises Exception:         if not a dictionary or a string.
        """

        if isinstance(oauth2_return_json, dict):
            oauth2_return = OAuth2Return.from_dict(oauth2_return_json)
        elif isinstance(oauth2_return_json, str):
            oauth2_return_dict = json.loads(oauth2_return_json)
            oauth2_return = OAuth2Return.from_dict(oauth2_return_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(oauth2_return_json), "oauth2_return_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return oauth2_return
        
    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype:                     string
        """

        return json.dumps(self.to_dict())
#}}}

#fold: OAuth2 Class {{{
class OAuth2(object):
    #_host: str
    #_username: str
    #_api_key: str
    #_api_key_file: str
    #_client_id: str
    #_endpoint: str
    #_jwt_token: str
    
    #_oauth2_return: OAuth2Return
    
    """
    An object to represent OAuth2 credentials and recovery from a file.
    
    :param host:         IBM PAIRS host, defaults to https://pairs.res.ibm.com
    :type host:          str
    :param username:     IBM PAIRS username
    :type username:      str
    :param api_key:      IBM PAIRS API key
    :type api_key:       str
    :param api_key_file: IBM PAIRS API key file, defaults to auth/oauth2.txt
    :type api_key_file:  str
    :param client_id:    A client id for the authentication system, defaults to 'ibm-pairs'.
    :type client_id:     str
    :param endpoint:     The authentication endpoint.
    :type endpoint:      str
    :param jwt_token:    A jwt token for authentication.
    :type jwt_token:     str
    :returns:            None
    :rtype:              None
    :raises Exception:   if an api key cannot be acquired from the information provided
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        elif ("apiKey" in return_dict):
            return_dict["apiKey"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return_dict = self.to_dict()
        
        if ("api_key" in return_dict):
            return_dict["api_key"] = "********"
        elif ("apiKey" in return_dict):
            return_dict["apiKey"] = "********"
        
        return json.dumps(return_dict, 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __init__(self,
                 host: str         = constants.CLIENT_PAIRS_URL,
                 username: str     = None,
                 api_key: str      = None,
                 api_key_file: str = "auth/oauth2.txt",
                 client_id: str    = "ibm-pairs",
                 endpoint: str     = "auth-b2b-twc.ibm.com",
                 jwt_token: str    = None,
                ):

        self._host          = common.strip_protocol(host)
        self._username      = username
        self._api_key       = api_key
        self._api_key_file  = api_key_file
        self._client_id     = client_id
        self._endpoint      = endpoint
        self._jwt_token     = jwt_token
        
        self._oauth2_return = OAuth2Return()
        
        if ((self._api_key is None) and (self._username is not None)):
            try:
                self.set_credentials_from_file(self._username,
                                               self._api_key_file, 
                                               self._host
                                              )
            except:
                msg = messages.INFO_AUTHENTICATION_API_KEY_NOT_FOUND_IN_FILE.format(self._username, self._api_key_file, self._host)
                logger.info(msg)
        
        if (self._api_key is not None):
            try:
                self.get_auth_token(api_key   = self._api_key,
                                    client_id = self._client_id, 
                                    endpoint  = self._endpoint
                                   )
            except Exception as ex:
                msg = messages.INFO_AUTHENTICATION_COULD_NOT_GET_AUTH_TOKEN.format(api_key, ex)
                logger.info(msg)
                
        if self._jwt_token is None:
            msg = messages.ERROR_AUTHENTICATION_FAILED.format("JWT token")
            logger.error(msg)
            raise common.PAWException(msg)

    #
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.check_str(common.strip_protocol(host))
        
    #    
    def del_host(self): 
        del self._host

    #    
    host = property(get_host, set_host, del_host)

    #
    def get_username(self):
        return self._username
    
    #
    def set_username(self, username):
        self._username = common.check_str(username)
        
    #    
    def del_username(self): 
        del self._username

    #    
    username = property(get_username, set_username, del_username)
    
    #
    def get_api_key(self):
        return self._api_key

    #
    def set_api_key(self, api_key):
        self._api_key = common.check_str(api_key)
        
    #    
    def del_api_key(self): 
        del self._api_key

    #    
    api_key = property(get_api_key, set_api_key, del_api_key)
    
    #
    def get_api_key_file(self):
        return self._api_key_file

    #
    def set_api_key_file(self, api_key_file):
        
        if os.path.isfile(os.path.join(os.getcwd(), api_key_file)):
            self._api_key_file = os.path.join(os.getcwd(), api_key_file)
        elif os.path.isfile(api_key_file):
            self._api_key_file = common.check_str(api_key_file)
        else:
            msg = messages.ERROR_AUTHENTICATION_COULD_NOT_FIND_API_KEY_FILE.format(api_key_file)
            logger.info(msg)
            raise common.PAWException(msg)
        
    #    
    def del_api_key_file(self): 
        del self._api_key_file

    #    
    api_key_file = property(get_api_key_file, set_api_key_file, del_api_key_file)
    
    #
    def get_client_id(self):
        return self._client_id

    #
    def set_client_id(self, client_id):
        self._client_id = common.check_str(client_id)
        
    #    
    def del_client_id(self): 
        del self._client_id

    #    
    client_id = property(get_client_id, set_client_id, del_client_id)
    
    #
    def get_endpoint(self):
        return self._endpoint

    #
    def set_endpoint(self, endpoint):
        self._endpoint = common.check_str(endpoint)
        
    #    
    def del_endpoint(self): 
        del self._endpoint

    #    
    endpoint = property(get_endpoint, set_endpoint, del_endpoint)
    
    #
    def get_jwt_token(self):
        return self._jwt_token

    #
    def set_jwt_token(self, jwt_token):
        self._jwt_token = common.check_str(jwt_token)
        
    #    
    def del_jwt_token(self): 
        del self._jwt_token

    #    
    jwt_token = property(get_jwt_token, set_jwt_token, del_jwt_token) 
    
    #
    def get_oauth2_return(self):
        return self._oauth2_return

    #
    def set_oauth2_return(self, oauth2_return):
        self._oauth2_return = common.check_class(oauth2_return, OAuth2Return)
        
    #    
    def del_oauth2_return(self): 
        del self._oauth2_return

    #    
    oauth2_return = property(get_oauth2_return, set_oauth2_return, del_oauth2_return) 
    
    #
    def set_credentials_from_file(self, 
                                  username, 
                                  api_key_file, 
                                  host
                                 ):
        
        """
        The method sets the username, api_key_file, host and a resulting api_key.
        
        :param username:     A username for the user.
        :type username:      str
        :param api_key_file: An file which stores the api key.
        :type api_key_file:  str
        :param host:         The host to execute requests against.
        :type host:          str
        """
        
        self.set_username(username)
        self.set_api_key_file(api_key_file)
        self.set_host(host)
        self.set_api_key(get_password_from_file(server   = self._host,
                                                user     = self._username,
                                                passFile = self._api_key_file
                                               )
                        )
    
    #
    def get_auth_token(self, 
                       api_key   = None, 
                       client_id = None, 
                       endpoint  = None,
                       verify    = constants.GLOBAL_SSL_VERIFY
                      ):
        
        """
        The method submits a request to the authentication system and obtains a response.
        
        :param api_key:   An api key for the authentication system.
        :type api_key:    str
        :param client_id: A client id for the authentication system.
        :type client_id:  str
        :param endpoint:  The authentication endpoint.
        :type endpoint:   str
        """
        
        response               = None
        response_oauth2_return = None
        
        if api_key is not None:
            self.set_api_key(api_key)
        if client_id is not None:
            self.set_client_id(client_id)
        if endpoint is not None:
            self.set_endpoint(endpoint)

        if (self._api_key is not None) and (self._client_id is not None):
            
            phoenix_request_headers: dict             = {}
            phoenix_request_headers["Content-Type"]   = "application/json"
            phoenix_request_headers["Cache-Control"]  = "no-cache"

            phoenix_request_body: dict               = {}
            phoenix_request_body["apiKey"]           = self.get_api_key()
            phoenix_request_body["clientId"]         = self.get_client_id()

            body = json.dumps(phoenix_request_body)

            response = requests.post("https://" + 
                                         self.get_endpoint() +
                                         "/Auth/GetBearerForClient",
                                     headers = phoenix_request_headers,
                                     data    = body,
                                     verify  = verify
                                    )
        else:
            msg = messages.ERROR_AUTHENTICATION_NO_API_KEY_OR_CLIENT_ID
            logger.error(msg)
            raise common.PAWException(msg)
            
        if response.status_code == 200:
            try:
                response_oauth2_return = oauth2_return_from_dict(response.json())
            except Exception as ex:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_RETURN_NOT_OAUTH2RETURN.format("Phoenix GetBearerForClient", response.json(), ex)
                logger.error(msg)
                raise common.PAWException(msg)
            
            if response_oauth2_return.error is None:
                self.set_jwt_token(response_oauth2_return.access_token)
                self.set_oauth2_return(response_oauth2_return)
            else:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_200_RETURN_ERROR.format("Phoenix GetBearerForClient", response_oauth2_return.error)
                logger.error(msg)
                raise common.PAWException(msg)
                
        else:
            msg = messages.ERROR_AUTHENTICATION_PHOENIX_NOT_SUCCESSFUL.format("Phoenix GetBearerForClient", str(response))
            logger.error(msg)
            raise common.PAWException(msg)

    def refresh_auth_token(self,
                           verify    = constants.GLOBAL_SSL_VERIFY
                          ):
        
        """
        The method submits a request to the authentication system for a refreshed token, gets a response and updates the internal self._oauth2_return and self._jwt_token objects.
        """
        
        msg = messages.INFO_AUTHENTICATION_TOKEN_REFRESH
        logger.info(msg)
        
        response               = None
        response_oauth2_return = None

        if (self._oauth2_return is not None) and (self._oauth2_return._refresh_token is not None) and (self._client_id is not None):
            
            phoenix_request_headers: dict             = {}
            phoenix_request_headers["Content-Type"]   = "application/x-www-form-urlencoded"
            phoenix_request_headers["Cache-Control"]  = "no-cache"

            phoenix_request_body = "grant_type=refresh_token" + \
                                   "&client_id=" + self.get_client_id() + \
                                   "&refresh_token=" + self.oauth2_return.get_refresh_token()

            response = requests.post("https://" + 
                                         self.get_endpoint() +
                                         "/connect/token",
                                     headers = phoenix_request_headers,
                                     data    = phoenix_request_body,
                                     verify  = verify
                                    )
        else:
            msg = messages.ERROR_AUTHENTICATION_NO_REFRESH_TOKEN_OR_CLIENT_ID
            logger.error(msg)
            raise common.PAWException(msg)
            
        if response.status_code == 200:
            try:
                response_oauth2_return = oauth2_return_from_dict(response.json())
            except:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_RETURN_NOT_OAUTH2RETURN.format("/connect/token", response.json())
                logger.error(msg)
                raise common.PAWException(msg)
            
            if response_oauth2_return.error is None:
                self.set_jwt_token(response_oauth2_return.access_token)
                self.set_oauth2_return(response_oauth2_return)
                msg = messages.INFO_AUTHENTICATION_TOKEN_REFRESH_SUCCESS
                logger.info(msg)
            else:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_REFRESH_200_RETURN_ERROR.format("/connect/token", response_oauth2_return.error)
                logger.error(msg)
                raise common.PAWException(msg)
                
        else:
            msg = messages.ERROR_AUTHENTICATION_PHOENIX_NOT_SUCCESSFUL.format("/connect/token", str(response))
            logger.error(msg)
            raise common.PAWException(msg)
    
    #
    def from_dict(authentication_dict: Any):
        
        """
        Create a OAuth2 authentication object from a dictionary.
        
        :param authentication_dict: A dictionary that contains the keys of a OAuth2 object.
        :type authentication_dict:  Any             
        :rtype:                     ibmpairs.authentication.OAuth2
        :raises Exception:          if not a dictionary.
        """
        
        host         = None
        username     = None
        api_key      = None
        api_key_file = None
        client_id    = None
        endpoint     = None
        jwt_token    = None
        
        common.check_dict(authentication_dict)
        if "host" in authentication_dict:
            if authentication_dict.get("host") is not None:
                host = common.check_str(authentication_dict.get("host"))
        if "username" in authentication_dict:
            if authentication_dict.get("username") is not None:
                username = common.check_str(authentication_dict.get("username"))
        if "api_key" in authentication_dict:
            if authentication_dict.get("api_key") is not None:
                api_key = common.check_str(authentication_dict.get("api_key"))
        if "api_key_file" in authentication_dict:
            if authentication_dict.get("api_key_file") is not None:
                api_key_file = common.check_str(authentication_dict.get("api_key_file"))
        if "client_id" in authentication_dict:
            if authentication_dict.get("client_id") is not None:
                client_id = common.check_str(authentication_dict.get("client_id"))
        if "endpoint" in authentication_dict:
            if authentication_dict.get("endpoint") is not None:
                endpoint = common.check_str(authentication_dict.get("endpoint"))
        if "jwt_token" in authentication_dict:
            if authentication_dict.get("jwt_token") is not None:
                jwt_token = common.check_str(authentication_dict.get("jwt_token"))
            
        return OAuth2(host,
                      username,
                      api_key,
                      api_key_file,
                      client_id,
                      endpoint,
                      jwt_token
                     )

    #
    def to_dict(self):
      
        """
        Create a dictionary from the objects structure.  
                  
        :rtype: dict
        """
        
        authentication_dict: dict = {}
        if self._host is not None:
            authentication_dict["host"] = self._host
        if self._username is not None:
            authentication_dict["username"] = self._username
        if self._api_key is not None:
            authentication_dict["api_key"] = self._api_key
        if self._api_key_file is not None:
            authentication_dict["api_key_file"] = self._api_key_file
        if self._client_id is not None:
            authentication_dict["client_id"] = self._client_id
        if self._endpoint is not None:
            authentication_dict["endpoint"] = self._endpoint
        if self._jwt_token is not None:
            authentication_dict["jwt_token"] = self._jwt_token
        if self._oauth2_return is not None:
            authentication_dict["oauth2_return"] = common.class_to_dict(self._oauth2_return, OAuth2Return)
        return authentication_dict
    
    #
    def from_json(oauth2_json: Any):

        """
        Create an OAuth2 object from json (dictonary or str).
        
        :param oauth2_dict: A json dictionary that contains the keys of an OAuth2 or a string representation of a json dictionary.
        :type oauth2_dict:  Any             
        :rtype:             ibmpairs.authentication.OAuth2
        :raises Exception:  if not a dictionary or a string.
        """

        if isinstance(oauth2_json, dict):
            oauth2 = OAuth2.from_dict(oauth2_json)
        elif isinstance(oauth2_json, str):
            oauth2_dict = json.loads(oauth2_json)
            oauth2 = OAuth2.from_dict(oauth2_dict)
        else:
            msg = messages.ERROR_FROM_JSON_TYPE_NOT_RECOGNIZED.format(type(oauth2_json), "oauth2_json")
            logger.error(msg)
            raise common.PAWException(msg)
        return oauth2
    
    #
    def to_json(self):

        """
        Create a string representation of a json dictionary from the objects structure. 
                   
        :rtype: string
        """

        return json.dumps(self.to_dict())
    
#}}}

# fold: Common Functions {{{
def get_password_from_file(server, 
                           user,
                           passFile=None):
    """
    Tries to obtain the PAIRS API password for a given user on a given server.

    :param server:      PAIRS API server name, e.g. 'pairs.res.ibm.com'
    :type server:       str
    :param user:        user name for which to obtain the corresponding password
    :type user:         str
    :param passFile:    path to file with password, it is expected to have the format
                        `<server>:<user>:<password>`, colons in passwords need to be escaped
    :type passFile:     str
    :returns:           corresponding password if available, `None` otherwise
                        *note*: if either user or server is `None`, no password searched
                        for, and `None` is returned
    :rtype:             str
    :raises Exception:  if password file does not exist
                        if password was not found
    """
    
    # of either no user or server is provided
    if server is None or user is None:
        return None
    # Search for a password file in (a) the current working directory and (b) $HOME
    if passFile is None:
        if os.path.isfile(os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        elif os.path.isfile(os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        else:
            raise ValueError(
                "passFile = None requires existence of a '{}' file in a default location.".format(
                    PAIRS_DEFAULT_PASSWORD_FILE_NAME
                )
            )

    # Often the value to server is the same as some global variable PAIRS_SERVER
    # That however if later handed to PAIRSQuery objects. The following code allows
    # using PAIRS_SERVER='https://pairs.res.ibm.com' and avoids later use of
    # 'https://'+PAIRS_SERVER
    if server.startswith('https://'):
        server = server[8:]
    if server.startswith('http://'):
        server = server[7:]

    if ":" in server:
        server = server.split(":")[0]

    passFound = False
    try:
    # parse PAIRS API access password file
        with open(passFile) as f:
            for line in f:
                if not re.match(PAIRS_PASSWORD_FILE_COMMENT_REG_EX, line):
                    serverF, userF, password  = re.split(r'(?<!\\):',line.strip())
                    password = password.replace(r'\:', ':')
                    if server == serverF and user == userF:
                        passFound = True
                        break
    except EnvironmentError as e:
        raise e
    except Exception as e:
        raise ValueError('Failed loading PAIRS password from {0}'.format(passFile))

    # return password (if any)
    if passFound:
        return password
    else:
        raise ValueError('Unable to find line starting with {0}:{1} in {2}.'.format(server, user, passFile))

#}}}

#
def basic_from_dict(basic_dictionary: dict):
  """
  The function converts a dictionary of Basic to a Basic object.
  
  :param basic_dict: A dictionary that contains the keys of a Basic.
  :type basic_dict:  dict             
  :rtype:            ibmpairs.authentication.Basic
  :raises Exception: if not a dict.
  """
  basic = Basic.from_dict(basic_dictionary)
    
  return basic

#
def basic_to_dict(basic: Basic):
  """
  The function converts an object of Basic to a dict.
  
  :param basic: A Basic object.
  :type basic:  ibmpairs.authentication.Basic             
  :rtype:       dict
  """
  return Basic.to_dict(basic)

#
def basic_from_json(basic_json: Any):
  """
  The function converts a dictionary or json string of Basic to a Basic object.
  
  :param basic_json: A dictionary or json string that contains the keys of a Basic.
  :type basic_json:  Any             
  :rtype:            ibmpairs.authentication.Basic
  :raises Exception: if not a dict or a str.
  """
  basic = Basic.from_json(basic_json)
  return basic

#
def basic_to_json(basic: Basic):
  """
  The function converts an object of Basic to a json string.
  
  :param basic: A Basic object.
  :type basic:  ibmpairs.authentication.Basic             
  :rtype:       str
  """
  return Basic.to_json(basic)

#
def oauth2_return_from_dict(oauth2_return_dictionary: dict):
  """
  The function converts a dictionary of OAuth2Return to a OAuth2Return object.
  
  :param oauth2_return_dict: A dictionary that contains the keys of a OAuth2Return.
  :type oauth2_return_dict:  dict             
  :rtype:                    ibmpairs.authentication.OAuth2Return
  :raises Exception:         if not a dict.
  """
  oauth2_return = OAuth2Return.from_dict(oauth2_return_dictionary)
    
  return oauth2_return

#
def oauth2_return_to_dict(oauth2_return: OAuth2Return):
  """
  The function converts an object of OAuth2Return to a dict.
  
  :param oauth2_return: A OAuth2Return object.
  :type oauth2_return:  ibmpairs.authentication.OAuth2Return             
  :rtype:               dict
  """
  return OAuth2Return.to_dict(oauth2_return)

#
def oauth2_return_from_json(oauth2_return_json: Any):
  """
  The function converts a dictionary or json string of OAuth2Return to a OAuth2Return object.
  
  :param oauth2_return_json: A dictionary or json string that contains the keys of a OAuth2Return.
  :type oauth2_return_json:  Any             
  :rtype:                    ibmpairs.authentication.OAuth2Return
  :raises Exception:         if not a dict or a str.
  """
  oauth2_return = OAuth2Return.from_json(oauth2_return_json)
  return oauth2_return

#
def oauth2_return_to_json(oauth2_return: OAuth2Return):
  """
  The function converts an object of OAuth2Return to a json string.
  
  :param oauth2_return: A OAuth2Return object.
  :type oauth2_return:  ibmpairs.authentication.OAuth2Return             
  :rtype:               str
  """
  return OAuth2Return.to_json(oauth2_return)

#
def oauth2_from_dict(oauth2_dictionary: dict):
  """
  The function converts a dictionary of OAuth2 to a OAuth2 object.
  
  :param oauth2_dict: A dictionary that contains the keys of a OAuth2.
  :type oauth2_dict:  dict             
  :rtype:             ibmpairs.authentication.OAuth2
  :raises Exception:  if not a dict.
  """
  oauth2 = OAuth2.from_dict(oauth2_dictionary)
    
  return oauth2

#
def oauth2_to_dict(oauth2: OAuth2):
  """
  The function converts an object of OAuth2 to a dict.
  
  :param oauth2: A OAuth2 object.
  :type oauth2:  ibmpairs.authentication.OAuth2             
  :rtype:        dict
  """
  return OAuth2.to_dict(oauth2)

#
def oauth2_from_json(oauth2_json: Any):
  """
  The function converts a dictionary or json string of OAuth2 to a OAuth2 object.
  
  :param oauth2_json: A dictionary or json string that contains the keys of a OAuth2.
  :type oauth2_json:  Any             
  :rtype:             ibmpairs.authentication.OAuth2
  :raises Exception:  if not a dict or a str.
  """
  oauth2 = OAuth2.from_json(oauth2_json)
  return oauth2

#
def oauth2_to_json(oauth2: OAuth2):
  """
  The function converts an object of OAuth2 to a json string.
  
  :param oauth2: A OAuth2 object.
  :type oauth2:  ibmpairs.authentication.OAuth2             
  :rtype:        str
  """
  return OAuth2.to_json(oauth2)