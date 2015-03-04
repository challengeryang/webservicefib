#!/usr/bin/python
#
# author: Bo Yang
#

"""
thread to send requests to server 
it picks up request from job queue, and then picks 
up one available connection to send this request
"""

import threading 
import Queue

class HttpClientThread(threading.Thread):
    """
    Thread to send request to server. it's just a work thread, 
    and doesn't maintain any state
    it picks up job from job queue, and get an available connection
    from connection queue, finally send the request through this 
    connection
    """

    def __init__(self, job_queue, connection_queue):
        threading.Thread.__init__(self)
        self.job_queue = job_queue
        self.connection_queue = connection_queue

    def run(self):
        print '%s: starting' % self.getName()
        num_request = 0
        while True:
            job = None
            try:
                # get job from job queue
                job = self.job_queue.get(True, 3)
            except Queue.Empty:
                print '%s: no more jobs(sent %d requests), existing' \
                    % (self.getName(), num_request)
                break
            num_request += 1
            # pick up a conenction from connection queue
            conn = self.connection_queue.get(True)
            #try: 
            msg = ""
            if job['op'] == 'HEAD':
                conn.HEAD(job['val'])
                msg = job['op'] + " " + str(job['val'])
            elif job['op'] == 'GET':
                conn.GET(job['val'])
                msg = job['op'] + " " + str(job['val'])
            elif job['op'] == 'POST':
                conn.POST(job['val'])
                msg = job['op'] + " " + str(job['val'])
            else:
                msg = '%s unsupported operation' % job['op']
 
            print "## " + msg

            # put back the connection so other threads can 
            # use this connection as well 
            self.connection_queue.put(conn, True)  
