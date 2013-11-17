#!/usr/bin/env python
# encoding: utf-8

__author__    = "Ole Weidner"
__copyright__ = "Copyright 2013, Ole Weidner"
__license__   = "MIT"

from cgi import parse_qs
import json
import datetime
import threading

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
        url = Url(task_results_url)
        print url

        # extract hostname, session uid and agent uid from 
        # the url.
        self.session_uid = None
        self.agent_uid = None

        for key, val in parse_qs(url.query).iteritems():
            print "%s -- %s" % (key, val)
            if key == 'session':
                self.session_uid = val[0]
            if key == 'agent':
                self.agent_uid = val[0]

        if self.session_uid is None or self.agent_uid is None:
            raise Exception("URL doesn't define 'session' or 'agent'.")

        # # extract the file path and open the file
        # # and read the task data
        # self._tasks = list()
        # self.log = logger

        # self.file_path = task_results_url.path
        # # a global lock so file access can be synchronized
        # self._putlock = threading.Lock()

        # self.log.info("%s: Successfully created/opened events file '%s'" % (DRIVER, self.file_path))

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
