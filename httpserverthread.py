#!/usr/bin/python
#
# author: Bo Yang
#

"""
Web Server for Fib function
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import fib
import signal
from daemon import daemonize
import logging

PORT = 8000
PIDFILE = "/var/run/webservice_fib.pid"
LOGFILE = "/var/webservice/httpd.log"

# set logger 
httpdlogger = logging.getLogger('httpd-logger')
httpdlogger.setLevel(logging.INFO)
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.INFO)
httpdlogger.addHandler(fh)

class Handler(BaseHTTPRequestHandler):
    """handler class"""

    def log_message(self, format, *args):
        """ overriden log_message to redirect log to file """
        # TODO: better logging format
        httpdlogger.info("%s - - [%s] %s" \
            % (self.address_string(), self.log_date_time_string(), format%args))
    
    def do_HEAD(self):
        """HEAD handler"""
        # to be implemented 
        self.send_response(405)

    def do_GET(self):
        """GET handler"""
        # to be implemented 
        self.send_response(405)

    def do_POST(self):
        """POST handler"""
        length = int(self.headers['Content-length'])
        if length <= 0:
            self.rfile.read()
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        else:
            data = self.rfile.read(length)
            ret_str = fib.fib_sequence_wapper(data)
            if ret_str == fib.HELP_MESSAGE:
                self.send_response(404)
            else:
                self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(ret_str)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each request in a separate thread by extending ThreadingMixIn"""
    pass

def signal_handler():
    """ handle signnals """
    # optional because the service is set to daemon
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

if __name__ == '__main__':

    daemonize("/", PIDFILE)
    signal_handler()

    http_server = ThreadedHTTPServer(('0.0.0.0', PORT), Handler)
    httpdlogger.info("serving at port %d" % PORT)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        httpdlogger.info("existing...")
