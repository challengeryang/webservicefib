#!/usr/bin/python
#
# author: Bo Yang
#

"""
Client simulator 
"""

from httpclientconnection import HttpClientConnection 
from httpclientthread import HttpClientThread
import argparse
import Queue

REQUEST_QUEUE = Queue.Queue()
CONN_QUEUE = Queue.Queue()
NUM_THREAD = 2

def __generate_rainy_test():
    """ generate rainy test cases """
    REQUEST_QUEUE.put({'op':'HEAD', 'val': -1})
    REQUEST_QUEUE.put({'op':'GET' , 'val': -1})
    REQUEST_QUEUE.put({'op':'DEL' , 'val': -1})
    REQUEST_QUEUE.put({'op':'POST', 'val': -1})
    REQUEST_QUEUE.put({'op':'POST', 'val': ''})
    REQUEST_QUEUE.put({'op':'POST', 'val': 1.1})
    REQUEST_QUEUE.put({'op':'POST', 'val': 'abc'})
    REQUEST_QUEUE.put({'op':'POST', 'val': []})
    REQUEST_QUEUE.put({'op':'POST', 'val': [1, 2, 3]})
    REQUEST_QUEUE.put({'op':'POST', 'val': {1:'a'}})
    REQUEST_QUEUE.put({'op':'POST', 'val': 'asdfagar323434_3~!@#$%^*5'})
    # can add more, TODO, enhancement: read test cases 
    # from external source 

def generate_requests(num):
    """ generate requests and put them to Queue """
    for i in range(num):
        REQUEST_QUEUE.put({'op':'POST', 'val': i})

    __generate_rainy_test() 
    

def generate_connections(num, host, port):
    """ generate connections and put them to Queue """
    for _ in range(num):
        conn = HttpClientConnection(host, port)
        CONN_QUEUE.put(conn, True)

def remove_connections():
    """ clean up connections """
    while not CONN_QUEUE.empty():
        conn = CONN_QUEUE.get(True)
        conn.CLOSE()

def send_requests():
    """ send requests to server """
    worker_thread_list = []
    for _ in range(NUM_THREAD):
        worker_thread = HttpClientThread(REQUEST_QUEUE, CONN_QUEUE)
        worker_thread_list.append(worker_thread) 
    for worker in worker_thread_list:
        worker.start()
    for worker in worker_thread_list:
        worker.join()

def _parse_args():
    """ parse input parameters """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connection', dest='conn_num',
        required=True, help='num of connections')
    parser.add_argument('-t', '--thread', dest='thread_num',
        required=True, help='num of threads')
    parser.add_argument('-s', '--server', dest='server_host',
        required=True, help='server hostname')
    parser.add_argument('-p', '--port', dest='server_port',
        required=True, help='server port')
    parser.add_argument('-r', '--round', dest='round_test',
        required=True, help='num of rounds of test')
    return parser.parse_args()


def main():
    """send requests as clients"""
    args = _parse_args()
    generate_connections(int(args.conn_num), \
        args.server_host, int(args.server_port))
    global NUM_THREAD
    NUM_THREAD = int(args.thread_num)
    generate_requests(int(args.round_test))
    send_requests()
    remove_connections()

if __name__ == "__main__":
    main()
