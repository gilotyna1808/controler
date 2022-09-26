import socket
import os
import datetime
from turtle import bgcolor
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
server_addres = ("192.168.70.123", 4447) # ToDo dodac do config file

sock.sendto(b"", server_addres)

bcolors = {
    "HEADER" : '\033[95m',
    "OKBLUE" : '\033[94m',
    "OKCYAN" : '\033[96m',
    "OKGREEN" : '\033[92m',
    "WARNING" : '\033[93m',
    "FAIL" : '\033[91m',
    "ENDC" : '\033[0m',
    "BOLD" : '\033[1m',
    "UNDERLINE" : '\033[4m',
}

def sec_to_time(sec):
    color = ""
    sec = int(sec)
    if sec < 0:
        return bcolors["FAIL"]+"INF"+bcolors["ENDC"]
    elif sec<3600:
        color = bcolors["FAIL"]
    return f"{color}{int(sec/3600)}:{int(sec/60)%60}:{sec%60}"+bcolors["ENDC"]

def print_time(time):
    color=""
    if datetime.datetime.now().timestamp() - float(time) > 2:
        color = bcolors["FAIL"]
    print(f"{color}Czas: {datetime.datetime.fromtimestamp(float(time))}"+bcolors["ENDC"])

def print_free_space(space):
    print(f"Wolne Miejsce: {space}%")

def print_disk_time(time):
    print(f"Pozostały czas: {sec_to_time(time)}")

def print_is_program_working(flag):
    color = bcolors["FAIL"]
    if flag == 'True':
        color = bcolors["OKGREEN"]
    print(f"Program działa {color}{flag}"+bcolors["ENDC"])

def print_is_measurments_working(flag):
    color = bcolors["FAIL"]
    if flag == 'True':
        color = bcolors["OKGREEN"]
    print(f"Pomiary działają {color}{flag}" +bcolors["ENDC"])

while True:
    data, addres = sock.recvfrom(4096)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(data)
    datas = data.decode("utf-8").split(",")
    print_time(datas[0])
    print_free_space(datas[1])
    print_disk_time(datas[2])
    print_is_program_working(datas[3])
    print_is_measurments_working(datas[4])
    
    

    # print(f"Data: {data.decode('utf-8')}")s