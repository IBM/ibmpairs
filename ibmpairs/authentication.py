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
import ibmpairs.common as common
from ibmpairs.logger import logger
import ibmpairs.messages as messages
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import requests
#}}}

# fold: String Literals {{{
PAIRS_DEFAULT_PASSWORD_FILE_NAME    = u'ibmpairspass.txt'
PAIRS_PASSWORD_FILE_COMMENT_REG_EX  = re.compile(r'^\s*#')
#}}}

#fold: OAuth2Return Class {{{
class OAuth2Return:
    _access_token: str
    _expires_in: int
    _token_type: str
    _refresh_token: str
    _scope: str
    _error: str
    
    #
    def __str__(self):
        
        '''
        The method creates a string representation of the internal class structure.
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        '''
        
        return json.dumps(self.to_dict())

    #
    def __repr__(self):
        
        '''
        The method creates a dict representation of the internal class structure.
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        '''
        
        return json.dumps(self.to_dict())
    
    def __init__(self,
                 access_token: str  = None,
                 expires_in: int    = None,
                 token_type: str    = None,
                 refresh_token: str = None,
                 scope: str         = None,
                 error: str         = None
                ) -> None:
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
    def from_dict(authentication_dict: Any):
        access_token  = None
        expires_in    = None
        token_type    = None
        refresh_token = None
        scope         = None
        error         = None
        
        common.check_dict(authentication_dict)
        if "access_token" in authentication_dict:
            if authentication_dict.get("access_token") is not None:
                access_token = common.check_str(authentication_dict.get("access_token"))
        if "expires_in" in authentication_dict:
            if authentication_dict.get("expires_in") is not None:
                expires_in = common.check_int(authentication_dict.get("expires_in"))
        if "token_type" in authentication_dict:
            if authentication_dict.get("token_type") is not None:
                token_type = common.check_str(authentication_dict.get("token_type"))
        if "refresh_token" in authentication_dict:
            if authentication_dict.get("refresh_token") is not None:
                refresh_token = common.check_str(authentication_dict.get("refresh_token"))
        if "scope" in authentication_dict:
            if authentication_dict.get("scope") is not None:
                scope = common.check_str(authentication_dict.get("scope"))
        if "error" in authentication_dict:
            if authentication_dict.get("error") is not None:
                error = common.check_str(authentication_dict.get("error"))
            
        return OAuth2Return(access_token,
                            expires_in,
                            token_type,
                            refresh_token,
                            scope,
                            error
                           )

    #
    def to_dict(self):
        authentication_dict: dict = {}
        if self._access_token is not None:
            authentication_dict["access_token"] = self._access_token
        if self._expires_in is not None:
            authentication_dict["expires_in"] = self._expires_in
        if self._token_type is not None:
            authentication_dict["token_type"] = self._token_type
        if self._refresh_token is not None:
            authentication_dict["refresh_token"] = self._refresh_token
        if self._scope is not None:
            authentication_dict["scope"] = self._scope
        if self._error is not None:
            authentication_dict["error"] = self._error
        return authentication_dict
#}}}

#fold: OAuth2 Class {{{
class OAuth2(object):
    _host: str
    _username: str
    _api_key: str
    _api_key_file: str
    _client_id: str
    _endpoint: str
    _jwt_token: str
    
    _oauth2_return: OAuth2Return
    
    #
    def __str__(self):
        
        '''
        The method creates a string representation of the internal class structure.
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        '''
        
        return json.dumps(self.to_dict())

    #
    def __repr__(self):
        
        '''
        The method creates a dict representation of the internal class structure.
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        '''
        
        return json.dumps(self.to_dict())
    
    
    #
    def __init__(self,
                 host: str         = 'pairs.res.ibm.com',
                 username: str     = None,
                 api_key: str      = None,
                 api_key_file: str = "ibmpairspass.txt",
                 client_id: str    = "ibm-pairs",
                 endpoint: str     = "auth-b2b-twc.ibm.com",
                 jwt_token: str    = None
                ) -> None:
                    
        '''
        The method initializes the instance of the class.
        :param host:         The host to execute requests against.
        :type host:          str
        :param username:     A username for the user.
        :type username:      str
        :param api_key:      An api key for the user.
        :type api_key:       str
        :param api_key_file: An file which stores the api key.
        :type api_key_file:  str
        :param client_id:    A client id for the authentication system.
        :type client_id:     str
        :param endpoint:     The authentication endpoint.
        :type endpoint:      str
        :param jwt_token:    A jwt token for authentication.
        :type jwt_token:     str
        :returns:            None
        :rtype:              None
        '''
                    
        self._host          = host
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
                msg = messages.INFO_AUTHENTICATION_API_KEY_NOT_FOUND_IN_FILE.format(username, api_key_file, host)
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
    
    #
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.check_str(host)
        
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
        
        '''
        The method sets the username, api_key_file, host and a resulting api_key.
        :param username:     A username for the user.
        :type username:      str
        :param api_key_file: An file which stores the api key.
        :type api_key_file:  str
        :param host:         The host to execute requests against.
        :type host:          str
        :returns:            None
        :rtype:              None
        '''
        
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
                       api_key = None, 
                       client_id = None, 
                       endpoint = None
                      ):
        
        '''
        The method submits a request to the authentication system and obtains a response.
        :param api_key:      An api key for the authentication system.
        :type api_key:       str
        :param client_id:    A client id for the authentication system.
        :type client_id:     str
        :param endpoint:     The authentication endpoint.
        :type endpoint:      str
        :returns:            None
        :rtype:              None
        '''
        
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
            phoenix_request_body_json = json.dumps(phoenix_request_body)

            response = requests.post("https://"+
                                     self.get_endpoint()+
                                     "/Auth/GetBearerForClient",
                                     headers = phoenix_request_headers,
                                     data = phoenix_request_body_json
                                    )
                            
        else:
            msg = messages.ERROR_AUTHENTICATION_NO_API_KEY_OR_CLIENT_ID
            logger.error(msg)
            raise common.PAWException(msg)
            
        if response.status_code == 200:
            try:
                response_oauth2_return = oauth2_return_from_dict(response.json())
            except Exception as ex:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_RETURN_NOT_OAUTH2RETURN.format(response.json(), ex)
                logger.error(msg)
                raise common.PAWException(msg)
            
            if response_oauth2_return.error is None:
                self.set_jwt_token(response_oauth2_return.access_token)
                self.set_oauth2_return(response_oauth2_return)
            else:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_200_RETURN_ERROR.format(response_oauth2_return.error)
                logger.error(msg)
                raise common.PAWException(msg)
                
        else:
            msg = messages.ERROR_AUTHENTICATION_PHOENIX_NOT_SUCCESSFUL.format(str(response))
            logger.error(msg)
            raise common.PAWException(msg)

    def refresh_auth_token(self):
        
        '''
        The method submits a request to the authentication system for a refreshed token, gets a 
        response and updates the internal self._oauth2_return and self._jwt_token objects.
        :returns:            None
        :rtype:              None
        '''
        
        response               = None
        response_oauth2_return = None

        if (self._oauth2_return is not None) and (self._oauth2_return._refresh_token is not None) and (self._client_id is not None):

            phoenix_request_headers: dict             = {}
            phoenix_request_headers["Content-Type"]   = "application/x-www-form-urlencoded"
            phoenix_request_headers["Cache-Control"]  = "no-cache"

            phoenix_request_body: dict               = {}
            phoenix_request_body["grant_type"]       = "refresh_token"
            phoenix_request_body["client_id"]        = self.get_client_id()
            phoenix_request_body["refresh_token"]    = self.oauth2_return.get_refresh_token()

            response = requests.post("https://"+
                                     self.get_endpoint()+
                                     "/connect/token",
                                     headers = phoenix_request_headers,
                                     data = phoenix_request_body
                                    )
            
        else:
            msg = messages.ERROR_AUTHENTICATION_NO_REFRESH_TOKEN_OR_CLIENT_ID
            logger.error(msg)
            raise common.PAWException(msg)
            
        if response.status_code == 200:
            try:
                response_oauth2_return = oauth2_return_from_dict(response.json())
            except:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_RETURN_NOT_OAUTH2RETURN.format(response.json())
                logger.error(msg)
                raise common.PAWException(msg)
            
            if response_oauth2_return.error is None:
                self.set_jwt_token(response_oauth2_return.access_token)
                self.set_oauth2_return(response_oauth2_return)
            else:
                msg = messages.ERROR_AUTHENTICATION_PHOENIX_REFRESH_200_RETURN_ERROR.format(response_oauth2_return.error)
                logger.error(msg)
                raise common.PAWException(msg)
                
        else:
            msg = messages.ERROR_AUTHENTICATION_PHOENIX_NOT_SUCCESSFUL.format(str(response))
            logger.error(msg)
            raise common.PAWException(msg)
    
    #
    def from_dict(authentication_dict: Any):
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
#}}}

# fold: Common Functions {{{
def get_password_from_file(server, 
                           user,
                           passFile=None):
    '''
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
    '''
    
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

# fold: OAuth2 Authentication Help Methods {{{
#
def oauth2_authentication_from_dict(d: OAuth2):
    return OAuth2.from_dict(d)

#
def oauth2_authentication_to_dict(b: OAuth2):
    return OAuth2.to_dict(b)

#
def oauth2_authentication_from_json(j: Any):
    d = json.loads(j)
    o = oauth2_authentication_from_dict(d)
    return o

#
def oauth2_authentication_to_json(o: OAuth2):
    return json.dumps(OAuth2.to_dict(o))

#
def get_oauth2_credentials(api_key = None, 
                           client_id = None, 
                           endpoint = None):
    oauth2 = OAuth2()
    oauth2_return = oauth2.get_auth_token(api_key = api_key, 
                                          client_id = client_id, 
                                          endpoint = endpoint
                                         )
    return oauth2
#}}}

# fold: OAuth2 Return Help Methods {{{
#
def oauth2_return_from_dict(d: OAuth2Return):
    return OAuth2Return.from_dict(d)

#
def oauth2_return_to_dict(b: OAuth2Return):
    return OAuth2Return.to_dict(b)

#
def oauth2_return_from_json(j: Any):
    d = json.loads(j)
    o = oauth2_return_from_dict(d)
    return o

#
def oauth2_return_to_json(o: OAuth2Return):
    return json.dumps(OAuth2Return.to_dict(o))

#}}}
