#netstat -an | grep '9999'

import socket ,sys


port = 9999 
size = 16
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((socket.gethostname(),port)) 

try:
    
    # Send data
    message = 'Hello Socket'
    print('sending "%s"' % message, file = sys.stderr)  #for py2.x  print >>sys.stderr, ..
    s.send(bytes(message, 'utf-8')) 

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = s.recv(size).decode('utf-8')
        amount_received += len(data)
        print('received "%s"' % data, file = sys.stderr)

finally:    
    s.close()
