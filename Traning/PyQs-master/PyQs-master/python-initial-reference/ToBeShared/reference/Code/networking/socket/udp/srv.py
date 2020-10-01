#Since there is no connection, per se, 
#the server does not need to listen for and accept connections. 
#It only needs to use bind() to associate its socket with a port, 
#and then wait for individual messages.

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
#Messages are read from the socket using recvfrom(), 
#which returns the data as well as the address of the client from which it was sent.
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)    
    print('received %s bytes from %s' % (len(data), address))
    print(sys.stderr, data)    
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address) )