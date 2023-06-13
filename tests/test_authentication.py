"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# Please note, none of the values in this unit test module are, or have even been, valid to access the system.

# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
import os
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

class BasicUnitTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')
    
    def test_basic_init(self):
        self.logger.info('test_basic_init')
        
        got_exception = False
        
        try:
            basic = authentication.Basic(username = "email@domain.com",
                                         password = "thisisnotapassword")
            basic.host          = "https://pairs.res.ibm.com"
            basic.username      = "email@domain.com"
            basic.password      = "thisisnotapassword"
            basic.password_file = "auth/basic.txt"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(basic.host, "pairs.res.ibm.com")
        self.assertEqual(basic.username, "email@domain.com")
        self.assertEqual(basic.password, "thisisnotapassword")
        cwd = os.getcwd()
        self.assertEqual(basic.password_file, cwd + "/auth/basic.txt")
        
        self.logger.info('test_basic_init: file find password')
        
        self.logger.info('writing \'basic-unittest.txt\'')
        f = open("basic-unittest.txt", "a")
        f.write("pairs.res.ibm.com:email@domain.com:thisisnotapassword")
        f.close()
        
        credentials2 = None
        
        try:
            credentials2 = authentication.Basic(password_file = 'basic-unittest.txt',
                                                username      = 'email@domain.com')
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(credentials2.username, "email@domain.com")
        self.assertEqual(credentials2.password, "thisisnotapassword")

        self.logger.info('removing \'basic-unittest.txt\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'basic-unittest.txt')):
            os.remove(os.path.join(os.getcwd(), 'basic-unittest.txt'))
        
        self.logger.info('test_basic_init: password is present')
        
        credentials3 = None
        
        try:
            credentials3 = authentication.Basic(username = 'email@domain.com',
                                                password = 'thisisnotapassword')
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(credentials3.username, "email@domain.com")
        self.assertEqual(credentials3.password, "thisisnotapassword")
        
        self.logger.info('test_oauth2_init: no api_key')
        
        credentials4 = None
        
        try:
            credentials4 = authentication.Basic(password = 'abc')
        except Exception as ex:
            self.assertEqual(str(ex), "AUTHENTICATION FAILED: A username and password could not be gathered from the provided attributes.")
            got_exception = True
            
        self.assertTrue(got_exception)
        
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

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
            
            if input_data_dict.get("apiKey") is not None:
                api_key = input_data_dict["apiKey"]
        
            if input_data_dict.get("api_key") is not None:
                api_key = input_data_dict["api_key"]
                
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
            return MockResponse({"error":"unsupported_grant_type"}, 200)
    elif (url == 'https://iam.cloud.ibm.com/identity/token'):

        iam_api_key = remove_prefix(input_data, "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=")
        
        if (iam_api_key == 'thisisnotanapikey'):
            return_dict = {}
            return_dict["access_token"]  = "thisisnotanaccesstoken"
            return_dict["expiration"]    = 1000000000
            return_dict["expires_in"]    = 3600
            return_dict["token_type"]    = "Bearer"
            return_dict["refresh_token"] = "not_supported"
            return_dict["scope"]         = "xxx xxx"
        
            return MockResponse(return_dict, 200)
        else:
            return_dict = {}
            return_dict["errorCode"]  = "BXNIM0415E"
            return_dict["errorCode"]  = "Provided API key could not be found."
            context_dict = {}
            context_dict["requestId"]  = "XXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            context_dict["requestType"]  = "incoming.Identity_Token"
            context_dict["userAgent"]  = "python-requests/2.28.1"
            context_dict["url"]  = "https://iam.cloud.ibm.com"
            context_dict["instanceId"]  = "XXXXX-XXXXX-XXXXX-XXXXX"
            context_dict["threadId"]  = "XXXXXX"
            context_dict["host"]  = "XXXXX-XXXXX-XXXXX-XXXXX"
            context_dict["startTime"]  = "01.01.1970 00:00:00:000 GMT"
            context_dict["elapsedTime"]  = "0"
            context_dict["locale"]  = "en_US"
            context_dict["clusterName"]  = "XXXXX-XXXXX-XXXXX-XXXXX"
            return_dict["context"] = context_dict
            
            return MockResponse(return_dict, 500)
        
    return MockResponse(None, 404)

def mocked_requests_get(*args, **kwargs):

    url = args[0]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code
            
        def json(self):
            return self.json_data
    
    if (url == 'https://api.ibm.com/saascore/run/authentication-retrieve?orgId=thisisnotanorgid'):
        return MockResponse("thisisnotanaccesstoken", 200)
    elif (url == 'https://api.ibm.com/saascore/run/authentication-retrieve?orgId=2'):
        return MockResponse({"httpCode":"500","httpMessage":"External Dependency (process-guut-response)","moreInformation":"Unable to retrieve organization. Status code: 404. myOrganizationMembershipInfoByOrganization.body: {\"errors\":[\"404 NOT_FOUND \\\"No existing organization with this ID 3418fa7d-b57a-4666-8cf0-0a27c271dfcc.\\\"\"]}"}, 500)
    elif (url == 'https://api.ibm.com/saascore/run/authentication-retrieve?orgId=3'):
        return MockResponse({"httpCode":"401","httpMessage":"Unauthorized","moreInformation":"Invalid client id or secret."}, 401)

class OAuth2ReturnUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')
    
    def test_from_dict(self):
        
        self.logger.info('test_from_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "thisisnotanaccesstoken"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "thisisnotarefreshtoken"
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
        self.assertEqual(oauth2_return_from_dict.access_token, "thisisnotanaccesstoken")
        self.assertEqual(oauth2_return_from_dict.expires_in, 3600)
        self.assertEqual(oauth2_return_from_dict.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_dict.refresh_token, "thisisnotarefreshtoken")
        self.assertEqual(oauth2_return_from_dict.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_dict.error, "invalid_grant")
        
    def test_to_dict(self):
        
        self.logger.info('test_to_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "thisisnotanaccesstoken"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "thisisnotarefreshtoken"
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
        self.assertEqual(oauth2_return_to_dict["access_token"], "thisisnotanaccesstoken")
        self.assertEqual(oauth2_return_to_dict["expires_in"], 3600)
        self.assertEqual(oauth2_return_to_dict["token_type"], "Bearer")
        self.assertEqual(oauth2_return_to_dict["refresh_token"], "thisisnotarefreshtoken")
        self.assertEqual(oauth2_return_to_dict["scope"], "access:A B C D")
        self.assertEqual(oauth2_return_to_dict["error"], "invalid_grant")


class OAuth2UnitTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')
    
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_oauth2_init(self, mock_post):
        self.logger.info('test_oauth2_init')
        
        got_exception = False
        
        try:
            oauth2 = authentication.OAuth2(api_key = 'thisisnotanapikey')
            oauth2.host         = "https://pairs.res.ibm.com"
            oauth2.username     = "email@domain.com"
            oauth2.api_key      = "thisisnotanapikey"
            oauth2.api_key_file = "auth/oauth2.txt"
            oauth2.client_id    = "ibm-pairs"
            oauth2.tenant_id    = "thisisnotatenantid"
            oauth2.org_id       = "thisisnotanorgid"
            oauth2.endpoint     = "auth-b2b-twc.ibm.com"
            oauth2.iam_endpoint = "iam.cloud.ibm.com"
            oauth2.jwt_token    = "thisisnotajwttoken"
            oauth2.legacy       = False
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(oauth2.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2.username, "email@domain.com")
        self.assertEqual(oauth2.api_key, "thisisnotanapikey")
        cwd = os.getcwd()
        self.assertEqual(oauth2.api_key_file, cwd + "/auth/oauth2.txt")
        self.assertEqual(oauth2.client_id, "ibm-pairs")
        self.assertEqual(oauth2.tenant_id, "thisisnotatenantid")
        self.assertEqual(oauth2.org_id, "thisisnotanorgid")
        self.assertEqual(oauth2.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2.iam_endpoint, "iam.cloud.ibm.com")
        self.assertEqual(oauth2.jwt_token, "thisisnotajwttoken")
        self.assertEqual(oauth2.legacy, False)
        
        self.logger.info('test_oauth2_init: file find api_key')
        
        self.logger.info('writing \'oauth2-unittest.txt\'')
        f = open("oauth2-unittest.txt", "a")
        f.write("pairs.res.ibm.com:email@domain.com:thisisnotanapikey")
        f.close()
        
        credentials2 = None
        
        try:
            credentials2 = authentication.OAuth2(api_key_file = 'oauth2-unittest.txt',
                                                username     = 'email@domain.com')
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(credentials2.jwt_token, "thisisnotanaccesstoken")

        self.logger.info('removing \'oauth2-unittest.txt\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'oauth2-unittest.txt')):
            os.remove(os.path.join(os.getcwd(), 'oauth2-unittest.txt'))
        
        self.logger.info('test_oauth2_init: api_key is present')
        
        credentials3 = None
        
        try:
            credentials3 = authentication.OAuth2(api_key = 'thisisnotanapikey')
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(credentials3.jwt_token, "thisisnotanaccesstoken")
        
        self.logger.info('test_oauth2_init: no api_key')
        
        credentials4 = None
        
        try:
            credentials4 = authentication.OAuth2(api_key = 'thisisnotavalidapikey')
        except Exception as ex:
            self.assertEqual(str(ex), "AUTHENTICATION FAILED: A JWT token could not be gathered from the provided attributes.")
            got_exception = True
            
        self.assertTrue(got_exception)
        

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_auth_token(self, mock_post):
        
        #
        self.logger.info('test_get_auth_token')

        self.logger.info('test: 200, success')

        got_exception = False
        
        try:
            credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
            credentials.get_auth_token(api_key = 'thisisnotanapikey')
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)

        self.assertEqual(credentials.jwt_token, "thisisnotanaccesstoken")
        self.assertEqual(credentials.oauth2_return.access_token, "thisisnotanaccesstoken")
        self.assertEqual(credentials.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials.oauth2_return.refresh_token, "thisisnotarefreshtoken")
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
            credentials.get_auth_token(api_key = 'thisisnotanapikey')
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
            credentials.get_auth_token(api_key = 'thisisnotanapikey')
        except Exception as ex:
            got_exception = True

        self.assertTrue(got_exception)
        
        credentials.endpoint = 'auth-b2b-twc.ibm.com'

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_refresh_auth_token(self, mock_post):
        
        #
        self.logger.info('test_refresh_auth_token')

        self.logger.info('test_refresh_auth_token: 200, success')
        
        got_exception = False
        try:
            credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
            credentials.refresh_auth_token()
        except:
           got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(credentials.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(credentials.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(credentials.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials.oauth2_return.refresh_token, "thisisnotanewrefreshtoken")
        self.assertEqual(credentials.oauth2_return.scope, "access:A B C D")
        
        #
        self.logger.info('test_refresh_auth_token: 200, invalid_grant')
        
        credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
        
        got_exception = False
        try:
            credentials.oauth2_return.refresh_token = "wrong-refresh-token"
            credentials.refresh_auth_token()
            self.assertEqual(credentials.oauth2_return.error, "invalid_grant")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test_refresh_auth_token: 200, wrong client id')
        
        credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
        
        got_exception = False
        try:
            credentials.client_id = 'wrong-client-id'
            credentials.refresh_auth_token()
            self.assertEqual(credentials.oauth2_return.error, "invalid_client")
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test_refresh_auth_token: 404, wrong endpoint')
        
        credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
        
        got_exception = False
        try:
            credentials.endpoint = 'wrong.end.point'
            credentials.refresh_auth_token()
        except Exception as ex:
            got_exception = True

        self.assertTrue(got_exception)
        
    @mock.patch('requests.get', 
                side_effect=mocked_requests_get
               )
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_get_api_connect_auth_token(self, mock_post, mock_get):
        
        #
        self.logger.info('test_get_api_connect_auth_token')
        
        self.logger.info('test_get_api_connect_auth_token: 200, success')
        
        got_exception = False
        
        try:
            credentials_api_connect = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                                            tenant_id = 'thisisnotatenantid',
                                                            org_id = 'thisisnotanorgid',
                                                            legacy = False
                                                           )
            
            credentials_api_connect.get_auth_token(api_key = 'thisisnotanapikey',
                                                   tenant_id = 'thisisnotatenantid',
                                                   org_id = 'thisisnotanorgid'
                                              )
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        
        self.assertEqual(credentials_api_connect.client_id, "saascore-thisisnotatenantid")
        self.assertEqual(credentials_api_connect.tenant_id, "thisisnotatenantid")
        self.assertEqual(credentials_api_connect.org_id, "thisisnotanorgid")
        self.assertEqual(credentials_api_connect.endpoint, "api.ibm.com")
        self.assertEqual(credentials_api_connect.host, "api.ibm.com/geospatial/run/na/pairs-query")
        self.assertEqual(credentials_api_connect.iam_endpoint, "iam.cloud.ibm.com")
        self.assertEqual(credentials_api_connect.legacy, False)
        
        self.assertEqual(credentials_api_connect.jwt_token, "thisisnotanaccesstoken")
        self.assertEqual(credentials_api_connect.oauth2_return.access_token, "thisisnotanaccesstoken")
        self.assertEqual(credentials_api_connect.oauth2_return.expiration, 1000000000)
        self.assertEqual(credentials_api_connect.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials_api_connect.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials_api_connect.oauth2_return.refresh_token, "not_supported")
        self.assertEqual(credentials_api_connect.oauth2_return.scope, "xxx xxx")
        
        #
        self.logger.info('test_get_api_connect_auth_token: 200, invalid_grant')
        
        got_exception = False
        try:
            credentials_api_connect.get_auth_token(api_key = 'incorrect_key',
                                                   tenant_id = 'thisisnotatenantid',
                                                   org_id = 'thisisnotanorgid',
                                                   legacy = False
                                                  )
            self.assertEqual(credentials_api_connect.oauth2_return.error, "BXNIM0415E Provided API key could not be found.")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test_get_api_connect_auth_token: 200, wrong client id')
        
        got_exception = False
        try:
            credentials_api_connect.client_id = 'wrong-client-id'
            credentials_api_connect.get_auth_token(api_key = 'thisisnotanapikey')
            self.assertEqual(credentials_api_connect.oauth2_return.error, "Unauthorized: Invalid client id or secret.")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        credentials_api_connect.client_id = 'saascore-thisisnotatenantid'
        
        #
        self.logger.info('test_get_api_connect_auth_token: 404, wrong endpoint')
        
        got_exception = False
        try:
            credentials_api_connect.endpoint = 'wrong.end.point'
            credentials_api_connect.get_auth_token(api_key = 'thisisnotanapikey')
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        credentials_api_connect.endpoint = 'api.ibm.com'
    '''
    @mock.patch('requests.get', 
                side_effect=mocked_requests_get
               )
    @mock.patch('requests.post', 
                side_effect=mocked_requests_post
               )
    def test_get_api_connect_refresh_token(self, mock_post):
        
        #
        self.logger.info('test_get_api_connect_refresh_token')
        
        self.logger.info('test_get_api_connect_refresh_token: 200, success')
        
        got_exception = False
        try:
            credentials_api_connect = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                                            tenant_id = 'thisisnotatenantid',
                                                            org_id = 'thisisnotanorgid',
                                                            legacy = False
                                                           )
            credentials_api_connect.refresh_auth_token()
        except:
           got_exception = True
            
        self.assertFalse(got_exception)
        
        self.assertEqual(credentials_api_connect.client_id, "saascore-thisisnotatenantid")
        self.assertEqual(credentials_api_connect.tenant_id, "thisisnotatenantid")
        self.assertEqual(credentials_api_connect.org_id, "thisisnotanorgid")
        self.assertEqual(credentials_api_connect.endpoint, "api.ibm.com")
        self.assertEqual(credentials_api_connect.host, "api.ibm.com/geospatial/run/na/pairs-query")
        self.assertEqual(credentials_api_connect.iam_endpoint, "iam.cloud.ibm.com")
        self.assertEqual(credentials_api_connect.legacy, False)
        
        self.assertEqual(credentials_api_connect.jwt_token, "thisisnotanewaccesstoken")
        self.assertEqual(credentials_api_connect.oauth2_return.access_token, "thisisnotanewaccesstoken")
        self.assertEqual(credentials_api_connect.oauth2_return.expiration, 1000000000)
        self.assertEqual(credentials_api_connect.oauth2_return.expires_in, 3600)
        self.assertEqual(credentials_api_connect.oauth2_return.token_type, "Bearer")
        self.assertEqual(credentials_api_connect.oauth2_return.refresh_token, "not_supported")
        self.assertEqual(credentials_api_connect.oauth2_return.scope, "xxx xxx")
        
        #
        self.logger.info('test_get_api_connect_refresh_token: 200, invalid_grant')
        
        credentials_api_connect = authentication.OAuth2(api_key = 'thisisnotanapikey',
                                                        tenant_id = 'thisisnotatenantid',
                                                        org_id = 'thisisnotanorgid',
                                                        legacy = False
                                                       )
        
        got_exception = False
        try:
            credentials_api_connect.oauth2_return.refresh_token = "wrong-refresh-token"
            credentials_api_connect.refresh_auth_token()
            self.assertEqual(credentials_api_connect.oauth2_return.error, "BXNIM0415E Provided API key could not be found.")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test_get_api_connect_refresh_token: 200, wrong client id')
        
        credentials = authentication.OAuth2(api_key = 'thisisnotanapikey')
        
        got_exception = False
        try:
            credentials_api_connect.client_id = 'wrong-client-id'
            credentials_api_connect.refresh_auth_token()
            self.assertEqual(credentials_api_connect.oauth2_return.error, "Unauthorized: Invalid client id or secret.")
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
        
        #
        self.logger.info('test_get_api_connect_refresh_token: 404, wrong endpoint')
        
        credentials_api_connect = authentication.OAuth2(api_key = 'thisisnotanapikey')
        
        got_exception = False
        try:
            credentials_api_connect.endpoint = 'wrong.end.point'
            credentials_api_connect.refresh_auth_token()
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(got_exception)
    '''
        
    def test_from_dict(self):
        
        self.logger.info('test_from_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "thisisnotanapikey"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "thisisnotanaccesstoken"
        
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
        self.assertEqual(oauth2_from_dict.api_key, "thisisnotanapikey")
        self.assertEqual(oauth2_from_dict.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_dict.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_dict.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_dict.jwt_token, "thisisnotanaccesstoken")
        
    def test_to_dict(self):
        
        self.logger.info('test_to_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "thisisnotanapikey"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "thisisnotanaccesstoken"
        
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
        self.assertEqual(oauth2_to_dict["api_key"], "thisisnotanapikey")
        self.assertEqual(oauth2_to_dict["api_key_file"], "ibmpairspass.txt")
        self.assertEqual(oauth2_to_dict["client_id"], "ibm-pairs")
        self.assertEqual(oauth2_to_dict["endpoint"], "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_to_dict["jwt_token"], "thisisnotanaccesstoken")

class OAuth2HelperFunctionsTest(unittest.TestCase):

    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    def tearDown(self):
        self.logger.info('teardown')

    #
    def test_oauth2_from_dict(self):
        
        self.logger.info('test_oauth2_from_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "thisisnotanapikey"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "thisisnotanaccesstoken"
    
        got_exception = False
        try:
            oauth2_from_dict = authentication.oauth2_from_dict(oauth2_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_from_dict.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2_from_dict.username, "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_from_dict.api_key, "thisisnotanapikey")
        self.assertEqual(oauth2_from_dict.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_dict.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_dict.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_dict.jwt_token, "thisisnotanaccesstoken")

    #
    def test_oauth2_to_dict(self):
        
        self.logger.info('test_oauth2_to_dict')
        
        oauth2_dict = {}
        oauth2_dict["host"]         = "pairs.res.ibm.com"
        oauth2_dict["username"]     = "TWCcustomersupport@us.ibm.com"
        oauth2_dict["api_key"]      = "thisisnotanapikey"
        oauth2_dict["api_key_file"] = "ibmpairspass.txt"
        oauth2_dict["client_id"]    = "ibm-pairs"
        oauth2_dict["endpoint"]     = "auth-b2b-twc.ibm.com"
        oauth2_dict["jwt_token"]    = "thisisnotanaccesstoken"
    
        got_exception = False
        try:
            oauth2_from_dict = authentication.oauth2_from_dict(oauth2_dict)
            oauth2_to_dict = authentication.oauth2_to_dict(oauth2_from_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(oauth2_to_dict , dict)
        self.assertEqual(oauth2_to_dict["host"], "pairs.res.ibm.com")
        self.assertEqual(oauth2_to_dict["username"], "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_to_dict["api_key"], "thisisnotanapikey")
        self.assertEqual(oauth2_to_dict["api_key_file"], "ibmpairspass.txt")
        self.assertEqual(oauth2_to_dict["client_id"], "ibm-pairs")
        self.assertEqual(oauth2_to_dict["endpoint"], "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_to_dict["jwt_token"], "thisisnotanaccesstoken")

    #
    def test_oauth2_from_json(self):
        
        self.logger.info('test_oauth2_from_json')
        
        oauth2_str = r'''
        {
             "host" : "pairs.res.ibm.com",
             "username" : "TWCcustomersupport@us.ibm.com",
             "api_key" : "thisisnotanapikey",
             "api_key_file" : "ibmpairspass.txt",
             "client_id" : "ibm-pairs",
             "endpoint" : "auth-b2b-twc.ibm.com",
             "jwt_token" : "thisisnotanaccesstoken"
        }'''
    
        got_exception = False
        try:
            oauth2_from_json = authentication.oauth2_from_json(oauth2_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
        self.assertEqual(oauth2_from_json.host, "pairs.res.ibm.com")
        self.assertEqual(oauth2_from_json.username, "TWCcustomersupport@us.ibm.com")
        self.assertEqual(oauth2_from_json.api_key, "thisisnotanapikey")
        self.assertEqual(oauth2_from_json.api_key_file, "ibmpairspass.txt")
        self.assertEqual(oauth2_from_json.client_id, "ibm-pairs")
        self.assertEqual(oauth2_from_json.endpoint, "auth-b2b-twc.ibm.com")
        self.assertEqual(oauth2_from_json.jwt_token, "thisisnotanaccesstoken")

    #
    def test_oauth2_to_json(self):
        
        self.logger.info('test_oauth2_to_json')
        
        oauth2_str = r'''
        {
             "host" : "pairs.res.ibm.com",
             "username" : "TWCcustomersupport@us.ibm.com",
             "api_key" : "thisisnotanapikey",
             "api_key_file" : "ibmpairspass.txt",
             "client_id" : "ibm-pairs",
             "endpoint" : "auth-b2b-twc.ibm.com",
             "jwt_token" : "thisisnotanaccesstoken"
        }'''

        got_exception = False
        try:
            oauth2_from_json = authentication.oauth2_from_json(oauth2_str)
            oauth2_to_json = authentication.oauth2_to_json(oauth2_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
    #
    #def test_get_oauth2_credentials():

    def test_oauth2_return_from_dict(self):
        
        self.logger.info('test_oauth2_return_from_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "thisisnotanaccesstoken"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "thisisnotarefreshtoken"
        oauth2_return_dict["scope"]         = "access:A B C D"
        oauth2_return_dict["error"]         = "invalid_grant"
               
        got_exception = False
        try:
            oauth2_return_from_dict = authentication.oauth2_return_from_dict(oauth2_return_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_return_from_dict.access_token, "thisisnotanaccesstoken")
        self.assertEqual(oauth2_return_from_dict.expires_in, 3600)
        self.assertEqual(oauth2_return_from_dict.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_dict.refresh_token, "thisisnotarefreshtoken")
        self.assertEqual(oauth2_return_from_dict.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_dict.error, "invalid_grant")
        
    def test_oauth2_return_to_dict(self):
        
        self.logger.info('test_oauth2_return_to_dict')
        
        oauth2_return_dict = {}
        oauth2_return_dict["access_token"]  = "thisisnotanaccesstoken"
        oauth2_return_dict["expires_in"]    = 3600
        oauth2_return_dict["token_type"]    = "Bearer"
        oauth2_return_dict["refresh_token"] = "thisisnotarefreshtoken"
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
        self.assertEqual(oauth2_return_to_dict["access_token"], "thisisnotanaccesstoken")
        self.assertEqual(oauth2_return_to_dict["expires_in"], 3600)
        self.assertEqual(oauth2_return_to_dict["token_type"], "Bearer")
        self.assertEqual(oauth2_return_to_dict["refresh_token"], "thisisnotarefreshtoken")
        self.assertEqual(oauth2_return_to_dict["scope"], "access:A B C D")
        self.assertEqual(oauth2_return_to_dict["error"], "invalid_grant")    

    #
    def test_oauth2_return_from_json(self):
        
        self.logger.info('test_oauth2_return_from_json')
        
        oauth2_return_str = r'''
        {
             "access_token" : "thisisnotanaccesstoken",
             "expires_in" : 3600,
             "token_type" : "Bearer",
             "refresh_token" : "thisisnotarefreshtoken",
             "scope" : "access:A B C D",
             "error" : "invalid_grant"
        }'''

        got_exception = False
        try:
            oauth2_return_from_json = authentication.oauth2_return_from_json(oauth2_return_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(oauth2_return_from_json.access_token, "thisisnotanaccesstoken")
        self.assertEqual(oauth2_return_from_json.expires_in, 3600)
        self.assertEqual(oauth2_return_from_json.token_type, "Bearer")
        self.assertEqual(oauth2_return_from_json.refresh_token, "thisisnotarefreshtoken")
        self.assertEqual(oauth2_return_from_json.scope, "access:A B C D")
        self.assertEqual(oauth2_return_from_json.error, "invalid_grant")
 
    #
    def test_oauth2_return_to_json(self):
        
        self.logger.info('test_oauth2_return_to_json')
        
        oauth2_return_str = r'''
        {
             "access_token" : "thisisnotanaccesstoken",
             "expires_in" : 3600,
             "token_type" : "Bearer",
             "refresh_token" : "thisisnotarefreshtoken",
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
        