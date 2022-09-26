from genericpath import isfile
from re import T
#/usr/bin/env python

import os
import sys
import time
import signal



pid = str(os.getpid())
pidfile = "/tmp/sensys_rasp.pid"
pid_file_unlinked = True

def handler_stop_signals(signum, frame):
    if os.path.isfile(pidfile):
        os.unlink(pidfile)
        sys.exit()

signal.signal(signal.SIGTERM,handler_stop_signals)

if os.path.isfile(pidfile):
    print(f"{pidfile} already exists, exiting")
    sys.exit()

open(pidfile, 'w').write(pid)
i = 0
try:
    while True:
        print(i)
        i += 1
        time.sleep(1)
finally:
    if os.path.isfile(pidfile):
        os.unlink(pidfile)