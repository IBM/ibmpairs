"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2021 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# fold: Import Python Standard Library {{{
# Python Standard Library:
import json
import os
os.environ['UPLOAD_MIN_STATUS_INTERVAL'] = '1'
os.environ['UPLOAD_STATUS_CHECK_INTERVAL'] = '2'
#}}}
# fold: Import ibmpairs Modules {{{
# ibmpairs Modules:
from ibmpairs.logger import logger
import ibmpairs.client as client
import ibmpairs.external.ibm as ibm_cos
import ibmpairs.upload as upload_module
#}}}
# fold: Import Third Party Libraries {{{
# Third Party Libraries:
import responses
import unittest
from unittest import mock
import asyncio
#}}}

#
upload_dict_submit_1 = {
"datalayer_id": [1,2,3],
"hdftype":["HDF4_EOS:EOS_GRID"],
"hdfbandname":["layer_1", "layer_2", "layer_3"],
"timestamp": "1",
"filetype": "hdf", 
"pairsdatatype": "raster"
}

#
upload_dict_submit_2 = {
"datalayer_id": [1,2,3],
"hdftype":["HDF4_EOS:EOS_GRID"],
"hdfbandname":["layer_1", "layer_2", "layer_3"],
"timestamp": "2",
"filetype": "hdf", 
"pairsdatatype": "raster"
}

#
upload_dict_submit_3 = {
"datalayer_id": [1,2,3],
"hdftype":["HDF4_EOS:EOS_GRID"],
"hdfbandname":["layer_1", "layer_2", "layer_3"],
"timestamp": "3",
"filetype": "hdf", 
"pairsdatatype": "raster"
}

# 
def mocked_submit_get_presigned_url(*args, **kwargs):

    if kwargs.get("key") is not None:
        key = kwargs["key"]

    region = "thisisnotaregion"
    bucket = "thisisnotabucket"
    credential = "thisisnotacredential"
    signature = "thisisnotasignature"

    return "https://s3."+region+".cloud-object-storage.appdomain.cloud/"+bucket+"/"+key+"?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential="+credential+"%2F19700101%2F"+region+"-1%2Fs3%2Faws4_request&X-Amz-Date=19700101T000000Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=" + signature
        
#
def mocked_submit_get_metadata(*args, **kwargs):
    
    if kwargs.get("storage_key") is not None:
        storage_key = kwargs["storage_key"]
        
    if (storage_key == 'file1.hdf'):        
        return upload_dict_submit_1
    elif (storage_key == 'file2.hdf'):        
        return upload_dict_submit_2
    else: 
        return upload_dict_submit_3
        
#
async def mocked_submit_async_post(*args, **kwargs):

    timestamp = None
    
    if kwargs.get("body") is not None:

        input_data_dict = kwargs["body"]
        
        if input_data_dict.get("timestamp") is not None:
            timestamp = input_data_dict["timestamp"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.body   = json_data
            self.status = status_code

        def json(self):
            return self.body
            
    if (timestamp == '1'):        
        return_dict = {}
        return_dict["id"]  = "thisisnotanid"
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 201)
    elif (timestamp == '2'):
        return_dict = {}
        return_dict["message"]  = "Error: 404 Not Found."
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 404)
    else:
        return_dict = {}
        return_dict["message"]  = "Error: 401 Unauthorized."
        return_json = json.dumps(return_dict)
            
        return MockResponse(return_json, 401)

#
def mocked_submit_delete(*args, **kwargs):
    return True

#
def mocked_submit_upload(*args, **kwargs):
    return True

#
def mocked_submit_check_local_file(*args, **kwargs):
    return True
    
#
upload_status_response_dict_1 = {
    "status": "INITIALIZING",
    "last_updated": "1970-01-01 00:00:00+00:00",
    "summary": [
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        },
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        }
    ],
    "tracking_id": "1",
    "progress": 34,
    "user_tag": "1"
}

#
upload_status_response_dict_2 = {
    "status": "PROCESSING",
    "last_updated": "1970-01-01 00:00:00+00:00",
    "summary": [
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        },
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        }
    ],
    "tracking_id": "1",
    "progress": 34,
    "user_tag": "2"
}

#
upload_status_response_dict_3 = {
    "status": "SUCCEEDED",
    "last_updated": "1970-01-01 00:00:00+00:00",
    "summary": [
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        },
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        }
    ],
    "tracking_id": "1",
    "progress": 34,
    "user_tag": "3"
}

#
upload_status_response_dict_4 = {
    "status": "SUCCEEDED",
    "last_updated": "1970-01-01 00:00:00+00:00",
    "summary": [
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        },
        {
            "status": -1,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Failed",
            "raw_filename": "file1.hdf"
        }
    ],
    "tracking_id": "1",
    "progress": 34,
    "user_tag": "4"
}

#
upload_status_response_dict_5 = {
    "status": "FAILED",
    "last_updated": "1970-01-01 00:00:00+00:00",
    "summary": [
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        },
        {
            "status": 2.24,
            "last_updated": "1970-01-01 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "file1.hdf"
        }
    ],
    "tracking_id": "1",
    "progress": 34,
    "user_tag": "5"
}

poll_tracker = 0

async def mocked_status_async_get(*args, **kwargs):
    
    global poll_tracker
    
    print(kwargs)
    
    url = None
    
    if kwargs.get("url") is not None:
        url = kwargs["url"]
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.body   = json_data
            self.status = status_code

        def json(self):
            return self.body
            
    if (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/1'): 
        return_dict = {}
        return_dict["message"]  = "Error: 404 Not Found." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/2'): 
        return_dict = {}
        return_dict["message"]  = "Error: 503 Service Unavailable." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 503)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/3'):
        return_json = json.dumps(upload_status_response_dict_3)
        
        print(MockResponse(return_json, 200))
        
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/4'): 
        return_json = json.dumps(upload_status_response_dict_4)
                           
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/5'):
        return_json = json.dumps(upload_status_response_dict_5)
                            
        return MockResponse(return_json, 200)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/6'): 
        return_dict = {}
        return_dict["message"]  = "Error: 401 Unauthorized." 
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 401)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/7'): 

        return_dict = {}

        if poll_tracker == 0:
            return_json = json.dumps(upload_status_response_dict_1)
            poll_tracker = poll_tracker + 1
            return MockResponse(return_json, 200)
        elif poll_tracker == 1:
            return_json = json.dumps(upload_status_response_dict_2)
            poll_tracker = poll_tracker + 1
            return MockResponse(return_json, 200)
        elif poll_tracker == 2:
            return_json = json.dumps(upload_status_response_dict_3)
            return MockResponse(return_json, 200)
        else:
            return_dict["message"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    elif (url == 'https://api.ibm.com/geospatial/run/na/core/v3/uploader/upload/8'): 

        return_dict = {}

        if poll_tracker == 0:
            return_json = json.dumps(upload_status_response_dict_1)
            poll_tracker = poll_tracker + 1
            return MockResponse(return_json, 200)
        elif poll_tracker == 1:
            return_json = json.dumps(upload_status_response_dict_2)
            poll_tracker = poll_tracker + 1
            return MockResponse(return_json, 200)
        elif poll_tracker == 2:
            return_json = json.dumps(upload_status_response_dict_5)
            return MockResponse(return_json, 200)
        else:
            return_dict["message"]  = "Error: 404 Not Found." 
            return_json = json.dumps(return_dict)
            
            return MockResponse(return_json, 404)
    else:
        return_dict = {}
        return_dict["message"]  = "pass"
        return_json = json.dumps(return_dict)
        
        return MockResponse(return_json, 200)

#
pdal_preprocessing_json_dict = {
    "type": "filters.range",
    "limits": "Classification![7:7]"
}

#
pdal_preprocessing_json_str = r'''
{
    "type": "filters.range",
    "limits": "Classification![7:7]"
}'''

#
class PdalPreprocessingJSONUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')

    #    
    def test_pdal_preprocessing_json_from_dict(self):
        
        self.logger.info('test_pdal_preprocessing_json_from_dict')
        
        pdal_preprocessing_json = upload_module.PdalPreprocessingJSON

        pdal_preprocessing_json_from_dict = None
            
        got_exception = False

        try:
            pdal_preprocessing_json_from_dict = pdal_preprocessing_json.from_dict(pdal_preprocessing_json_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(pdal_preprocessing_json_from_dict.type, "filters.range")
        self.assertEqual(pdal_preprocessing_json_from_dict.limits, "Classification![7:7]")
        
    #    
    def test_pdal_preprocessing_json_to_dict(self):
        
        self.logger.info('test_pdal_preprocessing_json_to_dict')
        
        pdal_preprocessing_json = upload_module.PdalPreprocessingJSON

        pdal_preprocessing_json_from_dict = None
        pdal_preprocessing_json_to_dict   = None
                
        got_exception = False

        try:
            pdal_preprocessing_json_from_dict = pdal_preprocessing_json.from_dict(pdal_preprocessing_json_dict)
            pdal_preprocessing_json_to_dict = pdal_preprocessing_json_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(pdal_preprocessing_json_to_dict, dict)
        self.assertEqual(pdal_preprocessing_json_to_dict["type"], "filters.range")
        self.assertEqual(pdal_preprocessing_json_to_dict["limits"], "Classification![7:7]")
        
    #
    def test_pdal_preprocessing_json_from_json(self):
        
        self.logger.info('test_pdal_preprocessing_json_from_json')

        got_exception = False

        try:
            pdal_preprocessing_json_from_json = upload_module.pdal_preprocessing_json_from_json(pdal_preprocessing_json_str)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(pdal_preprocessing_json_from_json.type, "filters.range")
        self.assertEqual(pdal_preprocessing_json_from_json.limits, "Classification![7:7]")
 
    #
    def test_pdal_preprocessing_json_to_json(self):
        
        self.logger.info('test_pdal_preprocessing_json_to_json')

        got_exception = False
        
        try:
            pdal_preprocessing_json_from_json = upload_module.pdal_preprocessing_json_from_json(pdal_preprocessing_json_str)
            pdal_preprocessing_json_to_json = upload_module.pdal_preprocessing_json_to_json(pdal_preprocessing_json_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

#
options_dict = {
    "data-layers": [
        "dtm",
        "dsm",
        "chm"
    ],
    "n-pix-global-scale": 30,
    "pdal-preprocessing-jsons": [
        {
            "type": "filters.range",
            "limits": "Classification![7:7]"
        }
    ],
    "raster-params": [
        1.4,
        3.0
    ]
}

#
options_str = r'''
{
    "data-layers": [
        "dtm",
        "dsm",
        "chm"
    ],
    "n-pix-global-scale": 30,
    "pdal-preprocessing-jsons": [
        {
            "type": "filters.range",
            "limits": "Classification![7:7]"
        }
    ],
    "raster-params": [
        1.4,
        3.0
    ]
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
    def test_options_from_dict(self):
        
        self.logger.info('test_options_from_dict')
        
        options = upload_module.Options

        options_from_dict = None
                
        got_exception = False

        try:
            options_from_dict = options.from_dict(options_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(options_from_dict.data_layers[0], "dtm")
        self.assertEqual(options_from_dict.data_layers[1], "dsm")
        self.assertEqual(options_from_dict.data_layers[2], "chm")
        self.assertEqual(options_from_dict.n_pix_global_scale, 30)
        self.assertEqual(options_from_dict.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(options_from_dict.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(options_from_dict.raster_params[0], 1.4)
        self.assertEqual(options_from_dict.raster_params[1], 3.0)
        
    #    
    def test_options_to_dict(self):
        
        self.logger.info('test_options_to_dict')
        
        options = upload_module.Options

        options_from_dict = None
        options_to_dict   = None
                
        got_exception = False

        try:
            options_from_dict = options.from_dict(options_dict)
            options_to_dict = options_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(options_to_dict, dict)
        self.assertEqual(options_to_dict["data_layers"][0], "dtm")
        self.assertEqual(options_to_dict["data_layers"][1], "dsm")
        self.assertEqual(options_to_dict["data_layers"][2], "chm")
        self.assertEqual(options_to_dict["n_pix_global_scale"], 30)
        self.assertEqual(options_to_dict["pdal_preprocessing_jsons"][0]["type"], "filters.range")
        self.assertEqual(options_to_dict["pdal_preprocessing_jsons"][0]["limits"], "Classification![7:7]")
        self.assertEqual(options_to_dict["raster_params"][0], 1.4)
        self.assertEqual(options_to_dict["raster_params"][1], 3.0)
        
    #
    def test_options_from_json(self):
        
        self.logger.info('test_options_from_json')

        got_exception = False

        try:
            options_from_json = upload_module.options_from_json(options_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(options_from_json.data_layers[0], "dtm")
        self.assertEqual(options_from_json.data_layers[1], "dsm")
        self.assertEqual(options_from_json.data_layers[2], "chm")
        self.assertEqual(options_from_json.n_pix_global_scale, 30)
        self.assertEqual(options_from_json.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(options_from_json.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(options_from_json.raster_params[0], 1.4)
        self.assertEqual(options_from_json.raster_params[1], 3.0)
 
    #
    def test_options_to_json(self):
        
        self.logger.info('test_options_to_json')

        got_exception = False
        
        try:
            options_from_json = upload_module.options_from_json(options_str)
            options_to_json = upload_module.options_to_json(options_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

#
preprocessing_dict = {
    "type": "lidar-rasterize",
    "order": 4,
    "options": {
        "data-layers": [
            "dtm",
            "dsm",
            "chm"
        ],
        "n-pix-global-scale": 30,
        "pdal-preprocessing-jsons": [
            {
                "type": "filters.range",
                "limits": "Classification![7:7]"
            }
        ],
        "raster-params": [
            1.4,
            3.0
        ]
    }
}

#
preprocessing_str = r'''{
    "type": "lidar-rasterize",
    "order": 4,
    "options": {
        "data-layers": [
            "dtm",
            "dsm",
            "chm"
        ],
        "n-pix-global-scale": 30,
        "pdal-preprocessing-jsons": [
            {
                "type": "filters.range",
                "limits": "Classification![7:7]"
            }
        ],
        "raster-params": [
            1.4,
            3.0
        ]
    }
}'''
        
#
class PreprocessingUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
        
    #    
    def test_preprocessing_from_dict(self):
        
        self.logger.info('test_preprocessing_from_dict')
        
        preprocessing = upload_module.Preprocessing

        preprocessing_from_dict = None
                
        got_exception = False

        try:
            preprocessing_from_dict = preprocessing.from_dict(preprocessing_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(preprocessing_from_dict.type, "lidar-rasterize")
        self.assertEqual(preprocessing_from_dict.order, 4)
        self.assertEqual(preprocessing_from_dict.options.data_layers[0], "dtm")
        self.assertEqual(preprocessing_from_dict.options.data_layers[1], "dsm")
        self.assertEqual(preprocessing_from_dict.options.data_layers[2], "chm")
        self.assertEqual(preprocessing_from_dict.options.n_pix_global_scale, 30)
        self.assertEqual(preprocessing_from_dict.options.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(preprocessing_from_dict.options.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(preprocessing_from_dict.options.raster_params[0], 1.4)
        self.assertEqual(preprocessing_from_dict.options.raster_params[1], 3.0)
        
    #    
    def test_preprocessing_to_dict(self):
        
        self.logger.info('test_preprocessing_to_dict')
        
        preprocessing = upload_module.Preprocessing

        preprocessing_from_dict = None
        preprocessing_to_dict   = None
                
        got_exception = False

        try:
            preprocessing_from_dict = preprocessing.from_dict(preprocessing_dict)
            preprocessing_to_dict = preprocessing_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(preprocessing_to_dict, dict)
        self.assertEqual(preprocessing_to_dict["type"], "lidar-rasterize")
        self.assertEqual(preprocessing_to_dict["order"], 4)
        self.assertEqual(preprocessing_to_dict["options"]["data_layers"][0], "dtm")
        self.assertEqual(preprocessing_to_dict["options"]["data_layers"][1], "dsm")
        self.assertEqual(preprocessing_to_dict["options"]["data_layers"][2], "chm")
        self.assertEqual(preprocessing_to_dict["options"]["n_pix_global_scale"], 30)
        self.assertEqual(preprocessing_to_dict["options"]["pdal_preprocessing_jsons"][0]["type"], "filters.range")
        self.assertEqual(preprocessing_to_dict["options"]["pdal_preprocessing_jsons"][0]["limits"], "Classification![7:7]")
        self.assertEqual(preprocessing_to_dict["options"]["raster_params"][0], 1.4)
        self.assertEqual(preprocessing_to_dict["options"]["raster_params"][1], 3.0)
        
    #
    def test_preprocessing_from_json(self):
        
        self.logger.info('test_preprocessing_from_json')

        got_exception = False

        try:
            preprocessing_from_json = upload_module.preprocessing_from_json(preprocessing_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
        self.assertEqual(preprocessing_from_json.type, "lidar-rasterize")
        self.assertEqual(preprocessing_from_json.order, 4)
        self.assertEqual(preprocessing_from_json.options.data_layers[0], "dtm")
        self.assertEqual(preprocessing_from_json.options.data_layers[1], "dsm")
        self.assertEqual(preprocessing_from_json.options.data_layers[2], "chm")
        self.assertEqual(preprocessing_from_json.options.n_pix_global_scale, 30)
        self.assertEqual(preprocessing_from_json.options.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(preprocessing_from_json.options.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(preprocessing_from_json.options.raster_params[0], 1.4)
        self.assertEqual(preprocessing_from_json.options.raster_params[1], 3.0)
 
    #
    def test_preprocessing_to_json(self):
        
        self.logger.info('test_preprocessing_to_json')

        got_exception = False
        
        try:
            preprocessing_from_json = upload_module.preprocessing_from_json(preprocessing_str)
            preprocessing_to_json = upload_module.preprocessing_to_json(preprocessing_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

#
conv_params_dict_dict = {
    "lin-conv-offset": -30.2,
    "lin-conv-slope": 1.2,
    "non-lin-param2": 5.5,
    "non-lin-param1": 4.2
}

#
conv_params_dict_str = r'''{
    "lin-conv-offset": -30.2,
    "lin-conv-slope": 1.2,
    "non-lin-param2": 5.5,
    "non-lin-param1": 4.2
}'''
        
#
class ConvParamsDictUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
        
    #    
    def test_conv_params_dict_from_dict(self):
        
        self.logger.info('test_conv_params_dict_from_dict')
        
        conv_params_dict = upload_module.ConvParamsDict

        conv_params_dict_from_dict = None
            
        got_exception = False

        try:
            conv_params_dict_from_dict = conv_params_dict.from_dict(conv_params_dict_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(conv_params_dict_from_dict.lin_conv_offset, -30.2)
        self.assertEqual(conv_params_dict_from_dict.lin_conv_slope, 1.2)
        self.assertEqual(conv_params_dict_from_dict.non_lin_param2, 5.5)
        self.assertEqual(conv_params_dict_from_dict.non_lin_param1, 4.2)
        
    #    
    def test_conv_params_dict_to_dict(self):
        
        self.logger.info('test_conv_params_dict_to_dict')
        
        conv_params_dict = upload_module.ConvParamsDict

        conv_params_dict_from_dict = None
        conv_params_dict_to_dict   = None
                
        got_exception = False

        try:
            conv_params_dict_from_dict = conv_params_dict.from_dict(conv_params_dict_dict)
            conv_params_dict_to_dict = conv_params_dict_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(conv_params_dict_to_dict, dict)
        self.assertEqual(conv_params_dict_to_dict["lin_conv_offset"], -30.2)
        self.assertEqual(conv_params_dict_to_dict["lin_conv_slope"], 1.2)
        self.assertEqual(conv_params_dict_to_dict["non_lin_param2"], 5.5)
        self.assertEqual(conv_params_dict_to_dict["non_lin_param1"], 4.2)
        
    #
    def test_conv_params_dict_from_json(self):
        
        self.logger.info('test_conv_params_dict_from_json')

        got_exception = False

        try:
            conv_params_dict_from_json = upload_module.conv_params_dict_from_json(conv_params_dict_str)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(conv_params_dict_from_json.lin_conv_offset, -30.2)
        self.assertEqual(conv_params_dict_from_json.lin_conv_slope, 1.2)
        self.assertEqual(conv_params_dict_from_json.non_lin_param2, 5.5)
        self.assertEqual(conv_params_dict_from_json.non_lin_param1, 4.2)
 
    #
    def test_conv_params_dict_to_json(self):
        
        self.logger.info('test_conv_params_dict_to_json')

        got_exception = False
        
        try:
            conv_params_dict_from_json = upload_module.conv_params_dict_from_json(conv_params_dict_str)
            conv_params_dict_to_json = upload_module.conv_params_dict_to_json(conv_params_dict_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        
#
summary_dict = {
    "status": "2.24",
    "last_updated": "2019-08-08 00:00:00+00:00",
    "details": "Success",
    "raw_filename": "22334521-22ddasfggas.tif"
}

#
summary_str = r'''{
    "status": "2.24",
    "last_updated": "2019-08-08 00:00:00+00:00",
    "details": "Success",
    "raw_filename": "22334521-22ddasfggas.tif"
}'''

#
class SummaryUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
        
    #    
    def test_summary_from_dict(self):
        
        self.logger.info('test_summary_from_dict')
        
        summary = upload_module.Summary

        summary_from_dict = None
            
        got_exception = False

        try:
            summary_from_dict = summary.from_dict(summary_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(summary_from_dict.status, 2.24)
        self.assertEqual(summary_from_dict.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(summary_from_dict.details, "Success")
        self.assertEqual(summary_from_dict.raw_filename, "22334521-22ddasfggas.tif")
        
    #    
    def test_summary_to_dict(self):
        
        self.logger.info('test_summary_to_dict')
        
        summary = upload_module.Summary

        summary_from_dict = None
        summary_to_dict   = None
                
        got_exception = False

        try:
            summary_from_dict = summary.from_dict(summary_dict)
            summary_to_dict = summary_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(summary_to_dict, dict)
        self.assertEqual(summary_to_dict["status"], 2.24)
        self.assertEqual(summary_to_dict["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(summary_to_dict["details"], "Success")
        self.assertEqual(summary_to_dict["raw_filename"], "22334521-22ddasfggas.tif")
        
    #
    def test_summary_from_json(self):
        
        self.logger.info('test_summary_from_json')

        got_exception = False

        try:
            summary_from_json = upload_module.summary_from_json(summary_str)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(summary_from_json.status, 2.24)
        self.assertEqual(summary_from_json.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(summary_from_json.details, "Success")
        self.assertEqual(summary_from_json.raw_filename, "22334521-22ddasfggas.tif")
 
    #
    def test_summary_to_json(self):
        
        self.logger.info('test_summary_to_json')

        got_exception = False
        
        try:
            summary_from_json = upload_module.summary_from_json(summary_str)
            summary_to_json = upload_module.summary_to_json(summary_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

#
upload_status_response_dict = {
    "status": "INITIALIZING",
    "last_updated": "2019-08-08 00:00:00+00:00",
    "summary": [
        {
            "status": "2.24",
            "last_updated": "2019-08-08 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "22334521-22ddasfggas.tif"
        },
        {
            "status": "-1",
            "last_updated": "2019-08-08 00:00:00+00:00",
            "details": "Failed",
            "raw_filename": "11223410-11cczreffzr.tif"
        }
    ],
    "tracking_id": "oiie8deehw88wwjslsdoifuhe43",
    "progress": "34",
    "user_tag": "myTagForLatestUploadOn2019-08-06"
}

#
upload_status_response_str = r'''{
    "status": "INITIALIZING",
    "last_updated": "2019-08-08 00:00:00+00:00",
    "summary": [
        {
            "status": "2.24",
            "last_updated": "2019-08-08 00:00:00+00:00",
            "details": "Success",
            "raw_filename": "22334521-22ddasfggas.tif"
        },
        {
            "status": "-1",
            "last_updated": "2019-08-08 00:00:00+00:00",
            "details": "Failed",
            "raw_filename": "11223410-11cczreffzr.tif"
        }
    ],
    "tracking_id": "oiie8deehw88wwjslsdoifuhe43",
    "progress": "34",
    "user_tag": "myTagForLatestUploadOn2019-08-06"
}'''

#
class UploadStatusResponseUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')
        
    #    
    def test_upload_status_response_from_dict(self):
        
        self.logger.info('test_upload_status_response_from_dict')
        
        upload_status_response = upload_module.UploadStatusResponse

        upload_status_response_from_dict = None
                
        got_exception = False

        try:
            upload_status_response_from_dict = upload_status_response.from_dict(upload_status_response_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(upload_status_response_from_dict.status, "INITIALIZING")
        self.assertEqual(upload_status_response_from_dict.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_dict.summary[0].status, 2.24)
        self.assertEqual(upload_status_response_from_dict.summary[0].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_dict.summary[0].details, "Success")
        self.assertEqual(upload_status_response_from_dict.summary[0].raw_filename, "22334521-22ddasfggas.tif")
        self.assertEqual(upload_status_response_from_dict.summary[1].status, -1.0)
        self.assertEqual(upload_status_response_from_dict.summary[1].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_dict.summary[1].details, "Failed")
        self.assertEqual(upload_status_response_from_dict.summary[1].raw_filename, "11223410-11cczreffzr.tif")
        self.assertEqual(upload_status_response_from_dict.tracking_id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_status_response_from_dict.progress, 34)
        self.assertEqual(upload_status_response_from_dict.user_tag, "myTagForLatestUploadOn2019-08-06")
        
    #    
    def test_upload_status_response_to_dict(self):
        
        self.logger.info('test_upload_status_response_to_dict')
        
        upload_status_response = upload_module.UploadStatusResponse

        upload_status_response_from_dict = None
        upload_status_response_to_dict   = None
                
        got_exception = False

        try:
            upload_status_response_from_dict = upload_status_response.from_dict(upload_status_response_dict)
            upload_status_response_to_dict = upload_status_response_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(upload_status_response_to_dict, dict)
        self.assertEqual(upload_status_response_to_dict["status"], "INITIALIZING")
        self.assertEqual(upload_status_response_to_dict["last_updated"], "2019-08-08 00:00:00+00:00")
        
        self.assertEqual(upload_status_response_to_dict["status"], "INITIALIZING")
        self.assertEqual(upload_status_response_to_dict["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_to_dict["summary"][0]["status"], 2.24)
        self.assertEqual(upload_status_response_to_dict["summary"][0]["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_to_dict["summary"][0]["details"], "Success")
        self.assertEqual(upload_status_response_to_dict["summary"][0]["raw_filename"], "22334521-22ddasfggas.tif")
        self.assertEqual(upload_status_response_to_dict["summary"][1]["status"], -1.0)
        self.assertEqual(upload_status_response_to_dict["summary"][1]["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_to_dict["summary"][1]["details"], "Failed")
        self.assertEqual(upload_status_response_to_dict["summary"][1]["raw_filename"], "11223410-11cczreffzr.tif")
        
        self.assertEqual(upload_status_response_to_dict["tracking_id"], "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_status_response_to_dict["progress"], 34)
        self.assertEqual(upload_status_response_to_dict["user_tag"], "myTagForLatestUploadOn2019-08-06")
        
    #
    def test_upload_status_response_from_json(self):
        
        self.logger.info('test_upload_status_response_from_json')

        got_exception = False

        try:
            upload_status_response_from_json = upload_module.upload_status_response_from_json(upload_status_response_str)
        except Exception as ex:
            got_exception = True
            
        self.assertFalse(got_exception)
        self.assertEqual(upload_status_response_from_json.status, "INITIALIZING")
        self.assertEqual(upload_status_response_from_json.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_json.summary[0].status, 2.24)
        self.assertEqual(upload_status_response_from_json.summary[0].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_json.summary[0].details, "Success")
        self.assertEqual(upload_status_response_from_json.summary[0].raw_filename, "22334521-22ddasfggas.tif")
        self.assertEqual(upload_status_response_from_json.summary[1].status, -1.0)
        self.assertEqual(upload_status_response_from_json.summary[1].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_status_response_from_json.summary[1].details, "Failed")
        self.assertEqual(upload_status_response_from_json.summary[1].raw_filename, "11223410-11cczreffzr.tif")
        self.assertEqual(upload_status_response_from_json.tracking_id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_status_response_from_json.progress, 34)
        self.assertEqual(upload_status_response_from_json.user_tag, "myTagForLatestUploadOn2019-08-06")
 
    #
    def test_upload_status_response_to_json(self):
        
        self.logger.info('test_upload_status_response_to_json')

        got_exception = False
        
        try:
            upload_status_response_from_json = upload_module.upload_status_response_from_json(upload_status_response_str)
            upload_status_response_to_json = upload_module.upload_status_response_to_json(upload_status_response_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

#
upload_response_dict_1 = {
    "id": "oiie8deehw88wwjslsdoifuhe43"
}

#
upload_response_dict_2 = {
    "message": "ERROR"
}

#
upload_response_str_1 = r'''{
    "id": "oiie8deehw88wwjslsdoifuhe43"
}'''

#
upload_response_str_2 = r'''{
    "message": "ERROR"
}'''
    
#
class UploadResponseUnitTest(unittest.TestCase):
    
    #
    def setUp(self):
        self.logger = logger
        self.logger.info('setup')
    
    #
    def tearDown(self):
        self.logger.info('teardown')

    #    
    def test_upload_response_from_dict(self):
        
        self.logger.info('test_upload_response_from_dict')
        
        upload_response = upload_module.UploadResponse

        upload_response_1_from_dict = None
        upload_response_2_from_dict = None
            
        got_exception_1 = False
        got_exception_2 = False

        try:
            upload_response_1_from_dict = upload_response.from_dict(upload_response_dict_1)
        except Exception as ex:
            got_exception_1 = True
            
        try:
            upload_response_2_from_dict = upload_response.from_dict(upload_response_dict_2)
        except Exception as ex:
            got_exception_2 = True

        self.assertFalse(got_exception_1)
        self.assertFalse(got_exception_2)
        self.assertEqual(upload_response_1_from_dict.id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_response_2_from_dict.message, "ERROR")
        
    #    
    def test_upload_response_to_dict(self):
        
        self.logger.info('test_upload_response_to_dict')
        
        upload_response = upload_module.UploadResponse

        upload_response_1_from_dict = None
        upload_response_1_to_dict   = None
        
        upload_response_2_from_dict = None
        upload_response_2_to_dict   = None
                
        got_exception_1 = False
        got_exception_2 = False

        try:
            upload_response_1_from_dict = upload_response.from_dict(upload_response_dict_1)
            upload_response_1_to_dict = upload_response_1_from_dict.to_dict()
        except Exception as ex:
            got_exception_1 = True
            
        try:
            upload_response_2_from_dict = upload_response.from_dict(upload_response_dict_2)
            upload_response_2_to_dict = upload_response_2_from_dict.to_dict()
        except Exception as ex:
            got_exception_2 = True

        self.assertFalse(got_exception_1)
        self.assertFalse(got_exception_2)
        self.assertIsInstance(upload_response_1_to_dict, dict)
        self.assertIsInstance(upload_response_2_to_dict, dict)
        self.assertEqual(upload_response_1_to_dict["id"], "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_response_2_to_dict["message"], "ERROR")

    #
    def test_upload_response_from_json(self):
        
        self.logger.info('test_upload_response_from_json')

        got_exception_1 = False
        got_exception_2 = False

        try:
            upload_response_1_from_json = upload_module.upload_response_from_json(upload_response_str_1)
        except Exception as ex:
            got_exception_1 = True
            
        try:
            upload_response_2_from_json = upload_module.upload_response_from_json(upload_response_str_2)
        except Exception as ex:
            got_exception_2 = True
            
        self.assertFalse(got_exception_1)
        self.assertFalse(got_exception_2)
        self.assertEqual(upload_response_1_from_json.id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_response_2_from_json.message, "ERROR")
 
    #
    def test_upload_response_to_json(self):
        
        self.logger.info('test_upload_response_to_json')

        got_exception_1 = False
        got_exception_2 = False
        
        try:
            upload_status_response_1_from_json = upload_module.upload_response_from_json(upload_response_str_1)
            upload_status_response_1_to_json = upload_module.upload_response_to_json(upload_status_response_1_from_json)
        except Exception as ex:
            got_exception = True
        
        try:
            upload_status_response_2_from_json = upload_module.upload_response_from_json(upload_response_str_2)
            upload_status_response_2_to_json = upload_module.upload_response_to_json(upload_status_response_2_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception_1)
        self.assertFalse(got_exception_2)

#
upload_dict = {
    "tracking_id": "dwpncapweiuvprenuiopanvuopnjlcxzncmdnlak",
    "deletedata": False,
    "datalayer_id": [
        35072,
        30000
    ],
    "hdftype": [
        "HDF4_EOS:EOS_GRID"
    ],
    "conv": [
        "genLin:fl",
        "genLin:fl"
    ],
    "hdfbandname": [
        "minimum_temperature"
    ],
    "url": "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz",
    "timestamp": "2019-4-19 23:4:05 EST",
    "filetype": "hdf",
    "pairsdatatype": "2draster",
    "pairsdimension": [
        "height_above_ground",
        "relative_forecast_issue_time"
    ],
    "band": [
        7,
        4
    ],
    "inputnodata": "-9999",
    "preprocessing": [
        {
            "type": "lidar-rasterize",
            "order": 4,
            "options": {
                "data-layers": [
                    "dtm",
                    "dsm",
                    "chm"
                ],
                "n-pix-global-scale": 30,
                "pdal-preprocessing-jsons": [
                    {
                        "type": "filters.range",
                        "limits": "Classification![7:7]"
                    }
                ],
                "raster-params": [
                    1.4,
                    3.0
                ]
            }
        }
    ],
    "ignoretile": False,
    "geospatialprojection": "EPSG:4326",
    "conv_params_dict": [
        {
            "lin-conv-offset": -30.2,
            "lin-conv-slope": 1.2,
            "non-lin-param2": 5.5,
            "non-lin-param1": 4.2
        }
    ],
    "datainterpolation": "near",
    "user_tag": "myTagForLatestUploadOn2019-08-06",
    "dimension_value": [
        "1200",
        "1504819573"
    ],
    "tile_y": 0,
    "tile_x": 0,
    "upload_status": 
    {
        "status": "INITIALIZING",
        "last_updated": "2019-08-08 00:00:00+00:00",
        "summary": [
            {
                "status": "2.24",
                "last_updated": "2019-08-08 00:00:00+00:00",
                "details": "Success",
                "raw_filename": "22334521-22ddasfggas.tif"
            },
            {
                "status": "-1",
                "last_updated": "2019-08-08 00:00:00+00:00",
                "details": "Failed",
                "raw_filename": "11223410-11cczreffzr.tif"
            }
        ],
        "tracking_id": "oiie8deehw88wwjslsdoifuhe43",
        "progress": "34",
        "user_tag": "myTagForLatestUploadOn2019-08-06"
    },
    "file_path": "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf",
    "storage_key": "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf",
    "delete": False,
    "local": False
}

#
upload_str = r'''{
    "tracking_id": "dwpncapweiuvprenuiopanvuopnjlcxzncmdnlak",
    "deletedata": false,
    "datalayer_id": [
        35072,
        30000
    ],
    "hdftype": [
        "HDF4_EOS:EOS_GRID"
    ],
    "conv": [
        "genLin:fl",
        "genLin:fl"
    ],
    "hdfbandname": [
        "minimum_temperature"
    ],
    "url": "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz",
    "timestamp": "2019-4-19 23:4:05 EST",
    "filetype": "hdf",
    "pairsdatatype": "2draster",
    "pairsdimension": [
        "height_above_ground",
        "relative_forecast_issue_time"
    ],
    "band": [
        7,
        4
    ],
    "inputnodata": "-9999",
    "preprocessing": [
        {
            "type": "lidar-rasterize",
            "order": 4,
            "options": {
                "data-layers": [
                    "dtm",
                    "dsm",
                    "chm"
                ],
                "n-pix-global-scale": 30,
                "pdal-preprocessing-jsons": [
                    {
                        "type": "filters.range",
                        "limits": "Classification![7:7]"
                    }
                ],
                "raster-params": [
                    1.4,
                    3.0
                ]
            }
        }
    ],
    "ignoretile": false,
    "geospatialprojection": "EPSG:4326",
    "conv_params_dict": [
        {
            "lin-conv-offset": -30.2,
            "lin-conv-slope": 1.2,
            "non-lin-param2": 5.5,
            "non-lin-param1": 4.2
        }
    ],
    "datainterpolation": "near",
    "user_tag": "myTagForLatestUploadOn2019-08-06",
    "dimension_value": [
        "1200",
        "1504819573"
    ],
    "tile_y": 0,
    "tile_x": 0,
    "upload_status": 
    {
        "status": "INITIALIZING",
        "last_updated": "2019-08-08 00:00:00+00:00",
        "summary": [
            {
                "status": "2.24",
                "last_updated": "2019-08-08 00:00:00+00:00",
                "details": "Success",
                "raw_filename": "22334521-22ddasfggas.tif"
            },
            {
                "status": "-1",
                "last_updated": "2019-08-08 00:00:00+00:00",
                "details": "Failed",
                "raw_filename": "11223410-11cczreffzr.tif"
            }
        ],
        "tracking_id": "oiie8deehw88wwjslsdoifuhe43",
        "progress": "34",
        "user_tag": "myTagForLatestUploadOn2019-08-06"
    },
    "file_path": "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf",
    "storage_key": "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf",
    "delete": false,
    "local": false
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
    def test_upload_from_dict(self):
        
        self.logger.info('test_upload_from_dict')
        
        upload = upload_module.Upload

        upload_from_dict = None
                
        got_exception = False

        try:
            upload_from_dict = upload.from_dict(upload_dict)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(upload_from_dict.tracking_id, "dwpncapweiuvprenuiopanvuopnjlcxzncmdnlak")
        self.assertEqual(upload_from_dict.delete_data, False)
        self.assertEqual(upload_from_dict.data_layer_id[0], 35072)
        self.assertEqual(upload_from_dict.data_layer_id[1], 30000)
        self.assertEqual(upload_from_dict.hdf_type[0], "HDF4_EOS:EOS_GRID")
        self.assertEqual(upload_from_dict.conv[0], "genLin:fl")
        self.assertEqual(upload_from_dict.conv[1], "genLin:fl")
        self.assertEqual(upload_from_dict.hdf_band_name[0], "minimum_temperature")
        self.assertEqual(upload_from_dict.url, "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz")
        self.assertEqual(upload_from_dict.timestamp, "2019-4-19 23:4:05 EST")
        self.assertEqual(upload_from_dict.file_type, "hdf")
        self.assertEqual(upload_from_dict.pairs_data_type, "2draster")
        self.assertEqual(upload_from_dict.pairs_dimension[0], "height_above_ground")
        self.assertEqual(upload_from_dict.pairs_dimension[1], "relative_forecast_issue_time")
        self.assertEqual(upload_from_dict.band[0], 7)
        self.assertEqual(upload_from_dict.band[1], 4)
        self.assertEqual(upload_from_dict.input_no_data, "-9999")
        self.assertEqual(upload_from_dict.preprocessing[0].type, "lidar-rasterize")
        self.assertEqual(upload_from_dict.preprocessing[0].order, 4)
        self.assertEqual(upload_from_dict.preprocessing[0].options.data_layers[0], "dtm")
        self.assertEqual(upload_from_dict.preprocessing[0].options.data_layers[1], "dsm")
        self.assertEqual(upload_from_dict.preprocessing[0].options.data_layers[2], "chm")
        self.assertEqual(upload_from_dict.preprocessing[0].options.n_pix_global_scale, 30)
        self.assertEqual(upload_from_dict.preprocessing[0].options.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(upload_from_dict.preprocessing[0].options.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(upload_from_dict.preprocessing[0].options.raster_params[0], 1.4)
        self.assertEqual(upload_from_dict.preprocessing[0].options.raster_params[1], 3.0)
        self.assertEqual(upload_from_dict.ignore_tile, False)
        self.assertEqual(upload_from_dict.geospatial_projection, "EPSG:4326")
        self.assertEqual(upload_from_dict.conv_params_dict[0].lin_conv_offset, -30.2)
        self.assertEqual(upload_from_dict.conv_params_dict[0].lin_conv_slope, 1.2)
        self.assertEqual(upload_from_dict.conv_params_dict[0].non_lin_param2, 5.5)
        self.assertEqual(upload_from_dict.conv_params_dict[0].non_lin_param1, 4.2)
        self.assertEqual(upload_from_dict.data_interpolation, "near")
        self.assertEqual(upload_from_dict.user_tag, "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_from_dict.dimension_value[0], "1200")
        self.assertEqual(upload_from_dict.dimension_value[1], "1504819573")
        self.assertEqual(upload_from_dict.tile_y, 0)
        self.assertEqual(upload_from_dict.tile_x, 0)
        self.assertEqual(upload_from_dict.upload_status.status, "INITIALIZING")
        self.assertEqual(upload_from_dict.upload_status.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_dict.upload_status.summary[0].status, 2.24)
        self.assertEqual(upload_from_dict.upload_status.summary[0].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_dict.upload_status.summary[0].details, "Success")
        self.assertEqual(upload_from_dict.upload_status.summary[0].raw_filename, "22334521-22ddasfggas.tif")
        self.assertEqual(upload_from_dict.upload_status.summary[1].status, -1.0)
        self.assertEqual(upload_from_dict.upload_status.summary[1].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_dict.upload_status.summary[1].details, "Failed")
        self.assertEqual(upload_from_dict.upload_status.summary[1].raw_filename, "11223410-11cczreffzr.tif")
        self.assertEqual(upload_from_dict.upload_status.tracking_id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_from_dict.upload_status.progress, 34)
        self.assertEqual(upload_from_dict.upload_status.user_tag, "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_from_dict.file_path, "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_from_dict.storage_key, "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_from_dict.delete, False)
        self.assertEqual(upload_from_dict.local, False)
        
    #    
    def test_upload_to_dict(self):
        
        self.logger.info('test_upload_to_dict')
        
        upload = upload_module.Upload

        upload_from_dict = None
        upload_to_dict   = None
                
        got_exception = False

        try:
            upload_from_dict = upload.from_dict(upload_dict)
            upload_to_dict = upload_from_dict.to_dict()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(upload_to_dict, dict)
        self.assertEqual(upload_to_dict["tracking_id"], "dwpncapweiuvprenuiopanvuopnjlcxzncmdnlak")
        self.assertEqual(upload_to_dict["delete_data"], False)
        self.assertEqual(upload_to_dict["data_layer_id"][0], 35072)
        self.assertEqual(upload_to_dict["data_layer_id"][1], 30000)
        self.assertEqual(upload_to_dict["hdf_type"][0], "HDF4_EOS:EOS_GRID")
        self.assertEqual(upload_to_dict["conv"][0], "genLin:fl")
        self.assertEqual(upload_to_dict["conv"][1], "genLin:fl")
        self.assertEqual(upload_to_dict["hdf_band_name"][0], "minimum_temperature")
        self.assertEqual(upload_to_dict["url"], "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz")
        self.assertEqual(upload_to_dict["timestamp"], "2019-4-19 23:4:05 EST")
        self.assertEqual(upload_to_dict["file_type"], "hdf")
        self.assertEqual(upload_to_dict["pairs_data_type"], "2draster")
        self.assertEqual(upload_to_dict["pairs_dimension"][0], "height_above_ground")
        self.assertEqual(upload_to_dict["pairs_dimension"][1], "relative_forecast_issue_time")
        self.assertEqual(upload_to_dict["band"][0], 7)
        self.assertEqual(upload_to_dict["band"][1], 4)
        self.assertEqual(upload_to_dict["input_no_data"], "-9999")
        self.assertEqual(upload_to_dict["preprocessing"][0]["type"], "lidar-rasterize")
        self.assertEqual(upload_to_dict["preprocessing"][0]["order"], 4)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data_layers"][0], "dtm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data_layers"][1], "dsm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data_layers"][2], "chm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["n_pix_global_scale"], 30)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["pdal_preprocessing_jsons"][0]["type"], "filters.range")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["pdal_preprocessing_jsons"][0]["limits"], "Classification![7:7]")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["raster_params"][0], 1.4)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["raster_params"][1], 3.0)
        self.assertEqual(upload_to_dict["ignore_tile"], False)
        self.assertEqual(upload_to_dict["geospatial_projection"], "EPSG:4326")
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["lin_conv_offset"], -30.2)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["lin_conv_slope"], 1.2)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["non_lin_param2"], 5.5)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["non_lin_param1"], 4.2)
        self.assertEqual(upload_to_dict["data_interpolation"], "near")
        self.assertEqual(upload_to_dict["user_tag"], "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_to_dict["dimension_value"][0], "1200")
        self.assertEqual(upload_to_dict["dimension_value"][1], "1504819573")
        self.assertEqual(upload_to_dict["tile_y"], 0)
        self.assertEqual(upload_to_dict["tile_x"], 0)
        self.assertEqual(upload_to_dict["upload_status"]["status"], "INITIALIZING")
        self.assertEqual(upload_to_dict["upload_status"]["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][0]["status"], 2.24)
        self.assertEqual(upload_to_dict["upload_status"]["summary"][0]["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][0]["details"], "Success")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][0]["raw_filename"], "22334521-22ddasfggas.tif")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][1]["status"], -1.0)
        self.assertEqual(upload_to_dict["upload_status"]["summary"][1]["last_updated"], "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][1]["details"], "Failed")
        self.assertEqual(upload_to_dict["upload_status"]["summary"][1]["raw_filename"], "11223410-11cczreffzr.tif")
        self.assertEqual(upload_to_dict["upload_status"]["tracking_id"], "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_to_dict["upload_status"]["progress"], 34)
        self.assertEqual(upload_to_dict["upload_status"]["user_tag"], "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_to_dict["file_path"], "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_to_dict["storage_key"], "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_to_dict["delete"], False)
        self.assertEqual(upload_to_dict["local"], False)
    
    #    
    def test_upload_to_dict_upload_post(self):
        
        self.logger.info('test_upload_to_dict_upload_post')
        
        upload = upload_module.Upload

        upload_from_dict = None
        upload_to_dict   = None
                
        got_exception = False

        try:
            upload_from_dict = upload.from_dict(upload_dict)
            upload_to_dict = upload_from_dict.to_dict_upload_post()
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)
        self.assertIsInstance(upload_to_dict, dict)
        self.assertEqual(upload_to_dict["deletedata"], False)
        self.assertEqual(upload_to_dict["datalayer_id"][0], 35072)
        self.assertEqual(upload_to_dict["datalayer_id"][1], 30000)
        self.assertEqual(upload_to_dict["hdftype"][0], "HDF4_EOS:EOS_GRID")
        self.assertEqual(upload_to_dict["conv"][0], "genLin:fl")
        self.assertEqual(upload_to_dict["conv"][1], "genLin:fl")
        self.assertEqual(upload_to_dict["hdfbandname"][0], "minimum_temperature")
        self.assertEqual(upload_to_dict["url"], "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz")
        self.assertEqual(upload_to_dict["timestamp"], "2019-4-19 23:4:05 EST")
        self.assertEqual(upload_to_dict["filetype"], "hdf")
        self.assertEqual(upload_to_dict["pairsdatatype"], "2draster")
        self.assertEqual(upload_to_dict["pairsdimension"][0], "height_above_ground")
        self.assertEqual(upload_to_dict["pairsdimension"][1], "relative_forecast_issue_time")
        self.assertEqual(upload_to_dict["band"][0], 7)
        self.assertEqual(upload_to_dict["band"][1], 4)
        self.assertEqual(upload_to_dict["inputnodata"], "-9999")
        self.assertEqual(upload_to_dict["preprocessing"][0]["type"], "lidar-rasterize")
        self.assertEqual(upload_to_dict["preprocessing"][0]["order"], 4)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data-layers"][0], "dtm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data-layers"][1], "dsm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["data-layers"][2], "chm")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["n-pix-global-scale"], 30)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["pdal-preprocessing-jsons"][0]["type"], "filters.range")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["pdal-preprocessing-jsons"][0]["limits"], "Classification![7:7]")
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["raster-params"][0], 1.4)
        self.assertEqual(upload_to_dict["preprocessing"][0]["options"]["raster-params"][1], 3.0)
        self.assertEqual(upload_to_dict["ignoretile"], False)
        self.assertEqual(upload_to_dict["geospatialprojection"], "EPSG:4326")
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["lin-conv-offset"], -30.2)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["lin-conv-slope"], 1.2)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["non-lin-param2"], 5.5)
        self.assertEqual(upload_to_dict["conv_params_dict"][0]["non-lin-param1"], 4.2)
        self.assertEqual(upload_to_dict["datainterpolation"], "near")
        self.assertEqual(upload_to_dict["user_tag"], "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_to_dict["dimension_value"][0], "1200")
        self.assertEqual(upload_to_dict["dimension_value"][1], "1504819573")
        self.assertEqual(upload_to_dict["tile_y"], 0)
        self.assertEqual(upload_to_dict["tile_x"], 0)
        
    #
    def test_upload_from_json(self):
        
        self.logger.info('test_upload_from_json')

        got_exception = False

        try:
            upload_from_json = upload_module.upload_from_json(upload_str)
        except Exception as ex:
            self.logger.info(ex)
            got_exception = True

        self.assertFalse(got_exception)
        self.assertEqual(upload_from_json.tracking_id, "dwpncapweiuvprenuiopanvuopnjlcxzncmdnlak")
        self.assertEqual(upload_from_json.delete_data, False)
        self.assertEqual(upload_from_json.data_layer_id[0], 35072)
        self.assertEqual(upload_from_json.data_layer_id[1], 30000)
        self.assertEqual(upload_from_json.hdf_type[0], "HDF4_EOS:EOS_GRID")
        self.assertEqual(upload_from_json.conv[0], "genLin:fl")
        self.assertEqual(upload_from_json.conv[1], "genLin:fl")
        self.assertEqual(upload_from_json.hdf_band_name[0], "minimum_temperature")
        self.assertEqual(upload_from_json.url, "https://ibm.box.com/shared/static/07egx2po25haozc0mfp4zr6x37h8q0f3.gz")
        self.assertEqual(upload_from_json.timestamp, "2019-4-19 23:4:05 EST")
        self.assertEqual(upload_from_json.file_type, "hdf")
        self.assertEqual(upload_from_json.pairs_data_type, "2draster")
        self.assertEqual(upload_from_json.pairs_dimension[0], "height_above_ground")
        self.assertEqual(upload_from_json.pairs_dimension[1], "relative_forecast_issue_time")
        self.assertEqual(upload_from_json.band[0], 7)
        self.assertEqual(upload_from_json.band[1], 4)
        self.assertEqual(upload_from_json.input_no_data, "-9999")
        self.assertEqual(upload_from_json.preprocessing[0].type, "lidar-rasterize")
        self.assertEqual(upload_from_json.preprocessing[0].order, 4)
        self.assertEqual(upload_from_json.preprocessing[0].options.data_layers[0], "dtm")
        self.assertEqual(upload_from_json.preprocessing[0].options.data_layers[1], "dsm")
        self.assertEqual(upload_from_json.preprocessing[0].options.data_layers[2], "chm")
        self.assertEqual(upload_from_json.preprocessing[0].options.n_pix_global_scale, 30)
        self.assertEqual(upload_from_json.preprocessing[0].options.pdal_preprocessing_jsons[0].type, "filters.range")
        self.assertEqual(upload_from_json.preprocessing[0].options.pdal_preprocessing_jsons[0].limits, "Classification![7:7]")
        self.assertEqual(upload_from_json.preprocessing[0].options.raster_params[0], 1.4)
        self.assertEqual(upload_from_json.preprocessing[0].options.raster_params[1], 3.0)
        self.assertEqual(upload_from_json.ignore_tile, False)
        self.assertEqual(upload_from_json.geospatial_projection, "EPSG:4326")
        self.assertEqual(upload_from_json.conv_params_dict[0].lin_conv_offset, -30.2)
        self.assertEqual(upload_from_json.conv_params_dict[0].lin_conv_slope, 1.2)
        self.assertEqual(upload_from_json.conv_params_dict[0].non_lin_param2, 5.5)
        self.assertEqual(upload_from_json.conv_params_dict[0].non_lin_param1, 4.2)
        self.assertEqual(upload_from_json.data_interpolation, "near")
        self.assertEqual(upload_from_json.user_tag, "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_from_json.dimension_value[0], "1200")
        self.assertEqual(upload_from_json.dimension_value[1], "1504819573")
        self.assertEqual(upload_from_json.tile_y, 0)
        self.assertEqual(upload_from_json.tile_x, 0)
        self.assertEqual(upload_from_json.upload_status.status, "INITIALIZING")
        self.assertEqual(upload_from_json.upload_status.last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_json.upload_status.summary[0].status, 2.24)
        self.assertEqual(upload_from_json.upload_status.summary[0].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_json.upload_status.summary[0].details, "Success")
        self.assertEqual(upload_from_json.upload_status.summary[0].raw_filename, "22334521-22ddasfggas.tif")
        self.assertEqual(upload_from_json.upload_status.summary[1].status, -1.0)
        self.assertEqual(upload_from_json.upload_status.summary[1].last_updated, "2019-08-08 00:00:00+00:00")
        self.assertEqual(upload_from_json.upload_status.summary[1].details, "Failed")
        self.assertEqual(upload_from_json.upload_status.summary[1].raw_filename, "11223410-11cczreffzr.tif")
        self.assertEqual(upload_from_json.upload_status.tracking_id, "oiie8deehw88wwjslsdoifuhe43")
        self.assertEqual(upload_from_json.upload_status.progress, 34)
        self.assertEqual(upload_from_json.upload_status.user_tag, "myTagForLatestUploadOn2019-08-06")
        self.assertEqual(upload_from_json.file_path, "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_from_json.storage_key, "XYZ12X1_X19700101_h00v00_000_1970010100000.hdf")
        self.assertEqual(upload_from_json.delete, False)
        self.assertEqual(upload_from_json.local, False)
 
    #
    def test_upload_to_json(self):
        
        self.logger.info('test_upload_to_json')

        got_exception = False
        
        try:
            upload_from_json = upload_module.upload_from_json(upload_str)
            upload_to_json = upload_module.upload_to_json(upload_from_json)
        except Exception as ex:
            got_exception = True

        self.assertFalse(got_exception)

    @mock.patch('ibmpairs.external.ibm.IBMCOSBucket.get_presigned_url', 
                side_effect = mocked_submit_get_presigned_url
               )
    @mock.patch('ibmpairs.upload.Upload.get_metadata', 
                side_effect = mocked_submit_get_metadata
               )
    @mock.patch('ibmpairs.client.Client.async_post', 
                side_effect=mocked_submit_async_post
               )
    @mock.patch('ibmpairs.external.ibm.IBMCOSBucket.delete', 
                side_effect=mocked_submit_delete
               )
    @mock.patch('ibmpairs.external.ibm.IBMCOSBucket.upload', 
                side_effect = mocked_submit_upload
               )
    @mock.patch('ibmpairs.upload.Upload.check_local_file', 
                side_effect = mocked_submit_check_local_file
               )
    def test_async_submit(self, mock_check, mock_upload, mock_delete, mock_post, mock_metadata, mock_presigned):
        #
        self.logger.info('test_async_submit')
        
        self.logger.info('test_async_submit: upload from COS')
        
        got_cos_1_exception = False
        
        storage       = ibm_cos.IBMCOSBucket()
        cl            = client.Client()
        
        up_from_cos_1 = upload_module.Upload(storage = storage,
                                             file_path = "file1.hdf",
                                             local     = False
                                            )
        
        try:
            asyncio.run(up_from_cos_1.async_submit(upload = up_from_cos_1,
                                                   client = cl
                                                  )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_cos_1_exception = True
                
        self.assertFalse(got_cos_1_exception)        
        
        self.logger.info('test_async_submit: upload from COS- 404')
        
        got_cos_2_exception = False
        
        storage       = ibm_cos.IBMCOSBucket()
        cl            = client.Client()
        
        up_from_cos_2 = upload_module.Upload(storage = storage,
                                             file_path = "file2.hdf",
                                             local     = False
                                            )
        
        try:
            asyncio.run(up_from_cos_2.async_submit(upload = up_from_cos_2,
                                                   client = cl
                                                  )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_cos_2_exception = True
                
        self.assertTrue(got_cos_2_exception)
        
        self.logger.info('test_async_submit: upload from COS- 401')
        
        got_cos_3_exception = False
        
        storage       = ibm_cos.IBMCOSBucket()
        cl            = client.Client()
        
        up_from_cos_3 = upload_module.Upload(storage = storage,
                                             file_path = "file3.hdf",
                                             local     = False
                                            )
        
        try:
            asyncio.run(up_from_cos_2.async_submit(upload = up_from_cos_3,
                                                   client = cl
                                                  )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_cos_3_exception = True
                
        self.assertTrue(got_cos_3_exception)
        
        self.logger.info('test_async_submit: delete after use')
        
        got_cos_4_exception = False
        
        storage       = ibm_cos.IBMCOSBucket()
        cl            = client.Client()
        
        up_from_cos_4 = upload_module.Upload(storage = storage,
                                             file_path = "file1.hdf",
                                             local     = False,
                                             delete    = True
                                            )
        
        try:
            asyncio.run(up_from_cos_4.async_submit(upload = up_from_cos_1,
                                                   client = cl
                                                  )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_cos_4_exception = True
                
        self.assertFalse(got_cos_4_exception)
        
        self.logger.info('test_async_submit: upload from local')
        
        got_local_exception = False
        
        storage       = ibm_cos.IBMCOSBucket()
        cl            = client.Client()
        
        up_from_local = upload_module.Upload(storage = storage,
                                             file_path = "file1.hdf"
                                            )
        
        try:
            asyncio.run(up_from_local.async_submit(upload = up_from_local,
                                                   client = cl
                                                  )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_local_exception = True
                
        self.assertFalse(got_local_exception)

    @mock.patch('ibmpairs.client.Client.async_get', 
                side_effect=mocked_status_async_get
               )
    def test_async_status(self, mock_get):

        #
        self.logger.info('test_async_status')
        
        self.logger.info('test_async_status: status success')
        
        got_submit_exception = False
        
        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up200 = upload_module.Upload(tracking_id = "3",
                                     storage     = storage    
                                    )
        
        try:
            asyncio.run(up200.async_status(upload = up200,
                                           client = cl,
                                           poll   = False,
                                          )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_exception = True
                
        self.assertFalse(got_submit_exception)
        self.assertEqual(up200.upload_status.status, "SUCCEEDED")
        
        self.logger.info('test_async_status: 200 single upload failure')
        
        got_submit_2_exception = False

        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up200_single_fail = upload_module.Upload(tracking_id = "4",
                                                 storage     = storage
                                                )
        
        try:
            asyncio.run(up200_single_fail.async_status(upload = up200_single_fail,
                                                       client = cl,
                                                       poll   = False
                                                      )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_2_exception = True
                
        self.assertFalse(got_submit_2_exception)
        self.assertEqual(up200_single_fail.upload_status.status, "FAILED")
        
        self.logger.info('test_async_status: 200 failure')
        
        got_submit_3_exception = False

        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up200_fail = upload_module.Upload(tracking_id = "5",
                                          storage     = storage
                                         )
        
        try:
            asyncio.run(up200_fail.async_status(upload = up200_fail,
                                                client = cl,
                                                poll   = False
                                               )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_3_exception = True
                
        self.assertFalse(got_submit_3_exception)
        self.assertEqual(up200_fail.upload_status.status, "FAILED")
        
        self.logger.info('test_async_status: 404')
        
        got_submit_4_exception = False

        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up404 = upload_module.Upload(tracking_id = "1",
                                     storage     = storage
                                    )
        
        try:
            asyncio.run(up404.async_status(upload = up404,
                                           client = cl,
                                           poll   = False
                                          )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_4_exception = True
                
        self.assertFalse(got_submit_4_exception)
        self.assertEqual(up404.upload_status.status, "FAILED")
        
        self.logger.info('test_async_status: 503')
        
        got_submit_5_exception = False

        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()

        up503 = upload_module.Upload(tracking_id = "2",
                                     storage     = storage
                                    )
        
        try:
            asyncio.run(up503.async_status(upload = up503,
                                           client = cl,
                                           poll   = False
                                          )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_5_exception = True
                
        self.assertFalse(got_submit_5_exception)
        self.assertEqual(up503.upload_status.status, "FAILED")
        
        self.logger.info('test_async_status: 401')
        
        got_submit_6_exception = False
        
        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up401 = upload_module.Upload(tracking_id = "6",
                                     storage     = storage
                                    )
        
        try:
            asyncio.run(up401.async_status(upload = up401,
                                           client = cl,
                                           poll   = False
                                          )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_6_exception = True
                
        self.assertFalse(got_submit_6_exception)
        self.assertEqual(up401.upload_status.status, "FAILED")
        
        self.logger.info('test_async_status: 200 poll success')
        
        got_submit_7_exception = False
        
        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up200_poll = upload_module.Upload(tracking_id = "7",
                                          storage     = storage
                                         )
        
        try:
            asyncio.run(up200_poll.async_status(upload = up200_poll,
                                                client = cl,
                                                poll   = True
                                               )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_7_exception = True
                
        self.assertFalse(got_submit_7_exception)
        self.assertEqual(up200_poll.upload_status.status, "SUCCEEDED")
        
        self.logger.info('test_async_status: 200 poll failed')
        
        got_submit_8_exception = False
        
        storage       = ibm_cos.IBMCOSBucket(ibm_auth_endpoint = "123")
        cl            = client.Client()
        
        up200_poll_fail = upload_module.Upload(tracking_id = "8",
                                               storage     = storage
                                              )
        
        try:
            asyncio.run(up200_poll_fail.async_status(upload = up200_poll_fail,
                                                     client = cl,
                                                     poll   = True
                                                    )
                       )
        except Exception as ex:
            self.logger.info(ex)
            got_submit_8_exception = True
                
        self.assertFalse(got_submit_8_exception)
        self.assertEqual(up200_poll_fail.upload_status.status, "FAILED")
        
    #
#    def test_async_submit_and_check_status(self):

    #
#    def test_submit
    
    #
#    def test_status
    
    #
#    def test_submit_and_check_status(self):
   
        
#
#class BatchUploadUnitTest(unittest.TestCase):
    
    #
#    def setUp(self):
#        self.logger = logger
#        self.logger.info('setup')
    
    #
#    def tearDown(self):
#        self.logger.info('teardown')
    
    #    
#    def test_batch_upload(self):