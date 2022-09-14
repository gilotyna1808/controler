import socket
from threading import Thread
import time
from control import check_if_device_is_measuring, check_if_program_is_working, get_device_space, get_device_time, get_dir_size, get_time_until_full_disk

# Config
server_addres = ("192.168.70.123", 4447) # ToDo dodac do config file
send_freq = 1 # 1/s
check_freq = 2 # 0.5/s
path = "/"
proc_pid_file = "/tmp/sensys_rasp.pid"
data_directory = "/home/srr/sr_magnetometr_temp/Data"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_addres)
message = ",,,"
threads = []

def create_conn(socket, addres):
    while True:
        time_now = get_device_time()
        socket.sendto(f"{time_now},{message}".encode("utf-8"),addres)
        time.sleep(send_freq)

def create_msg(old_data_dir_size, data_dir_size):
    disk_space = round(100 - get_device_space(path)[3],2)
    disk_time = get_time_until_full_disk(old_data_dir_size,data_dir_size,path)
    is_working = check_if_program_is_working(proc_pid_file)
    is_measuring = check_if_device_is_measuring(old_data_dir_size,data_dir_size)
    # msg = "time,free_space,time_to_full,isWorking,isMeasuring,"
    msg = f"{disk_space},{disk_time*check_freq},{is_working},{is_measuring}"
    return msg

def check_device():
    old_data_dir_size = get_dir_size(data_directory)
    while True:
        data_dir_size = get_dir_size(data_directory)
        global message
        message = create_msg(old_data_dir_size,data_dir_size)
        time.sleep(check_freq)
        old_data_dir_size = data_dir_size

try:
    threads.append(Thread(target=check_device, daemon=True).start())
    while True:
        data, address = sock.recvfrom(4096)
        threads.append(Thread(target=create_conn, args=(sock, address), daemon=True).start())
finally:
    for t in threads:
        if t is not None:
            t.kill()
    sock.close()
    print("Colsed !!!")