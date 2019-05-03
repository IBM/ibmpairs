"""
IBM PAIRS RESTful API wrapper: A Python module to access PAIRS's core API to
load data into Python compatible data formats.

Copyright 2019 Physical Analytics, IBM Research All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
"""
# compatibility imports for Python 2 and 3
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

__maintainer__  = "Physical Analytics, TJ Watson Research Center"
__copyright__   = "(c) 2017-2019, IBM Research"
__authors__     = ['Conrad M Albrecht', 'Marcus Freitag']
__email__       = "pairs@us.ibm.com"
__status__      = "Development"
__date__        = "May 2019"

# fold: imports{{{
# basic imports
import os, sys
# compatibility of code with Python 2 and 3
from builtins import dict, range, map, filter, zip, input, chr
from past.builtins import xrange, execfile, intern, apply, cmp
from io import open
from functools import reduce
from imp import reload
from future import standard_library
standard_library.install_aliases()
PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 2:
    string_type = basestring
else:
    string_type = str
# make reading file pointer streams in Python 2 and 3
import codecs
# modules needed
import numpy
import pandas
import PIL.Image
from copy import copy, deepcopy
import errno
import shutil
import zipfile
import tempfile
import glob
from requests.compat import urlparse, urljoin
import requests
import json
HAS_GEOJSON = False
try:
    import geojson
    HAS_GEOJSON = True
except:
    pass
import hashlib
import time
from datetime import datetime, timedelta
import dateutil
import pytz
from shapely.geometry import shape, box, Point
import re
import logging
import itertools
# }}}
# fold: optional packages#{{{
try:
    import geopandas
    HAS_GEOPANDAS=True
except:
    HAS_GEOPANDAS=False
try:
    import coloredlogs
    HAS_COLOREDLOGS=True
except:
    HAS_COLOREDLOGS=False
try:
    from osgeo import gdal
    HAS_GDAL=True
except:
    HAS_GDAL=False
#}}}
# fold: global parameters{{{
## PAIRS base URI for API calles
PAIRS_BASE_URI = '/'
## PAIRS query meta data information file
PAIRS_QUERY_METADATA_FILE_NAME      = 'output.info'
## PAIRS vector JSON file name
PAIRS_VECTOR_CSV_FILE_NAME          = 'Vector_Data_Output.csv'
## PAIRS data acknowledgement file name
PAIRS_DATA_ACK_FILE_NAME            = 'data_acknowledgement.txt'
## default PAIRS password file path
PAIRS_DEFAULT_PASSWORD_FILE_NAME    = 'ibmpairspass.txt'
## PAIRS vector query (Geo)JSON output format names
PAIRS_VECTOR_JSON_TYPE_NAME         = 'json'
PAIRS_VECTOR_GEOJSON_TYPE_NAME      = 'geojson'
PAIRS_VECTOR_CSV_TYPE_NAME          = 'csv'
PAIRS_VECTOR_CSV_QUOTE_CHAR         = "'"
PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME  = 'timestamp'
PAIRS_VECTOR_LONGITUDE_COLUMN_NAME  = 'longitude'
PAIRS_VECTOR_LATITUDE_COLUMN_NAME   = 'latitude'
PAIRS_VECTOR_GEOMETRY_COLUMN_NAME   = 'geometry'
PAIRS_VECTOR_CSV_TIMESTAMP_COL_NUM  = 2
## PAIRS query type names
PAIRS_POINT_QUERY_NAME              = 'point'
PAIRS_VECTOR_QUERY_NAME             = 'vector'
PAIRS_RASTER_QUERY_NAME             = 'raster'
## PAIRS file name extensions
PAIRS_GEOTIFF_FILE_EXTENSION        = '.tiff'
PAIRS_CSV_FILE_EXTENSION            = '.csv'
PAIRS_JSON_FILE_EXTENSION           = '.json'
PAIRS_ZIP_FILE_EXTENSION            = '.zip'
## PAIRS JSON relevant constants
PAIRS_JSON_SPAT_AGG_KEY             = 'spatialAggregation'
## define PAIRS's georeference system
PAIRS_GEOREFERENCE_SYSTEM_NAME      = 'EPSG:4326'
# characters that split the property string of PAIRS vector data
PROPERTY_STRING_SPLIT_CHAR          = ';|:'
PROPERTY_STRING_SPLIT_CHAR1         = ';'
PROPERTY_STRING_SPLIT_CHAR2         = ':'
## basic PAIRS query stati classes
PAIRS_QUERY_RUN_STAT_REG_EX         = re.compile('^(0|1)')
PAIRS_QUERY_FINISH_STAT_REG_EX      = re.compile('^2')
PAIRS_QUERY_ERR_STAT_REG_EX         = re.compile('^(3|4)')
## define default download directory for PAIRS query object if needed
DEFAULT_DOWNLOAD_DIR	            = './downloads'
## PAIRS raster file extension
PAIRS_RASTER_FILE_EXT               = re.compile('.*\.tiff$')
# PAIRS raster file pixel data type classes
PAIRS_RASTER_INT_PIX_TYPE_CLASS     = ('bt','sh', 'in')
PAIRS_RASTER_FLOAT_PIX_TYPE_CLASS   = ('fl','db')
# PAIRS API wrapper specific setttings
PAW_QUERY_NAME_SEPARATOR            = '_'
# load parameters from the command line
PAW_LOG_LEVEL                       = logging.INFO
PAW_LOG_LEVEL_ENV                   = ''
for var in (
    'PAW_LOG_LEVEL',
):
    if var in os.environ:
        exec("{var}_ENV = os.environ['{var}']".format(var=var))
if PAW_LOG_LEVEL_ENV == "DEBUG":
    PAW_LOG_LEVEL = logging.DEBUG
elif PAW_LOG_LEVEL_ENV == "INFO":
    PAW_LOG_LEVEL = logging.INFO
elif PAW_LOG_LEVEL_ENV == "WARNING":
    PAW_LOG_LEVEL = logging.WARNING
elif PAW_LOG_LEVEL_ENV == "ERROR":
    PAW_LOG_LEVEL = logging.ERROR
elif PAW_LOG_LEVEL_ENV == "CRITICAL":
    PAW_LOG_LEVEL = logging.CRITICAL
# }}}
# fold: settings#{{{
## set log level
if HAS_COLOREDLOGS:
    coloredlogs.install(
        level=PAW_LOG_LEVEL,
        fmt='%(levelname)s - %(asctime)s: "%(message)s" [%(funcName)s]',
        level_styles={
            'info':     {'color': 'green'},
            'warning':  {'color': 'yellow'},
            'error':    {'color': 'red'},
            'critical': {'color': 'red', 'bold': True},
        },
        stream=sys.stdout,
    )
else:
    logging.basicConfig(
        format      = '%(levelname)s - %(asctime)s: "%(message)s" [%(funcName)s]',
        level       = logging.INFO,
    )
    logging.StreamHandler(sys.stdout)
#}}}

# fold: misc functions {{{
def get_pairs_api_password(
    server, user,
    passFile=None
):
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
    :rtype:             str
    '''
    # Search for a password file in (a) the current working directory and (b) $HOME
    if passFile is None:
        if os.path.isfile(os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        elif os.path.isfile(os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        else:
            raise ValueError("passFile = None requires existence of a '{}' file in a default location.".format(PAIRS_DEFAULT_PASSWORD_FILE_NAME))

    # Often the value to server is the same as some global variable PAIRS_SERVER
    # That however if later handed to PAIRSQuery objects. The following code allows
    # using PAIRS_SERVER='https://pairs.res.ibm.com' and avoids later use of
    # 'https://'+PAIRS_SERVER
    if server.startswith('https://'):
        server = server[8:]

    passFound = False
    try:
        # parse PAIRS API access password file
        with open(passFile) as f:
            for line in f:
                serverF, userF, password  = re.split(r'(?<!\\):',line.strip())
                password = password.replace('\:', ':')
                if server == serverF and user == userF:
                    passFound = True
                    break
    except (FileNotFoundError, IOError) as e:
        raise e
    except Exception as e:
        raise ValueError('Failed loading PAIRS password from {0}'.format(passFile))

    # return password (if any)
    if passFound:
        return password
    else:
        raise ValueError('Unable to find PAIRS password for {0}@{1} in {2}.'.format(user, server, passFile))
def make_sure_path_exists(dirpath):
    """
    Creates directory if it does not exist yet. (avoids race condition).

    :dirpath:  path to the directory
    """
    try:
        os.makedirs(dirpath)
        logging.info("Directory '{}' created.".format(dirpath))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return

def getQueryHash(query):
    return hashlib.md5(
        json.dumps(query).encode('utf-8')
    ).hexdigest()

def get_aoiSquare(my_polygon):
    """
    Translation from Shapely polygon to PAIRS aoiSquare.

    :my_polygon:    Shapely polygon
    :returns:       PAIRS aoiSquare
    """
    return [my_polygon.bounds[1],     # min. latitude
            my_polygon.bounds[0],     # min. longitude
            my_polygon.bounds[3],     # max. latitude
            my_polygon.bounds[2]]     # max. longitude

def get_polygon(aoiSquare):
    """
    Translation from PAIRS aoiSquare to Shapely polygon.

    :aoiSquare:     PAIRS aoiSquare
    :returns:       Shapely polygon
    """
    return box(aoiSquare[1], aoiSquare[0], aoiSquare[3], aoiSquare[2])

def json_from_qPars(qPars):
    """
    Given "simple" PAIRS query arguments, construct the full PAIRS query JSON load.

    :param qPars:   simple PAIRS query parameters
    :type qPars:    dict
    :returns:       full PAIRS query JSON load required to submit/define a PAIRS query
    :rtype:         dict
    """
    # generate PAIRS API query JSON load from parameters
    query = dict()
    query["layers"] = [
        {
            "type":     qPars['qType'],
            "id":       qPars['layerID']
        }
    ]

    # temporal information
    if isinstance(qPars['startTime'], datetime) and isinstance(qPars['endTime'], datetime):
        startEpochTime  = int(
            (qPars['startTime'] - PAIRSQuery.EPOCH_ZERO).total_seconds()
        ) * 1000
        endEpochTime    = int(
            (qPars['endTime']-PAIRSQuery.EPOCH_ZERO).total_seconds()
        ) * 1000
        query["temporal"] = {
            "intervals":    [ {"start": startEpochTime, "end": endEpochTime} ]
        }
    elif isinstance(qPars['startTime'], str) and isinstance(qPars['endTime'], str):
        query["temporal"] = {
            "intervals":    [ {"start": qPars['startTime'], "end": qPars['endTime']} ]
        }
    else:
        raise Exception(
            'Timestamps in unknown format.'
        )

    # spatial information
    if 'aoiSquare' in qPars:
        query["spatial"]= {"type": "square", "coordinates": qPars['aoiSquare']}
    elif 'aoiPoly' in qPars:
        query["spatial"]= {"type": "poly", "aoi": qPars['aoiPoly']}
    else:
        raise

    # general settings
    ## output type specification
    if 'vectorFormat' in qPars:
        query["outputType"] = qPars['vectorFormat']
    ## do not publish the data (for PAIRS GeoServer)
    query['publish'] = False

    return query
#}}}

# fold: PAIRS query class for managing single queries {{{
class PAIRSQuery(object):
    """
    Representation of a PAIRS query.
    """
    # class wide constants/parameters
    SUBMIT_API_STRING            = 'v2/query'
    STATUS_API_STRING            = 'v2/queryjobs/'
    DOWNLOAD_API_STRING          = 'v2/queryjobs/download/'
    GET_GEOJSON_API_STRING       = 'ws/queryaois/geojson/'
    GET_AOI_INFO_API_STRING      = 'ws/queryaois/aoi/'
    GET_QUERY_INFO               = 'v2/queryhistories/full/queryjob/'
    VECTOR_GEOJSON_DIR_IN_ZIP    = ''
    DOWNLOAD_DIR                 = './downloads'
    PAIRS_JUPYTER_QUERY_BASE_DIR = '.'
    STATUS_POLL_INTERVAL_SEC     = 10
    PAIRS_FILES_TIMESTAMP_SCHEMA2= '%m_%d_%YT%H:%M:%S'
    PAIRS_FILES_TIMESTAMP_SCHEMA = '%m_%d_%YT%H_%M_%S'
    PAIRS_FILES_SPLITTING_CHAR   = '-'
    EPOCH_ZERO                   = datetime(1970,1,1, tzinfo=pytz.utc)
    RASTER_FILE_EXTENSION        = PAIRS_GEOTIFF_FILE_EXTENSION
    VECTOR_FILE_EXTENSION        = PAIRS_CSV_FILE_EXTENSION

    def __init__(
            self, query, pairsHost, auth,
            overwriteExisting       = True,
            deleteDownload          = False,
            downloadDir             = DOWNLOAD_DIR,
            baseURI                 = PAIRS_BASE_URI,
            verifySSL               = True,
            vectorFormat            = None,
        ):
        """
        :param query:               dictionary equivalent to PAIRS JSON load that defines a query or
                                    path that references a ZIP file identified with a PAIRS query
        :type query:                dict or
                                    string
        :param pairsHost:           base URL + scheme of PAIRS host to connect to,
                                    e.g. 'https://pairs.res.ibm.com'
        :type pairsHost:            str
        :param auth:                user name and password as tuple for access to pairsHost
        :type auth:                 (str, str)
        :param overwriteExisting:   destroy locally cached data, if existing, otherwise grab the latest
                                    locally cached data, `latest` is defined by alphanumerical ordering
                                    of the PAIRS query ID
                                    *note:* ignored in case of a file path (string) is provided as query
        :type overwriteExisting:    bool
        :param deleteDownload:      destroy downloaded data with destruction of class instance
        :type overwriteExisting:    bool
        :param downloadDir:         directory where to store downloaded data
                                    note: ignored if the `query` is a string representing the
                                    PAIRS query ZIP directory
        :type downloadDir:          str
        :param baseURI:             PAIRS API base URI to append to the base URL (cf. `pairsHost`)
        :type baseURI:              str
        :param verifySSL:           if set SSL connections are verified
        :type verifySSL:            bool
        :param vectorFormat:        data format of the vector data
        :type vectorFormat:         str
        :raises Exception:          if an invalid URL was specified
                                    if a manually set PAIRS query ZIP directory does not exist
        """
        # update API resources with base URI
        self.SUBMIT_API_STRING          = urljoin(baseURI, self.SUBMIT_API_STRING)
        self.STATUS_API_STRING          = urljoin(baseURI, self.STATUS_API_STRING)
        self.DOWNLOAD_API_STRING        = urljoin(baseURI, self.DOWNLOAD_API_STRING)
        self.GET_GEOJSON_API_STRING     = urljoin(baseURI, self.GET_GEOJSON_API_STRING)
        self.GET_AOI_INFO_API_STRING    = urljoin(baseURI, self.GET_AOI_INFO_API_STRING)
        self.GET_QUERY_INFO             = urljoin(baseURI, self.GET_QUERY_INFO)
        self.verifySSL                  = verifySSL

        # JSON load defining the query
        self.query               = query if isinstance(query, dict) else None
        # ZIP file path storing the PAIRS query result
        # note: directly set by user if the query is of type string
        self.zipFilePath         = query if isinstance(query, string_type) else None
        if self.zipFilePath is not None and not os.path.exists(self.zipFilePath):
            raise Exception(
                "I am sorry, ZIP file '{}' does not exist, canno create PAIRS query object.".format(self.zipFilePath)
            )
        # host serving PAIRS API to connect to
        self.pairsHost           = urlparse(
            '' if pairsHost is None else pairsHost
        )
        if pairsHost is not None and self.pairsHost.scheme not in ['http', 'https']:
            raise Exception('Invalid PAIRS host URL: {}'.format(pairsHost))
        # indicate if query is used in PAIRS Jupyter notebook (spin-up from e.g. MVP)
        self.isPairsJupyter      = False
        # set base URI
        self.baseURI             = baseURI
        # PAIRS API authentication
        self.auth                = auth
        # folder to save query result
        self.downloadDir         = os.path.dirname(self.zipFilePath) if self.zipFilePath is not None else downloadDir
        # overwriting download directory according to ZIP directory information given (if any)
        if self.downloadDir is not None and not os.path.exists(self.downloadDir):
            os.mkdir(self.downloadDir)
            logging.info("Download directory '{}' created.".format(self.downloadDir))
        # keep downloaded data in file
        self.deleteDownload      = deleteDownload
        # associated PAIRS query ID (found in the JSON load)
        self.queryID             = None
        # flags prominently that query data is downloaded and available as files to be loaded
        self.downloaded          = os.path.exists(self.zipFilePath if self.zipFilePath is not None else '')
        # Query parameters to compose the json query
        self.qPars               = None
        # hash of the JSON query
        # (used as subfolder for saving files and to see if corresponding Tiff already exists)
        self.qHash               = getQueryHash(query) if isinstance(self.query, dict) else None
        # overwrite existing files
        self.overwriteExisting   = overwriteExisting if isinstance(self.query, dict) else False
        # Query directory
        self.queryDir            = None
        # query information retrieved via PAIRS API
        self.queryInfo           = None
        # submit of query
        self.querySubmit         = None
        # status of query
        self.queryStatus         = None
        # flag to indicate a failed Zip or GeoTiff generation. Used to re-issue the query
        self.BadDownloadFile     = None
        # general query metadata (based on `output.info`)
        self.metadata            = None
        # dict of in-memory data of the query result indexed by the file's name
        self.data                = dict()
        self.vectorFormat        = vectorFormat
        # data frame of the vector data
        self.vdf                 = None
        # geo data frame with query polygon information
        self.pdf                 = None
        # keyword to indicate translation of timestamp column in the dataframe.
        # data acknowledgement information
        self.dataAcknowledgeText = None
        # if loading data from existing ZIP, get the data acknowledgement
        if isinstance(query, string_type):
            try:
                self.read_data_acknowledgement()
            except Exception as e:
                pass

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __del__(self):
        # Delete the file and folder
        if self.deleteDownload and (not self.queryDir is None):
            if os.path.exists(self.queryDir):
                try:
                    # Remove the folder with all its contents
                    shutil.rmtree(self.queryDir)
                except Exception as e:
                    logging.warning(
                        "Unable to delete query directory '{}': {}.".format(self.queryDir, e)
                    )
                else:
                    logging.info("Query directory '{}' delete.".format(self.queryDir))
            # Remove the zip file
            try:
                os.remove(self.queryDir + PAIRS_ZIP_FILE_EXTENSION)
            except Exception as e:
                logging.warning(
                    "Unable to delete query result ZIP file '{}': {}.".format(self.queryDir, e)
                )
            else:
                logging.info(
                    "Query result ZIP file '{}' deleted: {}.".format(self.queryDir, e)
                )


    def get_query_JSON(self, queryID, reloadData=False):
        """
        Obtain JSON load that defines a PAIRS query assigned a given ID.

        :param queryID:         PAIRS query ID for which to obtain the defining query JSON load
        :type queryID:          str
        :param reloadData:      triggers usage of already retrieved/cached data
        :type reloadData:       bool
        :returns:               PAIRS query defining JSON load
        :rtype:                 dict
        :raises Exception:      if the data cannot be obtained from PAIRS through an API call
                                if cached data do not contain valid JSON load information
        """
        # use cached data (if any)
        if not reloadData and self.queryInfo is not None:
            try:
                return self.queryInfo['apiJson']
            except Exception as e:
                logging.error(
                    "Unable to extract query JSON load from PAIRS query info: '{}'.".format(e)
                )
                raise
        # query data through PAIRS API
        else:
            # construct RESTful endpoint
            queryInfoURL = urljoin(
                urljoin(
                    self.pairsHost.geturl(),
                    self.GET_QUERY_INFO
                ),
                queryID
            )
            # query for information
            try:
                resp = requests.get(
                    queryInfoURL,
                    auth    = self.auth,
                    verify  = self.verifySSL,
                )
                if resp.status_code != 200:
                    raise Exception('Sorry, bad response with code: {}'.format(resp.status_code))
                self.queryInfo = resp.json()
                # convert string to dict
                self.queryInfo['apiJson'] = json.loads(
                    self.queryInfo['apiJson']
                )

                return self.queryInfo['apiJson']
            except Exception as e:
                logging.error(
                    "Unable to fetch query information from PAIRS for ID '{}': '{}'".format(
                        queryID, e
                    )
                )
                raise

    @classmethod
    def from_query_id(
        cls, queryID, pairsHost, auth,
        overwriteExisting   = True,
        downloadDir         = DOWNLOAD_DIR,
        baseURI             = PAIRS_BASE_URI,
        clone4Mod           = False,
        verifySSL           = True,
    ):
        """
        Load data from an existing (previously submitted) query.

        :param queryID:             ID assigned by PAIRS query API (used to poll and download the data)
        :type queryID:              str
        :param pairsHost:           PAIRS host to be used for PAIRS API calls
        :type pairsHost:            str
        :param auth:                credentials ('user', 'password') for authentication with PAIRS
        :type auth:                 tuple
        :param overwriteExisting:   destroy locally cached data, if existing
        :type overwriteExisting:    bool
        :param downloadDir:         base directory where to store the downloaded/cached data
        :type downloadDir:          str
        :param baseURI:             base URI to use for PAIRS API calls
        :type baseURI:              str
        :param clone4Mod:           triggers if the query object will be used to define a new query
        :type clone4Mod:            bool
        :param verifySSL:           if set SSL connections are verified
        :type verifySSL:            bool
        :returns:                   PAIRS API wrapper query object
        :rtype:                     api_wrapper.PAIRSQuery
        :raises Exception:          if there was an error on getting the PAIRS query JSON load
        """
        # set mocked query status
        class MockSubmitResponse():
            def __init__(self, status_code=200):
                self.status_code = status_code
            def json(self):
                return {'id': str(queryID)}

        # instantiate class object
        clsInstance = cls(
            query               = None,
            pairsHost           = pairsHost if not clone4Mod else None,
            baseURI             = baseURI,
            auth                = auth,
            overwriteExisting   = overwriteExisting,
            downloadDir         = downloadDir,
            verifySSL           = verifySSL,
        )
        # clone (parsed) PAIRS host object (if any)
        if clone4Mod:
            clsInstance.pairsHost = pairsHost
        else:
            # set query ID
            clsInstance.queryID     = queryID
            # flag that data is already downloaded
            clsInstance.downloaded  = True
        # obtain and set JSON load for query from PAIRS
        try:
            clsInstance.query = clsInstance.get_query_JSON(queryID)
            # mocked submit response
            if clone4Mod:
                clsInstance.querySubmit = MockSubmitResponse(500)
            else:
                clsInstance.querySubmit = MockSubmitResponse()
        except Exception as e:
            # mocked submit code indicating error with query
            clsInstance.querySubmit = MockSubmitResponse(status_code=500)

        # Check if a subfolder beginning in the queryID exists already
        if not clone4Mod:
            for f in next(os.walk(downloadDir))[1]:
                if f[:len(queryID)] == clsInstance.queryID:
                    # Found subfolder
                    clsInstance.queryDir = os.path.join(downloadDir, f)
                    clsInstance.qHash = f[len(queryID)+1:]

                    clsInstance.list_rasters()
                    break

            if clsInstance.queryDir==None:
                # Exact query not known, so use hashed json None
                clsInstance.qHash = hashlib.md5(json.dumps(None).encode('utf-8')).hexdigest()
                clsInstance.queryDir = os.path.join(
                    downloadDir,
                    queryID + '_' + clsInstance.qHash
                )
        else:
            # reset query hash such that it is recomputed on download time
            clsInstance.qHash = None


        return clsInstance


    @classmethod
    def from_query_result_dir(
        cls, queryDir,
        pairsHost    = None,
        queryID      = None,
        baseURI      = PAIRS_BASE_URI,
    ):
        """
        Generates a PAIRS query object from a native PAIRS query directory.

        *Note*: Used for PAIRS query Jupyter notebook service.

        :param queryDir:        query directory from which to load raster and vector data
        :type queryDir:         str
        :param pairsHost:       PAIRS host to be used for PAIRS API calls
        :type pairsHost:        str
        :param queryID:         PAIRS query ID associated with the data folder queryDir
        :type queryID:          str
        :param baseURI:         base URI to use for PAIRS API calls
        :type baseURI:          str
        :returns:               PAIRS API wrapper query object
        :rtype:                 api_wrapper.PAIRSQuery
        """
        clsInstance = cls(
            query               = None,
            pairsHost           = pairsHost,
            baseURI             = baseURI,
            auth                = None,
            downloadDir         = None,
            overwriteExisting   = False,
        )
        # indicate PAIRS Jupyter notebook usage
        clsInstance.isPairsJupyter = True
        # set the PAIRS query ID for (meta)information retrieval from PAIRS
        clsInstance.queryID = queryID
        # indicate that the data does not need to be downloaded
        clsInstance.downloaded = True
        # set PAIRS query base directory
        clsInstance.PAIRS_JUPYTER_QUERY_BASE_DIR = queryDir
        # load all raster and vector data
        logging.info('Loading query result into memory ...')
        try:
            # try to load all queried layers
            cls.Instance.create_layers()
        except:
            # ... or if that fails default to old raster/vector data import
            try:
                clsInstance.create_rasters()
                logging.info('... raster data ...')
            except Exception as e:
                logging.warning('... no raster data available ...')
            try:
                clsInstance.create_VectorDataFrame()
                logging.info('... vector data ...')
            except Exception as e:
                logging.warning('... no vector data available ...')
        logging.info('... done.')

        return clsInstance

    def get_query_dir_name(self):
        """
        Compute query directory name by setting self.queryDir.

        :raises Exception:  if required information is missing
                            if the query hash cannot be constructed
        """
        # recompute query hash
        try:
            self.qHash = getQueryHash(self.query) if isinstance(self.query, dict) else None
        except:
            errMsg = 'Unable to determine query hash.'
            logging.error(errMsg)
            raise Exception(errMsg)

        # construct query directory name
        if self.downloadDir is not None and self.queryID is not None:
            self.queryDir = os.path.join(
                self.downloadDir,
                self.queryID + '_' + self.qHash
            )
        elif self.zipFilePath is not None:
            self.queryDir = os.path.dirname(self.zipFilePath)
        else:
            msg = 'Information to construct query directory incomplete.'
            logging.warning(msg)
            raise Exception(msg)

    def read_data_acknowledgement(self):
        """
        Extracts data acknowledge statement from PAIRS query result ZIP file.

        :raises Exception:      if no acknowledgement is found
        """
        # attempt to extract only if not set already
        if self.dataAcknowledgeText is None:
            # check that there exists a file with the acknowledgement
            if os.path.exists(self.zipFilePath) and \
               PAIRS_DATA_ACK_FILE_NAME in zipfile.ZipFile(self.zipFilePath).namelist():
                # extract data acknowledgement from PAIRS query ZIP file
                try:
                    with zipfile.ZipFile(self.zipFilePath).open(PAIRS_DATA_ACK_FILE_NAME) as f:
                        self.dataAcknowledgeText = ''.join(codecs.getreader('utf-8')(f))
                    logging.info('Data acknowledgement successfully loaded, print with `self.print_data_acknowledgement()`')
                except Exception as e:
                    msg = 'Unable to read data acknowledgement from PAIRS query result ZIP file: {}'.format(e)
                    logging.error(msg)
                    raise Exception(msg)
            else:
                msg = 'No PAIRS query ZIP file identified, or no acknowledgement in ZIP file found. Did you run `self.download()`, yet?'
                logging.warning(msg)
                raise Exception(msg)
        else:
            logging.info('Data acknowledgement loaded already - print with `self.print_data_acknowledgement()`')

    def print_data_acknowledgement(self):
        """
        Simply print out data acknowledgement statement.

        """
        try:
            self.read_data_acknowledgement()
        except:
            pass
        print("The data acknowledgement for self.data is:\n{}".format(self.dataAcknowledgeText))


    def get_query_params(self):
        """
        Extract and set query parameters from query JSON load to self.qPars.

        :raises Exception:      if the query is too complext to be mapped to the query parameters.
        """
        try:
            # check that the query JSON load exists
            if self.query is None:
                raise Exception()
            # check that there is just a single PAIRS layer to be queried
            if len(self.query['layers']) != 1:
                raise Exception()
            # populate parameters
            layer = self.query['layers'][0]
            self.qPars = dict()
            self.qPars['layerID']       = layer['id']
            self.qPars['qType']         = layer['type']
            # get temporal information
            if layer['temporal'] is not None:
                timeInfo = layer['temporal']['intervals']
            else:
                timeInfo = self.query['temporal']['intervals']
            # check that the query is not a temporal snapshot
            if len(timeInfo) != 1 or timeInfo[0]['snapshot'] is not None:
                raise Exception()
            timeInfo = timeInfo[0]
            self.qPars['startTime']     = datetime.fromtimestamp(
                int(timeInfo['start']) // 1000
            )
            self.qPars['endTime']       = datetime.fromtimestamp(
                int(timeInfo['end']) // 1000
            )
            # get spatial information
            if self.query['spatial']['coordinates'] is not None \
            and self.query['spatial']['type'] == 'square':
                self.qPars['aoiSquare'] = self.query['spatial']['coordinates']
            elif self.query['spatial']['aoi'] is not None \
            and self.query['spatial']['type'] == 'poly':
                self.qPars['aoiPoly']   = int(self.query['spatial']['aoi'])
            else:
                raise Exception()
        except:
            # reset query parameters
            self.qPars = dict()
            raise Exception('Query cannot be mapped to simple query parameters.')

    def clone_by_query_ID(self):
        """
        Clone query object based on its PAIRS query ID.

        :returns:           cloned PAIRS query object
        :rtype:             pairs_python.core.api_wrapper.PAIRSQuery
        :raises Exception:  if there is no query ID available
        """
        try:
            if self.queryID is not None:
                # clone query
                clonedQuery = PAIRSQuery.from_query_id(
                    self.queryID,
                    self.pairsHost,
                    self.auth,
                    overwriteExisting   = self.overwriteExisting,
                    downloadDir         = self.downloadDir \
                                          if self.downloadDir is not None \
                                          else DEFAULT_DOWNLOAD_DIR,
                    baseURI             = self.baseURI,
                    clone4Mod           = True,
                    verifySSL           = self.verifySSL,
                )
                # tweak query output type if parent query is from PAIRS Jupyter notebook
                if self.isPairsJupyter:
                    clonedQuery.query['outputType'] = PAIRS_VECTOR_GEOJSON_TYPE_NAME
                    clonedQuery.vectorFormat        = PAIRS_VECTOR_GEOJSON_TYPE_NAME
                # extract simple query parameters from query JSON load (if any)
                try:
                    clonedQuery.get_query_params()
                except:
                    pass

                return clonedQuery
            else:
                raise Exception('No query ID found.')
        except Exception as e:
            logging.error("Unable to clone query by ID: '{}'".format(e))
            raise

    def recompute_query_JSON_from_qPars(self):
        """
        """
        try:
            # make sure there is any info at all
            if bool(self.qPars):
                self.query = json_from_qPars(self.qPars)
            else:
                raise Exception('No qPars information found.')
        except Exception as e:
            logging.error(
                'Unable to update PAIRS query JSON load from qPars: {}'.format(e)
            )
            raise


    def submit(self):
        """
        Submit query to PAIRS (if defined).

        :raises Exception:  if no query is defined
                            if no local cache is available which is requested to use
                            if no PAIRS query ID can be identified from the return of the PAIRS server
        """
        if self.query is not None:
            # fake submit for using existing cache
            if not self.overwriteExisting:
                logging.warning("Fake submit to PAIRS in order to use (latest) locally cached data.")
                # check whether locally cache exists at all
                try:
                    if isinstance(self.query, dict):
                        self.queryDir = os.path.splitext(
                            os.path.abspath(
                                sorted(
                                    glob.glob(
                                        os.path.join(
                                            self.downloadDir,
                                            '*_{}{}'.format(self.qHash, PAIRS_ZIP_FILE_EXTENSION)
                                        )
                                    )
                                )[0]
                            )
                        )[0]
                        self.queryID = os.path.basename(
                            self.queryDir
                        ).rsplit(PAW_QUERY_NAME_SEPARATOR, 1)[0]
                        self.downloaded = True
                        logging.info("Alright, using cache of PAIRS query with ID: '{}'".format(self.queryID))
                except Exception as e:
                    msg = "I am sorry, you asked for using the local cache, but your query does not match any existing. I am gonna query PAIRS instead: '{}'.".format(e)
                    logging.warning(msg)
                    self.overwriteExisting = True
                    self.queryID = False
            # query PAIRS (if any)
            if self.overwriteExisting:
                # try to submit query to PAIRS
                try:
                    if (self.querySubmit is None) or (self.querySubmit.status_code != 200):
                        self.querySubmit = requests.post(
                            urljoin(
                                self.pairsHost.geturl(),
                                self.SUBMIT_API_STRING
                            ),
                            json   = self.query,
                            auth   = self.auth,
                            verify = self.verifySSL,
                        )
                except Exception as e:
                    raise Exception(
                        'Sorry, I have trouble to submit your query: {}.'.format(e)
                    )
                # obtain (and internally set) query ID (if any)
                try:
                    if self.query['spatial']['type'] != PAIRS_POINT_QUERY_NAME:
                        self.queryID = self.querySubmit.json()['id']
                        logging.info("Alright, PAIRS query sucessfully submitted, the reference ID is: {}".format(self.queryID))
                except Exception as e:
                    logging.error(
                        'Unable to extract query ID from submit JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                    )
                    raise
                # check for point query that immediately returns
                if self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME:
                    # set query status equal to submit status
                    self.queryStatus = self.querySubmit
                    # convert data into (vector) dataframe
                    try:
                        if self.queryStatus.status_code != 200:
                            raise Exception(
                                    "Querying PAIRS resulted in HTML error code '{}': {}.".format(
                                    self.queryStatus.status_code,
                                    self.queryStatus.text
                                )
                            )
                        self.vdf = pandas.DataFrame(
                            self.queryStatus.json()['data']
                        )
                        logging.info('Point data successfully imported into self.vdf')
                        # check for (default) timestamp column
                        if PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME in self.vdf.columns:
                            self.set_timestamp_column(PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME)
                            logging.info("Timestamp column '{}' detected.".format(PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME))
                        else:
                            logging.warning("No timestamp column '{}' detected.".format(PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME))
                        # check for (default) geo-coordinate columns
                        if PAIRS_VECTOR_LONGITUDE_COLUMN_NAME in self.vdf.columns \
                        and PAIRS_VECTOR_LATITUDE_COLUMN_NAME in self.vdf.columns:
                            self.set_lat_lon_columns(
                                PAIRS_VECTOR_LATITUDE_COLUMN_NAME,
                                PAIRS_VECTOR_LONGITUDE_COLUMN_NAME,
                                PAIRS_VECTOR_GEOMETRY_COLUMN_NAME,
                            )
                            logging.info(
                                "Geo-coordinate columns '{}' and '{}' detected.".format(
                                    PAIRS_VECTOR_LONGITUDE_COLUMN_NAME,
                                    PAIRS_VECTOR_LATITUDE_COLUMN_NAME,
                                )
                            )
                        else:
                            logging.warning("No timestamp column '{}' detected.".format(PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME))
                    except Exception as e:
                        logging.error("Unable to load point data into dataframe: '{}'.".format(e))
                        raise Exception()
        elif os.path.exists(self.zipFilePath):
            logging.info("Alright, using user provided PAIRS query ZIP file '{}'".format(self.zipFilePath))
            self.downloaded = True
        else:
            raise Exception(
                'Sorry, no query defined. You are probably using PAIRS Jupyter notebook?'
            )

    def poll(self, passNonSubmitted=False):
        """
        Polls the status a single time and updating self.queryStatus.

        :param passNonSubmitted:    allow the method to pass although no query has been submitted
                                    (this is used for locally cached data)
        :type passNonSubmitted:     bool
        :raises Exception:  if query submit response is unsuccessful,
                            if no query or query ID is defined,
                            if the provided credentials are incorrect
        """
        # skip point query case
        if self.query is None or not self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME:
            # in case the query is a local pointer to a directory, pass polling
            if isinstance(self.query, string_type):
                passNonSubmitted = True
            if passNonSubmitted:
                # Flag to allow poll() method to pass even though the query has not been submitted yet.
                pass
            elif (self.querySubmit is None) and self.queryID is not None and self.downloaded:
                # poll PAIRS API even though we don't have a querySubmit status code.
                # (Used to re-load old GeoTiffs).
                pollURL = urljoin(
                    urljoin(
                        self.pairsHost.geturl(),
                        self.STATUS_API_STRING
                    ),
                    self.queryID
                )
                self.queryStatus = requests.get(
                    pollURL,
                    auth = self.auth,
                    verify = self.verifySSL,
                )
            elif self.queryID is not None and \
                (not self.querySubmit is None) and \
                (self.querySubmit.status_code == 200) and \
                ('data' not in self.querySubmit.json()):
                # poll PAIRS API
                pollURL = urljoin(
                    urljoin(
                        self.pairsHost.geturl(),
                        self.STATUS_API_STRING
                    ),
                    self.queryID
                )
                self.queryStatus = requests.get(
                    pollURL,
                    auth = self.auth,
                    verify = self.verifySSL,
                )
            elif self.queryID is None and self.query is None:
                raise Exception(
                    'No query or query ID defined on record, so no submit possible, i.e. polling does not make sense. You are probably using PAIRS Jupyter notebook?'
                )
            else:
                raise Exception('Query submit response: ' + str(self.querySubmit.status_code))

            # raise an exception if credentials are wrong
            if not passNonSubmitted and self.queryStatus is not None and self.queryStatus.status_code == 401:
                raise Exception('ATTENTION: Provided credentials are incorrect!')

    def poll_till_finished(
            self,
            pollIntSec  = None,
            printStatus = False,
            timeout     = -1,
    ):
        """
        Polls the status until not running anymore.

        :param pollIntSec:      seconds to idle between polls
        :type pollIntSec:       int
        :param printPollStatus: triggers printing the poll status information
        :type printPollStatus:  bool
        :param timeout:         maximum (positive) time in seconds allowed to poll
                                till finished, the default is infinitely polling
        :type timeout:          int
        :raises Exception:      if query submit response is unsuccessful or not existing,
                                if no query or query ID is defined
                                if a user set timeout has been reached
        """
        # skip point query case
        if self.query is None or not self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME:
            # poll in case no locally cached data is used, only
            if not self.overwriteExisting:
                self.poll(passNonSubmitted = True)
            # report case where there is not enough information available to query PAIRS
            elif self.queryID is None and self.query is None:
                raise Exception(
                    'No query or query ID defined on record, so no submit possible, i.e. polling does not make sense. You are probably using PAIRS Jupyter notebook?'
                )
            elif self.querySubmit.status_code is None:
                raise Exception(
                    'Sorry, no query submitted so far. Try: `PAIRSQuery.submit()`.'
                )
            elif self.querySubmit.status_code == 200:
                # record start time of polling
                startTime = time.time()
                # wait for query to finish by constantly polling the API
                while True:
                    # check (user defined) timeout
                    if timeout > 0:
                        if time.time()-startTime > timeout:
                            raise Exception("User defined poll timeout reached.")
                    # poll PAIRS API (if not to use locally cached data)
                    self.poll()
                    # print polled status
                    if printStatus:
                        try:
                            status = self.queryStatus.json()['status']
                            logging.info("Query status is '{}' ...".format(status))
                        except:
                            pass
                    # break if query not running any more
                    try:
                        statusCode = self.queryStatus.json()['statusCode']
                    except Exception as e:
                        logging.error(
                            'Unable to extract query status code from poll JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                        )
                        raise
                    if statusCode is not None and PAIRS_QUERY_RUN_STAT_REG_EX.match(str(statusCode)) is None:
                        break
                    # idle before polling again
                    time.sleep(
                        pollIntSec if pollIntSec is not None \
                        else PAIRSQuery.STATUS_POLL_INTERVAL_SEC
                    )
            else:
                raise Exception('Query submit response: ' + str(self.querySubmit.status_code))

    def download(self):
        """
        Get the data previously queried and save the ZIP file.
        """
        # skip point query case
        if self.query is None or not self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME:
            # one more time poll/try to get query status
            if self.queryStatus is None and self.overwriteExisting:
                self.poll()

            # construct path
            self.get_query_dir_name()
            # note: if the ZIP file path is set already, we deal with the case where
            # there is a user specified PAIRS query directory, already
            if self.zipFilePath is None:
                self.zipFilePath = self.queryDir + PAIRS_ZIP_FILE_EXTENSION

            # check successful query
            if not self.overwriteExisting:
                # check if locally set path for downloaded PAIRS query ZIP file exists
                # to confirm the download
                self.downloaded = os.path.exists(self.zipFilePath)
            else:
                try:
                    statusCode = self.queryStatus.json()['statusCode']
                except Exception as e:
                    logging.error(
                        'Unable to extract query status code from poll JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                    )
                    raise

                if PAIRS_QUERY_FINISH_STAT_REG_EX.match(str(statusCode)) is not None:
                    # TODO: IS THIS STILL A VALID ASSUMPTION?
                    # Save the query ID prominently. This ID also flags that the file
                    # has been downloaded already
                    if not self.downloaded:
                        self.downloaded = True
                        try:
                            self.queryID = self.querySubmit.json()['id']
                        except Exception as e:
                            logging.error(
                                'Unable to extract query ID from submit JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                            )
                            raise

                    if self.overwriteExisting or not os.path.isfile(self.zipFilePath):
                        # stream the query result (ZIP file)
                        with open(self.zipFilePath, 'wb') as f:
                            downloadURL = urljoin(
                                urljoin(
                                    self.pairsHost.geturl(),
                                    self.DOWNLOAD_API_STRING
                                ),
                                self.queryID
                            )

                            downloadResponse = requests.get(
                                downloadURL,
                                auth = self.auth,
                                stream=True,
                                verify = self.verifySSL,
                            )
                            if not downloadResponse.ok:
                                self.BadDownloadFile = True
                                raise Exception('Sorry, downloading file failed.')

                            for block in downloadResponse.iter_content(1024):
                                f.write(block)
                        # test if downloaded ZIP file is readable
                        try:
                            fp = zipfile.ZipFile(self.zipFilePath, 'r')
                        except Exception as e:
                            # flag BadZipfile exception
                            self.BadDownloadFile = True
                            logging.error('Sorry, cannot read downloaded query ZIP file: {}'.format(e))
                        else:
                            fp.close()
                            self.BadDownloadFile = False
                            # Create folder manually in case the zipfile was empty.
                            # ATTENTION: Disabled due to direct reading from ZIP file
                            #make_sure_path_exists(self.queryDir)
                            logging.info(
                                "Here we go, PAIRS query result successfully downloaded as '{}'.".format(self.zipFilePath)
                            )
                    else:
                        logging.error('Aborted download: Zip file already present and overwriteExisting set to False')

                else:
                    msg = "Downloading data not an option (yet), status code is '{}'".format(
                        self.queryStatus.json()['statusCode']
                    )
                    logging.info(msg)
                    raise Exception(msg)

            # read data acknowledgement
            self.read_data_acknowledgement()

            # silently try to list the rasters and vectors
            try:
                self.list_layers()
                pass
            except Exception as e:
                logging.warning("Ah, implicitly running `list_layers()` did not work out: '{}'".format(e))


    def set_geometry_id_column(self, regionName):
        """
        Set geometry column for vector data.

        :param regionName:  pandas dataframe column name of data with region information
        :type regionName:   str
        """
        self.vdf_geom_col_name = regionName

    def set_timestamp_column(self, timeName):
        """
        Set timestamp column for vector data and try to convert it to datetime objects.

        :param timeName:    pandas dataframe column name of data with timestamps
        :type timeName:     str
        :raises Exception:  if it fails to convert timestamps
        """
        # is the data from a PAIRS point query?
        if self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME:
            try:
                self.vdf[timeName] = pandas.to_datetime(
                    self.vdf[timeName],
                    unit='ms',
                    utc=True,
                )
            except:
                raise Exception(
                    "Sorry, failed to convert timestampsof column '{}' to datetime object".format(timeName)
                )
        else:
            # set meta data
            for meta in self.metadata.values():
                meta.update({'timestamp_col_name': timeName})
            if self.query['outputType'] == PAIRS_VECTOR_JSON_TYPE_NAME:
                # convert timestamp column
                try:
                    self.vdf[timeName].astype(str).apply(dateutil.parser.parse)
                except:
                    raise Exception(
                        'Sorry, failed to convert timestamps to datetime objects for JSON ID: '+str(json_id)
                    )
            elif self.query['outputType'] == PAIRS_VECTOR_CSV_TYPE_NAME:
                # convert timestamp column
                try:
                    self.vdf[timeName] = pandas.to_datetime(self.vdf[timeName], utc=True)
                except:
                    raise Exception(
                        'Sorry, failed to convert timestamps to datetime objects for JSON ID: '+str(json_id)
                    )

    def set_lat_lon_columns(self, latColName, lonColName, geomColName):
        """
        Set latitude and longitude columns in order to generate a GeoPandas dataframe.

        :param latColName:  self.vdf Pandas data frame column name for latitude coordinate
        :type latColName:   str
        :param lonColName:  self.vdf Pandas data frame column name for longitude coordinate
        :type lonColName:   str
        :param geomColName: self.vdf GeoPandas data frame column name for point geometry
        :type geomColName:  str
        :raises Exception:  if it fails to generate a GeoPandas dataframe
        """
        try:
            # generate column with shapely point objects
            self.vdf[geomColName] = pandas.Series(
                [
                    Point(lon, lat)
                    for lon, lat in zip(
                        self.vdf[lonColName],
                        self.vdf[latColName]
                    )
                ]
            )
            # convert Pandas dataframe to GeoPandas dataframe (if any)
            if HAS_GEOPANDAS:
                self.vdf = geopandas.GeoDataFrame(
                    self.vdf,
                    crs         = PAIRS_GEOREFERENCE_SYSTEM_NAME,
                    geometry    = geomColName,
                )
            else:
                logging.warning("GeoPandas not available on your system. Cannot convert vector dataframe to GeoPandas dataframe.")
        except:
            raise Exception(
                    "Unable to convert Pandas dataframe to GeoDataframe: '{}'".format(timeName)
            )

    def split_property_string_column(self):
        """
        Split the property string into multiple pandas vector dataframe columns.

        *note:* Applies with CSV vector data import only.
        """
        if self.query['outputType'] == PAIRS_VECTOR_CSV_TYPE_NAME:
            split = pandas.DataFrame(
                self.vdf.PropertyString.apply(
                    lambda x: dict(
                        item.split(PROPERTY_STRING_SPLIT_CHAR2, 1)
                        for item in x.split(PROPERTY_STRING_SPLIT_CHAR1)
                    )
                ).tolist()
            )
            self.vdf = pandas.concat([self.vdf, split], axis=1)

    def query_pairs_polygon(self, polyID):
        """
        Uses PAIRS API to obtain the polygon that corresponds to a given AoI ID.

        :param polyID:  PAIRS AoI ID to query data for
        :type polyID:   int
        :returns:       shapely.geometry.shape of the polygon associated with polyID
                        if there is an error on retrieval, `None` is returned
        """
        try:
            return shape(
                geojson.loads(
                    requests.get(
                        urljoin(
                            urljoin(
                                self.pairsHost.geturl(),
                                self.GET_GEOJSON_API_STRING
                            ),
                            str(polyID)
                        ),
                        auth   = self.auth,
                        verify = self.verifySSL,
                    ).json()
                )
            )
        except Exception as e:
            logging.error(str(e))
            return None

    def query_pairs_polygon_meta(self, polyID):
        """
        Uses PAIRS API to obtain polygon meta-information that corresponds to a given AoI ID.

        :param polyID:  PAIRS AoI ID to query data for
        :type polyID:   int
        :returns:       dict of polygon meta-data associated with polyID
                        if there is an error on retrieval, `None` is returned
        """
        try:
            return requests.get(
                urljoin(
                    urljoin(
                        self.pairsHost.geturl(),
                        self.GET_AOI_INFO_API_STRING
                    ),
                    str(polyID)
                ),
                auth   = self.auth,
                verify = self.verifySSL,
            ).json()['name']
        except Exception as e:
            logging.error(e)
            return None

    def get_vector_polygon_table(self, includeGeometry=False):
        """
        For vector data obtain polygon geometry information from PAIRS.

        :param includeGeometry:     triggers whether to include the geometrys of the polygons or not
        :type includeGeometry:      bool
        :raises Exception:          if there is no polygon geometry specified,
                                    if it fails to retrieve vector geometries or info from PAIRS
        """
        # define vector polygon information dataframe
        if self.pdf is None:
            if HAS_GEOPANDAS:
                self.pdf = geopandas.GeoDataFrame(
                    [],
                    columns=['polygon_id', 'polygon_name'],
                    geometry=[],
                )
            else:
                self.pdf = pandas.DataFrame(
                    [],
                    columns=['polygon_id', 'polygon_name'],
                )
        # get JSON IDs that have geometry information
        try:
            polyColName = self.vdf_geom_col_name
            if polyColName is not None:
                polyIDs = pandas.Series(
                    self.vdf.get(
                        polyColName,
                    ).unique()
                )
        except Exception as e:
            raise Exception(
                'Sorry, no polygon ID columns specified yet, cf. PAIRSQuery.set_geometry_id_column().'
            )
        # remove existing polyIDs
        polyIDs = polyIDs[
            ~polyIDs.isin(self.pdf.polygon_id)
        ]
        # get polygons from PAIRS
        if includeGeometry:
            logging.info(
                'Alright, start fetching {} polygons from PAIRS, stay tuned ...'.format(len(polyIDs))
            )
            polys = [
                self.query_pairs_polygon(polyID)
                for polyID in polyIDs
            ]
            if None in polys:
                logging.warning('Sorry, failed to retrieve (some) vector geometries from PAIRS.')
        # get polygon names/info from PAIRS
        logging.info('Let me get the polygon meta data information for you ...')
        polyNameIDs = [
            [
                polyID,
                self.query_pairs_polygon_meta(polyID)
            ]
            for polyID in polyIDs
        ]
        if None in polyNameIDs:
            logging.warning('Sorry, failed to retrieve (some) vector meta data from PAIRS.')
        # append information to pandas dataframe
        if HAS_GEOPANDAS:
            self.pdf = self.pdf.append(
                geopandas.GeoDataFrame(
                    polyNameIDs,
                    columns=['polygon_id', 'polygon_name'],
                    geometry = polys if includeGeometry else None
                ),
                ignore_index=True,
            )
        else:
            self.pdf = self.pdf.append(
                pandas.DataFrame(
                    polyNameIDs,
                    columns=['polygon_id', 'polygon_name'],
                ),
                ignore_index=True,
            )
            if includeGeometry:
                self.pdf[PAIRS_VECTOR_GEOMETRY_COLUMN_NAME] = pandas.Series(polys)
        logging.info('Here you go, checkout your query object, property `pdf` for the result I assembled for you.')

    def list_layers(self, defaultExtension='', refresh=False):
        """
        Get general metadata information for data of the query.

        :param defaultExtension:    sets default extension for data layer types not specified
        :type defaultExtension:     str
        :param refresh:             triggers the reload of the meta data from scratch
        :type refresh:              bool
        :raises Exception:          if no PAIRS meta data can be found to list layer information
                                    if there is an issue reading the meta data information
        """
        # define path of main PAIRS query meta file
        pairsMetaInfoPath = os.path.join(
            self.PAIRS_JUPYTER_QUERY_BASE_DIR if self.isPairsJupyter else '',
            PAIRS_QUERY_METADATA_FILE_NAME
        )
        # load meta data just once
        if self.metadata is None or refresh:
            # check if required main meta data info exists
            if self.isPairsJupyter and not os.path.exists(pairsMetaInfoPath) \
            or not self.isPairsJupyter \
                and pairsMetaInfoPath not in zipfile.ZipFile(self.zipFilePath).namelist():
                msg = "No PAIRS meta data file '{}' found".format(
                    os.path.basename(pairsMetaInfoPath)
                )
                # ATTENTION: temporarily allow missing `output.info` for pure vector data
                if PAIRS_VECTOR_CSV_FILE_NAME in zipfile.ZipFile(self.zipFilePath).namelist():
                    logging.warning(msg)
                else:
                    logging.error(msg)
                    raise Exception(msg)
            # ATTENTION: temporarily allow missing `output.info` for pure vector data
            if os.path.exists(pairsMetaInfoPath) or \
               pairsMetaInfoPath in zipfile.ZipFile(self.zipFilePath).namelist():
                with open(pairsMetaInfoPath) if self.isPairsJupyter else \
                     zipfile.ZipFile(self.zipFilePath).open(pairsMetaInfoPath) \
                as j:
                    outputJson = json.load(codecs.getreader('utf-8')(j))
                # format meta data as dictionary with key the file name (without extension)
                # ATTENTION: temporary hack for file name and name mismatch
                self.metadata = {
                    fileDict['name'].replace(':', '_'): {
                         k: v for k, v in fileDict.items() if k is not 'name'
                    }
                    for fileDict in outputJson['files']
                }
                logging.info(
                    "PAIRS meta data loaded from '{}'.".format(os.path.basename(pairsMetaInfoPath))
                )
            else:
                self.metadata = {}
                logging.info("Initializing empty meta data dictionary.")
            # load (optional) detailed layer information (based on the existence of
            # a file with same name plus PAIRS file name extension for JSON files)
            for fileName, metaData in self.metadata.items():
                metaPath = os.path.join(
                    self.PAIRS_JUPYTER_QUERY_BASE_DIR if self.isPairsJupyter else '',
                    fileName + (
                        defaultExtension if 'layerType' not in metaData \
                        else self.RASTER_FILE_EXTENSION if metaData['layerType'] == PAIRS_RASTER_QUERY_NAME \
                        else self.VECTOR_FILE_EXTENSION if metaData['layerType'] == PAIRS_VECTOR_QUERY_NAME \
                        else ''
                    ) + PAIRS_JSON_FILE_EXTENSION
                )
                if self.isPairsJupyter and os.path.exists(metaPath) \
                or not self.isPairsJupyter and metaPath in zipfile.ZipFile(self.zipFilePath).namelist():
                    try:
                        with open(metaPath) if self.isPairsJupyter else \
                            zipfile.ZipFile(self.zipFilePath).open(metaPath) \
                        as j:
                            metaData.update(
                                {
                                    'details': json.load(codecs.getreader('utf-8')(j))
                                }
                            )
                        logging.debug(
                            "Detailed meta information for data file name '{}' loaded.".format(metaPath)
                        )
                    except Exception as e:
                        logging.debug(
                            "Unable to read detailed meta information for file '{}': {}.".format(metaPath, e)
                        )
            # note: special treatment of default vector data file name
            if PAIRS_VECTOR_CSV_FILE_NAME in zipfile.ZipFile(self.zipFilePath).namelist():
                self.metadata[os.path.splitext(PAIRS_VECTOR_CSV_FILE_NAME)[0]] = {
                    'layerType': 'vector',
                }

    def create_layer(self, fileName, layerMeta, defaultExtension=''):
        """
        Load layer data such as raster or vector data.

        :param fileName:            the key to identify a data layer, associated with the
                                    corresponding file's name
        :type fileName:             str
        :param layerMeta:           meta information of layer to load
        :type layerMeta:            dict
        :param defaultExtension:    sets default extension for data layer types not specified
        :type defaultExtension:     str
        :raises Exception:          if layer data cannot be loaded from query ZIP file
        """
        # convert timestamp information (if any)
        if 'timestamp' in layerMeta.keys() and not isinstance(layerMeta['timestamp'], datetime):
            layerMeta['timestamp'] = datetime.fromtimestamp(int(layerMeta['timestamp']))
        # load raster data
        # construct file path to load data from
        layerDataPath = os.path.join(
            self.PAIRS_JUPYTER_QUERY_BASE_DIR if self.isPairsJupyter else '',
            fileName + (
                defaultExtension if 'layerType' not in layerMeta \
                else self.RASTER_FILE_EXTENSION if layerMeta['layerType'] == PAIRS_RASTER_QUERY_NAME and PAIRS_JSON_SPAT_AGG_KEY not in layerMeta \
                else self.VECTOR_FILE_EXTENSION if layerMeta['layerType'] == PAIRS_VECTOR_QUERY_NAME or PAIRS_JSON_SPAT_AGG_KEY in layerMeta \
                else ''
            )
        )
        # extract data to temporary file from ZIP (if any)
        if not self.isPairsJupyter:
            # note: it looks like having the delete option causes issues on Windows machines
            # therefore we extract to the standard temporary directory and hope for the OS
            # to clean up, and that sufficient disk space is provided in the temporary directory
            tf = tempfile.NamedTemporaryFile('wb', delete=False,) #dir=self.downloadDir)
            with zipfile.ZipFile(self.zipFilePath) as zf:
                tf.write(zf.read(layerDataPath))
            tf.flush()
            layerDataPath = tf.name
        # get raster data
        # ATTENTION: temporary hack in order to circumvent issue
        if layerMeta['layerType'] == PAIRS_RASTER_QUERY_NAME \
           and not PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
            if HAS_GDAL:
                try:
                    # directly read from data path
                    ds = gdal.Open(layerDataPath)
                    a  = numpy.array(ds.GetRasterBand(1).ReadAsArray(), dtype=numpy.float)
                    ds = None
                except Exception as e:
                    logging.error(
                        "Unable to load '{}' from '{}' into NumPy array using GDAL: {}".format(fileName, self.zipFilePath, e)
                    )
            else:
                try:
                    logging.warning(
                        "GDAL is not available for proper GeoTiff loading, default to standard PIL module to load raster data."
                    )
                    im = PIL.Image.open(layerDataPath)
                    if layerMeta['details']['pixelType'] in PAIRS_RASTER_INT_PIX_TYPE_CLASS:
                        im.mode='I'
                    elif layerMeta['details']['pixelType'] in PAIRS_RASTER_FLOAT_PIX_TYPE_CLASS:
                        im.mode='F'
                    a = numpy.array(im).astype(numpy.float)
                except Exception as e:
                    logging.error(
                        "Unable to load '{}' from '{}' into NumPy array using PIL: {}".format(fileName, self.zipFilePath, e)
                    )
            # close temporary file (if any)
            if not self.isPairsJupyter:
                tf.close()
            # mask no-data value
            a[a==numpy.float(layerMeta['details']['pixelNoDataVal'])] = numpy.nan
            # assign loaded data to object's data dictionary
            self.data[fileName] = a
        # load vector data (note: CSV file format assumed)
        elif layerMeta['layerType'] == PAIRS_VECTOR_QUERY_NAME \
            or PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
            try:
                # spatial aggregation vector data
                if PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
                    self.data[fileName] = pandas.read_csv(
                        layerDataPath,
                        header      = 0,
                        index_col   = False,
                        quotechar   = PAIRS_VECTOR_CSV_QUOTE_CHAR,
                    )
                # *conventional* PAIRS vector data
                else:
                    self.data[fileName] = pandas.read_csv(
                        layerDataPath,
                        header      = 0,
                        index_col   = False,
                        quotechar   = PAIRS_VECTOR_CSV_QUOTE_CHAR,
                        parse_dates = {
                            PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME: [PAIRS_VECTOR_CSV_TIMESTAMP_COL_NUM]
                        },
                    )
            except Exception as e:
                logging.error(
                    "Unable to load '{}' from '{}' into Pandas dataframe: {}".format(fileName, self.zipFilePath, e)
                )
        else:
            msg = "Sorry, I do not know how to load PAIRS query data of type '{}'".format(layerMeta['layerType'])
            logging.error(msg)
            raise Exception(msg)

    def create_layers(self, defaultExtension=''):
        """
        Generate data Python data structures for layers queried.

        :param defaultExtension:    sets default extension for data layer types not specified
        :type defaultExtension:     str
        """
        # Make sure that the layer listing exists
        if self.metadata is None:
            self.list_layers()
        # no raster data availabile?
        if self.metadata is not None:
            for fileName, layerMeta in self.metadata.items():
                self.create_layer(fileName, layerMeta, defaultExtension=defaultExtension)

# }}}
