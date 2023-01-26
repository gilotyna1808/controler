#!/usr/bin/env python3
import pi_device_message_module as pi
import mag_module as mag
import socket
from threading import Thread

diagnostics_server_address = ("192.168.70.147",42042)

def send_pi_message(address):
    raspberry_mesage = pi.raspberry_message(True)
    condition = raspberry_mesage.get_condition()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    while True:
        with condition:
            message = raspberry_mesage.get_message()
            sock.sendto(message.encode("utf-8"),address)
            condition.wait()

def send_magdata(address):
    magnetometr_message = mag.magnetometr_check(True)
    condition = magnetometr_message.get_condition()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    while True:
        with condition:
            message = magnetometr_message.get_message()
            sock.sendto(message.encode("utf-8"),address)
            condition.wait()

Thread(target=send_pi_message, args=(diagnostics_server_address,), daemon=True).start()
Thread(target=send_magdata, args=(diagnostics_server_address,), daemon=True).start()

while 1:True