import socket
import sys
from time import sleep

SERVER_ADDRESS = ('localhost', 65432)
SOCKET_LISTENER = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCKET_LISTENER.bind(SERVER_ADDRESS)

while True:
    data, address = SOCKET_LISTENER.recvfrom(4096)
    data = data.decode("utf-8").split(",")
    conn = (SOCKET_LISTENER, address)
    print(data)
    sleep(10)
    SOCKET_LISTENER.sendto("LOLALA".encode("utf-8"),address)