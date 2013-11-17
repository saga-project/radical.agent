#!/usr/bin/env python
# encoding: utf-8

__author__    = "Ole Weidner"
__copyright__ = "Copyright 2013, Ole Weidner"
__license__   = "MIT"

from cgi import parse_qs
import json
import datetime
import threading
from pymongo import MongoClient

from radical.utils import Url

DRIVER = "SAGAPilot"

#-----------------------------------------------------------------------------
#
class SAGAPilot(object):

    #-------------------------------------------------------------------------
    #
    def __init__(self, logger, task_results_url):
        """
        """
        self.log = logger

        # extract hostname, session uid and agent uid from 
        # the url.
        url = Url(task_results_url)

        self.db_name     = None
        self.session_uid = None
        self.agent_uid   = None

        for key, val in parse_qs(url.query).iteritems():
            if key == 'session':
                self.session_uid = val[0]
            if key == 'agent':
                self.agent_uid = val[0]
            if key == 'dbname':
                self.db_name = val[0]

        if self.session_uid is None or self.agent_uid is None or self.db_name is None:
            raise Exception("--event URL doesn't define 'session', 'agent' or 'dbname'")

        # connect to MongoDB
        mongodb_url = "mongodb://%s" % url.host
        if url.port is not None:
            mongodb_url += ":%s" % url.port

        self._client = MongoClient(str(mongodb_url))
        self._db     = self._client[self.db_name]
  
    #-------------------------------------------------------------------------
    #
    def __del__(self):
        # nothing to do
        pass

    #-------------------------------------------------------------------------
    #
    def close(self):
        # nothing to do
        pass

    #-------------------------------------------------------------------------
    #
    def put(self, origin, event, value):
        ''' Publish a new task event.
        '''
        # synchronize file access
        # with self._putlock:
        #     events_file = open(self.file_path, 'a')
        #     # create a JSON dictionary for the task result
        #     result = {
        #         'type': 'event',
        #         'timestamp': str(datetime.datetime.now()),
        #         'task_id': task_id,
        #         'event': event,
        #         'value': value
        #     }
        #     events_file.write(json.dumps(result)+'\n')
        #     events_file.close()
