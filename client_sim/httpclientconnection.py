#!/usr/bin/python
#
# author: Bo Yang
#

"""
class to connect web server, send requests and collect responses
"""

import httplib

class HttpClientConnection(object):
    """ client connection class"""

    def __init__(self, host, port):
        """ init func """
        self.host = host
        self.port = port
        self._create_connection()

    def _create_connection(self):
        """ create a new connection """
        print('create connection to %s:%s' % (self.host, self.port))
        self.connection = httplib.HTTPConnection(self.host, self.port)

    def _get_response(self):
        """ parse response """
        retcode = 200
	result = ""
        try: 
            response = self.connection.getresponse()
            retcode = response.status
            result = response.read().decode()
            print("Result %s" % result)
        except httplib.HTTPException:
            retcode = 500
        # TODO, shall enhance to handle different types of exceptions
        except Exception as excpt:
            # connection is reset by peer, need to close and then 
            # create a new one
            if excpt.errno == 104:
                retcode = 500  
                self.CLOSE()
                self._create_connection()

    def POST(self, data):
        """ POST method """
        headers = {'Content-type': 'text/html'}
        try:
            self.connection.request('POST', "", str(data), headers)
        # TODO, shall enhance to handle different types of exceptions
        except Exception:
            # recreate it even though the exception might not be caused
            # by broken connection. it will make code easier 
            # but it's still a TODO item
            self.CLOSE()
            self._create_connection()
            return
        self._get_response()
       
    def GET(self, data):
        """ GET method """
        self.connection.request('GET', str(data))
        self._get_response()

    def HEAD(self, data):
        """ HEAD method """
        self.connection.request('HEAD', str(data))
        self._get_response()

    def CLOSE(self):
        """ close connection """
        self.connection.close()
