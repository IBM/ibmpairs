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
__date__        = "August 2019"

# fold: imports{{{
# basic imports
import os, sys
# compatibility of code with Python 2 and 3
from builtins import dict, range, map, filter, zip, input, chr, str
from past.builtins import xrange, execfile, intern, apply, cmp
from io import open
from functools import reduce
from imp import reload
from future import standard_library
standard_library.install_aliases()
try:
    string_type = basestring
except NameError:
    string_type = str
# make reading file pointer streams in Python 2 and 3
import codecs
# modules needed
import numpy
import pandas
import errno
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
import tempfile
# file system abstraction
import fs
from fs.osfs import OSFS
from fs import zipfs
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
    try:
        import PIL.Image
        # adjust maximum size of pixels for image to load (1 TPix)
        PIL.Image.MAX_IMAGE_PIXELS = 10**12
    except Exception as e:
        raise ImportError('Neither GDAL nor PIL could be imported.')
#}}}
# fold: global parameters{{{
## PAIRS base URI for API calles
PAIRS_BASE_URI = u'/'
## PAIRS query meta data information file
PAIRS_QUERY_METADATA_FILE_NAME      = u'output.info'
## PAIRS vector JSON file name
PAIRS_VECTOR_CSV_FILE_NAME          = u'Vector_Data_Output.csv'
## PAIRS data acknowledgement file name
PAIRS_DATA_ACK_FILE_NAME            = u'data_acknowledgement.txt'
## default PAIRS password file path
PAIRS_DEFAULT_PASSWORD_FILE_NAME    = u'ibmpairspass.txt'
## PAIRS vector query (Geo)JSON output format names
PAIRS_VECTOR_JSON_TYPE_NAME         = u'json'
PAIRS_VECTOR_GEOJSON_TYPE_NAME      = u'geojson'
PAIRS_VECTOR_CSV_TYPE_NAME          = u'csv'
PAIRS_VECTOR_CSV_QUOTE_CHAR         = u"'"
PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME  = u'timestamp'
PAIRS_VECTOR_LONGITUDE_COLUMN_NAME  = u'longitude'
PAIRS_VECTOR_LATITUDE_COLUMN_NAME   = u'latitude'
PAIRS_VECTOR_GEOMETRY_COLUMN_NAME   = u'geometry'
PAIRS_VECTOR_CSV_TIMESTAMP_COL_NUM  = 2
## PAIRS meta data constants
PAIRS_META_TIMESTAMP_NAME           = u'timestamp'
## PAIRS query type names
PAIRS_POINT_QUERY_NAME              = u'point'
PAIRS_VECTOR_QUERY_NAME             = u'vector'
PAIRS_RASTER_QUERY_NAME             = u'raster'
## PAIRS file name extensions
PAIRS_GEOTIFF_FILE_EXTENSION        = u'.tiff'
PAIRS_CSV_FILE_EXTENSION            = u'.csv'
PAIRS_JSON_FILE_EXTENSION           = u'.json'
PAIRS_ZIP_FILE_EXTENSION            = u'.zip'
## PAIRS JSON relevant constants
PAIRS_JSON_SPAT_AGG_KEY             = u'spatialAggregation'
## define PAIRS's georeference system
PAIRS_GEOREFERENCE_SYSTEM_NAME      = u'EPSG:4326'
# characters that split the property string of PAIRS vector data
PROPERTY_STRING_SPLIT_CHAR1         = u';'
PROPERTY_STRING_SPLIT_CHAR2         = u':'
PROPERTY_STRING_COL_NAME            = u'PropertyString'
PROPERTY_STRING_COL_NAME_POINT      = u'property'
## basic PAIRS query stati classes
PAIRS_QUERY_RUN_STAT_REG_EX         = re.compile('^(0|1)')
PAIRS_QUERY_FINISH_STAT_REG_EX      = re.compile('^2')
PAIRS_QUERY_ERR_STAT_REG_EX         = re.compile('^(3|4)')
PAIRS_QUERY_DOWNLOADABLE_STAT       = 20
## define default download directory for PAIRS query object if needed
DEFAULT_DOWNLOAD_DIR	            = u'./downloads'
## PAIRS raster file extension
PAIRS_RASTER_FILE_EXT               = re.compile('.*\.tiff$')
# PAIRS raster file pixel data type classes
PAIRS_RASTER_INT_PIX_TYPE_CLASS     = (u'bt', u'sh', u'in')
PAIRS_RASTER_FLOAT_PIX_TYPE_CLASS   = (u'fl', u'db')
# PAIRS API wrapper specific setttings
PAW_QUERY_NAME_SEPARATOR            = '_'
# load parameters from the command line
PAW_LOG_LEVEL                       = logging.INFO
PAW_LOG_LEVEL_ENV                   = u''
for var in (
    u'PAW_LOG_LEVEL',
):
    if var in os.environ:
        exec("{var}_ENV = os.environ['{var}']".format(var=var))
if PAW_LOG_LEVEL_ENV == u"DEBUG":
    PAW_LOG_LEVEL = logging.DEBUG
elif PAW_LOG_LEVEL_ENV == u"INFO":
    PAW_LOG_LEVEL = logging.INFO
elif PAW_LOG_LEVEL_ENV == u"WARNING":
    PAW_LOG_LEVEL = logging.WARNING
elif PAW_LOG_LEVEL_ENV == u"ERROR":
    PAW_LOG_LEVEL = logging.ERROR
elif PAW_LOG_LEVEL_ENV == u"CRITICAL":
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
    passFile=None,
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
    :raises Exception:  if password file does not exist
                        if password was not found
    '''
    # Search for a password file in (a) the current working directory and (b) $HOME
    if passFile is None:
        if os.path.isfile(os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.getcwd(), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        elif os.path.isfile(os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)):
            passFile = os.path.join(os.path.expanduser('~'), PAIRS_DEFAULT_PASSWORD_FILE_NAME)
        else:
            raise ValueError(
                "passFile = None requires existence of a '{}' file in a default location.".format(
                    PAIRS_DEFAULT_PASSWORD_FILE_NAME
                )
            )

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
    except EnvironmentError as e:
        raise e
    except Exception as e:
        raise ValueError('Failed loading PAIRS password from {0}'.format(passFile))

    # return password (if any)
    if passFound:
        return password
    else:
        raise ValueError('Unable to find PAIRS password for {0}@{1} in {2}.'.format(user, server, passFile))

def getQueryHash(query):
    return hashlib.md5(
        json.dumps(query).encode('utf-8')
    ).hexdigest()
#}}}

# fold: PAIRS query class for managing single queries {{{
# set mocked query status
class MockSubmitResponse():
    """
    Helper class for mocking a PAIRS query submit response.

    It is useful to simulate a query submission when reloading a previously submitted
    query based on a given PAIRS query ID.
    """
    def __init__(self, queryID, status_code=200):
        self.status_code = status_code
        self.queryID     = queryID
        self.ok          = True
    def json(self):
        return {u'id': str(self.queryID)}

class PAIRSQuery(object):
    """
    Representation of a PAIRS query.
    """
    # class wide constants/parameters
    SUBMIT_API_STRING            = u'v2/query'
    STATUS_API_STRING            = u'v2/queryjobs/'
    DOWNLOAD_API_STRING          = u'v2/queryjobs/download/'
    COS_UPLOAD_API_STRING        = u'v2/queryjobs/upload/'
    COS_API_ENDPOINT             = u'https://s3.us.cloud-object-storage.appdomain.cloud'
    GET_GEOJSON_API_STRING       = u'ws/queryaois/geojson/'
    GET_AOI_INFO_API_STRING      = u'ws/queryaois/aoi/'
    GET_QUERY_INFO               = u'v2/queryhistories/full/queryjob/'
    VECTOR_GEOJSON_DIR_IN_ZIP    = u''
    DOWNLOAD_DIR                 = u'./downloads'
    PAIRS_JUPYTER_QUERY_BASE_DIR = u'.'
    STATUS_POLL_INTERVAL_SEC     = 10
    PAIRS_FILES_TIMESTAMP_SCHEMA2= '%m_%d_%YT%H:%M:%S'
    PAIRS_FILES_TIMESTAMP_SCHEMA = '%m_%d_%YT%H_%M_%S'
    PAIRS_FILES_SPLITTING_CHAR   = '-'
    EPOCH_ZERO                   = datetime(1970,1,1, tzinfo=pytz.utc)
    RASTER_FILE_EXTENSION        = PAIRS_GEOTIFF_FILE_EXTENSION
    VECTOR_FILE_EXTENSION        = PAIRS_CSV_FILE_EXTENSION

    def __init__(
        self, query, pairsHost, auth,
        port                    = 80,
        overwriteExisting       = True,
        deleteDownload          = False,
        downloadDir             = DOWNLOAD_DIR,
        baseURI                 = PAIRS_BASE_URI,
        verifySSL               = True,
        vectorFormat            = None,
        inMemory                = False,
    ):
        """
        :param query:               dictionary equivalent to PAIRS JSON load that defines a query or
                                    path that references a ZIP file identified with a PAIRS query or
                                    ID of existing (submitted) query
        :type query:                dict or
                                    str
        :param pairsHost:           base URL + scheme of PAIRS host to connect to,
                                    e.g. 'https://pairs.res.ibm.com'
        :type pairsHost:            str
        :param auth:                user name and password as tuple for access to pairsHost
        :type auth:                 (str, str)
        :param port:                port to use for pairsHost
        :type port:                 int
        :param overwriteExisting:   destroy locally cached data, if existing, otherwise grab the latest
                                    locally cached data, `latest` is defined by alphanumerical ordering
                                    of the PAIRS query ID
                                    *note:* ignored in case of a file path (string) is provided as query
        :type overwriteExisting:    bool
        :param deleteDownload:      destroy downloaded data with destruction of class instance
        :type deleteDownload:       bool
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
        :param inMemory:            triggers storing files directly in memory
                                    note: ignored if query is loaded from existing ZIP file
        :type inMemory:             bool
        :raises Exception:          if an invalid URL was specified
                                    if the query defintion is not understood
                                    if a manually set PAIRS query ZIP directory does not exist
        """
        # update API resources with base URI
        self.SUBMIT_API_STRING          = urljoin(baseURI, self.SUBMIT_API_STRING)
        self.STATUS_API_STRING          = urljoin(baseURI, self.STATUS_API_STRING)
        self.DOWNLOAD_API_STRING        = urljoin(baseURI, self.DOWNLOAD_API_STRING)
        self.GET_GEOJSON_API_STRING     = urljoin(baseURI, self.GET_GEOJSON_API_STRING)
        self.GET_AOI_INFO_API_STRING    = urljoin(baseURI, self.GET_AOI_INFO_API_STRING)
        self.GET_QUERY_INFO             = urljoin(baseURI, self.GET_QUERY_INFO)

        # use SSL verification
        self.verifySSL                  = verifySSL
        # PAIRS API authentication
        self.auth                       = auth
        # check and set port for IBM PAIRS core API server
        if isinstance(port, int) and port > 0 and port < 65536:
            self.pairsPort              = port
        else:
            logging.warning("Incorrect port number provided: {}, defaulting to port 80".format(port))
            self.pairsPort              = 80
        # host serving PAIRS API to connect to
        self.pairsHost                  = urlparse(
            u'' if pairsHost is None else \
            '{}:{}'.format(pairsHost, self.pairsPort) if self.pairsPort != 80 else pairsHost
        )
        if pairsHost is not None and self.pairsHost.scheme not in ['http', 'https']:
            raise Exception('Invalid PAIRS host URL: {}'.format(pairsHost))
        # set base URI
        self.baseURI                    = baseURI

        # query information retrieved via PAIRS API
        self.queryInfo                  = None
        # associated PAIRS query ID (found in the JSON load)
        self.queryID                    = None

        # variable for file system object
        self.fs                         = None
        # variable for file system of query result
        self.queryFS                    = None
        # variable for query result data stream
        self._queryStream               = None

        # define query (depending on what information is provided)
        ## assumption on whether or not the query immediately returns
        ## (e.g. for point query without batch processing)
        self._isOnlineQuery             = False
        ## submit of query
        self.querySubmit                = None
        # flag for how to handle downloaded data on object delete
        self.deleteDownload             = deleteDownload
        ## JSON load defining the query
        if isinstance(query, dict):
            # assign query JSON definition
            self.query                  = query
            self.zipFilePath            = None
            # determine the query whether or not the query immediately returns (e.g. for point query)
            self._isOnlineQuery         =  self.query['spatial']['type'] == PAIRS_POINT_QUERY_NAME \
                and (not self.query['batch'] if 'batch' in self.query else True)
            logging.info(
                'PAIRS query JSON initialized{}.'.format(' as online query' if self._isOnlineQuery else '')
            )
        elif isinstance(query, string_type):
            ## ZIP file path storing the PAIRS query result
            # TODO: detect and incorporate case where string represents e.g. COS
            #       to be abstracted by pyfilesystem2, i.e. split apart COS part
            #       from zipFilePath
            if os.path.exists(query):
                self.zipFilePath        = str(query)
                self.query              = None
                # reset in memory user option, since contradicting
                inMemory                = False
                logging.info("Will load PAIRS query data from '{}'.".format(query))
            else:
                ## PAIRS query ID defining the query result
                try:
                    self.query          = self.get_query_JSON(query)
                except Exception as e:
                    self.query          = None
                    logging.warning(
                        "Unable to fetch query definition from PAIRS for query ID '{}': {}".format(query, e)
                    )
                self.queryID            = query
                self.zipFilePath        = None
                self.querySubmit        = MockSubmitResponse(self.queryID)
                logging.info("Will load PAIRS query data from '{}'.".format(query))
        else:
            raise Exception(
                "Query definition of type '{}' not an option.".format(type(query))
            )

        # folder to save query result
        self.downloadDir         = str(
            os.path.dirname(self.zipFilePath) if self.zipFilePath is not None else downloadDir
        )
        # separate ZIP file name from directory (if any)
        # note: the download directory where the ZIP file is located gets abstracted
        # away by self.fs
        if self.zipFilePath is not None:
            self.zipFilePath = os.path.basename(self.zipFilePath)
        # overwriting download directory according to ZIP directory information given (if any)
        if self.downloadDir is not None and not inMemory and not os.path.exists(self.downloadDir):
            os.mkdir(self.downloadDir)
            logging.info("Download directory '{}' created.".format(self.downloadDir))
        # file system for query storage
        if self.fs is None:
            try:
                if inMemory:
                    # create in-memory file system
                    self.fs = fs.open_fs(u'mem://')
                    # ignore user set download directory
                    self.downloadDir=u''
                else:
                    self.fs = fs.open_fs(self.downloadDir)
            except Exception as e:
                raise Exception(
                    "Unable to initialize download directory '{}': {}".format(self.downloadDir, e)
                )
        # try to open the ZIP file (if any)
        if self.zipFilePath is not None:
            try:
                self._queryStream   = self.fs.open(self.zipFilePath, 'rb')
                self.queryFS        = zipfs.ZipFS(self._queryStream, write=False)
                self.queryFS.listdir(u'')
            except Exception as e:
                raise Exception('Hm, cannot load data from ZIP file: {}'.format(e))
            # flags prominently that query data is downloaded and available as files to be loaded
            self.downloaded = True
        else:
            # flag data is not downloaded, yet
            self.downloaded = False
        # hash of the JSON query
        # (used as subfolder for saving files and to see if corresponding Tiff already exists)
        self.qHash               = getQueryHash(query if isinstance(self.query, dict) else {})
        # overwrite existing files
        self.overwriteExisting   = overwriteExisting if (
            isinstance(self.query, dict) or isinstance(self.querySubmit, MockSubmitResponse)
        ) else False
        # Query directory
        self.queryDir            = None
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
        if isinstance(self.fs, fs.memoryfs.MemoryFS):
            logging.info('Just FYI: Local file system is in memory - no data saved on local disk.')

    def __del__(self):
        # Delete the file and folder
        if self.deleteDownload and (not self.queryDir is None):
            if self.fs.exists(self.queryDir):
                try:
                    # Remove the folder with all its contents
                    self.fs.removetree(self.queryDir)
                except Exception as e:
                    logging.warning(
                        "Unable to delete query directory '{}': {}.".format(self.queryDir, e)
                    )
                else:
                    logging.info("Query directory '{}' delete.".format(self.queryDir))
            # Remove the zip file
            try:
                self.fs.remove(self.queryDir + PAIRS_ZIP_FILE_EXTENSION)
            except Exception as e:
                logging.warning(
                    "Unable to delete query result ZIP file '{}': {}.".format(self.queryDir, e)
                )
            else:
                logging.info(
                    "Query result ZIP file '{}' deleted.".format(self.queryDir)
                )
        # decouple from file system
        try:
            if self.queryFS is not None: self.queryFS.close()
            if self._queryStream is not None: self._queryStream.close()
            if self.fs is not None: self.fs.close()
        except Exception as e:
            logging.error('Cannot properly close file system handlers: {}'.format(e))


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
        # indicate that the data does not need to be downloaded
        clsInstance.downloaded  = True
        # set PAIRS query base directory
        # note: incorporates a hack due to a bug in the fs Python module (on parsing)
        clsInstance.queryFS     = OSFS(queryDir)
        # load all raster and vector data
        logging.info('Loading query result into memory ...')
        # load all queried layers
        clsInstance.create_layers()
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
            self.qHash = getQueryHash(self.query if isinstance(self.query, dict) else {})
        except:
            errMsg = u'Unable to determine query hash.'
            logging.error(errMsg)
            raise Exception(errMsg)

        # construct query directory name
        # note: download directory abstracted away by self.fs
        if self.queryID is not None:
            self.queryDir = str(
                    self.queryID + '_' + self.qHash
            )
        elif self.zipFilePath is not None:
            self.queryDir = str(os.path.dirname(self.zipFilePath))
        else:
            msg = u'Information to construct query directory incomplete.'
            logging.warning(msg)
            raise Exception(msg)

    def read_data_acknowledgement(self):
        """
        Extracts data acknowledge statement from PAIRS query result ZIP file.

        :raises Exception:      if no acknowledgement is found
        """
        # attempt to extract only if not set already
        if self.dataAcknowledgeText is None and self.queryFS is not None:
            # check that there exists a file with the acknowledgement
            if self.fs.exists(self.zipFilePath) and \
               PAIRS_DATA_ACK_FILE_NAME in self.queryFS.listdir(u''):
                # extract data acknowledgement from PAIRS query ZIP file
                try:
                    with self.queryFS.open(PAIRS_DATA_ACK_FILE_NAME, 'rb') as f:
                        self.dataAcknowledgeText = ''.join(codecs.getreader('utf-8')(f))
                    logging.info('Data acknowledgement successfully loaded, print with `self.print_data_acknowledgement()`')
                except Exception as e:
                    msg = u'Unable to read data acknowledgement from PAIRS query result ZIP file: {}'.format(e)
                    logging.error(msg)
                    raise Exception(msg)
            else:
                msg = u'No PAIRS query ZIP file identified, or no acknowledgement in ZIP file found. Did you run `self.download()`, yet?'
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
                        self.queryDir = str(
                            os.path.splitext(
                                os.path.abspath(
                                    sorted(
                                        [
                                            g.path
                                            for g in self.fs.glob(
                                                os.path.join(
                                                    '*_{}{}'.format(
                                                        self.qHash,
                                                        PAIRS_ZIP_FILE_EXTENSION
                                                    )
                                                )
                                            )
                                        ]
                                    )[0]
                                )
                            )[0]
                        )
                        self.queryID = str(
                            os.path.basename(
                                self.queryDir
                            ).rsplit(PAW_QUERY_NAME_SEPARATOR, 1)[0]
                        )
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
                            data    = json.dumps(self.query),
                            headers = {'Content-Type': 'application/json'},
                            auth    = self.auth,
                            verify  = self.verifySSL,
                        )
                except Exception as e:
                    raise Exception(
                        'Sorry, I have trouble to submit your query: {}.'.format(e)
                    )
                # check that submission return is proper JSON
                try:
                    _ = self.querySubmit.json()
                except Exception as e:
                    logging.error(
                        'Unable to extract query ID from submit JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                    )
                    logging.error(
                        "Maybe your query definition is not right? Here is the PAIRS server response:\n{}".format(self.querySubmit.text)
                    )
                    raise

                # obtain (and internally set) query ID, or ...
                if not self._isOnlineQuery:
                    self.queryID = self.querySubmit.json()['id']
                    logging.info("Query successfully submitted, reference ID: {}".format(self.queryID))
                # ... handle online (point) query that immediately returns
                else:
                    # set query status equal to submit status
                    self.queryStatus = self.querySubmit
                    # convert data into (vector) dataframe
                    # catch empty return
                    if self.queryStatus.json() is None:
                        logging.warning('No point data available to load/returned.')
                    else:
                        try:
                            if self.queryStatus.status_code != 200:
                                raise Exception(
                                        "Querying PAIRS resulted in HTML error code '{}': {}.".format(
                                        self.queryStatus.status_code,
                                        self.queryStatus.text,
                                    )
                                )
                            else:
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
                                logging.warning(
                                    "No geo-coordinate columns '{}' detected.".format(
                                        [PAIRS_VECTOR_LONGITUDE_COLUMN_NAME, PAIRS_VECTOR_LATITUDE_COLUMN_NAME]
                                    )
                                )
                        except Exception as e:
                            logging.error("Unable to load point data into dataframe: '{}'.".format(e))
                            raise
        # case of PAIRS cached query (previously run)
        elif isinstance(self.querySubmit, MockSubmitResponse):
            logging.info(
                "Alright, using remotely cached PAIRS query with ID '{}'.".format(self.queryID)
            )
        # case of locally cached PAIRS query ZIP directory
        elif self.fs.exists(self.zipFilePath):
            logging.info(
                "Alright, using locally cached PAIRS query ZIP file '{}'.".format(self.zipFilePath)
            )
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
        # skip online (point) query
        if isinstance(self.querySubmit, MockSubmitResponse) or self.query is None \
        or not self._isOnlineQuery:
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
                    auth    = self.auth,
                    verify  = self.verifySSL,
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
                    auth    = self.auth,
                    verify  = self.verifySSL,
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
        :type pollIntSec:       float
        :param printStatus:     triggers printing the poll status information
        :type printStatus:      bool
        :param timeout:         maximum (positive) time in seconds allowed to poll
                                till finished, the default is infinitely polling
        :type timeout:          int
        :raises Exception:      if query submit response is unsuccessful or not existing,
                                if no query or query ID is defined
                                if a user set timeout has been reached
        """
        # skip online (point) query case
        if isinstance(self.querySubmit, MockSubmitResponse) or self.query is None \
        or not self._isOnlineQuery:
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
                            progressPercent = float(self.queryStatus.json()['exPercent'])
                            if progressPercent > 0:
                                percMsg = ' ({}%)'.format(progressPercent)
                            else:
                                percMsg = u''
                            logging.info("Query status is '{}'{}.".format(status, percMsg))
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

    def download(self, cosInfo=None):
        """
        Get the data previously queried and save the ZIP file.

        :param cosInfo:     tuple with IBM Cloud Object Storage bucket name and access token
                            if set, the query result is not locally downloaded, but
                            published in your IBM cloud (this is a useful feature
                            in combination with IBM Watson Studio notebooks)
        :type cosInfo:      (str, str)
        """
        # skip online (point) query case (including reload query and cached query)
        if isinstance(self.querySubmit, MockSubmitResponse) or self.query is None \
        or not self._isOnlineQuery:
            # one more time poll/try to get query status
            if self.queryStatus is None and self.overwriteExisting:
                self.poll()

            # construct path
            self.get_query_dir_name()
            # note: if the ZIP file path is set already, we deal with the case where
            # there is a user specified PAIRS query directory, already
            if self.zipFilePath is None:
                self.zipFilePath = str(self.queryDir + PAIRS_ZIP_FILE_EXTENSION)

            # check successful query
            if not self.overwriteExisting:
                # check if locally set path for downloaded PAIRS query ZIP file exists
                # to confirm the download
                self.downloaded = self.fs.exists(self.zipFilePath)
            else:
                try:
                    respJson    = self.queryStatus.json()
                    statusCode  = respJson['statusCode']
                    statusMsg   = str(respJson['status'])
                except Exception as e:
                    logging.error(
                        'Unable to extract query status code from poll JSON return - are you using the correct base URI ({})?'.format(self.baseURI)
                    )
                    raise

                # check that the data can be really downloaded
                if int(statusCode) == PAIRS_QUERY_DOWNLOADABLE_STAT:
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
                    # note on streaming into memory
                    if isinstance(self.fs, fs.memoryfs.MemoryFS):
                        logging.warning(
                            'Be aware: As directed, downloading query result directly into memory!'
                        )

                    if self.overwriteExisting or not self.fs.isfile(self.zipFilePath):
                        # stream the query result (ZIP file)
                        if cosInfo is None:
                            with self.fs.open(self.zipFilePath, 'wb') as f:
                                downloadURL = urljoin(
                                    urljoin(
                                        self.pairsHost.geturl(),
                                        self.DOWNLOAD_API_STRING
                                    ),
                                    self.queryID
                                )

                                downloadResponse = requests.get(
                                    downloadURL,
                                    auth    = self.auth,
                                    stream  = True,
                                    verify  = self.verifySSL,
                                )
                                if not downloadResponse.ok:
                                    self.BadDownloadFile = True
                                    raise Exception('Sorry, downloading file failed.')

                                for block in downloadResponse.iter_content(1024):
                                    f.write(block)
                        # publish query result to COS
                        elif isinstance(cosInfo, tuple) and len(cosInfo)==2:
                            try:
                                resp = requests.post(
                                    urljoin(
                                        urljoin(
                                            self.pairsHost.geturl(),
                                            self.COS_UPLOAD_API_STRING
                                        ),
                                        str(self.queryID)
                                    ),
                                    data   = json.dumps(
                                        {
                                            'provider': 'ibm',
                                            'endpoint': self.COS_API_ENDPOINT,
                                            'bucket':   str(cosInfo[0]),
                                            'token':    str(cosInfo[1]),
                                        }
                                    ),
                                    headers = {'Content-Type': 'application/json'},
                                    auth    = self.auth,
                                    verify  = self.verifySSL,
                                )
                                if resp.status_code == 200:
                                    logging.info('Upload of query result to IBM COS initialized.')
                                else:
                                    raise Exception(
                                        'PAIRS failed publishing query result to COS: {}'.format(resp.text)
                                    )
                            except Exception as e:
                                raise Exception(
                                        'Sorry, I have trouble getting your query result to Cloud Object storage: {}.'.format(e)
                                )
                        else:
                            msg = u'Sorry, I do not know what to do based on the `cosInfo` you provided.'
                            logging.error(msg)
                            raise Exception(msg)
                    else:
                        logging.error('Aborted download: Zip file already present and overwriteExisting set to False')
                else:
                    if PAIRS_QUERY_ERR_STAT_REG_EX.match(str(statusCode)):
                        msg = "I am sorry, IBM PAIRS query failed, status code: '{}' ({})".format(statusCode, statusMsg)
                    elif PAIRS_QUERY_RUN_STAT_REG_EX.match(str(statusCode)):
                        msg = "Hold on, please, downloading data not an option yet, status code: '{}' ({})".format(statusCode, statusMsg)
                    elif PAIRS_QUERY_FINISH_STAT_REG_EX.match(str(statusCode)):
                        msg = "Bummer, the PAIRS query finished, but you'll never be able to download anything, status code: '{}' ({})".format(statusCode, statusMsg)
                    else:
                        msg = "Hm, not sure what is going on, status code from IBM PAIRS is '{}' ({})".format(statusCode, statusMsg)
                    logging.info(msg)
                    raise Exception(msg)

            # test if downloaded ZIP file is readable
            try:
                self._queryStream   = self.fs.open(self.zipFilePath, 'rb')
                self.queryFS        = zipfs.ZipFS(self._queryStream, write=False)
                self.queryFS.listdir(u'')
            except Exception as e:
                # flag BadZipfile exception
                self.BadDownloadFile = True
                logging.error('Sorry, cannot read downloaded query ZIP file: {}'.format(e))
            else:
                self.BadDownloadFile = False
                logging.info(
                    "Here we go, PAIRS query result successfully downloaded as '{}'.".format(self.zipFilePath)
                )

            # try to read data acknowledgement
            try:
                self.read_data_acknowledgement()
            except:
                pass

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
        # is the data from an online (point) query?
        if self._isOnlineQuery:
            try:
                if self.vdf is not None and isinstance(self.vdf, pandas.DataFrame) \
                and self.vdf[timeName].dtype in (numpy.float, numpy.int):
                    self.vdf[timeName] = self.vdf[timeName].apply(
                        lambda t: datetime.fromtimestamp(
                            t/1e3, tz=pytz.UTC
                        )
                    )
            except Exception as e:
                raise Exception(
                    "Sorry, failed to convert timestamps of column '{}' to datetime object: {}".format(timeName, e)
                )
        else:
            # set meta data
            for meta in self.metadata.values():
                meta.update({'timestamp_col_name': timeName})
            if self.query['outputType'] == PAIRS_VECTOR_JSON_TYPE_NAME:
                # convert timestamp column
                try:
                    self.vdf[timeName].astype(str).apply(dateutil.parser.parse)
                    self.vdf[timeName].apply(lambda ts: pytz.UTC.localize(ts) if ts.tzinfo is None else ts)
                except Exception as e:
                    raise Exception(
                        'Sorry, failed to convert timestamps to datetime objects: {}'.format(e)
                    )
            elif self.query['outputType'] == PAIRS_VECTOR_CSV_TYPE_NAME:
                # convert timestamp column
                try:
                    if self.vdf is not None and isinstance(self.vdf, pandas.DataFrame) \
                    and self.vdf[timeName].dtype in (numpy.float, numpy.int):
                        self.vdf[timeName] = self.vdf[timeName].apply(
                            lambda t: datetime.fromtimestamp(t, tz=pytz.UTC)
                        )
                except Exception as e:
                    raise Exception(
                        "Sorry, failed to convert timestamps to datetime objects: {}".format(e)
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
        except Exception as e:
            raise Exception(
                "Unable to convert Pandas dataframe to GeoDataframe: '{}'".format(e)
            )

    def split_property_string_column(self):
        """
        Split the property string into multiple pandas vector dataframe columns.

        *note:* Applies with CSV vector data import only.

        :raises Exception:  if existing columns clash with the generation of property
                            columns produced here
        """
        # determine if there is property columns to operate on (if any)
        propertyCols = list(
            set(
                self.vdf.columns.intersection(
                    [PROPERTY_STRING_COL_NAME, PROPERTY_STRING_COL_NAME_POINT]
                )
            )
        )
        if len(propertyCols)>0:
            # split the property column (assumption: there is just one)
            split = pandas.DataFrame(
                self.vdf[propertyCols[0]].apply(
                    lambda x: dict(
                        item.split(PROPERTY_STRING_SPLIT_CHAR2, 1)
                        for item in x.split(PROPERTY_STRING_SPLIT_CHAR1)
                    ) if isinstance(x, string_type) else {}
                ).tolist()
            )
            # check that there was no previous call of this function or there
            # is no column existing with the name of any property split
            doubledCols = list(set(self.vdf.columns.intersection(split.columns)))
            if len(doubledCols) == 0:
                # concatenate property columns
                self.vdf = pandas.concat([self.vdf, split], axis=1)
            # most likely this function ran before
            elif len(doubledCols) == len(split.columns):
                logging.warning('FYI: Looks like you ran this functon before?')
                for col in doubledCols:
                    self.vdf[col] = split[col]
            # most likely there is a clash between existing columns not previously
            # generated by this function
            else:
                msg = "Oops, it looks like the columns {} exist, sorry, won't overwrite.".format(doubledCols)
                logging.error(msg)
                raise Exception(msg)

    def query_pairs_polygon(self, polyID):
        """
        Uses PAIRS API to obtain the polygon that corresponds to a given AoI ID.

        :param polyID:  PAIRS AoI ID to query data for
        :type polyID:   int
        :returns:       shapely.geometry.shape of the polygon associated with polyID
                        if there is an error on retrieval, `None` is returned
        """
        try:
            if not HAS_GEOJSON:
                raise Exception('Sorry, you have not installed the GeoJSON Python module (e.g. via `pip install geojson`)')
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

    def list_layers(self, defaultExtension=u'', refresh=False):
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
        pairsMetaInfoPath = PAIRS_QUERY_METADATA_FILE_NAME
        # load meta data just once (and if no point query)
        if (self.metadata is None or refresh) and (
            self.queryStatus is not self.querySubmit if self.queryStatus is not None else True
        ):
            # check if required main meta data info exists
            if pairsMetaInfoPath not in self.queryFS.listdir(u''):
                msg = "No PAIRS meta data file '{}' found".format(
                    os.path.basename(pairsMetaInfoPath)
                )
                # ATTENTION: temporarily allow missing `output.info` for pure vector data
                if PAIRS_VECTOR_CSV_FILE_NAME in self.queryFS.listdir(u''):
                    logging.warning(msg)
                else:
                    logging.error(msg)
                    raise Exception(msg)
            # ATTENTION: temporarily allow missing `output.info` for pure vector data
            if pairsMetaInfoPath in self.queryFS.listdir(u''):
                with self.queryFS.open(pairsMetaInfoPath, 'rb') as j:
                    outputJson = json.load(codecs.getreader('utf-8')(j))
                # format meta data as dictionary with key the file name (without extension)
                # ATTENTION: temporary hack for file name and name mismatch
                self.metadata = {
                    fileDict['name'].replace(':', '_'): {
                         k: v for k, v in fileDict.items() if k != 'name'
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
                metaPath = fileName + (
                    defaultExtension if 'layerType' not in metaData \
                    else self.RASTER_FILE_EXTENSION if metaData['layerType'] == PAIRS_RASTER_QUERY_NAME \
                    else self.VECTOR_FILE_EXTENSION if metaData['layerType'] == PAIRS_VECTOR_QUERY_NAME \
                    else u''
                ) + PAIRS_JSON_FILE_EXTENSION
                if metaPath in self.queryFS.listdir(u''):
                    try:
                        with self.queryFS.open(metaPath, 'rb') as j:
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
            if PAIRS_VECTOR_CSV_FILE_NAME in self.queryFS.listdir(u''):
                self.metadata[os.path.splitext(PAIRS_VECTOR_CSV_FILE_NAME)[0]] = {
                    'layerType': 'vector',
                }

    def create_layer(self, fileName, layerMeta, defaultExtension=u''):
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
        if PAIRS_META_TIMESTAMP_NAME in layerMeta.keys() \
        and not isinstance(layerMeta[PAIRS_META_TIMESTAMP_NAME], datetime):
            layerMeta[PAIRS_META_TIMESTAMP_NAME] = datetime.fromtimestamp(
                int(layerMeta[PAIRS_META_TIMESTAMP_NAME])/1000.,
                tz=pytz.UTC
            )
        # load raster data
        # construct file path to load data from
        layerDataPath = fileName + (
            defaultExtension if 'layerType' not in layerMeta \
            else self.RASTER_FILE_EXTENSION if layerMeta['layerType'] == PAIRS_RASTER_QUERY_NAME and PAIRS_JSON_SPAT_AGG_KEY not in layerMeta \
            else self.VECTOR_FILE_EXTENSION if layerMeta['layerType'] == PAIRS_VECTOR_QUERY_NAME or PAIRS_JSON_SPAT_AGG_KEY in layerMeta \
            else u''
        )
        # extract data to temporary file from ZIP (if any)
        # get raster data
        # ATTENTION: temporary hack in order to circumvent issue
        if layerMeta['layerType'] == PAIRS_RASTER_QUERY_NAME \
           and not PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
            if HAS_GDAL:
                # note: Unforetunately GDAL does not allow to directly take Python
                # binary file streams, thus one needs to inefficiently write back
                # to local temporary file to get a physical file name one can and over
                # with a file name string
                try:
                    # extract data to temporary file from ZIP
                    # note: it looks like having the delete option causes issues on Windows machines
                    # therefore we extract to the standard temporary directory and hope for the OS
                    # to clean up, and that sufficient disk space is provided in the temporary directory
                    with tempfile.NamedTemporaryFile('wb', delete=False,) as tf: #dir=self.downloadDir)
                        with self.queryFS.open(layerDataPath, 'rb') as zf:
                            tf.write(zf.read())
                        tf.flush()
                        # directly read from data path
                        ds = gdal.Open(tf.name)
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
                    with self.queryFS.open(layerDataPath, 'rb') as f:
                        im = PIL.Image.open(f)
                        if layerMeta['details']['pixelType'] in PAIRS_RASTER_INT_PIX_TYPE_CLASS:
                            im.mode=u'I'
                        elif layerMeta['details']['pixelType'] in PAIRS_RASTER_FLOAT_PIX_TYPE_CLASS:
                            im.mode=u'F'
                        a = numpy.array(im).astype(numpy.float)
                except Exception as e:
                    logging.error(
                        "Unable to load '{}' from '{}' into NumPy array using PIL: {}".format(fileName, self.zipFilePath, e)
                    )
            # mask no-data value
            a[a==numpy.float(layerMeta['details']['pixelNoDataVal'])] = numpy.nan
            # assign loaded data to object's data dictionary
            self.data[fileName] = a
        # load vector data (note: CSV file format assumed)
        elif layerMeta['layerType'] == PAIRS_VECTOR_QUERY_NAME \
            or PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
            try:
                with self.queryFS.open(layerDataPath, 'rb') as f:
                    # spatial aggregation vector data
                    if PAIRS_JSON_SPAT_AGG_KEY in layerMeta:
                        logging.info('Identified spatial aggregation data.')
                        self.data[fileName] = pandas.read_csv(
                            f,
                            header      = 0,
                            index_col   = False,
                            quotechar   = PAIRS_VECTOR_CSV_QUOTE_CHAR,
                        )
                    # *conventional* PAIRS vector data
                    else:
                        try:
                            self.data[fileName] = pandas.read_csv(
                                f,
                                header      = 0,
                                index_col   = False,
                                quotechar   = PAIRS_VECTOR_CSV_QUOTE_CHAR,
                                parse_dates = {
                                    PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME: [PAIRS_VECTOR_CSV_TIMESTAMP_COL_NUM]
                                },
                            )
                        except:
                            # catch clash due to same timestamp column naming (Pandas bug)
                            with self.queryFS.open(layerDataPath, 'rb') as f2:
                                self.data[fileName] = pandas.read_csv(
                                    f2,
                                    header      = 0,
                                    index_col   = False,
                                    quotechar   = PAIRS_VECTOR_CSV_QUOTE_CHAR,
                                    parse_dates = [PAIRS_VECTOR_CSV_TIMESTAMP_COL_NUM],
                                )
                        logging.info(
                            "'{}' from '{}' loaded into Pandas dataframe.".format(layerDataPath, self.zipFilePath)
                        )
                        # check if timestamp column is completely empty, and if so,
                        # assign the timestamp from the meta data
                        try:
                            if self.data[fileName][PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME].apply(
                                lambda t: isinstance(t, pandas._libs.tslibs.nattype.NaTType)
                            ).all() and PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME in layerMeta.keys():
                                self.data[fileName][PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME] = layerMeta[PAIRS_META_TIMESTAMP_NAME]
                                logging.info(
                                    "Successfully populated timestamp column '{}' with '{}'.".format(
                                        PAIRS_VECTOR_TIMESTAMP_COLUMN_NAME,
                                        layerMeta[PAIRS_META_TIMESTAMP_NAME]
                                    )
                                )
                        except:
                            # silently pass if this bonus option does not work
                            pass
            except Exception as e:
                logging.error(
                    "Unable to load '{}' from '{}' into Pandas dataframe: {}".format(layerDataPath, self.zipFilePath, e)
                )
        else:
            msg = "Sorry, I do not know how to load PAIRS query data of type '{}'".format(layerMeta['layerType'])
            logging.error(msg)
            raise Exception(msg)

    def create_layers(self, defaultExtension=u''):
        """
        From PAIRS query ZIP file generate Python data structures for layers in memory.

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
