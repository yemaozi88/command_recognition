#!/usr/bin/env python3

import socket
import time

HOST = 'ev3dev'  # The server's hostname or IP address
PORT = 65432     # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    time.sleep(2)
    s.sendall(b'this is a test')
    time.sleep(2)
    s.sendall(b'did you hear me')
    #data = s.recv(1024)

#print('Received', repr(data))