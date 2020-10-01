#netstat -an | grep '50007'

import socket, threading, time, signal, sys


HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        no = input("Give number:")
        if not no.strip() : break
        print("Got:", int(no))
        s.sendall(no.encode('ascii'))
        data = s.recv(1024)
        print('Is Prime:', data.decode('ascii'))