import socket, threading, time, signal, sys

#add crtl-c exit
def signal_handler(signal, frame):
	# close the socket here
	tcpsock.shutdown(sockect.SHUT_RDWR)
	tcpsock.close()
	sys.exit(0)

	
signal.signal(signal.SIGINT, signal_handler)

def is_prime(n):
    import math
    if n == 2 : return True 
    if n % 2 == 0:	return False
    sqrt_n = int(math.sqrt(n))
    a = [1 for i in range(3, sqrt_n + 1, 2) if n % i == 0]
    return False if sum(a) > 0 else True
    
def worker(con,addr):
    print('Connected by', addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data.strip(): 
                print("  exiting...",addr)
                return
            no = int(data.decode('ascii').strip().split()[0])
            result = str(is_prime(no))
            conn.sendall(result.encode("ascii"))
            print("    ->sent:", addr, result)
    

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #SOCK_STREAM or SOCK_DGRAM
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # no TIME_WAIT loop

s.bind((HOST, PORT))
print("listening now...")
s.listen(5)
while True:
    conn, addr = s.accept()
    t = threading.Thread(target=worker, args=(conn,addr))
    t.start()
        
        
