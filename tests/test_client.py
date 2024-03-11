"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
from ibmpairs.logger import logger
import ibmpairs.authentication as authentication
import ibmpairs.client as cl
import ibmpairs.constants as constants
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import responses
import unittest
from unittest import mock
import asyncio
import aiohttp
#}}}

mocked_requests_get_tracker = 0

#
def mocked_requests_get(*args, **kwargs):

    global mocked_requests_get_tracker

    url           = args[0]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (url == 'https://token.refresh'):
        if mocked_requests_get_tracker == 0:
            message = {"error":"jwt signature verification failed: 'exp' claim expired at Mon, 12 Jul 2021 13:14:14 GMT"}
            mocked_requests_get_tracker = mocked_requests_get_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_get_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_get_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    elif (url == 'https://token.refreshed'):
        if mocked_requests_get_tracker == 0:
            message = r'''{"description": "b'{\"error\":\"jwt signature verification failed: \\'exp\\' claim expired at Mon, 12 Jul 2021 13:14:14 GMT\"}\\n'"}'''
            mocked_requests_get_tracker = mocked_requests_get_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_get_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_get_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    else:
        return MockResponse(None, 404)

mocked_requests_post_tracker = 0

#
def mocked_requests_post(*args, **kwargs):

    global mocked_requests_post_tracker

    url           = args[0]
    input_headers = None
    input_data    = None
    api_key       = None
    client_id     = None
    grant_type    = None
    refresh_token = None
    
    if kwargs.get("headers") is not None:
        input_headers = kwargs["headers"]
    
    if kwargs.get("data") is not None:
        input_data = kwargs["data"]
        
        if (url == 'https://auth-b2b-twc.ibm.com/Auth/GetBearerForClient'):
            input_data_dict = json.loads(input_data)
            
            if input_data_dict.get("apiKey") is not None:
                api_key = input_data_dict["apiKey"]
                
            if input_data_dict.get("clientId") is not None:
                client_id = input_data_dict["clientId"]
            
            if input_data_dict.get("client_id") is not None:
                client_id = input_data_dict["client_id"]
                
            if input_data_dict.get("grant_type") is not None:
                grant_type = input_data_dict["grant_type"]
                
            if input_data_dict.get("refresh_token") is not None:
                refresh_token = input_data_dict["refresh_token"]
        elif (url == 'https://auth-b2b-twc.ibm.com/connect/token'):
            input_data  = input_data.replace('=', '&')
            split       = input_data.split('&')
            
            grant_type    = split[1]
            client_id     = split[3]
            refresh_token = split[5]
        else:
            input_data_dict = input_data
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (url == 'https://auth-b2b-twc.ibm.com/Auth/GetBearerForClient'):        
        if api_key == 'thisisnotanapikey':
            return_dict = {}
            return_dict["access_token"]  = "thisisnotanaccesstoken"
            return_dict["expires_in"]    = 3600
            return_dict["token_type"]    = "Bearer"
            return_dict["refresh_token"] = "thisisnotarefreshtoken"
            return_dict["scope"]         = "access:A B C D"
            
            if client_id == 'ibm-pairs':
                return MockResponse(return_dict, 200)
            else:
                return MockResponse({"error":"invalid_client"}, 200)
        else:
            return MockResponse({"error":"invalid_grant"}, 200)
    elif (url == 'https://auth-b2b-twc.ibm.com/connect/token'):
        if grant_type == 'refresh_token':
            if refresh_token == 'thisisnotarefreshtoken':
                return_dict = {}
                return_dict["access_token"]  = "thisisnotanewaccesstoken"
                return_dict["expires_in"]    = 3600
                return_dict["token_type"]    = "Bearer"
                return_dict["refresh_token"] = "thisisnotanewrefreshtoken"
                return_dict["scope"]         = "access:A B C D"
            
                if client_id == 'ibm-pairs':
                    return MockResponse(return_dict, 200)
                else:
                    return MockResponse({"error":"invalid_client"}, 200)
            else:
                return MockResponse({"error":"invalid_grant"}, 200)
        else:
            return MockResponse({"error": "unsupported_grant_type"}, 200)
    elif (url == 'https://token.refresh'):
        if mocked_requests_post_tracker == 0:
            message = {"error":"jwt signature verification failed: 'exp' claim expired at Mon, 12 Jul 2021 13:14:14 GMT"}
            mocked_requests_post_tracker = mocked_requests_post_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_post_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_post_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    elif (url == 'https://token.refreshed'):
        if mocked_requests_post_tracker == 0:
            message = r'''{"description": "b'{\"error\":\"jwt signature verification failed: \\'exp\\' claim expired at Mon, 12 Jul 2021 13:14:14 GMT\"}\\n'"}'''
            mocked_requests_post_tracker = mocked_requests_post_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_post_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_post_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
            
    return MockResponse(None, 404)

mocked_requests_put_tracker = 0

#
def mocked_requests_put(*args, **kwargs):

    global mocked_requests_put_tracker

    url           = args[0]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (url == 'https://token.refresh'):
        if mocked_requests_put_tracker == 0:
            message = {"error":"jwt signature verification failed: 'exp' claim expired at Mon, 12 Jul 2021 13:14:14 GMT"}
            mocked_requests_put_tracker = mocked_requests_put_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_put_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_put_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    elif (url == 'https://token.refreshed'):
        if mocked_requests_put_tracker == 0:
            message = r'''{"description": "b'{\"error\":\"jwt signature verification failed: \\'exp\\' claim expired at Mon, 12 Jul 2021 13:14:14 GMT\"}\\n'"}'''
            mocked_requests_put_tracker = mocked_requests_put_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_put_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_put_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    else:
        return MockResponse(None, 404)
        
mocked_requests_delete_tracker = 0

#
def mocked_requests_delete(*args, **kwargs):

    global mocked_requests_delete_tracker

    url           = args[0]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (url == 'https://token.refresh'):
        if mocked_requests_delete_tracker == 0:
            message = {"error":"jwt signature verification failed: 'exp' claim expired at Mon, 12 Jul 2021 13:14:14 GMT"}
            mocked_requests_delete_tracker = mocked_requests_delete_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_delete_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_delete_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    elif (url == 'https://token.refreshed'):
        if mocked_requests_delete_tracker == 0:
            message = r'''{"description": "b'{\"error\":\"jwt signature verification failed: \\'exp\\' claim expired at Mon, 12 Jul 2021 13:14:14 GMT\"}\\n'"}'''
            mocked_requests_delete_tracker = mocked_requests_delete_tracker + 1
            return MockResponse(message, 403)
        elif mocked_requests_delete_tracker == 1:
            message = r'''{"message":"success"}'''
            mocked_requests_delete_tracker = 0
            return MockResponse(message, 200)
        else:
            return MockResponse(None, 404)
    else:
        return MockResponse(None, 404)

#
class ClientUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')
    
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_client_init(self, mock_post):
        
        basic = authentication.Basic(username = "email@domain.com",
                                     password = "thisisnotapassword"
                                    )
        
        oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                       legacy = True)
        
        self.logger.info('test_client_init')
        
        got_exception = False
        
        try:
            client = cl.Client(authentication = oauth2)
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(client.host, "https://pairs.res.ibm.com/v2")
        self.assertEqual(client.headers, constants.CLIENT_JSON_HEADER)
        self.assertEqual(client.authentication.api_key, "thisisnotanapikey")
        self.assertEqual(client.authentication.jwt_token, "thisisnotanaccesstoken")
        self.assertEqual(client.body, None)
        
        self.logger.info('test_client_init: set attributes')
        
        got_exception = False
        
        try:
            client.host                     = "https://pairs.res.ibm.com/v2"
            client.headers                  = constants.CLIENT_JSON_HEADER
            client.authentication.api_key   = "thisisnotanapikey"
            client.authentication.jwt_token = "thisisnotanaccesstoken"
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)

    @mock.patch('requests.get', 
                side_effect=mocked_requests_get
               )
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_client_get(self, mock_post, mock_get):
        self.logger.info('test_client_get')
        
        basic = authentication.Basic(username = "email@domain.com",
                                     password = "thisisnotapassword"
                                    )
        
        oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                       legacy  = True)
        
        got_exception = False
        
        try:
            client = cl.Client(authentication = oauth2)
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        got_exception2 = False
        
        self.assertEqual(client.authentication.jwt_token, "thisisnotanaccesstoken")
        
        self.logger.info('test_client_get: expired token core')
        
        try:
            resp = client.get(url = "https://token.refresh")
        except:
            got_exception2 = True
    
        self.assertFalse(got_exception2)
        self.assertEqual(resp.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_get: expired token upload')
        
        got_exception3 = False
        
        try:
            oauth2_2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                             legacy = True)
            client2 = cl.Client(authentication = oauth2_2)
            resp2 = client2.get(url = "https://token.refreshed")
        except:
            got_exception3 = True
    
        self.assertFalse(got_exception3)
        self.assertEqual(resp2.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_get: 404')
        
        got_exception4 = False
        
        try:
            resp3 = client.get(url = "https://token.refreshing")
        except:
            got_exception4 = True
    
        self.assertFalse(got_exception4)
        self.assertEqual(resp3.status_code, 404)
        self.assertEqual(resp3.json(), None)
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
    
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_client_post(self, mock_post):
        self.logger.info('test_client_post')
        
        basic = authentication.Basic(username = "email@domain.com",
                                     password = "thisisnotapassword"
                                    )
        
        oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                       legacy  = True)
        
        got_exception = False
        
        try:
           client = cl.Client(authentication = oauth2)
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        got_exception2 = False
        
        self.assertEqual(client.authentication.jwt_token, "thisisnotanaccesstoken")
        
        self.logger.info('test_client_post: expired token core')
        
        try:
            resp = client.post(url  = "https://token.refresh",
                               body = "body")
        except:
            got_exception2 = True
    
        self.assertFalse(got_exception2)
        self.assertEqual(resp.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_post: expired token upload')
        
        got_exception3 = False
        
        try:
            oauth2_2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                             legacy = True)
            client2 = cl.Client(authentication = oauth2_2)
            resp2 = client2.post(url  = "https://token.refreshed",
                                 body = "body")
        except:
            got_exception3 = True
    
        self.assertFalse(got_exception3)
        self.assertEqual(resp2.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_post: 404')
        
        got_exception4 = False
        
        try:
            resp3 = client.post(url  = "https://token.refreshing",
                               body = "body")
        except:
            got_exception4 = True
    
        self.assertFalse(got_exception4)
        self.assertEqual(resp3.status_code, 404)
        self.assertEqual(resp3.json(), None)
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
    
    @mock.patch('requests.put', 
                side_effect=mocked_requests_put
               )
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_client_put(self, mock_post, mock_put):
        self.logger.info('test_client_put')
        
        basic = authentication.Basic(username = "email@domain.com",
                                     password = "thisisnotapassword"
                                    )
        
        oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                       legacy  = True)
        
        got_exception = False
        
        try:
           client = cl.Client(authentication = oauth2)
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        got_exception2 = False
        
        self.assertEqual(client.authentication.jwt_token, "thisisnotanaccesstoken")
        
        self.logger.info('test_client_put: expired token core')
        
        try:
            resp = client.put(url  = "https://token.refresh",
                              body = "body")
        except:
            got_exception2 = True
    
        self.assertFalse(got_exception2)
        self.assertEqual(resp.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_post: expired token upload')
            
        got_exception3 = False
        
        try:
            oauth2_2 = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                             legacy = True)
            client2 = cl.Client(authentication = oauth2_2)
            resp2 = client2.put(url  = "https://token.refreshed",
                                body = "body")
        except:
            got_exception3 = True
    
        self.assertFalse(got_exception3)
        self.assertEqual(resp2.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_put: 404')
        
        got_exception4 = False
        
        try:
            resp3 = client.post(url  = "https://token.refreshing",
                               body = "body")
        except:
            got_exception4 = True
    
        self.assertFalse(got_exception4)
        self.assertEqual(resp3.status_code, 404)
        self.assertEqual(resp3.json(), None)
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
    @mock.patch('requests.delete', 
                side_effect=mocked_requests_delete
               )
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_client_delete(self, mock_post, mock_delete):
        self.logger.info('test_client_delete')
        
        basic = authentication.Basic(username = "email@domain.com",
                                     password = "thisisnotapassword"
                                    )
        
        oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey', 
                                       legacy  = True)
        
        got_exception = False
        
        try:
           client = cl.Client(authentication = oauth2)
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        got_exception2 = False
        
        self.assertEqual(client.authentication.jwt_token, "thisisnotanaccesstoken")
        
        self.logger.info('test_client_delete: expired token core')
        
        try:
            resp = client.delete(url  = "https://token.refresh")
        except:
            got_exception2 = True
    
        self.assertFalse(got_exception2)
        self.assertEqual(resp.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_delete: expired token upload')
            
        got_exception3 = False
        
        try:
            oauth2_2 = authentication.OAuth2(api_key = 'thisisnotanapikey', 
                                             legacy  = True)
            client2 = cl.Client(authentication = oauth2_2)
            resp2 = client2.delete(url  = "https://token.refreshed")
        except:
            got_exception3 = True
    
        self.assertFalse(got_exception3)
        self.assertEqual(resp2.json(), r'''{"message":"success"}''')
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        
        self.logger.info('test_client_delete: 404')
        
        got_exception4 = False
        
        try:
            resp3 = client.delete(url  = "https://token.refreshing")
        except:
            got_exception4 = True
    
        self.assertFalse(got_exception4)
        self.assertEqual(resp3.status_code, 404)
        self.assertEqual(resp3.json(), None)
        self.assertEqual(client.authentication.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(client.authentication.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
    
