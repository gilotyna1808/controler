import psutil
import subprocess
import time
import os
from threading import Thread
space_10, space_50, current_u_v, occured_u_v, temp_80, temp_50, current_throttling, occured_throttling, program, mesurment = (0,0,0,0,0,0,0,0,0,0)

def get_cpu_temp():
    global temp_80, temp_50
    while 1:
        temperature = psutil.sensors_temperatures()['cpu_thermal'][0][1]
        if temperature >= 80:temp_80 = 1
        else: temp_80 = 0
        if temperature >= 50:temp_50 = 1
        else: temp_50 = 0
        time.sleep(1)

def get_disk_space():
    global space_10, space_50
    while 1:
        space =100 - psutil.disk_usage("/").percent
        if space < 10: space_10 = 1
        else: space_10 = 0
        if space < 50: space_50 = 1
        else: space_50 = 0
        time.sleep(1)

def get_throttling_values():
    global current_u_v, occured_u_v, current_throttling, occured_throttling
    while 1:
        err, msg = subprocess.getstatusoutput('vcgencmd get_throttled')
        if not err:
            msg = bin(int(msg.split("=")[1], 16))[2:]
            msg = msg[::-1]
            if len(msg) >= 18:
                current_u_v = msg[0]
                current_throttling = msg[2]
                occured_u_v = msg[16]
                occured_throttling = msg[18]
            elif len(msg) >= 16:
                current_u_v = msg[0]
                current_throttling = msg[2]
                occured_u_v = msg[16]
                occured_throttling = 0
            elif len(msg) >= 2:
                current_u_v = msg[0]
                current_throttling = msg[2]
                occured_u_v = 0
                occured_throttling = 0
            elif len(msg) == 1:
                current_u_v = msg[0]
                current_throttling = 0
                occured_u_v = 0
                occured_throttling = 0
        time.sleep(1)

def get_if_program_is_working(path):
    global program
    while 1:
        program = check_if_program_is_working(path)
        time.sleep(1)

def get_if_devise_is_measuring():
    global mesurment
    while 1:
        mesurment = check_if_device_is_measuring(1,1)
        time.sleep(1)

def get_pid_from_file(file):
    if not os.path.isfile(file):
        raise Exception("file does not exist")
    try:
        f = open(file,"r")
        pid  = f.readline()
        if not pid.isnumeric():
            raise Exception("pid is not a number")
        pid = int(pid)
        return pid
    finally:
        f.close()

def check_if_program_is_working(proc_pid_file):
    if os.path.exists(proc_pid_file):
        f = open(proc_pid_file,"r")
        pid = f.readline()
        if pid != "":
            if psutil.pid_exists(int(pid)):
                return True
    return False

def check_if_device_is_measuring(old_data_dir_size, data_dir_size):
    if old_data_dir_size < data_dir_size:
        return True
    return False

# def get_cpu_temp():
#     temp = psutil.sensors_temperatures()
#     print(temp)
#     temp = psutil.disk_usage('/')
#     # print(temp)
#     print(f"Total: {temp.total/ (1024.0 ** 3)}")
#     print(f"Free: {temp.free/ (1024.0 ** 3)}")
#     print(f"Used: {temp.used/ (1024.0 ** 3)}")
#     print(f"P{temp.free/temp.total} P:{temp.percent}")

# def get_info():
#     err, msg = subprocess.getstatusoutput('vcgencmd get_throttled')
#     print(msg)
#     print(bin(int(msg.split("=")[1], 16))[:])
#     print(bin(int(msg.split("=")[1], 16))[2:])

# get_cpu_temp()
# get_info()
Thread(target =  get_cpu_temp, daemon=True).start()
Thread(target =  get_disk_space, daemon=True).start()
Thread(target =  get_throttling_values, daemon=True).start()
Thread(target =  get_if_program_is_working, args=("/tmp/geometrics_rasp.pid",), daemon=True).start()
Thread(target =  get_if_devise_is_measuring, daemon=True).start()

i = 0
while 1:
    print(f"NR:{i}##########")
    print(f"Space < 50%: {space_50}")
    print(f"Space < 10%: {space_10}")
    print(f"Temp > 50C: {temp_50}")
    print(f"Temp > 80C: {temp_80}")
    print(f"Currently under voltage: {current_u_v}")
    print(f"Under voltage occured: {occured_u_v}")
    print(f"Currently throttling: {current_throttling}")
    print(f"throttling occured: {occured_throttling}")
    print(f"Program is working: {program}")
    print(f"Program is measuring: {mesurment}")
    i+=1
    time.sleep(1)


# from genericpath import isfile
# from re import T
# #/usr/bin/env python

# import os
# import sys
# import time
# import signal



# pid = str(os.getpid())
# pidfile = "/tmp/sensys_rasp.pid"
# pid_file_unlinked = True

# def handler_stop_signals(signum, frame):
#     if os.path.isfile(pidfile):
#         os.unlink(pidfile)
#         sys.exit()

# signal.signal(signal.SIGTERM,handler_stop_signals)

# if os.path.isfile(pidfile):
#     print(f"{pidfile} already exists, exiting")
#     sys.exit()

# open(pidfile, 'w').write(pid)
# i = 0
# try:
#     while True:
#         print(i)
#         i += 1
#         time.sleep(1)
# finally:
#     if os.path.isfile(pidfile):
#         os.unlink(pidfile)