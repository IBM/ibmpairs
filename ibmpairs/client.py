"""
Environmental Intelligence: Geospatial APIs SDK (ibmpairs): A Python module to 
wrap the core functionality of the Geospatial APIs component.            

Copyright 2019-2024 IBM Software: Sustainability, IBM Corp. All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
from typing import List, Any
import json
import logging
import os
import warnings
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
import ibmpairs.authentication as authentication
import ibmpairs.common as common
import ibmpairs.messages as messages
import ibmpairs.constants as constants
from ibmpairs.logger import logger
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import requests
from requests.auth import HTTPBasicAuth
import aiohttp
#}}}

GLOBAL_PAIRS_CLIENT = None

GLOBAL_LEGACY_ENVIRONMENT      = os.environ.get('GLOBAL_LEGACY_ENVIRONMENT', "False")
if GLOBAL_LEGACY_ENVIRONMENT.lower() in ('true', 't', 'yes', 'y'):
    GLOBAL_LEGACY_ENVIRONMENT  = True
else:
    GLOBAL_LEGACY_ENVIRONMENT  = False

#
class ClientResponse:
    #_status: int
    #_body: str
    
    """
    A representation of a client response.
    
    :param status:            A response status.
    :type headers:            int
    :param body:              A response body.
    :type body:               str or bytes
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
      
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
      
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
                        
    #
    def __init__(self,
                 status: int = None,
                 body: str   = None
                ) -> None:
            self._status = status
            self._body   = body
            
    #       
    def get_status(self):
        return self._status

    #
    def set_status(self, status):
        self._status = common.check_int(status)
        
    #    
    def del_status(self): 
        del self._status

    #    
    status = property(get_status, set_status, del_status)
            
    #       
    def get_body(self):
        return self._body

    #
    def set_body(self, body):
        if isinstance(body, str):
            self._body = common.check_str(body)
        elif isinstance(body, bytes):
            self._body = body
        
    #    
    def del_body(self): 
        del self._body

    #    
    body = property(get_body, set_body, del_body)
    
    #
    def from_dict(client_response_dict: Any):
        status = None
        body   = None
        
        common.check_dict(client_response_dict)
        if "status" in client_response_dict:
            if client_response_dict.get("status") is not None:
                status = common.check_int(client_response_dict.get("status"))
        if "body" in client_response_dict:
            if client_response_dict.get("body") is not None:
                if isinstance(body, str):
                    body = common.check_str(client_response_dict.get("body"))
                elif isinstance(body, bytes):
                    body = client_response_dict.get("body")
        return ClientResponse(status = status,
                              body   = body
                             )

    #
    def to_dict(self):
        client_response_dict: dict = {}
        if self._status is not None:
            client_response_dict["status"] = self._status
        if self._body is not None:
            client_response_dict["body"] = self._body
        return client_response_dict
 
#
class Client:
    #_host: str
    #_headers: dict
    #_authentication
    #_body: str
    #_client_id: str
    #_tenant_id: str
    #_legacy: bool
    #_version: int
    
    """
    A client wrapper for interaction with IBM PAIRS.
    
    :param host:               IBM PAIRS host.
    :type host:                str
    :param headers:            A dictionary of request headers.
    :type headers:             dict
    :param authentication:     An authentication object.
    :type authentication:      ibmpairs.authentication.Oauth2 or ibmpairs.authentication.Basic
    :param body:               A message body.
    :type body:                str
    :param client_id:          A client id for the authentication system, defaults to 'ibm-pairs' if legacy.
    :type client_id:           str
    :param tenant_id:          IBM EIS GA API Connect Tenant Id
    :type tenant_id:           str
    :param legacy:             IBM EIS GA Legacy Environment selector override
    :type legacy:              bool
    :param version:            IBM EIS GA api version (default: 3)
    :type version:             int
    """
    
    #
    def __str__(self):
        
        """
        The method creates a string representation of the internal class structure.
        
        :returns:           A string representation of the internal class structure.
        :rtype:             str
        """
        
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)

    #
    def __repr__(self):
    
        """
        The method creates a dict representation of the internal class structure.
        
        :returns:           A dict representation of the internal class structure.
        :rtype:             dict
        """
    
        return json.dumps(self.to_dict(), 
                          indent    = constants.GLOBAL_JSON_REPR_INDENT, 
                          sort_keys = constants.GLOBAL_JSON_REPR_SORT_KEYS)
                      
    def to_dict(self):
        client_dict: dict = {}
        if self._host is not None:
            client_dict["host"] = self._host
        if self._headers is not None:
            client_dict["headers"] = self._headers
        if self._authentication is not None:
            if isinstance(self._authentication, authentication.Basic):
                client_dict["authentication"] = common.class_to_dict(self._authentication, authentication.Basic)
            elif isinstance(self._authentication, authentication.OAuth2):
                client_dict["authentication"] = common.class_to_dict(self._authentication, authentication.OAuth2)
            else:
                client_dict["authentication"] = self._authentication
        if self._body is not None:
            client_dict["body"] = self._body

        try:
            if self._client_id is not None:
                client_dict["client_id"] = self._client_id
        except Exception as e:
            pass
        try:
            if self._tenant_id is not None:
                client_dict["tenant_id"] = self._tenant_id
        except Exception as e:
            pass

        if self._legacy is not None:
            client_dict["legacy"] = self._legacy
        return client_dict

    #
    def __init__(self,
                 host: str      = None,
                 headers: dict  = None,
                 authentication = None,
                 body: str      = None,
                 client_id: str = None, 
                 tenant_id: str = None,
                 legacy: bool   = None,
                 version: int   = None
                ):
            
            self._authentication = authentication

            if legacy is not None:
                self._legacy = legacy
            elif ((legacy is None) and ((self._authentication is not None) and (self._authentication.legacy is not None))):
                self._legacy = self._authentication.legacy
            else:
                self._legacy = GLOBAL_LEGACY_ENVIRONMENT
                
            if version is not None:
                if version in (3,4):
                    self._version = version
                elif version == 2:
                    self._version = version
                    self._legacy = True
                    msg = messages.INFO_AUTHENTICATION_TWO_IS_LEGACY
                    logger.info(msg)
                else:
                    msg = messages.ERROR_AUTHENTICATION_VERSION_UNKNOWN.format(version)
                    logger.error(msg)
                    raise common.PAWException(msg)
            elif ((version is None) and ((self._authentication is not None) and (self._authentication.version is not None))):
                self._version = self._authentication.version
            else:
                self._version = 3

            if (headers is not None):
                self._headers = headers
            else:
                self._headers = dict(constants.CLIENT_JSON_HEADER)

            if (host is not None):
                self._host = common.ensure_api_path(common.ensure_protocol(host), version)
            elif (host is None) and (self._authentication is not None) and (self._authentication.host is not None) and (self._legacy is False):
                self._host = common.ensure_api_path(common.ensure_protocol(self._authentication.host), version)
            else:
                if self._legacy is True:
                    self.set_version(2)
                    self._host = common.ensure_api_path(common.ensure_protocol(constants.CLIENT_LEGACY_URL))
                else:
                    if ((version is not None) and (version == 4)) \
                        or ((self._authentication is not None) and 
                            (self._authentication.version is not None) and 
                            (self._authentication.version == 4)
                    ):
                        self.set_version(4)
                        self._host = common.ensure_api_path(common.ensure_protocol(constants.CLIENT_URL_V4), 4)
                    else:
                        self.set_version(3)
                        self._host = common.ensure_api_path(common.ensure_protocol(constants.CLIENT_URL_V3))

            logger.info("HOST: " + self._host)
            
            self._body = body
            
            if self._legacy is True:
                if client_id is not None:
                    self._client_id = client_id
                else:
                    self._client_id = 'ibm-pairs'
                self._tenant_id = tenant_id
            else:
                if self.authentication_mode(self._authentication) in ['OAuth2']:
                    if (client_id is not None) and (tenant_id is not None):
                        msg = messages.INFO_BOTH_CLIENT_ID_AND_TENANT_ID.format(client_id, tenant_id)
                        logger.info(msg)
                        if client_id.startswith('saascore-'):
                            msg = messages.INFO_STARTS_WITH_SAASCORE
                            logger.info(msg)
                            self._client_id = 'geospatial-' + common.get_tenant_id(client_id)
                        else:
                            self._client_id = client_id
                        self._tenant_id = common.get_tenant_id(client_id)
                    elif (client_id is not None) and (tenant_id is None):
                        if client_id.startswith('saascore-'):
                            msg = messages.INFO_STARTS_WITH_SAASCORE
                            logger.info(msg)
                            self._client_id = 'geospatial-' + common.get_tenant_id(client_id)
                        else:
                            self._client_id = client_id
                        self._tenant_id = common.get_tenant_id(client_id)
                    elif (client_id is None) and (tenant_id is not None):
                        self._tenant_id = common.get_tenant_id(tenant_id)
                        self._client_id = 'geospatial-' + self._tenant_id
                    else:
                        if (self._authentication is not None) and (self._authentication.tenant_id is not None):
                            self._tenant_id = self._authentication.tenant_id
                            self._client_id = 'geospatial-' + self._tenant_id
                        else:
                            msg = messages.ERROR_NO_CLIENT_OR_TENANT_ID
                            logger.error(msg)
                            raise common.PAWException(msg)
                else:
                    if client_id is not None:
                        self._client_id = client_id
                    else:
                        self._client_id = 'ibm-pairs'
            
            global GLOBAL_PAIRS_CLIENT
            GLOBAL_PAIRS_CLIENT = self
    
    #       
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.check_str(common.ensure_api_path(common.ensure_protocol(host)))
        
    #    
    def del_host(self): 
        del self._host
        
    #    
    host = property(get_host, set_host, del_host)

    #       
    def get_headers(self):
        return self._headers

    #
    def set_headers(self, headers):
        self._headers = common.check_dict(headers)
        
    #    
    def del_headers(self): 
        del self._headers

    #
    def append_header(self, key: str, value: str):   
        self._headers[key] = value
        
    #    
    headers = property(get_headers, set_headers, del_headers)

    #       
    def get_authentication(self):
        return self._authentication

    #
    def set_authentication(self, authentication):
        self._authentication = authentication
        
    #    
    def del_authentication(self): 
        del self._authentication

    #    
    authentication = property(get_authentication, set_authentication, del_authentication)

    #       
    def get_body(self):
        return self._body

    #
    def set_body(self, body):
        self._body = body
        
    #    
    def del_body(self): 
        del self._body

    #    
    body = property(get_body, set_body, del_body)
    
    #       
    def get_client_id(self):
        return self._client_id
    
    #
    def set_client_id(self, client_id):
        self._client_id = client_id
        
    #    
    def del_client_id(self): 
        del self._client_id
        
    #    
    client_id = property(get_client_id, set_client_id, del_client_id)
    
    #       
    def get_tenant_id(self):
        return self._tenant_id
  
    #
    def set_tenant_id(self, tenant_id):
        self._tenant_id = tenant_id
      
    #    
    def del_tenant_id(self): 
        del self._tenant_id
      
    #    
    tenant_id = property(get_tenant_id, set_tenant_id, del_tenant_id)
    
    #
    def get_legacy(self):
        return self._legacy
    
    #
    def set_legacy(self, legacy):
        self._legacy = common.check_bool(legacy)
        
    #    
    def del_legacy(self): 
        del self._legacy
        
    #    
    legacy = property(get_legacy, set_legacy, del_legacy)
    
    #
    def get_version(self):
        return self._version
  
    #
    def set_version(self, version):
        self._version = common.check_int(version)
      
    #    
    def del_version(self): 
        del self._version
      
    #    
    version = property(get_version, set_version, del_version)
    
    def session(self,
                authentication = None,
                headers        = None,
                verify         = None
               ):
        
        """
        A wrapper method around aiohttp.ClientSession.
        
        :param authentication:     A username for the user.
        :type authentication:      ibmpairs.authentication.Basic or ibmpairs.authentication.OAuth2
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  A aiohttp.ClientSession using the attributes provided.
        :rtype:                    aiohttp.ClientSession
        """

        if headers is not None:
            self.set_headers(headers)
            
            if ((self._legacy is False) and (self.authentication_mode(self._authentication) in ['OAuth2'])):
                self.append_header('x-ibm-client-id', self.get_client_id())
                
            msg = messages.DEBUG_CLIENT_SET_HEADERS.format(headers)
            logger.debug(msg)
        
        if authentication is not None:
            self.set_authentication(authentication)
            msg = messages.DEBUG_CLIENT_SET_HEADERS.format(authentication)
            logger.debug(msg)
                        
        connector = aiohttp.TCPConnector(ssl = verify)
                                        
        if self.authentication_mode(self._authentication) in ['Basic', 'None']:
            # If authentication.Basic then get set authenication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = aiohttp.BasicAuth(self._authentication.username, self._authentication.password)

            timeout = aiohttp.ClientTimeout(constants.CLIENT_TIMEOUT)
            session = aiohttp.ClientSession(connector = connector, 
                                            auth      = authentication,
                                            headers   = self._headers,
                                            timeout   = timeout
                                           )
        elif self.authentication_mode(self._authentication) in ['OAuth2']:
            
            # Add bearer token to headers.
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)

            timeout = aiohttp.ClientTimeout(constants.CLIENT_TIMEOUT)
            session = aiohttp.ClientSession(connector = connector, 
                                            headers   = self._headers,
                                            timeout   = timeout
                                           )
        else: 
            msg = messages.ERROR_CLIENT_AUTHENTICATION_MECHANISM.format(self.authentication_mode(self._authentication))
            logger.error(msg)
            raise common.PAWException(msg)

        return session

    #
    async def async_get(self,
                        url,
                        session: aiohttp.ClientSession = None,
                        authentication                 = None,
                        headers                        = None,
                        verify                         = None,
                        response_type                  = 'json'
                       ):
                        
        """
        A wrapper method around aiohttp.ClientSession.get.
        
        :param url:                A URL to GET.
        :type url:                 str
        :param session:            An aiohttp.ClientSession to use for a GET request.
        :type session:             aiohttp.ClientSession
        :param authentication:     A username for the user.
        :type authentication:      ibmpairs.authentication.Basic or ibmpairs.authentication.OAuth2
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :param response_type:      A response type, defaults to json.
        :type response_type:       str
        :returns:                  An ibmpairs.client.ClientResponse object.
        :rtype:                    ibmpairs.client.ClientResponse
        """
    
        retry: bool = False

        client_response = ClientResponse()

        if session is None:
            session = self.session(authentication, 
                                   headers,
                                   verify
                                  )

        async with session.get(url = url
                              ) as response:
            
            client_response.status = response.status  
            if response_type == 'json':
                client_response.body   = await response.text()
            else:
                client_response.body   = await response.read()

            await session.close() 
            
        if ((self._legacy is True) and (client_response.status in (401,403))):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
            if client_response.body is not None:
                response_string = client_response.body
                if token_refresh_message in response_string:
                    logger.debug(response_string)
                    retry = True
        elif ((self._legacy is False) and (client_response.status == 500)):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
            if client_response.body is not None:
                response_string = str(client_response.body)
                if token_refresh_message in response_string:
                    logger.debug(response_string)
                    retry = True

        if retry is True:
            self._authentication.refresh_auth_token()
                    
            session = self.session(self._authentication, 
                                   headers,
                                   verify
                                  )

            async with session.get(url = url
                                  ) as response:
                            
                client_response.status = response.status  
                if response_type == 'json':
                    client_response.body   = await response.text()
                else:
                    client_response.body   = await response.read()

                await session.close()
        
        return client_response
    
    #
    def get(self, 
            url,
            headers = None,
            verify  = True
           ):
            
        """
        A wrapper method around requests.get.
        
        :param url:                A URL to GET.
        :type url:                 str
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  A requests.Response object.
        :rtype:                    requests.Response
        """
        
        retry: bool = False
        
        response = None
        
        if headers is not None:
            self.set_headers(headers)
            
        if self._legacy is False:
            self.append_header('x-ibm-client-id', self.get_client_id())
              
        msg = messages.DEBUG_CLIENT_SET_HEADERS.format('GET', headers)
        logger.debug(msg)
        
        if self.authentication_mode(self._authentication) in ['Basic', 'tuple', 'Dict', 'None']:
            # If Basic, construct an authentication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = self._authentication.get_credentials()
                
            response = requests.get(url, 
                                    auth    = authentication,
                                    headers = self._headers,
                                    verify  = verify)
        elif self.authentication_mode(self._authentication) in ['OAuth2']:
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)
            response = requests.get(url, 
                                    headers = self._headers,
                                    verify  = verify
                                   )
                                    
            if ((self._legacy is True) and (response.status_code in (401,403))):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            elif ((self._legacy is False) and (response.status_code == 500)):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            
            if retry is True:
                self._authentication.refresh_auth_token()
                token = 'Bearer ' + self._authentication.jwt_token
                self.append_header('Authorization', token)
                response = requests.get(url, 
                                        headers = self._headers,
                                        verify  = verify
                                       )
        else:
            msg = messages.ERROR_AUTHENTICATION_TYPE_NOT_RECOGNIZED.format(type(self._authentication))
            logger.error(msg)
            raise Exception(msg)
            
        return response

    #
    def put(self, 
            url,
            body    = None,
            headers = None,
            verify  = True
           ):
            
        """
        A wrapper method around requests.put.
        
        :param url:                A URL to PUT.
        :type url:                 str
        :param body:               A body for the PUT request.
        :type body:                Any
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  A requests.Response object.
        :rtype:                    requests.Response
        """
        
        retry: bool = False
            
        response = None
        
        if headers is not None:
            self.set_headers(headers)

        if self._legacy is False:
            self.append_header('x-ibm-client-id', self.get_client_id())
              
        msg = messages.DEBUG_CLIENT_SET_HEADERS.format('PUT', headers)
        logger.debug(msg)
        
        if self.authentication_mode(self._authentication) in ['Basic', 'tuple', 'Dict', 'None']:
            # If Basic, construct an authentication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = self._authentication.get_credentials()
                
            response = requests.put(url, 
                                    auth    = authentication,
                                    headers = self._headers,
                                    data    = body,
                                    verify  = verify
                                   )
        elif self.authentication_mode(self._authentication) in ['OAuth2']:
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)
            response = requests.put(url,
                                    headers = self._headers,
                                    data    = body,
                                    verify  = verify
                                   )
            
            if ((self._legacy is True) and (response.status_code in (401,403))):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            elif ((self._legacy is False) and (response.status_code == 500)):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            
            if retry is True:
                self._authentication.refresh_auth_token()
                token = 'Bearer ' + self._authentication.jwt_token
                self.append_header('Authorization', token)
                response = requests.put(url,
                                        headers = self._headers,
                                        data    = body,
                                        verify  = verify
                                       )

        else:
            msg = messages.ERROR_AUTHENTICATION_TYPE_NOT_RECOGNIZED.format(type(self._authentication))
            logger.error(msg)
            raise Exception(msg)
                    
        return response
    
    #
    async def async_post(self,
                         url,
                         body,
                         session: aiohttp.ClientSession = None,
                         authentication                 = None,
                         headers                        = None,
                         verify                         = None
                        ):
                          
        """
        A wrapper method around aiohttp.ClientSession.post.
        
        :param url:                A URL to POST.
        :type url:                 str
        :param body:               A body for the POST request.
        :type body:                Any
        :param session:            An aiohttp.ClientSession to use for a get request.
        :type session:             aiohttp.ClientSession
        :param authentication:     A username for the user.
        :type authentication:      ibmpairs.authentication.Basic or ibmpairs.authentication.OAuth2
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  An ibmpairs.client.ClientResponse object.
        :rtype:                    ibmpairs.client.ClientResponse
        """

        retry: bool = False
                            
        client_response = ClientResponse()

        if session is None:
            session = self.session(authentication, 
                                   headers,
                                   verify
                                  )

        async with session.post(url  = url,
                                json = body 
                               ) as response:
            
            client_response.status = response.status
            client_response.body   = await response.text()

            await session.close()
            
        if ((self._legacy is True) and (client_response.status in (401,403))):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
            if client_response.body is not None:
                response_string = client_response.body
                if token_refresh_message in response_string:
                    logger.debug(response_string)
                    retry = True
        elif ((self._legacy is False) and (client_response.status == 500)):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
            if client_response.body is not None:
                response_string = str(client_response.body)
                if token_refresh_message in response_string:
                    logger.debug(response_string)
                    retry = True
        
        if retry is True:
            self._authentication.refresh_auth_token()
                    
            session = self.session(self._authentication, 
                                   headers,
                                   verify
                                  )

            async with session.post(url  = url,
                                    json = body 
                                   ) as response:
            
                client_response.status = response.status
                client_response.body   = await response.text()

                await session.close()
        
        return client_response

    #
    def post(self, 
             url,
             body,
             headers = None,
             verify  = True
            ):
              
        """
        A wrapper method around requests.post.
        
        :param url:                A URL to POST.
        :type url:                 str
        :param body:               A body for the POST request.
        :type body:                Any
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  A requests.Response object.
        :rtype:                    requests.Response
        """
        
        retry: bool = False
        
        response = None
        
        if headers is not None:
            self.set_headers(headers)
     
        if self._legacy is False:
            self.append_header('x-ibm-client-id', self.get_client_id())

        msg = messages.DEBUG_CLIENT_SET_HEADERS.format('POST', headers)
        logger.debug(msg)
        
        auth_mode = self.authentication_mode(self._authentication)
        
        if auth_mode in ['Basic', 'tuple', 'Dict', 'None']:
            # If Basic, construct an authentication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = self._authentication.get_credentials()

            logger.debug(messages.DEBUG_CLIENT_POST_BASIC.format(body, url))
            response = requests.post(url,
                                     auth    = authentication,
                                     headers = self._headers,
                                     data    = body,
                                     verify  = verify
                                    )
        elif auth_mode in ['OAuth2']:
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)
            logger.debug(messages.DEBUG_CLIENT_POST_OAUTH.format(body, url))
            response = requests.post(url,
                                     headers = self._headers,
                                     data    = body,
                                     verify  = verify
                                    )
            
            if ((self._legacy is True) and (response.status_code in (401,403))):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            elif ((self._legacy is False) and (response.status_code == 500)):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            
            if retry is True:
                self._authentication.refresh_auth_token()
                token = 'Bearer ' + self._authentication.jwt_token
                self.append_header('Authorization', token)
                logger.debug(messages.DEBUG_CLIENT_POST_OAUTH.format(body, url))
                response = requests.post(url,
                                         headers = self._headers,
                                         data    = body,
                                         verify  = verify
                                        )
        else:
            msg = messages.ERROR_AUTHENTICATION_TYPE_NOT_RECOGNIZED.format(type(self._authentication))
            logger.error(msg)
            raise Exception(msg)

        return response
      
    #
    def delete(self,
               url,
               headers = None,
               verify  = True
              ):
                
        """
        A wrapper method around requests.delete.
        
        :param url:                A URL to DELETE.
        :type url:                 str
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param verify:             Verify SSL.
        :type verify:              bool
        :returns:                  A requests.Response object.
        :rtype:                    requests.Response
        """
        
        retry: bool = False
                
        response = None
        
        if headers is not None:
            self.set_headers(headers)
            
        if self._legacy is False:
            self.append_header('x-ibm-client-id', self.get_client_id())

        msg = messages.DEBUG_CLIENT_SET_HEADERS.format('DELETE', headers)
        logger.debug(msg)
        
        auth_mode = self.authentication_mode(self._authentication)
        
        if auth_mode in ['Basic', 'tuple', 'Dict', 'None']:
            # If Basic, construct an authentication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = self._authentication.get_credentials()

            logger.debug(messages.DEBUG_CLIENT_DELETE_BASIC.format(url))
            response = requests.delete(url, 
                                       auth    = authentication,
                                       headers = self._headers,
                                       verify  = verify
                                      )
        elif auth_mode in ['OAuth2']:
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)
            logger.debug(messages.DEBUG_CLIENT_DELETE_OAUTH.format(url))
            response = requests.delete(url,
                                       headers = self._headers,
                                       verify  = verify
                                      )
                                        
            if ((self._legacy is True) and (response.status_code in (401,403))):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
            elif ((self._legacy is False) and (response.status_code == 500)):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE_APIC
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
                        logger.debug(response_string)
                        retry = True
          
            if retry is True:
                self._authentication.refresh_auth_token()
                token = 'Bearer ' + self._authentication.jwt_token
                self.append_header('Authorization', token)
                logger.debug(messages.DEBUG_CLIENT_DELETE_OAUTH.format(url))
                response = requests.delete(url,
                                           headers = self._headers,
                                           verify  = verify
                                          )
        else:
            msg = messages.ERROR_AUTHENTICATION_TYPE_NOT_RECOGNIZED.format(type(self._authentication))
            logger.error(msg)
            raise Exception(msg)

        return response

    @staticmethod
    def authentication_mode(a):
      
        """
        A wrapper method to determine authentication type.
        
        :param a: authentication
        :type a:  Any
        :returns: An authentication type string.
        :rtype:   str
        """
      
        authentication_mode: str
    
        if a is None:
            msg = u'The authentication object is not set.'
#            logger.warning(msg)
            authentication_mode = 'None' 
        elif type(a) is tuple:
            authentication_mode = 'tuple'
        elif type(a) is authentication.Basic:
            authentication_mode = 'Basic'
        elif type(a) is authentication.OAuth2:
             authentication_mode = 'OAuth2'
        elif type(a) is dict:
            authentication_mode = 'dict'
        else:
            msg = u'The authentication object was not recognized.'
#            logger.warning(msg)
            raise Exception(msg)
        
        return authentication_mode
  
#
def get_client(host: str          = None,
               username: str      = None,
               api_key: str       = None,
               api_key_file: str  = "auth/oauth2.txt",
               client_id: str     = None,
               endpoint: str      = None,
               jwt_token: str     = None,
               iam_endpoint: str  = "iam.cloud.ibm.com",
               org_id: str        = None, 
               tenant_id: str     = None,
               headers: dict      = None,
               body: str          = None,
               password: str      = None,
               password_file: str = None,
               legacy: bool       = None,
               version: int       = None
              ):
    """
    Gets either a authentication.Basic or authentication.OAuth2 from authentication credentials.
    
    :param host:          IBM PAIRS host
    :type host:           str
    :param username:      IBM PAIRS username
    :type username:       str
    :param api_key:       IBM PAIRS API key
    :type api_key:        str
    :param api_key_file:  IBM PAIRS API key file, defaults to auth/oauth2.txt
    :type api_key_file:   str
    :param client_id:     A client id for the authentication system, defaults to 'ibm-pairs' if legacy.
    :type client_id:      str
    :param endpoint:      The authentication endpoint.
    :type endpoint:       str
    :param jwt_token:     A jwt token for authentication.
    :type jwt_token:      str
    :param iam_endpoint:  IBM Cloud IAM Endpoint
    :type iam_endpoint:   str
    :param org_id:        IBM EIS GA API Connect Org Id
    :type org_id:         str
    :param tenant_id:     IBM EIS GA API Connect Tenant Id
    :type tenant_id:      str
    :param password:      IBM PAIRS password
    :type password:       str
    :param password_file: IBM PAIRS password file, defaults to auth/basic.txt
    :type password_file:  str
    :param legacy:        IBM EIS GA Legacy Environment selector override
    :type legacy:         bool
    :param version:       IBM EIS GA api version (default: 3)
    :type version:        int
    :rtype:               authentication.Basic or authentication.OAuth2
    :raises Exception:    if authentication.Basic or authentication.OAuth2 raise an error
    """
    
    auth = None
    
    if (password is not None) or (password_file is not None):
        msg = messages.INFO_BASIC_AUTH_ASSUMPTION
        logger.info(msg)
        
        auth = authentication.Basic(host          = host,
                                    username      = username,
                                    password      = password,
                                    password_file = password_file,
                                    legacy        = legacy,
                                    version       = version
                                   )
    
    else:
        msg = messages.INFO_0AUTH2_AUTH_ASSUMPTION
        logger.info(msg)
        
        auth = authentication.OAuth2(host         = host,
                                     username     = username,
                                     api_key      = api_key,
                                     api_key_file = api_key_file,
                                     client_id    = client_id,
                                     endpoint     = endpoint,
                                     jwt_token    = jwt_token,
                                     iam_endpoint = iam_endpoint,
                                     org_id       = org_id, 
                                     tenant_id    = tenant_id,
                                     legacy       = legacy,
                                     version      = version
                                    )
        
    eis_client = Client(headers = headers,
                        authentication = auth,
                        body = body
                       )
    
    return eis_client
