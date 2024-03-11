"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
import os
os.environ['QUERY_MIN_STATUS_INTERVAL'] = '1'
os.environ['QUERY_STATUS_CHECK_INTERVAL'] = '1'
from datetime import datetime
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
from ibmpairs.logger import logger
import ibmpairs.client as client
import ibmpairs.external.ibm as ibm_cos
import ibmpairs.query as query_module
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import responses
import unittest
from unittest import mock
import asyncio
import hashlib
import shutil
#}}}

# test_favorite, test_unfavorite
def mocked_favorite_requests_put(*args, **kwargs):
        
    identifier = None
    
    if kwargs.get("url") is not None:
        url = kwargs["url"]

        identifier = url[-1:]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
            
    if (identifier == '1'):        
        return_dict = {}
        return_dict["id"] = identifier
            
        return MockResponse(return_dict, 200)
    elif (identifier == '2'):
        return_dict = {}
        return_dict["message"] = "Error: 404 Not Found."
            
        return MockResponse(return_dict, 404)
    else:
        return_dict = {}
        return_dict["message"] = "Error: 401 Unauthorized."
            
        return MockResponse(return_dict, 401)
        
# test_async_submit
async def mocked_submit_async_post(*args, **kwargs):

    name = None
    
    if kwargs.get("body") is not None:

        input_data_dict = kwargs["body"]
        
        if input_data_dict.get("name") is not None:
            name = input_data_dict["name"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.body   = json_data
            self.status = status_code

        def json(self):
            return self.body
            
    if (name == '1'):        
        return_dict              = {}
        return_dict["id"]        = "1"
        return_dict["url"]       = "string"
        return_dict["data"]      = []
        data_dict                = {}
        data_dict["layerId"]     = 0
        data_dict["layerName"]   = "string"
        data_dict["dataset"]     = "string"
        data_dict["timestamp"]   = 0
        data_dict["longitude"]   = 0
        data_dict["latitude"]    = 0
        data_dict["region"]      = "string"
        data_dict["value"]       = "string"
        data_dict["unit"]        = "string"
        data_dict["property"]    = "string"
        data_dict["aggregation"] = "string"
        return_dict["data"].append(data_dict)
        
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 200)
    elif (name == '2'):
        return_dict = {}
        return_dict["message"]  = "Error: 404 Not Found."
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 404)
    elif (name == '3'):
        return_dict = None
            
        return MockResponse(return_dict, 502)
    elif (name == '1000000000_30000000'):
        return_dict              = {}
        return_dict["id"]        = '1000000000_30000000'
    
        return MockResponse(return_dict, 200)
    elif (name == '1625544000_31302646'):        
        return_dict              = {}
        return_dict["id"]        = '1625544000_31302646'
        return_dict["url"]       = "string"
        return_dict["data"]      = []
        data_dict                = {}
        data_dict["layerId"]     = 0
        data_dict["layerName"]   = "string"
        data_dict["dataset"]     = "string"
        data_dict["timestamp"]   = 0
        data_dict["longitude"]   = 0
        data_dict["latitude"]    = 0
        data_dict["region"]      = "string"
        data_dict["value"]       = "string"
        data_dict["unit"]        = "string"
        data_dict["property"]    = "string"
        data_dict["aggregation"] = "string"
        return_dict["data"].append(data_dict)
        
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 200)
    else:
        return_dict = {}
        return_dict["message"]  = "Error: 401 Unauthorized."
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 401)

# Queued(0)
# Initializing(1)
# Running(10)
# Writing(11)
# Packaging(12)
# Succeeded(20)
# NoDataFound(21)
# Killed(30)
# Deleted(31)
# Failed(40)
# FailedConversion(41)

#
query_status_response_dict_1 = {
    "id": "1",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

#
query_status_response_dict_2 = {
    "id": "2",
    "status": "NoDataFound(21)",
    "statusCode": 21
}

#
query_status_response_dict_3 = {
    "id": "3",
    "status": "Killed(30)",
    "statusCode": 30
}

#
query_status_response_dict_4 = {
    "id": "4",
    "status": "Deleted(31)",
    "statusCode": 31
}

#
query_status_response_dict_5 = {
    "id": "5",
    "status": "Failed(40)",
    "statusCode": 40
}

#
query_status_response_dict_6 = {
    "id": "6",
    "status": "FailedConversion(41)",
    "statusCode": 41
}

#
query_status_response_dict_10_1 = {
    "id": "10",
    "status": "Queued(0)",
    "statusCode": 0
}

#
query_status_response_dict_10_2 = {
    "id": "10",
    "status": "Initializing(1)",
    "statusCode": 1
}

#
query_status_response_dict_10_3 = {
    "id": "10",
    "status": "Running(10)",
    "statusCode": 10
}

#
query_status_response_dict_10_4 = {
    "id": "10",
    "status": "Writing(11)",
    "statusCode": 11
}

#
query_status_response_dict_10_5 = {
    "id": "10",
    "status": "Packaging(12)",
    "statusCode": 12
}

#
query_status_response_dict_11_1 = {
    "id": "11",
    "status": "Initializing(1)",
    "statusCode": 1
}

#
query_status_response_dict_11_2 = {
    "id": "11",
    "status": "Running(10)",
    "statusCode": 10
}

#
query_status_response_dict_13 = {
    "id": "1625544000_31302646",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

query_status_response_dict_1000000000_30000000 = {
    "id": "1000000000_30000000",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

poll_tracker_status = 0

# test_async_status
async def mocked_status_async_get(*args, **kwargs):
    
    global poll_tracker_status
    
    url = None
    
    if kwargs.get("url") is not None:
        url = kwargs["url"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.body   = json_data
            self.status = status_code

        def json(self):
            return self.body
            
    if (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1'): 
        return_json = json.dumps(query_status_response_dict_1)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/2'): 
        return_json = json.dumps(query_status_response_dict_2)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/3'): 
        return_json = json.dumps(query_status_response_dict_3)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/4'): 
        return_json = json.dumps(query_status_response_dict_4)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/5'): 
        return_json = json.dumps(query_status_response_dict_5)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/6'): 
        return_json = json.dumps(query_status_response_dict_6)
                   
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/7'):
        return_dict = {}
        return_dict["status"]  = "Error: 404 Not Found." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/8'):
        return_dict = {}
        return_dict["status"]  = "Error: 404 Not Found." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/9'):
        return_dict = {}
        return_dict["status"]  = "Error: 503 Service Unavailable." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 503)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/10'): 

        return_dict = {}

        if poll_tracker_status == 0:
            return_json = json.dumps(query_status_response_dict_10_1)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 1:
            return_json = json.dumps(query_status_response_dict_10_2)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 2:
            return_json = json.dumps(query_status_response_dict_10_3)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 3:
            return_json = json.dumps(query_status_response_dict_10_4)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 4:
            return_json = json.dumps(query_status_response_dict_10_5)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 5:
            return_json = json.dumps(query_status_response_dict_1)
            poll_tracker_status = 0
            return MockResponse(return_json, 200)
        else:
            return_dict["status"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/11'): 

        return_dict = {}

        if poll_tracker_status == 0:
            return_json = json.dumps(query_status_response_dict_11_1)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 1:
            return_json = json.dumps(query_status_response_dict_11_2)
            poll_tracker_status = poll_tracker_status + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_status == 2:
            return_json = json.dumps(query_status_response_dict_5)
            poll_tracker_status = 0
            return MockResponse(return_json, 200)
        else:
            return_dict["status"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/12'):
        return_dict["invalid"] = "return"
        return_json = json.dumps(return_dict)
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1000000000_30000000'):
        return_json = json.dumps(query_status_response_dict_1000000000_30000000)
        
        return MockResponse(return_json, 200)
    else:
        return_dict = {}
        return_dict["status"]  = "pass"
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 200) 

#
query_download_status_response_dict = {
    "id": "1625544000_31302646",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

#
query_download_status_response_csv_dict = {
    "id": "1702468800_05116057",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

#
query_download_status_response_json_dict = {
    "id": "1702468800_05212195",
    "status": "Succeeded(20)",
    "statusCode": 20,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "hadoopId": "string"
}

#
query_download_status_response_dict_success_1 = {
    "id": "1625544000_31302648",
    "status": "Running(10)",
    "statusCode": 10
}

query_download_status_response_dict_success_2 = {
    "id": "1625544000_31302648",
    "status": "Succeeded(20)",
    "statusCode": 20,
}

#
query_download_status_response_dict_fail_1 = {
    "id": "1625544000_31302649",
    "status": "Running(10)",
    "statusCode": 10
}

#
query_download_status_response_dict_fail_2 = {
    "id": "1625544000_31302649",
    "status": "Failed(40)",
    "statusCode": 40
}

#
query_download_status_response_dict_deleted = {
    "id": "1625544000_31302649",
    "status": "Deleted(31)",
    "statusCode": 31
}

query_online_response_1000000000_30000000 = {"data": "1,2,3\na,b,c"}

poll_tracker_download = 0
        
# test_async_download
async def mocked_download_async_get(*args, **kwargs):
    
    global poll_tracker_download
    
    url = None
    
    if kwargs.get("url") is not None:
        url = kwargs["url"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.body   = json_data
            self.status = status_code

        def json(self):
            return self.body
            
    if (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302646'):
        return_json = json.dumps(query_download_status_response_dict)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302647'):
        return_json = json.dumps(query_download_status_response_dict)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302645'):
        return_json = json.dumps(query_download_status_response_dict)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1702468800_05116057'):
        return_json = json.dumps(query_download_status_response_csv_dict)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1702468800_05212195'):
        return_json = json.dumps(query_download_status_response_json_dict)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302648'): 

        return_dict = {}

        if poll_tracker_download == 0:
            return_json = json.dumps(query_download_status_response_dict_success_1)
            poll_tracker_download = poll_tracker_download + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_download == 1:
            return_json = json.dumps(query_download_status_response_dict_success_2)
            poll_tracker_status = 0
            return MockResponse(return_json, 200)
        else:
            return_dict["status"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302649'): 

        return_dict = {}

        if poll_tracker_download == 0:
            return_json = json.dumps(query_download_status_response_dict_fail_1)
            poll_tracker_download = poll_tracker_download + 1
            return MockResponse(return_json, 200)
        elif poll_tracker_download == 1:
            return_json = json.dumps(query_download_status_response_dict_fail_2)
            poll_tracker_status = 0
            return MockResponse(return_json, 200)
        else:
            return_dict["status"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302650'):
        return_json = json.dumps(query_download_status_response_dict_deleted)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1000000000_30000000'):
        return_json = json.dumps(query_status_response_dict_1000000000_30000000)
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302646/download'): 
        with open(os.path.join('tests/data/v2','1625544000_31302646.zip'), "rb") as zipfile:
            resp = zipfile.read()
        return MockResponse(resp, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1702468800_05116057/download'): 
        with open(os.path.join('tests/data/v2','1702468800_05116057.csv'), "rb") as csvfile:
            resp = csvfile.read()
        return MockResponse(resp, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1702468800_05212195/download'): 
        with open(os.path.join('tests/data/v2','1702468800_05212195.json'), "rb") as jsonfile:
            resp = jsonfile.read()
        return MockResponse(resp, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302647/download'): 
        # This is intended to mock a 'server error' init of MockResponse has no attribute status.
        return MockResponse(status = 401)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302645/download'): 
        # This is intended to produce an invalid zip, -> byte reader, rather than -> 'bytes'.
        with open(os.path.join('tests/data/v2','1625544000_31302646.zip'), "rb") as zipfile:
            resp = zipfile
        return MockResponse(resp, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1625544000_31302648/download'): 
        with open(os.path.join('tests/data/v2','1625544000_31302646.zip'), "rb") as zipfile:
            resp = zipfile.read()
        return MockResponse(resp, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1000000000_30000000/download'):
        resp = json.dumps(query_online_response_1000000000_30000000)
        return MockResponse(resp, 200)
    else:
        return_dict = {}
        return_dict["status"]  = "pass"
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 200)

query_jobs_list_merge_success = [
    {
        "datalayer": "string",
        "datalayer_id": "string",
        "dataset": "string",
        "dataset_id": 0,
        "geoserver_url": "string",
        "geoserver_ws": "string",
        "max": 0.1,
        "min": 0.1,
        "name": "1string",
        "style": "",
        "timestamp": 0,
        "type": "raster"
    },
    {
        "datalayer": "string",
        "datalayer_id": "string",
        "dataset": "string",
        "dataset_id": 0,
        "geoserver_url": "string",
        "geoserver_ws": "string",
        "max": 0.1,
        "min": 0.1,
        "name": "2string",
        "style": "",
        "timestamp": 0,
        "type": "raster"
    }
]

# test_merge
def mocked_merge_requests_put(*args, **kwargs):
        
    identifier = None
    
    if kwargs.get("url") is not None:
        url = kwargs["url"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
            
    if (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/1/merge/2'):
        
        return MockResponse(query_jobs_list_merge_success, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/2/merge/3'):
        return_dict = {}
        return_dict["message"] = "Error: 404 Not Found."
            
        return MockResponse(return_dict, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/3/merge/4'):
        return_dict = {}
        return_dict["message"] = "Error: 401 Unauthorized."
            
        return MockResponse(return_dict, 401)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/queryjobs/4/merge/5'):
        return_dict = {}
        return_dict["message"] = "Error: 412 Precondition Failed."
            
        return MockResponse(return_dict, 412)
    else:
        return_dict = {}
        return_dict["message"] = "Error: 503 Service Unavailable."
            
        return MockResponse(return_dict, 503)

aggregation_dict = {
    "aoi": [
        "string"
    ]
}

aggregation_json = r'''{
    "aoi": [
        "string"
    ]
}'''

#
class AggregationUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_aggregation_init(self):
        self.logger.info('test_aggregation_init')
        
        aggregation = query_module.Aggregation()
        
        got_exception = False
        
        try:
            aggregation.aoi = ["string", "string2"]
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(aggregation.aoi[0], "string")
        self.assertEqual(aggregation.aoi[1], "string2")

    #    
    def test_aggregation_from_dict(self):
        self.logger.info('test_aggregation_from_dict')
        
        aggregation = query_module.Aggregation

        aggregation_from_dict = None
            
        got_exception = False

        try:
            aggregation_from_dict = aggregation.from_dict(aggregation_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(aggregation_from_dict.aoi[0], "string")
        
    #    
    def test_aggregation_to_dict(self):
        self.logger.info('test_aggregation_from_dict')
        
        aggregation = query_module.Aggregation

        aggregation_from_dict = None
        aggregation_to_dict   = None
                
        got_exception = False

        try:
            aggregation_from_dict = aggregation.from_dict(aggregation_dict)
            aggregation_to_dict   = aggregation_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(aggregation_to_dict, dict)
        self.assertEqual(aggregation_to_dict["aoi"][0], "string")

    #
    def test_aggregation_from_json(self):
        self.logger.info('test_aggregation_from_json')

        aggregation = query_module.Aggregation
        
        aggregation_from_json = None

        got_exception = False

        try:
            aggregation_from_json = aggregation.from_json(aggregation_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(aggregation_from_json.aoi[0], "string")
    
    #
    def test_aggregation_to_json(self):
        self.logger.info('test_aggregation_to_json')
        
        aggregation = query_module.Aggregation
        
        aggregation_from_json = None
        aggregation_from_json = None

        got_exception = False
        
        try:
            aggregation_from_json = aggregation.from_json(aggregation_json)
            aggregation_to_json = aggregation_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
dimension_dict = {
    "name": "string",
    "value": "string",
    "operator": "EQ",
    "options": [
        "string"
    ]
}

dimension_json = r'''{
    "name": "string",
    "value": "string",
    "operator": "EQ",
    "options": [
        "string"
    ]
}'''

#
class DimensionUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_dimension_init(self):
        self.logger.info('test_dimension_init')
        
        dimension = query_module.Dimension()
        
        got_exception = False
        
        try:
            dimension.name     = "string"
            dimension.value    = "string"
            dimension.operator = "EQ"
            dimension.options  = ["string", "string2"]
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(dimension.name, "string")
        self.assertEqual(dimension.value, "string")
        self.assertEqual(dimension.operator, "EQ")
        self.assertEqual(dimension.options[0], "string")
        self.assertEqual(dimension.options[1], "string2")

    #    
    def test_dimension_from_dict(self):
        self.logger.info('test_dimension_from_dict')
        
        dimension = query_module.Dimension

        dimension_from_dict = None
            
        got_exception = False

        try:
            dimension_from_dict = dimension.from_dict(dimension_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(dimension_from_dict.name, "string")
        self.assertEqual(dimension_from_dict.value, "string")
        self.assertEqual(dimension_from_dict.operator, "EQ")
        self.assertEqual(dimension_from_dict.options[0], "string")
        
    #    
    def test_dimension_to_dict(self):
        self.logger.info('test_dimension_from_dict')
        
        dimension = query_module.Dimension

        dimension_from_dict = None
        dimension_to_dict   = None
                
        got_exception = False

        try:
            dimension_from_dict = dimension.from_dict(dimension_dict)
            dimension_to_dict   = dimension_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(dimension_to_dict, dict)
        self.assertEqual(dimension_to_dict["name"], "string")
        self.assertEqual(dimension_to_dict["value"], "string")
        self.assertEqual(dimension_to_dict["operator"], "EQ")
        self.assertEqual(dimension_to_dict["options"][0], "string")

    #
    def test_dimension_from_json(self):
        self.logger.info('test_dimension_from_json')

        dimension = query_module.Dimension
        
        dimension_from_json = None

        got_exception = False

        try:
            dimension_from_json = dimension.from_json(dimension_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(dimension_from_json.name, "string")
        self.assertEqual(dimension_from_json.value, "string")
        self.assertEqual(dimension_from_json.operator, "EQ")
        self.assertEqual(dimension_from_json.options[0], "string")
    
    #
    def test_dimension_to_json(self):
        self.logger.info('test_dimension_to_json')
        
        dimension = query_module.Dimension
        
        dimension_from_json = None
        dimension_to_json = None

        got_exception = False
        
        try:
            dimension_from_json = dimension.from_json(dimension_json)
            dimension_to_json = dimension_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

filter_dict = {
    "value": "string",
    "operator": "EQ",
    "expression": "EQ string"
}

filter_json = r'''{
    "value": "string",
    "operator": "EQ",
    "expression": "EQ string"
}'''

#
class FilterUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_filter_init(self):
        self.logger.info('test_filter_init')
        
        filter = query_module.Filter()
        
        got_exception = False
        
        try:
            filter.value      = "string"
            filter.operator   = "EQ"
            filter.expression = "EQ string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(filter.value, "string")
        self.assertEqual(filter.operator, "EQ")
        self.assertEqual(filter.expression, "EQ string")

    #    
    def test_filter_from_dict(self):
        self.logger.info('test_filter_from_dict')
        
        filter = query_module.Filter

        filter_from_dict = None
            
        got_exception = False

        try:
            filter_from_dict = filter.from_dict(filter_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(filter_from_dict.value, "string")
        self.assertEqual(filter_from_dict.operator, "EQ")
        self.assertEqual(filter_from_dict.expression, "EQ string")
        
    #    
    def test_filter_to_dict(self):
        self.logger.info('test_filter_from_dict')
        
        filter = query_module.Filter

        filter_from_dict = None
        filter_to_dict   = None
                
        got_exception = False

        try:
            filter_from_dict = filter.from_dict(filter_dict)
            filter_to_dict   = filter_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(filter_to_dict, dict)
        self.assertEqual(filter_to_dict["value"], "string")
        self.assertEqual(filter_to_dict["operator"], "EQ")
        self.assertEqual(filter_to_dict["expression"], "EQ string")

    #
    def test_filter_from_json(self):
        self.logger.info('test_filter_from_json')

        filter = query_module.Filter
        
        filter_from_json = None

        got_exception = False

        try:
            filter_from_json = filter.from_json(filter_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(filter_from_json.value, "string")
        self.assertEqual(filter_from_json.operator, "EQ")
        self.assertEqual(filter_from_json.expression, "EQ string")
    
    #
    def test_filter_to_json(self):
        self.logger.info('test_filter_to_json')
        
        filter = query_module.Filter
        
        filter_from_json = None
        filter_to_json = None

        got_exception = False
        
        try:
            filter_from_json = filter.from_json(filter_json)
            filter_to_json = filter_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

interval_dict = {
    "snapshot": "string",
    "end": "string",
    "start": "string"
}

interval_json = r'''{
    "snapshot": "string",
    "end": "string",
    "start": "string"
}'''

#
class IntervalUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_interval_init(self):
        self.logger.info('test_interval_init')
        
        interval = query_module.Interval()
        
        got_exception = False
        
        try:
            interval.snapshot = "string"
            interval.end      = "string"
            interval.start    = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(interval.snapshot, "string")
        self.assertEqual(interval.end, "string")
        self.assertEqual(interval.start, "string")

    #    
    def test_interval_from_dict(self):
        self.logger.info('test_interval_from_dict')
        
        interval = query_module.Interval

        interval_from_dict = None
            
        got_exception = False

        try:
            interval_from_dict = interval.from_dict(interval_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(interval_from_dict.snapshot, "string")
        self.assertEqual(interval_from_dict.end, "string")
        self.assertEqual(interval_from_dict.start, "string")
        
    #    
    def test_interval_to_dict(self):
        self.logger.info('test_interval_from_dict')
        
        interval = query_module.Interval

        interval_from_dict = None
        interval_to_dict   = None
                
        got_exception = False

        try:
            interval_from_dict = interval.from_dict(interval_dict)
            interval_to_dict   = interval_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(interval_to_dict, dict)
        self.assertEqual(interval_to_dict["snapshot"], "string")
        self.assertEqual(interval_to_dict["end"], "string")
        self.assertEqual(interval_to_dict["start"], "string")

    #
    def test_interval_from_json(self):
        self.logger.info('test_interval_from_json')

        interval = query_module.Interval
        
        interval_from_json = None

        got_exception = False

        try:
            interval_from_json = interval.from_json(interval_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(interval_from_json.snapshot, "string")
        self.assertEqual(interval_from_json.end, "string")
        self.assertEqual(interval_from_json.start, "string")
    
    #
    def test_interval_to_json(self):
        self.logger.info('test_interval_to_json')
        
        interval = query_module.Interval
        
        interval_from_json = None
        interval_to_json = None

        got_exception = False
        
        try:
            interval_from_json = interval.from_json(interval_json)
            interval_to_json = interval_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
temporal_dict = {
    "intervals": [
        {
            "snapshot": "string",
            "end": "string",
            "start": "string"
        }
    ]
}

temporal_json = r'''{
    "intervals": [
        {
            "snapshot": "string",
            "end": "string",
            "start": "string"
        }
    ]
}'''

#
class TemporalUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_temporal_init(self):
        self.logger.info('test_temporal_init')
        
        temporal = query_module.Temporal()
        
        got_exception = False
        
        try:
            interval = query_module.Interval()
            interval.snapshot = "string"
            interval.end = "string"
            interval.start = "string"
            interval_list = [interval]
            temporal.intervals = interval_list
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(temporal.intervals[0].snapshot, "string")
        self.assertEqual(temporal.intervals[0].end, "string")
        self.assertEqual(temporal.intervals[0].start, "string")

    #    
    def test_temporal_from_dict(self):
        self.logger.info('test_temporal_from_dict')
        
        temporal = query_module.Temporal

        temporal_from_dict = None
            
        got_exception = False

        try:
            temporal_from_dict = temporal.from_dict(temporal_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(temporal_from_dict.intervals[0].snapshot, "string")
        self.assertEqual(temporal_from_dict.intervals[0].end, "string")
        self.assertEqual(temporal_from_dict.intervals[0].start, "string")
        
    #    
    def test_temporal_to_dict(self):
        self.logger.info('test_temporal_from_dict')
        
        temporal = query_module.Temporal

        temporal_from_dict = None
        temporal_to_dict   = None
                
        got_exception = False

        try:
            temporal_from_dict = temporal.from_dict(temporal_dict)
            temporal_to_dict   = temporal_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(temporal_to_dict, dict)
        self.assertEqual(temporal_to_dict["intervals"][0]["snapshot"], "string")
        self.assertEqual(temporal_to_dict["intervals"][0]["end"], "string")
        self.assertEqual(temporal_to_dict["intervals"][0]["start"], "string")

    #
    def test_temporal_from_json(self):
        self.logger.info('test_temporal_from_json')

        temporal = query_module.Temporal
        
        temporal_from_json = None

        got_exception = False

        try:
            temporal_from_json = temporal.from_json(temporal_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(temporal_from_json.intervals[0].snapshot, "string")
        self.assertEqual(temporal_from_json.intervals[0].end, "string")
        self.assertEqual(temporal_from_json.intervals[0].start, "string")
    
    #
    def test_temporal_to_json(self):
        self.logger.info('test_temporal_to_json')
        
        temporal = query_module.Temporal
        
        temporal_from_json = None
        temporal_to_json = None

        got_exception = False
        
        try:
            temporal_from_json = temporal.from_json(temporal_json)
            temporal_to_json = temporal_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

layer_dict = {
    "id": "string",
    "type": "raster",
    "temporal": {
        "intervals": [
            {
                "snapshot": "string",
                "end": "string",
                "start": "string"
            }
        ]
    },
    "alias": "string",
    "filterOnly": True,
    "aggregation": "None",
    "filter": {
        "value": "string",
        "operator": "EQ"
    },
    "dimensions": [
        {
            "name": "string",
            "value": "string",
            "operator": "EQ",
            "options": [
                "string"
            ]
        }
    ],
    "expression": "string",
    "output": True
}

layer_json = r'''{
    "id": "string",
    "type": "raster",
    "temporal": {
        "intervals": [
            {
                "snapshot": "string",
                "end": "string",
                "start": "string"
            }
        ]
    },
    "alias": "string",
    "filterOnly": true,
    "aggregation": "None",
    "filter": {
        "value": "string",
        "operator": "EQ"
    },
    "dimensions": [
        {
            "name": "string",
            "value": "string",
            "operator": "EQ",
            "options": [
                "string"
            ]
        }
    ],
    "expression": "string",
    "output": true
}'''

#
class LayerUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_layer_init(self):
        self.logger.info('test_layer_init')
        
        layer = query_module.Layer()
        
        got_exception = False
        
        try:
            layer.id           = "string"
            layer.type         = "raster"
            temporal           = query_module.Temporal()
            interval           = query_module.Interval()
            interval.snapshot  = "string"
            interval.end       = "string"
            interval.start     = "string"
            interval_list      = [interval]
            temporal.intervals = interval_list
            layer.temporal     = temporal
            layer.alias        = "string"
            layer.filter_only  = True
            layer.aggregation  = "None"
            filter_            = query_module.Filter()
            filter_.value      = "string"
            filter_.operator   = "EQ"
            layer.filter       = filter_
            dimension          = query_module.Dimension()
            dimension.name     = "string"
            dimension.value    = "string"
            dimension.operator = "EQ"
            dimension.options  = ["string"]
            layer.dimensions   = [dimension]
            layer.expression   = "string"
            layer.output       = True
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(layer.id, "string")
        self.assertEqual(layer.type, "raster")
        self.assertEqual(layer.temporal.intervals[0].snapshot, "string")
        self.assertEqual(layer.temporal.intervals[0].end, "string")
        self.assertEqual(layer.temporal.intervals[0].start, "string")
        self.assertEqual(layer.alias, "string")
        self.assertEqual(layer.filter_only, True)
        self.assertEqual(layer.aggregation, "None")
        self.assertEqual(layer.filter.value, "string")
        self.assertEqual(layer.filter.operator, "EQ")
        self.assertEqual(layer.dimensions[0].name, "string")
        self.assertEqual(layer.dimensions[0].value, "string")
        self.assertEqual(layer.dimensions[0].operator, "EQ")
        self.assertEqual(layer.dimensions[0].options[0], "string")
        self.assertEqual(layer.expression, "string")
        self.assertEqual(layer.output, True)

    #    
    def test_layer_from_dict(self):
        self.logger.info('test_layer_from_dict')
        
        layer = query_module.Layer

        layer_from_dict = None
            
        got_exception = False

        try:
            layer_from_dict = layer.from_dict(layer_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(layer_from_dict.id, "string")
        self.assertEqual(layer_from_dict.type, "raster")
        self.assertEqual(layer_from_dict.temporal.intervals[0].snapshot, "string")
        self.assertEqual(layer_from_dict.temporal.intervals[0].end, "string")
        self.assertEqual(layer_from_dict.temporal.intervals[0].start, "string")
        self.assertEqual(layer_from_dict.alias, "string")
        self.assertEqual(layer_from_dict.filter_only, True)
        self.assertEqual(layer_from_dict.aggregation, "None")
        self.assertEqual(layer_from_dict.filter.value, "string")
        self.assertEqual(layer_from_dict.filter.operator, "EQ")
        self.assertEqual(layer_from_dict.dimensions[0].name, "string")
        self.assertEqual(layer_from_dict.dimensions[0].value, "string")
        self.assertEqual(layer_from_dict.dimensions[0].operator, "EQ")
        self.assertEqual(layer_from_dict.dimensions[0].options[0], "string")
        self.assertEqual(layer_from_dict.expression, "string")
        self.assertEqual(layer_from_dict.output, True)
        
    #    
    def test_layer_to_dict(self):
        self.logger.info('test_layer_from_dict')
        
        layer = query_module.Layer

        layer_from_dict = None
        layer_to_dict   = None
                
        got_exception = False

        try:
            layer_from_dict = layer.from_dict(layer_dict)
            layer_to_dict   = layer_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(layer_to_dict, dict)
        self.assertEqual(layer_to_dict["id"], "string")
        self.assertEqual(layer_to_dict["type"], "raster")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(layer_to_dict["alias"], "string")
        self.assertEqual(layer_to_dict["filter_only"], True)
        self.assertEqual(layer_to_dict["aggregation"], "None")
        self.assertEqual(layer_to_dict["filter"]["value"], "string")
        self.assertEqual(layer_to_dict["filter"]["operator"], "EQ")
        self.assertEqual(layer_to_dict["dimensions"][0]["name"], "string")
        self.assertEqual(layer_to_dict["dimensions"][0]["value"], "string")
        self.assertEqual(layer_to_dict["dimensions"][0]["operator"], "EQ")
        self.assertEqual(layer_to_dict["dimensions"][0]["options"][0], "string")
        self.assertEqual(layer_to_dict["expression"], "string")
        self.assertEqual(layer_to_dict["output"], True)
        
    #    
    def test_layer_to_dict_layer_post(self):
        self.logger.info('test_layer_from_dict_layer_post')
        
        layer = query_module.Layer

        layer_from_dict = None
        layer_to_dict   = None
                
        got_exception = False

        try:
            layer_from_dict = layer.from_dict(layer_dict)
            layer_to_dict   = layer_from_dict.to_dict_layer_post()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(layer_to_dict, dict)
        self.assertEqual(layer_to_dict["id"], "string")
        self.assertEqual(layer_to_dict["type"], "raster")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(layer_to_dict["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(layer_to_dict["alias"], "string")
        self.assertEqual(layer_to_dict["filterOnly"], True)
        self.assertEqual(layer_to_dict["aggregation"], "None")
        self.assertEqual(layer_to_dict["filter"]["value"], "string")
        self.assertEqual(layer_to_dict["filter"]["operator"], "EQ")
        self.assertEqual(layer_to_dict["dimensions"][0]["name"], "string")
        self.assertEqual(layer_to_dict["dimensions"][0]["value"], "string")
        self.assertEqual(layer_to_dict["dimensions"][0]["operator"], "EQ")
        self.assertEqual(layer_to_dict["dimensions"][0]["options"][0], "string")
        self.assertEqual(layer_to_dict["expression"], "string")
        self.assertEqual(layer_to_dict["output"], True)

    #
    def test_layer_from_json(self):
        self.logger.info('test_layer_from_json')

        layer = query_module.Layer
        
        layer_from_json = None

        got_exception = False

        try:
            layer_from_json = layer.from_json(layer_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(layer_from_json.id, "string")
        self.assertEqual(layer_from_json.type, "raster")
        self.assertEqual(layer_from_json.temporal.intervals[0].snapshot, "string")
        self.assertEqual(layer_from_json.temporal.intervals[0].end, "string")
        self.assertEqual(layer_from_json.temporal.intervals[0].start, "string")
        self.assertEqual(layer_from_json.alias, "string")
        self.assertEqual(layer_from_json.filter_only, True)
        self.assertEqual(layer_from_json.aggregation, "None")
        self.assertEqual(layer_from_json.filter.value, "string")
        self.assertEqual(layer_from_json.filter.operator, "EQ")
        self.assertEqual(layer_from_json.dimensions[0].name, "string")
        self.assertEqual(layer_from_json.dimensions[0].value, "string")
        self.assertEqual(layer_from_json.dimensions[0].operator, "EQ")
        self.assertEqual(layer_from_json.dimensions[0].options[0], "string")
        self.assertEqual(layer_from_json.expression, "string")
        self.assertEqual(layer_from_json.output, True)
    
    #
    def test_layer_to_json(self):
        self.logger.info('test_layer_to_json')
        
        layer = query_module.Layer
        
        layer_from_json = None
        layer_to_json = None

        got_exception = False
        
        try:
            layer_from_json = layer.from_json(layer_json)
            layer_to_json = layer_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
    #
    def test_layer_to_json_layer_post(self):
        self.logger.info('test_layer_to_json_layer_post')
        
        layer = query_module.Layer
        
        layer_from_json = None
        layer_to_json = None

        got_exception = False
        
        try:
            layer_from_json = layer.from_json(layer_json)
            layer_to_json = layer_from_json.to_json_layer_post()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

notification_dict = {
    "type": "rabbitmq",
    "host": "string",
    "queue": "string"
}

notification_json = r'''{
    "type": "rabbitmq",
    "host": "string",
    "queue": "string"
}'''

#
class NotificationUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_notification_init(self):
        self.logger.info('test_notification_init')
        
        notification = query_module.Notification()
        
        got_exception = False
        
        try:
            notification.type  = "rabbitmq"
            notification.host  = "string"
            notification.queue = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(notification.type, "rabbitmq")
        self.assertEqual(notification.host, "string")
        self.assertEqual(notification.queue, "string")

    #    
    def test_notification_from_dict(self):
        self.logger.info('test_notification_from_dict')
        
        notification = query_module.Notification

        notification_from_dict = None
            
        got_exception = False

        try:
            notification_from_dict = notification.from_dict(notification_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(notification_from_dict.type, "rabbitmq")
        self.assertEqual(notification_from_dict.host, "string")
        self.assertEqual(notification_from_dict.queue, "string")
        
    #    
    def test_notification_to_dict(self):
        self.logger.info('test_notification_from_dict')
        
        notification = query_module.Notification

        notification_from_dict = None
        notification_to_dict   = None
                
        got_exception = False

        try:
            notification_from_dict = notification.from_dict(notification_dict)
            notification_to_dict   = notification_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(notification_to_dict, dict)
        self.assertEqual(notification_to_dict["type"], "rabbitmq")
        self.assertEqual(notification_to_dict["host"], "string")
        self.assertEqual(notification_to_dict["queue"], "string")

    #
    def test_notification_from_json(self):
        self.logger.info('test_notification_from_json')

        notification = query_module.Notification
        
        notification_from_json = None

        got_exception = False

        try:
            notification_from_json = notification.from_json(notification_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(notification_from_json.type, "rabbitmq")
        self.assertEqual(notification_from_json.host, "string")
        self.assertEqual(notification_from_json.queue, "string")
    
    #
    def test_notification_to_json(self):
        self.logger.info('test_notification_to_json')
        
        notification = query_module.Notification
        
        notification_from_json = None
        notification_to_json = None

        got_exception = False
        
        try:
            notification_from_json = notification.from_json(notification_json)
            notification_to_json = notification_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
    
spatial_dict = {
    "type": "point",
    "aoi": "string",
    "coordinates": [
        0
    ],
    "aggregation": {
        "aoi": [
            "string"
        ]
    }
}

spatial_json = r'''{
    "type": "point",
    "aoi": "string",
    "coordinates": [
        0
    ],
    "aggregation": {
        "aoi": [
            "string"
        ]
    }
}'''
    
spatial_geojson_dict = {
    "type": "poly",
    "geojson": {
        "type": "Feature",
        "geometry": {"coordinates":[[[[-9.164699678818277,39.10329357870404],
            [-9.148221910727607,39.146135775739786],
            [-9.092197499219324,39.13295356126725],
            [-9.118561928164398,39.090111364231504],
            [-9.164699678818277,39.10329357870404]]]],
            "type":"MultiPolygon"
        }
    }
}

spatial_geojson_json = r'''{
    "type": "poly",
    "geojson": {
        "type": "Feature",
        "geometry": {"coordinates":[[[[-9.164699678818277,39.10329357870404],
            [-9.148221910727607,39.146135775739786],
            [-9.092197499219324,39.13295356126725],
            [-9.118561928164398,39.090111364231504],
            [-9.164699678818277,39.10329357870404]]]],
            "type":"MultiPolygon"
        }
    }
}'''

#
class SpatialUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_spatial_init(self):
        self.logger.info('test_spatial_init')
        
        spatial = query_module.Spatial()
        
        got_exception = False
        
        try:
            spatial.type        = "point"
            spatial.aoi         = "string"
            coordinates_list    = [0] 
            spatial.coordinates = coordinates_list
            aggregation         = query_module.Aggregation()
            aoi_list            = ["string"] 
            aggregation.aoi     = aoi_list
            spatial.aggregation = aggregation
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(spatial.type, "point")
        self.assertEqual(spatial.aoi, "string")
        self.assertEqual(spatial.coordinates[0], 0)
        self.assertEqual(spatial.aggregation.aoi[0], "string")

    #    
    def test_spatial_from_dict(self):
        self.logger.info('test_spatial_from_dict')
        
        spatial = query_module.Spatial

        spatial_from_dict = None
            
        got_exception = False

        try:
            spatial_from_dict = spatial.from_dict(spatial_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(spatial_from_dict.type, "point")
        self.assertEqual(spatial_from_dict.aoi, "string")
        self.assertEqual(spatial_from_dict.coordinates[0], 0)
        self.assertEqual(spatial_from_dict.aggregation.aoi[0], "string")
        
    #    
    def test_spatial_to_dict(self):
        self.logger.info('test_spatial_from_dict')
        
        spatial = query_module.Spatial

        spatial_from_dict = None
        spatial_to_dict   = None
                
        got_exception = False

        try:
            spatial_from_dict = spatial.from_dict(spatial_dict)
            spatial_to_dict   = spatial_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(spatial_to_dict, dict)
        self.assertEqual(spatial_to_dict["type"], "point")
        self.assertEqual(spatial_to_dict["aoi"], "string")
        self.assertEqual(spatial_to_dict["coordinates"][0], 0)
        self.assertEqual(spatial_to_dict["aggregation"]["aoi"][0], "string")

    #
    def test_spatial_from_json(self):
        self.logger.info('test_spatial_from_json')

        spatial = query_module.Spatial
        
        spatial_from_json = None

        got_exception = False

        try:
            spatial_from_json = spatial.from_json(spatial_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(spatial_from_json.type, "point")
        self.assertEqual(spatial_from_json.aoi, "string")
        self.assertEqual(spatial_from_json.coordinates[0], 0)
        self.assertEqual(spatial_from_json.aggregation.aoi[0], "string")
    
    #
    def test_spatial_to_json(self):
        self.logger.info('test_spatial_to_json')
        
        spatial = query_module.Spatial
        
        spatial_from_json = None
        spatial_to_json = None

        got_exception = False
        
        try:
            spatial_from_json = spatial.from_json(spatial_json)
            spatial_to_json = spatial_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
    
    #    
    def test_spatial_geojson_from_dict(self):
        self.logger.info('test_spatial_geojson_from_dict')
        
        spatial = query_module.Spatial
        
        spatial_from_dict = None
        
        got_exception = False
        
        try:
            spatial_from_dict = spatial.from_dict(spatial_geojson_dict)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(spatial_from_dict.type, "poly")
        self.assertEqual(spatial_from_dict.geojson.type, "Feature")
        self.assertEqual(spatial_from_dict.geojson.geometry.coordinates, [[[[-9.164699678818277,39.10329357870404],[-9.148221910727607,39.146135775739786],[-9.092197499219324,39.13295356126725],[-9.118561928164398,39.090111364231504],[-9.164699678818277,39.10329357870404]]]])
        self.assertEqual(spatial_from_dict.geojson.geometry.type, "MultiPolygon")
        
    #    
    def test_spatial_geojson_to_dict(self):
        self.logger.info('test_spatial_geojson_to_dict')
        
        spatial = query_module.Spatial
        
        spatial_from_dict = None
        spatial_to_dict   = None
        
        got_exception = False
        
        #try:
        spatial_from_dict = spatial.from_dict(spatial_geojson_dict)
        spatial_to_dict   = spatial_from_dict.to_dict()
        #except Exception as ex:
        #    got_exception = True
        
        self.assertFalse(got_exception)
        self.assertIsInstance(spatial_to_dict, dict)
        self.assertEqual(spatial_to_dict["type"], "poly")
        self.assertEqual(spatial_to_dict["geojson"]["type"], "Feature")
        self.assertEqual(spatial_to_dict["geojson"]["geometry"]["coordinates"], [[[[-9.164699678818277,39.10329357870404],[-9.148221910727607,39.146135775739786],[-9.092197499219324,39.13295356126725],[-9.118561928164398,39.090111364231504],[-9.164699678818277,39.10329357870404]]]])
        self.assertEqual(spatial_to_dict["geojson"]["geometry"]["type"], "MultiPolygon")
'''
    #
    def test_spatial_geojson_from_json(self):
        self.logger.info('test_spatial_from_json')
        
        spatial = query_module.Spatial
        
        spatial_from_json = None
        
        got_exception = False
        
        try:
            spatial_from_json = spatial.from_json(spatial_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(spatial_from_json.type, "point")
        self.assertEqual(spatial_from_json.aoi, "string")
        self.assertEqual(spatial_from_json.coordinates[0], 0)
        self.assertEqual(spatial_from_json.aggregation.aoi[0], "string")
        
    #
    def test_spatial_geojson_to_json(self):
        self.logger.info('test_spatial_to_json')
        
        spatial = query_module.Spatial
        
        spatial_from_json = None
        spatial_to_json = None
        
        got_exception = False
        
        try:
            spatial_from_json = spatial.from_json(spatial_json)
            spatial_to_json = spatial_from_json.to_json()
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
'''

upload_dict = {
    "provider": "ibm",
    "endpoint": "string",
    "bucket": "string",
    "token": "string"
}

upload_json = r'''{
    "provider": "ibm",
    "endpoint": "string",
    "bucket": "string",
    "token": "string"
}'''

#
class UploadUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_upload_init(self):
        self.logger.info('test_upload_init')
        
        upload = query_module.Upload()
        
        got_exception = False
        
        try:
            upload.provider = "ibm"
            upload.endpoint = "string"
            upload.bucket   = "string"
            upload.token    = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(upload.provider, "ibm")
        self.assertEqual(upload.endpoint, "string")
        self.assertEqual(upload.bucket, "string")
        self.assertEqual(upload.token, "string")

    #    
    def test_upload_from_dict(self):
        self.logger.info('test_upload_from_dict')
        
        upload = query_module.Upload

        upload_from_dict = None
            
        got_exception = False

        try:
            upload_from_dict = upload.from_dict(upload_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(upload_from_dict.provider, "ibm")
        self.assertEqual(upload_from_dict.endpoint, "string")
        self.assertEqual(upload_from_dict.bucket, "string")
        self.assertEqual(upload_from_dict.token, "string")
        
    #    
    def test_upload_to_dict(self):
        self.logger.info('test_upload_from_dict')
        
        upload = query_module.Upload

        upload_from_dict = None
        upload_to_dict   = None
                
        got_exception = False

        try:
            upload_from_dict = upload.from_dict(upload_dict)
            upload_to_dict   = upload_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(upload_to_dict, dict)
        self.assertEqual(upload_to_dict["provider"], "ibm")
        self.assertEqual(upload_to_dict["endpoint"], "string")
        self.assertEqual(upload_to_dict["bucket"], "string")
        self.assertEqual(upload_to_dict["token"], "string")

    #
    def test_upload_from_json(self):
        self.logger.info('test_upload_from_json')

        upload = query_module.Upload
        
        upload_from_json = None

        got_exception = False

        try:
            upload_from_json = upload.from_json(upload_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(upload_from_json.provider, "ibm")
        self.assertEqual(upload_from_json.endpoint, "string")
        self.assertEqual(upload_from_json.bucket, "string")
        self.assertEqual(upload_from_json.token, "string")
    
    #
    def test_upload_to_json(self):
        self.logger.info('test_upload_to_json')
        
        upload = query_module.Upload
        
        upload_from_json = None
        upload_to_json = None

        got_exception = False
        
        try:
            upload_from_json = upload.from_json(upload_json)
            upload_to_json = upload_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

query_response_data_dict = {
    "layerId": 0,
    "layerName": "string",
    "dataset": "string",
    "timestamp": 0,
    "longitude": 0,
    "latitude": 0,
    "region": "string",
    "value": "string",
    "unit": "string",
    "property": "string",
    "aggregation": "string",
    "alias": "string"
}

query_response_data_json = r'''{
    "layerId": 0,
    "layerName": "string",
    "dataset": "string",
    "timestamp": 0,
    "longitude": 0,
    "latitude": 0,
    "region": "string",
    "value": "string",
    "unit": "string",
    "property": "string",
    "aggregation": "string",
    "alias": "string"
}'''

#
class QueryResponseDataUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_response_data_init(self):
        self.logger.info('test_query_response_data_init')
        
        query_response_data = query_module.QueryResponseData()
        
        got_exception = False
        
        try:
            query_response_data.layer_id    = 0
            query_response_data.layer_name  = "string"
            query_response_data.dataset     = "string"
            query_response_data.timestamp   = 0
            query_response_data.longitude   = 0
            query_response_data.latitude    = 0
            query_response_data.region      = "string"
            query_response_data.value       = "string"
            query_response_data.unit        = "string"
            query_response_data.pty         = "string"
            query_response_data.aggregation = "string"
            query_response_data.alias       = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query_response_data.layer_id, 0)
        self.assertEqual(query_response_data.layer_name, "string")
        self.assertEqual(query_response_data.dataset, "string")
        self.assertEqual(query_response_data.timestamp, 0)
        self.assertEqual(query_response_data.longitude, 0)
        self.assertEqual(query_response_data.latitude, 0)
        self.assertEqual(query_response_data.region, "string")
        self.assertEqual(query_response_data.value, "string")
        self.assertEqual(query_response_data.unit, "string")
        self.assertEqual(query_response_data.pty, "string")
        self.assertEqual(query_response_data.aggregation, "string")
        self.assertEqual(query_response_data.alias, "string")

    #    
    def test_query_response_data_from_dict(self):
        self.logger.info('test_query_response_data_from_dict')
        
        query_response_data = query_module.QueryResponseData

        query_response_data_from_dict = None
            
        got_exception = False

        try:
            query_response_data_from_dict = query_response_data.from_dict(query_response_data_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_data_from_dict.layer_id, 0)
        self.assertEqual(query_response_data_from_dict.layer_name, "string")
        self.assertEqual(query_response_data_from_dict.dataset, "string")
        self.assertEqual(query_response_data_from_dict.timestamp, 0)
        self.assertEqual(query_response_data_from_dict.longitude, 0)
        self.assertEqual(query_response_data_from_dict.latitude, 0)
        self.assertEqual(query_response_data_from_dict.region, "string")
        self.assertEqual(query_response_data_from_dict.value, "string")
        self.assertEqual(query_response_data_from_dict.unit, "string")
        self.assertEqual(query_response_data_from_dict.pty, "string")
        self.assertEqual(query_response_data_from_dict.aggregation, "string")
        self.assertEqual(query_response_data_from_dict.alias, "string")
        
    #    
    def test_query_response_data_to_dict(self):
        self.logger.info('test_query_response_data_from_dict')
        
        query_response_data = query_module.QueryResponseData

        query_response_data_from_dict = None
        query_response_data_to_dict   = None
                
        got_exception = False

        try:
            query_response_data_from_dict = query_response_data.from_dict(query_response_data_dict)
            query_response_data_to_dict   = query_response_data_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_response_data_to_dict, dict)
        self.assertEqual(query_response_data_to_dict["layer_id"], 0)
        self.assertEqual(query_response_data_to_dict["layer_name"], "string")
        self.assertEqual(query_response_data_to_dict["dataset"], "string")
        self.assertEqual(query_response_data_to_dict["timestamp"], 0)
        self.assertEqual(query_response_data_to_dict["longitude"], 0)
        self.assertEqual(query_response_data_to_dict["latitude"], 0)
        self.assertEqual(query_response_data_to_dict["region"], "string")
        self.assertEqual(query_response_data_to_dict["value"], "string")
        self.assertEqual(query_response_data_to_dict["unit"], "string")
        self.assertEqual(query_response_data_to_dict["property"], "string")
        self.assertEqual(query_response_data_to_dict["aggregation"], "string")
        self.assertEqual(query_response_data_to_dict["alias"], "string")

    #
    def test_query_response_data_from_json(self):
        self.logger.info('test_query_response_data_from_json')

        query_response_data = query_module.QueryResponseData
        
        query_response_data_from_json = None

        got_exception = False

        try:
            query_response_data_from_json = query_response_data.from_json(query_response_data_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_data_from_json.layer_id, 0)
        self.assertEqual(query_response_data_from_json.layer_name, "string")
        self.assertEqual(query_response_data_from_json.dataset, "string")
        self.assertEqual(query_response_data_from_json.timestamp, 0)
        self.assertEqual(query_response_data_from_json.longitude, 0)
        self.assertEqual(query_response_data_from_json.latitude, 0)
        self.assertEqual(query_response_data_from_json.region, "string")
        self.assertEqual(query_response_data_from_json.value, "string")
        self.assertEqual(query_response_data_from_json.unit, "string")
        self.assertEqual(query_response_data_from_json.pty, "string")
        self.assertEqual(query_response_data_from_json.aggregation, "string")
        self.assertEqual(query_response_data_from_json.alias, "string")
    
    #
    def test_query_response_data_to_json(self):
        self.logger.info('test_query_response_data_to_json')
        
        query_response_data = query_module.QueryResponseData
        
        query_response_data_from_json = None
        query_response_data_to_json = None

        got_exception = False
        
        try:
            query_response_data_from_json = query_response_data.from_json(query_response_data_json)
            query_response_data_to_json = query_response_data_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

query_response_dict = {
    "id": "string",
    "url": "string",
    "data": [
        {
            "layerId": 0,
            "layerName": "string",
            "dataset": "string",
            "timestamp": 0,
            "longitude": 0,
            "latitude": 0,
            "region": "string",
            "value": "string",
            "unit": "string",
            "property": "string",
            "aggregation": "string"
        }
    ],
    "message": "string"
}

query_response_csv_dict = {
    "id": "string",
    "url": "string",
    "data": "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,",
    "message": "string"
}

query_response_json = r'''{
    "id": "string",
    "url": "string",
    "data": [
        {
            "layerId": 0,
            "layerName": "string",
            "dataset": "string",
            "timestamp": 0,
            "longitude": 0,
            "latitude": 0,
            "region": "string",
            "value": "string",
            "unit": "string",
            "property": "string",
            "aggregation": "string"
        }
    ],
    "message": "string"
}'''

query_response_csv_json = r'''{
    "id": "string",
    "url": "string",
    "data": "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,",
    "message": "string"
}'''

#
class QueryResponseUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_response_init(self):
        self.logger.info('test_query_response_init')
        
        query_response = query_module.QueryResponse()
        
        got_exception = False
        
        try:
            query_response.id                = "string"
            query_response.url               = "string"
            query_response_data              = query_module.QueryResponseData()
            query_response_data.layer_id     = 0
            query_response_data.layer_name   = "string"
            query_response_data.dataset      = "string"
            query_response_data.timestamp    = 0
            query_response_data.longitude    = 0
            query_response_data.latitude     = 0
            query_response_data.region       = "string"
            query_response_data.value        = "string"
            query_response_data.unit         = "string"
            query_response_data.pty          = "string"
            query_response_data.aggregation  = "string"
            query_response.data              = [query_response_data]
            query_response.message           = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query_response.id, "string")
        self.assertEqual(query_response.url, "string")
        self.assertEqual(query_response.data[0].layer_id, 0)
        self.assertEqual(query_response.data[0].layer_name, "string")
        self.assertEqual(query_response.data[0].dataset, "string")
        self.assertEqual(query_response.data[0].timestamp, 0)
        self.assertEqual(query_response.data[0].longitude, 0)
        self.assertEqual(query_response.data[0].latitude, 0)
        self.assertEqual(query_response.data[0].region, "string")
        self.assertEqual(query_response.data[0].value, "string")
        self.assertEqual(query_response.data[0].unit, "string")
        self.assertEqual(query_response.data[0].pty, "string")
        self.assertEqual(query_response.data[0].aggregation, "string")
        self.assertEqual(query_response.message, "string")

    #    
    def test_query_response_from_dict(self):
        self.logger.info('test_query_response_from_dict')
        
        query_response = query_module.QueryResponse

        query_response_from_dict = None
            
        got_exception = False

        try:
            query_response_from_dict = query_response.from_dict(query_response_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_from_dict.id, "string")
        self.assertEqual(query_response_from_dict.url, "string")
        self.assertEqual(query_response_from_dict.data[0].layer_id, 0)
        self.assertEqual(query_response_from_dict.data[0].layer_name, "string")
        self.assertEqual(query_response_from_dict.data[0].dataset, "string")
        self.assertEqual(query_response_from_dict.data[0].timestamp, 0)
        self.assertEqual(query_response_from_dict.data[0].longitude, 0)
        self.assertEqual(query_response_from_dict.data[0].latitude, 0)
        self.assertEqual(query_response_from_dict.data[0].region, "string")
        self.assertEqual(query_response_from_dict.data[0].value, "string")
        self.assertEqual(query_response_from_dict.data[0].unit, "string")
        self.assertEqual(query_response_from_dict.data[0].pty, "string")
        self.assertEqual(query_response_from_dict.data[0].aggregation, "string")
        self.assertEqual(query_response_from_dict.message, "string")
    
    #    
    def test_query_response_csv_from_dict(self):
        self.logger.info('test_query_response_csv_from_dict')
        
        query_response_csv = query_module.QueryResponse

        query_response_csv_from_dict = None
            
        got_exception = False

        try:
            query_response_csv_from_dict = query_response_csv.from_dict(query_response_csv_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_csv_from_dict.id, "string")
        self.assertEqual(query_response_csv_from_dict.url, "string")
        self.assertEqual(query_response_csv_from_dict.data, "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,")
        self.assertEqual(query_response_csv_from_dict.message, "string")
        
    #    
    def test_query_response_to_dict(self):
        self.logger.info('test_query_response_from_dict')
        
        query_response = query_module.QueryResponse

        query_response_from_dict = None
        query_response_to_dict   = None
                
        got_exception = False

        try:
            query_response_from_dict = query_response.from_dict(query_response_dict)
            query_response_to_dict   = query_response_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_response_to_dict, dict)
        
        self.assertEqual(query_response_to_dict["id"], "string")
        self.assertEqual(query_response_to_dict["url"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["layer_id"], 0)
        self.assertEqual(query_response_to_dict["data"][0]["layer_name"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["dataset"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["timestamp"], 0)
        self.assertEqual(query_response_to_dict["data"][0]["longitude"], 0)
        self.assertEqual(query_response_to_dict["data"][0]["latitude"], 0)
        self.assertEqual(query_response_to_dict["data"][0]["region"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["value"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["unit"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["property"], "string")
        self.assertEqual(query_response_to_dict["data"][0]["aggregation"], "string")
        self.assertEqual(query_response_to_dict["message"], "string")
    
    #    
    def test_query_response_csv_to_dict(self):
        self.logger.info('test_query_response_csv_from_dict')
        
        query_response_csv = query_module.QueryResponse

        query_response_csv_from_dict = None
        query_response_csv_to_dict   = None
                
        got_exception = False

        try:
            query_response_csv_from_dict = query_response_csv.from_dict(query_response_csv_dict)
            query_response_csv_to_dict   = query_response_csv_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_response_csv_to_dict, dict)
        
        self.assertEqual(query_response_csv_to_dict["id"], "string")
        self.assertEqual(query_response_csv_to_dict["url"], "string")
        self.assertEqual(query_response_csv_to_dict["data"], "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,")
        self.assertEqual(query_response_csv_to_dict["message"], "string")

    #
    def test_query_response_from_json(self):
        self.logger.info('test_query_response_from_json')

        query_response = query_module.QueryResponse
        
        query_response_from_json = None

        got_exception = False

        try:
            query_response_from_json = query_response.from_json(query_response_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_from_json.id, "string")
        self.assertEqual(query_response_from_json.url, "string")
        self.assertEqual(query_response_from_json.data[0].layer_id, 0)
        self.assertEqual(query_response_from_json.data[0].layer_name, "string")
        self.assertEqual(query_response_from_json.data[0].dataset, "string")
        self.assertEqual(query_response_from_json.data[0].timestamp, 0)
        self.assertEqual(query_response_from_json.data[0].longitude, 0)
        self.assertEqual(query_response_from_json.data[0].latitude, 0)
        self.assertEqual(query_response_from_json.data[0].region, "string")
        self.assertEqual(query_response_from_json.data[0].value, "string")
        self.assertEqual(query_response_from_json.data[0].unit, "string")
        self.assertEqual(query_response_from_json.data[0].pty, "string")
        self.assertEqual(query_response_from_json.data[0].aggregation, "string")
        self.assertEqual(query_response_from_json.message, "string")
    
    #
    def test_query_response_csv_from_json(self):
        self.logger.info('test_query_response_csv_from_json')

        query_response_csv = query_module.QueryResponse
        
        query_response_csv_from_json = None

        got_exception = False

        try:
            query_response_csv_from_json = query_response_csv.from_json(query_response_csv_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_response_csv_from_json.id, "string")
        self.assertEqual(query_response_csv_from_json.url, "string")
        self.assertEqual(query_response_csv_from_json.data, "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,")
        self.assertEqual(query_response_csv_from_json.message, "string")
    
    #
    def test_query_response_to_json(self):
        self.logger.info('test_query_response_to_json')
        
        query_response = query_module.QueryResponse
        
        query_response_from_json = None
        query_response_to_json = None

        got_exception = False
        
        try:
            query_response_from_json = query_response.from_json(query_response_json)
            query_response_to_json = query_response_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
 
query_job_dict = {
    "id": "string",
    "status": "Queued(0)",
    "statusCode": 0,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "flag": True,
    "hadoopId": "string",
    "ready": True,
    "rtStatus": "string",
    "pdStatus": "string"
}

query_job_json = r'''{
    "id": "string",
    "status": "Queued(0)",
    "statusCode": 0,
    "start": 0,
    "swLat": 0,
    "swLon": 0,
    "neLat": 0,
    "neLon": 0,
    "nickname": "string",
    "exPercent": 0,
    "flag": true,
    "hadoopId": "string",
    "ready": true,
    "rtStatus": "string",
    "pdStatus": "string"
}'''

#
class QueryJobUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_job_init(self):
        self.logger.info('test_query_job_init')
        
        query_job = query_module.QueryJob()
        
        got_exception = False
        
        try:
            query_job.id          = "string"
            query_job.status      = "Queued(0)"
            query_job.status_code = 0
            query_job.start       = 0
            query_job.sw_lat      = 0
            query_job.sw_lon      = 0
            query_job.ne_lat      = 0
            query_job.ne_lon      = 0
            query_job.nickname    = "string"
            query_job.ex_percent  = 0
            query_job.flag        = True
            query_job.hadoop_id   = "string"
            query_job.ready       = True
            query_job.rt_status   = "string"
            query_job.pd_status   = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query_job.id, "string")
        self.assertEqual(query_job.status, "Queued(0)")
        self.assertEqual(query_job.status_code, 0)
        self.assertEqual(query_job.start, 0)
        self.assertEqual(query_job.sw_lat, 0)
        self.assertEqual(query_job.sw_lon, 0)
        self.assertEqual(query_job.ne_lat, 0)
        self.assertEqual(query_job.ne_lon, 0)
        self.assertEqual(query_job.nickname, "string")
        self.assertEqual(query_job.ex_percent, 0)
        self.assertEqual(query_job.flag, True)
        self.assertEqual(query_job.hadoop_id, "string")
        self.assertEqual(query_job.ready, True)
        self.assertEqual(query_job.rt_status, "string")
        self.assertEqual(query_job.pd_status, "string")
    #    
    def test_query_job_from_dict(self):
        self.logger.info('test_query_job_from_dict')
        
        query_job = query_module.QueryJob

        query_job_from_dict = None
            
        got_exception = False

        try:
            query_job_from_dict = query_job.from_dict(query_job_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_job_from_dict.id, "string")
        self.assertEqual(query_job_from_dict.status, "Queued(0)")
        self.assertEqual(query_job_from_dict.status_code, 0)
        self.assertEqual(query_job_from_dict.start, 0)
        self.assertEqual(query_job_from_dict.sw_lat, 0)
        self.assertEqual(query_job_from_dict.sw_lon, 0)
        self.assertEqual(query_job_from_dict.ne_lat, 0)
        self.assertEqual(query_job_from_dict.ne_lon, 0)
        self.assertEqual(query_job_from_dict.nickname, "string")
        self.assertEqual(query_job_from_dict.ex_percent, 0)
        self.assertEqual(query_job_from_dict.flag, True)
        self.assertEqual(query_job_from_dict.hadoop_id, "string")
        self.assertEqual(query_job_from_dict.ready, True)
        self.assertEqual(query_job_from_dict.rt_status, "string")
        self.assertEqual(query_job_from_dict.pd_status, "string")
        
    #    
    def test_query_job_to_dict(self):
        self.logger.info('test_query_job_from_dict')
        
        query_job = query_module.QueryJob

        query_job_from_dict = None
        query_job_to_dict   = None
                
        got_exception = False

        try:
            query_job_from_dict = query_job.from_dict(query_job_dict)
            query_job_to_dict   = query_job_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_job_to_dict, dict)
        self.assertEqual(query_job_to_dict["id"], "string")
        self.assertEqual(query_job_to_dict["status"], "Queued(0)")
        self.assertEqual(query_job_to_dict["status_code"], 0)
        self.assertEqual(query_job_to_dict["start"], 0)
        self.assertEqual(query_job_to_dict["sw_lat"], 0)
        self.assertEqual(query_job_to_dict["sw_lon"], 0)
        self.assertEqual(query_job_to_dict["ne_lat"], 0)
        self.assertEqual(query_job_to_dict["ne_lon"], 0)
        self.assertEqual(query_job_to_dict["nickname"], "string")
        self.assertEqual(query_job_to_dict["ex_percent"], 0)
        self.assertEqual(query_job_to_dict["flag"], True)
        self.assertEqual(query_job_to_dict["hadoop_id"], "string")
        self.assertEqual(query_job_to_dict["ready"], True)
        self.assertEqual(query_job_to_dict["rt_status"], "string")
        self.assertEqual(query_job_to_dict["pd_status"], "string")

    #
    def test_query_job_from_json(self):
        self.logger.info('test_query_job_from_json')

        query_job = query_module.QueryJob
        
        query_job_from_json = None

        got_exception = False

        try:
            query_job_from_json = query_job.from_json(query_job_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_job_from_json.id, "string")
        self.assertEqual(query_job_from_json.status, "Queued(0)")
        self.assertEqual(query_job_from_json.status_code, 0)
        self.assertEqual(query_job_from_json.start, 0)
        self.assertEqual(query_job_from_json.sw_lat, 0)
        self.assertEqual(query_job_from_json.sw_lon, 0)
        self.assertEqual(query_job_from_json.ne_lat, 0)
        self.assertEqual(query_job_from_json.ne_lon, 0)
        self.assertEqual(query_job_from_json.nickname, "string")
        self.assertEqual(query_job_from_json.ex_percent, 0)
        self.assertEqual(query_job_from_json.flag, True)
        self.assertEqual(query_job_from_json.hadoop_id, "string")
        self.assertEqual(query_job_from_json.ready, True)
        self.assertEqual(query_job_from_json.rt_status, "string")
        self.assertEqual(query_job_from_json.pd_status, "string")
    
    #
    def test_query_job_to_json(self):
        self.logger.info('test_query_job_to_json')
        
        query_job = query_module.QueryJob
        
        query_job_from_json = None
        query_job_to_json = None

        got_exception = False
        
        try:
            query_job_from_json = query_job.from_json(query_job_json)
            query_job_to_json = query_job_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

query_jobs_dict = {
    "totPages": 0,
    "queryJobList":
    [
        {
            "id": "string",
            "status": "Queued(0)",
            "statusCode": 0,
            "start": 0,
            "swLat": 0,
            "swLon": 0,
            "neLat": 0,
            "neLon": 0,
            "nickname": "string",
            "exPercent": 0,
            "flag": True,
            "hadoopId": "string",
            "ready": True,
            "rtStatus": "string",
            "pdStatus": "string"
        },
        {
            "id": "string",
            "status": "Queued(2)",
            "statusCode": 1,
            "start": 1,
            "swLat": 1,
            "swLon": 1,
            "neLat": 1,
            "neLon": 1,
            "nickname": "string",
            "exPercent": 1,
            "flag": False,
            "hadoopId": "string",
            "ready": False,
            "rtStatus": "string",
            "pdStatus": "string"
        }
    ]
}

query_jobs_json = r'''{
    "totPages": 0,
    "queryJobList":
    [
        {
            "id": "string",
            "status": "Queued(0)",
            "statusCode": 0,
            "start": 0,
            "swLat": 0,
            "swLon": 0,
            "neLat": 0,
            "neLon": 0,
            "nickname": "string",
            "exPercent": 0,
            "flag": true,
            "hadoopId": "string",
            "ready": true,
            "rtStatus": "string",
            "pdStatus": "string"
        },
        {
            "id": "string",
            "status": "Queued(2)",
            "statusCode": 1,
            "start": 1,
            "swLat": 1,
            "swLon": 1,
            "neLat": 1,
            "neLon": 1,
            "nickname": "string",
            "exPercent": 1,
            "flag": false,
            "hadoopId": "string",
            "ready": false,
            "rtStatus": "string",
            "pdStatus": "string"
        }
    ]
}'''

#
class QueryJobsUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_jobs_init(self):
        self.logger.info('test_query_jobs_init')
        
        query_jobs = query_module.QueryJobs()
        
        got_exception = False
        
        try:
            query_jobs.tot_pages       = 0
            query_job                  = query_module.QueryJob()
            query_job.id               = "string"
            query_job.status           = "Queued(0)"
            query_job.status_code      = 0
            query_job.start            = 0
            query_job.sw_lat           = 0
            query_job.sw_lon           = 0
            query_job.ne_lat           = 0
            query_job.ne_lon           = 0
            query_job.nickname         = "string"
            query_job.ex_percent       = 0
            query_job.flag             = True
            query_job.hadoop_id        = "string"
            query_job.ready            = True
            query_job.rt_status        = "string"
            query_job.pd_status        = "string"
            query_job_2                = query_module.QueryJob()
            query_job_2.id             = "string"
            query_job_2.status         = "Queued(2)"
            query_job_2.status_code    = 1
            query_job_2.start          = 1
            query_job_2.sw_lat         = 1
            query_job_2.sw_lon         = 1
            query_job_2.ne_lat         = 1
            query_job_2.ne_lon         = 1
            query_job_2.nickname       = "string"
            query_job_2.ex_percent     = 1
            query_job_2.flag           = False
            query_job_2.hadoop_id      = "string"
            query_job_2.ready          = False
            query_job_2.rt_status      = "string"
            query_job_2.pd_status      = "string"
            query_job_list             = [query_job, query_job_2]
            query_jobs.query_job_list  = query_job_list
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_jobs.tot_pages, 0)
        self.assertEqual(query_jobs.query_job_list[0].id, "string")
        self.assertEqual(query_jobs.query_job_list[0].status, "Queued(0)")
        self.assertEqual(query_jobs.query_job_list[0].status_code, 0)
        self.assertEqual(query_jobs.query_job_list[0].start, 0)
        self.assertEqual(query_jobs.query_job_list[0].sw_lat, 0)
        self.assertEqual(query_jobs.query_job_list[0].sw_lon, 0)
        self.assertEqual(query_jobs.query_job_list[0].ne_lat, 0)
        self.assertEqual(query_jobs.query_job_list[0].ne_lon, 0)
        self.assertEqual(query_jobs.query_job_list[0].nickname, "string")
        self.assertEqual(query_jobs.query_job_list[0].ex_percent, 0)
        self.assertEqual(query_jobs.query_job_list[0].flag, True)
        self.assertEqual(query_jobs.query_job_list[0].hadoop_id, "string")
        self.assertEqual(query_jobs.query_job_list[0].ready, True)
        self.assertEqual(query_jobs.query_job_list[0].rt_status, "string")
        self.assertEqual(query_jobs.query_job_list[0].pd_status, "string")
        self.assertEqual(query_jobs.query_job_list[1].id, "string")
        self.assertEqual(query_jobs.query_job_list[1].status, "Queued(2)")
        self.assertEqual(query_jobs.query_job_list[1].status_code, 1)
        self.assertEqual(query_jobs.query_job_list[1].start, 1)
        self.assertEqual(query_jobs.query_job_list[1].sw_lat, 1)
        self.assertEqual(query_jobs.query_job_list[1].sw_lon, 1)
        self.assertEqual(query_jobs.query_job_list[1].ne_lat, 1)
        self.assertEqual(query_jobs.query_job_list[1].ne_lon, 1)
        self.assertEqual(query_jobs.query_job_list[1].nickname, "string")
        self.assertEqual(query_jobs.query_job_list[1].ex_percent, 1)
        self.assertEqual(query_jobs.query_job_list[1].flag, False)
        self.assertEqual(query_jobs.query_job_list[1].hadoop_id, "string")
        self.assertEqual(query_jobs.query_job_list[1].ready, False)
        self.assertEqual(query_jobs.query_job_list[1].rt_status, "string")
        self.assertEqual(query_jobs.query_job_list[1].pd_status, "string")
    
    #
    def test_query_jobs_from_dict(self):
        self.logger.info('test_query_jobs_from_dict')
        
        query_jobs_2 = query_module.QueryJobs

        query_jobs_from_dict = None
            
        got_exception = False

        try:
            query_jobs_from_dict = query_jobs_2.from_dict(query_jobs_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_jobs_from_dict.tot_pages, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._id, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._status, "Queued(0)")
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._status_code, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._start, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._sw_lat, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._sw_lon, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._ne_lat, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._ne_lon, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._nickname, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._ex_percent, 0)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._flag, True)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._hadoop_id, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._ready, True)
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._rt_status, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[0]._pd_status, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._id, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._status, "Queued(2)")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._status_code, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._start, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._sw_lat, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._sw_lon, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._ne_lat, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._ne_lon, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._nickname, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._ex_percent, 1)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._flag, False)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._hadoop_id, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._ready, False)
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._rt_status, "string")
        self.assertEqual(query_jobs_from_dict.query_job_list[1]._pd_status, "string")
    
    #    
    def test_query_jobs_to_dict(self):
        self.logger.info('test_query_jobs_from_dict')
        
        query_jobs = query_module.QueryJobs

        query_jobs_from_dict = None
        query_jobs_to_dict   = None
                
        got_exception = False

        try:
            query_jobs_from_dict = query_jobs.from_dict(query_jobs_dict)
            query_jobs_to_dict   = query_jobs_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_jobs_to_dict, dict)
        self.assertEqual(query_jobs_to_dict["tot_pages"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["id"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["status"], "Queued(0)")
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["status_code"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["start"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["sw_lat"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["sw_lon"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["ne_lat"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["ne_lon"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["nickname"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["ex_percent"], 0)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["flag"], True)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["hadoop_id"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["ready"], True)
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["rt_status"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][0]["pd_status"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["id"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["status"], "Queued(2)")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["status_code"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["start"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["sw_lat"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["sw_lon"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["ne_lat"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["ne_lon"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["nickname"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["ex_percent"], 1)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["flag"], False)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["hadoop_id"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["ready"], False)
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["rt_status"], "string")
        self.assertEqual(query_jobs_to_dict["query_job_list"][1]["pd_status"], "string")

    #
    def test_query_jobs_from_json(self):
        self.logger.info('test_query_jobs_from_json')

        query_jobs = query_module.QueryJobs
        
        query_jobs_from_json = None

        got_exception = False

        try:
            query_jobs_from_json = query_jobs.from_json(query_jobs_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_jobs_from_json.tot_pages, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._id, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[0]._status, "Queued(0)")
        self.assertEqual(query_jobs_from_json.query_job_list[0]._status_code, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._start, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._sw_lat, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._sw_lon, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._ne_lat, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._ne_lon, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._nickname, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[0]._ex_percent, 0)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._flag, True)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._hadoop_id, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[0]._ready, True)
        self.assertEqual(query_jobs_from_json.query_job_list[0]._rt_status, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[0]._pd_status, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._id, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._status, "Queued(2)")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._status_code, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._start, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._sw_lat, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._sw_lon, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._ne_lat, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._ne_lon, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._nickname, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._ex_percent, 1)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._flag, False)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._hadoop_id, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._ready, False)
        self.assertEqual(query_jobs_from_json.query_job_list[1]._rt_status, "string")
        self.assertEqual(query_jobs_from_json.query_job_list[1]._pd_status, "string")
    
    #
    def test_query_jobs_to_json(self):
        self.logger.info('test_query_jobs_to_json')
        
        query_jobs = query_module.QueryJobs
        
        query_jobs_from_json = None
        query_jobs_to_json = None

        got_exception = False
        
        try:
            query_jobs_from_json = query_jobs.from_json(query_jobs_json)
            query_jobs_to_json = query_jobs_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

query_job_layer_dict = {
    "name": "string",
    "style": "string",
    "datasetId": 0,
    "dataset": "string",
    "datalayerId": "string",
    "datalayer": "string",
    "group": "string",
    "timestamp": 0,
    "dimensions": [
        {
            "name": "string",
            "value": "string",
            "operator": "EQ",
            "options": [
                "string"
            ]
        }
    ],
    "min": 0,
    "max": 0,
    "colortableId": 0,
    "options": [
        "string"
    ],
    "type": "string",
    "geoserverUrl": "string",
    "geoserverWS": "string"
}

query_job_layer_json = r'''{
    "name": "string",
    "style": "string",
    "datasetId": 0,
    "dataset": "string",
    "datalayerId": "string",
    "datalayer": "string",
    "group": "string",
    "timestamp": 0,
    "dimensions": [
        {
            "name": "string",
            "value": "string",
            "operator": "EQ",
            "options": [
                "string"
            ]
        }
    ],
    "min": 0,
    "max": 0,
    "colortableId": 0,
    "options": [
        "string"
    ],
    "type": "string",
    "geoserverUrl": "string",
    "geoserverWS": "string"
}'''

#
class QueryJobLayerUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_job_layer_init(self):
        self.logger.info('test_query_job_layer_init')
        
        query_job_layer = query_module.QueryJobLayer()
        
        got_exception = False
        
        try:
            query_job_layer.name           = "string"
            query_job_layer.style          = "string"
            query_job_layer.dataset_id     = 0
            query_job_layer.dataset        = "string"
            query_job_layer.datalayer_id   = "string"
            query_job_layer.datalayer      = "string"
            query_job_layer.group          = "string"
            query_job_layer.timestamp      = 0
            dimension                      = query_module.Dimension()
            dimension.name                 = "string"
            dimension.value                = "string"
            dimension.operator             = "EQ"
            dimension.options              = ["string"]
            query_job_layer.dimensions     = [dimension]
            query_job_layer.min            = 0
            query_job_layer.max            = 0
            query_job_layer.colortable_id  = 0
            query_job_layer.options        = ["string"]
            query_job_layer.type           = "string"
            query_job_layer.geoserver_url  = "string"
            query_job_layer.geoserver_ws   = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query_job_layer.name, "string")
        self.assertEqual(query_job_layer.style, "string")
        self.assertEqual(query_job_layer.dataset_id, 0)
        self.assertEqual(query_job_layer.dataset, "string")
        self.assertEqual(query_job_layer.datalayer_id, "string")
        self.assertEqual(query_job_layer.datalayer, "string")
        self.assertEqual(query_job_layer.group, "string")
        self.assertEqual(query_job_layer.timestamp, 0)
        self.assertEqual(query_job_layer.dimensions[0].name, "string")
        self.assertEqual(query_job_layer.dimensions[0].value, "string")
        self.assertEqual(query_job_layer.dimensions[0].operator, "EQ")
        self.assertEqual(query_job_layer.dimensions[0].options[0], "string")
        self.assertEqual(query_job_layer.min, 0)
        self.assertEqual(query_job_layer.max, 0)
        self.assertEqual(query_job_layer.colortable_id, 0)
        self.assertEqual(query_job_layer.options[0], "string")
        self.assertEqual(query_job_layer.type, "string")
        self.assertEqual(query_job_layer.geoserver_url, "string")
        self.assertEqual(query_job_layer.geoserver_ws, "string")

    #    
    def test_query_job_layer_from_dict(self):
        self.logger.info('test_query_job_layer_from_dict')
        
        query_job_layer = query_module.QueryJobLayer

        query_job_layer_from_dict = None
            
        got_exception = False

        try:
            query_job_layer_from_dict = query_job_layer.from_dict(query_job_layer_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_job_layer_from_dict.name, "string")
        self.assertEqual(query_job_layer_from_dict.style, "string")
        self.assertEqual(query_job_layer_from_dict.dataset_id, 0)
        self.assertEqual(query_job_layer_from_dict.dataset, "string")
        self.assertEqual(query_job_layer_from_dict.datalayer_id, "string")
        self.assertEqual(query_job_layer_from_dict.datalayer, "string")
        self.assertEqual(query_job_layer_from_dict.group, "string")
        self.assertEqual(query_job_layer_from_dict.timestamp, 0)
        self.assertEqual(query_job_layer_from_dict.dimensions[0].name, "string")
        self.assertEqual(query_job_layer_from_dict.dimensions[0].value, "string")
        self.assertEqual(query_job_layer_from_dict.dimensions[0].operator, "EQ")
        self.assertEqual(query_job_layer_from_dict.dimensions[0].options[0], "string")
        self.assertEqual(query_job_layer_from_dict.min, 0)
        self.assertEqual(query_job_layer_from_dict.max, 0)
        self.assertEqual(query_job_layer_from_dict.options[0], "string")
        self.assertEqual(query_job_layer_from_dict.type, "string")
        self.assertEqual(query_job_layer_from_dict.geoserver_url, "string")
        self.assertEqual(query_job_layer_from_dict.geoserver_ws, "string")
        
    #    
    def test_query_job_layer_to_dict(self):
        self.logger.info('test_query_job_layer_from_dict')
        
        query_job_layer = query_module.QueryJobLayer

        query_job_layer_from_dict = None
        query_job_layer_to_dict   = None
                
        got_exception = False

        try:
            query_job_layer_from_dict = query_job_layer.from_dict(query_job_layer_dict)
            query_job_layer_to_dict   = query_job_layer_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_job_layer_to_dict, dict)
        self.assertEqual(query_job_layer_to_dict["name"], "string")
        self.assertEqual(query_job_layer_to_dict["style"], "string")
        self.assertEqual(query_job_layer_to_dict["dataset_id"], 0)
        self.assertEqual(query_job_layer_to_dict["dataset"], "string")
        self.assertEqual(query_job_layer_to_dict["datalayer_id"], "string")
        self.assertEqual(query_job_layer_to_dict["datalayer"], "string")
        self.assertEqual(query_job_layer_to_dict["group"], "string")
        self.assertEqual(query_job_layer_to_dict["timestamp"], 0)
        self.assertEqual(query_job_layer_to_dict["dimensions"][0]["name"], "string")
        self.assertEqual(query_job_layer_to_dict["dimensions"][0]["value"], "string")
        self.assertEqual(query_job_layer_to_dict["dimensions"][0]["operator"], "EQ")
        self.assertEqual(query_job_layer_to_dict["dimensions"][0]["options"][0], "string")
        self.assertEqual(query_job_layer_to_dict["min"], 0)
        self.assertEqual(query_job_layer_to_dict["max"], 0)
        self.assertEqual(query_job_layer_to_dict["options"][0], "string")
        self.assertEqual(query_job_layer_to_dict["type"], "string")
        self.assertEqual(query_job_layer_to_dict["geoserver_url"], "string")
        self.assertEqual(query_job_layer_to_dict["geoserver_ws"], "string")

    #
    def test_query_job_layer_from_json(self):
        self.logger.info('test_query_job_layer_from_json')

        query_job_layer = query_module.QueryJobLayer
        
        query_job_layer_from_json = None

        got_exception = False

        try:
            query_job_layer_from_json = query_job_layer.from_json(query_job_layer_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_job_layer_from_json.name, "string")
        self.assertEqual(query_job_layer_from_json.style, "string")
        self.assertEqual(query_job_layer_from_json.dataset_id, 0)
        self.assertEqual(query_job_layer_from_json.dataset, "string")
        self.assertEqual(query_job_layer_from_json.datalayer_id, "string")
        self.assertEqual(query_job_layer_from_json.datalayer, "string")
        self.assertEqual(query_job_layer_from_json.group, "string")
        self.assertEqual(query_job_layer_from_json.timestamp, 0)
        self.assertEqual(query_job_layer_from_json.dimensions[0].name, "string")
        self.assertEqual(query_job_layer_from_json.dimensions[0].value, "string")
        self.assertEqual(query_job_layer_from_json.dimensions[0].operator, "EQ")
        self.assertEqual(query_job_layer_from_json.dimensions[0].options[0], "string")
        self.assertEqual(query_job_layer_from_json.min, 0)
        self.assertEqual(query_job_layer_from_json.max, 0)
        self.assertEqual(query_job_layer_from_json.options[0], "string")
        self.assertEqual(query_job_layer_from_json.type, "string")
        self.assertEqual(query_job_layer_from_json.geoserver_url, "string")
        self.assertEqual(query_job_layer_from_json.geoserver_ws, "string")
    
    #
    def test_query_job_layer_to_json(self):
        self.logger.info('test_query_job_layer_to_json')
        
        query_job_layer = query_module.QueryJobLayer
        
        query_job_layer_from_json = None
        query_job_layer_to_json = None

        got_exception = False
        
        try:
            query_job_layer_from_json = query_job_layer.from_json(query_job_layer_json)
            query_job_layer_to_json = query_job_layer_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
options_dict = {
    "name": "string",
    "value": "string"
}

options_json = r'''{
    "name": "string",
    "value": "string"
}'''

#
class OptionsUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_options_init(self):
        self.logger.info('test_options_init')
        
        options = query_module.Options()
        
        got_exception = False
        
        try:
            options.name  = "string"
            options.value = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(options.name, "string")
        self.assertEqual(options.value, "string")

    #    
    def test_options_from_dict(self):
        self.logger.info('test_options_from_dict')
        
        options = query_module.Options

        options_from_dict = None
            
        got_exception = False

        try:
            options_from_dict = options.from_dict(options_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(options_from_dict.name, "string")
        self.assertEqual(options_from_dict.value, "string")
        
    #    
    def test_options_to_dict(self):
        self.logger.info('test_options_to_dict')
        
        options = query_module.Options

        options_from_dict = None
        options_to_dict   = None
                
        got_exception = False

        try:
            options_from_dict = options.from_dict(options_dict)
            options_to_dict   = options_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(options_to_dict, dict)
        self.assertEqual(options_to_dict["name"], "string")
        self.assertEqual(options_to_dict["value"], "string")

    #
    def test_options_from_json(self):
        self.logger.info('test_options_from_json')

        options = query_module.Options
        
        options_from_json = None

        got_exception = False

        try:
            options_from_json = options.from_json(options_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(options_from_json.name, "string")
        self.assertEqual(options_from_json.value, "string")
    
    #
    def test_options_to_json(self):
        self.logger.info('test_options_to_json')
        
        options = query_module.Options
        
        options_from_json = None
        options_to_json = None

        got_exception = False
        
        try:
            options_from_json = options.from_json(options_json)
            options_to_json = options_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
    
processor_dict = {
    "order": 0,
    "type" : "string",
    "options": [
        {
            "name": "string",
            "value": "string"
        },
        {
            "name": "string2",
            "value": "string2"
        }
    ]
}

processor_json = r'''{
    "order": 0,
    "type" : "string",
    "options": [
        {
            "name": "string",
            "value": "string"
        },
        {
            "name": "string2",
            "value": "string2"
        }
    ]
}'''

#
class ProcessorUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_processor_init(self):
        self.logger.info('test_processor_init')
        
        processor = query_module.Processor()
        
        got_exception = False
        
        try:
            processor.order   = 0
            processor.type    = "string"
            options           = query_module.Options()
            options.name      = "string"
            options.value     = "string"
            processor.options = [options]
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(processor.order, 0)
        self.assertEqual(processor.type, "string")
        self.assertEqual(processor.options[0].name, "string")
        self.assertEqual(processor.options[0].value, "string")

    #    
    def test_processor_from_dict(self):
        self.logger.info('test_processor_from_dict')
        
        processor = query_module.Processor

        processor_from_dict = None
            
        got_exception = False

        #try:
        processor_from_dict = processor.from_dict(processor_dict)
        #except Exception as ex:
        #    got_exception = True
        
        print(processor_from_dict)

        self.assertFalse(got_exception)
        self.assertFalse(got_exception)
        self.assertEqual(processor_from_dict.order, 0)
        self.assertEqual(processor_from_dict.type, "string")
        self.assertEqual(processor_from_dict.options[0].name, "string")
        self.assertEqual(processor_from_dict.options[0].value, "string")
        self.assertEqual(processor_from_dict.options[1].name, "string2")
        self.assertEqual(processor_from_dict.options[1].value, "string2")
        
    #    
    def test_processor_to_dict(self):
        self.logger.info('test_processor_to_dict')
        
        processor = query_module.Processor

        processor_from_dict = None
        processor_to_dict   = None
                
        got_exception = False

        try:
            processor_from_dict = processor.from_dict(processor_dict)
            processor_to_dict   = processor_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(processor_to_dict, dict)
        self.assertEqual(processor_to_dict["order"], 0)
        self.assertEqual(processor_to_dict["type"], "string")
        self.assertEqual(processor_to_dict["options"][0]["name"], "string")
        self.assertEqual(processor_to_dict["options"][0]["value"], "string")
        self.assertEqual(processor_to_dict["options"][1]["name"], "string2")
        self.assertEqual(processor_to_dict["options"][1]["value"], "string2")

    #
    def test_processor_from_json(self):
        self.logger.info('test_processor_from_json')

        processor = query_module.Processor
        
        processor_from_json = None

        got_exception = False

        try:
            processor_from_json = processor.from_json(processor_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertEqual(processor_from_json.order, 0)
        self.assertEqual(processor_from_json.type, "string")
        self.assertEqual(processor_from_json.options[0].name, "string")
        self.assertEqual(processor_from_json.options[0].value, "string")
        self.assertEqual(processor_from_json.options[1].name, "string2")
        self.assertEqual(processor_from_json.options[1].value, "string2")
    
    #
    def test_processor_to_json(self):
        self.logger.info('test_processor_to_json')
        
        processor = query_module.Processor
        
        processor_from_json = None
        processor_to_json = None

        got_exception = False
        
        try:
            processor_from_json = processor.from_json(processor_json)
            processor_to_json = processor_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

query_dict = {
    "name": "string",
    "layers": [
        {
            "id": "string",
            "type": "raster",
            "temporal": {
                "intervals": [
                    {
                        "snapshot": "string",
                        "end": "string",
                        "start": "string"
                    }
                ]
            },
            "alias": "string",
            "filterOnly": True,
            "aggregation": "None",
            "filter": 
                {
                    "value": "string",
                    "operator": "EQ"
                },
            "dimensions": [
                {
                    "name": "string",
                    "value": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ]
                }
            ],
            "expression": "string",
            "output": True
        }
    ],
    "temporal": 
        {
            "intervals": [
                {
                    "snapshot": "string",
                    "end": "string",
                    "start": "string"
                }
            ]
        },
    "spatial": 
        {
            "type": "point",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        },
    "outputType": "json",
    "outputLevel": 0,
    "description": "string",
    "publish": True,
    "notification": 
        {
            "type": "rabbitmq",
            "host": "string",
            "queue": "string"
        },
    "upload": 
        {
            "provider": "ibm",
            "endpoint": "string",
            "bucket": "string",
            "token": "string"
        },
    "processor": [
        {
            "order": 0,
            "type" : "string",
            "options": [
                {
                    "name": "string",
                    "value": "string"
                }
            ]
        },
        {
            "order": 1,
            "type" : "string2",
            "options": [
                {
                    "name": "string2",
                    "value": "string2"
                }
            ]
        }
    ]
}

query_json = r'''{
    "name": "string",
    "layers": [
        {
            "id": "string",
            "type": "raster",
            "temporal": {
                "intervals": [
                    {
                        "snapshot": "string",
                        "end": "string",
                        "start": "string"
                    }
                ]
            },
            "alias": "string",
            "filterOnly": true,
            "aggregation": "None",
            "filter": 
                {
                    "value": "string",
                    "operator": "EQ"
                },
            "dimensions": [
                {
                    "name": "string",
                    "value": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ]
                }
            ],
            "expression": "string",
            "output": true
        }
    ],
    "temporal": 
        {
            "intervals": [
                {
                    "snapshot": "string",
                    "end": "string",
                    "start": "string"
                }
            ]
        },
    "spatial": 
        {
            "type": "point",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        },
    "outputType": "json",
    "outputLevel": 0,
    "description": "string",
    "publish": true,
    "notification": 
        {
            "type": "rabbitmq",
            "host": "string",
            "queue": "string"
        },
    "upload": 
        {
            "provider": "ibm",
            "endpoint": "string",
            "bucket": "string",
            "token": "string"
        },
    "processor": [
        {
            "order": 0,
            "type" : "string",
            "options": [
                {
                    "name": "string",
                    "value": "string"
                }
            ]
        },
        {
            "order": 1,
            "type" : "string2",
            "options": [
                {
                    "name": "string2",
                    "value": "string2"
                }
            ]
        }
    ]
}'''

query_replace_dates_dict = {
    "name": "string",
    "layers": [
        {
            "id": "string",
            "type": "raster",
            "temporal": {
                "intervals": [
                    {
                        "snapshot": "string",
                        "end": "string",
                        "start": "string"
                    }
                ]
            },
            "alias": "string",
            "filterOnly": True,
            "aggregation": "None",
            "filter": 
                {
                    "value": "string",
                    "operator": "EQ"
                },
            "dimensions": [
                {
                    "name": "string",
                    "value": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ]
                }
            ],
            "expression": "string",
            "output": True
        },
        {
            "id": "string2",
            "type": "raster",
            "temporal": {
                "intervals": [
                    {
                        "snapshot": "string",
                        "end": "string2",
                        "start": "string2"
                    }
                ]
            },
            "alias": "string2.9999999999999>9999999999999",
            "filterOnly": True,
            "aggregation": "None",
            "filter": 
                {
                    "value": "string",
                    "operator": "EQ"
                },
            "dimensions": [
                {
                    "name": "string",
                    "value": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ]
                }
            ],
            "expression": "string",
            "output": True
        }
    ],
    "temporal": 
        {
            "intervals": [
                {
                    "snapshot": "string",
                    "end": "string",
                    "start": "string"
                }
            ]
        },
    "spatial": 
        {
            "type": "point",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        },
    "outputType": "json",
    "outputLevel": 0,
    "description": "string",
    "publish": True,
    "notification": 
        {
            "type": "rabbitmq",
            "host": "string",
            "queue": "string"
        },
    "upload": 
        {
            "provider": "ibm",
            "endpoint": "string",
            "bucket": "string",
            "token": "string"
        }
}

query_dict_is_bulk_1 = {
    "spatial": 
        {
            "type": "point",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        }
}

query_dict_is_bulk_2 = {
    "spatial": 
        {
            "type": "square",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        }
}

query_dict_is_bulk_3 = {
    "spatial": 
        {
            "type": "poly",
            "aoi": "string",
            "coordinates": [
                0
            ],
            "aggregation": {
                "aoi": [
                    "string"
                ]
            }
        }
}

query_dict_download_status_20 = {
    "description": "string",
    "id": "1",
    "layers": [
        {
            "aggregation": "None",
            "alias": "string",
            "dimensions": [
                {
                    "name": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ],
                    "value": "string"
                }
            ],
            "expression": "string",
            "filter": {
                "operator": "EQ",
                "value": "string"
            },
            "filter_only": True,
            "id": "string",
            "output": True,
            "temporal": {
                "intervals": [
                    {
                        "end": "string",
                        "snapshot": "string",
                        "start": "string"
                    }
                ]
            },
            "type": "raster"
        }
    ],
    "merge_response": {},
    "name": "1",
    "notification": {
        "host": "string",
        "queue": "string",
        "type": "rabbitmq"
    },
    "output_level": 0,
    "output_type": "json",
    "publish": True,
    "spatial": {
        "aggregation": {
            "aoi": [
                "string"
            ]
        },
        "aoi": "string",
        "coordinates": [
            0.0
        ],
        "type": "square"
    },
    "status_response": {
        "ex_percent": 0.0,
        "hadoop_id": "string",
        "id": "1",
        "ne_lat": 0.0,
        "ne_lon": 0.0,
        "nickname": "string",
        "start": 0,
        "status": "Succeeded(20)",
        "status_code": 20,
        "sw_lat": 0.0,
        "sw_lon": 0.0
    },
    "submit_response": {
        "data": [
            {
                "aggregation": "string",
                "dataset": "string",
                "latitude": 0.0,
                "layer_id": 0,
                "layer_name": "string",
                "longitude": 0.0,
                "property": "string",
                "region": "string",
                "timestamp": 0,
                "unit": "string",
                "value": "string"
            }
        ],
        "id": "1",
        "url": "string"
    },
    "temporal": {
        "intervals": [
            {
                "end": "string",
                "snapshot": "string",
                "start": "string"
            }
        ]
    },
    "upload": {
        "bucket": "string",
        "endpoint": "string",
        "provider": "ibm",
        "token": "string"
    }
}

query_dict_download_status_20_no_point_values = {
    "description": "string",
    "id": "1",
    "layers": [
        {
            "aggregation": "None",
            "alias": "string",
            "dimensions": [
                {
                    "name": "string",
                    "operator": "EQ",
                    "options": [
                        "string"
                    ],
                    "value": "string"
                }
            ],
            "expression": "string",
            "filter": {
                "operator": "EQ",
                "value": "string"
            },
            "filter_only": True,
            "id": "string",
            "output": True,
            "temporal": {
                "intervals": [
                    {
                        "end": "string",
                        "snapshot": "string",
                        "start": "string"
                    }
                ]
            },
            "type": "raster"
        }
    ],
    "merge_response": {},
    "name": "1",
    "notification": {
        "host": "string",
        "queue": "string",
        "type": "rabbitmq"
    },
    "output_level": 0,
    "output_type": "json",
    "publish": True,
    "spatial": {
        "aggregation": {
            "aoi": [
                "string"
            ]
        },
        "aoi": "string",
        "coordinates": [
            0.0
        ],
        "type": "square"
    },
    "status_response": {
        "ex_percent": 0.0,
        "hadoop_id": "string",
        "id": "1",
        "ne_lat": 0.0,
        "ne_lon": 0.0,
        "nickname": "string",
        "start": 0,
        "status": "Succeeded(20)",
        "status_code": 20,
        "sw_lat": 0.0,
        "sw_lon": 0.0
    },
    "submit_response": {
        "id": "1",
        "url": "string"
    },
    "temporal": {
        "intervals": [
            {
                "end": "string",
                "snapshot": "string",
                "start": "string"
            }
        ]
    },
    "upload": {
        "bucket": "string",
        "endpoint": "string",
        "provider": "ibm",
        "token": "string"
    }
}

#
class QueryUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_init(self):
        self.logger.info('test_query_init')
        
        query = query_module.Query()
        
        got_exception = False
        
        try:
            query.name                = "string"
            layer                     = query_module.Layer()
            layer.id                  = "string"
            layer.type                = "raster"
            temporal                  = query_module.Temporal()
            interval                  = query_module.Interval()
            interval.snapshot         = "string"
            interval.end              = "string"
            interval.start            = "string"
            temporal.intervals        = [interval]
            layer.temporal            = temporal
            layer.alias               = "string"
            layer.filter_only         = True
            layer.aggregation         = "None"
            filter_                   = query_module.Filter() 
            filter_.value             = "string"
            filter_.operator          = "EQ"
            layer.filter              = filter_
            dimension                 = query_module.Dimension()
            dimension.name            = "string"
            dimension.value           = "string"
            dimension.operator        = "EQ"
            dimension.options         = ["string"]
            layer.dimensions          = [dimension]
            layer.expression          = "string"
            layer.output              = True
            query.layers              = [layer]
            global_temporal           = query_module.Temporal()
            global_interval           = query_module.Interval()
            global_interval.snapshot  = "string"
            global_interval.end       = "string"
            global_interval.start     = "string"
            global_temporal.intervals = [global_interval]
            query.temporal            = global_temporal
            spatial                   = query_module.Spatial()
            spatial.type              = "point"
            spatial.aoi               = "string"
            spatial.coordinates       = [0]
            aggregation               = query_module.Aggregation()
            aggregation.aoi           = ["string"]
            spatial.aggregation       = aggregation
            query.spatial             = spatial
            query.output_type         = "json"
            query.output_level        = 0
            query.description         = "string"
            query.publish             = True
            notification              = query_module.Notification()
            notification.type         = "rabbitmq"
            notification.host         = "string"
            notification.queue        = "string"
            query.notification        = notification
            upload                    = query_module.Upload()
            upload.provider           = "ibm"
            upload.endpoint           = "string"
            upload.bucket             = "string"
            upload.token              = "string"
            query.upload              = upload
            options                   = query_module.Options()
            options.name              = "string"
            options.value             = "string"
            processor                 = query_module.Processor()
            processor.order           = 0
            processor.type            = "string"
            processor.options         = [options]
            query.processor           = [processor]
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query.name, "string")
        self.assertEqual(query.layers[0].id, "string")
        self.assertEqual(query.layers[0].type, "raster")
        self.assertEqual(query.layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(query.layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(query.layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(query.layers[0].alias, "string")
        self.assertEqual(query.layers[0].filter_only, True)
        self.assertEqual(query.layers[0].aggregation, "None")
        self.assertEqual(query.layers[0].filter.value, "string")
        self.assertEqual(query.layers[0].filter.operator, "EQ")
        self.assertEqual(query.layers[0].dimensions[0].name, "string")
        self.assertEqual(query.layers[0].dimensions[0].value, "string")
        self.assertEqual(query.layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(query.layers[0].dimensions[0].options[0], "string")
        self.assertEqual(query.layers[0].expression, "string")
        self.assertEqual(query.layers[0].output, True)
        self.assertEqual(query.temporal.intervals[0].snapshot, "string")
        self.assertEqual(query.temporal.intervals[0].end, "string")
        self.assertEqual(query.temporal.intervals[0].start, "string")
        self.assertEqual(query.spatial.type, "point")
        self.assertEqual(query.spatial.aoi, "string")
        self.assertEqual(query.spatial.coordinates[0], 0)
        self.assertEqual(query.spatial.aggregation.aoi[0], "string")
        self.assertEqual(query.output_type, "json")
        self.assertEqual(query.output_level, 0)
        self.assertEqual(query.description, "string")
        self.assertEqual(query.publish, True)
        self.assertEqual(query.notification.type, "rabbitmq")
        self.assertEqual(query.notification.host, "string")
        self.assertEqual(query.notification.queue, "string")
        self.assertEqual(query.upload.provider, "ibm")
        self.assertEqual(query.upload.endpoint, "string")
        self.assertEqual(query.upload.bucket, "string")
        self.assertEqual(query.upload.token, "string")
        self.assertEqual(query.processor[0].order, 0)
        self.assertEqual(query.processor[0].type, "string")
        self.assertEqual(query.processor[0].options[0].name, "string")
        self.assertEqual(query.processor[0].options[0].value, "string")

    #    
    def test_query_from_dict(self):
        self.logger.info('test_query_from_dict')
        
        query = query_module.Query

        query_from_dict = None
            
        got_exception = False

        try:
            query_from_dict = query.from_dict(query_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_from_dict.name, "string")
        self.assertEqual(query_from_dict.layers[0].id, "string")
        self.assertEqual(query_from_dict.layers[0].type, "raster")
        self.assertEqual(query_from_dict.layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(query_from_dict.layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(query_from_dict.layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(query_from_dict.layers[0].alias, "string")
        self.assertEqual(query_from_dict.layers[0].filter_only, True)
        self.assertEqual(query_from_dict.layers[0].aggregation, "None")
        self.assertEqual(query_from_dict.layers[0].filter.value, "string")
        self.assertEqual(query_from_dict.layers[0].filter.operator, "EQ")
        self.assertEqual(query_from_dict.layers[0].dimensions[0].name, "string")
        self.assertEqual(query_from_dict.layers[0].dimensions[0].value, "string")
        self.assertEqual(query_from_dict.layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(query_from_dict.layers[0].dimensions[0].options[0], "string")
        self.assertEqual(query_from_dict.layers[0].expression, "string")
        self.assertEqual(query_from_dict.layers[0].output, True)
        self.assertEqual(query_from_dict.temporal.intervals[0].snapshot, "string")
        self.assertEqual(query_from_dict.temporal.intervals[0].end, "string")
        self.assertEqual(query_from_dict.temporal.intervals[0].start, "string")
        self.assertEqual(query_from_dict.spatial.type, "point")
        self.assertEqual(query_from_dict.spatial.aoi, "string")
        self.assertEqual(query_from_dict.spatial.coordinates[0], 0)
        self.assertEqual(query_from_dict.spatial.aggregation.aoi[0], "string")
        self.assertEqual(query_from_dict.output_type, "json")
        self.assertEqual(query_from_dict.output_level, 0)
        self.assertEqual(query_from_dict.description, "string")
        self.assertEqual(query_from_dict.publish, True)
        self.assertEqual(query_from_dict.notification.type, "rabbitmq")
        self.assertEqual(query_from_dict.notification.host, "string")
        self.assertEqual(query_from_dict.notification.queue, "string")
        self.assertEqual(query_from_dict.upload.provider, "ibm")
        self.assertEqual(query_from_dict.upload.endpoint, "string")
        self.assertEqual(query_from_dict.upload.bucket, "string")
        self.assertEqual(query_from_dict.upload.token, "string")
        self.assertEqual(query_from_dict.processor[0].order, 0)
        self.assertEqual(query_from_dict.processor[0].type, "string")
        self.assertEqual(query_from_dict.processor[0].options[0].name, "string")
        self.assertEqual(query_from_dict.processor[0].options[0].value, "string")
        self.assertEqual(query_from_dict.processor[1].order, 1)
        self.assertEqual(query_from_dict.processor[1].type, "string2")
        self.assertEqual(query_from_dict.processor[1].options[0].name, "string2")
        self.assertEqual(query_from_dict.processor[1].options[0].value, "string2")
        
    #    
    def test_query_to_dict(self):
        self.logger.info('test_query_from_dict')
        
        query = query_module.Query
    
        query_from_dict = None
        query_to_dict   = None
                
        got_exception = False
    
        try:
            query_from_dict = query.from_dict(query_dict)
            query_to_dict   = query_from_dict.to_dict()
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
        self.assertIsInstance(query_to_dict, dict)
        self.assertEqual(query_to_dict["name"], "string")
        self.assertEqual(query_to_dict["layers"][0]["id"], "string")
        self.assertEqual(query_to_dict["layers"][0]["type"], "raster")
        self.assertEqual(query_to_dict["layers"][0]["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(query_to_dict["layers"][0]["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(query_to_dict["layers"][0]["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(query_to_dict["layers"][0]["alias"], "string")
        self.assertEqual(query_to_dict["layers"][0]["filter_only"], True)
        self.assertEqual(query_to_dict["layers"][0]["aggregation"], "None")
        self.assertEqual(query_to_dict["layers"][0]["filter"]["value"], "string")
        self.assertEqual(query_to_dict["layers"][0]["filter"]["operator"], "EQ")
        self.assertEqual(query_to_dict["layers"][0]["dimensions"][0]["name"], "string")
        self.assertEqual(query_to_dict["layers"][0]["dimensions"][0]["value"], "string")
        self.assertEqual(query_to_dict["layers"][0]["dimensions"][0]["operator"], "EQ")
        self.assertEqual(query_to_dict["layers"][0]["dimensions"][0]["options"][0], "string")
        self.assertEqual(query_to_dict["layers"][0]["expression"], "string")
        self.assertEqual(query_to_dict["layers"][0]["output"], True)
        self.assertEqual(query_to_dict["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(query_to_dict["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(query_to_dict["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(query_to_dict["spatial"]["type"], "point")
        self.assertEqual(query_to_dict["spatial"]["aoi"], "string")
        self.assertEqual(query_to_dict["spatial"]["coordinates"][0], 0)
        self.assertEqual(query_to_dict["spatial"]["aggregation"]["aoi"][0], "string")
        self.assertEqual(query_to_dict["output_type"], "json")
        self.assertEqual(query_to_dict["output_level"], 0)
        self.assertEqual(query_to_dict["description"], "string")
        self.assertEqual(query_to_dict["publish"], True)
        self.assertEqual(query_to_dict["notification"]["type"], "rabbitmq")
        self.assertEqual(query_to_dict["notification"]["host"], "string")
        self.assertEqual(query_to_dict["notification"]["queue"], "string")
        self.assertEqual(query_to_dict["upload"]["provider"], "ibm")
        self.assertEqual(query_to_dict["upload"]["endpoint"], "string")
        self.assertEqual(query_to_dict["upload"]["bucket"], "string")
        self.assertEqual(query_to_dict["upload"]["token"], "string")
        self.assertEqual(query_to_dict["processor"][0]["order"], 0)
        self.assertEqual(query_to_dict["processor"][0]["type"], "string")
        self.assertEqual(query_to_dict["processor"][0]["options"][0]["name"], "string")
        self.assertEqual(query_to_dict["processor"][0]["options"][0]["value"], "string")
        self.assertEqual(query_to_dict["processor"][1]["order"], 1)
        self.assertEqual(query_to_dict["processor"][1]["type"], "string2")
        self.assertEqual(query_to_dict["processor"][1]["options"][0]["name"], "string2")
        self.assertEqual(query_to_dict["processor"][1]["options"][0]["value"], "string2")
        
    #
    def test_query_to_dict_query_post(self):
        self.logger.info('test_query_to_dict_query_post')
        
        query = query_module.Query
    
        query_from_dict            = None
        query_to_dict_query_post   = None
                
        got_exception = False
    
        try:
            query_from_dict            = query.from_dict(query_dict)
            query_to_dict_query_post   = query_from_dict.to_dict_query_post()
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
        self.assertIsInstance(query_to_dict_query_post, dict)
        self.assertEqual(query_to_dict_query_post["name"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["id"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["type"], "raster")
        self.assertEqual(query_to_dict_query_post["layers"][0]["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["alias"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["filterOnly"], True)
        self.assertEqual(query_to_dict_query_post["layers"][0]["aggregation"], "None")
        self.assertEqual(query_to_dict_query_post["layers"][0]["filter"]["value"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["filter"]["operator"], "EQ")
        self.assertEqual(query_to_dict_query_post["layers"][0]["dimensions"][0]["name"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["dimensions"][0]["value"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["dimensions"][0]["operator"], "EQ")
        self.assertEqual(query_to_dict_query_post["layers"][0]["dimensions"][0]["options"][0], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["expression"], "string")
        self.assertEqual(query_to_dict_query_post["layers"][0]["output"], True)
        self.assertEqual(query_to_dict_query_post["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(query_to_dict_query_post["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(query_to_dict_query_post["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(query_to_dict_query_post["spatial"]["type"], "point")
        self.assertEqual(query_to_dict_query_post["spatial"]["aoi"], "string")
        self.assertEqual(query_to_dict_query_post["spatial"]["coordinates"][0], 0)
        self.assertEqual(query_to_dict_query_post["spatial"]["aggregation"]["aoi"][0], "string")
        self.assertEqual(query_to_dict_query_post["outputType"], "json")
        self.assertEqual(query_to_dict_query_post["outputLevel"], 0)
        self.assertEqual(query_to_dict_query_post["description"], "string")
        self.assertEqual(query_to_dict_query_post["publish"], True)
        self.assertEqual(query_to_dict_query_post["notification"]["type"], "rabbitmq")
        self.assertEqual(query_to_dict_query_post["notification"]["host"], "string")
        self.assertEqual(query_to_dict_query_post["notification"]["queue"], "string")
        self.assertEqual(query_to_dict_query_post["upload"]["provider"], "ibm")
        self.assertEqual(query_to_dict_query_post["upload"]["endpoint"], "string")
        self.assertEqual(query_to_dict_query_post["upload"]["bucket"], "string")
        self.assertEqual(query_to_dict_query_post["upload"]["token"], "string")
        self.assertEqual(query_to_dict_query_post["processor"][0]["order"], 0)
        self.assertEqual(query_to_dict_query_post["processor"][0]["type"], "string")
        self.assertEqual(query_to_dict_query_post["processor"][0]["options"][0]["name"], "string")
        self.assertEqual(query_to_dict_query_post["processor"][0]["options"][0]["value"], "string")
        self.assertEqual(query_to_dict_query_post["processor"][1]["order"], 1)
        self.assertEqual(query_to_dict_query_post["processor"][1]["type"], "string2")
        self.assertEqual(query_to_dict_query_post["processor"][1]["options"][0]["name"], "string2")
        self.assertEqual(query_to_dict_query_post["processor"][1]["options"][0]["value"], "string2")

    #
    def test_query_from_json(self):
        self.logger.info('test_query_from_json')

        query = query_module.Query
        
        query_from_json = None

        got_exception = False

        try:
            query_from_json = query.from_json(query_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_from_json.name, "string")
        self.assertEqual(query_from_json.layers[0].id, "string")
        self.assertEqual(query_from_json.layers[0].type, "raster")
        self.assertEqual(query_from_json.layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(query_from_json.layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(query_from_json.layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(query_from_json.layers[0].alias, "string")
        self.assertEqual(query_from_json.layers[0].filter_only, True)
        self.assertEqual(query_from_json.layers[0].aggregation, "None")
        self.assertEqual(query_from_json.layers[0].filter.value, "string")
        self.assertEqual(query_from_json.layers[0].filter.operator, "EQ")
        self.assertEqual(query_from_json.layers[0].dimensions[0].name, "string")
        self.assertEqual(query_from_json.layers[0].dimensions[0].value, "string")
        self.assertEqual(query_from_json.layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(query_from_json.layers[0].dimensions[0].options[0], "string")
        self.assertEqual(query_from_json.layers[0].expression, "string")
        self.assertEqual(query_from_json.layers[0].output, True)
        self.assertEqual(query_from_json.temporal.intervals[0].snapshot, "string")
        self.assertEqual(query_from_json.temporal.intervals[0].end, "string")
        self.assertEqual(query_from_json.temporal.intervals[0].start, "string")
        self.assertEqual(query_from_json.spatial.type, "point")
        self.assertEqual(query_from_json.spatial.aoi, "string")
        self.assertEqual(query_from_json.spatial.coordinates[0], 0)
        self.assertEqual(query_from_json.spatial.aggregation.aoi[0], "string")
        self.assertEqual(query_from_json.output_type, "json")
        self.assertEqual(query_from_json.output_level, 0)
        self.assertEqual(query_from_json.description, "string")
        self.assertEqual(query_from_json.publish, True)
        self.assertEqual(query_from_json.notification.type, "rabbitmq")
        self.assertEqual(query_from_json.notification.host, "string")
        self.assertEqual(query_from_json.notification.queue, "string")
        self.assertEqual(query_from_json.upload.provider, "ibm")
        self.assertEqual(query_from_json.upload.endpoint, "string")
        self.assertEqual(query_from_json.upload.bucket, "string")
        self.assertEqual(query_from_json.upload.token, "string")
        self.assertEqual(query_from_json.processor[0].order, 0)
        self.assertEqual(query_from_json.processor[0].type, "string")
        self.assertEqual(query_from_json.processor[0].options[0].name, "string")
        self.assertEqual(query_from_json.processor[0].options[0].value, "string")
        self.assertEqual(query_from_json.processor[1].order, 1)
        self.assertEqual(query_from_json.processor[1].type, "string2")
        self.assertEqual(query_from_json.processor[1].options[0].name, "string2")
        self.assertEqual(query_from_json.processor[1].options[0].value, "string2")
    
    #
    def test_query_to_json(self):
        self.logger.info('test_query_to_json')
        
        query = query_module.Query
        
        query_from_json = None
        query_to_json = None

        got_exception = False
        
        try:
            query_from_json = query.from_json(query_json)
            query_to_json = query_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
    
    #
    def test_query_to_json_query_post(self):
        self.logger.info('test_query_to_json_query_post')
        
        query = query_module.Query
        
        query_from_json          = None
        query_to_json_query_post = None

        got_exception = False
        
        try:
            query_from_json          = query.from_json(query_json)
            query_to_json_query_post = query_from_json.to_json_query_post()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
          
    @mock.patch('ibmpairs.client.Client.put', 
                side_effect=mocked_favorite_requests_put
               )
    def test_favorite(self, mock_put):
        self.logger.info('test_favorite')
        
        c      = client.Client() 
        query  = query_module.Query()
        query.client = c
        
        got_exception_1 = False
        got_exception_2 = False
        got_exception_3 = False
        
        try:
            query.favorite(id = 1)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertFalse(got_exception_1)
        
        try:
            query.favorite(id = 2)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertTrue(got_exception_1)
        
        try:
            query.favorite(id = 3)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertTrue(got_exception_1)
        
    @mock.patch('ibmpairs.client.Client.put', 
                side_effect=mocked_favorite_requests_put
               )
    def test_unfavorite(self, mock_put):
        self.logger.info('test_unfavorite')
        
        c      = client.Client() 
        query  = query_module.Query()
        query.client = c
        
        got_exception_1 = False
        got_exception_2 = False
        got_exception_3 = False
        
        try:
            query.unfavorite(id = 1)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertFalse(got_exception_1)
        
        try:
            query.unfavorite(id = 2)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertTrue(got_exception_1)
        
        try:
            query.unfavorite(id = 3)
        except Exception as ex:
            got_exception_1 = True
        
        self.assertTrue(got_exception_1)
    
    #    
    def test_replace_dates(self):
        self.logger.info('test_replace_dates')
        
        query = query_module.Query

        query_from_dict_replace_dates = None
            
        got_exception   = False
        got_exception_2 = False

        try:
            query_from_dict_replace_dates = query.from_dict(query_replace_dates_dict)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_from_dict_replace_dates.name, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].id, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].alias, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[1].id, "string2")
        self.assertEqual(query_from_dict_replace_dates.layers[1].alias, "string2.9999999999999>9999999999999")
        self.assertEqual(query_from_dict_replace_dates.layers[1].temporal.intervals[0].start, "string2")
        self.assertEqual(query_from_dict_replace_dates.layers[1].temporal.intervals[0].end, "string2")
        self.assertEqual(query_from_dict_replace_dates.temporal.intervals[0].start, "string")
        self.assertEqual(query_from_dict_replace_dates.temporal.intervals[0].end, "string")
        
        try:
            start = datetime(1970,1,1,1,0,0)
            end = datetime(1970,1,31,0,0,0)
            query_from_dict_replace_dates.replace_dates(start, end, 'test_replace_dates')
        except Exception as ex:
            got_exception_2 = True
            
        self.assertFalse(got_exception_2)        
        self.assertEqual(query_from_dict_replace_dates.name, "test_replace_dates")
        self.assertEqual(query_from_dict_replace_dates.layers[0].id, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].alias, "string")
        self.assertEqual(query_from_dict_replace_dates.layers[0].temporal.intervals[0].start, "1970-01-01")
        self.assertEqual(query_from_dict_replace_dates.layers[0].temporal.intervals[0].end, "1970-01-31")
        self.assertEqual(query_from_dict_replace_dates.layers[1].id, "string2")
        #self.assertEqual(query_from_dict_replace_dates.layers[1].alias, "string2.0>2588400000")
        self.assertEqual(query_from_dict_replace_dates.layers[1].temporal.intervals[0].start, "1970-01-01")
        self.assertEqual(query_from_dict_replace_dates.layers[1].temporal.intervals[0].end, "1970-01-31")
        self.assertEqual(query_from_dict_replace_dates.temporal.intervals[0].start, "1970-01-01")
        self.assertEqual(query_from_dict_replace_dates.temporal.intervals[0].end, "1970-01-31")
        
    #    
    def test_is_bulk(self):
        self.logger.info('test_is_bulk')  
        
        query = query_module.Query

        query_from_dict_is_bulk_1 = None
        query_from_dict_is_bulk_2 = None
        query_from_dict_is_bulk_3 = None
            
        got_exception = False

        self.logger.info('test_is_bulk: point') 
        
        try:
            query_from_dict_is_bulk_1 = query.from_dict(query_dict_is_bulk_1)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(query_from_dict_is_bulk_1.is_bulk())
        
        self.logger.info('test_is_bulk: square')
        
        try:
            query_from_dict_is_bulk_2 = query.from_dict(query_dict_is_bulk_2)
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(query_from_dict_is_bulk_2.is_bulk())
        
        self.logger.info('test_is_bulk: poly')
        
        try:
            query_from_dict_is_bulk_3 = query.from_dict(query_dict_is_bulk_3)
        except Exception as ex:
            got_exception = True
            
        self.assertTrue(query_from_dict_is_bulk_3.is_bulk())
            
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_async_submit(self, mock_post):
        self.logger.info('test_async_submit')
        
        c      = client.Client() 
        query  = query_module.Query

        query_async_submit     = None
        query_async_submit_404 = None
        query_async_submit_502 = None
        query_async_submit_401 = None
            
        got_exception     = False
        got_exception_404 = False
        got_exception_502 = False
        got_exception_401 = False

        self.logger.info('test_async_submit: 200')

        try:
            query_async_submit = query.from_dict(query_dict)
            query_async_submit.name = "1"
            query_async_submit.spatial.type = "square"
            asyncio.run(query_async_submit.async_submit(query  = query_async_submit,
                                                        client = c
                                                       )
                       )
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_async_submit.id, "1")
        self.assertEqual(query_async_submit.submit_response.id, "1")
        self.assertEqual(query_async_submit.submit_response.url, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].layer_id, 0)
        self.assertEqual(query_async_submit.submit_response.data[0].layer_name, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].dataset, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].timestamp, 0)
        self.assertEqual(query_async_submit.submit_response.data[0].longitude, 0)
        self.assertEqual(query_async_submit.submit_response.data[0].latitude, 0)
        self.assertEqual(query_async_submit.submit_response.data[0].region, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].value, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].unit, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].pty, "string")
        self.assertEqual(query_async_submit.submit_response.data[0].aggregation, "string")

        self.logger.info('test_async_submit: 404')

        try:
            query_async_submit_404 = query.from_dict(query_dict)
            query_async_submit_404.name = "2"
            asyncio.run(query_async_submit_404.async_submit(query  = query_async_submit_404,
                                                            client = c
                                                           )
                       )
        except Exception as ex:
            got_exception_404 = True
        
        self.assertTrue(got_exception_404)
        
        self.assertEqual(query_async_submit_404.submit_response.message, "Error: 404 Not Found.")
        
        self.logger.info('test_async_submit: 502, no body')

        try:
            query_async_submit_502 = query.from_dict(query_dict)
            query_async_submit_502.name = "3"
            asyncio.run(query_async_submit_502.async_submit(query  = query_async_submit_502,
                                                            client = c
                                                           )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_submit_502.submit_response.message, "FAILED")
        
        self.logger.info('test_async_submit: 401')

        try:
            query_async_submit_401 = query.from_dict(query_dict)
            query_async_submit_401.name = "9"
            asyncio.run(query_async_submit_401.async_submit(query  = query_async_submit_401,
                                                            client = c
                                                           )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_submit_401.submit_response.message, "Error: 401 Unauthorized.")
        
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_submit(self, mock_post):
        self.logger.info('test_submit')
        
        c      = client.Client() 
        query  = query_module.Query

        query_submit     = None
            
        got_exception     = False

        self.logger.info('test_submit: 200')

        try:
            query_submit = query.from_dict(query_dict)
            query_submit.name = "1"
            query_submit.spatial.type = "square"
            query_submit.submit(client = c)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_submit.id, "1")
        self.assertEqual(query_submit.submit_response.id, "1")
        self.assertEqual(query_submit.submit_response.url, "string")
        self.assertEqual(query_submit.submit_response.data[0].layer_id, 0)
        self.assertEqual(query_submit.submit_response.data[0].layer_name, "string")
        self.assertEqual(query_submit.submit_response.data[0].dataset, "string")
        self.assertEqual(query_submit.submit_response.data[0].timestamp, 0)
        self.assertEqual(query_submit.submit_response.data[0].longitude, 0)
        self.assertEqual(query_submit.submit_response.data[0].latitude, 0)
        self.assertEqual(query_submit.submit_response.data[0].region, "string")
        self.assertEqual(query_submit.submit_response.data[0].value, "string")
        self.assertEqual(query_submit.submit_response.data[0].unit, "string")
        self.assertEqual(query_submit.submit_response.data[0].pty, "string")
        self.assertEqual(query_submit.submit_response.data[0].aggregation, "string")
    
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_status_async_get
               )    
    def test_async_status(self, mock_get):
        self.logger.info('test_async_status')
        
        c      = client.Client() 
        query  = query_module.Query
        
        self.logger.info('test_async_status: 200 Succeeded(20)')

        query_async_status_success = None
        
        got_exception = False

        try:
            query_async_status_success = query.from_dict(query_dict)
            query_async_status_success.id = "1"
            query_async_status_success.spatial.type = "square"
            asyncio.run(query_async_status_success.async_status(query  = query_async_status_success,
                                                                client = c,
                                                                poll   = False
                                                               )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_success.status_response.status, "Succeeded(20)")
        
        self.logger.info('test_async_status: 200 NoDataFound(21)')
        
        query_async_status_no_data = None
        
        got_exception = False

        try:
            query_async_status_no_data = query.from_dict(query_dict)
            query_async_status_no_data.id = "2"
            query_async_status_no_data.spatial.type = "square"
            asyncio.run(query_async_status_no_data.async_status(query  = query_async_status_no_data,
                                                                client = c,
                                                                poll   = False
                                                               )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_no_data.status_response.status, "NoDataFound(21)")
        
        self.logger.info('test_async_status: 200 Killed(30)')
        
        query_async_status_killed = None
        
        got_exception = False

        try:
            query_async_status_killed = query.from_dict(query_dict)
            query_async_status_killed.id = "3"
            query_async_status_killed.spatial.type = "square"
            asyncio.run(query_async_status_killed.async_status(query  = query_async_status_killed,
                                                               client = c,
                                                               poll   = False
                                                              )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_killed.status_response.status, "Killed(30)")
        
        self.logger.info('test_async_status: 200 Deleted(31)')
        
        query_async_status_deleted = None
        
        got_exception = False

        try:
            query_async_status_deleted = query.from_dict(query_dict)
            query_async_status_deleted.id = "4"
            query_async_status_deleted.spatial.type = "square"
            asyncio.run(query_async_status_deleted.async_status(query  = query_async_status_deleted,
                                                                client = c,
                                                                poll   = False
                                                               )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_deleted.status_response.status, "Deleted(31)")
        
        self.logger.info('test_async_status: 200 Failed(40)')
        
        query_async_status_failed = None
        
        got_exception = False

        try:
            query_async_status_failed = query.from_dict(query_dict)
            query_async_status_failed.id = "5"
            query_async_status_failed.spatial.type = "square"
            asyncio.run(query_async_status_failed.async_status(query  = query_async_status_failed,
                                                               client = c,
                                                               poll   = False
                                                              )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_failed.status_response.status, "Failed(40)")
        
        self.logger.info('test_async_status: 200 FailedConversion(41)')
        
        query_async_status_failed_conversion = None
        
        got_exception = False

        try:
            query_async_status_failed_conversion = query.from_dict(query_dict)
            query_async_status_failed_conversion.id = "6"
            query_async_status_failed_conversion.spatial.type = "square"
            asyncio.run(query_async_status_failed_conversion.async_status(query  = query_async_status_failed_conversion,
                                                                          client = c,
                                                                          poll   = False
                                                                         )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_failed_conversion.status_response.status, "FailedConversion(41)")

        self.logger.info('test_async_status: skip point query')
        
        query_async_status_skip = None
        
        got_exception = False

        try:
            query_async_status_skip = query.from_dict(query_dict)
            query_async_status_skip.id = "7"
            asyncio.run(query_async_status_skip.async_status(query  = query_async_status_skip,
                                                             client = c,
                                                             poll   = False
                                                            )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_skip.status_response.status, "A real time point query is returned at the time of executing the Query.submit() method. The status is therefore complete. Skipping.")
        
        self.logger.info('test_async_status: 404')
        
        query_async_status_404 = None
        
        got_exception = False

        try:
            query_async_status_404 = query.from_dict(query_dict)
            query_async_status_404.id = "8"
            query_async_status_404.spatial.type = "square"
            asyncio.run(query_async_status_404.async_status(query  = query_async_status_404,
                                                            client = c,
                                                            poll   = False
                                                           )
                       )
        except Exception as ex:
                got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_status_404.status_response.status, "FAILED: 404")
        
        self.logger.info('test_async_status: 503')
        
        query_async_status_503 = None
        
        got_exception = False

        try:
            query_async_status_503 = query.from_dict(query_dict)
            query_async_status_503.id = "9"
            query_async_status_503.spatial.type = "square"
            asyncio.run(query_async_status_503.async_status(query  = query_async_status_503,
                                                            client = c,
                                                            poll   = False
                                                           )
                       )
        except Exception as ex:
                got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_status_503.status_response.status, "FAILED: 503")
        
        self.logger.info('test_async_status: 200 poll success')
        
        query_async_status_poll_success = None
        
        got_exception = False

        try:
            query_async_status_poll_success = query.from_dict(query_dict)
            query_async_status_poll_success.id = "10"
            query_async_status_poll_success.spatial.type = "square"
            asyncio.run(query_async_status_poll_success.async_status(query  = query_async_status_poll_success,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_poll_success.status_response.status, "Succeeded(20)")
        
        self.logger.info('test_async_status: 200 poll failed')
        
        query_async_status_poll_failed = None
        
        got_exception = False

        try:
            query_async_status_poll_failed = query.from_dict(query_dict)
            query_async_status_poll_failed.id = "11"
            query_async_status_poll_failed.spatial.type = "square"
            asyncio.run(query_async_status_poll_failed.async_status(query  = query_async_status_poll_failed,
                                                                    client = c
                                                                   )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_status_poll_failed.status_response.status, "Failed(40)")
        
        self.logger.info('test_async_status: -999 unspecified error')
        
        query_async_status_unspec = None
        
        got_exception = False

        try:
            query_async_status_unspec = query.from_dict(query_dict)
            query_async_status_unspec.id = "12"
            query_async_status_unspec.spatial.type = "square"
            asyncio.run(query_async_status_unspec.async_status(query  = query_async_status_unspec,
                                                               client = c
                                                              )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_status_unspec.status_response.status, "FAILED: -999")
        
        self.logger.info('test_async_status: no id')
        
        query_async_status_no_id = None
        
        got_exception = False

        try:
            query_async_status_no_id = query.from_dict(query_dict_is_bulk_2)
            asyncio.run(query_async_status_no_id.async_status(query  = query_async_status_no_id,
                                                              client = c
                                                             )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_status_no_id.status_response.status, "The query id was not present in the query object.")


    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_status_async_get
               )    
    def test_status(self, mock_get):
        self.logger.info('test_status')
        
        c      = client.Client() 
        query  = query_module.Query
        
        self.logger.info('test_status: 200 poll success')
    
        query_status_poll_success = None
    
        got_exception = False

        try:
            query_status_poll_success = query.from_dict(query_dict)
            query_status_poll_success.id = "10"
            query_status_poll_success.spatial.type = "square"
            query_status_poll_success.status(client = c)
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
    
        self.assertEqual(query_status_poll_success.status_response.status, "Succeeded(20)")

    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_status_async_get
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_async_submit_and_check_status(self, mock_post, mock_get):
        self.logger.info('test_async_submit_and_check_status')
        
        c      = client.Client() 
        query  = query_module.Query

        query_async_scs = None
            
        got_exception = False

        self.logger.info('test_async_submit_and_check_status: 200')

        try:
            query_async_scs = query.from_dict(query_dict)
            query_async_scs.name         = "1"
            query_async_scs.spatial.type = "square"
            asyncio.run(query_async_scs.async_submit_and_check_status(query  = query_async_scs,
                                                                      client = c
                                                                     )
                       )
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_async_scs.id, "1")
        self.assertEqual(query_async_scs.status_response.status, "Succeeded(20)")
    
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_status_async_get
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_submit_and_check_status(self, mock_post, mock_get):
        self.logger.info('test_submit_and_check_status')
        
        c      = client.Client() 
        query  = query_module.Query

        query_scs = None
            
        got_exception = False

        self.logger.info('test_submit_and_check_status: 200')

        try:
            query_scs = query.from_dict(query_dict)
            query_scs.name         = "1"
            query_scs.spatial.type = "square"
            query_scs.submit_and_check_status(client = c)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_scs.id, "1")
        self.assertEqual(query_scs.status_response.status, "Succeeded(20)")


    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    def test_async_download(self, mock_get):
        self.logger.info('test_async_download: point skip')
        
        c      = client.Client() 
        query  = query_module.Query

        query_async_download_skip = None

        got_exception = False

        try:
            query_async_download_skip = query.from_dict(query_dict_is_bulk_1)
            asyncio.run(query_async_download_skip.async_download(query  = query_async_download_skip,
                                                                 client = c
                                                                )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_download_skip.download_status, "SKIPPED")
        
        self.logger.info('test_async_download: download ok')
        self.logger.info('test_async_download: unzip ok')
        self.logger.info('test_async_download: create folder')
        self.logger.info('test_async_download: relative folder')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_relative = None
        
        got_exception = False
        
        try:
            query_async_download_relative = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_relative.id = '1625544000_31302646'
            # The prepared output has a data entry in submit_response (its a generic structure), needs to be removed.
            asyncio.run(query_async_download_relative.async_download(query  = query_async_download_relative,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_download_relative.download_status, "SUCCEEDED")
        
        md5_test_zip = hashlib.md5()
        test_zip = open("tests/data/v2/1625544000_31302646.zip", "rb")
        content_test_zip = test_zip.read()
        md5_test_zip.update(content_test_zip)
        digest_test_zip = md5_test_zip.hexdigest()
        
        md5_downloaded = hashlib.md5()
        downloaded = open("download/1625544000_31302646.zip", "rb")
        content_downloaded = downloaded.read()
        md5_downloaded.update(content_downloaded)
        digest_downloaded = md5_downloaded.hexdigest()
        
        self.assertEqual(digest_test_zip, digest_downloaded)
        
        self.assertTrue(os.path.isdir("download"))
        
        self.logger.info('removing \'download/1625544000_31302646.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip'))
        self.logger.info('removing \'download/1625544000_31302646\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302646')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302646'))
        
        self.logger.info('test_async_download: fixed folder')
        self.logger.info('test_async_download: changed file name from id')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_change_filename = None
        
        got_exception = False
        
        try:
            query_async_download_change_filename = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_change_filename.id = '1625544000_31302646'
            query_async_download_change_filename.download_folder = '/tmp'
            query_async_download_change_filename.download_file_name = 'ibmpairs_unit_test'
            asyncio.run(query_async_download_change_filename.async_download(query  = query_async_download_change_filename,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_download_change_filename.download_status, "SUCCEEDED")
        
        self.assertTrue(os.path.isdir("/tmp"))
        self.assertTrue(os.path.isfile("/tmp/ibmpairs_unit_test.zip"))
        
        self.logger.info('removing \'/tmp/ibmpairs_unit_test.zip\'')
        if os.path.isfile('/tmp/ibmpairs_unit_test.zip'):
            os.remove('/tmp/ibmpairs_unit_test.zip')
        self.logger.info('removing \'/tmp/ibmpairs_unit_test\'')
        if os.path.exists('tmp/ibmpairs_unit_test'):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/ibmpairs_unit_test'))
        
        self.logger.info('test_async_download: download failed')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_failed = None
        
        got_exception = False
        
        try:
            query_async_download_failed = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_failed.id = '1625544000_31302647'
            asyncio.run(query_async_download_failed.async_download(query  = query_async_download_failed,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_download_failed.download_status, "FAILED")
        
        self.logger.info('test_async_download: download ok, zip failed')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_unzip_failed = None
        
        got_exception = False
        
        try:
            query_async_unzip_failed = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_unzip_failed.id = '1625544000_31302645'
            asyncio.run(query_async_unzip_failed.async_download(query  = query_async_unzip_failed,
                                                                client = c
                                                               )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_unzip_failed.download_status, "FAILED")
        
        self.logger.info('removing \'download/1625544000_31302645.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302645.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302645.zip'))
        
        self.logger.info('test_async_download: query status incomplete to success')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_poll_success = None
        
        got_exception = False
        
        try:
            query_async_download_poll_success = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_poll_success.id = '1625544000_31302648'
            asyncio.run(query_async_download_poll_success.async_download(query  = query_async_download_poll_success,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        
        self.assertEqual(query_async_download_poll_success.download_status, "SUCCEEDED")
        
        self.logger.info('removing \'download/1625544000_31302648.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302648.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302648.zip'))
        self.logger.info('removing \'download/1625544000_31302648\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302648')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302648'))
        
        self.logger.info('test_async_download: query status incomplete to failure')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_poll_fail = None
        
        got_exception = False
        
        try:
            query_async_download_poll_fail = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_poll_fail.id = '1625544000_31302649'
            asyncio.run(query_async_download_poll_fail.async_download(query  = query_async_download_poll_fail,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_download_poll_fail.download_status, "FAILED")
        
        self.logger.info('test_async_download: query deleted')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_download_deleted = None
        
        got_exception = False
        
        try:
            query_async_download_deleted = query.from_dict(query_dict_download_status_20_no_point_values)
            query_async_download_deleted.id = '1625544000_31302650'
            asyncio.run(query_async_download_deleted.async_download(query  = query_async_download_deleted,
                                                                     client = c
                                                                    )
                       )
        except Exception as ex:
            got_exception = True
        
        self.assertTrue(got_exception)
        
        self.assertEqual(query_async_download_deleted.download_status, "FAILED")
        
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    def test_download(self, mock_get):
        self.logger.info('test_download: success')
        
        c      = client.Client() 
        query  = query_module.Query

        query_download = None

        got_exception = False

        try:
            query_download = query.from_dict(query_dict_download_status_20_no_point_values)
            query_download.id = '1625544000_31302646'
            query_download.download(client = c)
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
    
        self.assertEqual(query_download.status_response.status, "Succeeded(20)")
        
        self.logger.info('removing \'download/1625544000_31302646.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip'))
        self.logger.info('removing \'download/1625544000_31302646\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302646')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302646'))
        
        self.logger.info('test_download: folder parameters')
        
        c      = client.Client() 
        query  = query_module.Query

        query_download_params = None

        got_exception = False

        try:
            query_download_params = query.from_dict(query_dict_download_status_20_no_point_values)
            query_download_params.id = '1625544000_31302646'
            query_download_params.download(client             = c,
                                           download_folder    = '/tmp',
                                           download_file_name = 'ibmpairs_unit_test_2'
                                          )
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
    
        self.assertEqual(query_download_params.status_response.status, "Succeeded(20)")
        self.assertTrue(os.path.isfile("/tmp/ibmpairs_unit_test_2.zip"))
        
        self.logger.info('removing \'/tmp/ibmpairs_unit_test_2.zip\'')
        if os.path.isfile('/tmp/ibmpairs_unit_test_2.zip'):
            os.remove('/tmp/ibmpairs_unit_test_2.zip')
        self.logger.info('removing \'/tmp/ibmpairs_unit_test_2\'')
        if os.path.exists('/tmp/ibmpairs_unit_test_2'):
            shutil.rmtree('/tmp/ibmpairs_unit_test_2')

    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    def test_download_csv(self, mock_get):
        self.logger.info('test_download: csv success')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_download = None
        
        got_exception = False
        
        try:
            query_download = query.from_dict(query_dict_download_status_20_no_point_values)
            query_download.id = '1702468800_05116057'
            query_download.download(client = c)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        
        self.assertEqual(query_download.status_response.status, "Succeeded(20)")
        
        self.logger.info('removing \'download/1702468800_05116057.csv\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1702468800_05116057.csv')):
            os.remove(os.path.join(os.getcwd(), 'download/1702468800_05116057.csv'))

            
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    def test_download_json(self, mock_get):
        self.logger.info('test_download: json success')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_download = None
        
        got_exception = False
        
        try:
            query_download = query.from_dict(query_dict_download_status_20_no_point_values)
            query_download.id = '1702468800_05212195'
            query_download.download(client = c)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        
        self.assertEqual(query_download.status_response.status, "Succeeded(20)")
        
        self.logger.info('removing \'download/1702468800_05212195.json\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1702468800_05212195.json')):
            os.remove(os.path.join(os.getcwd(), 'download/1702468800_05212195.json'))

    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    def test_check_status_and_download(self, mock_get):
        self.logger.info('test_check_status_and_download: success')
        
        c      = client.Client() 
        query  = query_module.Query

        query_check_status_and_download = None

        got_exception = False

        try:            
            query_check_status_and_download = query.from_dict(query_dict_download_status_20_no_point_values)
            query_check_status_and_download.id = '1625544000_31302646'
            query_check_status_and_download.check_status_and_download(client = c)
        except Exception as ex:
            got_exception = True
    
        self.assertFalse(got_exception)
    
        self.assertEqual(query_check_status_and_download.status_response.status, "Succeeded(20)")

        self.logger.info('removing \'download/1625544000_31302646.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip'))
        self.logger.info('removing \'download/1625544000_31302646\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302646')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302646'))


    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_async_submit_check_status_and_download(self, mock_post, mock_get):
        self.logger.info('test_async_submit_check_status_and_download')
        
        c      = client.Client() 
        query  = query_module.Query

        query_async_scsd = None
            
        got_exception = False

        self.logger.info('test_async_submit_check_status_and_download: 200')

        try:
            query_async_scsd = query.from_dict(query_dict)
            query_async_scsd.name         = "1625544000_31302646"
            query_async_scsd.spatial.type = "square"
            asyncio.run(query_async_scsd.async_submit_check_status_and_download(query  = query_async_scsd,
                                                                                client = c
                                                                               )
                       )
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_async_scsd.id, "1625544000_31302646")
        self.assertEqual(query_async_scsd.status_response.status, "Succeeded(20)")
        self.assertEqual(query_async_scsd.download_status, "SUCCEEDED")
        
        self.logger.info('removing \'download/1625544000_31302646.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip'))
        self.logger.info('removing \'download/1625544000_31302646\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302646')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302646'))

    
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_submit_check_status_and_download(self, mock_post, mock_get):
        self.logger.info('test_submit_check_status_and_download')
        
        c      = client.Client() 
        query  = query_module.Query

        query_scsd = None
            
        got_exception = False

        self.logger.info('test_submit_check_status_and_download: 200')

        try:
            query_scsd = query.from_dict(query_dict)
            query_scsd.name         = "1625544000_31302646"
            query_scsd.spatial.type = "square"
            query_scsd.submit_check_status_and_download(client = c)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_scsd.id, "1625544000_31302646")
        self.assertEqual(query_scsd.status_response.status, "Succeeded(20)")
        self.assertEqual(query_scsd.download_status, "SUCCEEDED")
        
        self.logger.info('removing \'download/1625544000_31302646.zip\'')
        if os.path.isfile(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip')):
            os.remove(os.path.join(os.getcwd(), 'download/1625544000_31302646.zip'))
        self.logger.info('removing \'download/1625544000_31302646\'')
        if os.path.exists(os.path.join(os.getcwd(), 'download/1625544000_31302646')):
            shutil.rmtree(os.path.join(os.getcwd(), 'download/1625544000_31302646'))
        
    #mocked_merge_requests_put
    @mock.patch('ibmpairs.client.Client.put', 
                side_effect=mocked_merge_requests_put
               )
    def test_merge_query_into_base(self, mock_put):
        
        self.logger.info('test_merge_query_into_base: success')
        
        c      = client.Client() 
        query  = query_module.Query

        query_merge_success = None
                
        got_exception = False

        try:
            query_merge_success = query.from_dict(query_dict)
            query_merge_success.merge_query_into_base(other_job_id = "2",
                                                      base_job_id  = "1",
                                                      client       = c
                                                     )
        except Exception as ex:
            got_exception = True
                
        self.assertFalse(got_exception)
        self.assertEqual(query_merge_success.merge_status, "SUCCEEDED")
        
        self.logger.info('test_merge_query_into_base: 401')
        
        c      = client.Client() 
        query  = query_module.Query

        query_merge_401 = None
                
        got_exception = False

        try:
            query_merge_401 = query.from_dict(query_dict)
            query_merge_401.merge_query_into_base(other_job_id = "4",
                                                  base_job_id  = "3",
                                                  client       = c
                                                 )
        except Exception as ex:
            got_exception = True
                
        self.assertTrue(got_exception)
        self.assertEqual(query_merge_401.merge_status, "FAILED")
        
        self.logger.info('test_merge_query_into_base: 404')
        
        c      = client.Client() 
        query  = query_module.Query

        query_merge_404 = None
                
        got_exception = False

        try:
            query_merge_404 = query.from_dict(query_dict)
            query_merge_404.merge_query_into_base(other_job_id = "3",
                                                  base_job_id  = "2",
                                                  client       = c
                                                 )
        except Exception as ex:
            got_exception = True
                
        self.assertTrue(got_exception)
        self.assertEqual(query_merge_404.merge_status, "FAILED")
        
        self.logger.info('test_merge_query_into_base: 412')
        
        c      = client.Client() 
        query  = query_module.Query

        query_merge_412 = None
                
        got_exception = False

        try:
            query_merge_412 = query.from_dict(query_dict)
            query_merge_412.merge_query_into_base(other_job_id = "5",
                                                  base_job_id  = "4",
                                                  client       = c
                                                 )
        except Exception as ex:
            got_exception = True
                
        self.assertTrue(got_exception)
        self.assertEqual(query_merge_412.merge_status, "FAILED")
        
        self.logger.info('test_merge_query_into_base: 503')
        
        c      = client.Client() 
        query  = query_module.Query

        query_merge_503 = None
                
        got_exception = False

        try:
            query_merge_503 = query.from_dict(query_dict)
            query_merge_503.merge_query_into_base(other_job_id = "100",
                                                  base_job_id  = "99",
                                                  client       = c
                                                 )
        except Exception as ex:
            got_exception = True
                
        self.assertTrue(got_exception)
        self.assertEqual(query_merge_503.merge_status, "FAILED")

        self.logger.info('test_merge_query_into_base: Query type')
        
        c              = client.Client() 
        query          = query_module.Query
        query_other    = query_module.Query()
        query_other.id = '2'
        query_base     = query_module.Query()
        query_base.id  = '1'

        query_merge_success = None
                
        got_exception = False

        try:
            query_merge_success = query.from_dict(query_dict)
            query_merge_success.merge_query_into_base(other_job_id = query_other,
                                                      base_job_id  = query_base,
                                                      client       = c
                                                     )
        except Exception as ex:
            got_exception = True
                
        self.assertFalse(got_exception)
        self.assertEqual(query_merge_success.merge_status, "SUCCEEDED")
    
    #
    def test_point_data_as_dataframe_csv(self):
        self.logger.info('test_point_data_as_dataframe_csv')
        
        query_df_csv = query_module.Query

        query_from_dict_df_csv = None
        query_as_df_csv = None
            
        got_exception = False

        try:
            query_from_dict_df_csv = query_df_csv.from_dict(query_dict)
            query_from_dict_df_csv.submit_response.data = "layerId,timestamp,longitude,latitude,value,region,property,alias\n16100,1421528400000,139.7,35.7,273.918212890625,,,"
            query_as_df_csv = query_from_dict_df_csv.point_data_as_dataframe()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(int(query_as_df_csv.head(1)["layerId"]), 16100)
        self.assertEqual(int(query_as_df_csv.head(1)["timestamp"]), 1421528400000)
        self.assertEqual(float(query_as_df_csv.head(1)["longitude"]), 139.7)
        self.assertEqual(float(query_as_df_csv.head(1)["latitude"]), 35.7)
        self.assertEqual(float(query_as_df_csv.head(1)["value"]), 273.918212890625)
        
    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_download_async_get
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    def test_point_query_online_intransparent_batch(self, mock_post, mock_get):
        self.logger.info('test_point_query_online_intransparent_batch')
        
        self.logger.info('test_point_query_online_intransparent_batch: 200')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_point_online = None
        
        got_exception = False
        
        try:
            query_async_point_online = query.from_dict(query_dict)
            query_async_point_online.name         = "1000000000_30000000"
            query_async_point_online.spatial.type = "point"
            asyncio.run(query_async_point_online.async_submit(query  = query_async_point_online,
                                                              client = c
                                                             )
                       )
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(query_async_point_online.id, "1000000000_30000000")
        self.assertEqual(query_async_point_online.status_response.status, "Succeeded(20)")
        self.assertEqual(query_async_point_online.download_status, "SUCCEEDED")
        self.assertEqual(query_async_point_online.submit_response.data, '1,2,3\na,b,c')
        
        self.logger.info('test_point_query_online_status_intransparent_batch: 200')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_point_online_status = None
        
        got_exception2 = False
        
        try:
            query_async_point_online_status = query.from_dict(query_dict)
            query_async_point_online_status.name         = "1000000000_30000000"
            query_async_point_online_status.spatial.type = "point"
            asyncio.run(query_async_point_online_status.async_submit_and_check_status(query  = query_async_point_online_status,
                                                                                      client = c
                                                                                     )
                       )
        except Exception as ex:
            got_exception2 = True
            
        self.assertFalse(got_exception2)
        self.assertEqual(query_async_point_online_status.id, "1000000000_30000000")
        self.assertEqual(query_async_point_online_status.status_response.status, "Succeeded(20)")
        self.assertEqual(query_async_point_online_status.download_status, "SUCCEEDED")
        self.assertEqual(query_async_point_online_status.submit_response.data, '1,2,3\na,b,c')
        
        # This test should trigger an 'online skip', see query.submit_response.
        self.logger.info('test_point_query_online_status_and_download_intransparent_batch + online skip: 200')
        
        c      = client.Client() 
        query  = query_module.Query
        
        query_async_point_online_status_and_download = None
        
        got_exception3 = False
        
        try:
            query_async_point_online_status_and_download = query.from_dict(query_dict)
            query_async_point_online_status_and_download.name         = "1000000000_30000000"
            query_async_point_online_status_and_download.spatial.type = "point"
            asyncio.run(query_async_point_online_status_and_download.async_submit_check_status_and_download(query  = query_async_point_online_status_and_download,
                                                                                                            client = c
                                                                                                           )
                       )
        except Exception as ex:
            got_exception3 = True
            
        self.assertFalse(got_exception3)
        self.assertEqual(query_async_point_online_status_and_download.id, "1000000000_30000000")
        self.assertEqual(query_async_point_online_status_and_download.status_response.status, "Succeeded(20)")
        self.assertEqual(query_async_point_online_status_and_download.download_status, "SUCCEEDED")
        self.assertEqual(query_async_point_online_status_and_download.submit_response.data, '1,2,3\na,b,c')
        
        
    
#
#class BatchQueryUnitTest(unittest.TestCase):
    
    #
#    def setUp(self):
#        self.logger = logger
#        self.logger.info('setup')
    
    #
#    def tearDown(self):
#        self.logger.info('teardown')
    
    #    
#    def test_batch_upload(self):


group_dict = {
    "id": 0,
    "name": "string"
}

group_json = r'''{
    "id": 0,
    "name": "string"
}'''

#
class GroupUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_group_init(self):
        self.logger.info('test_group_init')
        
        group = query_module.Group()
        
        got_exception = False
        
        try:
            group.id    = 0
            group.name  = "string"
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(group.id, 0)
        self.assertEqual(group.name, "string")

    #    
    def test_group_from_dict(self):
        self.logger.info('test_group_from_dict')
        
        group = query_module.Group

        group_from_dict = None
            
        got_exception = False

        try:
            group_from_dict = group.from_dict(group_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(group_from_dict.id, 0)
        self.assertEqual(group_from_dict.name, "string")
        
    #    
    def test_group_to_dict(self):
        self.logger.info('test_group_from_dict')
        
        group = query_module.Group

        group_from_dict = None
        group_to_dict   = None
                
        got_exception = False

        try:
            group_from_dict = group.from_dict(group_dict)
            group_to_dict   = group_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(group_to_dict, dict)
        self.assertEqual(group_to_dict["id"], 0)
        self.assertEqual(group_to_dict["name"], "string")

    #
    def test_group_from_json(self):
        self.logger.info('test_group_from_json')

        group = query_module.Group
        
        group_from_json = None

        got_exception = False

        try:
            group_from_json = group.from_json(group_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(group_from_json.id, 0)
        self.assertEqual(group_from_json.name, "string")
    
    #
    def test_group_to_json(self):
        self.logger.info('test_group_to_json')
        
        group = query_module.Group
        
        group_from_json = None
        group_to_json = None

        got_exception = False
        
        try:
            group_from_json = group.from_json(group_json)
            group_to_json = group_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

user_dict = {
    "id": "string",
    "login": "string",
    "group": 
        {
            "id": 0,
            "name": "string"
        },
    "email": "string",
    "company": "string",
    "admin": "string",
    "secondary_groups": [
        {
            "id": 0,
            "name": "string"
        }
    ]
}

user_json = r'''{
    "id": "string",
    "login": "string",
    "group": 
        {
            "id": 0,
            "name": "string"
        },
    "email": "string",
    "company": "string",
    "admin": "string",
    "secondary_groups": [
        {
            "id": 0,
            "name": "string"
        }
    ]
}'''

#
class UserUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_user_init(self):
        self.logger.info('test_user_init')
        
        user = query_module.User()
        
        got_exception = False
        
        try:
            user.id                = "string"
            user.login             = "string"
            group                  = query_module.Group()
            group.id               = 0
            group.name             = "string"
            user.group             = group
            user.email             = "string"
            user.company           = "string"
            user.admin             = "string"
            secondary_group        = query_module.Group()
            secondary_group.id     = 0
            secondary_group.name   = "string"
            user.secondary_groups  = [secondary_group]
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(user.id, "string")
        self.assertEqual(user.login, "string")
        self.assertEqual(user.group.id, 0)
        self.assertEqual(user.group.name, "string")
        self.assertEqual(user.email, "string")
        self.assertEqual(user.company, "string")
        self.assertEqual(user.admin, "string")
        self.assertEqual(user.secondary_groups[0].id, 0)
        self.assertEqual(user.secondary_groups[0].name, "string")

    #    
    def test_user_from_dict(self):
        self.logger.info('test_user_from_dict')
        
        user = query_module.User

        user_from_dict = None
            
        got_exception = False

        try:
            user_from_dict = user.from_dict(user_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(user_from_dict.id, "string")
        self.assertEqual(user_from_dict.login, "string")
        self.assertEqual(user_from_dict.group.id, 0)
        self.assertEqual(user_from_dict.group.name, "string")
        self.assertEqual(user_from_dict.email, "string")
        self.assertEqual(user_from_dict.company, "string")
        self.assertEqual(user_from_dict.admin, "string")
        self.assertEqual(user_from_dict.secondary_groups[0].id, 0)
        self.assertEqual(user_from_dict.secondary_groups[0].name, "string")
        
    #    
    def test_user_to_dict(self):
        self.logger.info('test_user_from_dict')
        
        user = query_module.User

        user_from_dict = None
        user_to_dict   = None
                
        got_exception = False

        #try:
        user_from_dict = user.from_dict(user_dict)
        user_to_dict   = user_from_dict.to_dict()
        #except Exception as ex:
        #    got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(user_to_dict, dict)
        self.assertEqual(user_to_dict["id"], "string")
        self.assertEqual(user_to_dict["login"], "string")
        self.assertEqual(user_to_dict["group"]["id"], 0)
        self.assertEqual(user_to_dict["group"]["name"], "string")
        self.assertEqual(user_to_dict["email"], "string")
        self.assertEqual(user_to_dict["company"], "string")
        self.assertEqual(user_to_dict["admin"], "string")
        self.assertEqual(user_to_dict["secondary_groups"][0]["id"], 0)
        self.assertEqual(user_to_dict["secondary_groups"][0]["name"], "string")

    #
    def test_user_from_json(self):
        self.logger.info('test_user_from_json')

        user = query_module.User
        
        user_from_json = None

        got_exception = False

        try:
            user_from_json = user.from_json(user_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(user_from_json.id, "string")
        self.assertEqual(user_from_json.login, "string")
        self.assertEqual(user_from_json.group.id, 0)
        self.assertEqual(user_from_json.group.name, "string")
        self.assertEqual(user_from_json.email, "string")
        self.assertEqual(user_from_json.company, "string")
        self.assertEqual(user_from_json.admin, "string")
        self.assertEqual(user_from_json.secondary_groups[0].id, 0)
        self.assertEqual(user_from_json.secondary_groups[0].name, "string")
    
    #
    def test_user_to_json(self):
        self.logger.info('test_user_to_json')
        
        user = query_module.User
        
        user_from_json = None
        user_to_json = None

        got_exception = False
        
        try:
            user_from_json = user.from_json(user_json)
            user_to_json = user_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)   

query_history_dict = {
    "id": 0,
    "user": 
        {
            "id": "string",
            "login": "string",
            "group": 
                {
                    "id": 0,
                    "name": "string"
                },
            "email": "string",
            "company": "string",
            "admin": "string",
            "secondary_groups": [
                {
                    "id": 0,
                    "name": "string"
                }
            ]
        },
    "type": "string",
    "date": "string",
    "query_job": "string",
    "api_json": "string",
    "sizeTotal": 0,
    "sizeRaw": 0,
    "sizeZip": 0,
    "countTotal": 0
}

query_history_json = r'''{
    "id": 0,
    "user": 
        {
            "id": "string",
            "login": "string",
            "group": 
                {
                    "id": 0,
                    "name": "string"
                },
            "email": "string",
            "company": "string",
            "admin": "string",
            "secondary_groups": [
                {
                    "id": 0,
                    "name": "string"
                }
            ]
        },
    "type": "string",
    "date": "string",
    "query_job": "string",
    "api_json": "string",
    "sizeTotal": 0,
    "sizeRaw": 0,
    "sizeZip": 0,
    "countTotal": 0
}'''

#
class QueryHistoryUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_query_history_init(self):
        self.logger.info('test_query_history_init')
        
        query_history = query_module.QueryHistory()
        
        got_exception = False
        
        try:
            query_history.id          = 0
            user                      = query_module.User()
            user.id                   = "string"
            user.login                = "string"
            group                     = query_module.Group()
            group.id                  = 0
            group.name                = "string"
            user.group                = group
            user.email                = "string"
            user.company              = "string"
            user.admin                = "string"
            secondary_group           = query_module.Group()
            secondary_group.id        = 0
            secondary_group.name      = "string"
            user.secondary_groups     = [secondary_group]
            query_history.user        = user
            query_history.type        = "string"
            query_history.date        = "string"
            query_history.query_job   = "string"
            query_history.api_json    = "string"
            query_history.size_total  = 0
            query_history.size_raw    = 0
            query_history.size_zip    = 0
            query_history.count_total = 0
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(query_history.id, 0)
        self.assertEqual(query_history.user.id, "string")
        self.assertEqual(query_history.user.login, "string")
        self.assertEqual(query_history.user.group.id, 0)
        self.assertEqual(query_history.user.group.name, "string")
        self.assertEqual(query_history.user.email, "string")
        self.assertEqual(query_history.user.company, "string")
        self.assertEqual(query_history.user.admin, "string")
        self.assertEqual(query_history.user.secondary_groups[0].id, 0)
        self.assertEqual(query_history.user.secondary_groups[0].name, "string")
        self.assertEqual(query_history.type, "string")
        self.assertEqual(query_history.date, "string")
        self.assertEqual(query_history.query_job, "string")
        self.assertEqual(query_history.api_json, "string")
        self.assertEqual(query_history.size_total, 0)
        self.assertEqual(query_history.size_raw, 0)
        self.assertEqual(query_history.size_zip, 0)
        self.assertEqual(query_history.count_total, 0)

    #    
    def test_query_history_from_dict(self):
        self.logger.info('test_query_history_from_dict')
        
        query_history = query_module.QueryHistory

        query_history_from_dict = None
            
        got_exception = False

        try:
            query_history_from_dict = query_history.from_dict(query_history_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_history_from_dict.id, 0)
        self.assertEqual(query_history_from_dict.user.id, "string")
        self.assertEqual(query_history_from_dict.user.login, "string")
        self.assertEqual(query_history_from_dict.user.group.id, 0)
        self.assertEqual(query_history_from_dict.user.group.name, "string")
        self.assertEqual(query_history_from_dict.user.email, "string")
        self.assertEqual(query_history_from_dict.user.company, "string")
        self.assertEqual(query_history_from_dict.user.admin, "string")
        self.assertEqual(query_history_from_dict.user.secondary_groups[0].id, 0)
        self.assertEqual(query_history_from_dict.user.secondary_groups[0].name, "string")
        self.assertEqual(query_history_from_dict.type, "string")
        self.assertEqual(query_history_from_dict.date, "string")
        self.assertEqual(query_history_from_dict.query_job, "string")
        self.assertEqual(query_history_from_dict.api_json, "string")
        self.assertEqual(query_history_from_dict.size_total, 0)
        self.assertEqual(query_history_from_dict.size_raw, 0)
        self.assertEqual(query_history_from_dict.size_zip, 0)
        self.assertEqual(query_history_from_dict.count_total, 0)
        
    #    
    def test_query_history_to_dict(self):
        self.logger.info('test_query_history_from_dict')
        
        query_history = query_module.QueryHistory

        query_history_from_dict = None
        query_history_to_dict   = None
                
        got_exception = False

        try:
            query_history_from_dict = query_history.from_dict(query_history_dict)
            query_history_to_dict   = query_history_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(query_history_to_dict, dict)
        self.assertEqual(query_history_to_dict["id"], 0)
        self.assertEqual(query_history_to_dict["user"]["id"], "string")
        self.assertEqual(query_history_to_dict["user"]["login"], "string")
        self.assertEqual(query_history_to_dict["user"]["group"]["id"], 0)
        self.assertEqual(query_history_to_dict["user"]["group"]["name"], "string")
        self.assertEqual(query_history_to_dict["user"]["email"], "string")
        self.assertEqual(query_history_to_dict["user"]["company"], "string")
        self.assertEqual(query_history_to_dict["user"]["admin"], "string")
        self.assertEqual(query_history_to_dict["user"]["secondary_groups"][0]["id"], 0)
        self.assertEqual(query_history_to_dict["user"]["secondary_groups"][0]["name"], "string")
        self.assertEqual(query_history_to_dict["type"], "string")
        self.assertEqual(query_history_to_dict["date"], "string")
        self.assertEqual(query_history_to_dict["query_job"], "string")
        self.assertEqual(query_history_to_dict["api_json"], "string")
        self.assertEqual(query_history_to_dict["size_total"], 0)
        self.assertEqual(query_history_to_dict["size_raw"], 0)
        self.assertEqual(query_history_to_dict["size_zip"], 0)
        self.assertEqual(query_history_to_dict["count_total"], 0)        

    #
    def test_query_history_from_json(self):
        self.logger.info('test_query_history_from_json')

        query_history = query_module.QueryHistory
        
        query_history_from_json = None

        got_exception = False

        try:
            query_history_from_json = query_history.from_json(query_history_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(query_history_from_json.id, 0)
        self.assertEqual(query_history_from_json.user.id, "string")
        self.assertEqual(query_history_from_json.user.login, "string")
        self.assertEqual(query_history_from_json.user.group.id, 0)
        self.assertEqual(query_history_from_json.user.group.name, "string")
        self.assertEqual(query_history_from_json.user.email, "string")
        self.assertEqual(query_history_from_json.user.company, "string")
        self.assertEqual(query_history_from_json.user.admin, "string")
        self.assertEqual(query_history_from_json.user.secondary_groups[0].id, 0)
        self.assertEqual(query_history_from_json.user.secondary_groups[0].name, "string")
        self.assertEqual(query_history_from_json.type, "string")
        self.assertEqual(query_history_from_json.date, "string")
        self.assertEqual(query_history_from_json.query_job, "string")
        self.assertEqual(query_history_from_json.api_json, "string")
        self.assertEqual(query_history_from_json.size_total, 0)
        self.assertEqual(query_history_from_json.size_raw, 0)
        self.assertEqual(query_history_from_json.size_zip, 0)
        self.assertEqual(query_history_from_json.count_total, 0)
    
    #
    def test_query_history_to_json(self):
        self.logger.info('test_query_history_to_json')
        
        query_history = query_module.QueryHistory
        
        query_history_from_json = None
        query_history_to_json = None

        got_exception = False
        
        try:
            query_history_from_json = query_history.from_json(query_history_json)
            query_history_to_json = query_history_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

latest_queries_dict = {
    "latest_queries": [
        {
            "description": "string",
            "layers": [
                {
                    "aggregation": "None",
                    "alias": "string",
                    "dimensions": [
                        {
                            "name": "string",
                            "operator": "EQ",
                            "options": [
                                "string"
                            ],
                            "value": "string"
                        }
                    ],
                    "expression": "string",
                    "filter": {
                        "operator": "EQ",
                        "value": "string"
                    },
                    "filterOnly": True,
                    "id": "string",
                    "output": True,
                    "temporal": {
                        "intervals": [
                            {
                                "end": "string",
                                "snapshot": "string",
                                "start": "string"
                            }
                        ]
                    },
                    "type": "raster"
                }
            ],
            "name": "string",
            "notification": {
                "host": "string",
                "queue": "string",
                "type": "rabbitmq"
            },
            "outputLevel": 0,
            "outputType": "json",
            "publish": True,
            "spatial": {
                "aggregation": {
                    "aoi": [
                        "string"
                    ]
                },
                "aoi": "string",
                "coordinates": [
                    0
                ],
                "type": "point"
            },
            "temporal": {
                "intervals": [
                    {
                        "end": "string",
                        "snapshot": "string",
                        "start": "string"
                    }
                ]
            },
            "upload": {
                "bucket": "string",
                "endpoint": "string",
                "provider": "ibm",
                "token": "string"
            }
        },
        {
            "description": "string2",
            "layers": [
                {
                    "aggregation": "None2",
                    "alias": "string2",
                    "dimensions": [
                        {
                            "name": "string2",
                            "operator": "EQ2",
                            "options": [
                                "string2"
                            ],
                            "value": "string2"
                        }
                    ],
                    "expression": "string2",
                    "filter": {
                        "operator": "EQ2",
                        "value": "string2"
                    },
                    "filterOnly": True,
                    "id": "string2",
                    "output": True,
                    "temporal": {
                        "intervals": [
                            {
                                "end": "string2",
                                "snapshot": "string2",
                                "start": "string2"
                            }
                        ]
                    },
                    "type": "raster2"
                }
            ],
            "name": "string2",
            "notification": {
                "host": "string2",
                "queue": "string2",
                "type": "rabbitmq2"
            },
            "outputLevel": 1,
            "outputType": "json2",
            "publish": True,
            "spatial": {
                "aggregation": {
                    "aoi": [
                        "string2"
                    ]
                },
                "aoi": "string2",
                "coordinates": [
                    1
                ],
                "type": "point2"
            },
            "temporal": {
                "intervals": [
                    {
                        "end": "string2",
                        "snapshot": "string2",
                        "start": "string2"
                    }
                ]
            },
            "upload": {
                "bucket": "string2",
                "endpoint": "string2",
                "provider": "ibm2",
                "token": "string2"
            }
        }
    ]
}

latest_queries_json = r'''{
    "latest_queries": [
        {
            "description": "string",
            "layers": [
                {
                    "aggregation": "None",
                    "alias": "string",
                    "dimensions": [
                        {
                            "name": "string",
                            "operator": "EQ",
                            "options": [
                                "string"
                            ],
                            "value": "string"
                        }
                    ],
                    "expression": "string",
                    "filter": {
                        "operator": "EQ",
                        "value": "string"
                    },
                    "filterOnly": true,
                    "id": "string",
                    "output": true,
                    "temporal": {
                        "intervals": [
                            {
                                "end": "string",
                                "snapshot": "string",
                                "start": "string"
                            }
                        ]
                    },
                    "type": "raster"
                }
            ],
            "name": "string",
            "notification": {
                "host": "string",
                "queue": "string",
                "type": "rabbitmq"
            },
            "outputLevel": 0,
            "outputType": "json",
            "publish": true,
            "spatial": {
                "aggregation": {
                    "aoi": [
                        "string"
                    ]
                },
                "aoi": "string",
                "coordinates": [
                    0
                ],
                "type": "point"
            },
            "temporal": {
                "intervals": [
                    {
                        "end": "string",
                        "snapshot": "string",
                        "start": "string"
                    }
                ]
            },
            "upload": {
                "bucket": "string",
                "endpoint": "string",
                "provider": "ibm",
                "token": "string"
            }
        },
        {
            "description": "string2",
            "layers": [
                {
                    "aggregation": "None2",
                    "alias": "string2",
                    "dimensions": [
                        {
                            "name": "string2",
                            "operator": "EQ2",
                            "options": [
                                "string2"
                            ],
                            "value": "string2"
                        }
                    ],
                    "expression": "string2",
                    "filter": {
                        "operator": "EQ2",
                        "value": "string2"
                    },
                    "filterOnly": true,
                    "id": "string2",
                    "output": true,
                    "temporal": {
                        "intervals": [
                            {
                                "end": "string2",
                                "snapshot": "string2",
                                "start": "string2"
                            }
                        ]
                    },
                    "type": "raster2"
                }
            ],
            "name": "string2",
            "notification": {
                "host": "string2",
                "queue": "string2",
                "type": "rabbitmq2"
            },
            "outputLevel": 1,
            "outputType": "json2",
            "publish": true,
            "spatial": {
                "aggregation": {
                    "aoi": [
                        "string2"
                    ]
                },
                "aoi": "string2",
                "coordinates": [
                    1
                ],
                "type": "point2"
            },
            "temporal": {
                "intervals": [
                    {
                        "end": "string2",
                        "snapshot": "string2",
                        "start": "string2"
                    }
                ]
            },
            "upload": {
                "bucket": "string2",
                "endpoint": "string2",
                "provider": "ibm2",
                "token": "string2"
            }
        }
    ]
}'''

#
class LatestQueriesUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
    
    #
    def test_latest_queries_init(self):
        self.logger.info('test_latest_queries_init')
        
        c      = client.Client() 
        latest_queries_object_1 = query_module.LatestQueries()
        
        got_exception = False
        
        try:
            query1                                 = query_module.Query()
            query1.name                            = "string"
            layer                                  = query_module.Layer()
            layer.id                               = "string"
            layer.type                             = "raster"
            temporal                               = query_module.Temporal()
            interval                               = query_module.Interval()
            interval.snapshot                      = "string"
            interval.end                           = "string"
            interval.start                         = "string"
            temporal.intervals                     = [interval]
            layer.temporal                         = temporal
            layer.alias                            = "string"
            layer.filter_only                      = True
            layer.aggregation                      = "None"
            filter_                                = query_module.Filter() 
            filter_.value                          = "string"
            filter_.operator                       = "EQ"
            layer.filter                           = filter_
            dimension                              = query_module.Dimension()
            dimension.name                         = "string"
            dimension.value                        = "string"
            dimension.operator                     = "EQ"
            dimension.options                      = ["string"]
            layer.dimensions                       = [dimension]
            layer.expression                       = "string"
            layer.output                           = True
            query1.layers                          = [layer]
            global_temporal                        = query_module.Temporal()
            global_interval                        = query_module.Interval()
            global_interval.snapshot               = "string"
            global_interval.end                    = "string"
            global_interval.start                  = "string"
            global_temporal.intervals              = [global_interval]
            query1.temporal                        = global_temporal
            spatial                                = query_module.Spatial()
            spatial.type                           = "point"
            spatial.aoi                            = "string"
            spatial.coordinates                    = [0]
            aggregation                            = query_module.Aggregation()
            aggregation.aoi                        = ["string"]
            spatial.aggregation                    = aggregation
            query1.spatial                         = spatial
            query1.output_type                     = "json"
            query1.output_level                    = 0
            query1.description                     = "string"
            query1.publish                         = True
            notification                           = query_module.Notification()
            notification.type                      = "rabbitmq"
            notification.host                      = "string"
            notification.queue                     = "string"
            query1.notification                    = notification
            upload                                 = query_module.Upload()
            upload.provider                        = "ibm"
            upload.endpoint                        = "string"
            upload.bucket                          = "string"
            upload.token                           = "string"
            query1.upload                          = upload
            query2                                 = query_module.Query()
            query2.name                            = "string2"
            layer2                                 = query_module.Layer()
            layer2.id                              = "string2"
            layer2.type                            = "raster2"
            temporal2                              = query_module.Temporal()
            interval2                              = query_module.Interval()
            interval2.snapshot                     = "string2"
            interval2.end                          = "string2"
            interval2.start                        = "string2"
            temporal2.intervals                    = [interval2]
            layer2.temporal                        = temporal2
            layer2.alias                           = "string2"
            layer2.filter_only                     = True
            layer2.aggregation                     = "None2"
            filter_2                               = query_module.Filter() 
            filter_2.value                         = "string2"
            filter_2.operator                      = "EQ2"
            layer2.filter                          = filter_2
            dimension2                             = query_module.Dimension()
            dimension2.name                        = "string2"
            dimension2.value                       = "string2"
            dimension2.operator                    = "EQ2"
            dimension2.options                     = ["string2"]
            layer2.dimensions                      = [dimension2]
            layer2.expression                      = "string2"
            layer2.output                          = True
            query2.layers                          = [layer2]
            global_temporal2                       = query_module.Temporal()
            global_interval2                       = query_module.Interval()
            global_interval2.snapshot              = "string2"
            global_interval2.end                   = "string2"
            global_interval2.start                 = "string2"
            global_temporal2.intervals             = [global_interval2]
            query2.temporal                        = global_temporal2
            spatial2                               = query_module.Spatial()
            spatial2.type                          = "point2"
            spatial2.aoi                           = "string2"
            spatial2.coordinates                  = [1]
            aggregation2                           = query_module.Aggregation()
            aggregation2.aoi                       = ["string2"]
            spatial2.aggregation                   = aggregation2
            query2.spatial                         = spatial2
            query2.output_type                     = "json2"
            query2.output_level                    = 1
            query2.description                     = "string2"
            query2.publish                         = True
            notification2                          = query_module.Notification()
            notification2.type                     = "rabbitmq2"
            notification2.host                     = "string2"
            notification2.queue                    = "string2"
            query2.notification                    = notification2
            upload2                                = query_module.Upload()
            upload2.provider                       = "ibm2"
            upload2.endpoint                       = "string2"
            upload2.bucket                         = "string2"
            upload2.token                          = "string2"
            query2.upload                          = upload2
            latest_queries_list                    = [query1, query2]
            latest_queries_object_1.latest_queries = latest_queries_list
        except Exception as ex:
            got_exception = True
        
        self.assertFalse(got_exception)
        self.assertEqual(latest_queries_object_1.latest_queries[0].name, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].id, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].type, "raster")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].alias, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].filter_only, True)
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].aggregation, "None")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].filter.value, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].filter.operator, "EQ")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].dimensions[0].name, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].dimensions[0].value, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].dimensions[0].options[0], "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].expression, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].layers[0].output, True)
        self.assertEqual(latest_queries_object_1.latest_queries[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].spatial.type, "point")
        self.assertEqual(latest_queries_object_1.latest_queries[0].spatial.aoi, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].spatial.coordinates[0], 0)
        self.assertEqual(latest_queries_object_1.latest_queries[0].spatial.aggregation.aoi[0], "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].output_type, "json")
        self.assertEqual(latest_queries_object_1.latest_queries[0].output_level, 0)
        self.assertEqual(latest_queries_object_1.latest_queries[0].description, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].publish, True)
        self.assertEqual(latest_queries_object_1.latest_queries[0].notification.type, "rabbitmq")
        self.assertEqual(latest_queries_object_1.latest_queries[0].notification.host, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].notification.queue, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].upload.provider, "ibm")
        self.assertEqual(latest_queries_object_1.latest_queries[0].upload.endpoint, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].upload.bucket, "string")
        self.assertEqual(latest_queries_object_1.latest_queries[0].upload.token, "string")
        
        self.assertEqual(latest_queries_object_1.latest_queries[1].name, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].id, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].type, "raster2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].alias, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].filter_only, True)
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].aggregation, "None2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].filter.value, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].filter.operator, "EQ2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].dimensions[0].name, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].dimensions[0].value, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].dimensions[0].operator, "EQ2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].dimensions[0].options[0], "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].expression, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].layers[0].output, True)
        self.assertEqual(latest_queries_object_1.latest_queries[1].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].spatial.type, "point2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].spatial.aoi, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].spatial.coordinates[0], 1)
        self.assertEqual(latest_queries_object_1.latest_queries[1].spatial.aggregation.aoi[0], "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].output_type, "json2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].output_level, 1)
        self.assertEqual(latest_queries_object_1.latest_queries[1].description, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].publish, True)
        self.assertEqual(latest_queries_object_1.latest_queries[1].notification.type, "rabbitmq2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].notification.host, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].notification.queue, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].upload.provider, "ibm2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].upload.endpoint, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].upload.bucket, "string2")
        self.assertEqual(latest_queries_object_1.latest_queries[1].upload.token, "string2")
        
        self.logger.info('test_latest_queries_from_dict: overload positional')
        
        self.assertEqual(latest_queries_object_1[0].name, "string")
        self.assertEqual(latest_queries_object_1[1].name, "string2")
        
        self.logger.info('test_latest_queries_from_dict: overload string')
        
        latest_queries_object_1["string"].id = "newstring"
        latest_queries_object_1["string2"].id = "newstring2"
        latest_queries_object_1["string"].name = "newstring"
        latest_queries_object_1["string2"].name = "newstring2"

    #    
    def test_latest_queries_from_dict(self):
        self.logger.info('test_latest_queries_from_dict')
        
        latest_queries = query_module.LatestQueries

        latest_queries_from_dict = None
            
        got_exception = False

        try:
            c      = client.Client()
            latest_queries_from_dict = latest_queries.from_dict(latest_queries_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].name, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].id, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].type, "raster")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].alias, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].filter_only, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].aggregation, "None")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].filter.value, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].filter.operator, "EQ")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].dimensions[0].name, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].dimensions[0].value, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].dimensions[0].options[0], "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].expression, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].layers[0].output, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].spatial.type, "point")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].spatial.aoi, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].spatial.coordinates[0], 0)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].spatial.aggregation.aoi[0], "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].output_type, "json")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].output_level, 0)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].description, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].publish, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[0].notification.type, "rabbitmq")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].notification.host, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].notification.queue, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].upload.provider, "ibm")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].upload.endpoint, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].upload.bucket, "string")
        self.assertEqual(latest_queries_from_dict.latest_queries[0].upload.token, "string")
        
        self.assertEqual(latest_queries_from_dict.latest_queries[1].name, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].id, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].type, "raster2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].alias, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].filter_only, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].aggregation, "None2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].filter.value, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].filter.operator, "EQ2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].dimensions[0].name, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].dimensions[0].value, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].dimensions[0].operator, "EQ2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].dimensions[0].options[0], "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].expression, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].layers[0].output, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[1].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].spatial.type, "point2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].spatial.aoi, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].spatial.coordinates[0], 1)
        self.assertEqual(latest_queries_from_dict.latest_queries[1].spatial.aggregation.aoi[0], "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].output_type, "json2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].output_level, 1)
        self.assertEqual(latest_queries_from_dict.latest_queries[1].description, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].publish, True)
        self.assertEqual(latest_queries_from_dict.latest_queries[1].notification.type, "rabbitmq2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].notification.host, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].notification.queue, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].upload.provider, "ibm2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].upload.endpoint, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].upload.bucket, "string2")
        self.assertEqual(latest_queries_from_dict.latest_queries[1].upload.token, "string2")

    #    
    def test_latest_queries_to_dict(self):
        self.logger.info('test_latest_queries_from_dict')
        
        latest_queries = query_module.LatestQueries

        latest_queries_from_dict = None
        latest_queries_to_dict   = None
                
        got_exception = False

        try:
            latest_queries_from_dict = latest_queries.from_dict(latest_queries_dict)
            latest_queries_to_dict   = latest_queries_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(latest_queries_to_dict, dict)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["name"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["id"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["type"], "raster")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["temporal"]['intervals'][0]["snapshot"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["temporal"]['intervals'][0]["end"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["temporal"]['intervals'][0]["start"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["alias"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["filter_only"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["aggregation"], "None")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["filter"]["value"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["filter"]["operator"], "EQ")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["dimensions"][0]["name"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["dimensions"][0]["value"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["dimensions"][0]["operator"], "EQ")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["dimensions"][0]["options"][0], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["expression"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["layers"][0]["output"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["temporal"]["intervals"][0]["snapshot"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["temporal"]["intervals"][0]["end"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["temporal"]["intervals"][0]["start"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["spatial"]["type"], "point")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["spatial"]["aoi"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["spatial"]["coordinates"][0], 0)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["spatial"]["aggregation"]["aoi"][0], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["output_type"], "json")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["output_level"], 0)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["description"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["publish"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["notification"]["type"], "rabbitmq")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["notification"]["host"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["notification"]["queue"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["upload"]["provider"], "ibm")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["upload"]["endpoint"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["upload"]["bucket"], "string")
        self.assertEqual(latest_queries_to_dict["latest_queries"][0]["upload"]["token"], "string")
        
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["name"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["id"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["type"], "raster2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["temporal"]['intervals'][0]["snapshot"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["temporal"]['intervals'][0]["end"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["temporal"]['intervals'][0]["start"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["alias"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["filter_only"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["aggregation"], "None2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["filter"]["value"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["filter"]["operator"], "EQ2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["dimensions"][0]["name"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["dimensions"][0]["value"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["dimensions"][0]["operator"], "EQ2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["dimensions"][0]["options"][0], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["expression"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["layers"][0]["output"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["temporal"]["intervals"][0]["snapshot"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["temporal"]["intervals"][0]["end"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["temporal"]["intervals"][0]["start"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["spatial"]["type"], "point2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["spatial"]["aoi"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["spatial"]["coordinates"][0], 1)
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["spatial"]["aggregation"]["aoi"][0], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["output_type"], "json2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["output_level"], 1)
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["description"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["publish"], True)
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["notification"]["type"], "rabbitmq2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["notification"]["host"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["notification"]["queue"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["upload"]["provider"], "ibm2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["upload"]["endpoint"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["upload"]["bucket"], "string2")
        self.assertEqual(latest_queries_to_dict["latest_queries"][1]["upload"]["token"], "string2")

    #
    def test_latest_queries_from_json(self):
        self.logger.info('test_latest_queries_from_json')

        latest_queries = query_module.LatestQueries
        
        latest_queries_from_json = None

        got_exception = False

        try:
            latest_queries_from_json = latest_queries.from_json(latest_queries_json)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(latest_queries_from_json.latest_queries[0].name, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].id, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].type, "raster")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].alias, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].filter_only, True)
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].aggregation, "None")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].filter.value, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].filter.operator, "EQ")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].dimensions[0].name, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].dimensions[0].value, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].dimensions[0].operator, "EQ")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].dimensions[0].options[0], "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].expression, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].layers[0].output, True)
        self.assertEqual(latest_queries_from_json.latest_queries[0].temporal.intervals[0].snapshot, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].temporal.intervals[0].end, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].temporal.intervals[0].start, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].spatial.type, "point")
        self.assertEqual(latest_queries_from_json.latest_queries[0].spatial.aoi, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].spatial.coordinates[0], 0)
        self.assertEqual(latest_queries_from_json.latest_queries[0].spatial.aggregation.aoi[0], "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].output_type, "json")
        self.assertEqual(latest_queries_from_json.latest_queries[0].output_level, 0)
        self.assertEqual(latest_queries_from_json.latest_queries[0].description, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].publish, True)
        self.assertEqual(latest_queries_from_json.latest_queries[0].notification.type, "rabbitmq")
        self.assertEqual(latest_queries_from_json.latest_queries[0].notification.host, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].notification.queue, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].upload.provider, "ibm")
        self.assertEqual(latest_queries_from_json.latest_queries[0].upload.endpoint, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].upload.bucket, "string")
        self.assertEqual(latest_queries_from_json.latest_queries[0].upload.token, "string")
        
        self.assertEqual(latest_queries_from_json.latest_queries[1].name, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].id, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].type, "raster2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].alias, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].filter_only, True)
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].aggregation, "None2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].filter.value, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].filter.operator, "EQ2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].dimensions[0].name, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].dimensions[0].value, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].dimensions[0].operator, "EQ2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].dimensions[0].options[0], "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].expression, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].layers[0].output, True)
        self.assertEqual(latest_queries_from_json.latest_queries[1].temporal.intervals[0].snapshot, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].temporal.intervals[0].end, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].temporal.intervals[0].start, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].spatial.type, "point2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].spatial.aoi, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].spatial.coordinates[0], 1)
        self.assertEqual(latest_queries_from_json.latest_queries[1].spatial.aggregation.aoi[0], "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].output_type, "json2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].output_level, 1)
        self.assertEqual(latest_queries_from_json.latest_queries[1].description, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].publish, True)
        self.assertEqual(latest_queries_from_json.latest_queries[1].notification.type, "rabbitmq2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].notification.host, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].notification.queue, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].upload.provider, "ibm2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].upload.endpoint, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].upload.bucket, "string2")
        self.assertEqual(latest_queries_from_json.latest_queries[1].upload.token, "string2")
    
    #
    def test_latest_queries_to_json(self):
        self.logger.info('test_latest_queries_to_json')
        
        latest_queries = query_module.LatestQueries
        
        latest_queries_from_json = None
        latest_queries_to_json = None

        got_exception = False
        
        try:
            latest_queries_from_json = latest_queries.from_json(latest_queries_json)
            latest_queries_to_json = latest_queries_from_json.to_json()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)






#TODO: ?
#class QueryOutputInfoFileUnitTest(unittest.TestCase):
    
#TODO: ?
#class QueryJobLayersUnitTest(unittest.TestCase):