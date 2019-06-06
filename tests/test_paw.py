#!/usr/bin/env python
"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause

*notes*:
    - set the environment variable `PAW_TESTS_REAL_CONNECT=true` in order
      to check the defined mocks against real responses from the PAIRS server
      set by `PAW_TESTS_PAIRS_SERVER` with base URI `PAW_TESTS_PAIRS_BASE_URI`.
    - credentials can be set with `PAW_TESTS_PAIRS_USER` and a corresponding
      `ibmpairspass.txt` file, cf. `ibmpairs.paw.get_pairs_api_password()`


**TODO**:
    - compare mock vs. real data for aggregated queries
"""

# fold: imports{{{
# general imports
import sys, os, time, glob
# Python unit testing
import unittest
# compare files
import filecmp
# requests module
import requests
# requests module mocking
import responses
# regular expressions
import re
# handle json
import json
# handle timestamps
import datetime
# get PAW to test
sys.path.append('.')
from ibmpairs import paw
# message logging tool
import logging
# handle ZIP files
import zipfile
# handling scientific data
import numpy
import pandas
# string type compatibility with Python 2 and 3
try:
    string_type = basestring
except NameError:
    string_type = str
#}}}
# fold: parameter settings{{{
# define global test parameters
TEST_DATA_DIR               = 'tests/data'
PAIRS_SERVER                = 'pairs.res.ibm.com'
PAIRS_BASE_URI              = '/'
QUERY_ENDPOINT              = 'v2/query'
STATUS_ENDPOINT             = 'v2/queryjobs/'
DOWNLOAD_ENDPOINT           = 'v2/queryjobs/download/'
REAL_CONNECT                = False
PAIRS_USER                  = 'fakeUser'
PAIRS_PASSWORD              = 'fakePassword'
PAIRS_PASSWORD_FILE_NAME    = 'ibmpairspass.txt'
# read/overwrite parameters from environment
for var in (
    'REAL_CONNECT',
    'PAIRS_SERVER',
    'PAIRS_USER',
):
    if 'PAW_TESTS_'+var in os.environ:
        exec(
            "%s = os.environ['PAW_TESTS_%s']" % (var, var)
        )
# convert types read in from environment
REAL_CONNECT            = REAL_CONNECT == 'true'
# set credentials
if os.path.exists(os.path.expanduser(PAIRS_PASSWORD_FILE_NAME)):
    try:
        PAIRS_PASSWORD  = paw.get_pairs_api_password(PAIRS_SERVER, PAIRS_USER)
    except:
        PAIRS_PASSWORD  = None
PAIRS_CREDENTIALS       = (PAIRS_USER, PAIRS_PASSWORD)
# }}}

# fold: test PAIRS point queries{{{
class TestPointQuery(unittest.TestCase):
    """
    Test cases for querying point data from PAIRS.
    """
    # fold: setup mocked environment#{{{
    @classmethod
    def setUpClass(cls):
        # define and start PAIRS mock server
        cls.pairsServerMock = responses.RequestsMock()
        ## define endpoint processing
        def point_data_endpoint(request):
            respCode        = 400
            payload         = json.loads(request.body)
            # perform some tests on payload sent
            if  payload['spatial']['type'] == 'point' \
            and len(payload['spatial']['coordinates']) > 1 \
            and len(payload['spatial']['coordinates']) % 2 == 0:
                respCode    = 200
            # check whether a raster or vector point query is performed
            if re.match('^P', payload['layers'][0]['id']) is not None:
                # so far, vector queries can take a single point only
                if 2==len(payload['spatial']['coordinates']):
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR, 'point-data-sample-response-vector.json'))
                    )
                else:
                    respCode    = 400
            else:
                # generate response body
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'point-data-sample-response-raster.json'))
                )
            headers         = {}
            return respCode, headers, json.dumps(response_body)
        ## add endpoint
        cls.pairsServerMock.add_callback(
            responses.POST,
            'https://'+PAIRS_SERVER+PAIRS_BASE_URI+QUERY_ENDPOINT,
            callback=point_data_endpoint,
            content_type='application/json',
        )
        cls.pairsServerMock.start()

    @classmethod
    def tearDownClass(cls):
        cls.pairsServerMock.stop()
    #}}}

    def test_from_point_query_raster(self):
        """
        Test querying raster point data.
        """
        # query mocked data
        logging.info("TEST: Query (mocked) point data.")
        # define point query
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # submit point query
        testPointQuery.submit()
        # for complience with general PAW query scheme, perform fake poll and download
        testPointQuery.poll_till_finished()
        testPointQuery.download()
        testPointQuery.create_layers()
        # try to split property string column (although having no effect, it should run through) 
        colsBeforeSplit     = len(testPointQuery.vdf.columns)
        testPointQuery.split_property_string_column()
        colsAfterSplit      = len(testPointQuery.vdf.columns)
        self.assertEqual(colsBeforeSplit, colsAfterSplit)
        # check vector data frame
        ## number of data points is correct
        logging.info("TEST: Perform vector data frame tests.")
        self.assertEqual(
            2, len(testPointQuery.vdf)
        )
        ## column names agree with data response
        self.assertListEqual(
            sorted(
                list(testPointQuery.querySubmit.json()['data'][0].keys()) \
              + [paw.PAIRS_VECTOR_GEOMETRY_COLUMN_NAME]
            ),
            sorted(testPointQuery.vdf.columns),
        )
        ## check (some) data types from response
        self.assertIsInstance(
            testPointQuery.vdf.longitude[0],
            float,
        )
        self.assertIsInstance(
            testPointQuery.vdf.timestamp[0],
            datetime.datetime,
        )
        self.assertIsInstance(
            testPointQuery.vdf.value[0],
            string_type,
        )

    def test_from_point_query_vector(self):
        """
        Test querying vector point data.
        """
        # query mocked data
        logging.info("TEST: Query (mocked) point data.")
        # define point query
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-vector.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # submit point query
        testPointQuery.submit()
        # for complience with general PAW query scheme, perform fake poll and download
        testPointQuery.poll_till_finished()
        testPointQuery.download()
        testPointQuery.create_layers()
        # check vector data frame
        ## number of data points is correct
        logging.info("TEST: Perform vector data frame tests.")
        self.assertEqual(
            2, len(testPointQuery.vdf)
        )
        ## column names agree with data response
        self.assertListEqual(
            sorted(
                list(testPointQuery.querySubmit.json()['data'][0].keys())
            ),
            sorted(testPointQuery.vdf.columns),
        )
        ## check (some) data types from response
        self.assertIsInstance(
            testPointQuery.vdf.timestamp[0],
            datetime.datetime,
        )
        self.assertIsInstance(
            testPointQuery.vdf.value[0],
            string_type,
        )
        # check property string column splitting
        colsBeforeSplit     = len(testPointQuery.vdf.columns)
        testPointQuery.split_property_string_column()
        colsAfterSplit      = len(testPointQuery.vdf.columns)
        if paw.PROPERTY_STRING_COL_NAME_POINT in testPointQuery.vdf.columns:
            self.assertLess(colsBeforeSplit, colsAfterSplit)
        else:
            self.assertEqual(colsBeforeSplit, colsAfterSplit)
        # run twice to double-check it is not increasing the number of columns
        testPointQuery.split_property_string_column()
        colsAfter2ndSplit   = len(testPointQuery.vdf.columns)
        self.assertEqual(colsAfterSplit, colsAfter2ndSplit)

    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service."
    )
    def test_mock_from_point_query(self):
        """
        Checks the real PAIRS point query service against the mock used.
        """
        # get real data
        self.pairsServerMock.stop()
        testPointQueryRasterReal = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        testPointQueryVectorReal = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-vector.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        self.pairsServerMock.start()
        # get mock data
        testPointQueryRasterMock = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        testPointQueryVectorMock = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-vector.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # compare data entry keys
        self.assertListEqual(
            sorted(testPointQueryRasterReal.querySubmit.json()['data'][0].keys()),
            sorted(testPointQueryRasterMock.querySubmit.json()['data'][0].keys()),
        )
        self.assertListEqual(
            sorted(testPointQueryVectorReal.querySubmit.json()['data'][0].keys()),
            sorted(testPointQueryVectorMock.querySubmit.json()['data'][0].keys()),
        )

    def test_dataframe_generation(self):
        """
        Tests functions that massage the received data to the *unified* PAW dataframe.
        """
        # query mocked data
        logging.info("TEST: Generation of unified PAW dataframe for point data.")
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # submit query
        testPointQuery.submit()
        # set timestamp column
        testPointQuery.set_timestamp_column('timestamp')
        # set point coordinate columns
        testPointQuery.set_lat_lon_columns('latitude', 'longitude', 'geometry')
#}}}

# fold: test PAIRS raster and vector queries{{{
class TestPollQuery(unittest.TestCase):
    """
    Test cases for poll-queries of raster and vector data from PAIRS.
    """
    # fold: general class parameters#{{{
    ## time to simulate raster query generation
    RASTER_QUERY_TIME_SEC       = 2
    ## relative deviation of file size for comparing downloaded data with mock
    REL_FILESIZE_DEV            = .1
    ## local sample data
    PAIRS_RASTER_ZIP_PATH       = os.path.join(TEST_DATA_DIR,'12_07_2018T18_39_36-1544202000_23976938.zip')
    PAIRS_AGG_RASTER_ZIP_PATH   = os.path.join(TEST_DATA_DIR,'12_07_2018T19_10_50-1544202000_25850895.zip')
    PAIRS_VECTOR_ZIP_PATH       = os.path.join(TEST_DATA_DIR,'04_10_2019T21_45_15-1554912000_35115995.zip')
    #}}}

    # fold: test environment setup#{{{
    @classmethod
    def setUpClass(cls):
        # mock polls till finished
        cls.pollsTillRasterFinished = 2
        cls.pollsTillAggFinished    = 2
        # define time of last server call (default UNIX epoch time 0)
        cls.lastCallTime    = datetime.datetime.fromtimestamp(0)
        # define and start PAIRS mock server
        cls.pairsServerMock = responses.RequestsMock()

        # define query submit endpoint processings
        def submit_query_endpoint(request):
            respCode        = 400
            payload         = json.loads(request.body)
            # perform some tests on payload sent
            if  payload['spatial']['type'] == 'square' \
                and len(payload['spatial']['coordinates']) == 4:
                respCode    = 200
            # generate response body (depending on various scenarios)
            if "aggregation" in payload["spatial"].keys():
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'aggregation-data-sample-response.json'))
                )
            elif re.match('^P', payload['layers'][0]['id']) is not None:
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'vector-data-sample-response.json'))
                )
            else:
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'raster-data-sample-response.json'))
                )
            headers         = {}
            return respCode, headers, json.dumps(response_body)

        # define query status endpoint processings
        def poll_query_status_endpoint(request):
            # extract PAIRS query ID from query URL
            pairsQueryID = request.url.split('/')[-1]
            # generate response body
            headers         = {}
            if pairsQueryID == os.path.splitext(
                os.path.basename(cls.PAIRS_RASTER_ZIP_PATH)
            )[0].split('-')[-1]:
                cls.pollsTillRasterFinished -= 1
                if cls.pollsTillRasterFinished > 0:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'raster-data-sample-status-running-response.json'))
                    )
                else:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'raster-data-sample-status-finished-response.json'))
                    )
            elif pairsQueryID == os.path.splitext(
                os.path.basename(cls.PAIRS_AGG_RASTER_ZIP_PATH)
            )[0].split('-')[-1]:
                cls.pollsTillAggFinished -= 1
                if cls.pollsTillAggFinished > 0:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'aggregation-data-sample-status-running-response.json'))
                    )
                else:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'aggregation-data-sample-status-finished-response.json'))
                    )
            elif pairsQueryID == os.path.splitext(
                os.path.basename(cls.PAIRS_VECTOR_ZIP_PATH)
            )[0].split('-')[-1]:
                cls.pollsTillAggFinished -= 1
                if cls.pollsTillAggFinished > 0:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'vector-data-sample-status-running-response.json'))
                    )
                else:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'vector-data-sample-status-finished-response.json'))
                    )
            else:
                return 404, headers, json.dumps(
                    {
                        "message": "mocked test server does not have data for ID '{}'".format(pairsQueryID)
                    }
                )
            # simulate query processing time
            time.sleep(cls.RASTER_QUERY_TIME_SEC)
            # result return
            return 200, headers, json.dumps(response_body)


        ## add endpoints
        ### query submit
        cls.pairsServerMock.add_callback(
            responses.POST,
            'https://'+PAIRS_SERVER+PAIRS_BASE_URI+QUERY_ENDPOINT,
            callback=submit_query_endpoint,
            content_type='application/json',
        )
        ### query downloads
        for queryZIPPath in [
            cls.PAIRS_RASTER_ZIP_PATH,
            cls.PAIRS_AGG_RASTER_ZIP_PATH,
            cls.PAIRS_VECTOR_ZIP_PATH
        ]:
            queryID = os.path.splitext(
                os.path.basename(queryZIPPath)
            )[0].split('-')[-1]
            with open(queryZIPPath, 'rb') as queryData:
                cls.pairsServerMock.add(
                    responses.GET,
                    r'https://{}{}{}{}'.format(PAIRS_SERVER, PAIRS_BASE_URI, DOWNLOAD_ENDPOINT, queryID),
                    body        = queryData.read(),
                    status      = 200,
                    content_type='application/zip',
                    stream=True,
                )
        ### query status
        cls.pairsServerMock.add_callback(
            responses.GET,
            re.compile(
                r'https://{}{}{}[0-9]+_[0-9]+'.format(PAIRS_SERVER, PAIRS_BASE_URI, STATUS_ENDPOINT)
            ),
            callback=poll_query_status_endpoint,
            content_type='application/json',
        )
        ### start the mocked server
        cls.pairsServerMock.start()

    @classmethod
    def tearDownClass(cls):
        cls.pairsServerMock.stop()
    #}}}


    # fold: test ordinary raster queries#{{{
    def raster_query(self, useLocalZip=False):
        """
        Query raster data in various ways.
        """
        # query mocked data
        logging.info("TEST: Query (mocked) data.")
        testRasterQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'raster-data-sample-request.json'))) \
            if not useLocalZip else self.PAIRS_RASTER_ZIP_PATH,
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # check that query got submitted
        testRasterQuery.submit()
        if not useLocalZip:
            self.assertTrue(testRasterQuery.querySubmit.ok)
        # poll and check that data status is finished
        testRasterQuery.poll_till_finished(printStatus=True)
        if not useLocalZip:
            self.assertTrue(testRasterQuery.queryStatus.ok)
        # check that certain files exist
        testRasterQuery.download()
        self.assertTrue(
            os.path.exists(testRasterQuery.zipFilePath)
        )
        logging.info("TEST: Check files downloaded.")
        with zipfile.ZipFile(testRasterQuery.zipFilePath) as zf:
            # test the existence of the basic meta file
            for fileName in ['output.info', ]:
                self.assertTrue(
                        fileName in zf.namelist()
                )
            # check that for each GeoTiff file there exists a corresonding JSON meta file
            for rasterFilePath in zf.namelist():
                # find all PAIRS GeoTiff files
                if rasterFilePath.endswith('.tiff'):
                    # check a corresponding JSON file exists
                    self.assertTrue(
                        rasterFilePath+'.json' in zf.namelist()
                    )
                    # try to temporarily open the JSON file
                    json.loads(zf.read(rasterFilePath+'.json'))
        # load raster meta data
        logging.info("TEST: Load raster meta data.")
        testRasterQuery.list_layers()
        # check that 'details' of raster data have been successfully loaded by
        # getting the spatial reference information
        self.assertIsInstance(
            list(testRasterQuery.metadata.values())[0]["details"]["spatialRef"],
            string_type
        )
        # check that all data are listed as type raster
        self.assertTrue(
            all([
                'raster' == meta['layerType']
                for meta in testRasterQuery.metadata.values()
            ])
        )
        logging.info("TEST: Create NumPy arrays from raster data.")
        # load the raster data into a NumPy array
        testRasterQuery.create_layers()
        # access the numpy array
        for name, meta in testRasterQuery.metadata.items():
            if meta['layerType'] == 'raster':
                self.assertIsInstance(
                    testRasterQuery.data[name],
                    numpy.ndarray
                )
        # check that the data acknowledgement statement is not empty
        self.assertIsNotNone(testRasterQuery.dataAcknowledgeText)

    def test_raster_query(self):
        """
        Test querying raster data.
        """
        self.raster_query()

    def test_raster_query_cached(self):
        """
        Test querying raster data from local PAIRS ZIP file.
        """
        self.raster_query(useLocalZip=True)
    #}}}

    # fold: test raster aggregation queries#{{{
    def raster_aggregation_query(self, useLocalZip=False):
        """
        Query aggregated raster data.
        """
        # query mocked data
        logging.info("TEST: Query (mocked) aggregation data.")
        testRasterAggQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'aggregation-data-sample-request.json'))) \
            if not useLocalZip else self.PAIRS_AGG_RASTER_ZIP_PATH,
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # check that query got submitted
        testRasterAggQuery.submit()
        if not useLocalZip:
            self.assertTrue(testRasterAggQuery.querySubmit.ok)
        # poll and check that data status is finished
        testRasterAggQuery.poll_till_finished(printStatus=True)
        if not useLocalZip:
            self.assertTrue(testRasterAggQuery.queryStatus.ok)
        # check that certain files exist
        testRasterAggQuery.download()
        self.assertTrue(
            os.path.exists(testRasterAggQuery.zipFilePath)
        )
        logging.info("TEST: Check files downloaded.")
        with zipfile.ZipFile(testRasterAggQuery.zipFilePath) as zf:
            # test the existence of the basic meta file
            for fileName in ['output.info', ]:
                self.assertTrue(
                        fileName in zf.namelist()
                )
            # check that for each aggregated CSV file there exists a corresonding JSON meta file
            for rasterFilePath in zf.namelist():
                # find all PAIRS GeoTiff files
                if rasterFilePath.endswith('.csv'):
                    # check a corresponding JSON file exists
                    self.assertTrue(
                        rasterFilePath+'.json' in zf.namelist()
                    )
                    # try to temporarily open the JSON file
                    json.loads(zf.read(rasterFilePath+'.json'))
        # load aggregated raster meta data (which are actually vector-type data!)
        logging.info("TEST: Load aggregated raster meta data.")
        testRasterAggQuery.list_layers()
        # check that 'details' of raster data have been successfully loaded by
        # getting the spatial reference information
        self.assertIsInstance(
            list(testRasterAggQuery.metadata.values())[0]["details"]["spatialRef"],
            string_type
        )
        # check that all data are listed as type vector
        self.assertTrue(
            all([
                'vector' == meta['layerType']
                for meta in testRasterAggQuery.metadata.values()
            ])
        )
        logging.info("TEST: Create Pandas dataframes from aggregated raster data.")
        # load the aggregated raster data as vector data into Pandas dataframes 
        testRasterAggQuery.create_layers()
        # access the numpy array
        for name, meta in testRasterAggQuery.metadata.items():
            if meta['layerType'] == 'vector':
                self.assertIsInstance(
                    testRasterAggQuery.data[name],
                    pandas.DataFrame,
                )
        # check that the data acknowledgement statement is not empty
        self.assertIsNotNone(testRasterAggQuery.dataAcknowledgeText)

    def test_raster_aggregation_query(self):
        """
        Test querying aggregated raster data.
        """
        self.raster_aggregation_query()

    def test_raster_aggregation_query_cached(self):
        """
        Test querying aggregated raster data from local PAIRS ZIP file.
        """
        self.raster_aggregation_query(useLocalZip=True)
    #}}}

    # fold: test vector queries #{{{
    def vector_query(self, useLocalZip=False):
        """
        Query vector data in various ways.
        """
        # query mocked data
        logging.info("TEST: Query (mocked) data.")
        testVectorQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'vector-data-sample-request.json'))) \
            if not useLocalZip else self.PAIRS_VECTOR_ZIP_PATH,
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        # check that query got submitted
        testVectorQuery.submit()
        if not useLocalZip:
            self.assertTrue(testVectorQuery.querySubmit.ok)
        # poll and check that data status is finished
        testVectorQuery.poll_till_finished(printStatus=True)
        if not useLocalZip:
            self.assertTrue(testVectorQuery.queryStatus.ok)
        # check that certain files exist
        testVectorQuery.download()
        self.assertTrue(
            os.path.exists(testVectorQuery.zipFilePath)
        )
        logging.info("TEST: Check files downloaded.")
        with zipfile.ZipFile(testVectorQuery.zipFilePath) as zf:
            pass
            # test the existence of the basic meta file
            # ATTENTION: disabled for now, because it needs to be implemented
            #for fileName in ['output.info', ]:
            #    self.assertTrue(
            #            fileName in zf.namelist()
            #    )
        # load raster meta data
        logging.info("TEST: Load vector meta data.")
        testVectorQuery.list_layers()
        # check that all data are listed as type vector
        self.assertTrue(
            all([
                'vector' == meta['layerType']
                for meta in testVectorQuery.metadata.values()
            ])
        )
        logging.info("TEST: Create dataframe from raster data.")
        # load the raster data into a NumPy array
        testVectorQuery.create_layers()
        # access the vector dataframe
        for name, meta in testVectorQuery.metadata.items():
            if meta['layerType'] == 'vector':
                self.assertIsInstance(
                    testVectorQuery.data[name],
                    pandas.DataFrame,
                )
                # try to split property string column (if any)
                testVectorQuery.vdf = testVectorQuery.data[name]
                # check property string column splitting
                colsBeforeSplit     = len(testVectorQuery.vdf.columns)
                testVectorQuery.split_property_string_column()
                colsAfterSplit      = len(testVectorQuery.vdf.columns)
                if paw.PROPERTY_STRING_COL_NAME in testVectorQuery.vdf.columns:
                    self.assertLess(colsBeforeSplit, colsAfterSplit)
                else:
                    self.assertEqual(colsBeforeSplit, colsAfterSplit)
                # run twice to double-check it is not increasing the number of columns
                testVectorQuery.split_property_string_column()
                colsAfter2ndSplit   = len(testVectorQuery.vdf.columns)
                self.assertEqual(colsAfterSplit, colsAfter2ndSplit)
        # check that the data acknowledgement statement is not empty
        self.assertIsNotNone(testVectorQuery.dataAcknowledgeText)

    def test_vector_query(self):
        """
        Test querying vector data.
        """
        self.vector_query()

    def test_vector_query_cached(self):
        """
        Test querying vector data from local PAIRS ZIP file.
        """
        self.vector_query(useLocalZip=True)
    #}}}

    def TO_BE_IMPLEMENTED_test_dataframe_generation(self):
        """
        Tests functions that massage the received data to the *unified* PAW dataframe.
        """
        # query mocked data
        logging.info("TEST: Generation of unified PAW dataframe for raster data.")
        testRasterQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'raster-data-sample-request.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        testRasterQuery.submit()
        testRasterQuery.poll_till_finished(printStatus=True)
        testRasterQuery.download()
        # create dataframe from ratser data
        testRasterQuery.create_dataframe()
        # check that the dataset and datalayer column names have been added
        self.assertIn(
            'layerName',
            testRasterQuery.dataframe[list(testRasterQuery.metadata.keys())[0]].columns
        )


    # fold: test cached mock data to simulate PAIRS server against real service#{{{
    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service."
    )
    def test_mock_raster_query(self):
        """
        Checks the real PAIRS raster query service against the mock used.
        """
        # get real data
        # prevent the responses module to complain about unused URL endponts of the mock
        try:
            self.pairsServerMock.stop()
        except Exception as e:
            # catch not all requests called error
            logging.warning(
                'Stopping the mocked PAIRS server caused (potentially irrelevant) trouble: {}'.format(e)
            )
        # check query submit
        logging.info("TEST: Perform query to real PAIRS server.")
        subResp = requests.post(
            'https://'+PAIRS_SERVER+PAIRS_BASE_URI+QUERY_ENDPOINT,
            json    = json.load(open(os.path.join(TEST_DATA_DIR,'raster-data-sample-request.json'))),
            auth    = PAIRS_CREDENTIALS,
        ).json()
        self.assertIn(
            'id',
            subResp.keys()
        )
        self.assertIsInstance(
            subResp['id'],
            string_type
        )
        # check query poll
        while True:
            statResp = requests.get(
                'https://'+PAIRS_SERVER+PAIRS_BASE_URI+STATUS_ENDPOINT+subResp['id'],
                auth    = PAIRS_CREDENTIALS,
            ).json()
            assert set(['id', 'rtStatus', 'statusCode']) <= set(statResp.keys())
            self.assertIsInstance(
                statResp['statusCode'],
                int
            )
            if statResp['statusCode'] >= 20:
                break
        # check query result
        downloadResp = requests.get(
            'https://'+PAIRS_SERVER+PAIRS_BASE_URI+DOWNLOAD_ENDPOINT+subResp['id'],
            auth    = PAIRS_CREDENTIALS,
            stream  = True,
        )
        pairsDataZip = '/tmp/pairs-test-raster-download-{}.zip'.format(subResp['id'])
        with open(pairsDataZip, 'wb') as f:
            for chunk in downloadResp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        self.pairsServerMock.start()
        # basic test of real data
        self.assertTrue(
            zipfile.is_zipfile(pairsDataZip)
        )
        # get mock data
        testRasterQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'raster-data-sample-request.json'))),
            'https://'+PAIRS_SERVER,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
        )
        testRasterQuery.submit()
        testRasterQuery.poll_till_finished(printStatus=True)
        testRasterQuery.download()
        pairsMockZip = testRasterQuery.queryDir+'.zip'
        # make sure that files in mock are available in real download
        # and that the size of the data and the mock are approximately the same
        logging.info("TEST: Check that all files from the mock exist in the real data queried.")
        with zipfile.ZipFile(pairsMockZip, 'r') as mock, \
             zipfile.ZipFile(pairsDataZip, 'r') as real:
            # generate info dictionaries
            mockInfo = {
                f.filename: f.file_size
                for f in mock.infolist()
            }
            realInfo = {
                f.filename: f.file_size
                for f in real.infolist()
            }
            # check that files in mock are contained in real data (in terms of names)
            assert set(mockInfo.keys()) <= set(realInfo.keys())
            # check that file sizes are approximately the same
            for key in mockInfo.keys():
                self.assertAlmostEqual(
                    mockInfo[key], realInfo[key],
                    delta = self.REL_FILESIZE_DEV * realInfo[key]
                )
    #}}}
# }}}

if __name__ == '__main__':
    unittest.main()
