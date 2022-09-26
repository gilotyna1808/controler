from signal import SIGTERM
import socket
from threading import Thread
import time
from types import FunctionType
from control import check_if_device_is_measuring, check_if_program_is_working, get_device_space, get_device_time, get_dir_size, get_pid_from_file, get_time_until_full_disk
import psutil
import os
import subprocess

# Config
SERVER_ADDRESS = ("192.168.70.139", 4447) # Address i port, na którym bedzie komunikacja z klientem
LOCAL_ADDRESS = ("localhost", 65432) # Address i port do lokalnej komunikacji z programem lokalnym
SEND_FREQ = 1 # 1/s
CHECK_FREQ = 2 # 0.5/s
TASK_TIMEOUT = 5 #s
PATH = "/" # Scieżka do głównego katalogu
PROC_PID_FILE = "/tmp/sensys_rasp.pid"
DATA_DIRECTORY = "/home/srr/sr_magnetometr_temp/Data"
ERROR_REPLY = "Cos poszlo nie tak"
TIMEOUT_REPLY = f"Przekroczono ograniczenie czasowe: {TASK_TIMEOUT}s"
PROGRAM_FILE = "test1.py"
PYTHON_INTERPRETER = "python"

SOCKET_LISTENER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCKET_LISTENER.bind(SERVER_ADDRESS)
SOCKET_TASKER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
SOCKET_TASKER.settimeout(TASK_TIMEOUT)
#Zmienne globalne
message = ",,,"
task_lock = False

def create_conn(sock, addres):
    while True:
        time_now = get_device_time()
        sock.sendto(f"{time_now},{message}".encode("utf-8"),addres)
        time.sleep(SEND_FREQ)

def create_msg(old_data_dir_size, data_dir_size):
    disk_space = round(100 - get_device_space(PATH)[3],2)
    disk_time = get_time_until_full_disk(old_data_dir_size,data_dir_size,PATH)
    is_working = check_if_program_is_working(PROC_PID_FILE)
    is_measuring = check_if_device_is_measuring(old_data_dir_size,data_dir_size)
    # msg = "time,free_space,time_to_full,isWorking,isMeasuring,"
    msg = f"{disk_space},{disk_time*CHECK_FREQ},{is_working},{is_measuring}"
    return msg

def check_device():
    old_data_dir_size = get_dir_size(DATA_DIRECTORY)
    while True:
        data_dir_size = get_dir_size(DATA_DIRECTORY)
        global message
        message = create_msg(old_data_dir_size,data_dir_size)
        time.sleep(CHECK_FREQ)
        old_data_dir_size = data_dir_size

def send_msg(conn:tuple, args=None):
    sock = conn[0]
    address = conn[1]
    msg = "".join(args)
    if msg is None:
        sock.sendto(ERROR_REPLY.encode("utf-8"),address)
        return
    sock.sendto(msg.encode("utf-8"),address)

def task_wraper(conn:tuple, task:FunctionType, args=None):
    msg = "done"
    global task_lock
    if not task_lock:
        task_lock = True
        try:
            task(args)
        except socket.timeout as ex:
            print(ex)
            msg = TIMEOUT_REPLY
        except Exception as ex:
            print(ex)
            msg = ERROR_REPLY
        finally:
            task_lock = False
            send_msg(conn, msg)
    else: send_msg(conn, "Wykonywane jest inne zadanie")

def flush_socket(sock:socket.socket):
    try:
        t = sock.gettimeout()
        sock.settimeout(0.01)
        res = SOCKET_TASKER.recv(16384)
    except socket.timeout:
        pass
    finally:
        sock.settimeout(TASK_TIMEOUT)

def send_task(args=None):
    if type(args) is not type(list()):
        raise Exception("Brak zadania")
    flush_socket(SOCKET_TASKER)
    msg = args[0]
    SOCKET_TASKER.sendto(msg.encode("utf-8"),LOCAL_ADDRESS)
    res = SOCKET_TASKER.recv(4096)
    print(res)

def task_kill_proc(args=None):
    pid  = get_pid_from_file(PROC_PID_FILE)
    if not psutil.pid_exists(pid):
        raise Exception("proces pod odczytanym pid nie istnieje")
    os.kill(pid, SIGTERM)

def task_start_proc(args=None):
    print_to_console = False
    if type(args) is type(list()):
        if len(args) > 1:
            print_to_console = args[1].lower() in ['true', 'yes', 'y', '1']
    if check_if_program_is_working(PROC_PID_FILE):
        raise Exception("program jest juz uruchomiony")
    if print_to_console:
        pid = subprocess.Popen([PYTHON_INTERPRETER, PROGRAM_FILE]).pid
    else:
        pid = subprocess.Popen(['nohup', PYTHON_INTERPRETER, PROGRAM_FILE]).pid
    print(f"PID: {pid}, Is running:{psutil.pid_exists(pid)}")

CMD_ACTION = {
    "hibernate" : send_task,
    "get_up": send_task,
    "reset_ch": send_task,
    "reset_laser_lock": send_task,
    "reset_larmor_lock": send_task,
    "fpga_reset": send_task,
    "low_heading": send_task,
    "set_individual": send_task,
    "set_combined": send_task,
    "shutdown_program": task_kill_proc,
    "task_start_proc": task_start_proc
}

try:
    # Thread(target=check_device, daemon=True).start()
    while True:
        data, address = SOCKET_LISTENER.recvfrom(4096)
        data = data.decode("utf-8").split(",")
        conn = (SOCKET_LISTENER, address)
        print(data)
        if data[0] == "info":
            Thread(target=create_conn, args=(SOCKET_LISTENER, address), daemon=True).start()
        elif data[0] == "cmd" and len(data) > 1:
            print(data[1])
            cmd_action = CMD_ACTION.get(data[1])
            if cmd_action is not None:
                Thread(target=task_wraper, args=(conn, cmd_action, data[1:]), daemon=True).start()
            else:
                send_msg(conn, "Wrong command")
finally:
    if os.path.isfile("nohup.out"):
        os.remove("nohup.out")
    SOCKET_LISTENER.close()
    SOCKET_TASKER.close()
    print("Colsed !!!")