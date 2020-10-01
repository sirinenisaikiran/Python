#http://man7.org/linux/man-pages/man7/socket.7.html
#https://docs.python.org/3/library/socket.html
	
import socket, threading, time, signal, sys

#add crtl-c exit
def signal_handler(signal, frame):
	# close the socket here
	tcpsock.shutdown(sockect.SHUT_RDWR)
	tcpsock.close()
	sys.exit(0)

	
signal.signal(signal.SIGINT, signal_handler)


class ClientThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print("[+] New thread started for "+ip+":"+str(port))

    def run(self):    
        print("Connection from : "+ip+":"+str(port))        
        data = "dummydata"
        while len(data):
            data = self.csocket.recv(2048).decode('utf-8')
            print("Client(%s:%s) sent : %s" % (self.ip, str(self.port), data))
            self.csocket.send( data.encode('utf-8'))  #in py2.x, encode/decode not needed
        print("Client at "+self.ip+" disconnected...")


		
#Server Socket,create an INET, STREAMing socket
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #SOCK_STREAM or SOCK_DGRAM
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # no TIME_WAIT loop




# binding
print("binding to %s @ %s" % (socket.gethostname(), 9999))
tcpsock.bind((socket.gethostname(), 9999))
tcpsock.listen(4)  # max 4 cnnection


while True:	  
	print("Listening for incoming connections...")
	(clientsock, (ip, port)) = tcpsock.accept()
	#pass clientsock to the ClientThread thread object being created
	newthread = ClientThread(ip, port, clientsock)
	newthread.start()