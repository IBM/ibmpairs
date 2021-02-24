"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2020 Physical Analytics, IBM Research All Rights Reserved.

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
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import responses
import unittest
from unittest import mock
#}}}

def mocked_requests_post(*args, **kwargs):

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
        else:
            input_data_dict = input_data
        
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
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (url == 'https://auth-b2b-twc.ibm.com/Auth/GetBearerForClient'):        
        if api_key == 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd':
            return_dict = {}
            return_dict["access_token"]  = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
            return_dict["expires_in"]    = 3600
            return_dict["token_type"]    = "Bearer"
            return_dict["refresh_token"] = "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD"
            return_dict["scope"]         = "access:A B C D"
            
            if client_id == 'ibm-pairs':
                return MockResponse(return_dict, 200)
            else:
                return MockResponse({"error":"invalid_client"}, 200)
        else:
            return MockResponse({"error":"invalid_grant"}, 200)
    elif (url == 'https://auth-b2b-twc.ibm.com/connect/token'):
        if grant_type == 'refresh_token':
            if refresh_token == '8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD':
                return_dict = {}
                return_dict["access_token"]  = "HNanna8s8hx8nsnDNXS2NONKNW4QKNXCNWnc8whWH0cwh8cH"
                return_dict["expires_in"]    = 3600
                return_dict["token_type"]    = "Bearer"
                return_dict["refresh_token"] = "J-xaooxmPWXopmcpqm0h80h8nicwonkoxnx0qxhj887"
                return_dict["scope"]         = "access:A B C D"
            
                if client_id == 'ibm-pairs':
                    return MockResponse(return_dict, 200)
                else:
                    return MockResponse({"error":"invalid_client"}, 200)
            else:
                return MockResponse({"error":"invalid_grant"}, 200)
        else:
            return MockResponse({"error": "unsupported_grant_type"}, 200)

    return MockResponse(None, 404)

class OAuth2ReturnUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')
    
    def test_from_dict(self):
        
        self.logger.info('test_from_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD"
        oauth2_return_dict["scope"]         = "access:A B C D"
        oauth2_return_dict["error"]         = "invalid_grant"
        
        oauth2_return = authentication.OAuth2Return

        oauth2_return_from_dict = None
                
        got_exception = False
        try:
            oauth2_return_from_dict = oauth2_return.from_dict(oauth2_return_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_return_from_dict.access_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(oauth2_return_from_dict.expires_in, 3600)
        self.assertEqual(oauth2_return_from_dict.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_dict.refresh_token, "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(oauth2_return_from_dict.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_dict.error, "invalid_grant")
        
    def test_to_dict(self):
        
        self.logger.info('test_to_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD"
        oauth2_return_dict["scope"]         = "access:A B C D"
        oauth2_return_dict["error"]         = "invalid_grant"
        
        oauth2_return_to_dict = None
        
        got_exception = False
        try:
            oauth2_return_from_dict = authentication.OAuth2Return.from_dict(oauth2_return_dict)
            oauth2_return_to_dict = oauth2_return_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(oauth2_return_to_dict , dict)
        self.assertEqual(oauth2_return_to_dict["access_token"], "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(oauth2_return_to_dict["expires_in"], 3600)
        self.assertEqual(oauth2_return_to_dict["token_type"], "Bearer")
        self.assertEqual(oauth2_return_to_dict["refresh_token"], "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(oauth2_return_to_dict["scope"], "access:A B C D")
        self.assertEqual(oauth2_return_to_dict["error"], "invalid_grant")


class OAuth2UnitTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_auth_token(self, mock_post):
        
        #
        self.logger.info('test_get_auth_token')

        self.logger.info('test: 200, success')

        credentials = authentication.OAuth2()
        
        credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')

        self.assertEqual(credentials.jwt_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(credentials.oauth2_return.access_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(credentials.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials.oauth2_return.refresh_token, "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(credentials.oauth2_return.scope, "access:A B C D")

        #
        self.logger.info('test: 200, invalid_grant')
        
        got_exception = False
        try:
            credentials.get_auth_token(api_key = 'incorrect_key')
            self.assertEqual(credentials.oauth2_return.error, "invalid_grant")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test: 200, wrong client id')
        
        got_exception = False
        try:
            credentials.client_id = 'wrong-client-id'
            credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
            self.assertEqual(credentials.oauth2_return.error, "invalid_client")
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        credentials.client_id = 'ibm-pairs'
        
        #
        self.logger.info('test: 404, wrong endpoint')
        
        got_exception = False
        try:
            credentials.endpoint = 'wrong.end.point'
            credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
        except Exception as ex:
            got_exception = True

        self.assertTrue(got_exception)
        
        credentials.endpoint = 'auth-b2b-twc.ibm.com'
        
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_refresh_auth_token(self, mock_post):
        
        #
        self.logger.info('test_refresh_auth_token')

        self.logger.info('test: 200, success')

        credentials = authentication.OAuth2()
        
        credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
        
        credentials.refresh_auth_token()
        
        self.assertEqual(credentials.jwt_token, "HNanna8s8hx8nsnDNXS2NONKNW4QKNXCNWnc8whWH0cwh8cH")
        self.assertEqual(credentials.oauth2_return.access_token, "HNanna8s8hx8nsnDNXS2NONKNW4QKNXCNWnc8whWH0cwh8cH")
        self.assertEqual(credentials.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials.oauth2_return.refresh_token, "J-xaooxmPWXopmcpqm0h80h8nicwonkoxnx0qxhj887")
        self.assertEqual(credentials.oauth2_return.scope, "access:A B C D")
        
        #
        self.logger.info('test: 200, invalid_grant')
        
        credentials = authentication.OAuth2()
        
        credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
        
        got_exception = False
        try:
            credentials.oauth2_return.refresh_token = "wrong-refresh-token"
            credentials.refresh_auth_token()
            self.assertEqual(credentials.oauth2_return.error, "invalid_grant")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test: 200, wrong client id')
        
        credentials = authentication.OAuth2()
        
        credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
        
        got_exception = False
        try:
            credentials.client_id = 'wrong-client-id'
            credentials.refresh_auth_token()
            self.assertEqual(credentials.oauth2_return.error, "invalid_client")
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test: 404, wrong endpoint')
        
        credentials = authentication.OAuth2()
        
        credentials.get_auth_token(api_key = 'PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd')
        
        got_exception = False
        try:
            credentials.endpoint = 'wrong.end.point'
            credentials.refresh_auth_token()
        except Exception as ex:
            got_exception = True

        self.assertTrue(got_exception)
        
    def test_from_dict(self):
        
        self.logger.info('test_from_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        
        oauth2 = authentication.OAuth2
                
        oauth2_from_dict = None
        
        got_exception = False
        try:
            oauth2_from_dict = oauth2.from_dict(oauth2_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_from_dict.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2_from_dict.username, "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_from_dict.api_key, "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd")
        self.assertEqual(oauth2_from_dict.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_dict.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_dict.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_dict.jwt_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        
    def test_to_dict(self):
        
        self.logger.info('test_to_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        
        oauth2_to_dict = None
        
        got_exception = False
        try:
            oauth2_from_dict = authentication.OAuth2.from_dict(oauth2_dict)
            oauth2_to_dict = oauth2_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(oauth2_to_dict , dict)
        self.assertEqual(oauth2_to_dict["host"], "pairs.res.ibm.com")
        self.assertEqual(oauth2_to_dict["username"], "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_to_dict["api_key"], "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd")
        self.assertEqual(oauth2_to_dict["api_key_file"], "ibmpairspass.txt")
        self.assertEqual(oauth2_to_dict["client_id"], "ibm-pairs")
        self.assertEqual(oauth2_to_dict["endpoint"], "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_to_dict["jwt_token"], "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")

class OAuth2HelperFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')

    #
    def test_oauth2_authentication_from_dict(self):
        
        self.logger.info('test_oauth2_authentication_from_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
    
        got_exception = False
        try:
            oauth2_from_dict = authentication.oauth2_authentication_from_dict(oauth2_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_from_dict.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2_from_dict.username, "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_from_dict.api_key, "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd")
        self.assertEqual(oauth2_from_dict.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_dict.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_dict.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_dict.jwt_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")

    #
    def test_oauth2_authentication_to_dict(self):
        
        self.logger.info('test_oauth2_authentication_to_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
    
        got_exception = False
        try:
            oauth2_from_dict = authentication.oauth2_authentication_from_dict(oauth2_dict)
            oauth2_to_dict = authentication.oauth2_authentication_to_dict(oauth2_from_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(oauth2_to_dict , dict)
        self.assertEqual(oauth2_to_dict["host"], "pairs.res.ibm.com")
        self.assertEqual(oauth2_to_dict["username"], "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_to_dict["api_key"], "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd")
        self.assertEqual(oauth2_to_dict["api_key_file"], "ibmpairspass.txt")
        self.assertEqual(oauth2_to_dict["client_id"], "ibm-pairs")
        self.assertEqual(oauth2_to_dict["endpoint"], "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_to_dict["jwt_token"], "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")

    #
    def test_oauth2_authentication_from_json(self):
        
        self.logger.info('test_oauth2_authentication_from_json')
        
        oauth2_str = r'''
        {
             "host" : "pairs.res.ibm.com",
             "username" : "TWCcustomersupport@us.ibm.com",
             "api_key" : "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd",
             "api_key_file" : "ibmpairspass.txt",
             "client_id" : "ibm-pairs",
             "endpoint" : "auth-b2b-twc.ibm.com",
             "jwt_token" : "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        }'''
    
        got_exception = False
        try:
            oauth2_from_json = authentication.oauth2_authentication_from_json(oauth2_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
        self.assertEqual(oauth2_from_json.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2_from_json.username, "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_from_json.api_key, "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd")
        self.assertEqual(oauth2_from_json.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_json.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_json.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_json.jwt_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")

    #
    def test_oauth2_authentication_to_json(self):
        
        self.logger.info('test_oauth2_authentication_to_json')
        
        oauth2_str = r'''
        {
             "host" : "pairs.res.ibm.com",
             "username" : "TWCcustomersupport@us.ibm.com",
             "api_key" : "PABUdniu33fu2NIODSNOmkfenw80hn0hdsh9NOSDInd",
             "api_key_file" : "ibmpairspass.txt",
             "client_id" : "ibm-pairs",
             "endpoint" : "auth-b2b-twc.ibm.com",
             "jwt_token" : "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        }'''

        got_exception = False
        try:
            oauth2_from_json = authentication.oauth2_authentication_from_json(oauth2_str)
            oauth2_to_json = authentication.oauth2_authentication_to_json(oauth2_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
    #
    #def test_get_oauth2_credentials():

    def test_oauth2_return_from_dict(self):
        
        self.logger.info('test_oauth2_return_from_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD"
        oauth2_return_dict["scope"]         = "access:A B C D"
        oauth2_return_dict["error"]         = "invalid_grant"
               
        got_exception = False
        try:
            oauth2_return_from_dict = authentication.oauth2_return_from_dict(oauth2_return_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_return_from_dict.access_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(oauth2_return_from_dict.expires_in, 3600)
        self.assertEqual(oauth2_return_from_dict.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_dict.refresh_token, "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(oauth2_return_from_dict.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_dict.error, "invalid_grant")
        
    def test_oauth2_return_to_dict(self):
        
        self.logger.info('test_oauth2_return_to_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD"
        oauth2_return_dict["scope"]         = "access:A B C D"
        oauth2_return_dict["error"]         = "invalid_grant"
        
        got_exception = False
        try:
            oauth2_return_from_dict = authentication.oauth2_return_from_dict(oauth2_return_dict)
            oauth2_return_to_dict = authentication.oauth2_return_to_dict(oauth2_return_from_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(oauth2_return_to_dict , dict)
        self.assertEqual(oauth2_return_to_dict["access_token"], "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(oauth2_return_to_dict["expires_in"], 3600)
        self.assertEqual(oauth2_return_to_dict["token_type"], "Bearer")
        self.assertEqual(oauth2_return_to_dict["refresh_token"], "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(oauth2_return_to_dict["scope"], "access:A B C D")
        self.assertEqual(oauth2_return_to_dict["error"], "invalid_grant")    

    #
    def test_oauth2_return_from_json(self):
        
        self.logger.info('test_oauth2_return_from_json')
        
        oauth2_return_str = r'''
        {
             "access_token" : "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO",
             "expires_in" : 3600,
             "token_type" : "Bearer",
             "refresh_token" : "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD",
             "scope" : "access:A B C D",
             "error" : "invalid_grant"
        }'''

        got_exception = False
        try:
            oauth2_return_from_json = authentication.oauth2_return_from_json(oauth2_return_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_return_from_json.access_token, "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO")
        self.assertEqual(oauth2_return_from_json.expires_in, 3600)
        self.assertEqual(oauth2_return_from_json.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_json.refresh_token, "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD")
        self.assertEqual(oauth2_return_from_json.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_json.error, "invalid_grant")
 
    #
    def test_oauth2_return_to_json(self):
        
        self.logger.info('test_oauth2_return_to_json')
        
        oauth2_return_str = r'''
        {
             "access_token" : "MDASPcnivo8enPCSnadPNC8PNC8D9PNV8DPNVDS8DNVPASCO",
             "expires_in" : 3600,
             "token_type" : "Bearer",
             "refresh_token" : "8dh0oNDIWONIOWNM-NDNNIondini0_nidoidoimioJD",
             "scope" : "access:A B C D",
             "error" : "invalid_grant"
        }'''

        got_exception = False
        try:
            oauth2_return_from_json = authentication.oauth2_return_from_json(oauth2_return_str)
            oauth2_to_json = authentication.oauth2_return_to_json(oauth2_return_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
