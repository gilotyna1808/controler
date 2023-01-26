#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:39:13 2022

@author: Daniel
"""
from cmath import inf
from genericpath import isfile
import psutil
import os
from datetime import datetime
import time

def heart_beat():
    raise Exception("Not implemented")

def get_device_time():
    return datetime.now().timestamp()

def get_device_space(path:str):
    return psutil.disk_usage(path)

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

def get_dir_size(dir):
    size = 0
    for file in os.scandir(dir):
        size+=os.path.getsize(file)
    return size

changes = []

def get_time_until_full_disk(old_data_dir_size, data_dir_size, path):
    change = data_dir_size-old_data_dir_size
    if(change > 0):
        global changes
        changes.append(change)
        free = psutil.disk_usage(path)[2]
        change = sum(changes)/len(changes)
        if len(changes) > 1000:
            changes = changes[-100:]
        return int(free/change)
    return -1

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

# A = get_device_space('/dev/sda')
# B = int(A[1])/int(A[0])
# C = A[2]/A[0]
# print(B)
# print(C)
# print(A)

# print(get_device_time())
# print(check_if_program_is_working())