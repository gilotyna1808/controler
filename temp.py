from genericpath import isfile
from re import T
#/usr/bin/env python

import os
import sys
import time

pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"

if os.path.isfile(pidfile):
    print(f"{pidfile} already exists, exiting")
    sys.exit()

open(pidfile, 'w').write(pid)
try:
    while True:
        time.sleep(1)
finally:
    os.unlink(pidfile)