#!/usr/bin/python
# Deamon method
#
# it's nothing new, almost the same logic for all daemon process
# no matter which language we use

import os
import sys

# make a the process a daemon
def daemonize(root_dir="/", \
              pidfile="", \
              stdin="/dev/null", \
              stdout="/dev/null", \
              stderr="/dev/null"):
    '''
    Make the process into a daemon
    '''
    # Perform the first fork.
    try:
        pid = os.fork()
        if pid > 0:
            # parent exits
            os._exit(0)
    except OSError, excep:
        msg = "fork failed: %d %s" % (excep.errno, excep.strerror)
        raise(Exception(msg))

    # Decouple from parent environment.
    try:
        os.chdir(root_dir)
    except OSError, excep:
        msg = "chdir(%s) failed: %d %s" \
            % (root_dir, excep.errno, excep.strerror)
        raise(Exception(msg))

    try:
        os.umask(0)
    except OSError, excep:
        msg = "umask failed: %d %s" % (excep.errno, excep.strerror)
        raise(Exception(msg))

    try:
        # core function
        os.setsid()
    except OSError, excep:
        msg = "setsid failed: %d %s" % (excep.errno, excep.strerror)
        raise(Exception(msg))

    # Perform the second fork.
    # not very necessary but no side effect to do so
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError, excep:
        msg = "fork failed: %d %s" % (excep.errno, excep.strerror)
        raise(Exception(msg))

    for fd in sys.stdout, sys.stderr:
        fd.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)

    try:
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    except OSError, excep:
        msg = "dup2 failed: %d %s" % (excep.errno, excep.strerror)
        raise(Exception(msg))

    # Create the pid file if specified
    if pidfile != "":
        if os.path.exists(pidfile):
            os.remove(pidfile)
        with open(pidfile, "w") as f:
            f.write("%d" % os.getpid())
