#!/usr/bin/env python
"""
Tests the IBM PAIRS API wrapper features.

Copyright 2019-2020 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause

*notes*:
    - set the environment variable `PAW_TESTS_REAL_CONNECT=true` in order
      to check the defined mocks against real responses from the PAIRS server
      set by `PAW_TESTS_PAIRS_SERVER` with base URI `PAW_TESTS_PAIRS_BASE_URI`.
    - credentials can be set with `PAW_TESTS_PAIRS_USER` and a corresponding
      `ibmpairspass.txt` file or another one specified by `PAW_TESTS_PAIRS_PASSWORD_FILE_NAME`,
      cf. `ibmpairs.paw.get_pairs_api_password()`


**TODO**:
    - full integration of query-to-COS feature (among others, test against real service)
      by getting COS bucket information from environment for real connection, delete
      files from COS?
    - compare mock vs. real data for aggregated queries, batch point queries, raster as csv
    - check that apiJSON for v2/queryhistories/full/queryjobs/{ID} is complete
      for aggregation and raster queries, vector queries is empty today
    - check split_property_string_column() from mixed point query (add corresponding JSON)
    - add test of *publish query to GUI*-feature for `REAL_CONNECT=True`
"""

# fold: imports{{{
import pytest
# general imports
import sys, os, time, glob, tempfile
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
import datetime, pytz
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
# handle geometric data
import shapely
# string type compatibility with Python 2 and 3
PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 2:
    string_type = basestring
else:
    string_type = str
#}}}
# fold: parameter settings{{{
# define global test parameters
TEST_DATA_DIR                   = 'tests/data'
PAIRS_SERVER                    = 'pairs.res.ibm.com'
PAIRS_PORT                      = None
PAIRS_BASE_URI                  = '/'
QUERY_ENDPOINT                  = 'v2/query'
STATUS_ENDPOINT                 = 'v2/queryjobs/'
DOWNLOAD_ENDPOINT               = 'v2/queryjobs/download/'
COS_UPLOAD_ENDPOINT             = 'v2/queryjobs/upload/'
TIMESERIES_ENDPOINT             = 'v2/timeseries'
TIMESERIES_RESPONSE_FILE_SCHEMA = '{layerID}_{lon}~{lat}_{t0}-{t1}.json'
PAIRS_QUERY_ID_REGEX            = '[0-9]+_[0-9]+'
QUERY_INFO_ENDPOINT             = 'v2/queryhistories/full/queryjob/'
REAL_CONNECT                    = False
USE_SSL                         = True
VERIFY_SSL                      = True
PAIRS_USER                      = 'fakeUser'
PAIRS_PASSWORD                  = 'fakePassword'
PAIRS_PASSWORD_FILE_NAME        = 'ibmpairspass.txt'
pytest.realConnectZIPPath       = None
pytest.realConnectQueryID       = None
COS_BUCKET_NAME                 = 'test-paw'
COS_BUCKET_KEY                  = 'faKeKEY4M0ckTest'
COS_ENDPOINT                    = 'https://s3.us-east.cloud-object-storage.appdomain.cloud'
# read/overwrite parameters from environment
for var in (
    'REAL_CONNECT',
    'USE_SSL',
    'VERIFY_SSL',
    'PAIRS_SERVER',
    'PAIRS_BASE_URI',
    'PAIRS_USER',
    'PAIRS_PORT',
    'PAIRS_PASSWORD_FILE_NAME',
    'COS_BUCKET_NAME',
    'COS_BUCKET_KEY',
):
    if 'PAW_TESTS_'+var in os.environ:
        exec(
            "%s = os.environ['PAW_TESTS_%s']" % (var, var)
        )
# convert types read in from environment
if isinstance(REAL_CONNECT, string_type):
    REAL_CONNECT    = REAL_CONNECT.lower()  == 'true'
if isinstance(VERIFY_SSL, string_type):
    VERIFY_SSL      = VERIFY_SSL.lower()    == 'true'
if isinstance(USE_SSL, string_type):
    USE_SSL         = USE_SSL.lower()       == 'true'
# set protocol
WEB_PROTOCOL        = 'https' if USE_SSL else 'http'
try:
    PAIRS_PORT      = int(PAIRS_PORT)
except:
    pass
# set credentials
if os.path.exists(os.path.expanduser(PAIRS_PASSWORD_FILE_NAME)):
    try:
        PAIRS_PASSWORD  = paw.get_pairs_api_password(
            PAIRS_SERVER,
            PAIRS_USER,
            passFile=PAIRS_PASSWORD_FILE_NAME,
        )
    except Exception as e:
        PAIRS_PASSWORD  = None
PAIRS_CREDENTIALS       = (PAIRS_USER, PAIRS_PASSWORD,)
if REAL_CONNECT:
    logging.info(
        "Using IBM PAIRS server base endpoint '{}{}' and login user '{}' with password file '{}'.".format(
            PAIRS_SERVER, PAIRS_BASE_URI, PAIRS_USER, PAIRS_PASSWORD_FILE_NAME,
        )
    )
else:
    logging.warning('Not testing against real PAIRS instance.')
# }}}

# fold: test password reading function #{{{
def test_password_reader():
    # if password file cannot be found, error needs to be raised
    with pytest.raises(Exception):
        paw.get_pairs_api_password(
            PAIRS_SERVER, PAIRS_USER,
            passFile='/not-existing-at-all-random-87jklkooclkclsiddadaoi',
        )
    with pytest.raises(Exception) as e_info:
        paw.get_pairs_api_password(
            PAIRS_SERVER, PAIRS_USER+'a', passFile=None
        )
    # create temporary password file
    with tempfile.NamedTemporaryFile('w') as tf:
        tf.write('{}:{}:{}\n'.format(PAIRS_SERVER, PAIRS_USER, PAIRS_PASSWORD,))
        tf.flush()
        # function should throw in case it gets an incorrect user or server name
        with pytest.raises(Exception):
            paw.get_pairs_api_password(
                PAIRS_SERVER+'a', PAIRS_USER,
                passFile=tf.name,
            )
        with pytest.raises(Exception):
            paw.get_pairs_api_password(
                PAIRS_SERVER, PAIRS_USER+'a',
                passFile=tf.name,
            )
        # finally we want to get back the correct password
        assert PAIRS_PASSWORD == paw.get_pairs_api_password(
            WEB_PROTOCOL+'://'+PAIRS_SERVER, PAIRS_USER,
            passFile=tf.name,
        )
        assert PAIRS_PASSWORD == paw.get_pairs_api_password(
            PAIRS_SERVER, PAIRS_USER,
            passFile=tf.name,
        )
#}}}

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
            # check header (hard stopper if not correct)
            if not 'Content-Type' in request.headers.keys() \
            or request.headers['Content-Type'] != 'application/json':
                respCode        = 415
                response_body   = {}
                logging.error('Request header incompatible: {}'.format(request.headers))

            return respCode, headers, json.dumps(response_body)
        ## add endpoint
        cls.pairsServerMock.add_callback(
            responses.POST,
            WEB_PROTOCOL+'://'+PAIRS_SERVER+PAIRS_BASE_URI+QUERY_ENDPOINT,
            callback=point_data_endpoint,
            content_type='application/json',
        )
        if not REAL_CONNECT:
            cls.pairsServerMock.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.pairsServerMock.stop()
        except:
            pass
    #}}}

    def test_point_query_raster(self):
        """
        Test querying raster point data.
        """
        # query mocked data
        logging.info("TEST: Query {}point data (raster).".format('' if REAL_CONNECT else 'mocked '))
        # define point query
        # note: test automatic correction for trailing slash in PAIRS base URI
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI[:-1] \
                if len(PAIRS_BASE_URI)>0 and PAIRS_BASE_URI[-1]=='/' else PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
        )
        # submit point query
        testPointQuery.submit()
        # for complience with general PAW query scheme, perform fake poll and download
        testPointQuery.poll_till_finished()
        testPointQuery.download()
        testPointQuery.create_layers()
        # split property string column (3 new columns should be generated for specific example)
        colsBeforeSplit     = len(testPointQuery.vdf.columns)
        testPointQuery.split_property_string_column()
        colsAfterSplit      = len(testPointQuery.vdf.columns)
        self.assertEqual(colsBeforeSplit+3, colsAfterSplit)
        # recalling column splitting function should be invariant now
        colsBeforeSplit     = len(testPointQuery.vdf.columns)
        testPointQuery.split_property_string_column()
        colsAfterSplit      = len(testPointQuery.vdf.columns)
        self.assertEqual(colsBeforeSplit, colsAfterSplit)
        # check vector data frame
        ## number of data points is correct
        logging.info("TEST: Perform vector data frame tests.")
        self.assertEqual(
            5, len(testPointQuery.vdf)
        )
        ## column names agree with data response
        self.assertListEqual(
            sorted(
                list(testPointQuery.querySubmit.json()['data'][0].keys()) \
              + [paw.PAIRS_VECTOR_GEOMETRY_COLUMN_NAME, 'horizon', 'model', 'issuetime']
            ),
            sorted(testPointQuery.vdf.columns),
        )
        ## check (some) data types from response
        self.assertIsInstance(
            testPointQuery.vdf.longitude[0],
            (int, float, numpy.number),
        )
        self.assertIsInstance(
            testPointQuery.vdf.timestamp[0],
            datetime.datetime,
        )
        self.assertIsInstance(
            testPointQuery.vdf.timestamp[0].tzinfo,
            type(pytz.UTC),
        )
        self.assertIsInstance(
            testPointQuery.vdf.geometry[0],
            shapely.geometry.point.Point,
        )
        self.assertIsInstance(
            testPointQuery.vdf.value[0],
            string_type,
        )
        # test deleting query object
        del testPointQuery

    def test_point_query_vector(self):
        """
        Test querying vector point data.
        """
        # query mocked data
        logging.info("TEST: Query {}point data (vector).".format('' if REAL_CONNECT else 'mocked '))
        # define point query
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR, 'point-data-sample-request-vector.json'), 'r')),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
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
            testPointQuery.vdf.timestamp[0].tzinfo,
            type(pytz.UTC),
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

        # test deleting query object
        del testPointQuery

    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (point query)."
    )
    def test_mock_from_point_query(self):
        """
        Checks the real PAIRS point query service against the mock used.
        """
        # get real data
        try:
            self.pairsServerMock.stop()
        except Exception as e:
            # catch not all requests called error
            logging.warning(
                'Stopping the mocked PAIRS server caused (potentially irrelevant) trouble: {}'.format(e)
            )
        testRealRasterResponse = requests.post(
            '{protocol}://{server}{port}{base}{endpoint}'.format(
                protocol    = WEB_PROTOCOL,
                server      = PAIRS_SERVER,
                port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                base        = PAIRS_BASE_URI,
                endpoint    = QUERY_ENDPOINT,
            ),
            json    = json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'), 'r')),
            auth    = PAIRS_CREDENTIALS,
            verify  = VERIFY_SSL,
        )
        testRealVectorResponse = requests.post(
            '{protocol}://{server}{port}{base}{endpoint}'.format(
                protocol    = WEB_PROTOCOL,
                server      = PAIRS_SERVER,
                port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                base        = PAIRS_BASE_URI,
                endpoint    = QUERY_ENDPOINT,
            ),
            json    = json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-vector.json'), 'r')),
            auth    = PAIRS_CREDENTIALS,
            verify  = VERIFY_SSL,
        )
        # make sure the return from the real server was successful
        self.assertEqual(200, testRealRasterResponse.status_code)
        self.assertEqual(200, testRealVectorResponse.status_code)
        # get mock data
        self.pairsServerMock.start()
        testPointQueryRasterMock = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
        )
        testPointQueryRasterMock.submit()
        testPointQueryVectorMock = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-vector.json'))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
        )
        testPointQueryVectorMock.submit()
        # compare data entry keys
        self.assertListEqual(
            sorted(testRealRasterResponse.json()['data'][0].keys()),
            sorted(testPointQueryRasterMock.querySubmit.json()['data'][0].keys()),
        )
        self.assertListEqual(
            sorted(testRealVectorResponse.json()['data'][0].keys()),
            sorted(testPointQueryVectorMock.querySubmit.json()['data'][0].keys()),
        )
        try:
            self.pairsServerMock.stop()
        except Exception as e:
            # catch not all requests called error
            logging.warning(
                'Stopping the mocked PAIRS server caused (potentially irrelevant) trouble: {}'.format(e)
            )

    def test_dataframe_generation(self):
        """
        Tests functions that massage the received data to the *unified* PAW dataframe.
        """
        # query mocked data
        logging.info("TEST: Generation of unified PAW dataframe for point data.")
        testPointQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
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
    PAIRS_BATCH_POINT_ZIP_PATH  = os.path.join(TEST_DATA_DIR, '08_19_2019T10_46_05-1566187200_38765410.zip')
    PAIRS_RASTER_ZIP_PATH       = os.path.join(TEST_DATA_DIR, '12_07_2018T18_39_36-1544202000_23976938.zip')
    PAIRS_RASTER_CSV_ZIP_PATH   = os.path.join(TEST_DATA_DIR, '07_30_2019T19_34_40-1564502400_27280298.zip')
    PAIRS_AGG_RASTER_ZIP_PATH   = os.path.join(TEST_DATA_DIR, '12_07_2018T19_10_50-1544202000_25850895.zip')
    PAIRS_VECTOR_ZIP_PATH       = os.path.join(TEST_DATA_DIR, '04_10_2019T21_45_15-1554912000_35115995.zip')
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
            if (
                payload['spatial']['type'] == 'square' and len(payload['spatial']['coordinates']) == 4
            ) or (
                payload['spatial']['type'] == 'point' and 'batch' in payload and payload['batch']
            ):
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
            elif 'outputType' in payload and payload['outputType'] == 'csv':
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'raster-as-csv-sample-response.json'))
                )
            elif 'batch' in payload and payload['batch']:
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'point-batch-data-sample-response-raster.json'))
                )
            else:
                response_body   = json.load(
                    open(os.path.join(TEST_DATA_DIR,'raster-data-sample-response.json'))
                )
            headers         = {}
            # check header (hard stopper if not correct)
            if not str('Content-Type') in request.headers.keys() \
            or request.headers['Content-Type'] != 'application/json':
                respCode        = 415
                response_body   = {}
                logging.error('Request header incompatible: {}'.format(request.headers))

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
                os.path.basename(cls.PAIRS_RASTER_CSV_ZIP_PATH)
            )[0].split('-')[-1]:
                cls.pollsTillAggFinished -= 1
                if cls.pollsTillAggFinished > 0:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'raster-as-csv-sample-status-running-response.json'))
                    )
                else:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'raster-as-csv-sample-status-finished-response.json'))
                    )
            elif pairsQueryID == os.path.splitext(
                os.path.basename(cls.PAIRS_BATCH_POINT_ZIP_PATH)
            )[0].split('-')[-1]:
                cls.pollsTillAggFinished -= 1
                if cls.pollsTillAggFinished > 0:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'point-batch-data-sample-status-running-response.json'))
                    )
                else:
                    response_body   = json.load(
                        open(os.path.join(TEST_DATA_DIR,'point-batch-data-sample-status-finished-response.json'))
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

        # define upload to IBM COS endpoint
        def cos_upload_init_endpoint(request):
            respCode        = 400
            payload         = json.loads(request.body)
            # perform some tests on payload sent
            if(
                set(('endpoint', 'bucket', 'token')) <= set(payload) \
                and payload['provider']=='ibm'
            ):
                respCode    = 200
            # check header (hard stopper if not correct)
            if not str('Content-Type') in request.headers.keys() \
            or request.headers['Content-Type'] != 'application/json':
                respCode        = 415
                logging.error('Request header incompatible: {}'.format(request.headers))
            # generate response body (depending on various scenarios)
            headers         = {}

            return respCode, headers, None

        # define upload to IBM COS status endpoint
        cls.cosPollCount=2
        def cos_upload_status_endpoint(request):
            respCode        = 400
            # check header (hard stopper if not correct)
            if not str('Content-Type') in request.headers.keys() \
            or request.headers['Content-Type'] != 'application/json':
                respCode        = 415
                logging.error('Request header incompatible: {}'.format(request.headers))
            # generate response body (depending on various scenarios)
            headers   = json.load(
                open(os.path.join(TEST_DATA_DIR,'cos_upload_status_header.json'))
            )
            # count down number of polls performed already
            # define response body by simulating progressive upload
            if cls.cosPollCount>0:
                cls.cosPollCount-=1
            response_body = {
                'id': 79,
                'sizeTotal': 336179,
                'sizeUploaded': int(336179*(1-cls.cosPollCount/2.)),
                'status': 'finished' if cls.cosPollCount==0 else 'uploading',
            }

            return 200, headers, json.dumps(response_body)

        ## add endpoints
        ### query submit
        cls.pairsServerMock.add_callback(
            responses.POST,
            WEB_PROTOCOL+'://'+PAIRS_SERVER+PAIRS_BASE_URI+QUERY_ENDPOINT,
            callback=submit_query_endpoint,
            content_type='application/json',
        )
        ### COS upload endpoints
        cls.pairsServerMock.add_callback(
            responses.POST,
            re.compile(
                r'{}://{}{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, COS_UPLOAD_ENDPOINT, PAIRS_QUERY_ID_REGEX)
            ),
            callback=cos_upload_init_endpoint,
            content_type='application/json',
        )
        cls.pairsServerMock.add_callback(
            responses.GET,
            re.compile(
                r'{}://{}{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, COS_UPLOAD_ENDPOINT, PAIRS_QUERY_ID_REGEX)
            ),
            callback=cos_upload_status_endpoint,
            content_type='application/json',
        )
        ### query downloads and query info
        for queryZIPPath, queryInfoJSONFileName in zip(
            [
                cls.PAIRS_RASTER_ZIP_PATH,
                cls.PAIRS_RASTER_CSV_ZIP_PATH,
                cls.PAIRS_BATCH_POINT_ZIP_PATH,
                cls.PAIRS_AGG_RASTER_ZIP_PATH,
                cls.PAIRS_VECTOR_ZIP_PATH
            ],
            [
                'raster-data-sample-query-json-response.json',
                'raster-as-csv-sample-query-json-response.json',
                'point-batch-data-sample-query-json-response-raster.json',
                'aggregation-data-sample-query-json-response.json',
                'vector-data-sample-query-json-response.json',
            ]
        ):
            queryID = os.path.splitext(
                os.path.basename(queryZIPPath)
            )[0].split('-')[-1]
            # query download
            with open(queryZIPPath, 'rb') as queryData:
                cls.pairsServerMock.add(
                    responses.GET,
                    r'{}://{}{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, DOWNLOAD_ENDPOINT, queryID),
                    body        = queryData.read(),
                    status      = 200,
                    content_type='application/zip',
                    stream=True,
                )
            # query info
            cls.pairsServerMock.add(
                responses.GET,
                r'{}://{}{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, QUERY_INFO_ENDPOINT, queryID),
                body        = json.dumps(
                    json.load(
                        open(os.path.join(TEST_DATA_DIR, queryInfoJSONFileName))
                    )
                ),
                status      = 200,
            )
        ### query status
        cls.pairsServerMock.add_callback(
            responses.GET,
            re.compile(
                r'{}://{}{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, STATUS_ENDPOINT, PAIRS_QUERY_ID_REGEX)
            ),
            callback=poll_query_status_endpoint,
            content_type='application/json',
        )
        ### start the mocked server
        if not REAL_CONNECT:
            cls.pairsServerMock.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.pairsServerMock.stop()
        except:
            pass
    #}}}


    # fold: test ordinary raster queries#{{{
    def raster_query(
        self,
        mode='query',
        inMemory        = False,
        searchExist     = False,
        wrongBaseURI    = False,
        cosUpload       = False,
    ):
        """
        Query raster data in various ways.

        :param mode:            sets the PAIRS query mode:
                                - `query` queries PAIRS
                                - `cached` uses locally cached PAIRS ZIP file
                                - `reload` uses PAIRS query ID
        :type mode:             str
        :param inMemory:        triggers storing files directly in memory for PAIRS query
        :type inMemory:         bool
        :param searchExist:     triggers the search for an existing ZIP file
        :type searchExist:      bool
        :param wrongBaseURI:    remove trailing slash from PAIRS base URI to simulate user typo
        :type wrongBaseURI:     bool
        :param cosUpload:       triggers query result upload to IBM Cloud Object Storage
        :type cosUpload:        bool
        :raises Exception:      if function parameters are incorrectly set
        """
        # check function parameters
        # query mocked data
        logging.info(
            "TEST: Query {}raster data ({}{}).".format(
                '' if REAL_CONNECT else 'mocked ',
                mode,
                ', in-memory' if inMemory else '',
            )
        )
        # define query
        if mode=='query':
            queryDef = json.load(open(os.path.join(TEST_DATA_DIR,'raster-data-sample-request.json')))
        elif mode=='cached':
            if REAL_CONNECT:
                # use ZIP file path set by previous download of real PAIRS connect
                if pytest.realConnectZIPPath is None:
                    raise Exception('Could not record locally cached ZIP file for raster query.')
                queryDef = pytest.realConnectZIPPath
            else:
                queryDef = self.PAIRS_RASTER_ZIP_PATH
        elif mode=='reload':
            if REAL_CONNECT:
                queryDef = pytest.realConnectQueryID
            else:
                queryDef = os.path.splitext(
                    os.path.basename(self.PAIRS_RASTER_ZIP_PATH)
                )[0].split('-')[-1]
        else:
            raise Exception("PAIRS raster query mode '{}' not defined.".format(mode))

        # note: test automatic correction for trailing slash in PAIRS base URI
        testRasterQuery = paw.PAIRSQuery(
            queryDef,
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port                = PAIRS_PORT,
            auth                = PAIRS_CREDENTIALS,
            baseURI             = PAIRS_BASE_URI[:-1] \
                if wrongBaseURI and len(PAIRS_BASE_URI)>0 and PAIRS_BASE_URI[-1]=='/' \
                    else PAIRS_BASE_URI,
            inMemory            = inMemory,
            overwriteExisting   = not searchExist,
            verifySSL           = VERIFY_SSL,
        )
        # check that query got submitted
        testRasterQuery.submit()
        if not mode=='cached' and not searchExist:
            self.assertTrue(testRasterQuery.querySubmit.ok)
        # poll and check that data status is finished
        testRasterQuery.poll_till_finished(printStatus=True)
        if not mode=='cached' and not searchExist:
            self.assertTrue(testRasterQuery.queryStatus.ok)
        # check data download
        testRasterQuery.download(
            cosInfoJSON = {
                "bucket": COS_BUCKET_NAME,
                "token": COS_BUCKET_KEY,
                "provider": "ibm",
                "endpoint": COS_ENDPOINT,
            } if cosUpload else None,
            printStatus = cosUpload,
        )
        # TODO: modify tests as soon as binding COS with fs is an option to read data
        if not cosUpload:
            # check that data acknowledgement was read-in
            self.assertIsNotNone(testRasterQuery.dataAcknowledgeText)
            testRasterQuery.print_data_acknowledgement()
            # for real connect to PAIRS and not in-memory case, get info for other
            # real-world query scenarios
            if not inMemory:
                fullZipFilePath = os.path.join(
                    testRasterQuery.downloadDir,
                    testRasterQuery.zipFilePath,
                )
                # in scenario with real PAIRS connect, store the PAIRS query ZIP path
                # for later reuse on loading from cached data
                if REAL_CONNECT and mode=='query':
                    pytest.realConnectQueryID = testRasterQuery.queryID
                    pytest.realConnectZIPPath = fullZipFilePath
                    logging.info(
                        "Saved local raster file '{}' (query ID: '{}') for testing of loading data from cache.".format(
                            pytest.realConnectZIPPath, pytest.realConnectQueryID
                         )
                    )
                self.assertTrue(
                    os.path.exists(fullZipFilePath)
                )
                logging.info("TEST: Check files downloaded.")
                with zipfile.ZipFile(fullZipFilePath) as zf:
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
                            json.loads(zf.read(rasterFilePath+'.json', pwd=u'').decode('utf-8'))
            # load raster meta data
            logging.info("TEST: Load raster meta data.")
            testRasterQuery.list_layers()
            # check that 'details' of raster data have been successfully loaded by
            # getting the spatial reference information
            self.assertIsInstance(
                list(testRasterQuery.metadata.values())[0]["details"]["spatialRef"],
                string_type
            )
            # check that all data are listed as type raster or vector for CSV output
            self.assertTrue(
                all([
                    meta['layerType'] == 'raster'
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

        # test deleting query object
        del testRasterQuery

    @pytest.mark.run(order=1)
    def test_raster_query_standard(self):
        """
        Test querying raster data.
        """
        self.raster_query()
    @pytest.mark.run(order=1)
    def test_raster_query_with_cos_upload(self):
        """
        Test querying raster data with upload into IBM Cloud Object Storage.
        """
        self.raster_query(cosUpload=True)
    def test_raster_query_standard_user_typo(self):
        """
        Test querying raster data (user typo in PAIRS base URI).
        """
        self.raster_query(wrongBaseURI=True)
    @pytest.mark.run(order=1)
    def test_raster_query_standard_in_memory(self):
        """
        Test querying raster data (in-memory storage).
        """
        self.raster_query(inMemory=True)
    @pytest.mark.run(order=2)
    def test_raster_query_cached(self):
        """
        Test querying raster data from local PAIRS ZIP file.
        """
        self.raster_query(mode='cached')
    @pytest.mark.run(order=2)
    def test_raster_query_cached_search(self):
        """
        Test querying raster data from local PAIRS ZIP file by query JSON definition.
        """
        self.raster_query(searchExist=True)
    @pytest.mark.run(order=2)
    def test_raster_query_cached_in_memory(self):
        """
        Test querying raster data from local PAIRS ZIP file (in-memory storage).
        """
        self.raster_query(mode='cached', inMemory=True)
    @pytest.mark.run(order=2)
    def test_raster_query_reload(self):
        """
        Test reloading previously queried data with PAIRS query ID.
        """
        self.raster_query(mode='reload')
    @pytest.mark.run(order=2)
    def test_raster_query_reload_in_memory(self):
        """
        Test reloading previously queried data with PAIRS query ID (in-memory storage).
        """
        self.raster_query(mode='reload', inMemory=True)
    #}}}

    # fold: test vector queries #{{{
    def vector_query(self, mode='query', inMemory=False, searchExist=False, wrongBaseURI=False, queryType=''):
        """
        Query vector data in various ways.

        :param mode:            sets the PAIRS query mode:
                                - `query` queries PAIRS
                                - `cached` uses locally cached PAIRS ZIP file
                                - `reload` uses PAIRS query ID
        :type mode:             str
        :param inMemory:        triggers storing files directly in memory for PAIRS query
        :type inMemory:         bool
        :param searchExist:     triggers the search for an existing ZIP file
        :type inMemory:         bool
        :param wrongBaseURI:    remove trailing slash from PAIRS base URI to simulate user typo
        :type wrongBaseURI:     bool
        :param queryType:       conceptual type of vector query:
                                    - `fromRaster`: raster data is returned pixel by pixel (center coordinates)
                                    - `batchPoint`: a point query is executed as an offline batch
                                    - `spatAgg`: spatial aggregation is performed on raster data
                                if not specified (default is empty string), an ordinary vector query is performed
        :type queryType:        str
        :raises Exception:      if function parameters are incorrectly set
        """
        # check function parameters
        logging.info(
            "TEST: Query {}vector data ({}{}).".format(
                '' if REAL_CONNECT else 'mocked ',
                mode,
                ', in-memory' if inMemory else '',
            )
        )
        # define query
        if mode=='query':
            if queryType=='fromRaster':
                queryDef = json.load(open(os.path.join(TEST_DATA_DIR,'raster-as-csv-sample-request.json')))
            elif queryType=='batchPoint':
                queryDef = json.load(open(os.path.join(TEST_DATA_DIR,'point-batch-data-sample-request-raster.json')))
            elif queryType=='spatAgg':
                queryDef = json.load(open(os.path.join(TEST_DATA_DIR,'aggregation-data-sample-request.json')))
            else:
                queryDef = json.load(open(os.path.join(TEST_DATA_DIR,'vector-data-sample-request.json')))
        elif mode=='cached':
            if REAL_CONNECT:
                # use ZIP file path set by previous download of real PAIRS connect
                if pytest.realConnectZIPPath is None:
                    raise Exception('Could not record locally cached ZIP file for vector query.')
                queryDef = pytest.realConnectZIPPath
            else:
                if queryType=='fromRaster':
                    queryDef = self.PAIRS_RASTER_CSV_ZIP_PATH
                elif queryType=='batchPoint':
                    queryDef = self.PAIRS_BATCH_POINT_ZIP_PATH
                elif queryType=='spatAgg':
                    queryDef = self.PAIRS_AGG_RASTER_ZIP_PATH
                else:
                    queryDef = self.PAIRS_VECTOR_ZIP_PATH
        elif mode=='reload':
            if REAL_CONNECT:
                queryDef = pytest.realConnectQueryID
            else:
                if queryType=='fromRaster':
                    zipPath = self.PAIRS_RASTER_CSV_ZIP_PATH
                elif queryType=='batchPoint':
                    zipPath = self.PAIRS_BATCH_POINT_ZIP_PATH
                elif queryType=='spatAgg':
                    zipPath = self.PAIRS_AGG_RASTER_ZIP_PATH
                else:
                    zipPath = self.PAIRS_VECTOR_ZIP_PATH
                queryDef = os.path.splitext(
                    os.path.basename(zipPath)
                )[0].split('-')[-1]
        else:
            raise Exception("PAIRS vector query mode '{}' not defined.".format(mode))
        # query mocked data
        testVectorQuery = paw.PAIRSQuery(
            queryDef,
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port                = PAIRS_PORT,
            auth                = PAIRS_CREDENTIALS,
            baseURI             = PAIRS_BASE_URI[:-1] \
                if wrongBaseURI and len(PAIRS_BASE_URI)>0 and PAIRS_BASE_URI[-1]=='/' \
                    else PAIRS_BASE_URI,
            inMemory            = inMemory,
            overwriteExisting   = not searchExist,
            verifySSL           = VERIFY_SSL,
        )
        # check that query got submitted
        testVectorQuery.submit()
        if not mode=='cached' and not searchExist:
            self.assertTrue(testVectorQuery.querySubmit.ok)
        # poll and check that data status is finished
        testVectorQuery.poll_till_finished(printStatus=True)
        if mode not in ['cached', 'reload'] and not searchExist:
            self.assertTrue(testVectorQuery.queryStatus.ok)
        # check that certain files exist
        testVectorQuery.download()
        if not inMemory:
            fullZipFilePath = os.path.join(
                testVectorQuery.downloadDir,
                testVectorQuery.zipFilePath,
            )
            # in scenario with real PAIRS connect, store the PAIRS query ZIP path
            # for later reuse on loading from cached data
            if REAL_CONNECT and mode=='query':
                pytest.realConnectQueryID = testVectorQuery.queryID
                pytest.realConnectZIPPath = fullZipFilePath
                logging.info(
                    "Saved local vector file '{}' (query ID: '{}') for testing of loading data from cache.".format(
                        pytest.realConnectZIPPath, pytest.realConnectQueryID
                     )
                )
            self.assertTrue(
                os.path.exists(fullZipFilePath)
            )
            logging.info("TEST: Check files downloaded.")
            with zipfile.ZipFile(fullZipFilePath) as zf:
                # test the existence of the basic meta file
                # ATTENTION: outputs a warning for now, because not fully implemented
                # by the PAIRS core API
                for fileName in ['output.info', ]:
                    try:
                        self.assertTrue(fileName in zf.namelist())
                    except:
                        logging.error(
                            "Unable to find file 'output.info' for query '{}'".format(testVectorQuery.query)
                        )
                # check that for each aggregated CSV file there exists a corresonding JSON meta file
                # in case of spatial aggregation from raster data
                if queryType=='spatAgg':
                    for rasterFilePath in zf.namelist():
                        # find all PAIRS GeoTiff files
                        if rasterFilePath.endswith('.csv'):
                            # check a corresponding JSON file exists
                            self.assertTrue(
                                rasterFilePath+'.json' in zf.namelist()
                            )
                            # try to temporarily open the JSON file
                            json.loads(zf.read(rasterFilePath+'.json', pwd=u'').decode('utf-8'))
        # load vector meta data
        logging.info("TEST: Load vector meta data.")
        testVectorQuery.list_layers()
        # check that 'details' of raster data have been successfully loaded by
        # getting the spatial reference information for spatial aggregation data
        if queryType=='spatAgg':
            self.assertIsInstance(
                list(testVectorQuery.metadata.values())[0]["details"]["spatialRef"],
                string_type
            )
        # check that all data are listed as type vector
        self.assertTrue(
            all([
                'vector' == meta['layerType']
                for meta in testVectorQuery.metadata.values()
            ])
        )
        logging.info("TEST: Create dataframe from vector data.")
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

        # test deleting query object
        del testVectorQuery

    @pytest.mark.run(order=3)
    def test_vector_query_standard(self):
        """
        Test querying vector data.
        """
        self.vector_query()
    @pytest.mark.run(order=3)
    def test_vector_query_standard_user_typo(self):
        """
        Test querying vector data (user typo in PAIRS base URI).
        """
        self.vector_query(wrongBaseURI=True)
    @pytest.mark.run(order=3)
    def test_vector_query_standard_in_memory(self):
        """
        Test querying vector data (in-memory storage).
        """
        self.vector_query(inMemory=True)
    @pytest.mark.run(order=4)
    def test_vector_query_cached(self):
        """
        Test querying vector data from local PAIRS ZIP file.
        """
        self.vector_query(mode='cached')
    @pytest.mark.run(order=4)
    def test_vector_query_cached_search(self):
        """
        Test querying vector data from local PAIRS ZIP file using query JSON definition.
        """
        self.vector_query(searchExist=True)
    @pytest.mark.run(order=4)
    def test_vector_query_cached_in_memory(self):
        """
        Test querying vector data from local PAIRS ZIP file (in-memory storage).
        """
        self.vector_query(mode='cached', inMemory=True)
    @pytest.mark.run(order=4)
    def test_vector_query_reload(self):
        """
        Test reloading previously queried vector data with PAIRS query ID.
        """
        self.vector_query(mode='reload')
    @pytest.mark.run(order=4)
    def test_vector_query_reload_in_memory(self):
        """
        Test reloading previously queried vector data with PAIRS query ID (in-memory storage).
        """
        self.vector_query(mode='reload', inMemory=True)


    @pytest.mark.run(order=5)
    def test_raster_query_as_csv(self):
        """
        Test querying raster data with CSV return.
        """
        self.vector_query(queryType='fromRaster')
    @pytest.mark.run(order=5)
    def test_raster_query_as_csv_in_memory(self):
        """
        Test querying raster data (in-memory storage) with CSV return.
        """
        self.vector_query(inMemory=True, queryType='fromRaster')
    @pytest.mark.run(order=6)
    def test_raster_query_as_csv_cached_in_memory(self):
        """
        Test querying raster data queried as CSV from local PAIRS ZIP file (in-memory storage).
        """
        self.vector_query(mode='cached', inMemory=True, queryType='fromRaster')
    @pytest.mark.run(order=6)
    def test_raster_query_as_csv_cached_search(self):
        """
        Test querying raster data returned as CSV from local PAIRS ZIP file by query JSON definition.
        """
        self.vector_query(searchExist=True, queryType='fromRaster')
    @pytest.mark.run(order=6)
    def test_raster_query_as_csv_reload(self):
        """
        Test reloading previously queried raster (returned as CSV) data with PAIRS query ID.
        """
        self.vector_query(mode='reload', queryType='fromRaster')


    @pytest.mark.run(order=7)
    def test_point_query_raster_batch(self):
        """
        Test querying raster data using a batch of points.
        """
        self.vector_query(queryType='batchPoint',)
    @pytest.mark.run(order=7)
    def test_point_query_raster_batch_in_memory(self):
        """
        Test querying raster data using a batch of points in memory.
        """
        self.vector_query(inMemory=True, queryType='batchPoint')
    @pytest.mark.run(order=8)
    def test_point_query_raster_batch_cached(self):
        """
        Test querying raster data using a batch of points from local PAIRS ZIP file.
        """
        self.vector_query(mode='cached', queryType='batchPoint')
    @pytest.mark.run(order=8)
    def test_point_query_raster_batch_reload_in_memory(self):
        """
        Test reloading previously queried batch of point data with PAIRS query ID (in-memory storage).
        """
        self.vector_query(mode='reload', inMemory=True, queryType='batchPoint')


    @pytest.mark.run(order=9)
    def test_raster_aggregation_query_standard(self):
        """
        Test querying aggregated raster data.
        """
        self.vector_query(queryType='spatAgg')
    @pytest.mark.run(order=9)
    def test_raster_aggregation_query_standard_in_memory(self):
        """
        Test querying aggregated raster data (in-memory storage).
        """
        self.vector_query(queryType='spatAgg', inMemory=True)

    @pytest.mark.run(order=10)
    def test_raster_aggregation_query_cached(self):
        """
        Test querying aggregated raster data from local PAIRS ZIP file.
        """
        self.vector_query(queryType='spatAgg', mode='cached')
    @pytest.mark.run(order=10)
    def test_raster_aggregation_query_cached_search(self):
        """
        Test querying aggregated raster data from local PAIRS ZIP file using query JSON definition.
        """
        self.vector_query(queryType='spatAgg', searchExist=True)
    @pytest.mark.run(order=10)
    def test_raster_aggregation_query_cached_in_memory(self):
        """
        Test querying aggregated raster data from local PAIRS ZIP file (in-memory).
        """
        self.vector_query(queryType='spatAgg', mode='cached', inMemory=True)
    @pytest.mark.run(order=10)
    def test_raster_aggregation_query_reload(self):
        """
        Test reloading previously queried aggregation data with PAIRS query ID.
        """
        self.vector_query(queryType='spatAgg', mode='reload')
    @pytest.mark.run(order=10)
    def test_raster_aggregation_query_reload_in_memory(self):
        """
        Test reloading previously queried aggregation data with PAIRS query ID (in-memory storage).
        """
        self.vector_query(queryType='spatAgg', mode='reload', inMemory=True)
    #}}}

    # fold: test vector queries #{{{
    # }}}

    # fold: test cached mock data to simulate PAIRS server against real service#{{{
    def compare_mock_vs_real_query(self, queryJSON):
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
            '{protocol}://{server}{port}{base}{endpoint}'.format(
                protocol    = WEB_PROTOCOL,
                server      = PAIRS_SERVER,
                port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                base        = PAIRS_BASE_URI,
                endpoint    = QUERY_ENDPOINT,
            ),
            json    = json.load(open(os.path.join(TEST_DATA_DIR, queryJSON))),
            auth    = PAIRS_CREDENTIALS,
            verify  = VERIFY_SSL,
        )
        self.assertEqual(200, subResp.status_code)
        subResp = subResp.json()
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
                '{protocol}://{server}{port}{base}{endpoint}'.format(
                    protocol    = WEB_PROTOCOL,
                    server      = PAIRS_SERVER,
                    port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                    base        = PAIRS_BASE_URI,
                    endpoint    = STATUS_ENDPOINT+subResp['id'],
                ),
                auth    = PAIRS_CREDENTIALS,
                verify  = VERIFY_SSL,
            )
            self.assertEqual(200, statResp.status_code)
            statResp = statResp.json()
            # check returned stati to exist and be of correct format
            assert set(['id', 'status', 'statusCode']) <= set(statResp.keys())
            self.assertIsInstance(
                statResp['statusCode'],
                int
            )
            if statResp['statusCode'] >= 20:
                break
        # check query result
        downloadResp = requests.get(
            '{protocol}://{server}{port}{base}{endpoint}'.format(
                protocol    = WEB_PROTOCOL,
                server      = PAIRS_SERVER,
                port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                base        = PAIRS_BASE_URI,
                endpoint    = DOWNLOAD_ENDPOINT+subResp['id'],
            ),
            auth    = PAIRS_CREDENTIALS,
            stream  = True,
            verify  = VERIFY_SSL,
        )
        self.assertEqual(200, downloadResp.status_code)
        pairsDataZip = '/tmp/pairs-test-download-{}.zip'.format(subResp['id'])
        with open(pairsDataZip, 'wb') as f:
            for chunk in downloadResp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        # basic test of real data
        self.assertTrue(
            zipfile.is_zipfile(pairsDataZip)
        )
        # get mock data
        self.pairsServerMock.start()
        testMockQuery = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR, queryJSON))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
        )
        testMockQuery.submit()
        testMockQuery.poll_till_finished(printStatus=True)
        testMockQuery.download()
        pairsMockZip = os.path.join(
            testMockQuery.downloadDir,
            testMockQuery.zipFilePath
        )
        # make sure that files in mock are available in real download
        # and that the size of the data and the mock are approximately the same
        logging.info("TEST: Check that all files from the mock exist in the real data queried.")
        with zipfile.ZipFile(pairsMockZip, 'r') as mock, \
             zipfile.ZipFile(pairsDataZip, 'r') as real:
            # generate info dictionaries (case insensitive to names)
            mockInfo = {
                f.filename.lower(): f.file_size
                for f in mock.infolist()
            }
            realInfo = {
                f.filename.lower(): f.file_size
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

    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (raster query)."
    )
    @pytest.mark.run(order=1)
    def test_mock_raster_query(self):
        self.compare_mock_vs_real_query('raster-data-sample-request.json')
    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (vector query)."
    )
    @pytest.mark.run(order=1)
    def test_mock_vector_query(self):
        self.compare_mock_vs_real_query('vector-data-sample-request.json')
    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (raster aggregation query)."
    )
    @pytest.mark.run(order=1)
    def test_mock_raster_aggregation_query(self):
        self.compare_mock_vs_real_query('aggregation-data-sample-request.json')
    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (batch point query)."
    )
    @pytest.mark.run(order=1)
    def test_mock_point_batch_query(self):
        self.compare_mock_vs_real_query('point-batch-data-sample-request-raster.json')
    #}}}
# }}}

# fold: test PAIRS timeseries queries{{{
class TestTimeseriesQuery(unittest.TestCase):
    """
    Test cases for querying timeseries from PAIRS (conceptually quite similar to point queries).
    """
    # fold: setup mocked environment#{{{
    @classmethod
    def setUpClass(cls):
        # define and start PAIRS mock server
        cls.pairsServerMock = responses.RequestsMock()
        cls.responseDataDir = os.path.join(TEST_DATA_DIR, 'timeseries')
        ## define endpoint processing
        def timeseries_data_endpoint(request):
            respCode        = 400
            headers         = {}
            response_body   = {}
            payload         = request.params
            logging.debug('The timeseries payload is: {}'.format(payload))
            # perform some tests on payload sent
            if {'lon', 'lat', 'start', 'end', 'layer'} <= set(payload.keys()):
                # check if dimensions are given to correct layer information:
                if 'dimension' in payload.keys():
                    payload['layer'] += '&dimension='+payload['dimension'].replace('=', '%3D')
                # generate response body
                responseJSONFileName = TIMESERIES_RESPONSE_FILE_SCHEMA.format(
                    lon         = payload['lon'],
                    lat         = payload['lat'],
                    layerID     = payload['layer'],
                    t0          = payload['start'],
                    t1          = payload['end'],
                )
                response_body   = json.load(
                    open(os.path.join(cls.responseDataDir,responseJSONFileName))
                )
                respCode    = 200

            return respCode, headers, json.dumps(response_body)
        ## add endpoint
        cls.pairsServerMock.add_callback(
            responses.GET,
            re.compile(
                '{}://{}{}{}'.format(WEB_PROTOCOL, PAIRS_SERVER, PAIRS_BASE_URI, TIMESERIES_ENDPOINT,)
            ),
            callback=timeseries_data_endpoint,
            # do not use given parameters for URL matching
            match_querystring=False,
        )
        if not REAL_CONNECT:
            cls.pairsServerMock.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.pairsServerMock.stop()
        except:
            pass
    #}}}

    def test_timeseries_query(self):
        """
        Test querying PAIRS for time series (conceptually to point queries).
        """
        # query mocked data
        logging.info("TEST: Query {}timeseries data.".format('' if REAL_CONNECT else 'mocked '))
        # define time series query
        testTimeSeriesQuery = paw.PAIRSTimeSeries(
            json.load(open(os.path.join(self.responseDataDir,'timeseries-sample-request.json'))),
        )
        df = testTimeSeriesQuery.get_dataframe(auth=PAIRS_CREDENTIALS,)
        # TODO: analyze DataFrame according to what is expected with self.assertIn, etc., data types
        # check vector data frame
        del testTimeSeriesQuery


    @unittest.skipIf(
        not REAL_CONNECT,
        "Skip checking mock against real service (point query)."
    )
    def test_mock_from_timeseries_query(self):
        """
        Checks the real PAIRS point query service against the mock used.
        """
        # TODO: adapt code below for timeseries queries
        # get real data
        try:
            self.pairsServerMock.stop()
        except Exception as e:
            # catch not all requests called error
            logging.warning(
                'Stopping the mocked PAIRS server caused (potentially irrelevant) trouble: {}'.format(e)
            )
        testRealRasterResponse = requests.post(
            '{protocol}://{server}{port}{base}{endpoint}'.format(
                protocol    = WEB_PROTOCOL,
                server      = PAIRS_SERVER,
                port        = ':'+str(PAIRS_PORT) if PAIRS_PORT is not None else '',
                base        = PAIRS_BASE_URI,
                endpoint    = QUERY_ENDPOINT,
            ),
            json    = json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'), 'r')),
            auth    = PAIRS_CREDENTIALS,
            verify  = VERIFY_SSL,
        )
        # make sure the return from the real server was successful
        self.assertEqual(200, testRealRasterResponse.status_code)
        # get mock data
        self.pairsServerMock.start()
        testPointQueryRasterMock = paw.PAIRSQuery(
            json.load(open(os.path.join(TEST_DATA_DIR,'point-data-sample-request-raster.json'))),
            WEB_PROTOCOL+'://'+PAIRS_SERVER,
            port        = PAIRS_PORT,
            auth        = PAIRS_CREDENTIALS,
            baseURI     = PAIRS_BASE_URI,
            verifySSL   = VERIFY_SSL,
        )
        testPointQueryRasterMock.submit()
        # compare data entry keys
        self.assertListEqual(
            sorted(testRealRasterResponse.json()['data'][0].keys()),
            sorted(testPointQueryRasterMock.querySubmit.json()['data'][0].keys()),
        )
        try:
            self.pairsServerMock.stop()
        except Exception as e:
            # catch not all requests called error
            logging.warning(
                'Stopping the mocked PAIRS server caused (potentially irrelevant) trouble: {}'.format(e)
            )
#}}}

if __name__ == '__main__':
    unittest.main()
