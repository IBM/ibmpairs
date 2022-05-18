"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""

# fold: Import Python Standard Library {{{
# Python Standard Library:
#}}}
from typing import List, Any
import json
import logging
import os
import warnings
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
    #_host: str           = None
    #_headers: dict       = None
    #_authentication      = None
    #_body                = None
    
    """
    A client wrapper for interaction with IBM PAIRS.
    
    :param headers:            IBM PAIRS host.
    :type headers:             str
    :param headers:            A dictionary of request headers.
    :type headers:             dict
    :param authentication:     An authentication object.
    :type authentication:      ibmpairs.authentication.Oauth2 or ibmpairs.authentication.Basic
    :param body:               A message body.
    :type body:                str
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
        return client_dict

    #
    def __init__(self,
                 host = None,
                 headers = None,
                 authentication = None,
                 body = None
                ):

            if (headers is not None):
                self._headers = headers
            else:
                self._headers = constants.CLIENT_JSON_HEADER

            self._authentication = authentication
            
            if (host is not None):
                self._host = common.ensure_protocol(host)
            elif (host is None) and (self._authentication is not None) and (self._authentication.host is not None):
                self._host = common.ensure_protocol(self._authentication.host)
            else:
                self._host = common.ensure_protocol(constants.CLIENT_PAIRS_URL)
            
            self._body = body
            
            global GLOBAL_PAIRS_CLIENT 
            GLOBAL_PAIRS_CLIENT = self
    
    #       
    def get_host(self):
        return self._host

    #
    def set_host(self, host):
        self._host = common.ensure_protocol(common.check_str(host))
        
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
    
    def session(self,
                authentication = None,
                headers        = None,
                ssl            = None,
                verify_ssl     = True
               ):
        
        """
        A wrapper method around aiohttp.ClientSession.
        
        :param authentication:     A username for the user.
        :type authentication:      ibmpairs.authentication.Basic or ibmpairs.authentication.OAuth2
        :param headers:            A dictionary of request headers.
        :type headers:             dict
        :param ssl:                SSL.
        :type ssl:                 str
        :param verify_ssl:         Verify SSL.
        :type verify_ssl:          bool
        :returns:                  A aiohttp.ClientSession using the attributes provided.
        :rtype:                    aiohttp.ClientSession
        """
        
        if headers is not None:
            self.set_headers(headers)
            msg = messages.DEBUG_CLIENT_SET_HEADERS.format(headers)
            logger.debug(msg)
        
        if authentication is not None:
            self.set_authentication(authentication)
            msg = messages.DEBUG_CLIENT_SET_HEADERS.format(authentication)
            logger.debug(msg)             
                        
        connector = aiohttp.TCPConnector(ssl        = ssl,
                                         verify_ssl = verify_ssl
                                        )
                                        
        if self.authentication_mode(self._authentication) in ['Basic', 'None']:
            # If authentication.Basic then get set authenication tuple.
            if self.authentication_mode(self._authentication) in ['Basic']:
                authentication = aiohttp.BasicAuth(self._authentication.username, self._authentication.password)

            session = aiohttp.ClientSession(connector = connector, 
                                            auth      = authentication,
                                            headers   = self._headers
                                           )
        elif self.authentication_mode(self._authentication) in ['OAuth2']:
            
            # Add bearer token to headers.
            token = 'Bearer ' + self._authentication.jwt_token
            self.append_header('Authorization', token)
            
            session = aiohttp.ClientSession(connector = connector, 
                                            headers   = self._headers
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
                        ssl                            = None,
                        verify                         = True,
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
        :param ssl:                SSL.
        :type ssl:                 str
        :param verify_ssl:         Verify SSL.
        :type verify_ssl:          bool
        :param response_type:      A response type, defaults to json.
        :type response_type:       str
        :returns:                  An ibmpairs.client.ClientResponse object.
        :rtype:                    ibmpairs.client.ClientResponse
        """

        client_response = ClientResponse()

        if session is None:
            session = self.session(authentication, 
                                   headers,
                                   ssl,
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

        if client_response.status in (401,403):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
            if client_response.body is not None:
                response_string = client_response.body
                if token_refresh_message in response_string:
                    
                    self._authentication.refresh_auth_token()
                    
                    session = self.session(self._authentication, 
                                           headers,
                                           ssl,
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
        
        response = None
        
        if headers is not None:
            self.set_headers(headers)
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
            
            if response.status_code in (401,403):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
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
            
        response = None
        
        if headers is not None:
            self.set_headers(headers)
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
            if response.status_code in (401,403):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
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
                         ssl                            = None,
                         verify                         = True
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
        :param ssl:                SSL.
        :type ssl:                 str
        :param verify_ssl:         Verify SSL.
        :type verify_ssl:          bool
        :returns:                  An ibmpairs.client.ClientResponse object.
        :rtype:                    ibmpairs.client.ClientResponse
        """
                            
        client_response = ClientResponse()

        if session is None:
            session = self.session(authentication, 
                                   headers,
                                   ssl,
                                   verify
                                  )

        async with session.post(url  = url,
                                json = body 
                               ) as response:
            
            client_response.status = response.status            
            client_response.body   = await response.text()

            await session.close()
        
        if client_response.status in (401,403):
            token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
            if client_response.body is not None:
                response_string = client_response.body
                if token_refresh_message in response_string:
                    
                    self._authentication.refresh_auth_token()
                    
                    session = self.session(self._authentication, 
                                           headers,
                                           ssl,
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
        
        response = None
        
        if headers is not None:
            self.set_headers(headers)
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
            if response.status_code in (401,403):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
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
                
        response = None
        
        if headers is not None:
            self.set_headers(headers)
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
          
            if response.status_code in (401,403):
                token_refresh_message = constants.CLIENT_TOKEN_REFRESH_MESSAGE
                if response.json() is not None:
                    response_string = json.dumps(response.json())
                    if token_refresh_message in response_string:
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
