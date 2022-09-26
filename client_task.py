import socket
import os
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
server_addres = ("192.168.70.139", 4447) # ToDo dodac do config file

# "hibernate" : send_msg,
# "get_up": send_msg,
# "reset_ch": send_msg,
# "reset_laser_lock": send_msg,
# "reset_larmor_lock": send_msg,
# "fpga_reset": send_msg,
# "low_heading": send_msg,
# "set_individual": send_msg,
# "set_combined": send_msg,
# "shutdown_program": task_kill_proc,
# "task_start_proc": task_start_proc

sock.sendto(b"cmd,shutdown_program", server_addres)
data = sock.recv(4096)
print(data)
# while True:
#     data, addres = sock.recvfrom(4096)
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print(data)