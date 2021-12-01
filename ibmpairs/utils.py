'''
IBM PAIRS Utilities: A collection of tools complementing the
RESTful API wrapper.

Copyright 2019-2021 Physical Analytics, IBM Research. All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
'''

import logging
from collections import deque
from functools import reduce
from time import sleep, time
from ibmpairs import paw

MAX_CONCURRENT = 5

logger = logging.getLogger(__name__)

class PAIRSProject(object):
    '''
    Utility class to submit a large number of queries to IBM PAIRS. The class leverages ``ibmpairs.paw.PAIRSQuery``
    and maintains a local queue.

    Usage
    
    >>> project = PAIRSProject(queryList)
    >>> project.submitAllQueued()

    Queries contained in ``queryList`` can be either query JSONs or ``paw.PAIRSQuery`` objects. In the latter case,
    only queries that have previously not been submitted will be submitted when calling ``submitAllQueued``. Once
    queries have completed processing, the downloaded data can be found in the directory indicated by
    ``downloadDir``. (There can be multiple download directories if ``queryList`` contains ``paw.PAIRSQuery`` objects.)

    While queries are running, the class gives a periodic status update via python's logging module.
    Note that this happens at the ``logging.INFO`` level. A rudimentary setup for this would be as follows:

    >>> import logging
    >>> logging.basicConfig(level = <log-level required for your application>)
    >>> pawLogger = logging.getLogger('ibmpairs.paw')
    >>> pawLogger.setLevel(logging.ERROR)
    >>> pairsUtilsLogger = logging.getLogger('ibmpairs.utils')
    >>> pairsUtilsLogger.setLevel(logging.INFO)

    The class stores queries in 4 queues, accessible as

    >>> project.queries['queued']
    >>> project.queries['running']
    >>> project.queries['completed']
    >>> project.queries['failed']

    One can obtain a list of all query JSONs in one particular queue by calling ``getQueryJSONs('<queue name>')``.
    The following is then feasible:

    >>> import json
    >>> completedQueries = oldProject.getQueryJSONs('completed')
    >>> with open('completedQueries.json', 'w') as fp:
    >>>     json.dump(completedQueries, fp)
    >>> # ... some other code ...
    >>> with open('completedQueries.json', 'r') as fp:
    >>>     recoveredQueries = json.load(fp)
    >>> newProject = PAIRSProject(recoveredQueries)

    The properties of the ``paw`` library make it quite simple to work with completed queries even if the program
    hosting the ``PAIRSProject`` object has been terminated. Assume the data of completed queries is stored in
    ``<downloads/>`` (typically the value of ``downloadDir``). Then the following builds an index of what is in that
    directory:

    >>> from glob imoprt glob
    >>> zippedQueries = glob('downloads/*.zip')
    >>> queries = [paw.PAIRSQuery(z) for z in zippedQueries]
    >>> for q in queries:
    >>>     q.list_layers()

    Crucially, the ``list_layers`` function here, parses the contents of a query without loading
    the data to memory. (This is in contrast to ``create_layers``.)
    
    :param queryList:           list containing a mix of PAIRS query JSONs
                                and ``paw.PAIRSQuery`` objects. For ``paw.PAIRSQuery`` objects, only those which have not been submitted yet will be submitted.
    :type queryList:            list
    :param auth:                user name and password as tuple for access to pairsHost
    :type auth:                 str, str
    :param overwriteExisting:   destroy locally cached data, if existing,
                                otherwise grab the latest locally cached data, `latest` is defined by alphanumerical ordering of the PAIRS query ID
    :type overwriteExisting:    bool
    :param downloadDir:         directory where to store downloaded data
    :type downloadDir:          str
    :param maxConcurrent:       maximum number of concurrent queries. Note that
                                the maximum number of concurrent queries might be limited server side for a particular user. There is no guarantee that a user can submit maxConcurrent queries at a given time.
    :type maxConcurrent:        int
    :param logEverySeconds:     time interval at which the class will send
                                status messages to its logger in seconds (via ``logging.INFO``)
    :type logEverySeconds:      int
    '''

    def __init__(self, queryList, auth = None, downloadDir='./downloads', overwriteExisting = False, maxConcurrent = 2, logEverySeconds = 30):

        if maxConcurrent > MAX_CONCURRENT:
            raise Exception('Maximum value for maxConcurrent is {}.'.format(MAX_CONCURRENT))

        self.maxConcurrent = maxConcurrent
        self.logEverySeconds = logEverySeconds

        self.queries = {
            'queued' : deque(),
            'running' : deque(),
            'completed' : deque(),
            'failed' : deque()
        }
        for q in queryList:
            if isinstance(q, paw.PAIRSQuery):
                if q.querySubmit is None:
                    self.queries['queued'].append(q)
                elif q.queryStatus is None:
                    self.queries['running'].append(q)
                elif q.queryStatus.json()['statusCode'] < 20:
                    self.queries['running'].append(q)
                elif q.queryStatus.json()['statusCode'] == 20:
                    self.queries['completed'].append(q)
                elif q.queryStatus.json()['statusCode'] > 20:
                    self.queries['failed'].append(q)
                else:
                    raise Exception('Cannot determine status of PAIRSQuery object.')
            else:
                self.queries['queued'].append(
                    paw.PAIRSQuery(q, auth = auth, downloadDir = downloadDir, overwriteExisting = overwriteExisting)
                )

    def __len__(self):
        lengths = [
            len(self.queries['queued']), len(self.queries['running']),
            len(self.queries['completed']), len(self.queries['failed'])
        ]
        return reduce(lambda x, y: x + y, lengths)

    def __repr__(self):
        return 'PAIRSProject: {}/{}/{}/{} queued/running/completed/failed.'.format(
            len(self.queries['queued']), len(self.queries['running']),
            len(self.queries['completed']), len(self.queries['failed'])
        )

    def _submitOneQuery(self):
        if len(self.queries['running']) >= self.maxConcurrent:
            return False
        try:
            q = self.queries['queued'].popleft()
        except IndexError:
            return False

        try:
            q.submit()
        except Exception as e:
            self.queries['failed'].append(q)
            logger.warning('Failed submitting query.')
        else:
            self.queries['running'].append(q)
            logger.debug('Query submitted.')
        sleep(1)
        return True

    def _logStatus(self):
        logger.info(self.__repr__())

    def submitAllQueued(self, cosInfoJSON=None, printStatus=False,):
        '''
        Submits all queries in the local queue. Ensures that there are always maxConcurrent
        queries running. (Note that the maximum number of concurrent queries might be limited
        server side for a particular user. There is no guarantee that a user can submit
        maxConcurrent queries at a given time.)

        :param cosInfoJSON:     IBM PAIRS with Cloud Object Storage bucket information like
                                ```JSON
                                {
                                    "provider": "ibm",
                                    "endpoint": "https://s3.us.cloud-object-storage.appdomain.cloud",
                                    "bucket": "<your bucket name>",
                                    "token": "<your secret token for bucket>"
                                }
                                ```
                                if set, the query result is published in the cloud
                                and not stored locally on your machine. It is a
                                useful feature in combination with IBM Watson Studio notebooks
        :type cosInfoJSON:      dict
        :param printStatus:     triggers printing the poll status information of downloading
                                a query
        :type printStatus:      bool
        '''

        while True:
            if (len(self.queries['queued']) == 0) and (len(self.queries['running']) == 0):
                break

            while self._submitOneQuery():
                pass

            logTimer = time()
            while True:
                try:
                    q = self.queries['running'].popleft()
                except IndexError:
                    break
                else:
                    q.poll()
                    # when utilizing cached data, do not wait
                    if q.overwriteExisting:
                        sleep(1)
                    if q.queryStatus.json()['statusCode'] < 20:
                        self.queries['running'].append(q)
                    elif q.queryStatus.json()['statusCode'] == 20:
                        try:
                            q.download(cosInfoJSON=cosInfoJSON, printStatus=printStatus)
                        except Exception as e:
                            print('Encountered exception {} while downloading.'.format(e))
                            self.queries['failed'].append(q)
                        else:
                            self.queries['completed'].append(q)
                            logger.debug('Completed download.')
                        finally:
                            self._submitOneQuery()
                    # ignore deleted PAIRS queries when cached
                    elif q.queryStatus.json()['statusCode']==31 and not q.overwriteExisting:
                        try:
                            q.download(cosInfoJSON=cosInfoJSON, printStatus=printStatus)
                        except Exception as e:
                            print('Encountered exception {} while (down)loading cached data deleted in PAIRS.'.format(e))
                            self.queries['failed'].append(q)
                        else:
                            self.queries['completed'].append(q)
                            logger.debug('Cached data locally loaded.')
                        finally:
                            self._submitOneQuery()
                    else:
                        self.queries['failed'].append(q)
                        logger.debug('Query failed.')
                        self._submitOneQuery()


                    if time() - logTimer > self.logEverySeconds:
                        logTimer = time()
                        self._logStatus()

    def getQueryJSONs(self, status):
        '''
        Returns all query JSONs in the queue self.queries[status].

        :param status:    indicates queue from which query JSONs should be returned.
        :type status:     string
        :returns:         list of PAIRS query JSONs
        :rtype:           list
        '''

        if status not in self.queries:
            raise Exception('\'status\' has to be one of {}'.format(self.queries.keys()))
        return [q.query for q in self.queries[status]]
