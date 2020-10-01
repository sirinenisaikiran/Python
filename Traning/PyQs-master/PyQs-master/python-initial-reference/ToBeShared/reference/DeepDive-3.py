#Contents 
Socket Programming - Introduction to std lib socket 
Network programming - socket 
Socket 
SocketServer  - High level API 
Asyncore and asyncio - Networking 
tkinter 
Python GUI - RAD tools 
wxpython 
#******************************************
###Socket Programming - Introduction to std lib socket 


###Network programming - socket 
#Python's standard library releases the GIL around each blocking i/o call
#Hence threads can be created with send/recv which runs in multicore

#check socket
#low level library for TCP, UDP
import socket
dir(socket)


#high level library, Only override handle()
import socketserver  # contains TCPServer, UDPServer and as well as asynchronous 

#Http server
import http.server


#using multiprocessing.Listener, multiprocessing.Client and multiprocessing.Connection objects
#multiprocessing lib has Process, Q, Pipe, sharing data and Pool object

# multiprocessing.connection has Listener for server side and Client for client side 
#Message based API with a message boundary, Must be used with pickleable data

import multiprocesing


# Creating asynchronous Socket server and clients using asyncore module (standard module)
#asyncore.dispatcher contains below asynchronous event handlers
handle_read()  Called data to be read and readable returns true
handle_write() called when data to be written ie when writable() return true
handle_expt()  Called when there is out of band (OOB) data 
handle_connect() Called when the active opener's socket actually makes a connection. 
handle_close()  Called when the socket is closed.
handle_error()  Called when an exception is raised and not otherwise handled.
handle_accept() Called on listening channels to accept
readable()   Called each time to get bool value for interested to read
writable() Called each time to get bool value for interested to write



###Socket 

##AF Families 
['AF_APPLETALK', 'AF_DECnet', 'AF_INET', 'AF_INET6', 'AF_IPX', 'AF_IRDA', 'AF_SNA', 'AF_UNSPEC']
#address for below families 
#a hostname in Internet domain notation like 'daring.cwi.nl' 
#or address like '100.50.200.5', and port is an integer.
'AF_INET6' : (host, port, flowinfo, scopeid)
'AF_INET' : (host, port) 
##AF Proto 
>>> [f for f in dir(socket) if f.startswith('IPPROTO')]
['IPPROTO_ICMP', 'IPPROTO_IP', 'IPPROTO_RAW', 'IPPROTO_TCP', 'IPPROTO_UDP']
#AF Types 
>>> [f for f in dir(socket) if f.startswith('SOCK')]
['SOCK_DGRAM', 'SOCK_RAW', 'SOCK_RDM', 'SOCK_SEQPACKET', 'SOCK_STREAM']

##Main methods 
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
    type should be SOCK_STREAM (the default), SOCK_DGRAM, SOCK_RAW
    Returns socket object 
  
socket_instance.close()
    Mark the socket closed. 
    
#TCP server - create by socket, bind(address), listen(how_many) and accept() returns clientsock and address, then send/sendall and recv
#TCP client - create by socket, connect(address), send/sendall  and recv 
#UDP server - create by socket ,bind(address), recvfrom(buff) returns conn,address, then sendto(data,address)
#UDP client  - create by socket ,  then sendto(data,address), recvfrom(buff) returns conn,server_address
#For multi threaded, after accept returning clientsock and address, create a thread to handle clientsock and address
socket_instance.bind(address)
    Bind the socket to address
socket_instance.listen([backlog])
    Enable a server to accept connections
socket_instance.accept()
    Accept a connection  
    Returns (conn, address) 
#for TCP    
socket_instance.recv(bufsize[, flags])
    Receive data from the socket. 
    The return value is a bytes object representing the data received. 
    The maximum amount of data to be received at once is specified by bufsize.
socket_instance.send(bytes[, flags])
    Send data to the socket. 
    Returns the number of bytes sent. Applications are responsible for checking that all data has been sent;
socket_instance.sendall(bytes[, flags])
    Send data to the socket. 
    Unlike send(), this method continues to send data from bytes until either all data has been sent or an error occurs. 
socket_instance.recvmsg(bufsize[, ancbufsize[, flags]])
    Receive normal data (up to bufsize bytes) and ancillary data from the socket
    The return value is a 4-tuple: (data, ancdata, msg_flags, address). 
socket_instance.sendmsg(buffers[, ancdata[, flags[, address]]])
    Send normal and ancillary data to the socket, gathering the non-ancillary data from a series of buffers and concatenating it into a single message
socket_instance.recv_into(buffer[, nbytes[, flags]])
    Receive up to nbytes bytes from the socket, storing the data into a buffer rather than creating a new bytestring.
#For UDP
socket_instance.sendto(bytes, address)
socket_instance.sendto(bytes, flags, address)
    Send data to the socket.
socket_instance.recvfrom(bufsize[, flags])
    Receive data from the socket. 
    The return value is a pair (bytes, address) where bytes is a bytes object representing the data received and address is the address of the socket sending the data. 

socket_instance.setsockopt(level, optname, value: int)
socket_instance.setsockopt(level, optname, value: buffer)
socket_instance.setsockopt(level, optname, None, optlen: int)
    Set the value of the given socket option 
    (see the Unix  setsockopt(2)). 
    The value can be an integer, None or a bytes-like object representing a buffer.
    >> [f for f in dir(socket) if f.startswith('SO_')]
    ['SO_ACCEPTCONN', 'SO_BROADCAST', 'SO_DEBUG', 'SO_DONTROUTE', 'SO_ERROR', 
    'SO_EXLUSIVEADDRUSE', 'SO_KEEPALIVE', 'SO_LINGER', 'SO_OOBINLINE', 
    'SO_RCVBUF', 'SO_RVLOWAT', 'SO_RCVTIMEO', 'SO_REUSEADDR', 'SO_SNDBUF', 
    'SO_SNDLOWAT', 'SO_SNDTIME', 'SO_TYPE', 'SO_USELOOPBACK']

socket_instance.shutdown(how)
    Shut down one or both halves of the connection. 
    If how is SHUT_RD, further receives are disallowed. 
    If how is SHUT_WR, further sends are disallowed. 
    If how is SHUT_RDWR, further sends and receives are disallowed.
socket_instance.settimeout(value)
    Set a timeout on blocking socket operations. 
socket_instance.ioctl(control, option)
    For Windows , use this 
    Currently only the following control codes are supported: SIO_RCVALL, SIO_KEEPALIVE_VALS, and SIO_LOOPBACK_FAST_PATH.
    For other, Use fcntl.fcntl() and fcntl.ioctl() ,they accept a socket object as their first argument.
socket_instance.close()
    Mark the socket closed. 
    
    
## Utilities
socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0)
    Get address based on host and port 
    returns (family, type, proto, canonname, sockaddr)
>>> socket.getaddrinfo("example.org", 80, proto=socket.IPPROTO_TCP)
[(<AddressFamily.AF_INET6: 10>, <SocketType.SOCK_STREAM: 1>,
 6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),
 (<AddressFamily.AF_INET: 2>, <SocketType.SOCK_STREAM: 1>,
 6, '', ('93.184.216.34', 80))]

socket.gethostbyname(hostname)
    Translate a host name to IPv4 address format
socket.gethostname()
    Return a string containing the hostname of the machine where the Python interpreter is currently executing.
socket.gethostbyaddr(ip_address)
    Return a triple (hostname, aliaslist, ipaddrlist)    
socket.getprotobyname(protocolname)
    Translate an Internet protocol name (for example, 'icmp') to a constant suitable for passing as the (optional) third argument to the socket() function
socket.ntohl(x)
    Convert 32-bit positive integers from network to host byte order.
socket.htonl(x)
    Convert 32-bit positive integers from host to network byte order
socket.inet_aton(ip_string)
    Convert an IPv4 address from dotted-quad string format 
    (for example, '123.45.67.89') to 32-bit packed binary format, 
socket.inet_ntoa(packed_ip)
    Convert a 32-bit packed IPv4 address (a bytes-like object four bytes in length) 
    to its standard dotted-quad string
 

##Example - Echo server program(IPV4)
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)

##Example - Echo client program(IPV4)
import socket

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))


##Example - Echo server program(IPV4/6)
#Attaching to each interface 
import socket
import sys

HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)

##Example - Echo client program(IPV4/6)
import socket
import sys

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
with s:
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))

##Example - network sniffer with raw sockets on Windows. 
#requires administrator privileges to modify the interface:

import socket

# the public network interface
HOST = socket.gethostbyname(socket.gethostname())

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# receive a package
print(s.recvfrom(65565))

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

#For error , OSError: [Errno 98] Address already in use
#This is because the previous execution has left the socket in a TIME_WAIT state,
# and can't be immediately reused.
#Solution - There is a socket flag to set, in order to prevent this, socket.SO_REUSEADDR:

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))


##Example - UDP Echo Server(IPV4)
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

##Example - UDP Echo Client(IPV4)
#does not use connect() to attach its socket to an address. 
#It uses sendto() to deliver its message directly to the server, 
#and recvfrom() to receive the response.

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'This is the message.  It will be repeated.'

try:

    # Send data
    print('sending "%s"' % message)
    sent = sock.sendto(message, server_address)
    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received "%s"' % data)
finally:
    print('closing socket')
    sock.close()

##Example - Multi threaded Echo server program(IPV4)
# import socket programming library
import socket
 
# import thread module
import threading
 

 
# thread function
def threaded(c,print_lock):
    while True: 
        # data received from client
        data = c.recv(1024)  #in bytes 
        if not data:
            with print_lock:
                print('Bye')          
            break 
        # reverse the given string from client
        data = data[::-1] 
        # send back reversed string to client
        c.send(data) 
    # connection closed
    c.close()
 
 
def Main():
    host = ""
    print_lock = threading.RLock()
    port = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True: 
        # establish connection with client
        c, addr = s.accept() 
        # lock acquired by client
        with print_lock:
            print('Connected to :', addr[0], ':', addr[1]) 
        # Start a new thread and return its identifier
        t = threading.Thread(target=threaded, args=(c,print_lock))
        t.start()
    s.close()
 
 
if __name__ == '__main__':
    Main()

 
    

###SocketServer  - High level API 
class socketserver.TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    This uses the Internet TCP protocol, 
    which provides for continuous streams of data between the client and server. 
    If bind_and_activate is true, the constructor automatically attempts to invoke server_bind() and server_activate(). 
    The other parameters are passed to the BaseServer base class.

class socketserver.UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    This uses datagrams, which are discrete packets of information that may arrive out of order 
    or be lost while in transit. The parameters are the same as for TCPServer.

##Creating a server -Steps 
1.create a request handler class by subclassing the BaseRequestHandler class 
  and overriding its handle() method; 
  this method will process incoming requests(inside handle(), user can access many attributes)
2.instantiate one of the server classes(server), passing it the server's address 
  and the request handler class(step1)
  Then call the server.handle_request() or server.serve_forever() method of the server object 
  to process one or many requests. 
  call server.server_close()() to close the socket (unless you used a with statement) for server.handle_request()
3. For multithreaded, Use Threaded mixin and then start thread with server.serve_forever()

##Methods 
class socketserver.BaseRequestHandler
    setup()
        Called before the handle() method to perform any initialization actions 
        required. The default implementation does nothing.
    handle()
        This function must do all the work required to service a request. 
        Inside handle(), code can access below attributes 
        the request is available as self.request; 
        the client address as self.client_address; 
        and the server instance as self.server, 
        For stream services, self.request is a socket object; do, send/sendall, recv 
        for datagram services, self.request is a pair of data and socket., can do recvfrom, sendto
    finish()
        Called after the handle() method to perform any clean-up actions required. 
        The default implementation does nothing.
        If setup() raises an exception, this function will not be called.

class socketserver.BaseServer(server_address, RequestHandlerClass)
    fileno()
    handle_request()
        Process a single request. 
        This function calls the following methods in order: 
        get_request(), verify_request(), and process_request(). 
        If the user-provided handle() method of the handler class raises an exception, 
        the server's handle_error() method will be called. 
        If no request is received within timeout seconds, 
        handle_timeout() will be called and handle_request() will return.
    serve_forever(poll_interval=0.5)
        Handle requests until an explicit shutdown() request. 
        Poll for shutdown every poll_interval seconds. 
        Ignores the timeout attribute. 
        It also calls service_actions(), which may be used by a subclass 
        or mixin to provide actions specific to a given service. 
    service_actions()
        This is called in the serve_forever() loop. 
        This method can be overridden by subclasses or mixin classes 
    shutdown()
        Tell the serve_forever() loop to stop and wait until it does.
    server_close()
        Clean up the server. May be overridden.
    address_family
        The family of protocols to which the server's socket belongs. 
        Common examples are socket.AF_INET and socket.AF_UNIX.
    RequestHandlerClass
        The user-provided request handler class; 
        an instance of this class is created for each request.
    server_address
        The address on which the server is listening. 
    socket
        The socket object on which the server will listen for incoming requests.
    classvariable allow_reuse_address
        Whether the server will allow the reuse of an address. 
        This defaults to False, and can be set in subclasses to change the policy.
    classvariable request_queue_size
        The size of the request queue. If it takes a long time to process a single request, any requests that arrive while the server is busy are placed into a queue, up to request_queue_size requests. Once the queue is full, further requests from clients will get a 'Connection denied' error. The default value is usually 5, but this can be overridden by subclasses.
    classvariable socket_type
        The type of socket used by the server; socket.SOCK_STREAM and socket.SOCK_DGRAM are two common values.
    classvariable timeout
        Timeout duration, measured in seconds, or None if no timeout is desired. If handle_request() receives no incoming requests within the timeout period, the handle_timeout() method is called.
    overrideInSubclassifRequired finish_request(request, client_address)
        Actually processes the request by instantiating RequestHandlerClass and calling its handle() method.
    overrideInSubclassifRequired get_request()
        Must accept a request from the socket, and return a 2-tuple containing the new socket object to be used to communicate with the client, and the client's address.
    overrideInSubclassifRequired handle_error(request, client_address)
        This function is called if the handle() method of a RequestHandlerClass instance raises an exception. The default action is to print the traceback to standard error and continue handling further requests.
    overrideInSubclassifRequired handle_timeout()
        This function is called when the timeout attribute has been set to a value other than None and the timeout period has passed with no requests being received. The default action for forking servers is to collect the status of any child processes that have exited, while in threading servers this method does nothing.
    overrideInSubclassifRequired process_request(request, client_address)
        Calls finish_request() to create an instance of the RequestHandlerClass. If desired, this function can create a new process or thread to handle the request; the ForkingMixIn and ThreadingMixIn classes do this.
    overrideInSubclassifRequired server_activate()
        Called by the server's constructor to activate the server. The default behavior for a TCP server just invokes listen() on the server's socket. May be overridden.
    overrideInSubclassifRequired server_bind()
        Called by the server's constructor to bind the socket to the desired address. May be overridden.
    overrideInSubclassifRequired verify_request(request, client_address)
        Must return a Boolean value; if the value is True, the request will be processed, and if it's False, the request will be denied. This function can be overridden to implement access controls for a server. The default implementation always returns True.

##socketServer - Mixin 
#The mix-in class comes first
#ForkingMixin are available for Unix 
class socketserver.ForkingMixIn
class socketserver.ThreadingMixIn
    Forking and threading versions of each type of server can be created 
    using these mix-in classes. 
    #Example 
    class ThreadingUDPServer(ThreadingMixIn, UDPServer):
        pass

class socketserver.ForkingTCPServer
class socketserver.ForkingUDPServer
class socketserver.ThreadingTCPServer
class socketserver.ThreadingUDPServer
    These classes are pre-defined using the mix-in classes.
    


##Example -  socketserver.TCPServer - using BaseRequestHandler

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

##Example -  socketserver.TCPServer - using StreamRequestHandler
#using  streams (file-like objects) that simplify communication by providing the standard file interface

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        #readline calls recv() multiple times until it encounters a newline 
        #Underlying socket is self.rfile._sock 
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

##Example -  socketserver. Tcp client 
import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))



##Example -  socketserver.UDPServer 

import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()

##Example -  socketserver. UDP client 

import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))


##Example -  socketserver.TCP server using  ThreadingMixIn

import socket
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        client(ip, port, "Hello World 1")
        client(ip, port, "Hello World 2")
        client(ip, port, "Hello World 3")
        server.shutdown()

        
        
        
###Using select with sockets for asynchronous operatons



select.select(rlist, wlist, xlist[, timeout])
        rlist: wait until ready for reading
        wlist: wait until ready for writing
        xlist: wait for an 'exceptional condition' 
    Empty sequences are allowed, but acceptance of three empty sequences is platform-dependent. 
    The return value is a triple of lists of objects that are ready: 
    subsets of the first three arguments. 
    When the time-out is reached without a file descriptor becoming ready, 
    three empty lists are returned.
    on Windows, it only works for sockets; 
    on other operating systems, it also works for other file types (e.g. sys.stdin, or objects returned by open() or os.popen())
    (in particular, on Unix, it works on pipes). 
    It cannot be used on regular files to determine whether a file has grown since it was last read.


##Example echo socketserver 
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''
It returns a socket object which has the following main methods:
bind()
listen()
accept()
connect()
send()
recv()
bind(), listen() and accept() are specific for server sockets. 
connect() is specific for client sockets. 
send() and recv() are common for both types. 
'''
#Exho server 
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
conn.close()

#Client code 
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)

#Using select 
#to watch for more than one connection at a time by using select().
 

import select
import socket
import sys
import Queue

# Create a TCP/IP socket and make it nonblocking 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print( 'starting up on %s port %s' % (server_address,), file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections- 5 connections can be made 
server.listen(5)


# Sockets from which we expect to read
inputs = [ server ]

# Sockets to which we expect to write
outputs = [ ]


# Outgoing message queues (socket:Queue)
message_queues = {}


while inputs:
    # Wait for at least one of the sockets to be ready for processing
    print('\nwaiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    #The 'readable' sockets represent three possible cases. 
    #If the socket is the main 'server' socket, the one being used to listen for connections, 
    #then the 'readable' condition means it is ready to accept another incoming connection. 
    #In addition to adding the new connection to the list of inputs to monitor, 
    #this section sets the client socket to not block.

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print(new connection from', client_address,, file=sys.stderr)
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue.Queue()

        #The next case is an established connection with a client that has sent data. 
        #The data is read with recv(), then placed on the queue so it can be sent through the socket and back to the client.

        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print('received "%s" from %s' % (data, s.getpeername()), file=sys.stderr)
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)

            #A readable socket without data available is from a client that has disconnected, 
            #and the stream is ready to be closed.

            else:
                # Interpret empty result as closed connection
                print('closing', client_address, 'after reading no data', file=sys.stderr)
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]


    #There are fewer cases for the writable connections. 
    #If there is data in the queue for a connection, the next message is sent. 
    #Otherwise, the connection is removed from the list of output connections 
    #so that the next time through the loop select() does not indicate 
    #that the socket is ready to send data.

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            # No messages waiting so stop checking for writability.
            print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            outputs.remove(s)
        else:
            print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            s.send(next_msg)

    #Finally, if there is an error with a socket, it is closed.

    # Handle "exceptional conditions"
    for s in exceptional:
        print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]


#Client program 

import socket
import sys

messages = [ 'This is the message. ',
             'It will be sent ',
             'in parts.',
             ]
server_address = ('localhost', 10000)

# Create a TCP/IP socket
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          socket.socket(socket.AF_INET, socket.SOCK_STREAM),
          ]

# Connect the socket to the port where the server is listening
print('connecting to %s port %s' % server_address, file=sys.stderr)
for s in socks:
    s.connect(server_address)

for message in messages:

    # Send messages on both sockets
    for s in socks:
        print('%s: sending "%s"' % (s.getsockname(), message), file=sys.stderr)
        s.send(message)

    # Read responses on both sockets
    for s in socks:
        data = s.recv(1024)
        print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
        if not data:
            print >>sys.stderr, 'closing socket', s.getsockname()
            s.close()




##Timeouts
#When the timeout expires, select() returns three empty lists. 

    # Wait for at least one of the sockets to be ready for processing
    print('\nwaiting for the next event', file=sys.stderr)
    timeout = 1
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

    if not (readable or writable or exceptional):
        print('  timed out, do some other work here', file=sys.stderr)
        continue


#This “slow” version of the client program pauses after sending each message, 
#to simulate latency or other delay in transmission.


import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)

time.sleep(1)

messages = [ 'Part one of the message.',
             'Part two of the message.',
             ]
amount_expected = len(''.join(messages))

try:

    # Send data
    for message in messages:
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        time.sleep(1.5)

    # Look for the response
    amount_received = 0
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()



    
    
##Highlevel version - using selectors and echo servers 
#> py 3.4 
register(fileobj, events, data=None)
    fileobj is the file object to monitor. 
    It may either be an integer file descriptor or an object with a fileno() method. events is a bitwise mask of events to monitor. 
    data is an opaque object.
    events are
        EVENT_READ Available for read 
        EVENT_WRITE Available for write 
unregister(fileobj)
    Unregister a file object from selection, removing it from monitoring. 
    A file object shall be unregistered prior to being closed.
modify(fileobj, events, data=None)
    Change a registered file object’s monitored events or attached data.
select(timeout=None)
    Wait until some registered file objects become ready, or the timeout expires
    This returns a list of (key, events) tuples, one for each ready file object.
close()
    Close the selector
 
class selectors.SelectorKey
    fileobj
        File object registered.
    fd
        Underlying file descriptor.
    events
        Events that must be waited for on this file object.
    data
        Optional opaque data associated to this file object: 
    
#code 
import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)


        
        
        
        
###Asyncore and asyncio - Networking 
#Asyncore module exists for backwards compatibility only. 
#For new code use asyncio.


###Asyncio primer 
1. await can be used inside another async def/coroutine 
   result = await arg 
   where arg is A Future/Task, a coroutine or an awaitable, 'arg' is required
2. Inside main process use loop.run_until_complete(future_or_coroutine)
4. Note all methods in asyncio takes loop as argument , if not provided, uses default loop 

#Create loop, on windows , subproces is supported only in ProactorEventLoop
import sys
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()


#simple coroutines 
async def m2(*args):
    print("m2")
    return args[0:1]


async def m1(arg1,arg2):
    #option 1
    r1 = await m2(arg1)  #blocks, m2 is executed now 
    await asyncio.sleep(1)
    #option 2 with Task(is a asyncio.Future with cancel()
    fut = asyncio.ensure_future(m2(arg2))
    fut.add_done_callback(lambda f: print(f.result())) #f= future of m2(arg2)
    #or 
    r2 = await fut     #r2 is direct result 
    await asyncio.sleep(1)
    #option-3 await with with timeout
    try:
        r3 = await asyncio.wait_for(m2(arg2), timeout=None) #any float , None means blocking
    except asyncio.TimeoutError:
        print('timeout!')
    #option-4: wait for many coroutines 
    r4 = await asyncio.gather(m2(2),m2(3))   #r4 is list of result 
    return [r1,r2,r3] 

#all the above obj in 'await obj' can be passed to  'run_until_complete'
#start the events loop 
r2 = loop.run_until_complete(m1(2,3))
#or a list of many coroutines 
r2 = loop.run_until_complete(asyncio.gather(m1(2,3), m1(2,3)))
    
#To run non coroutine based function  under asyncio 
#Option-1: with executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
loop.set_default_executor(executor)

def m3(*args):
    print("m3", threading.current_thread().getName())
    time.sleep(1)
    return len(args)

#r is asyncio.Future 
r = loop.run_in_executor(None, m3, 2,3 ) #executor=None , means default executor or provide custom axecutor 
result = loop.run_until_complete(r) #await r inside coroutine 

#Option-2: with delayed call , can not return result 
h1 = loop.call_soon(m3, 2,3)
h1 = loop.call_later(2, m3, 2,3) #after 2 secs, should not exceed one day.
h1 = loop.call_at(loop.time()+3, m3, 2,3) #after 3 sec, should not exceed one day.

async def dummy():
    await asyncio.sleep(10)

#some other thread function calling normal function under asyncio
def callback(loop):
    time.sleep(1)
    loop.call_soon_threadsafe(m3, 2,3)

t = threading.Thread(target=callback, args=(loop,))
t.start()
loop.run_until_complete(dummy())
    
    
#Synchronization primitives 
#also has 
asyncio.Lock
asyncio.Event
asyncio.Condition
asyncio.Semaphore
asyncio.BoundedSemaphore
#Usage 
count = 0 
async def proc(lck):
    global count 
    async with lck:
        print("Got it")
        lc = count 
        lc += 1 
        count = lc 


lock = asyncio.Lock() # asyncio.Semaphore(2) #asyncio.BoundedSemaphore(2)
loop.run_until_complete(asyncio.gather(*[proc(lock) for i in range(10)]))


#Usage Event 
async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # Create an Event object.
    event = asyncio.Event()
    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.ensure_future(waiter(event))
    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()
    # Wait until the waiter task is finished.
    await waiter_task

loop.run_until_complete(main())
    
#Queue 
#infinte loop 
async def worker(name,queue):
    while True:
        item = await queue.get()  #blocks , get_nowait(): does not block, but raises QueueEmpty
        await asyncio.sleep(1)
        print("Got",name, item)
        queue.task_done()

async def main():
    queue = asyncio.Queue()  #maxsize=0 , means infinite 
    tasks = []
    [queue.put_nowait(i) for i in range(10)] #does not block raises QueueFull, put():no block 
    for i in range(3):
        task = asyncio.ensure_future(worker(str(i),queue))
        tasks.append(task)
    await queue.join()
    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()


loop.run_until_complete(main())    
    
#Subprocess 
async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(cmd, 'exited with ',proc.returncode)
    if stdout:
        print('[stdout]\n',stdout.decode())
    if stderr:
        print('[stderr]\n',stderr.decode())
    return stdout.decode()

async def main(urls):
    coros = [run("nslookup "+ url) for url in urls]
    #for f in asyncio.as_completed(coros): # print in the order they finish
    #    print(await f)
    #or 
    return await asyncio.gather(*coros)

urls = ["www.google.com", "www.yahoo.com", "www.wikipedia.org"]
result = loop.run_until_complete(main(urls))


    

#aiohttp
import aiohttp  #asyncio enabled http requests 

        
async def get(session, url, *args, **kwargs):  
    async with session.get(url, *args, **kwargs ) as resp:
        return (await resp.json())

async def post(session, url, *args, **kwargs):  
    async with session.post(url, *args, **kwargs ) as resp:
        return (await resp.json())

async def download_get(urls, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[get(session, url, *args, **kwargs) for url in urls])
    return results 

async def download_post(urls, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[post(session, url, *args, **kwargs) for url in urls])
    return results 

urls1 = ["http://httpbin.org/get" for i in range(10)]
urls2 = ["http://httpbin.org/post" for i in range(10)]
headers = {'Content-Type': 'application/json'}
params = { 'name': 'abc'}
data = {'name': 'xyz'}
import json 

rsults = loop.run_until_complete(download_get(urls1, params=params))        
rsults = loop.run_until_complete(download_post(urls2, data=json.dumps(params),headers=headers))        




##Complete examples with executing external commands
import asyncio, sys
import threading, concurrent.futures  #in Py2, must do, pip install futures
import os.path 
import functools,time
import asyncio.subprocess


#Create loop, on windows , subproces is supported only in ProactorEventLoop
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
loop.set_default_executor(executor)


@asyncio.coroutine
def get_date():
    code = 'import datetime; print(datetime.datetime.now())'  #python code 
    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code,  stdout=asyncio.subprocess.PIPE)
    proc = yield from create
    # Read one line of output
    data = yield from proc.stdout.readline()
    line = data.decode('ascii').rstrip()
    # Wait for the subprocess exit
    yield from proc.wait()
    return line

#asyncio.subprocess.DEVNULL, asyncio.subprocess.STDOUT, asyncio.subprocess.PIPE
'''
If PIPE is passed to stdin argument, the Process.stdin attribute will point to a StreamWriter instance.
If PIPE is passed to stdout or stderr arguments, the Process.stdout and Process.stderr attributes will point to StreamReader instances.

class asyncio.StreamReader
    coroutine read(n=-1)
    coroutine readline()
    coroutine readexactly(n)
    coroutine readuntil(separator=b'\n')
    at_eof()
class asyncio.StreamWriter
    can_write_eof()
    write_eof()
    get_extra_info(name, default=None)
    write(data)
    writelines(data)
    coroutine drain()
        writer.write(data)
        await writer.drain()
    close()
    is_closing()
    coroutine wait_closed()
'''  

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(cmd, 'exited with ',proc.returncode)
    if stdout:
        print('[stdout]\n',stdout.decode())
    if stderr:
        print('[stderr]\n',stderr.decode())
    return stdout.decode()

#Another way 
async def get_lines(shell_command):
    p = await asyncio.create_subprocess_shell(shell_command,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
    return (await p.communicate())[0].splitlines()

async def main(urls):
    coros = [run("nslookup "+ url) for url in urls]
    # get commands output concurrently
    for f in asyncio.as_completed(coros): # print in the order they finish
        print("main\n",await f)


urls = ["www.google.com", "www.yahoo.com", "www.wikipedia.org"]
        

result = loop.run_until_complete(asyncio.gather(get_date(), main(urls), *[run("nslookup "+ url) for url in urls]))
print("Current date: %s" % result[0])
loop.close()


##Asynchronous Reader and Writer - Stream based(coroutine) - High level 

class asyncio.StreamReader(limit=None, loop=None)
    Not Thread safe 
        coroutine read(n=-1)
        coroutine readline()
        coroutine readexactly(n)
        coroutine readuntil(separator=b'\n')
        feed_eof()  #Acknowledge the EOF.
        at_eof() #Return True if the buffer is empty and feed_eof() was called.
        exception()
        feed_data(data)  #Feed data bytes in the internal buffer. Any operations waiting for the data will be resumed.
        set_exception(exc)
        set_transport(transport)

class asyncio.StreamWriter(transport, protocol, reader, loop)
    Not Thread safe 
        write(data)
        writelines(data)
        write_eof()
        can_write_eof()  #Return True if the transport supports write_eof(), False if not. 
        close()
        coroutine drain()   
            Let the write buffer of the underlying transport a chance to be flushed
            #use as 
            w.write(data)
            yield from w.drain()


    
    
    
##Example -TCP echo client using streams

import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    print('Send: %r' % message)
    writer.write(message.encode())
    data = await reader.read(100)
    print('Received: %r' % data.decode())
    print('Close the connection')
    writer.close()

loop.run_until_complete(tcp_echo_client('Hello World!'))


##Example - TCP echo server using streams

import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print('Serving on ", addr')
    async with server:
        await server.serve_forever()

loop.run_until_complete(main())



##Transports are classes to abstract various kinds of communication channels - low level

#protocol_factory must be a callable returning a protocol instance.
coroutine loop.create_connection(protocol_factory, host=None, port=None, *, 
    ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, 
    server_hostname=None)
    This method is a coroutine which will try to establish the connection in the background. 
    When successful, the coroutine returns a (transport, protocol) pair.

coroutine loop.create_server(protocol_factory, host=None, port=None, *, 
    family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, 
    ssl=None, reuse_address=None, reuse_port=None)
    Return a Server object, its sockets attribute contains created sockets. 
    Use the Server.close() method to stop the server: close listening sockets.
    
coroutine loop.create_datagram_endpoint(protocol_factory, local_addr=None, 
    remote_addr=None, *, family=0, proto=0, flags=0, reuse_address=None, 
    reuse_port=None, allow_broadcast=None, sock=None)
    This method is a coroutine which will try to establish the connection in the background. 
    When successful, the coroutine returns a (transport, protocol) pair.Returns a (transport, protocol) pair.

   
coroutine loop.getaddrinfo(host, port, *, family=0, type=0, proto=0, flags=0)
    This method is a coroutine, similar to socket.getaddrinfo() function but non-blocking.

coroutine loop.getnameinfo(sockaddr, flags=0)
    This method is a coroutine, similar to socket.getnameinfo() function but non-blocking.

#below are used with Transport
coroutine asyncio.start_server(client_connected_cb, host=None, port=None, *, loop=None, limit=None, **kwds)
    Start a socket server, with a callback for each client connected. 
    The return value is the same as create_server().
    The client_connected_cb parameter is called with two parameters: client_reader, client_writer. 
    client_reader is a StreamReader object, while client_writer is a StreamWriter object. 
    The client_connected_cb parameter can either be a plain callback function or a coroutine function; 
    if it is a coroutine function, it will be automatically converted into a Task.
coroutine asyncio.open_connection(host=None, port=None, *, loop=None, limit=None, **kwds)
    A wrapper for create_connection() returning a (reader, writer) pair.
    The reader returned is a StreamReader instance; the writer is a StreamWriter instance.

    
##Protocols 
#asyncio provides base classes that you can subclass to implement your network protocols
#override certain methods

class asyncio.Protocol
    The base class for implementing streaming protocols 
    (for use with e.g. TCP and SSL transports).
class asyncio.DatagramProtocol
    The base class for implementing datagram protocols 
    (for use with e.g. UDP transports).


##State machine:
start -> connection_made() 
            [-> data_received() *] or datagram_received
                [-> eof_received() ?]  or error_received
                    -> connection_lost() -> end

##Connection callbacks - Protocol, DatagramProtocol and SubprocessProtocol
BaseProtocol.connection_made(transport)
    Called when a connection is made.
BaseProtocol.connection_lost(exc)
    Called when the connection is lost or closed.


#For Streaming protocols - Protocol
Protocol.data_received(data)
    Called when some data is received. 
Protocol.eof_received()
    Called when the other end signals it won't send any more data 
    (for example by calling write_eof(), if the other end also uses asyncio).
    
##For Datagram protocols - DatagramProtocol
DatagramProtocol.datagram_received(data, addr)
    Called when a datagram is received. 
    data is a bytes object containing the incoming data. 
    addr is the address of the peer sending the data; 
    the exact format depends on the transport.
DatagramProtocol.error_received(exc)
    Called when a previous send or receive operation raises an OSError. 
    exc is the OSError instance.


##Flow control callbacks - Protocol, DatagramProtocol and SubprocessProtocol
BaseProtocol.pause_writing()
    Called when the transport's buffer goes over the high-water mark.
BaseProtocol.resume_writing()
    Called when the transport's buffer drains below the low-water mark.
    pause_writing() and resume_writing() calls are paired 

##Transport 
class asyncio.BaseTransport
    Base class for transports.
    close()
        Close the transport. If the transport has a buffer for outgoing data, buffered data will be flushed asynchronously. No more data will be received. After all buffered data is flushed, the protocol's connection_lost() method will be called with None as its argument.
    is_closing()
        Return True if the transport is closing or is closed.
    get_extra_info(name, default=None)
        Return optional transport information. name is a string representing the piece of transport-specific information to get, default is the value to return if the information doesn't exist.
        This method allows transport implementations to easily expose channel-specific information.
            socket:
                'peername': the remote address to which the socket is connected, result of socket.socket.getpeername() (None on error)
                'socket': socket.socket instance
                'sockname': the socket's own address, result of socket.socket.getsockname()
            SSL socket:
                'compression': the compression algorithm being used as a string, or None if the connection isn't compressed; result of ssl.SSLSocket.compression()
                'cipher': a three-value tuple containing the name of the cipher being used, the version of the SSL protocol that defines its use, and the number of secret bits being used; result of ssl.SSLSocket.cipher()
                'peercert': peer certificate; result of ssl.SSLSocket.getpeercert()
                'sslcontext': ssl.SSLContext instance
                'ssl_object': ssl.SSLObject or ssl.SSLSocket instance
            pipe:
                'pipe': pipe object
            subprocess:
                'subprocess': subprocess.Popen instance
    set_protocol(protocol)
        Set a new protocol. Switching protocol should only be done when both protocols are documented to support the switch.
    get_protocol()
        Return the current protocol.

##ReadTransport
class asyncio.ReadTransport
    Interface for read-only transports.
    pause_reading()
        Pause the receiving end of the transport. No data will be passed to the protocol's data_received() method until resume_reading() is called.
    resume_reading()
        Resume the receiving end. The protocol's data_received() method will be called once again if some data is available for reading.
##WriteTransport
class asyncio.WriteTransport
    Interface for write-only transports.
    abort()
        Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol's connection_lost() method will eventually be called with None as its argument.
    can_write_eof()
        Return True if the transport supports write_eof(), False if not.
    get_write_buffer_size()
        Return the current size of the output buffer used by the transport.
    get_write_buffer_limits()
        Get the high- and low-water limits for write flow control. Return a tuple (low, high) where low and high are positive number of bytes.
        Use set_write_buffer_limits() to set the limits.
    set_write_buffer_limits(high=None, low=None)
        Set the high- and low-water limits for write flow control.
        These two values (measured in number of bytes) control when the protocol's pause_writing() and resume_writing() methods are called. If specified, the low-water limit must be less than or equal to the high-water limit. Neither high nor low can be negative.
        pause_writing() is called when the buffer size becomes greater than or equal to the high value. If writing has been paused, resume_writing() is called when the buffer size becomes less than or equal to the low value.
        The defaults are implementation-specific. If only the high-water limit is given, the low-water limit defaults to an implementation-specific value less than or equal to the high-water limit. Setting high to zero forces low to zero as well, and causes pause_writing() to be called whenever the buffer becomes non-empty. Setting low to zero causes resume_writing() to be called only once the buffer is empty. Use of zero for either limit is generally sub-optimal as it reduces opportunities for doing I/O and computation concurrently.
        Use get_write_buffer_limits() to get the limits.
    write(data)
        Write some data bytes to the transport.
        This method does not block; it buffers the data and arranges for it to be sent out asynchronously.
    writelines(list_of_data)
        Write a list (or any iterable) of data bytes to the transport. This is functionally equivalent to calling write() on each element yielded by the iterable, but may be implemented more efficiently.
    write_eof()
        Close the write end of the transport after flushing buffered data. Data may still be received.
        This method can raise NotImplementedError if the transport (e.g. SSL) doesn't support half-closes.
##DatagramTransport
DatagramTransport.sendto(data, addr=None)
    Send the data bytes to the remote peer given by addr (a transport-dependent target address). If addr is None, the data is sent to the target address given on transport creation.
    This method does not block; it buffers the data and arranges for it to be sent out asynchronously.
DatagramTransport.abort()
    Close the transport immediately, without waiting for pending operations to complete. Buffered data will be lost. No more data will be received. The protocol's connection_lost() method will eventually be called with None as its argument.

    
    
##Example - TCP echo client 
#TCP echo client using the loop.create_connection() method, 
#send data and wait until the connection is closed:

import asyncio

#start -> connection_made(transport) 
#            [-> data_received(data) *] 
#                [-> eof_received() ?] 
#                    -> connection_lost(exc) -> end
class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'Hello World!'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()

##Example - TCP echo server 
#start -> connection_made(transport) 
#            [-> data_received(data) *] 
#                [-> eof_received() ?] 
#                    -> connection_lost(exc) -> end
import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


##Example - UDP echo client
#start -> connection_made(transport) 
#            [-> datagram_received(data) *] 
#                [-> error_received() ?] 
#                    -> connection_lost(exc) -> endUDP echo client protocol


import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()
message = "Hello World!"
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()


##Example - UDP echo server protocol
#start -> connection_made(transport) 
#            [-> datagram_received(data) *] 
#                [-> error_received() ?] 
#                    -> connection_lost(exc) -> endUDP echo client protocol

import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

loop = asyncio.get_event_loop()
print("Starting UDP server")
# One protocol instance will be created to serve all client requests
listen = loop.create_datagram_endpoint(
    EchoServerProtocol, local_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()





###Gevent based socket 
#http://www.gevent.org/intro.html
#Examples 
#gevent is a coroutine -based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev or libuv event loop
#replacement of asyncio 

#Use gevent socket 
import gevent
from gevent import socket
urls = ['www.google.com', 'www.example.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
>>> [job.value for job in jobs]
['74.125.79.106', '208.77.188.166', '82.94.164.162']

#Example 
"""Resolve hostnames concurrently, exit after 2 seconds.

Under the hood, this might use an asynchronous resolver based on
c-ares (the default) or thread-pool-based resolver.

You can choose between resolvers using GEVENT_RESOLVER environment
variable. To enable threading resolver:

    GEVENT_RESOLVER=thread python dns_mass_resolve.py
"""
from __future__ import print_function
import gevent
from gevent import socket
from gevent.pool import Pool

N = 1000
# limit ourselves to max 10 simultaneous outstanding requests
pool = Pool(10)
finished = 0


def job(url):
    global finished
    try:
        try:
            ip = socket.gethostbyname(url)
            print('%s = %s' % (url, ip))
        except socket.gaierror as ex:
            print('%s failed with %s' % (url, ex))
    finally:
        finished += 1

with gevent.Timeout(2, False):
    for x in range(10, 10 + N):
        pool.spawn(job, '%s.com' % x)
    pool.join()

print('finished within 2 seconds: %s/%s' % (finished, N))


##How to use with python socket and subprocess which are not co-routine based 
#When monkey patching, it is recommended to do so as early as possible 
from gevent import monkey; monkey.patch_socket()
import urllib2 # it's usable from multiple greenlets now

#OR 
from gevent import monkey; monkey.patch_all()
import subprocess # it's usable from multiple greenlets now

#Reqeuests Example 
from __future__ import print_function
import gevent
from gevent import monkey

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import requests

# Note that we're using HTTPS, so
# this demonstrates that SSL works.
urls = [
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/'
]



def print_head(url):
    print('Starting %s' % url)
    data = requests.get(url).text
    print('%s: %s bytes: %r' % (url, len(data), data[:50]))

jobs = [gevent.spawn(print_head, _url) for _url in urls]

gevent.wait(jobs)

#Subprocess 
from __future__ import print_function
import gevent
from gevent import subprocess

import sys

# run 2 jobs in parallel
p1 = subprocess.Popen(['dir'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['dir'], stdout=subprocess.PIPE)

gevent.wait([p1, p2], timeout=2)

# print the results (if available)
if p1.poll() is not None:
    print('uname: %r' % p1.stdout.read())
else:
    print('uname: job is still running')
if p2.poll() is not None:
    print('ls: %r' % p2.stdout.read())
else:
    print('ls: job is still running')

p1.stdout.close()
p2.stdout.close()



##Echoserver.py 
#!/usr/bin/env python
"""Simple server that listens on port 16000 and echos back every input to the client.

Connect to it with:
  telnet 127.0.0.1 16000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from __future__ import print_function
from gevent.server import StreamServer


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    print('New connection from %s:%s' % address)
    socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    rfileobj = socket.makefile(mode='rb')
    while True:
        line = rfileobj.readline()
        if not line:
            print("client disconnected")
            break
        if line.strip().lower() == b'quit':
            print("client quit")
            break
        socket.sendall(line)
        print("echoed %r" % line)
    rfileobj.close()

if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('127.0.0.1', 16000), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print('Starting echo server on port 16000')
    server.serve_forever()


    
    

    
    
    
    

###tkinter 
##Steps:
1. Create root= tk.Tk() , configure by .configure(attr=value), .geometry('nxn')
2. Creat a class derived from tk.Frame , call tk.Frame 's __init__ 
   Frame parent is 'root', Use self.pack()/.grid() for placement of Frame (preferred grid)
   Any number of Frame can be created, place them as required
   For .grid(), use parent(ie root).rowconfigure/.columnconfigure to configure row/column 
   Note each Frame must be same way managed by .grid or .pack (don't mix)
3. Create all controls inside Frame or root or TopLevel (use parent correctly eg frame self  )
   Each control has 'command' key with a python call back , gets called when clicked 
   Use control.pack()/.grid() for placement of Frame (preferred grid)
   Any number of Controls can be created, place them as required
   For .grid(), use parent.rowconfigure/.columnconfigure to configure row/column 
   Controls are created by passing it's attrb as keyword arg of Constructor 
   or by .configure(attr=value), Check all values by widget.keys()
4. Create tk.Menu instance and add_command for adding top level  menu command 
   or add_cascade for pull down menu with another tk.Menu instance 
   Each Menu  has 'command' key with a python call back ,gets called when clicked 
   Add above instance to root or Toplevel instance via .configure(menu=instance)
5. Bind any event to any control or root by 
   widget.bind(event, callback_taking_event_as_arg)  
5. call root.mainloop() for starting GUI loop    

##tkinter - constants and Tk 
>>> dir(tkinter.constants)
['ACTIVE', 'ALL', 'ANCHOR', 'ARC', 'BASELINE', 'BEVEL', 'BOTH', 'BOTTOM', 
'BROWSE', 'BUTT', 'CASCADE', 'CENTER', 'CHAR', 'CHECKBUTTON', 'CHORD', 
'COMMAND', 'CURRENT', 'DISABLED', 'DOTBOX', 'E', 'END', 'EW', 'EXTENDED', 
'FALSE', 'FIRST', 'FLAT', 'GROOVE', 'HIDDEN', 'HORIZONTAL', 'INSERT', 
'INSIDE', 'LAST', 'LEFT', 'MITER', 'MOVETO', 'MULTIPLE', 'N', 'NE', 'NO', 
'NONE', 'NORMAL', 'NS', 'NSEW', 'NUMERIC', 'NW', 'OFF', 'ON', 'OUTSIDE', 
'PAGES', 'PIESLICE', 'PROJECTING', 'RADIOBUTTON', 'RAISED', 'RIDGE', 'RIGHT', 
'ROUND', 'S', 'SCROLL', 'SE', 'SEL', 'SEL_FIRST', 'SEL_LAST', 'SEPARATOR', 
'SINGLE', 'SOLID', 'SUNKEN', 'SW', 'TOP', 'TRUE', 'UNDERLINE', 'UNITS', 
'VERTICAL', 'W', 'WORD', 'X', 'Y', 'YES', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']


class tkinter.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    This creates a toplevel widget of Tk which usually is the main window of an application. 
    Each instance has its own associated Tcl interpreter.
    Every Widgets must have a parent widget eg root widget 

##http://www.java2s.com/Code/Python/GUI-Tk/
##tkinter - Quick Code - 1
from tkinter import *

root = Tk()
w = Label(root, text="Hello, world!")
w.pack()			# make it visible
root.mainloop()     #start event main loop 


##tkinter - Quick Code -  2

from tkinter import *

class App:
    def __init__(self, master):
        self.root = master
        frame = Frame(master)
        frame.pack()
        self.button = Button( frame, text="QUIT", fg="red", command=self.quit  )
        self.button.pack(side=LEFT)
        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)
    def say_hi(self):
        print("hi there, everyone!")
    def quit(self):
        self.root.destroy()

root = Tk()
app = App(root)
root.mainloop()

##tkinter - Quick Code - 3
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",  command=root.destroy)
        self.quit.pack(side="bottom")
    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = App(master=root)
app.mainloop()

##tkinter - Base Windows
#the root window 
root = Tk()

#additional windows- Toplevel widget 
#Don't use pack to display the Toplevel, it is displayed automatically
top = Toplevel() # behaves like root and use this for creating other


##tkinter - Message Boxes
messagebox.function(title, message [, options]). 
    Open a dialog with 'message' with yes and no button 
    returns 'yes' 'no'
#Exmaple 
>>> import tkinter.messagebox
>>> tkinter.messagebox.askquestion('title','question') #askquestion(title=None, message=None, **options)
'yes'

>>> dir(tkinter.messagebox)
['ABORT', 'ABORTRETRYIGNORE', 'CANCEL', 'Dialog', 'ERROR', 'IGNORE', 'INFO', 
'Message', 'NO', 'OK', 'OKCANCEL', 'QUESTION', 'RETRY', 'RETRYCANCEL', 
'WARNING', 'YES', 'YESNO', 'YESNOCANCEL', '__builtins__', 
'__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_show', 
'askokcancel','askquestion', 'askretrycancel', 'askyesno', 'askyesnocancel', 
'showerror', 'showinfo', 'showwarning']

#The askquestion function returns the strings 'yes' or 'no' 
#(you can use options to modify the number and type of buttons shown), 
#while the others return a true value of the user gave a positive answer 
#(ok, yes, and retry, respectively).

>>> tkinter.messagebox.askyesno("Print", "Print this report?")
True



##tkinter - Configure options of a widget
#creation time 
fred = Button(self, fg = "red", bg = "blue")

#after creation like dict 
fred["fg"] = "red"
fred["bg"] = "blue"

#OR Use the config() 
fred.config(fg = "red", bg = "blue")

#Check all options of widget by instance.keys()(does not have items() or values()!!)
Button().keys()
Button().config()  #dict, key=option, 
                   #for real option, value=(option name,option name for database lookup,option class for database lookup,default value,current value)
                   #for shortcut option name, value = (name of synonym, real option)

##tkinter - core widgets
#tkinter supports 15 core widgets
#There's no widget class hierarchy in tkinter; 
#all widget classes are siblings in the inheritance tree.
Button
    A simple button, used to execute a command or other operation.
Canvas
    Structured graphics. 
    This widget can be used to draw graphs and plots, create graphics editors, 
    and to implement custom widgets.
Checkbutton
    Represents a variable that can have two distinct values. 
    Clicking the button toggles between the values.
Entry
    A text entry field.
Frame
    A container widget. 
    The frame can have a border and a background, 
    and is used to group other widgets when creating an application 
    or dialog layout.
Label
    Displays a text or an image.
Listbox
    Displays a list of alternatives. 
    The listbox can be configured to get radiobutton or checklist behavior.
Menu
    A menu pane. Used to implement pulldown and popup menus.
Menubutton
    A menubutton. Used to implement pulldown menus.
Message
    Display a text. Similar to the label widget, 
    but can automatically wrap text to a given width or aspect ratio.
Radiobutton
    Represents one value of a variable that can have one of many values. 
    Clicking the button sets the variable to that value, 
    and clears all other radiobuttons associated with the same variable.
Scale
    Allows you to set a numerical value by dragging a 'slider'.
Scrollbar
    Standard scrollbars for use with canvas, entry, listbox, and text widgets.
Text
    Formatted text display. 
    Allows you to display and edit text with various styles and attributes. 
    Also supports embedded images and windows.
Toplevel
    A container widget displayed as a separate, top-level window.
LabelFrame
    A variant of the Frame widget that can draw both a border and a title.
PanedWindow
    A container widget that organizes child widgets in resizable panes.
    SpinboxA variant of the Entry widget for selecting values from a range 
    or an ordered set.

##tkinter - Other modules 
tkinter.scrolledtext    Text widget with a vertical scroll bar built in.
tkinter.colorchooser    Dialog to let the user choose a color.
tkinter.commondialog    Base class for the dialogs defined in the other modules listed here.
tkinter.filedialog      Common dialogs to allow the user to specify a file to open or save.
tkinter.font            Utilities to help work with fonts.
tkinter.messagebox      Access to standard Tk dialog boxes.
tkinter.simpledialog    Basic dialogs and convenience functions.
tkinter.dnd             Drag-and-drop support for tkinter. This is experimental and should become deprecated when it is replaced with the Tk DND.
turtle                  Turtle graphics in a Tk window. 


##tkinter - Option's values that can be  used in Tk 
anchor
    Legal values are points of the compass: 
    "n", "ne", "e", "se", "s", "sw", "w", "nw", and also "center".
bitmap
    There are eight built-in, named bitmaps: 
    'error', 'gray25', 'gray50', 'hourglass', 'info', 'questhead', 'question', 'warning'. 
    To specify an X bitmap filename, give the full path to the file, 
    preceded with an @, as in "@/usr/contrib/bitmap/gumby.bit".
boolean
    You can pass integers 0 or 1 or the strings "yes" or "no".
callback
    This is any Python function that takes no arguments
    def print_it():
        print("hi there")
    fred["command"] = print_it
color
    Colors can be given as the names of X colors in the http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    or as strings representing RGB values in 4 bit: "#RGB", 
    8 bit: "#RRGGBB", 12 bit "#RRRGGGBBB", or 16 bit "#RRRRGGGGBBBB" ranges, 
    where R,G,B here represent any legal hex digit. 
cursor
    The standard X cursor names from cursorfont.h can be used(https://github.com/enthought/tk/blob/master/xlib/X11/cursorfont.h)
    without the XC_ prefix. 
    For example to get a hand cursor (XC_hand2), use the string "hand2". 
    You can also specify a bitmap and mask file of your own. 
distance
    Screen distances can be specified in either pixels or absolute distances. 
    Pixels are given as numbers and absolute distances as strings, 
    with the trailing character denoting units: 
    c for centimetres, i for inches, m for millimetres, p for printer's points. 
    For example, 3.5 inches is expressed as "3.5i".
region
    This is a string with four space-delimited elements, 
    each of which is a legal distance (see above). 
    For example: "2 3 4 5" and "3i 2i 4.5i 2i" and "3c 2c 4c 10.43c" 
    are all legal regions.
font
    Tk uses a list font name format, eg 
    ("Helvetica", "16") for a 16-point Helvetica regular.
    ("Times", "24", "bold italic") for a 24-point Times bold italic.
    Font sizes with positive numbers are measured in points; 
    sizes with negative numbers are measured in pixels.
    Or use 
    >>> from tkinter import Tk, font
    >>> root = Tk()
    >>> font.families()
    ('Terminal', 'System', 'Fixedsys', 'Modern', 'Script', 'Roman', 'Courier',...)
    >>> root = Tk()
    >>> font.names()
    ('fixed', 'oemfixed', 'TkDefaultFont', 'TkMenuFont', 'ansifixed', 'systemfixed'..
    #Create a font 
    helv2 = font.Font(family="Helvetica",size=36,weight="bold")
    #args 
    font -- font specifier ,name, system font, or (family, size, style)-tuple 
    or below 
    family      -- font 'family', e.g. Courier, Times, Helvetica
    size        -- font size in points
    weight      -- font thickness: NORMAL, BOLD
    slant       -- font slant: ROMAN, ITALIC
    underline   -- font underlining: false (0), true (1)
    overstrike  -- font strikeout: false (0), true (1)    
geometry
    This is a string of the form widthxheight, or widthxheight+x+y
    where width and height are measured in pixels for most widgets 
    (in characters for widgets displaying text). 
    For example: fred["geometry"] = "200x100".
justify
    Legal values are the strings: "left", "center", "right", and "fill".
relief
    Determines what the border style of a widget will be. 
    Legal values are: "raised", "sunken", "flat", "groove", and "ridge".
scrollcommand
    This is almost always the set() method of some scrollbar widget, 
    but can be any widget method that takes a single argument.
wrap:
    Must be one of: "none", "char", or "word".

    
    
##tkinter - widgets -Layout methods 
#Each widget has three layout management methods
w_instance.pack(...)
    organises widgets in horizontal and vertical boxes
w_instance.grid(...) 	
    places widgets in a two dimensional grid
w_instance.place(...) 	
    places widgets on their containers using absolute positioning inside parent widget 

##tkinter - TK pack options
#for situations:
1.Put a widget inside a frame (or any other container widget), 
  and have it fill the entire frame
2.Place a number of widgets on top of each other OR 
3.Place a number of widgets side by side
#Use eirther of LEFT and RIGHT for horizontal   or TOP and BOTTOM for vertical 
#note if only LEFT/RIGHT (or TOP/BOTTOM) is used then all are sized into horizontal (or vertical)
#if LEFT and TOP are mixed, final configuration is created combination of those, but check out visually
anchor=
    Where the widget is placed inside the packing box. Default is CENTER.
expand=
    Specifies whether the widgets should be expanded to fill any extra space 
    in the geometry master. If false (default), the widget is not expanded.
fill=
    Specifies whether the widget should occupy all the space provided to it 
    by the master. If NONE (default), keep the widget's original size. 
    If X (fill horizontally), Y (fill vertically), 
    or BOTH, fill the given space along that direction. 
in=
    Pack this widget inside the given widget. 
    This option should usually be left out, in which case the widget is packed inside its parent. 
ipadx=, ipady=
    Internal x,y padding. 
    This dimension is added inside the widget inside its left and right sides.  
padx=, pady=
    External x padding. 
    This dimension is added to the left and right outside the widget.  
side=
    Specifies which side to pack the widget against. TOP or BOTTOM OR LEFT or RIGHT
    To pack widgets vertically, use TOP (default). 
    To pack widgets horizontally, use LEFT. 
    
#http://www.java2s.com/Code/Python/GUI-Tk/LayoutanchorNWWandE.htm
#Example 
#displayed as 
        Top 
        Center 
        Bottom 
Left   This is center Botton    Right 

#fill= BOTH means full widget area would be filled, X means only X direction etc 
#Expand = Yes means expands to fill component location 
#
#Code 
from tkinter import *

class App:
    def __init__(self, master):
        fm = Frame(master)
        Button(fm, text='Top').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='Left').pack(side=LEFT)
        Button(fm, text='This is the Center button').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)        
        fm.pack(fill=BOTH, expand=YES)
        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 12")
display = App(root)
root.mainloop()

#Example - 2 
#Display 
side=TOP, anchor=NW
side=TOP,                   anchor=W
                  side=TOP, anchor=E
#code 
from tkinter import *

class App:
    def __init__(self, master):
        master.geometry("300x200")
        fm = Frame(master)
        Button(fm, text='side=TOP, anchor=NW').pack(side=TOP, anchor=NW, expand=YES)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='side=TOP, anchor=E').pack(side=TOP, anchor=E, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

        
root = Tk()
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 11")
display = App(root)
root.mainloop()


    

##tkinter - grid options
#Note row, column starts from zero and increases by 1 (take rowspan and columnspan into account, like matplotlib)
#grid() is called on widget, but rowconfigure/columnconfigure is called on widget.parent 
row 
    The row number into which you want to insert the widget, counting from 0. 
    The default is the next higher-numbered unoccupied row. 
column 
    The column number where you want the widget gridded, counting from zero. 
    The default value is zero.  
columnspan 
    For example, w.grid(row=0, column=2, columnspan=3) 
    would place widget w in a cell that spans columns 2, 3, and 4 of row 0.  
in, ipadx , ipady  ,padx  ,pady 
    similar to pack options  
rowspan 
    For example, w.grid(row=3, column=2, rowspan=4, columnspan=5) 
    would place widget w in an area formed by merging 20 cells, 
sticky 
    the default behavior is to center the widget in the cell. 
    Example 
    sticky=tk.NE (means top right), tk.SE (bottom right), 
        tk.SW (bottom left), or tk.NW (top left). 
    sticky=tk.N (top center), tk.E (right center), tk.S (bottom center), 
        or tk.W (left center). 
    Use sticky=tk.N+tk.S to stretch the widget vertically 
        but leave it centered horizontally. 
    Use sticky=tk.E+tk.W to stretch it horizontally
        but leave it centered vertically. 
    To automatically resize, use
    parent_widget.rowconfigure(row_number, weight = 1) 
        for all rows if you want row to be resized
    parent_widget.columnconfigure(column_number, weight = 1) 
        for all columns if you want column to be resized
    Options on rowconfigure/columnconfigure 
        minsize  
            The column or row's minimum size in pixels. 
            If there is nothing in the given column or row, it will not appear, even if you use this option.  
        pad  
            A number of pixels that will be added to the given column or row, over 
            and above the largest cell in the column or row.  
        weight  
            To make a column or row stretchable, use this option 
            and supply a value that gives the relative weight of this column or row 
            when distributing the extra space. 
            For example, if a widget w contains a grid layout, 
            these lines will distribute three-fourths of the extra space to the first column 
            and one-fourth to the second column:     
            w.columnconfigure(0, weight=3)
            w.columnconfigure(1, weight=1)
            If this option is not used, the column or row will not stretch.  


#Example 
import tkinter
root = tkinter.Tk(  )
for r in range(3):
    for c in range(4):
        tkinter.Label(root, text='R%s/C%s'%(r,c),borderwidth=1 ).grid(row=r,column=c)

root.mainloop(  )

##Note 
1.Rows and columns are made large enough to fit the largest widget. 
2.Using default values for row and column. 
  The first two labels use default values for the row and column options. 
  As a result, they are both placed in column 0, in the rows 0 and 1.
3.You can place the widgets into the grid in any order. 
  It’s only the row and column numbers that count 
  you can also leave empty rows and columns 
4.Use sticky=N+E+W+S if frame is packed fully with controls
  Else use accordingly such as that side is not streatched
5. Use rowconfigure/columnconfigure for fitting during resizing 
   Note this caled on parent widget whereas grid is called on widget 
   row/column starts from zero
   rowconfigure/columnconfigure should be done for row/column 
   starting from 0 to finalrow/column+rowspan/columnspan 
  
#code 
from tkinter import *
root = Tk()
w = Label(root, text="Additive:")
w.grid(sticky=E)  #row=0,col=0
w = Label(root, text="Subtractive:")
w.grid(sticky=E) #row=1,col=0

w = Label(root, text="Cyan", bg="cyan", height=2)
w.grid(row=1, column=1)
w = Label(root, text="Magenta", bg="magenta", fg="white")
w.grid(row=1, column=2)
w = Label(root, text="Yellow", bg="yellow", height=2)
w.grid(row=1, column=3)

w = Label(root, text="Red", bg="red", fg="white", height=2)
w.grid(row=0, column=1)
w = Label(root, text="Green", bg="green", height=3)
w.grid(row=0, column=2)
w = Label(root, text="Blue", bg="blue", fg="white")
w.grid(row=0, column=3)
mainloop()


##Rows, Columns, and Cells 
#The grid_size method returns 
#the number of columns and rows allocated by the grid manager. 
#use this function to add new rows (or columns) to a grid:
def add_entry(master, text):
    column, row = master.grid_size()
    label = Label(master, text=text)
    label.grid(row=row, column=0, sticky=E, padx=2)
    entry = Entry(master)
    entry.grid(row=row, column=1, sticky=E+W)
    return entry

##Expanding and Filling
#By default, the grid manager lets each widget keep its natural size . 
#If the cell turns out to be larger than this size, 
#the widget is placed in the middle of the cell.
#use the sticky option to modify this behavior. 
#This option tells the geometry manager to “attach” the widget to one or more of the cell borders.
#For example, “ns” stretches the widget vertically, while “we” stretches it horizontally. 
#Finally, “nswe” makes the widget fill the entire cell.

##Don't mix pack and grid 


#Complex grid Example 
#http://www.java2s.com/Code/Python/GUI-Tk/Gridlayoutmanagerdemonstration.htm


from tkinter import *

class GridDemo( Frame ):
   def __init__( self ):
      Frame.__init__( self )
      self.master.title( "Grid Demo" )

      self.master.rowconfigure( 0, weight = 1 )
      self.master.columnconfigure( 0, weight = 1 )
      self.grid( sticky = W+E+N+S )
  
      self.text1 = Text( self, width = 15, height = 5 )

      self.text1.grid( rowspan = 3, sticky = W+E+N+S )
      self.text1.insert( INSERT, "Text1" )

      self.button1 = Button( self, text = "Button 1", width = 25 )
      self.button1.grid( row = 0, column = 1, columnspan = 2, sticky = W+E+N+S )

      self.button2 = Button( self, text = "Button 2" )
      self.button2.grid( row = 1, column = 1, sticky = W+E+N+S )

      self.button3 = Button( self, text = "Button 3" )
      self.button3.grid( row = 1, column = 2, sticky = W+E+N+S )

      self.button4 = Button( self, text = "Button 4" )
      self.button4.grid( row = 2, column = 1, columnspan = 2, sticky = W+E+N+S )

      self.entry = Entry( self )
      self.entry.grid( row = 3, columnspan = 2, sticky = W+E+N+S )
      self.entry.insert( INSERT, "Entry" )

      self.text2 = Text( self, width = 2, height = 2 )
      self.text2.grid( row = 3, column = 2, sticky = W+E+N+S )
      self.text2.insert( INSERT, "Text2" )

      self.rowconfigure( 1, weight = 1 )
      self.columnconfigure( 1, weight = 1 )

def main():
   GridDemo().mainloop()   

if __name__ == "__main__":
   main()

#Example 
from tkinter import *

rows = []
for i in range(5):
    cols = []
    for j in range(4):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END, '%d.%d' % (i, j))
        cols.append(e)
    rows.append(cols)

def onPress():
    for row in rows:
        for col in row:
            print col.get(),
        print

Button(text='Fetch', command=onPress).grid()
mainloop()



##tkinter - place options 
in=master or in_=master 
    master relative to which the widget is placed
x=amount 
    locate anchor of this widget at position x of master
y=amount 
    locate anchor of this widget at position y of master
relx=amount 
    locate anchor of this widget between 0.0 and 1.0
    relative to width of master (1.0 is right edge)
rely=amount 
    locate anchor of this widget between 0.0 and 1.0
    relative to height of master (1.0 is bottom edge)
anchor=NSEW (or subset) 
    position anchor according to given direction
width=amount 
    width of this widget in pixel
height=amount
    height of this widget in pixel
relwidth=amount 
    width of this widget between 0.0 and 1.0
    relative to width of master (1.0 is the same width
    as the master)
relheight=amount 
    height of this widget between 0.0 and 1.0
    relative to height of master (1.0 is the same
    height as the master)
bordermode="inside" or "outside" 
    whether to take border width of
    master widget into account


##tkinter - Coupling Widget Variables to application variables (eg textentry widget)
#Configuration keys  are variable, textvariable, onvalue, offvalue, and value. 
#This connection works both ways

#Handling variable or textvariable : application variable must subclass tkinter.Variable
#builtin subclass : StringVar, IntVar, DoubleVar, and BooleanVar
#uset .get() to value and .set() to set value 

from tkinter import * 
class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()        
        self.entrythingy = Entry()
        self.entrythingy.pack()
        # here is the application variable
        self.contents = StringVar()
        # set it to some value
        self.contents.set("this is a variable")
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents
        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Key-Return>',self.print_contents)
    def print_contents(self, event):
        print("hi. contents of entry is now ---->",self.contents.get())

root = Tk()
app = App(master=root)
app.mainloop()
#OR 
app = App()
app.mainloop() 

##tkinter - The Window Manager
#allows to control titles, placement, icon bitmaps etc of top level window 

#To get at the toplevel window(if not packed inside Frame) , use .master (parent window) 
#for an arbitrary widget, use  ._root() method. 


import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()





##tkinter - The index Parameter of many widgets 
#For example : to point at a specific place in a Text widget, 
#or to particular characters in an Entry widget, 
#or to particular menu items in a Menu widget.

Entry widget indexes (index, view index, etc.)
    The entry widget is used to enter text strings. 
    This widget allows the user to enter one line of text, in a single font.
    To enter multiple lines of text, use the Text widget.
    index:(http://effbot.org/tkinterbook/entry.htm)
    •Numerical indexes- 0 and upwards or slice (0,5) like python slice
    •ANCHOR
    •END
    •INSERT
    •Mouse coordinates :"@%d" % x where x is given in pixels relative to the left edge of the entry widget.
    #Example 
    e = Entry(master)
    e.pack()
    e.delete(0, END)  #both are indexes 
    e.insert(0, "a default value") #firstarg is index 
    #To fetch the current entry text, use the get method:
    s = e.get()
    #OR StringVar instance, and set or get the entry text via that variable:
    v = StringVar()
    e = Entry(master, textvariable=v)
    e.pack()
    v.set("a default value")
    s = v.get()


    
Text widget indexes
    Check http://effbot.org/tkinterbook/text.htm
    http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/text-index.html
    indexes are used in amny methods 
        insert(index, text, *tags)
        search(pattern, index, stopindex=None, forwards=None, backwards=None, exact=None, regexp=None, nocase=None, count=None)
        see(index)
        delete(start, end=None) #both are index 
        get(start, end=None) #both are index 
    Example 
        text.insert(END, "hello, ")
        text.insert(END, "world")
        button = Button(text, text="Click", command=click)
        text.window_create(INSERT, window=button)
        text.delete(1.0, END)
        text.delete(INSERT) #single char 
        text.delete(button)
        contents = text.get(1.0, END)
        #with enable disable 
        text.config(state=NORMAL)
        text.delete(1.0, END)
        text.insert(END, text)
        text.config(state=DISABLED)
        #search 
        text.insert(END, "hello, world")
        start = 1.0
        while 1:
            pos = text.search("o", start, stopindex=END)
            if not pos:
                break
            print pos
            start = pos + "+1c"
    index:         
        •line/column (format line.column), line starts from 1, column starts from 0
        •line end ('line.end') , line starts from 1 
        •INSERT  : corresponds to the insertion cursor.
        •CURRENT :corresponds to the mouse pointer
        •END :corresponds to the position just after the last character 
        •user-defined marks
            corresponds to named positions in the text
        •user-defined tags ('tag.first', 'tag.last')
            represent special event bindings and styles that can be assigned to ranges of text
            beginning of a tag range using the syntax 'tag.first' (just before the first character in the text using that tag), and 'tag.last' (just after the last character using that tag).
            "%s.first" % tagname
            "%s.last" % tagname
        •selection (SEL_FIRST, SEL_LAST)
            SEL (or 'sel') that corresponds to the current selection. 
            You can use the constants SEL_FIRST and SEL_LAST to refer to the selection
        •window coordinate ('@x,y')
            "@%d,%d" % (event.x, event.y)
        •embedded object name (window, images)
            Use the corresponding tkinter widget instance as an index. 
            To refer to an embedded image, use the corresponding tkinter PhotoImage or BitmapImage object
        •expressions
            eg '+ count chars' moves the index forward


        
Menu indexes 
    check http://effbot.org/tkinterbook/menu.htm
    Example methods 
        delete(index1, index2=None) 
        invoke(index)
        insert(index, itemType, **options) , like  add(type, **options) but with index 
        activate(index)
    Some options and methods for menus manipulate specific menu entries. 
    Anytime a menu index is needed for an option or a parameter, 
    you may pass in:
        1.an integer which refers to the numeric position of the entry in the widget, counted from the top, starting with 0;
        2.the string "active", which refers to the menu position that is currently under the cursor;
        3.the string "last" which refers to the last menu item;
        4.An integer preceded by @, as in @6, where the integer is interpreted as a y pixel coordinate in the menu's coordinate system;
        5.the string "none", which indicates no menu entry at all, most often used with menu.activate() to deactivate all entries, 
        6.a text string that is pattern matched against the label of the menu entry, as scanned from the top of the menu to the bottom. 
          Note that this index type is considered after all the others, 
          which means that matches for menu items labelled last, active, or none may be interpreted as the above literals, instead.
       
          
          
          
          
          
          
          
          
##tkinter - Image object to be used with image= of labels, buttons, menus etc 
tkinter.BitmapImage 
    can be used for X11 bitmap data.
tkinter.PhotoImage(name=None, cnf={}, master=None, **kw)
    can be used for GIF and PPM/PGM color bitmaps.,
    Create an image with NAME.
    Valid resource names: data, format, file, gamma, height, palette,width. 
    eg photo = PhotoImage(file="image.gif")
    photo = """
    R0lGODdhEAAQAIcAAAAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4O
    Dg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEh
    ...
    AfjHtq1bAP/i/gPwry4AAP/yAtj77x+Af4ABAwDwrzAAAP8SA/j3DwCAfwAA/JsM4J/lfwD+/QMA
    4B8AAP9Ci/4HoLTpfwD+qV4NoHVAADs=
    """
    photo = PhotoImage(data=photo)
    

#Note Tk will not keep a reference to the image. , 
#hence would not be displayed if GC removes that 

photo = PhotoImage(...)
label = Label(image=photo)
label.image = photo # keep a reference!
label.pack()

#OR use Pillow 
$ pip install Pillow 

import tkinter as tk
from PIL import ImageTk, Image

#This creates the main window of an application
window = tk.Tk()
window.title("Join")
window.geometry("300x300")
window.configure(background='grey')

path = "my.jpg"

#Creates a tkinter-compatible photo image, which can be used everywhere tkinter expects an image object.
img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()





##tkinter - Capturing events
widget_instance.bind(sequence, func, add=''):
    sequence
        is a string that denotes the target kind of event. 
    func
        fn(event)to be invoked when the event occurs. 
    add
        is optional, either '' or '+'. 
        Passing an empty string denotes that this binding is to replace 
        any other bindings that this event is associated with. 
        Passing a '+' means that this function is to be added 
        to the list of functions bound to this event type.

#Example 
#Keyboard events are sent to the widget that currently owns the keyboard focus. 
#Use the focus_set() method to move focus to a widget
#in this example, click on frame to recieve keyboard events 

from tkinter import *

root = Tk()

def key(event):
    print("pressed", repr(event.char))

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack()
root.mainloop()

##tkinter - list of Events
#Events are given as strings,<modifier-type-detail>

<Button-1>
    A mouse button is pressed over the widget. 
    Button 1 is the leftmost button, 
    button 2 is the middle button (where available), 
    and button 3 the rightmost button.
<B1-Motion>
    The mouse is moved, with mouse button 1 being held down 
    (use B2 for the middle button, B3 for the right button). 
<ButtonRelease-1>
    Button 1 was released. 
    Use 2,3 for middle and right button 
<Double-Button-1>
    Button 1 was double clicked. 
    Use 2,3 for middle and right button 
    You can use Double or Triple as prefixes. 
    Note that if you bind to both a single click (<Button-1>) 
    and a double click, both bindings will be called.
<Enter>
    The mouse pointer entered the widget 
<Leave>
    The mouse pointer left the widget.
<FocusIn>
    Keyboard focus was moved to this widget, or to a child of this widget.
<FocusOut>
    Keyboard focus was moved from this widget to another widget. 
<Return>
    The user pressed the Enter key. 
    the special keys are 
    Cancel , BackSpace, Tab, Return(the Enter key), Shift-L (_* for any Shift + key), 
    Control-L (_* for any Control + key), Alt-L (_* for any Alt + key), 
    Pause, Caps_Lock, Escape, Prior (Page Up), 
    Next (Page Down), End, Home, Left, Up, Right, Down, Print, 
    Insert, Delete, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, 
    Num_Lock, and Scroll_Lock.
<Key>
    The user pressed any key. 
    The key is provided in the char member of the event 
    this is an empty string for special keys
a
    The user typed an 'a'. 
    Most printable characters can be used as is. 
    The exceptions are space (<space>) and less than (<less>). 
    Note that 1 is a keyboard binding, while <1> is a button binding.
<Shift-Up>
<Configure>
    The widget changed size (or location, on some platforms). 
    The new size is provided in the width and height attributes of the event object 

##tkinter - The Event Object attributes 
widget
    The widget which generated this event. 
    This is a valid tkinter widget instance, not a name. 
    This attribute is set for all events.
x, y
    The current mouse position, in pixels.
x_root, y_root
    The current mouse position relative to the upper left corner of the screen, in pixels.
char
    The character code (keyboard events only), as a string.
keysym
    The key symbol (keyboard events only).
keycode
    The key code (keyboard events only).
num
    The button number (mouse button events only).
width, height
    The new size of the widget, in pixels (Configure events only).
type
    The event type.

##tkinter - Instance and Class Bindings

#tkinter chooses the 'closest match' of the available bindings. 
#For example, for both <Key> and <Return> events, 
#only the second binding will be called for Enter key.

#propagation(if present, all four would be called if not using 'break')
1.tkinter first calls the best binding on the instance level, 
2.then the best binding on the toplevel window level, 
3.then the best binding on the class level (which is often a standard binding), 
4.and finally the best available binding on the application level.


##instance binding 
#binding applies to a single widget only; 
#if you create new frames, they will not inherit instance level bindings.
#Level.1: using bind : valid for particular  widget instance, 
self.canv.bind('<Button-2>', self.__drawOrangeBlob)
#Level.2:using bind :valid for  toplevel window (Toplevel or root)
root.bind('<Button-2>', self.__drawOrangeBlob)

#Level.3:valid for the whole widget class(ie for any instances in a Application)  using bind_class 
self.bind_class('Canvas', '<Button-2>', self.__drawOrangeBlob)

#Level.4:the whole application, using bind_all
self.bind_all('<Key-Print>', self.__printScreen)


##To disable the Enter key in a text widget,
#WRONG because class level binding is still called 
text.bind("<Return>", lambda e: None)
#WRONG: this  would change the behavior of all text widgets in the application.
top.bind_class("Text", "<Return>", lambda e: None)
#SOLUTION: Returns 'break' to stop propagation 
text.bind("<Return>", lambda e: "break")



##tkinter - Protocols
#Protocol refers to the interaction between the application and the window manager. 

#Window manager protocols were originally part of the X window system 
#(they are defined in a document titled Inter-Client Communication Conventions Manual, or ICCCM). 
#On that platform, you can install handlers for other protocols as well, 
#like WM_TAKE_FOCUS and WM_SAVE_YOURSELF


#eg  WM_DELETE_WINDOW: when user closes a window using the window manager.
widget.protocol("WM_DELETE_WINDOW", handler)
#Once you have installed  own handler, 
#tkinter will no longer automatically close the window.

#Example 
from tkinter import *
import tkMessageBox
def callback():
    if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
root = Tk()
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()






 

##tkinter - scheduling a call 
after(delay_ms, callback=None, *args)
    Registers an alarm callback that is called after a given time.


#Example 
from tkinter import *
import time
tk=Tk()
def clock():
    t=time.strftime('%I:%M:%S',time.localtime())
    if t!='':
        label1.config(text=t,font='times 25')
    tk.after(100,clock)

label1=Label(tk,justify='center')
label1.pack()
clock()
tk.mainloop()

##tkinter - Setting window width and height 
#setting some size 
root.geometry('400x400')

##min size after geometry manager 
root = Tk()
# set up widgets here, do your grid/pack/place
# root.geometry() will return '1x1+0+0' here(widthxheight+x+y)

#don't call update in event/command handler , use update_idletasks() there 
root.update()
# now root.geometry() returns valid size/placement
#call this before mainloop()
root.minsize(root.winfo_width(), root.winfo_height())


#This creates a fullscreen window. 
#Pressing Escape resizes the window to '200x200+0+0' by default.
#If you move or resize the window, Escape toggles between the current geometry 
#and the previous geometry.

import Tkinter as tk

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

root=tk.Tk()
app=FullScreenApp(root)
root.mainloop()


##tkinter - Basic Widget Methods
#provided by all widgets (including the root window).
#The root window and other Toplevel windows provide additional methods


#Configuration
w.config(option=value)
value = w.cget("option")
k = w.keys()

#Event processing
mainloop()
w.mainloop()
w.quit()
w.wait_variable(var)
w.wait_visibility(window)
w.wait_window(window)
w.update()
w.update_idletasks()

#Event callbacks
w.bind(event, callback)
w.unbind(event)
w.bind_class(event, callback)
w.bindtags()
w.bindtags(tags)

#Alarm handlers and other non-event callbacks
id = w.after(time, callback)
id = w.after_idle(callback)
w.after_cancel(id)

#Window management
w.lift()
w.lower()

#Window-related information
w.winfo_width(), w.winfo_height()
w.winfo_reqwidth(), w.winfo_reqheight()
w.winfo_id()

#The option database
w.option_add(pattern, value)
w.option_get(name, class)

#Reference of Widget methods 
after(delay_ms, callback=None, *args) 
    Registers an alarm callback that is called after a given time. 
    The callback is only called once for each call to this method. 
    To keep calling the callback, you need to reregister the callback inside itself 
    after_cancel to cancel the callback. 
after_cancel(id) 
    Cancels an alarm callback.
    id Alarm identifier.
after_idle(callback, *args) 
    Registers a callback that is called when the system is idle. 
bbox(column=None, row=None, col2=None, row2=None) 
    The bbox method.
bell(displayof=0) 
    Generate a system-dependent sound (typically a short beep).
bind(sequence=None, func=None, add=None) 
bind_all(sequence=None, func=None, add=None) 
bind_class(className, sequence=None, func=None, add=None) 
bindtags(tagList=None) 
    Sets or gets the binding search order for this widget. 
    If called without an argument, returns a tuple containing the binding search order used 
    By default, this tuple contains the widget's name (str(self)), 
    the widget class (e.g. Button), the root window's name, 
    and finally the special name all which refers to the application level. 
cget(key) 
    Returns the current value for an option. 
    Note that option values are always returned as strings 
clipboard_append(string, **options) 
    Adds text to the clipboard.
clipboard_clear(**options) 
    Clears the clipboard.
colormodel(value=None) 
    The colormodel method.
columnconfigure(index, cnf={}, **kw) 
    The columnconfigure method.
config(cnf=None, **kw) 
    Modifies one or more widget options. 
    If called without an argument, this method returns a dictionary containing the current settings for all widget options. 
configure(cnf=None, **kw) 
    Same as config. 
deletecommand(name) 
    The deletecommand method.
destroy() 
    Destroys the widget. 
    The widget is removed from the screen, 
    and all resources associated with the widget are released.
event_add(virtual, *sequences) 
    The event_add method.
event_delete(virtual, *sequences) 
    The event_delete method.
event_generate(sequence, **kw) 
    The event_generate method.
event_info(virtual=None) 
    The event_info method.
focus() 
    The focus method.
focus_displayof() 
    The focus_displayof method.
focus_force() 
    The focus_force method.
focus_get() 
    The focus_get method.
focus_lastfor() 
    The focus_lastfor method.
focus_set() 
    Moves the keyboard focus to this widget. 
    This means that all keyboard events sent to the application will be routed to this widget.
getvar(name='PY_VAR') 
    The getvar method.
grab_current() 
    The grab_current method.
grab_release() 
    Releases the event grab.
grab_set() 
    Routes all events for this application to this widget.
grab_set_global() 
    Routes all events for the entire screen to this widget. 
    This should only be used in very special circumstances, 
    since it blocks all other applications running on the same screen. 
grab_status() 
    The grab_status method.
image_names() 
    The image_names method.
image_types() 
    The image_types method.
keys() 
    Returns a tuple containing the options available for this widget. 
lift(aboveThis=None) 
    Moves the widget to the top of the window stack. 
    If the widget is a child window, it is moved to the top of it's toplevel window.
    If it is a toplevel window (the root or a Toplevel window), it is moved in front of all other windows on the display. If an argument is given, the widget (or window) is moved so it's just above the given widget (window).
lower(belowThis=None) 
    Moves the window to the bottom of the window stack. 
    Same as lift, but moves the widget to the bottom of the stack 
    (or places it just under the belowThis widget). 
mainloop(n=0) 
    Enters tkinter's main event loop. 
    To leave the event loop, use the quit method. 
    Event loops can be nested; it's ok to call mainloop from within an event handler. 
nametowidget(name) 
    Gets the widget object corresponding to a widget name.
option_add(pattern, value, priority=None) 
    The option_add method.
option_clear() 
    The option_clear method.
option_get(name, className) 
    The option_get method.
option_readfile(fileName, priority=None) 
    The option_readfile method.
pack_propagate(flag=['_noarg_']) 
    The pack_propagate method.
pack_slaves() 
    The pack_slaves method.
place_slaves() 
    The place_slaves method.
propagate(flag=['_noarg_']) 
    The propagate method.
quit() 
    The quit method.
register(func, subst=None, needcleanup=1) 
    Registers a Tcl to Python callback. 
    Returns the name of a Tcl wrapper procedure. When that procedure is called from a Tcl program, it will call the corresponding Python function with the arguments given to the Tcl procedure. Values returned from the Python callback are converted to strings, and returned to the Tcl program.
rowconfigure(index, cnf={}, **kw) 
    The rowconfigure method.
selection_clear(**kw) 
    The selection_clear method.
selection_get(**kw) 
    The selection_get method.
selection_handle(command, **kw) 
    The selection_handle method.
selection_own(**kw) 
    The selection_own method.
selection_own_get(**kw) 
    The selection_own_get method.
send(interp, cmd, *args) 
    The send method.
setvar(name='PY_VAR', value='1') 
    The setvar method.
size() 
    The size method.
slaves() 
    The slaves method.
tk_bisque() 
    The tk_bisque method.
tk_focusFollowsMouse() 
    The tk_focusFollowsMouse method.
tk_focusNext() 
    Returns the next widget (following self) that should have focus. 
    This is used by the default bindings for the Tab key. 
tk_focusPrev() 
    Returns the previous widget (preceding self) that should have focus. 
    This is used by the default bindings for the Shift-Tab key. 
tk_menuBar(*args) 
    The tk_menuBar method.
tk_setPalette(*args, **kw) 
    The tk_setPalette method.
tk_strictMotif(boolean=None) 
    he tk_strictMotif method.
tkraise(aboveThis=None) 
    The tkraise method.
unbind(sequence, funcid=None) 
    Removes any bindings for the given event sequence, for this widget.
unbind_all(sequence) 
    The unbind_all method.
unbind_class(className, sequence) 
    The unbind_class method.
update() 
    Processes all pending events, 
    calls event callbacks, completes any pending geometry management, 
    redraws widgets as necessary, and calls all pending idle tasks. 
    This method should be used with care, 
    since it may lead to really nasty race conditions 
    if called from the wrong place (from within an event callback, for example, 
    or from a function that can in any way be called from an event callback, etc.). 
    When in doubt, use update_idletasks instead. 
update_idletasks() 
    Calls all pending idle tasks, without processing any other events. 
    This can be used to carry out geometry management 
    and redraw widgets if necessary, without calling any callbacks.
wait_variable(name) 
    Waits for the given tkinter variable to change. 
    This method enters a local event loop, 
    so other parts of the application will still be responsive. 
    The local event loop is terminated when the variable is updated 
    (setting it to it's current value also counts).
wait_visibility(window=None) 
    Wait for the given widget to become visible. 
    This is typically used to wait until a new toplevel window appears on the screen. 
    Like wait_variable, this method enters a local event loop, 
    so other parts of the application will still work as usual. 
wait_window(window=None) 
    Waits for the given widget to be destroyed. 
    This is typically used to wait until a destroyed window disappears 
    from the screen. Like wait_variable and wait_visibility, 
    this method enters a local event loop, 
    so other parts of the application will still work as usual. 
waitvar(name='PY_VAR') 
    The waitvar method.
winfo_atom(name, displayof=0) 
    Maps the given string to a unique integer. 
    Every time you call this method with the same string, 
    the same integer will be returned.
winfo_atomname(id, displayof=0) 
    Returns the string corresponding to the given integer 
    (obtained by a call to winfo_atom). 
    If the integer isn't in use, tkinter raises a TclError exception. 
    Note that tkinter predefines a bunch of integers (typically 1-80 or so). 
    you can use this method to find out what they are used for. 
winfo_cells() 
    Returns the number of 'cells' in the color map for self. 
    This is typically a value between 2 and 256 (also for true color displays)
winfo_children() 
    Returns a list containing widget instances for all children of this widget. 
    The windows are returned in stacking order from bottom to top. 
    If the order doesn't matter, you can get the same information 
    from the children widget attribute (it's a dictionary mapping Tk widget names 
    to widget instances, so widget.children.values() gives you a list of instances).
winfo_class() 
    Returns the tkinter widget class name for this widget. 
    If the widget is a tkinter base widget, 
    widget.winfo_class() is the same as widget.__class__.__name__.
winfo_colormapfull() 
    Returns true if the color map for this widget is full.
winfo_containing(rootX, rootY, displayof=0) 
    Returns the widget at the given position, or None if there is no such window, 
    or it isn't owned by this application. 
    The coordinates are given relative to the screen's upper left corner.
winfo_depth() 
    Returns the bit depth used to display this widget. 
    This is typically 8 for a 256-color display device, 15 or 16 for a 'hicolor' display, and 24 or 32 for a true color display.
winfo_exists() 
    Returns true if there is Tk window corresponding to this widget. 
winfo_fpixels(distance) 
    Converts the given distance (in any form accepted by tkinter) 
    to the corresponding number of pixels.
winfo_geometry() 
    Returns a string describing the widget's 'geometry'. 
    The string has the following format: 
        "%dx%d%+d%+d" % (width, height, xoffset, yoffset)
winfo_height() 
    Get the height of this widget, in pixels. 
    Note that if the window isn't managed by a geometry manager, this method returns 1. 
    To you get the real value, call update_idletasks first. 
    Use winfo_reqheight to get the widget's requested height 
    (that is, the 'natural' size as defined by the widget itself based on it's contents). 
winfo_id() 
    Get a system-specific window identifier for this widget. 
    For Unix, this is the X window identifier.
    For Windows, this is the HWND cast to a long integer.
winfo_interps(displayof=0) 
    The winfo_interps method.
winfo_ismapped() 
    Check if the window has been created. 
    This method checks if tkinter has created a window corresponding 
    to the widget in the underlying window system (an X window, a Windows HWND, etc).
winfo_manager() 
    Return the name of the geometry manager used to keep manage this widget 
    (typically one of grid, pack, place, canvas, or text).
winfo_name() 
    Get the Tk widget name. 
    This is the same as the last part of the full widget name 
    (which you can get via str(widget)). 
winfo_parent() 
    Get the full widget name of this widget's parent. 
    This method returns an empty string if the widget doesn't have a parent 
    (if it's a root window or a toplevel, that is). 
winfo_pathname(id, displayof=0) 
    Get the full window name for the window having the given identity 
    If the window doesn't exist, or it isn't owned by this application, 
    tkinter raises a TclError exception. 
winfo_pixels(distance) 
    Convert the given distance (in any form accepted by tkinter) 
    to the corresponding number of pixels.
winfo_pointerx() 
    The winfo_pointerx method.
winfo_pointerxy() 
    The winfo_pointerxy method.
winfo_pointery() 
    The winfo_pointery method.
winfo_reqheight() 
    Returns the 'natural' height for this widget. The natural size is the minimal size needed to display the widget's contents, including padding, borders, etc. This size is calculated by the widget itself, based on the given options. The actual widget size is then determined by the widget's geometry manager, based on this value, the size of the widget's master, and the options given to the geometry manager.
winfo_reqwidth() 
    Returns the 'natural' width for this widget. The natural size is the minimal size needed to display the widget's contents, including padding, borders, etc. This size is calculated by the widget itself, based on the given options. The actual widget size is then determined by the widget's geometry manager, based on this value, the size of the widget's master, and the options given to the geometry manager.
winfo_rgb(color) 
    Convert a color string (in any form accepted by tkinter) to an RGB tuple.
    This can be a colour name, a string containing an rgb specifier ('#rrggbb'), 
    or any other syntax supported by tkinter.Returns:A 3-tuple containing the corresponding red, green, and blue components. Note that the tuple contains 16-bit values (0..65535).
winfo_rootx() 
    Get the pixel coordinate for the widget's left edge, 
    relative to the screen's upper left corner.
winfo_rooty() 
    Get the pixel coordinates for the widget's upper edge, 
    relative to the screen's upper left corner.
winfo_screen() 
    Get the X window screen name for the current window. 
    The screen name is a string having the format ':display.screen', 
    where display and screen are decimal numbers. 
winfo_screencells() 
    Get the number of 'color cells' in the default color map for this widget's screen.
winfo_screendepth() 
    Get the default bit depth for this widget's screen.
winfo_screenheight() 
    Get the height of this widget's screen, in pixels.
winfo_screenmmheight() 
    Get the height of this widget's screen, in millimetres. 
    This may not be accurate on all platforms.
winfo_screenmmwidth() 
    Get the width of this widget's screen, in millimetres. 
    This may not be accurate on all platforms.
winfo_screenvisual() 
    Get the 'visual' type used for this widget. 
    This is typically 'pseudocolor' (for 256-color displays) 
    or 'truecolor' (for 16- or 24-bit displays).
winfo_screenwidth() 
    Get the width of this widget's screen, in pixels.
winfo_server() 
    The winfo_server method.
winfo_toplevel() 
    Get the toplevel window (or root) window for this widget, as a widget instance.
winfo_viewable() 
    The winfo_viewable method.
winfo_visual() 
    Same as winfo_screenvisual.
winfo_visualid() 
    The winfo_visualid method.
winfo_visualsavailable(includeids=0) 
    The winfo_visualsavailable method.
winfo_vrootheight() 
    The winfo_vrootheight method.
winfo_vrootwidth() 
    The winfo_vrootwidth method.
winfo_vrootx() 
    The winfo_vrootx method.
winfo_vrooty() 
    The winfo_vrooty method.
winfo_width() 
    Get the width of this widget, in pixels. 
    Note that if the window isn't managed by a geometry manager, this method returns 1. 
    To you get the real value,  call update_idletasks first. 
    You can also use winfo_reqwidth to get the widget's requested width 
    (that is, the 'natural' size as defined by the widget itself based on it's contents). 
winfo_x() 
    Returns the pixel coordinates for the widgets's left corner, relative to its parent's left corner.
winfo_y() 
    Returns the pixel coordinates for the widgets's upper corner, relative to its parent's upper corner.



##tkinter - Toplevel Window Methods
#This group of methods are used to communicate with the window manager. 
#They are available on the root window (Tk), as well as on all Toplevel instances.

aspect(minNumer=None, minDenom=None, maxNumer=None, maxDenom=None) 
    Controls the aspect ratio (the relation between width and height) of this window
    If no arguments are given, this method returns the current constraints as a 4-tuple, if any. 
attributes(*args) 
    Sets or gets(attributeName, value) window attributes.
    For setting, use  root.attributes("-alpha",0.5)
    >>> root.attributes()
    ('-alpha', 1.0, '-transparentcolor', '', '-disabled', 0, '-fullscreen', 0, '-toolwindow', 0, '-topmost', 0)
client(name=None) 
    Sets or gets the WM_CLIENT_MACHINE property. 
    This property is used by window managers under the X window system. 
    It is ignored on other platforms. 
    To remove the property, set it to an empty string. 
colormapwindows(*wlist) 
    Sets or gets the WM_COLORMAP_WINDOWS property.
    This property is used by window managers under the X window system. 
    It is ignored on other platforms. 
command(value=None) 
    Sets or gets the WM_COMMAND property. 
    This property is used by window managers under the X window system. 
    It is ignored on other platforms. 
deiconify() 
    Displays the window. 
    New windows are displayed by default, so you only have to use this method 
    if you have used 'iconify' or 'withdraw' to remove the window from the screen. 
focusmodel(model=None) 
    Sets or gets the focus model. 
frame() 
    Returns a string containing a system-specific window identifier 
    corresponding to the window's outermost parent. 
geometry(geometry=None) 
    Sets or gets the window geometry. 
    If called with an argument, this changes the geometry. 
    The argument should have the following format: 
        "%dx%d%+d%+d" % (width, height, xoffset, yoffset)
    To convert a geometry string to pixel coordinates, you can use something like this: 
    import re
    def parsegeometry(geometry):
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", geometry)
        if not m:
            raise ValueError("failed to parse geometry string")
        return map(int, m.groups())
grid(baseWidth=None, baseHeight=None, widthInc=None, heightInc=None) 
    The grid method. Same as wm_grid. 
group(window=None) 
    Adds window to the window group controlled by the given window. 
    A group member is usually hidden 
    when the group owner is iconified or withdrawn 
    (the exact behavior depends on the window manager in use). 
iconbitmap(bitmap=None) 
    Sets or gets the icon bitmap to use when this window is iconified. 
    This method is ignored by some window managers (including Windows). 
iconify() 
    Turns the window into an icon (without destroying it). 
    To redraw the window, use deiconify. 
    Under Windows, the window will show up in the taskbar. 
    When the window has been iconified, the state method returns 'iconic'. 
iconmask(bitmap=None) 
    Sets or gets the icon bitmap mask to use when this window is iconified. 
    This method is ignored by some window managers (including Windows). 
iconname(newName=None) 
    Sets or gets the icon name to use when this window is iconified. 
    This method is ignored by some window managers (including Windows). 
iconposition(x=None, y=None) 
    Sets or gets the icon position hint to use when this window is iconified. 
    This method is ignored by some window managers (including Windows). 
iconwindow(window=None) 
    Sets or gets the icon window to use as an icon when this window is iconified. 
    This method is ignored by some window managers (including Windows). 
maxsize(width=None, height=None) 
    Sets or gets the maximum size for this window. 
minsize(width=None, height=None) 
    Sets or gets the minimum size for this window. 
overrideredirect(flag=None) 
    Sets or gets the override redirect flag. 
    If non-zero, this prevents the window manager from decorating the window. 
    In other words, the window will not have a title or a border, 
    and it cannot be moved or closed via ordinary means. 
positionfrom(who=None) 
    Sets or gets the position controller 
protocol(name=None, func=None) 
    Registers a callback function for the given protocol. 
    The name argument is typically one of 'WM_DELETE_WINDOW (the window is about to be deleted), 
    'WM_SAVE_YOURSELF' (called by X window managers when the application should save a snapshot of its working set) 
    or 'WM_TAKE_FOCUS' (called by X window managers when the application receives focus). 
resizable(width=None, height=None) 
    Sets or gets the resize flags. 
    The width flag controls whether the window can be resized horizontally by the user. 
    The height flag controls whether the window can be resized vertically. 
sizefrom(who=None) 
    Sets or gets the size controller 
state(newstate=None) 
    Sets or gets the window state. 
    This is one of the values 'normal', 'iconic' (see iconify), 
    'withdrawn' (see withdraw) or 'icon' (see iconwindow). 
title(string=None) 
    Sets or gets the window title. 
transient(master=None) 
    Makes window a transient window for the given master 
    (if omitted, master defaults to self's parent). A
    transient window is always drawn on top of its master, 
    and is automatically hidden when the master is iconified or withdrawn. 
    Under Windows, transient windows don't show show up in the task bar. 
withdraw() 
    Removes the window from the screen (without destroying it). 
    To redraw the window, use deiconify. 
    When the window has been withdrawn, the state method returns 'withdrawn'. 
wm_aspect(minNumer=None, minDenom=None, maxNumer=None, maxDenom=None) 
    Controls the aspect ratio. See aspect for details. 
wm_attributes(*args) 
    Sets or gets window attributes. See attributes for details. 
wm_client(name=None) 
    Sets or gets the WM_CLIENT_MACHINE property. See client for details. 
wm_colormapwindows(*wlist) 
    Sets or gets the WM_COLORMAP_WINDOWS property. See colormapwindows for details. 
wm_command(value=None) 
    Sets or gets the WM_COMMAND property. See command for details. 
wm_deiconify() 
    Displays the window. See deiconify for details. 
wm_focusmodel(model=None) 
    Sets or gets the focus model. See focusmodel for details. 
wm_frame() 
    Returns a window identifier corresponding for the window's outermost parent. See frame for details. 
wm_geometry(newGeometry=None) 
    Sets or gets the window geometry. See geometry for details. 
wm_grid(baseWidth=None, baseHeight=None, widthInc=None, heightInc=None) 
    See grid for details. 
wm_group(pathName=None) 
    Adds the window to a window group. See group for details. 
wm_iconbitmap(bitmap=None) 
    Sets or gets the icon bitmap. See iconbitmap for details. 
wm_iconify() 
    Turns the window into an icon. See iconify for details. 
wm_iconmask(bitmap=None) 
    Sets or gets the icon bitmap mask. See iconmask for details. 
wm_iconname(newName=None) 
    Sets or gets the icon name. See iconname for details. 
wm_iconposition(x=None, y=None) 
    Sets or gets the icon position hint. See iconposition for details. 
wm_iconwindow(pathName=None) 
    Sets or gets the icon window. See iconwindow for details. 
wm_maxsize(width=None, height=None) 
    Sets or gets the maximum size. See maxsize for details. 
wm_minsize(width=None, height=None) 
    Sets or gets the minimum size. See minsize for details. 
wm_overrideredirect(boolean=None) 
    Sets or gets the override redirect flag. See overrideredirect for details. 
wm_positionfrom(who=None) 
    See positionfrom for details. 
wm_protocol(name=None, func=None) 
    Registers a callback function for the given protocol. See protocol for details. 
wm_resizable(width=None, height=None) 
    Sets or gets the resize flags. See resizable for details. 
wm_sizefrom(who=None) 
    See sizefrom for details. 
wm_state(newstate=None) 
    Sets or gets the window state. See state for details. 
wm_title(string=None) 
    Sets or gets the window title. See title for details. 
wm_transient(master=None) 
    Makes window a transient window for a given master. See transient for details. 
wm_withdraw() 
    Removes the window from the screen. See withdraw for details. 




##TkInter - Widgets 
#http://effbot.org/tkinterbook/tkinter-index.htm

##TkInter - Widgets - Label 
#can be with text, a bitmap, or an image):
from tkinter import *
master = Tk()
w = Label(master, text="Hello, world!")
w.pack()
master.mainloop()

#Label's options 
#Note mainloop() destroys root, hence below setting should happen before mainloop()
w.keys()
w.config()

#setting options 
w = Label(master, text="Rouge", fg="red")
w = Label(master, text="Helvetica", font=("Helvetica", 16))
#Multiline text 
w = Label(master, text=longtext, anchor=W, justify=LEFT)
#associating with a variable 
v = StringVar()
Label(master, textvariable=v).pack()
v.set("New Text!")
#With image 
photo = PhotoImage(file="icon.gif")
w = Label(parent, image=photo)
w.photo = photo  #keep a reference
w.pack()


##TkInter - Widgets - Button 
from tkinter import *

master = Tk()

def callback():
    print "click!"

b = Button(master, text="OK", command=callback)
b.pack()
mainloop()

#Options 
#Note mainloop() destroys root, hence below setting should happen before mainloop()
b.keys()
b.config()

#To disable 
b = Button(master, text="Help", state=DISABLED)
#Setting options 
f = Frame(master, height=32, width=32)
f.pack_propagate(0) # don't shrink
f.pack()

b = Button(f, text="Sure!")
b.pack(fill=BOTH, expand=1)

#To display multiple lines of text
b = Button(master, text=longtext, anchor=W, justify=LEFT, padx=2)
#To make an ordinary button look like it's held down,
#change the relief from RAISED to SUNKEN:
b.config(relief=SUNKEN)

#To display text on top of an image, set compound to CENTER:
b = Button(master, text="Click me", image=pattern, compound=CENTER)

#To display an icon along with the text, set the option to one of LEFT, RIGHT, TOP, or BOTTOM:
# put the icon to the left of the text label
b = Button(compound=LEFT, image=icon, text="Action")
# put the icon on top of the text
b = Button(compound=TOP, image=icon, text="Quit")
    
    
    
##TkInter - Widgets - Checkbutton

from tkinter import *

master = Tk()

var = IntVar()  #asspciating a var 
c = Checkbutton(master, text="Expand", variable=var)
c.pack()
mainloop()

#Options
#Note mainloop() destroys root, hence below setting should happen before mainloop()
c.keys()
c.config()

#By default, the variable is set to 1 if the button is selected, and 0 otherwise. 
#OR use  onvalue and offvalue options
var = StringVar()
c = Checkbutton( master, text="Color image", variable=var,
    onvalue="RGB", offvalue="L" )

#to keep track of both the variable and the widget
v = IntVar()
c = Checkbutton(master, text="Don't show this again", variable=v)
c.var = v
#or in class
    def __init__(self, master):
        self.var = IntVar()
        c = Checkbutton(master, text="Enable Tab",
            variable=self.var, command=self.cb)
        c.pack()
    def cb(self, event):
        print("variable is", self.var.get())
 

##TkInter - Widgets - Radiobutton
#To get a proper radio behavior, 
#make sure to have all buttons in a group point to the same variable, 
#and use the value option to specify what value each button represents
 
from tkinter import *

master = Tk()

v = IntVar()
r = Radiobutton(master, text="One", variable=v, value=1).pack(anchor=W)
Radiobutton(master, text="Two", variable=v, value=2).pack(anchor=W)
mainloop()

#Options 
#Note mainloop() destroys root, hence below setting should happen before mainloop()
r.keys()
r.config()

#to get notified when the value changes, 
#attach a command callback to each button.
MODES = [
    ("Monochrome", "1"),
    ("Grayscale", "L"),
    ("True color", "RGB"),
    ("Color separation", "CMYK"),
]

v = StringVar()
v.set("L") # initialize

for text, mode in MODES:
    b = Radiobutton(master, text=text,variable=v, value=mode)
    b.pack(anchor=W)



##TkInter - Widgets - Listbox

#index can be item number (0 for the first item in the list)
#or ACTIVE for  'active' item , END end of the list 

from tkinter import *

master = Tk()
listbox = Listbox(master)  #Empty 
listbox.pack()

listbox.insert(END, "a list entry")  #index.item 

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

mainloop()

#options 
#Note mainloop() destroys root, hence below setting should happen before mainloop()
listbox.keys()
listbox.config()

#To remove items from the list,  use the delete method. 
listbox.delete(0, END)  #all items 
listbox.insert(END, newitem)

#a separate button is used to delete the ACTIVE item from a list.
lb = Listbox(master)
b = Button(master, text="Delete", command=lambda lb=lb: lb.delete(ANCHOR))

#The listbox offers four different selection modes through the selectmode option. 
#These are SINGLE (just a single choice), 
#BROWSE (same, but the selection can be moved using the mouse), 
#MULTIPLE (multiple item can be choosen, by clicking at them one at a time), 
#or EXTENDED (multiple ranges of items can be chosen, using the Shift and Control keyboard modifiers). 
#The default is BROWSE. 
lb = Listbox(selectmode=EXTENDED)

#To query the selection, use curselection method. 
items = map(int, list.curselection()) #return list of indexes 

#Use the get method to get the list item corresponding to a given index.
lb.get(0)  #index 

#Displaying key of a dict 
self.lb.delete(0, END) # clear
for key, value in data:  #[ (k,v), (k,v),... ]
    self.lb.insert(END, key)
self.data = data
#get selected items 
items = self.lb.curselection()
items = [self.data[int(item)] for item in items]

#to track changes to the selection. 
#This solution works best in BROWSE and EXTENDED modes.
lb.bind("<Double-Button-1>", self.ok)

#If you wish to track arbitrary changes to the selection, 
#you can either rebind the whole bunch of selection related events (see the Tk manual pages for a complete list of Listbox event bindings), 
#or, much easier, poll the list using a timer:
class Dialog(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.list = Listbox(self, selectmode=EXTENDED)
        self.list.pack(fill=BOTH, expand=1)
        self.current = None
        self.poll() # start polling the list

    def poll(self):
        now = self.list.curselection()
        if now != self.current:
            self.list_has_changed(now)
            self.current = now
        self.after(250, self.poll)
    def list_has_changed(self, selection):
        print "selection is", selection
        

#By default, the selection is exported via the X selection mechanism (or the clipboard, on Windows).
#For  more than one listbox on the screen, this is bad, hence disable it 
b1 = Listbox(exportselection=0)
for item in families:
    b1.insert(END, item)

b2 = Listbox(exportselection=0)
for item in fonts:
    b2.insert(END, item)

b3 = Listbox(exportselection=0)
for item in styles:
    b3.insert(END, item)

#The listbox itself doesn't include a scrollbar. 
#to attach , use xscrollcommand and yscrollcommand options 
#and the command options of the scrollbars to the corresponding xview and yview methods in the listbox.
frame = Frame(master)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)



##TkInter - Widgets - Entry  for entering text 
#To add entry text to the widget, use the insert method. 
#To replace the current text, you can call delete before you insert the new text.

e = Entry(master)
e.pack()

e.delete(0, END)
e.insert(0, "a default value")

#options 
e.keys()
e.config()

#To fetch the current entry text, use the get method:
s = e.get()

#bind the entry widget to a StringVar instance
v = StringVar()
e = Entry(master, textvariable=v)
e.pack()
v.set("a default value")
s = v.get()

#Example 
def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=LEFT)
    return entry

user = makeentry(parent, "User name:", 10)
password = makeentry(parent, "Password:", 10, show="*")
content = StringVar()
entry = Entry(parent, text=caption, textvariable=content)
text = content.get()
content.set(text)


##TkInter - Widgets - Canvas 
#To draw things in the canvas, use the create methods to add new items.

from tkinter import *

master = Tk()

w = Canvas(master, width=200, height=100)
dir(w)  # check all methods 
w.pack()

w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

w.create_rectangle(50, 25, 150, 75, fill="blue")

mainloop()

#Note that items added to the canvas are kept until you remove them. 
#To change the drawing, 
#you can either use methods like coords, itemconfig, and move to modify the items,
#or use delete to remove them.
i = w.create_line(xy, fill="red")

w.coords(i, new_xy) # change coordinates
w.itemconfig(i, fill="blue") # change color

w.delete(i) # remove
w.delete(ALL) # remove all items


##TkInter - Widgets - Spinbox Widget
#The Spinbox widget is a variant of the standard tkinter Entry widget, 
#which can be used to select from a fixed number of values.
#specify what values to allow, either as a range, or using a tuple.

from tkinter import *

master = Tk()

w = Spinbox(master, from_=0, to=10)
w.pack()

mainloop()

#You can specify a set of values instead of a range: 
w = Spinbox(values=(1, 2, 4, 8))
w.pack()


##TkInter - Widgets - Scale Widget
#to select a numerical value by moving a 'slider' knob along a scale. 
#You can control the minimum and maximum values, as well as the resolution.

from tkinter import *

master = Tk()

w = Scale(master, from_=0, to=100)
w.pack()

w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
w.pack()

mainloop()

#To query the widget, call the get method:
w = Scale(master, from_=0, to=100)
w.pack()

print(w.get())

#The default resolution is 1, 
#use -1 to disable rounding.
w = Scale(from_=0, to=100, resolution=0.1)


##TkInter - Widgets - Toplevel Widget
#The Toplevel widget is used to display extra application windows, 
#dialogs, and other 'pop-up' windows.

top = Toplevel()
top.title("About this application...")

msg = Message(top, text=about_message)
msg.pack()

button = Button(top, text="Dismiss", command=top.destroy)
button.pack()
 
 
##TkInter - Widgets - Scrollbar
#To connect a vertical scrollbar to such a widget
1.Set the widget's yscrollcommand callbacks to the set method of the scrollbar.
2.Set the scrollbar's command to the yview method of the widget.
#can be added to 
•the Listbox widget.
•the Text widget.
•the Canvas widget
•the Entry widget

#Example to Text  - http://effbot.org/zone/tkinter-scrollbar-patterns.htm

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

text = Text(master, wrap=WORD, yscrollcommand=scrollbar.set)
text.pack()

scrollbar.config(command=text.yview)
#The wrap option controls how to handle long lines in the text widget. 
#The default value is CHAR, 
#You can also switch off line wrapping, by setting the wrap option to NONE.
xscrollbar = Scrollbar(master, orient=HORIZONTAL)
xscrollbar.pack(side=BOTTOM, fill=X)

yscrollbar = Scrollbar(master)
yscrollbar.pack(side=RIGHT, fill=Y)

text = Text(master, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)
text.pack()

xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)

#Note that by using pack to display the widgets, 
#you’ll end up with either a horizontal scrollbar that’s wider than the text widget, 
#or a vertical scrollbar that’s taller than the text widget. 
#OR use the grid manager to display the widgets:
frame = Frame(master, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

text = Text(frame, wrap=NONE, bd=0,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)

text.grid(row=0, column=0, sticky=N+S+E+W)

xscrollbar.config(command=text.xview)
yscrollbar.config(command=text.yview)

frame.pack()

 
 
 
##TkInter - Widgets - Menus        
#Toplevel menus are displayed just under the title bar of the root 
#or any other toplevel windows 

#To create a toplevel menu, create a new Menu instance, 
#and use add methods to add commands and other menu entries to it.
from tkinter import *
root = Tk()

def hello():
    print "hello!"

# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=root.quit)

# display the menu
root.config(menu=menubar)


#Pulldown menus are attached to a parent menu (using add_cascade), 
root = Tk()

def hello():
    print "hello!"

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

#a popup menu is created in the same way, 
#but is explicitly displayed, using the post method:
root = Tk()

def hello():
    print "hello!"

# create a popup menu
menu = Menu(root, tearoff=0)
menu.add_command(label="Undo", command=hello)
menu.add_command(label="Redo", command=hello)

# create a canvas
frame = Frame(root, width=512, height=512)
frame.pack()

def popup(event):
    menu.post(event.x_root, event.y_root)

# attach popup to canvas
frame.bind("<Button-3>", popup)

#You can use the postcommand callback to update 
#(or even create) the menu every time it is displayed.
counter = 0

def update():
    global counter
    counter = counter + 1
    menu.entryconfig(0, label=str(counter))

root = Tk()

menubar = Menu(root)

menu = Menu(menubar, tearoff=0, postcommand=update)
menu.add_command(label=str(counter))
menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="Test", menu=menu)

root.config(menu=menubar)
     

     
##TkInter - Widgets - OptionMenu Widget
#a helper class that creates a popup menu, and a button to display it. 
#The option menu is similar to the combobox widgets commonly used on Windows.

from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one") # default value

w = OptionMenu(master, variable, "one", "two", "three")
w.pack()

mainloop()

#To get the selected option, use get on the variable:
from tkinter import *

master = Tk()

var = StringVar(master)
var.set("one") # initial value

option = OptionMenu(master, var, "one", "two", "three", "four")
option.pack()

#
# test stuff

def ok():
    print("value is", var.get())
    master.quit()

button = Button(master, text="OK", command=ok)
button.pack()

mainloop()
.

#The following example shows how to create an option menu from a list of options:
from tkinter import *

# the constructor syntax is:
# OptionMenu(master, variable, *values)

OPTIONS = [
    "egg",
    "bunny",
    "chicken"
]

master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = apply(OptionMenu, (master, variable) + tuple(OPTIONS))
w.pack()

mainloop()
       
        
##tkinter - Virtual events
#create your own new kinds of events called virtual events. 
#name synatx '<<any_name>>'

#Use widget_instance.event_add(), .event_delete(), and .event_info()

#For example - to create a new event called <<panic>>, 
#that is triggered either by mouse button 3 or by the pause key. 
w.event_add('<<panic>>', '<Button-3>', '<KeyPress-Pause>')

#use '<<panic>>' in any event sequence
#any mouse button 3 or pause keypress in widget w will trigger the handler h.
w.bind('<<panic>>', h)


        
##tkinter - Dialog box - Messages
#A messagebox can display information to a user. 
#There are three variations on these dialog boxes based on the type of message 

from tkinter import messagebox

messagebox.showinfo("Information","Informative message")
messagebox.showerror("Error", "Error message")
messagebox.showwarning("Warning","Warning message")


##tkinter - Dialog box - Yes/No Questions

from tkinter import messagebox

#The return value is a Boolean, True or False, answer to the question. 
#If 'cancel' is an option and the user selects the 'cancel' button, None is returned.

answer = messagebox.askokcancel("Question","Do you want to open this file?")
answer = messagebox.askretrycancel("Question", "Do you want to try that again?")
answer = messagebox.askyesno("Question","Do you like Python?")
answer = messagebox.askyesnocancel("Question", "Continue playing?")




##tkinter - Dialog box - Single Value Data Entry
#to ask the user for a single data value, either a string, integer, 
#or floating point value


import tkinter as tk
from tkinter import simpledialog

application_window = tk.Tk()

answer = simpledialog.askstring("Input", "What is your first name?",
                                parent=application_window)
if answer is not None:  #'cancel' returns None ,  else returns a value 
    print("Your first name is ", answer)
else:
    print("You don't have a first name?")

answer = simpledialog.askinteger("Input", "What is your age?",
                                 parent=application_window,
                                 minvalue=0, maxvalue=100)
if answer is not None:
    print("Your age is ", answer)
else:
    print("You don't have an age?")

answer = simpledialog.askfloat("Input", "What is your salary?",
                               parent=application_window,
                               minvalue=0.0, maxvalue=100000.0)
if answer is not None:
    print("Your salary is ", answer)
else:
    print("You don't have a salary?")



##tkinter - Dialog box - File Chooser

#Note that these commands do not save or load a file, but only gets a file name 


import tkinter as tk
from tkinter import filedialog
import os

application_window = tk.Tk()

# Build a list of tuples for each file type the file dialog should display
my_filetypes = [('all files', '.*'), ('text files', '.txt')]

# Ask the user to select a folder.
answer = filedialog.askdirectory(parent=application_window,
                                 initialdir=os.getcwd(),
                                 title="Please select a folder:")

# Ask the user to select a single file name.
answer = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)

# Ask the user to select a one or more file names.
answer = filedialog.askopenfilenames(parent=application_window,
                                     initialdir=os.getcwd(),
                                     title="Please select one or more files:",
                                     filetypes=my_filetypes)

# Ask the user to select a single file name for saving.
answer = filedialog.asksaveasfilename(parent=application_window,
                                      initialdir=os.getcwd(),
                                      title="Please select a file name for saving:",
                                      filetypes=my_filetypes)



##tkinter - Dialog box - Color Chooser

from tkinter import colorchooser

rgb_color, web_color = colorchooser.askcolor(parent=application_window,
                                             initialcolor=(255, 0, 0))

                                             
##tkinter - Dialog box - Creating Manual dialog 
#http://effbot.org/tkinterbook/tkinter-dialog-windows.htm

#Simple dialog 
from tkinter import *
class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Value").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
    def ok(self):
        print "value is", self.e.get()
        self.top.destroy()
root = Tk()
Button(root, text="Hello!").pack()
root.update()
d = MyDialog(root)
root.wait_window(d.top) #the local event loop handled by wait_window was sufficient). 

       
#professional dialog class 
from tkinter import *
import os
class Dialog(Toplevel):
    def __init__(self, parent, title = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)
    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()
    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks
    def validate(self):
        return 1 # override
    def apply(self):
        pass # override
        
#create the necessary widgets in the body method, and extract the result 
#and carry out business logic  in the apply method.
class MyDialog(Dialog):
    def body(self, master):
        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus
    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print(first, second) # or something 

d = MyDialog(root)
print d.result

#Using the grid geometry maanager 
def body(self, master):
    Label(master, text="First:").grid(row=0, sticky=W)
    Label(master, text="Second:").grid(row=1, sticky=W)
    self.e1 = Entry(master)
    self.e2 = Entry(master)
    self.e1.grid(row=0, column=1)
    self.e2.grid(row=1, column=1)
    self.cb = Checkbutton(master, text="Hardcopy")
    self.cb.grid(row=2, columnspan=2, sticky=W)
        
#validaing 
    def validate(self):
        try:
            first= int(self.e1.get())
            second = int(self.e2.get())
            self.result = first, second
            return 1
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )
            return 0

    def apply(self):
        dosomething(self.result)
       
##tkinter -PanedWindow Widget
#The child widgets can be resized by the user#

a 2-pane widget:
from tkinter import *

m = PanedWindow(orient=VERTICAL)
m.pack(fill=BOTH, expand=1)

top = Label(m, text="top pane")
m.add(top)

bottom = Label(m, text="bottom pane")
m.add(bottom)

mainloop()

#a 3-pane widget:
from tkinter import *

m1 = PanedWindow()
m1.pack(fill=BOTH, expand=1)

left = Label(m1, text="left pane")
m1.add(left)

m2 = PanedWindow(m1, orient=VERTICAL)
m1.add(m2)

top = Label(m2, text="top pane")
m2.add(top)

bottom = Label(m2, text="bottom pane")
m2.add(bottom)

mainloop()

#Reference

PanedWindow(master=None, **options) (class) 
    add(child, **options) 
        Adds a child window to the paned window.
    config(**options) 
        Modifies one or more widget optionsforget(child) 
    forget(child)
        Removes a child window.
    identify(x, y) 
        Identifies the widget element at the given position.
    panecget(child, option) 
        Gets a child window option.
    paneconfig(child, **options) 
        Same as paneconfigure. 
    paneconfigure(child, **options) 
        Set child window configuration options.
            after=Insert after this widget.
            before=Insert before this widget.
            height=Widget height.
            minsize=Minimal size (width for horizontal panes, height for vertical panes).
            padx=Horizontal padding.
            pady=Vertical padding.
            sticky=Defines how to expand a child widget if the resulting pane is larger than the widget itself. This can be any combination of the constants S, N, E, and W, or NW, NE, SW, and SE. 
            width=Widget width.
    panes() 
        Returns a list of child widgets.
        Returns:A list of widgets.
    proxy_coord() 
        Gets the most recent proxy position.
    proxy_forget() 
        Removes the proxy.
    proxy_place(x, y) 
        Places the proxy at the given position.
    remove(child) 
        Same as forget. 
    sash_coord(index) 
        Gets the current position for a sash (separator).
    index   Sash index (0..n).
        Returns:The upper left corner of the sash, given as a 2-tuple (x, y).
    sash_dragto(index, x, y) 
        Drag the sash (separator) to a new position, relative to the mark. 
    sash_mark(index, x, y) 
        Registers the current mouse position. 
    sash_place(index, x, y) 
        Moves the sash (separator) to a given position.
        indexSash index (0..n).
        x   Sash position.
        y   Sash position.       
       
       

##tkinter - ttk 
#https://docs.python.org/3/library/tkinter.ttk.html
#Tk themed widget set
#Using the Ttk widgets gives the application an improved look and feel.     

from tkinter import ttk

#To override the basic Tk widgets, 
#the import should follow the Tk import:

from tkinter import *
from tkinter.ttk import *
#tkinter.ttk widgets (Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale and Scrollbar) 
#automatically replacese the Tk widgets as tk import happened earlier 

##tkinter - ttk - Ttk Widgets(subclasses of Widget)
#Ttk comes with 17 widgets, eleven of which already existed in tkinter: 
#Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale and Scrollbar. 
#The other six are new: Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview. And all them are .


#Tk code:
l1 = tkinter.Label(text="Test", fg="black", bg="white")
l2 = tkinter.Label(text="Test", fg="black", bg="white")

#Ttk code: Style is the main component in ttk code 
#https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling
style = ttk.Style()

#'BW.TLabel' is newStyle.oldStyle form (ie inherit all styles of OldStyle but set few )
style.configure("BW.TLabel", foreground="black", background="white") #name, *styles
l1 = ttk.Label(text="Test", style="BW.TLabel")
l2 = ttk.Label(text="Test", style="BW.TLabel")

#Example - to change every default button to be a flat button 
#with some padding and a different background color:

from tkinter import ttk
import tkinter

root = tkinter.Tk()

#Change Buttons style 
ttk.Style().configure("TButton", padding=6, relief="flat",   background="#ccc")

btn = ttk.Button(text="Sample")
btn.pack()

root.mainloop()

##tkinter - ttk - To use predefined themes 
from tkinter import ttk
style = ttk.Style()
>>> dir(style)
[ 'configure', 'element_create', 'element_names', 'element_options','layout', 
'lookup', 'map', 'master', 'theme_create', 'theme_names', 'theme_settings', 
'theme_use', 'tk']
>>> style.theme_names()
('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
>>> style.element_names()
('Horizontal.Scrollbar.leftarrow', 'Vertical.Scale.slider', 'Spinbox.uparrow', 'Horizontal.Scrollbar.thumb', 'Horizontal.Scrollbar.trough', 'Horizontal.Scrollbar.rightarrow', 'Combobox.field', 'Vertical.Scrollbar.grip', 'Menubutton.dropdown', 'Horizontal.Progressbar.pbar', 'Vertical.Scrollbar.downarrow', 'Combobox.border', 'Spinbox.field', 'Spinbox.innerbg', 'Combobox.rightdownarrow', 'Entry.background', 'Horizontal.Scale.slider', 'ComboboxPopdownFrame.background', 'Spinbox.background', 'Vertical.Scrollbar.thumb', 'Vertical.Scrollbar.uparrow', 'Vertical.Scrollbar.trough', 'Horizontal.Scrollbar.grip', 'Entry.field', 'Spinbox.downarrow', 'Vertical.Progressbar.pbar')
#Get current theme and change 
>>> s.theme_use()
'default'
>>> s.theme_use('alt')
>>> s.theme_use()
'alt'

##tkinter - ttk - Using and customizing ttk styles
#Within a given theme, every widget has a default widget class; 
#Each widget also has a style. 
#In ttk, widget classes and styles are specified as strings. 
#In general the default style name of a widget is 'T' prefixed to the widget name

#Widget class	Style name
Button 	        TButton
Checkbutton 	TCheckbutton
Combobox 	    TCombobox
Entry 	        TEntry
Frame 	        TFrame
Label 	        TLabel
LabelFrame 	    TLabelFrame
Menubutton 	    TMenubutton
Notebook 	    TNotebook
PanedWindow 	TPanedwindow 
Progressbar 	Horizontal.TProgressbar or Vertical.TProgressbar, depending on the orient option.
Radiobutton 	TRadiobutton
Scale 	        Horizontal.TScale or Vertical.TScale, depending on the orient option.
Scrollbar 	    Horizontal.TScrollbar or Vertical.TScrollbar, depending on the orient option.
Separator 	    TSeparator
Sizegrip 	    TSizegrip
Treeview 	    Treeview (not TTreview!)

#To retrieve a widget's Widget(style) class by calling its .winfo_class() method.

>>> b=ttk.Button(None)
>>> b.winfo_class()
'TButton'
>>> t=ttk.Treeview(None)
>>> t.winfo_class()
'Treeview'
>>> b.__class__    # Here, we are asking for the Python class
<class ttk.Button at 0x21c76d0>

#The name of a style may have one of two forms.
1.The built-in styles are all a single word: 'TFrame' or 'TRadiobutton',
2.To create a new style derived from one of the built-in styles, 
  use a style name of the form 'newName.oldName'. 
  For example, to create a new style of Entry widget to hold a date, 
  you might call it 'Date.TEntry'. 

#Every style has a corresponding set of options that define its appearance. 
#For example, buttons have a foreground option that changes the color of the button's text.

#Getting or setting Style options 

#Current values 
>>> Style().configure('TButton')
{'padding': '1 1', 'anchor': 'center', 'width': '-11'}
#set a new values 
s.configure('TButton', foreground='green')

#To create a new style based on some style oldName, 
#Use  .configure() method using a name of the form 'newName.oldName'
#Would inherit all styles from 'oldName'
#Note hierarchies of styles can be created  
#For example, 'Panic.Kim.TButton',  style will inherit all the options from the 'Kim.TButton' style, 
s = ttk.Style()
s.configure('Kim.TButton', foreground='maroon')
#then use 
self.b = ttk.Button(self, text='Friday', style='Kim.TButton', command=self._fridayHandler)

#There is a root style whose name is '.'. 
#To change some feature's default appearance for every widget
s = ttk.Style()
s.configure('.', font=('Helvetica', 12))



##tkinter - ttk - Structuring a style

#the pieces of a widget are assembled using the idea of a cavity, 
#an empty space that is to be filled with elements.

#For example, in the classic theme, a button has four concentric elements(called layers). 
#From the outside in, they are focus highlight, border, padding,label elements.

#Each of these elements has a 'sticky' attribute that specifies 
#how many of the four sides of the cavity it 'sticks' to. 
#For example, if an element has a sticky='ew' attribute, 
#that means it must stretch in order to stick to the left (west) and right (east) sides of its cavity,
#but it does not have to stretch vertically.

#layout :to organize the different layers(concentric elements) that make up a widget. 

s = ttk.Style()
s.layout(widgetClass) #widgetClass is the name of the widget(Style) class

#A layout can be just None, if it takes no options, 
#or a dict of options specifying how to arrange the element. 
side: whichside
    Specifies which side of the cavity to place the element;
    one of top, right, bottom or left. 
    If omitted, the element occupies the entire cavity.
sticky: nswe
    Specifies where the element is placed inside its allocated parcel.
unit: 0 or 1
    If set to 1, causes the element and all of its descendants to be treated as a single element 
    for the purposes of Widget.identify() et al. 
    It's used for things like scrollbar thumbs with grips.
children: [sublayout… ]
    Specifies a list of elements to place inside the element. 
    Each element is a tuple (or other sequence type) 
    where the first item is the layout name, and the other is a Layout.

#Example 
import ttk
s = ttk.Style()
s.theme_use('classic')
b = ttk.Button(None, text='Yo')
bClass = b.winfo_class()
>>> bClass
'TButton'
layout = s.layout('TButton')
>>> layout
[('Button.highlight', {'children': [('Button.border', {'border':
'1', 'children': [('Button.padding', {'children': [('Button.label',
{'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})],
'sticky': 'nswe'})]
>>> import pprint
#From the outside in, layers are focus highlight, border, padding,label elements.
#layout = [ (styleName, Layout),...]
>>> pprint.pprint(layout)
[('Button.highlight',
  {'children': [('Button.border',
                 {'border': '1',
                  'children': [('Button.padding',
                                {'children': [('Button.label',
                                               {'sticky': 'nswe'})],
                                 'sticky': 'nswe'})],
                  'sticky': 'nswe'})],
   'sticky': 'nswe'}
)]

#To obtain the list of option names
s = ttk.Style()
s.element_options(styleName)
#Example 
>>> s.element_options('Button.padding')
('-padding', '-relief', '-shiftrelief')

>>> d = s.element_options('Button.highlight')
>>> d
('-highlightcolor', '-highlightthickness')

#To find out values of options 
s.lookup(layoutName, optName)

#Example 
>>> s.lookup('Button.highlight', 'highlightthickness')
1
>>> s.lookup('Button.highlight', 'highlightcolor')
'#d9d9d9'
>>> print(s.element_options('Button.label'))
('-compound', '-space', '-text', '-font', '-foreground', '-underline',
'-width', '-anchor', '-justify', '-wraplength', '-embossed', '-image',
'-stipple', '-background')
>>> s.lookup('Button.label', 'foreground')
'SystemWindowText'

##tkinter - ttk - Methods common to all ttk widgets

.cget(option)
    This method returns the value for the specified option. 
.configure(option=value, ...)
    To set one or more widget options, 
    use keyword arguments of the form option=value. 
    For example, to set a widget's font, use 'font=('serif', 12)'.
    If you provide no arguments, 
    the method will return a dictionary of all the widget's current option values.
    In this dictionary, the keys will be the option names, 
    and each related value will be a tuple (name, dbName, dbClass, default, current):
        name 	    The option name.
        dbName 	    The database name of the option.
        dbClass 	The database class of the option.
        default 	The default value of the option.
        current 	The current value of the option. 
.identify(x, y)
    Use this to determine what element is at a given location within the widget. 
    If the point (x, y) relative to the widget is somewhere within the widget, 
    this method returns the name of the element at that position; 
    otherwise it returns an empty string. 
.instate(stateSpec, callback=None, *args, **kw)
    The purpose of this to determine whether the widget is in a specified state or combination of states.
    If you provide a callable value as the callback argument, 
    and the widget matches the state or combination of states specified 
    by the stateSpec argument, that callable will be called 
    with positional arguments *args and keyword arguments **kw. 
    If the widget's state does not match stateSpec, 
    the callback will not be called.
    If you donot provide a callback argument, 
    the method will return True if the widget's state matches stateSpec, False otherwise.
.state(stateSpec=None)
    Use this item either to query a widget to determine its current states, 
    or to set or clear one state.
    If you provide a stateSpec argument 
    the method will set or clear states in the widget according to that argument.
    For example, for a widget w, the method 
    w.state(['!disabled', 'selected']) 
    would clear the widget's 'disabled' set and set its 'selected' state. 
    
##tkinter - ttk - Specifying widget states in ttk - stateSpec argument
1.A single state name such as 'pressed'. 
  A ttk.Button widget is in this state, 
  for example, when the mouse cursor is over the button 
  and mouse button 1 is down.
2.A single state name preceded with an exclamation point (!); 
  this matches the widget state only when that state is off.
  For example, a stateSpec argument '!pressed' specifies a widget 
  that is not currently being pressed.
3.A sequence of state names, or state names preceded by an '!'. 
 Such a stateSpec matches only when all of its components match. 
 For example, a stateSpec value of ('!disabled', 'focus') matches a widget 
 only when that widget is not disabled and it has focus. 

    

##tkinter - ttk - dynamic appearance changes

#The ttk widgets can change their appearance during the execution of the program.
#For example, when a widget is disabled, it will not respond to mouse or keyboard actions. 
#Typically a disabled widget presents a different appearance 

#In general, every ttk widget has a set of state flags 
#that you can use to make the appearance of a widget change during execution. 
#Some states will change in response to user actions,for example, the pressed state of a Button. 
#Your program can interrogate, clear, or set any state 
#Each state may be set (turned on) or reset (turned off) independently of the other states. 

#states     meanings
active 	    The mouse is currently within the widget.
alternate 	This state is reserved for application use.
background 	Under Windows or MacOS, the widget is located in a window that is not the foreground window.
disabled 	The widget will not respond to user actions.
focus 	    The widget currently has focus.
invalid 	The contents of the widget are not currently valid.
pressed 	The widget is currently being pressed (e.g., a button that is being clicked).
readonly 	The widget will not allow any user actions to change its current value. For example, a read-only Entry widget will not allow editing of its content.
selected 	The widget is selected. Examples are checkbuttons and radiobuttons that are in the 'on' state.

#To interrogate or set up dynamic behavior for a specific style, 
#styleName is the element's name, e.g., 'Button.label' or 'border'.
s = ttk.Style()
s.map(styleName, query_opt=None, **kw)

#To determine the dynamic behavior of one option of a given style element, 
#pass the option name as the second positional argument,
#Each state change specification is a sequence (s0, s1, n), 
#n is value when state matches all of s0,s1,... (AND)
#Each item si is either a state name, or a state name preceded by a '!'. 
#To match, the widget must be in all the states described by items that don't start with '!', 
#and it must not be in any of the states that start with '!'.

>>> s.theme_use('alt')
>>> s.map('TButton')
{'highlightcolor': [('alternate', 'black')], 
'relief': [('pressed', '!disabled', 'sunken'), ('active', '!disabled', 'raised')]}
>>> s.map('TButton', 'relief')
[('pressed', '!disabled', 'sunken'), ('active', '!disabled', 'raised')]

#To change the dynamic behavior of an element 
s.map('TCheckbutton',
        indicatoron=[('pressed', '#ececec'), ('selected', '#4a6984')])

#Example - To create custom button style based on the standard TButton class. 
#name: 'Wild.TButton'; 
#because our name ends with '.TButton', it automatically inherits the standard style features. 
s = ttk.Style()
s.configure('Wild.TButton',
    background='black',
    foreground='white',
    highlightthickness='20',
    font=('Helvetica', 18, 'bold'))
s.map('Wild.TButton',
    foreground=[('disabled', 'yellow'),
                ('pressed', 'red'),
                ('active', 'blue')],
    background=[('disabled', 'magenta'),
                ('pressed', '!focus', 'cyan'),
                ('active', 'green')],
    highlightcolor=[('focus', 'green'),
                    ('!focus', 'red')],
    relief=[('pressed', 'groove'),
            ('!pressed', 'ridge')])


##tkinter -ttk - other methods from  tkinter.ttk.Style
element_create(elementname, etype, *args, **kw)
    Create a new element in the current theme, 
    of the given etype which is expected to be either 'image', 'from' or 'vsapi'. 
    If 'image' is used, args should contain the default image name followed 
    by statespec/value pairs (this is the imagespec), 
    and kw may have the following options:
            border=padding
                padding is a list of up to four integers, 
                specifying the left, top, right, and bottom borders, respectively.
            height=height
                Specifies a minimum height for the element. 
                If less than zero, the base image's height is used as a default.
            padding=padding
                Specifies the element's interior padding. 
                Defaults to border's value if not specified.
            sticky=spec
                Specifies how the image is placed within the final parcel. 
                spec contains zero or more characters 'n', 's', 'w', or 'e'.
            width=width
                Specifies a minimum width for the element. 
                If less than zero, the base image's width is used as a default.
    If 'from' is used as the value of etype, 
    element_create() will clone an existing element. 
    args is expected to contain a themename, 
    from which the element will be cloned, and optionally an element to clone from. 
    If this element to clone from is not specified, an empty element will be used. 
    kw is discarded.
element_names()
    Returns the list of elements defined in the current theme.
element_options(elementname)
    Returns the list of elementname's options.
theme_create(themename, parent=None, settings=None)
    Create a new theme.
    It is an error if themename already exists. 
    If parent is specified, the new theme will inherit styles, elements and layouts from the parent theme. 
    If settings are present they are expected to have the same syntax used for theme_settings().
theme_settings(themename, settings)
    Temporarily sets the current theme to themename, 
    apply specified settings and then restore the previous theme.
    Each key in settings is a style 
    and each value may contain the keys 'configure', 'map', 'layout' and 'element create' and they are expected to have the same format as specified by the methods Style.configure(), Style.map(), Style.layout() and Style.element_create() respectively.
    #As an example, let's change the Combobox for the default theme a bit:
    from tkinter import ttk
    import tkinter
    root = tkinter.Tk()
    style = ttk.Style()
    style.theme_settings("default", {
       "TCombobox": {
           "configure": {"padding": 5},
           "map": {
               "background": [("active", "green2"),
                              ("!disabled", "green4")],
               "fieldbackground": [("!disabled", "green3")],
               "foreground": [("focus", "OliveDrab1"),
                              ("!disabled", "OliveDrab2")]
           }
       }
    })
    combo = ttk.Combobox().pack()
    root.mainloop()
theme_names()
    Returns a list of all known themes.
theme_use(themename=None)
    If themename is not given, returns the theme in use. Otherwise, sets the current theme to themename, refreshes all widgets and emits a <<ThemeChanged>> event.
    
    
    

    
##tkinter - scrolled text using tkinter.scrolledtext

import tkinter as tk

win = tk.Tk()

win.configure(background="#808000")

frame1 = tk.Frame(win,width=80, height=80,bg = '#ffffff',borderwidth=1, relief="sunken")
scrollbar = tk.Scrollbar(frame1) 
editArea = tk.Text(frame1, width=10, height=10, wrap="word",
                   yscrollcommand=scrollbar.set,
                   borderwidth=0, highlightthickness=0)
scrollbar.config(command=editArea.yview)
scrollbar.pack(side="right", fill="y")
editArea.pack(side="left", fill="both", expand=True)
frame1.place(x=10,y=30)

win.mainloop()

#or usin tkinter.scrolledtext
import tkinter as tk
import tkinter.scrolledtext as tkst

win = tk.Tk()
frame1 = tk.Frame(
    master = win,
    bg = '#808000'
)
frame1.pack(fill='both', expand='yes')
editArea = tkst.ScrolledText(
    master = frame1,
    wrap   = tk.WORD,
    width  = 20,
    height = 10
)
# Don't use widget.place(), use pack or grid instead, since
# They behave better on scaling the window -- and you don't
# have to calculate it manually!
editArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# Adding some text, to see if scroll is working as we expect it
editArea.insert(tk.INSERT, ("Hello "*20+"\n")*80)
win.mainloop()
 
 
###Python GUI - RAD tools 
#https://wiki.python.org/moin/GuiProgramming

##Page for tkinter 
#Install Tcl/Tk 8.6.4 from ActiveTcl;https://www.activestate.com/activetcl
#Install Page http://sourceforge.net/projects/page(install to C:\page)
#starts c:\page\winpage.bat
 
 

###wxpython 

#install 
$ pip install wxpython 

#Steps :
1. Create wx.App() instance 
2. Create a class derived from wx.Frame, 
3. Create a wx.Panel instance to contain all controls (ie parent=instance)
   Note  constructor of controls,panel, frame is of type 
   (parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=0, name=PanelNameStr)
   To bind any event to control, frame, panel , use 
   any_instance.Bind(wx.EVT_eventType, handler=fn_taking_event_arg, source=source_cntrl_if_different_than_self),
   Note handler, takes wx.Event(and it's subclass eg wx.CommandEvent)
   for wx.CommandEvent: to get data, use event.GetInt(), .GetSelection(), .GetString()   
4. To create menuitems, use wx.Menu(), then .Append(id, item='', helpString='')
   to append sub menues. Note wx has many welldefined ID (check that) else pass ID_ANY to create new ID 
   Create wx.MenuBar() and use.Append(menuitem, title) to append above menuitem to Bar 
   Note title may contain & to create Hotkey    
5. wx.BoxSizer can contain Many controls to be arranged in grids (rows, columns )
   Use .Add(control_or_another_sizer, proportion=0, flag=0, border=0, userData=None) to add controls or another wx.Sizer 
   use frm.SetSizer(instance) to set it 
   Use frm.SetAutoLayout(True)
6. Can create statusbar by frm.CreateStatusBar() , toolbar by  frm.CreateToolBar()
   Update status by frm.SetStatusText(string), 
   add tool as .AddTool(toolId, label, bitmap, shortHelp='', kind=ITEM_NORMAL), bind to EVT_TOOL event
7. Use frm.Show() to display it 
8. start event llop by app.MainLoop()
9. To draw lines etc, Use wx.PaintDC, wx.ClientDC, wx.WindowDC, wx.ScreenDC, wx.MemoryDC or wx.PrinterD


#Quick example 

import wx
app = wx.App(False)     # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)        # Show the frame.
app.MainLoop()

#Quick Example - 2
import wx

class HelloFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()
    
##Quick Example-3 
import wx
import os

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''

        # A "-1" in the size parameter instructs wx.Widgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)     #  Text Edit control
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)   # handling event
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)          #Boxing Widgets
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A sample editor \n in wx.Python", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()





##wxpython - Overview 
#https://docs.wxpython.org/wx.1moduleindex.html

wx
    The classes which appear in the main wx namespace
wx.adv
    Less commonly used or more advanced classes
wx.grid
    Widget and supporting classes for displaying and editing tabular data
wx.dataview
    Classes for viewing tabular or hierarchical data
wx.richtext
    A generic, ground-up implementation of a text control capable of showing multiple text styles and images.
wx.ribbon
    A set of classes for writing a ribbon-based UI, typically a combonation of tabs and toolbar, similar to the UI in MS Office and Windows 10.
wx.html
    Widget and supporting classes for a generic html renderer
wx.html2
    Widget and supporting classes for a native html renderer, with CSS and javascript support
wx.aui
    Docking/floating window panes, draggable notebook tabs, etc.
wx.lib
    Our pure-Python library of widgets
wx.glcanvas
    Classes for embedding OpenGL views in a window
wx.stc
    Classes for Styled Text Control, a.k.a Scintilla
wx.msw
    A few classes available only on Windows
wx.media
    MediaCtrl and related classes
wx.propgrid
    PropertyGrid and related classes for editing a grid of name/value pairs.
wx.xrc
    Classes for loading widgets and layout from XML
wx.xml
    Some simple XML classes for use with XRC
wx.py
    The py package, containing PyCrust and related modules
wx.tools
    Some useful tools and utilities for wxPython.




##wxpython - Style 
#Most of the constructors takes a style parameter of datat type long 

#Used for specifying alternative behaviour and appearances for windows
#it is a long type created via bitwise operation 
style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER

#wx.Window styles are 
wx.BORDER_DEFAULT
	 The window class will decide the kind of border to show, if any.
wx.BORDER_SIMPLE
	 Displays a thin border around the window. wx.SIMPLE_BORDER is the old name for this style.
wx.BORDER_SUNKEN
	 Displays a sunken border. wx.SUNKEN_BORDER is the old name for this style.
wx.BORDER_RAISED
	 Displays a raised border. wx.RAISED_BORDER is the old name for this style.
wx.BORDER_STATIC
	 Displays a border suitable for a static control. wx.STATIC_BORDER is the old name for this style. Windows only.
wx.BORDER_THEME
	 Displays a native border suitable for a control, on the current platform. On Windows XP or Vista, this will be a themed border; on most other platforms a sunken border will be used. For more information for themed borders on Windows, please see Themed borders on Windows.
wx.BORDER_NONE
	 Displays no border, overriding the default border style for the window. wx.NO_BORDER is the old name for this style.
wx.BORDER_DOUBLE
	 This style is obsolete and should not be used.
wx.TRANSPARENT_WINDOW
	 The window is transparent, that is, it will not receive paint events. Windows only.
wx.TAB_TRAVERSAL
	 Use this to enable tab traversal for non-dialog windows.
wx.WANTS_CHARS
	 Use this to indicate that the window wants to get all char/key events for all keys - even for keys like TAB or ENTER which are usually used for dialog navigation and which wouldn’t be generated without this style. If you need to use this style in order to get the arrows or etc., but would still like to have normal keyboard navigation take place, you should call Navigate in response to the key events for Tab and Shift-Tab.
wx.NO_FULL_REPAINT_ON_RESIZE
	 On Windows, this style used to disable repainting the window completely when its size is changed. Since this behaviour is now the default, the style is now obsolete and no longer has an effect.
wx.VSCROLL
	 Use this style to enable a vertical scrollbar. Notice that this style cannot be used with native controls which don’t support scrollbars nor with top-level windows in most ports.
wx.HSCROLL
	 Use this style to enable a horizontal scrollbar. The same limitations as for wx.VSCROLL apply to this style.
wx.ALWAYS_SHOW_SB
	 If a window has scrollbars, disable them instead of hiding them when they are not needed (i.e. when the size of the window is big enough to not require the scrollbars to navigate it). This style is currently implemented for wxMSW, wxGTK and wxUniversal and does nothing on the other platforms.
wx.CLIP_CHILDREN
	 Use this style to eliminate flicker caused by the background being repainted, then children being painted over them. Windows only.
wx.FULL_REPAINT_ON_RESIZE
	 Use this style to force a complete redraw of the window whenever it is resized instead of redrawing just the part of the window affected by resizing. Note that this was the behaviour by default before 2.5.1 release and that if you experience redraw problems with code which previously used to work you may want to try this. Currently this style applies on GTK+ 2 and Windows only, and full repainting is always done on other platforms.

#wx.Frame styles are 
wx.DEFAULT_FRAME_STYLE
	 Defined as wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN.
wx.ICONIZE
	 Display the frame iconized (minimized). Windows only.
wx.CAPTION
	 Puts a caption on the frame. Notice that this flag is required by wx.MINIMIZE_BOX, wx.MAXIMIZE_BOX and wx.CLOSE_BOX on most systems as the corresponding buttons cannot be shown if the window has no title bar at all. I.e. if wx.CAPTION is not specified those styles would be simply ignored.
wx.MINIMIZE
	 Identical to wx.ICONIZE. Windows only.
wx.MINIMIZE_BOX
	 Displays a minimize box on the frame.
wx.MAXIMIZE
	 Displays the frame maximized. Windows and GTK+ only.
wx.MAXIMIZE_BOX
	 Displays a maximize box on the frame. Notice that under wxGTK wx.RESIZE_BORDER must be used as well or this style is ignored.
wx.CLOSE_BOX
	 Displays a close box on the frame.
wx.STAY_ON_TOP
	 Stay on top of all other windows, see also wx.FRAME_FLOAT_ON_PARENT.
wx.SYSTEM_MENU
	 Displays a system menu containing the list of various windows commands in the window title bar. Unlike wx.MINIMIZE_BOX, wx.MAXIMIZE_BOX and wx.CLOSE_BOX styles this style can be used without wx.CAPTION, at least under Windows, and makes the system menu available without showing it on screen in this case. However it is recommended to only use it together with wx.CAPTION for consistent behaviour under all platforms.
wx.RESIZE_BORDER
	 Displays a resizable border around the window.
wx.FRAME_TOOL_WINDOW
	 Causes a frame with a small title bar to be created; the frame does not appear in the taskbar under Windows or GTK+.
wx.FRAME_NO_TASKBAR
	 Creates an otherwise normal frame but it does not appear in the taskbar under Windows or GTK+ (note that it will minimize to the desktop window under Windows which may seem strange to the users and thus it might be better to use this style only without wx.MINIMIZE_BOX style). In wxGTK, the flag is respected only if the window manager supports _NET_WM_STATE_SKIP_TASKBAR hint.
wx.FRAME_FLOAT_ON_PARENT
	 The frame will always be on top of its parent (unlike wx.STAY_ON_TOP). A frame created with this style must have a not None parent.
wx.FRAME_SHAPED
	 Windows with this style are allowed to have their shape changed with the SetShape method.
  
  
  
##wxpython - Standard event identifiers
#special identifier value wx.ID_ANY (-1) which is used in the following two situations:
1.When creating a new window(Frame, Panel, Control etc) , specify wx.ID_ANY 
  to let wxPython assign an unused identifier to it automatically
2.When installing an event handler using EvtHandler.Bind(event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY)
  Use from id to id2 to handle the events coming from any control,regardless of its identifier

#special identifier value is wx.ID_NONE
1. this is a value which is not matched by any other id.

#wxPython also defines a few standard command identifiers - https://docs.wxpython.org/stock_items.html#stock-items 
#These reserved identifiers are all in the range between wx.ID_LOWEST and wx.ID_HIGHEST 
#Use wx.NewId () to generate new ID 

 

##wxpython - Class Hierarchy

#Helper class 
wx.Size(width, height) 
     Store the special -1 value in wx.DefaultSize instance
     Has many methods eg 
        DecBy(self, pt)
        DecBy(self, size)
        DecBy(self, dx, dy)
        DecBy(self, d)
            Decrement by wx.Point, wx.Size etc 
        IncBy(self, pt)
        IncBy(self, size)
        IncBy(self, dx, dy)
        IncBy(self, d)
            Increment by wx.Point, wx.Size etc 
        Scale(self, xscale, yscale)
            Scales the dimensions of this object by the given factors.
        Set(self, width, height)
            Sets the width and height members.
        SetHeight(self, height)
            Sets the height.
        SetWidth(self, width)
            Sets the width.
wx.Point(x, y) 
    It contains integer x and y members
    wx.RealPoint for a floating point version.
        Get()
            returns a tuple (x,y)

#check 'wxPython Major Classes.pdf' for hierarchy

wx.Object 
    wx.Sizer 
            Use .Add(control_or_sizer, proportion=0, flag=0) to add one control or another sizer to sizer
        wx.BoxSizer(orient=wx.HORIZONTAL or wx.VERTICAL)
                Layout of controls in a row or a column or several hierarchies of either.
            wx.StaticBoxSizer(orient, parent, label='') 
                sizer derived from wx.BoxSizer but adds a static box around the sizer
        wx.GridSizer( rows, cols, vgap, hgap)
                A grid sizer is a sizer which lays out its children in a two-dimensional table with all table fields having the same size, i.e.
                the width of each field is the width of the widest child, the height of each field is the height of the tallest child.
            wx.FlexGridSizer(rows, cols, vgap, hgap)
                A flex grid sizer is a sizer which lays out its children in a two-dimensional table 
                with all table fields in one row having the same height and all fields in one column having the same width, but all rows or all columns are not necessarily the same height or width as in the wx.GridSizer.
                wx.GridBagSizer(vgap=0, hgap=0)
                    A Sizer that can lay out items in a virtual grid like a FlexGridSizer but in this case explicit positioning of the items is allowed using GBPosition, and items can optionally span more than one row and/or column using GBSpan.
            wx.WrapSizer(orient=HORIZONTAL, flags=WRAPSIZER_DEFAULT_FLAGS)
                A wrap sizer lays out its items in a single line, like a box sizer
                Once all available space in the primary direction has been used, a new line is added and items are added there.             
    wx.EvtHandler
        wx.AppConsole 
            wx.App(redirect=False, filename=None, useBestVisual=False, clearSigInt=True))
                The wx.App class represents the application and is used to:
                        bootstrap the wxPython system and initialize the underlying gui toolkit
                        set and get application-wide properties
                        implement the native windowing system main message or event loop, and to dispatch events to window instances
                        etc.
                Every wx application must have a single wx.App instance, 
                and all creation of UI objects should be delayed until after the wx.App object has been created 
                in order to ensure that the gui platform and wxWidgets have been fully initialized.
                Normally you would derive from this class and implement an OnInit method 
                that creates a frame and then calls self.SetTopWindow(frame), 
                however wx.App is also usable on it’s own without derivation.
        wx.Window(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=0, name=PanelNameStr)
            wx.NonOwnedWindow
                wx.TopLevelWindow
                    wx.Frame(parent, id=ID_ANY, title="", pos=DefaultPosition,size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
                    wx.Dialog(parent, id=ID_ANY, title="", pos=DefaultPosition,size=DefaultSize, style=DEFAULT_DIALOG_STYLE, name=DialogNameStr)
            wx.Panel(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=TAB_TRAVERSAL, name=PanelNameStr)
            wx.ScrolledWindow(parent, winid=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=ScrolledWindowStyle, name=PanelNameStr)
                Scrolled window 
            wx.Control 
                wx.AnyButton 
                    wx.Button(parent, id=ID_ANY, label="", pos=DefaultPosition,size=DefaultSize, style=0, validator=DefaultValidator, name=ButtonNameStr)
                        A button is a control that contains a text string, and is one of the most common elements of a GUI.
                        It may be placed on a dialog box or on a wx.Panel panel, or indeed on almost any other window.
                        styles:wx.BU_LEFT,wx.BU_TOP,wx.BU_RIGHT,wx.BU_BOTTOM,wx.BU_EXACTFIT,wx.BU_NOTEXT,wx.BORDER_NONE
                        Events: wx.CommandEvent : EVT_BUTTON event, when the button is clicked.
                wx.CheckBox(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=CheckBoxNameStr)
                    A checkbox is a labelled box which by default is either on (checkmark is visible) or off (no checkmark).
                    styles: wx.CHK_2STATE,wx.CHK_3STATE,wx.CHK_ALLOW_3RD_STATE_FOR_USER,wx.ALIGN_RIGHT
                    Events:wx.CommandEvent:  EVT_CHECKBOX event, when the checkbox is clicked.
                wx.Choice(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,choices=[], style=0, validator=DefaultValidator, name=ChoiceNameStr
                    A choice item is used to select one of a list of strings.
                    styles: wx.CB_SORT
                    Events:wx.CommandEvent:  EVT_CHOICE event, when an item on the list is selected
                wx.ComboBox(arent, id=ID_ANY, value="", pos=DefaultPosition,size=DefaultSize, choices=[], style=0, validator=DefaultValidator,name=ComboBoxNameStr )
                    (another base wx.TextEntry)
                    A combobox is like a combination of an edit control and a listbox.
                    It can be displayed as static list with editable or read-only text field; or a drop-down list 
                    with text field; or a drop-down list without a text field depending on the platform and presence of wx.CB_READONLY style.
                    styles: wx.CB_SIMPLE,wx.CB_DROPDOWN,wx.CB_READONLY,wx.CB_SORT,wx.TE_PROCESS_ENTER
                    Events : wx.CommandEvent
                        EVT_COMBOBOX event, when an item on the list is selected. 
                        EVT_TEXT event, when the combobox text changes.
                        EVT_TEXT_ENTER event, when RETURN is pressed in the combobox 
                        EVT_COMBOBOX_DROPDOWN event, which is generated when the list box part of the combo box is shown (drops down).
                        EVT_COMBOBOX_CLOSEUP event, which is generated when the list box of the combo box disappears (closes up)
                wx.FileCtrl(parent, id=ID_ANY, defaultDirectory="",defaultFilename="", wildCard=FileSelectorDefaultWildcardStr, style=FC_DEFAULT_STYLE, pos=DefaultPosition, size=DefaultSize, name=FileCtrlNameStr)
                    This control allows the user to select a file.
                    styles: wx.FC_DEFAULT_STYLE,wx.FC_OPEN,wx.FC_SAVE,wx.FC_MULTIPLE,wx.FC_NOSHOWHIDDEN
                    Events: wx.FileCtrlEvent:
                        EVT_FILECTRL_FILEACTIVATED,The user activated a file(by double-clicking or pressing Enter)
                        EVT_FILECTRL_SELECTIONCHANGED, The user changed the current selection(by selecting or deselecting a file)
                        EVT_FILECTRL_FOLDERCHANGED, The current folder of the file control has been changed
                        EVT_FILECTRL_FILTERCHANGED, The current file filter of the file control has been changed.
                wx.Gauge(parent, id=ID_ANY, range=100, pos=DefaultPosition,size=DefaultSize, style=GA_HORIZONTAL, validator=DefaultValidator, name=GaugeNameStr)
                        A gauge is a horizontal or vertical bar which shows a quantity (often time).
                        Use GetRange and SetRange for range and GetValue and SetValue for  get/set value 
                        styles: wx.GA_HORIZONTAL,wx.GA_VERTICAL,wx.GA_SMOOTH:
                wx.GenericDirCtrl(parent, id=ID_ANY, dir=DirDialogDefaultFolderStr, pos=DefaultPosition, size=DefaultSize, style=DIRCTRL_3D_INTERNAL,filter="", defaultFilter=0, name=TreeCtrlNameStr)
                    This control can be used to place a directory listing (with optional files) on an arbitrary window.
                    styles:wx.DIRCTRL_DIR_ONLY,wx.DIRCTRL_3D_INTERNAL,wx.DIRCTRL_SELECT_FIRST,wx.DIRCTRL_SHOW_FILTERS,wx.DIRCTRL_EDIT_LABELS,wx.DIRCTRL_MULTIPLE
                    Events:
                        EVT_DIRCTRL_SELECTIONCHANGED for Selected directory has changed
                wx.InfoBar(parent, winid=ID_ANY)
                        An info bar is a transient window shown at top or bottom of its parent window to display non-critical information to the user.
                        Use .ShowMessage(msg, flags=ICON_INFORMATION)
                wx.ListBox(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, choices=[], style=0, validator=DefaultValidator, name=ListBoxNameStr)
                    A listbox is used to select one or more of a list of strings.
                    styles:wx.LB_SINGLE:,wx.LB_MULTIPLE,wx.LB_EXTENDED,wx.LB_HSCROLL,wx.LB_ALWAYS_SB,wx.LB_NEEDED_SB:,wx.LB_NO_SB,wx.LB_SORT
                    Events: wx.CommandEvent parameter.
                        EVT_LISTBOX event, when an item on the list is selected or the selection changes.
                        EVT_LISTBOX_DCLICK event, when the listbox is double-clicked.
                wx.ListCtrl(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,style=LC_ICON, validator=DefaultValidator, name=ListCtrlNameStr)
                    A list control presents lists in a number of formats: list view, report view, icon view and small icon view. 
                    Styles:wx.LC_LIST,wx.LC_REPORT,wx.LC_VIRTUAL,wx.LC_ICON,wx.LC_SMALL_ICON,wx.LC_ALIGN_TOP,wx.LC_ALIGN_LEFT
                    wx.LC_AUTOARRANGE,wx.LC_EDIT_LABELS,wx.LC_NO_HEADER,wx.LC_SINGLE_SEL,wx.LC_SORT_ASCENDING,wx.LC_SORT_DESCENDING,wx.LC_HRULES,wx.LC_VRULES
                    Events: wx.ListEvent
                        EVT_LIST_BEGIN_DRAG: Begin dragging with the left mouse button. 
                        EVT_LIST_BEGIN_RDRAG: Begin dragging with the right mouse button. 
                        EVT_BEGIN_LABEL_EDIT: Begin editing a label. This can be prevented by calling Veto(). 
                        EVT_LIST_END_LABEL_EDIT: Finish editing a label. This can be prevented by calling Veto(). 
                        EVT_LIST_DELETE_ITEM: An item was deleted. 
                        EVT_LIST_DELETE_ALL_ITEMS: All items were deleted. 
                        EVT_LIST_ITEM_SELECTED: The item has been selected. 
                        EVT_LIST_ITEM_DESELECTED: The item has been deselected. 
                        EVT_LIST_ITEM_ACTIVATED: The item has been activated (ENTER or double click). 
                        EVT_LIST_ITEM_FOCUSED: The currently focused item has changed. 
                        EVT_LIST_ITEM_MIDDLE_CLICK: The middle mouse button has been clicked on an item. This is only supported by the generic control. 
                        EVT_LIST_ITEM_RIGHT_CLICK: The right mouse button has been clicked on an item. 
                        EVT_LIST_KEY_DOWN: A key has been pressed. 
                        EVT_LIST_INSERT_ITEM: An item has been inserted. 
                        EVT_LIST_COL_CLICK: A column (m_col) has been left-clicked. 
                        EVT_LIST_COL_RIGHT_CLICK: A column (m_col) has been right-clicked. 
                        EVT_LIST_COL_BEGIN_DRAG: The user started resizing a column - can be vetoed. 
                        EVT_LIST_COL_DRAGGING: The divider between columns is being dragged. 
                        EVT_LIST_COL_END_DRAG: A column has been resized by the user. 
                        EVT_LIST_CACHE_HINT: Prepare cache for a virtual list control. 
                wx.RadioBox(parent, id=ID_ANY, label="", pos=DefaultPosition,size=DefaultSize, choices=[], majorDimension=0, style=RA_SPECIFY_COLS, validator=DefaultValidator, name=RadioBoxNameStr)
                    A radio box item is used to select one of number of mutually exclusive choices.
                    styles: wx.RA_SPECIFY_ROWS,wx.RA_SPECIFY_COLS
                    Events:wx.CommandEvent
                        EVT_RADIOBOX event, when a radiobutton is clicked.
                wx.RadioButton(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=RadioButtonNameStr)
                    A radio button item is a button which usually denotes one of several mutually exclusive options.
                    Styles:wx.RB_GROUP,wx.RB_SINGLE
                    events:wx.CommandEvent
                        EVT_RADIOBUTTON event, when the radiobutton is clicked.
                wx.Slider(parent, id=ID_ANY, value=0, minValue=0, maxValue=100,pos=DefaultPosition, size=DefaultSize, style=SL_HORIZONTAL,validator=DefaultValidator, name=SliderNameStr)
                    A slider is a control with a handle which can be pulled back and forth to change the value.
                    Styles:    wx.SL_HORIZONTAL,wx.SL_VERTICAL,wx.SL_AUTOTICKS,wx.SL_MIN_MAX_LABELS,wx.SL_VALUE_LABEL,wx.SL_LABELS,wx.SL_LEFT,wx.SL_RIGHT,wx.SL_TOP,wx.SL_BOTTOM,wx.SL_SELRANGE,wx.SL_INVERSE: Inverses the minimum and maximum endpoints on the slider. Not compatible with wx.SL_SELRANGE.
                    Events:wx.ScrollEvent
                        EVT_SCROLL: Process all scroll events.
                        EVT_SCROLL_TOP: Process scroll-to-top events (minimum position).
                        EVT_SCROLL_BOTTOM: Process scroll-to-bottom events (maximum position).
                        EVT_SCROLL_LINEUP: Process line up events.
                        EVT_SCROLL_LINEDOWN: Process line down events.
                        EVT_SCROLL_PAGEUP: Process page up events.
                        EVT_SCROLL_PAGEDOWN: Process page down events.
                        EVT_SCROLL_THUMBTRACK: Process thumbtrack events (frequent events sent as the user drags the thumbtrack).
                        EVT_SCROLL_THUMBRELEASE: Process thumb release events.
                        EVT_SCROLL_CHANGED: Process end of scrolling events (MSW only).
                        EVT_COMMAND_SCROLL: Process all scroll events.
                        EVT_COMMAND_SCROLL_TOP: Process scroll-to-top events (minimum position).
                        EVT_COMMAND_SCROLL_BOTTOM: Process scroll-to-bottom events (maximum position).
                        EVT_COMMAND_SCROLL_LINEUP: Process line up events.
                        EVT_COMMAND_SCROLL_LINEDOWN: Process line down events.
                        EVT_COMMAND_SCROLL_PAGEUP: Process page up events.
                        EVT_COMMAND_SCROLL_PAGEDOWN: Process page down events.
                        EVT_COMMAND_SCROLL_THUMBTRACK: Process thumbtrack events (frequent events sent as the user drags the thumbtrack).
                        EVT_COMMAND_SCROLL_THUMBRELEASE: Process thumb release events.
                        EVT_COMMAND_SCROLL_CHANGED: Process end of scrolling events (MSW only).
                        EVT_SLIDER: Process which is generated after any change of wx.Slider position in addition to one of the events above. Notice that the handler of this event receives a wx.CommandEvent as argument and not wx.ScrollEvent, as all the other handlers.
                wx.SpinCtrl(parent, id=ID_ANY, value="", pos=DefaultPosition,size=DefaultSize, style=SP_ARROW_KEYS, min=0, max=100, initial=0,name="wxSpinCtrl")
                    SpinCtrl combines TextCtrl and SpinButton in one control. Displays a integer
                    Styles: wx.SP_ARROW_KEYS,wx.SP_WRAP,wx.TE_PROCESS_ENTER,wx.ALIGN_LEFT,wx.ALIGN_CENTRE_HORIZONTAL,wx.ALIGN_RIGHT,events Events Emitted by this Class
                    Events:wx.SpinEvent
                    EVT_SPINCTRL event, which is generated whenever the numeric value of the spin control is updated.
                wx.SpinCtrlDouble(parent, id=-1, value="", pos=DefaultPosition,size=DefaultSize, style=SP_ARROW_KEYS, min=0, max=100, initial=0, inc=1,name=T("wxSpinCtrlDouble"))
                    SpinCtrlDouble combines TextCtrl and SpinButton in one control and displays a real number.   
                    Styles: wx.SP_ARROW_KEYS,wx.SP_WRAP
                    Events: wx.SpinDoubleEvent
                        EVT_SPINCTRLDOUBLE: Generated whenever the numeric value of the spin control is changed, that is, when the up/down spin button is clicked, when ENTER is pressed, or the control loses focus and the new value is different from the last. See wx.SpinDoubleEvent.
                wx.StaticBitmap(parent, id=ID_ANY, bitmap=NullBitmap, pos=DefaultPosition,size=DefaultSize, style=0, name=StaticBitmapNameStr)
                    A static bitmap control displays a bitmap.
                wx.StaticBox(parent, id=ID_ANY, label="", pos=DefaultPosition, size=DefaultSize, style=0, name=StaticBoxNameStr)
                    A static box is a rectangle drawn around other windows to denote a logical grouping of items.
                wx.StaticLine(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,style=LI_HORIZONTAL, name=StaticLineNameStr)
                    A static line is just a line which may be used in a dialog to separate the groups of controls.
                    Styles: wx.LI_HORIZONTALwx.LI_VERTICAL   
                wx.StaticText(parent, id=ID_ANY, label="", pos=DefaultPosition,size=DefaultSize, style=0, name=StaticTextNameStr)
                    A static text control displays one or more lines of read-only text.
                    Styles: wx.ALIGN_LEFT,wx.ALIGN_RIGHT,wx.ALIGN_CENTRE_HORIZONTAL,wx.ST_NO_AUTORESIZE,wx.ST_ELLIPSIZE_START,wx.ST_ELLIPSIZE_MIDDLE,wx.ST_ELLIPSIZE_END,See also
                wx.TextCtrl(parent, id=ID_ANY, value="", pos=DefaultPosition,size=DefaultSize, style=0, validator=DefaultValidator,name=TextCtrlNameStr)
                        (another base wx.TextEntry)A text control allows text to be displayed and edited.
                        Styles:wx.TE_PROCESS_ENTER,wx.TE_PROCESS_TAB,wx.TE_MULTILINE,wx.TE_PASSWORD,wx.TE_READONLY,wx.TE_RICH,wx.TE_RICH2,wx.TE_AUTO_URL,wx.TE_NOHIDESEL,wx.HSCROLL,wx.TE_NO_VSCROLL,wx.TE_LEFT,wx.TE_CENTRE,wx.TE_RIGHT,wx.TE_DONTWRAP,wx.TE_CHARWRAP,wx.TE_WORDWRAP,wx.TE_BESTWRAP,TE_CAPITALIZE,Note that alignment styles (wx``wx.TE_LEFT``, wx.TE_CENTRE and wx.TE_RIGHT) can be changed dynamically after control creation on wxMSW and wxGTK. wx.TE_READONLY, wx.TE_PASSWORD and wrapping styles can be dynamically changed under wxGTK but not wxMSW. The other styles can be only set during control creation.
                        Events:wx.CommandEvent 
                            EVT_TEXT event, generated when the text changes. Notice that this event will be sent when the text controls contents changes wx.TextCtrl.SetValue is called); see wx.TextCtrl.ChangeValue for a function which does not send this event. This event is however not sent during the control creation.
                            EVT_TEXT_ENTER event, generated when enter is pressed in a text control which must have wx.TE_PROCESS_ENTER style for this event to be generated.
                            EVT_TEXT_URL: A mouse event occurred over an URL in the text control (wxMSW and wxGTK2 only currently).
                            EVT_TEXT_MAXLEN: This event is generated when the user tries to enter more text into the control than the limit set by wx.TextCtrl.SetMaxLength , see its description.
                        wx.SearchCtrl(parent, id=ID_ANY, value="", pos=DefaultPosition,size=DefaultSize, style=0, validator=DefaultValidator,name=SearchCtrlNameStr)
                            A search control is a composite control with a search button, a text control, and a cancel button.
                            Styles:wx.TE_PROCESS_ENTER,wx.TE_PROCESS_TAB,wx.TE_NOHIDESEL,wx.TE_LEFT,wx.TE_CENTRE,wx.TE_RIGHT,TE_CAPITALIZE,events Events Emitted by this Class
                            Events:wx.CommandEvent
                                EVT_SEARCHCTRL_SEARCH_BTN event, generated when the search button is clicked. Note that this does not initiate a search on its own, you need to perform the appropriate action in your event handler. You may use:
                TreeCtrl(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,style=TR_DEFAULT_STYLE, validator=DefaultValidator, name=TreeCtrlNameStr)
                    A tree control presents information as a hierarchy, with items that may be expanded to show further items.
                    Styles: wx.TR_EDIT_LABELS,wx.TR_NO_BUTTONS,wx.TR_HAS_BUTTONS,wx.TR_TWIST_BUTTONS,wx.TR_NO_LINES,wx.TR_FULL_ROW_HIGHLIGHT,wx.TR_LINES_AT_ROOT,wx.TR_HIDE_ROOT,wx.TR_ROW_LINES,wx.TR_HAS_VARIABLE_ROW_HEIGHT,wx.TR_SINGLE,wx.TR_MULTIPLE,wx.TR_DEFAULT_STYLE: The set of flags that are closest to the defaults for the native control for a particular toolkit.
                    Events: wx.TreeEvent 
                        EVT_TREE_BEGIN_DRAG: Begin dragging with the left mouse button. If you want to enable left-dragging you need to intercept this event and explicitly call wx.TreeEvent.Allow , as it’s vetoed by default. Processes a wxEVT_TREE_BEGIN_DRAG event type.
                        EVT_TREE_BEGIN_RDRAG: Begin dragging with the right mouse button. If you want to enable right-dragging you need to intercept this event and explicitly call wx.TreeEvent.Allow , as it’s vetoed by default. Processes a wxEVT_TREE_BEGIN_RDRAG event type.
                        EVT_TREE_END_DRAG: End dragging with the left or right mouse button. Processes a wxEVT_TREE_END_DRAG event type.
                        EVT_TREE_BEGIN_LABEL_EDIT: Begin editing a label. This can be prevented by calling Veto(). Processes a wxEVT_TREE_BEGIN_LABEL_EDIT event type.
                        EVT_TREE_END_LABEL_EDIT: Finish editing a label. This can be prevented by calling Veto(). Processes a wxEVT_TREE_END_LABEL_EDIT event type.
                        EVT_TREE_DELETE_ITEM: An item was deleted. Processes a wxEVT_TREE_DELETE_ITEM event type.
                        EVT_TREE_GET_INFO: Request information from the application. Processes a wxEVT_TREE_GET_INFO event type.
                        EVT_TREE_SET_INFO: Information is being supplied. Processes a wxEVT_TREE_SET_INFO event type.
                        EVT_TREE_ITEM_ACTIVATED: The item has been activated, i.e. chosen by double clicking it with mouse or from keyboard. Processes a wxEVT_TREE_ITEM_ACTIVATED event type.
                        EVT_TREE_ITEM_COLLAPSED: The item has been collapsed. Processes a wxEVT_TREE_ITEM_COLLAPSED event type.
                        EVT_TREE_ITEM_COLLAPSING: The item is being collapsed. This can be prevented by calling Veto(). Processes a wxEVT_TREE_ITEM_COLLAPSING event type.
                        EVT_TREE_ITEM_EXPANDED: The item has been expanded. Processes a wxEVT_TREE_ITEM_EXPANDED event type.
                        EVT_TREE_ITEM_EXPANDING: The item is being expanded. This can be prevented by calling Veto(). Processes a wxEVT_TREE_ITEM_EXPANDING event type.
                        EVT_TREE_ITEM_RIGHT_CLICK: The user has clicked the item with the right mouse button. Processes a wxEVT_TREE_ITEM_RIGHT_CLICK event type.
                        EVT_TREE_ITEM_MIDDLE_CLICK: The user has clicked the item with the middle mouse button. This is only supported by the generic control. Processes a wxEVT_TREE_ITEM_MIDDLE_CLICK event type.
                        EVT_TREE_SEL_CHANGED: Selection has changed. Processes a wxEVT_TREE_SEL_CHANGED event type.
                        EVT_TREE_SEL_CHANGING: Selection is changing. This can be prevented by calling Veto(). Processes a wxEVT_TREE_SEL_CHANGING event type.
                        EVT_TREE_KEY_DOWN: A key has been pressed. Processes a wxEVT_TREE_KEY_DOWN event type.
                        EVT_TREE_ITEM_GETTOOLTIP: The opportunity to set the item tooltip is being given to the application (call wx.TreeEvent.SetToolTip ). Windows only. Processes a wxEVT_TREE_ITEM_GETTOOLTIP event type.
                        EVT_TREE_ITEM_MENU: The context menu for the selected item has been requested, either by a right click or by using the menu key. Processes a wxEVT_TREE_ITEM_MENU event type.
                        EVT_TREE_STATE_IMAGE_CLICK: The state image has been clicked. Processes a wxEVT_TREE_STATE_IMAGE_CLICK event type.

#List of Methods 
#check details at https://docs.wxpython.org/wx.1moduleindex.html        
wx.Object 
    Root object 
    #Methods summary 
    __init__ 	    Default constructor; initializes to None the internal reference data.
    Destroy 	    Deletes the C++ object this Python object is a proxy for.
    GetClassName 	Returns the class name of the C++ class using RTTI.
    GetRefData 	    Returns the Object.m_refData pointer, i.e. the data referenced by this object.
    IsSameAs 	    Returns True if this object has the same data pointer as obj.
    Ref 	        Makes this object refer to the data in clone.
    SetRefData 	    Sets the Object.m_refData pointer.
    UnRef 	        Decrements the reference count in the associated data, and if it is zero, deletes the data.
    UnShare 	    This is the same of AllocExclusive but this method is public.

wx.EvtHandler
    A class that can handle events from the windowing system.
    #Methods summary 
    AddFilter 	        Add an event filter whose FilterEvent() method will be called for each and every event processed by wxWidgets.
    AddPendingEvent 	Post an event to be processed later.
    Bind 	            Bind an event to an event handler.
    Connect 	        Make an entry in the dynamic event table for an event binding.
    DeletePendingEvents 	Deletes all events queued on this event handler using wx.QueueEvent or AddPendingEvent .
    Disconnect 	        Remove an event binding by removing its entry in the dynamic event table.
    GetEvtHandlerEnabled 	Returns True if the event handler is enabled, False otherwise.
    GetNextHandler 	    Returns the pointer to the next handler in the chain.
    GetPreviousHandler 	Returns the pointer to the previous handler in the chain.
    IsUnlinked 	        Returns True if the next and the previous handler pointers of this event handler instance are None.
    ProcessEvent 	    Processes an event, searching event tables and calling zero or more suitable event handler function(s).
    ProcessEventLocally 	Try to process the event in this handler and all those chained to it.
    ProcessPendingEvents 	Processes the pending events previously queued using wx.QueueEvent or AddPendingEvent ; you must call this function only if you are sure there are pending events for this handler, otherwise a CHECK will fail.
    QueueEvent 	        Queue event for a later processing.
    RemoveFilter 	    Remove a filter previously installed with AddFilter .
    SafelyProcessEvent 	Processes an event by calling wx.ProcessEvent and handles any exceptions that occur in the process.
    SetEvtHandlerEnabled 	Enables or disables the event handler.
    SetNextHandler 	    Sets the pointer to the next handler.
    SetPreviousHandler 	Sets the pointer to the previous handler.
    TryAfter 	        Method called by wx.ProcessEvent as last resort.
    TryBefore 	        Method called by wx.ProcessEvent before examining this object event tables.
    Unbind 	            Disconnects the event handler binding for event from self.
    Unlink 	            Unlinks this event handler from the chain it’s part of (if any); then links the 'previous' event handler to the 'next' one (so that the chain won’t be interrupted).



wx.Window(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=0, name=PanelNameStr)
    wx.Window is the base class for all windows and represents any visible object on screen.
    Most of the wx.Class(child of wx.Window) have similar constructors ie (a parent object, followed by an Id). 
    eg Use None for "no parent" and wx.ID_ANY to have wxWidgets pick an id 
        wx.Class(parent, id=ID_ANY, title="", pos=DefaultPosition,size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
    All children of the window will be deleted automatically by the destructor 
    before the window itself is deleted 
    #Methods Summary
    AcceptsFocus 	            This method may be overridden in the derived classes to return False to indicate that this control doesn’t accept input at all (i.e. behaves like e.g. wx.StaticText) and so doesn’t need focus.
    AcceptsFocusFromKeyboard 	This method may be overridden in the derived classes to return False to indicate that while this control can, in principle, have focus if the user clicks it with the mouse, it shouldn’t be included in the TAB traversal chain when using the keyboard.
    AcceptsFocusRecursively 	Overridden to indicate whether this window or one of its children accepts focus.
    AddChild 	                Adds a child window.
    AdjustForLayoutDirection 	Mirror coordinates for RTL layout if this window uses it and if the mirroring is not done automatically like Win32.
    AlwaysShowScrollbars 	    Call this function to force one or both scrollbars to be always shown, even if the window is big enough to show its entire contents without scrolling.
    AssociateHandle 	        Associate the window with a new native handle
    BeginRepositioningChildren 	Prepare for changing positions of multiple child windows.
    CacheBestSize 	            Sets the cached best size value.
    CanAcceptFocus 	            Can this window have focus right now?
    CanAcceptFocusFromKeyboard 	Can this window be assigned focus from keyboard right now?
    CanScroll 	                Returns True if this window can have a scroll bar in this orientation.
    CanSetTransparent 	        Returns True if the system supports transparent windows and calling SetTransparent may succeed.
    CaptureMouse 	            Directs all mouse input to this window.
    Center 	                    A synonym for wx.Centre .
    CenterOnParent 	            A synonym for CentreOnParent .
    Centre 	                    Centres the window.
    CentreOnParent 	            Centres the window on its parent.
    ClearBackground 	        Clears the window by filling it with the current background colour.
    ClientToScreen 	            Converts to screen coordinates from coordinates relative to this window.
    ClientToWindowSize 	        Converts client area size size to corresponding window size.
    Close 	                    This function simply generates a wx.CloseEvent whose handler usually tries to close the window.
    ConvertDialogToPixels 	    Converts a point or size from dialog units to pixels.
    ConvertPixelsToDialog 	    Converts a point or size from pixels to dialog units.
    Create 	 
    DLG_UNIT 	                A convenience wrapper for ConvertDialogToPixels.
    Destroy 	                Destroys the window safely.
    DestroyChildren 	        Destroys all children of a window.
    DestroyLater 	            Schedules the window to be destroyed in the near future.
    Disable 	                Disables the window.
    DissociateHandle 	        Dissociate the current native handle from the window
    DoGetBestClientSize 	    Override this method to return the best size for a custom control.
    DoGetBestSize 	            Implementation of GetBestSize that can be overridden.
    DoUpdateWindowUI 	        Does the window-specific updating after processing the update event.
    DragAcceptFiles 	        Enables or disables eligibility for drop file events (OnDropFiles).
    Enable 	                    Enable or disable the window for user input.
    EndRepositioningChildren 	Fix child window positions after setting all of them at once.
    FindFocus 	                Finds the window or control which currently has the keyboard focus.
    FindWindow 	                Find a child of this window, by id.
    FindWindowById 	            Find the first window with the given id.
    FindWindowByLabel 	        Find a window by its label.
    FindWindowByName 	        Find a window by its name (as given in a window constructor or Create function call).
    Fit 	                    Sizes the window so that it fits around its subwindows.
    FitInside 	                Similar to Fit , but sizes the interior (virtual) size of a window.
    Freeze 	                    Freezes the window or, in other words, prevents any updates from taking place on screen, the window is not redrawn at all.
    GetAcceleratorTable 	    Gets the accelerator table for this window.
    GetAutoLayout 	            Returns the sizer of which this window is a member, if any, otherwise None.
    GetBackgroundColour 	    Returns the background colour of the window.
    GetBackgroundStyle 	        Returns the background style of the window.
    GetBestHeight 	            Returns the best height needed by this window if it had the given width.
    GetBestSize 	            This functions returns the best acceptable minimal size for the window.
    GetBestVirtualSize 	        Return the largest of ClientSize and BestSize (as determined by a sizer, interior children, or other means)
    GetBestWidth 	            Returns the best width needed by this window if it had the given height.
    GetBorder 	                Get the window border style from the given flags: this is different from simply doing flags wx.BORDER_MASK because it uses GetDefaultBorder() to translate wx.BORDER_DEFAULT to something reasonable.
    GetCapture 	                Returns the currently captured window.
    GetCaret 	                Returns the caret() associated with the window.
    GetCharHeight 	            Returns the character height for this window.
    GetCharWidth 	            Returns the average character width for this window.
    GetChildren 	            Returns a reference to the list of the window’s children.
    GetClassDefaultAttributes 	Returns the default font and colours which are used by the control.
    GetClientAreaOrigin 	    Get the origin of the client area of the window relative to the window top left corner (the client area may be shifted because of the borders, scrollbars, other decorations...)
    GetClientRect 	            Get the client rectangle in window (i.e. client) coordinates.
    GetClientSize 	            Returns the size of the window ‘client area’ in pixels.
    GetConstraints 	            Returns a pointer to the window’s layout constraints, or None if there are none.
    GetContainingSizer 	        Returns the sizer of which this window is a member, if any, otherwise None.
    GetContentScaleFactor 	    Returns the magnification of the backing store of this window, eg 2.0 for a window on a retina screen.
    GetCursor 	                Return the cursor associated with this window.
    GetDefaultAttributes 	    Currently this is the same as calling Window.GetClassDefaultAttributes(wxWindow.GetWindowVariant()).
    GetDropTarget 	            Returns the associated drop target, which may be None.
    GetEffectiveMinSize 	    Merges the window’s best size into the min size and returns the result.
    GetEventHandler 	        Returns the event handler for this window.
    GetExtraStyle 	            Returns the extra style bits for the window.
    GetFont 	                Returns the font for this window.
    GetForegroundColour 	    Returns the foreground colour of the window.
    GetGrandParent 	            Returns the grandparent of a window, or None if there isn’t one.
    GetGtkWidget 	 
    GetHandle 	                Returns the platform-specific handle of the physical window.
    GetHelpText 	            Gets the help text to be used as context-sensitive help for this window.
    GetHelpTextAtPoint 	        Gets the help text to be used as context-sensitive help for this window.
    GetId 	                    Returns the identifier of the window.
    GetLabel 	                Generic way of getting a label from any window, for identification purposes.
    GetLayoutDirection 	        Returns the layout direction for this window, Note that Layout_Default is returned if layout direction is not supported.
    GetMaxClientSize 	        Returns the maximum size of window’s client area.
    GetMaxHeight 	            Returns the vertical component of window maximal size.
    GetMaxSize 	                Returns the maximum size of the window.
    GetMaxWidth 	            Returns the horizontal component of window maximal size.
    GetMinClientSize 	        Returns the minimum size of window’s client area, an indication to the sizer layout mechanism that this is the minimum required size of its client area.
    GetMinHeight 	            Returns the vertical component of window minimal size.
    GetMinSize 	                Returns the minimum size of the window, an indication to the sizer layout mechanism that this is the minimum required size.
    GetMinWidth 	            Returns the horizontal component of window minimal size.
    GetName 	                Returns the window’s name.
    GetNextSibling 	            Returns the next window after this one among the parent’s children or None if this window is the last child.
    GetParent 	                Returns the parent of the window, or None if there is no parent.
    GetPopupMenuSelectionFromUser 	This function shows a popup menu at the given position in this window and returns the selected id.
    GetPosition 	            This gets the position of the window in pixels, relative to the parent window for the child windows or relative to the display origin for the top level windows.
    GetPrevSibling 	            Returns the previous window before this one among the parent’s children or
    GetRect 	                Returns the position and size of the window as a wx.Rect object.
    GetScreenPosition 	        Returns the window position in screen coordinates, whether the window is a child window or a top level one.
    GetScreenRect 	            Returns the position and size of the window on the screen as a wx.Rect object.
    GetScrollPos 	            Returns the built-in scrollbar position.
    GetScrollRange 	            Returns the built-in scrollbar range.
    GetScrollThumb 	            Returns the built-in scrollbar thumb size.
    GetSize 	                Returns the size of the entire window in pixels, including title bar, border, scrollbars, etc.
    GetSizer 	                Returns the sizer associated with the window by a previous call to SetSizer , or None.
    GetFullTextExtent 	        Gets the dimensions of the string as it would be drawn on the window with the currently selected font.
    GetThemeEnabled 	        Clears the window by filling it with the current background colour.
    GetToolTip 	                Get the associated tooltip or None if none.
    GetToolTipText 	            Get the text of the associated tooltip or empty string if none.
    GetTopLevelParent 	        Returns the first ancestor of this window which is a top-level window.
    GetUpdateClientRect         Get the update rectangle bounding box in client coords.
    GetUpdateRegion 	        Returns the region specifying which parts of the window have been damaged.
    GetValidator 	            Validator functions.
    GetVirtualSize 	            This gets the virtual size of the window in pixels.
    GetWindowBorderSize         Returns the size of the left/right and top/bottom borders of this window in x and y components of the result respectively.
    GetWindowStyle 	            See GetWindowStyleFlag for more info.
    GetWindowStyleFlag 	        Gets the window style that was passed to the constructor or Create method.
    GetWindowVariant 	        Returns the value previously passed to SetWindowVariant .
    HandleAsNavigationKey 	    This function will generate the appropriate call to Navigate if the key event is one normally used for keyboard navigation and return True in this case.
    HandleWindowEvent 	        
    HasCapture 	                Returns True if this window has the current mouse capture.
    HasExtraStyle 	            Returns True if the window has the given exFlag bit set in its extra styles.
    HasFlag 	                Returns True if the window has the given flag bit set.
    HasFocus 	                Returns True if the window (or in case of composite controls, its main child window) has focus.
    HasMultiplePages 	        This method should be overridden to return True if this window has multiple pages.
    HasScrollbar 	            Returns True if this window currently has a scroll bar for this orientation.
    HasTransparentBackground 	Returns True if this window background is transparent (as, for example, for wx.StaticText) and should show the parent window background.
    Hide 	                    Equivalent to calling wx.Window.Show (False).
    HideWithEffect 	            This function hides a window, like Hide , but using a special visual effect if possible.
    HitTest 	                Get the window border style from the given flags: this is different from simply doing flags wx.BORDER_MASK because it uses GetDefaultBorder() to translate wx.BORDER_DEFAULT to something reasonable.
    InformFirstDirection 	    wx.Sizer and friends use this to give a chance to a component to recalc its min size once one of the final size components is known.
    InheritAttributes 	        This function is (or should be, in case of custom controls) called during window creation to intelligently set up the window visual attributes, that is the font and the foreground and background colours.
    InheritsBackgroundColour 	Return True if this window inherits the background colour from its parent.
    InitDialog 	                Sends an wxEVT_INIT_DIALOG event, whose handler usually transfers data to the dialog via validators.
    InvalidateBestSize 	        Resets the cached best size value so it will be recalculated the next time it is needed.
    IsBeingDeleted 	            Returns True if this window is in process of being destroyed.
    IsDescendant 	            Check if the specified window is a descendant of this one.
    IsDoubleBuffered 	        Returns True if the window contents is double-buffered by the system, i.e. if any drawing done on the window is really done on a temporary backing surface and transferred to the screen all at once later.
    IsEnabled 	                Returns True if the window is enabled, i.e. if it accepts user input, False otherwise.
    IsExposed 	                Returns True if the given point or rectangle area has been exposed since the last repaint.
    IsFocusable 	            Can this window itself have focus?
    IsFrozen 	                Returns True if the window is currently frozen by a call to Freeze .
    IsRetained 	                Returns True if the window is retained, False otherwise.
    IsScrollbarAlwaysShown 	    Return whether a scrollbar is always shown.
    IsShown 	                Returns True if the window is shown, False if it has been hidden.
    IsShownOnScreen 	        Returns True if the window is physically visible on the screen, i.e. it is shown and all its parents up to the toplevel window are shown as well.
    IsThisEnabled 	            Returns True if this window is intrinsically enabled, False otherwise, i.e. if Enable Enable(false) had been called.
    IsTopLevel 	                Returns True if the given window is a top-level one.
    IsTransparentBackgroundSupported 	Checks whether using transparent background might work.
    Layout 	                    Invokes the constraint-based layout algorithm or the sizer-based algorithm for this window.
    LineDown 	                Same as ScrollLines (1).
    LineUp 	                    Same as ScrollLines (-1).
    Lower 	                    Lowers the window to the bottom of the window hierarchy (Z-order).
    MacIsWindowScrollbar 	    Is the given widget one of this window’s built-in scrollbars? Only applicable on Mac.
    Move 	                    Moves the window to the given position.
    MoveAfterInTabOrder 	    Moves this window in the tab navigation order after the specified win.
    MoveBeforeInTabOrder 	    Same as MoveAfterInTabOrder except that it inserts this window just before win instead of putting it right after it.
    Navigate 	                Performs a keyboard navigation action starting from this window.
    NavigateIn 	                Performs a keyboard navigation action inside this window.
    NewControlId 	            Create a new ID or range of IDs that are not currently in use.
    OnInternalIdle 	            This virtual function is normally only used internally, but sometimes an application may need it to implement functionality that should not be disabled by an application defining an OnIdle handler in a derived class.
    PageDown 	                Same as ScrollPages (1).
    PageUp 	                    Same as ScrollPages (-1).
    PopEventHandler 	        Removes and returns the top-most event handler on the event handler stack.
    PopupMenu 	                Pops up the given menu at the specified coordinates, relative to this window, and returns control when the user has dismissed the menu.
    PostSizeEvent 	            Posts a size event to the window.
    PostSizeEventToParent 	    Posts a size event to the parent of this window.
    ProcessEvent 	            This function is public in wx.EvtHandler but protected in wx.Window because for Windows you should always call wx.ProcessEvent on the pointer returned by GetEventHandler and not on the wx.Window object itself.
    ProcessWindowEvent 	        Convenient wrapper for wx.ProcessEvent.
    ProcessWindowEventLocally 	Wrapper for wx.EvtHandler.ProcessEventLocally .
    PushEventHandler 	        Pushes this event handler onto the event stack for the window.
    Raise 	                    Raises the window to the top of the window hierarchy (Z-order).
    Refresh 	                Causes this window, and all of its children recursively (except under GTK1 where this is not implemented), to be repainted.
    RefreshRect 	            Redraws the contents of the given rectangle: only the area inside it will be repainted.
    RegisterHotKey 	            Registers a system wide hotkey.
    ReleaseMouse 	            Releases mouse input captured with CaptureMouse .
    RemoveChild 	            Removes a child window.
    RemoveEventHandler 	        Find the given handler in the windows event handler stack and removes (but does not delete) it from the stack.
    Reparent 	                Reparents the window, i.e. the window will be removed from its current parent window (e.g.
    ScreenToClient 	            Converts from screen to client window coordinates.
    ScrollLines 	            Scrolls the window by the given number of lines down (if lines is positive) or up.
    ScrollPages 	            Scrolls the window by the given number of pages down (if pages is positive) or up.
    ScrollWindow 	            Physically scrolls the pixels in the window and move child windows accordingly.
    SendDestroyEvent 	        Generate wx.WindowDestroyEvent for this window.
    SendIdleEvents 	            Send idle event to window and all subwindows.
    SendSizeEvent 	            This function sends a dummy size event to the window allowing it to re-layout its children positions.
    SendSizeEventToParent 	    Safe wrapper for GetParent . SendSizeEvent .
    SetAcceleratorTable 	    Sets the accelerator table for this window.
    SetAutoLayout 	            Determines whether the Layout function will be called automatically when the window is resized.
    SetBackgroundColour 	    Sets the background colour of the window.
    SetBackgroundStyle 	        Sets the background style of the window.
    SetCanFocus 	            This method is only implemented by ports which have support for native TAB traversal (such as GTK+ 2.0).
    SetCaret 	                Sets the caret() associated with the window.
    SetClientRect 	 
    SetClientSize 	            This sets the size of the window client area in pixels.
    SetConstraints 	            Sets the window to have the given layout constraints.
    SetContainingSizer 	        This normally does not need to be called by user code.
    SetCursor 	                Sets the window’s cursor.
    SetDimensions 	 
    SetDoubleBuffered 	        Turn on or off double buffering of the window if the system supports it.
    SetDropTarget 	            Associates a drop target with this window.
    SetEventHandler 	        Sets the event handler for this window.
    SetExtraStyle 	            Sets the extra style bits for the window.
    SetFocus 	                This sets the window to receive keyboard input.
    SetFocusFromKbd 	        This function is called by wxWidgets keyboard navigation code when the user gives the focus to this window from keyboard (e.g.
    SetFont 	                Sets the font for this window.
    SetForegroundColour 	    Sets the foreground colour of the window.
    SetHelpText 	            Sets the help text to be used as context-sensitive help for this window.
    SetId 	                    Sets the identifier of the window.
    SetInitialSize 	            A smart SetSize that will fill in default size components with the window’s best size values.
    SetLabel 	                Sets the window’s label.
    SetLayoutDirection 	        Sets the layout direction for this window.
    SetMaxClientSize 	        Sets the maximum client size of the window, to indicate to the sizer layout mechanism that this is the maximum possible size of its client area.
    SetMaxSize 	                Sets the maximum size of the window, to indicate to the sizer layout mechanism that this is the maximum possible size.
    SetMinClientSize 	        Sets the minimum client size of the window, to indicate to the sizer layout mechanism that this is the minimum required size of window’s client area.
    SetMinSize 	                Sets the minimum size of the window, to indicate to the sizer layout mechanism that this is the minimum required size.
    SetName 	                Sets the window’s name.
    SetNextHandler 	            Windows cannot be used to form event handler chains; this function thus will assert when called.
    SetOwnBackgroundColour 	    Sets the background colour of the window but prevents it from being inherited by the children of this window.
    SetOwnFont 	                Sets the font of the window but prevents it from being inherited by the children of this window.
    SetOwnForegroundColour 	    Sets the foreground colour of the window but prevents it from being inherited by the children of this window.
    SetPalette 	 
    SetPosition 	            Moves the window to the specified position.
    SetPreviousHandler 	        Windows cannot be used to form event handler chains; this function thus will assert when called.
    SetRect 	 
    SetScrollPos 	            Sets the position of one of the built-in scrollbars.
    SetScrollbar 	            Sets the scrollbar properties of a built-in scrollbar.
    SetSize 	                Sets the size of the window in pixels.
    SetSizeHints 	            Use of this function for windows which are not toplevel windows (such as wx.Dialog or wx.Frame) is discouraged.
    SetSizer 	                Sets the window to have the given layout sizer.
    SetSizerAndFit 	            This method calls SetSizer and then wx.Sizer.SetSizeHints which sets the initial window size to the size needed to accommodate all sizer elements and sets the size hints which, if this window is a top level one, prevent the user from resizing it to be less than this minimal size.
    SetThemeEnabled 	        This function tells a window if it should use the system’s 'theme' code to draw the windows’ background instead of its own background drawing code.
    SetToolTip 	                Attach a tooltip to the window.
    SetTransparent 	            Set the transparency of the window.
    SetValidator 	            Deletes the current validator (if any) and sets the window validator, having called wx.Validator.Clone to create a new validator of this type.
    SetVirtualSize 	            Sets the virtual size of the window in pixels.
    SetWindowStyle 	            See SetWindowStyleFlag for more info.
    SetWindowStyleFlag      	Sets the style of the window.
    SetWindowVariant 	        Chooses a different variant of the window display to use.
    ShouldInheritColours 	    Return True from here to allow the colours of this window to be changed by InheritAttributes .
    Show 	                    Shows or hides the window.
    ShowWithEffect 	            This function shows a window, like Show , but using a special visual effect if possible.
    Thaw 	                    Re-enables window updating after a previous call to Freeze .
    ToggleWindowStyle 	        Turns the given flag on if it’s currently turned off and vice versa.
    TransferDataFromWindow 	    Transfers values from child controls to data areas specified by their validators.
    TransferDataToWindow 	    Transfers values to child controls from data areas specified by their validators.
    UnregisterHotKey 	        Unregisters a system wide hotkey.
    UnreserveControlId 	        Unreserve an ID or range of IDs that was reserved by NewControlId .
    UnsetToolTip 	            Unset any existing tooltip.
    Update 	                    Calling this method immediately repaints the invalidated area of the window and all of its children recursively (this normally only happens when the flow of control returns to the event loop).
    UpdateWindowUI 	            This function sends one or more wx.UpdateUIEvent to the window.
    UseBgCol 	                Return True if a background colour has been set for this window.
    Validate 	                Validates the current values of the child controls using their validators.
    WarpPointer 	            Moves the pointer to the given position on the window.
    WindowToClientSize 	        Converts window size size to corresponding client area size In other words, the returned value is what would GetClientSize return if this window had given window size.
    __nonzero__ 	            Can be used to test if the C++ part of the window still exists, with

    
    
wx.NonOwnedWindow
    Common base class for all non-child windows.
    #Methods Summary 
    SetShape 	    If the platform supports it, sets the shape of the window to that depicted by region.

wx.TopLevelWindow
    wx.TopLevelWindow is a common base class for wx.Dialog and wx.Frame.
    #Methods Summary
    CanSetTransparent 	    Returns True if the platform supports making the window translucent.
    CenterOnScreen 	        A synonym for CentreOnScreen .
    CentreOnScreen 	        Centres the window on screen.
    Create 	                Creates the top level window.
    EnableCloseButton 	    Enables or disables the Close button (most often in the right upper corner of a dialog) and the Close entry of the system menu (most often in the left upper corner of the dialog).
    GetDefaultItem 	        Returns a pointer to the button which is the default for this window, or
    GetDefaultSize 	        Get the default size for a new top level window.
    GetIcon 	            Returns the standard icon of the window.
    GetIcons 	            Returns all icons associated with the window, there will be none of them if neither SetIcon nor SetIcons had been called before.
    GetTitle 	            Gets a string containing the window title.
    GetTmpDefaultItem 	 
    Iconize 	            Iconizes or restores the window.
    IsActive 	            Returns True if this window is currently active, i.e. if the user is currently working with it.
    IsAlwaysMaximized 	    Returns True if this window is expected to be always maximized, either due to platform policy or due to local policy regarding particular class.
    IsFullScreen 	        Returns True if the window is in fullscreen mode.
    IsIconized 	            Returns True if the window is iconized.
    IsMaximized 	        Returns True if the window is maximized.
    Layout 	                See wx.Window.SetAutoLayout : when auto layout is on, this function gets called automatically when the window is resized.
    MacGetMetalAppearance 	 
    MacGetTopLevelWindowRef 	 
    MacGetUnifiedAppearance 	 
    MacSetMetalAppearance 	 
    Maximize 	            Maximizes or restores the window.
    OSXIsModified 	        Returns the current modified state of the wx.TopLevelWindow on OS X.
    OSXSetModified 	        This function sets the wx.TopLevelWindow‘s modified state on OS X, which currently draws a black dot in the wx.TopLevelWindow‘s close button.
    RequestUserAttention 	Use a system-dependent way to attract users attention to the window when it is in background.
    Restore 	            Restore a previously iconized or maximized window to its normal state.
    SetDefaultItem 	        Changes the default item for the panel, usually win is a button.
    SetIcon 	            Sets the icon for this window.
    SetIcons 	            Sets several icons of different sizes for this window: this allows to use different icons for different situations (e.g.
    SetMaxSize 	            A simpler interface for setting the size hints than SetSizeHints .
    SetMinSize 	            A simpler interface for setting the size hints than SetSizeHints .
    SetRepresentedFilename 	Sets the file name represented by this wx.TopLevelWindow.
    SetSizeHints 	        Allows specification of minimum and maximum window sizes, and window size increments.
    SetTitle 	            Sets the window title.
    SetTmpDefaultItem 	 
    SetTransparent 	        If the platform supports it will set the window to be translucent.
    ShouldPreventAppExit 	This virtual function is not meant to be called directly but can be overridden to return False (it returns True by default) to allow the application to close even if this, presumably not very important, window is still opened.
    ShowFullScreen 	        Depending on the value of show parameter the window is either shown full screen or restored to its normal state.
    ShowWithoutActivating 	Show the wx.TopLevelWindow, but do not give it keyboard focus.


wx.Frame(parent, id=ID_ANY, title="", pos=DefaultPosition,size=DefaultSize, 
            style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
    A wx.Frame is a top-level window. 
    #Parameters 
    parent (wx.Window) 
        The window parent. None for no parent. 
        If it is not None, the frame will be minimized when its parent is minimized 
        and restored when it is restored (although it will still be possible to minimize and restore just this frame itself).
    id (wx.WindowID) 
        The window identifier. 
        It may take a value of -1 to indicate a default value.
    title (string) 
        The caption to be displayed on the frame's title bar.
    pos (wx.Point)
        The window position. 
        The value DefaultPosition indicates a default position, 
        chosen by either the windowing system or wxWidgets, depending on platform.
    size (wx.Size)
        The window size. 
        The value DefaultSize indicates a default size, 
        chosen by either the windowing system or wxWidgets, depending on platform.
    style (long) 
        The window style. .
    name (string) 
        The name of the window. 
        This parameter is used to associate a name with the item, allowing the application user to set Motif resource values for individual windows.
    #Methods Summary
    Centre 	                Centres the frame on the display.
    Create 	                Used in two-step frame construction.
    CreateStatusBar 	    Creates a status bar at the bottom of the frame.
    CreateToolBar 	        Creates a toolbar at the top or left of the frame.
    GetClientAreaOrigin 	Returns the origin of the frame client area (in client coordinates).
    GetMenuBar 	            Returns a pointer to the menubar currently associated with the frame (if any).
    GetStatusBar 	        Returns a pointer to the status bar currently associated with the frame (if any).
    GetStatusBarPane 	    Returns the status bar pane used to display menu and toolbar help.
    GetToolBar 	            Returns a pointer to the toolbar currently associated with the frame (if any).
    OnCreateStatusBar 	    Virtual function called when a status bar is requested by CreateStatusBar .
    OnCreateToolBar 	    Virtual function called when a toolbar is requested by CreateToolBar .
    PopStatusText 	 
    ProcessCommand 	        Simulate a menu command.
    PushStatusText 	 
    SetMenuBar 	            Tells the frame to show the given menu bar.
    SetStatusBar 	        Associates a status bar with the frame.
    SetStatusBarPane 	    Set the status bar pane used to display menu and toolbar help.
    SetStatusText 	        Sets the status bar text and redraws the status bar.
    SetStatusWidths 	    Sets the widths of the fields in the status bar.
    SetToolBar 	            Associates a toolbar with the frame.

    
    
wx.Panel(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, 
            style=TAB_TRAVERSAL, name=PanelNameStr)
    A panel is a window on which controls are placed.
    It is usually placed within a frame. 
    Its main feature over its parent class wx.Window is code for handling child windows and TAB traversal. 
    #Methods Summary
    AcceptsFocus 	            This method is overridden from wx.Window.AcceptsFocus and returns True only if there is no child window in the panel which can accept the focus.
    Create      	            Used for two-step panel construction.
    InitDialog  	            Sends a wx.InitDialogEvent, which in turn transfers data to the dialog via validators.
    Layout 	                    See wx.Window.SetAutoLayout : when auto layout is on, this function gets called automatically when the window is resized.
    SetFocus 	                Overrides wx.Window.SetFocus .
    SetFocusIgnoringChildren 	In contrast to SetFocus (see above) this will set the focus to the panel even if there are child windows in the panel.

    
wx.Control
    This is the base class for a control or 'widget'
    A control is generally a small window which processes user input 
    and/or displays one or more item of data.
    #Methods Summary
    Command 	        Simulates the effect of the user issuing a command to the item.
    Create 	 
    Ellipsize 	        Replaces parts of the label string with ellipsis, if needed, so that it fits into maxWidth pixels if possible.
    EscapeMnemonics 	Escapes the special mnemonics characters ('&') in the given string.
    GetLabel 	        Returns the control’s label, as it was passed to SetLabel .
    GetLabelText 	    Returns the control’s label without mnemonics.
    GetSizeFromTextSize 	Determine the size needed by the control to leave the given area for its text.
    RemoveMnemonics 	Returns the given str string without mnemonics ('&' characters).
    SetLabel 	        Sets the control’s label.
    SetLabelMarkup 	    Sets the controls label to a string using markup.
    SetLabelText 	    Sets the control’s label to exactly the given string.


wx.AnyButton
    A class for common button functionality used as the base for the various button classes.
    #Methods Summary 	 
    GetBitmap 	        Return the bitmap shown by the button.
    GetBitmapCurrent 	Returns the bitmap used when the mouse is over the button, which may be invalid.
    GetBitmapDisabled 	Returns the bitmap for the disabled state, which may be invalid.
    GetBitmapFocus 	    Returns the bitmap for the focused state, which may be invalid.
    GetBitmapLabel 	    Returns the bitmap for the normal state.
    GetBitmapMargins 	Get the margins between the bitmap and the text of the button.
    GetBitmapPressed 	Returns the bitmap for the pressed state, which may be invalid.
    SetBitmap 	        Sets the bitmap to display in the button.
    SetBitmapCurrent 	Sets the bitmap to be shown when the mouse is over the button.
    SetBitmapDisabled 	Sets the bitmap for the disabled button appearance.
    SetBitmapFocus 	    Sets the bitmap for the button appearance when it has the keyboard focus.
    SetBitmapLabel 	    Sets the bitmap label for the button.
    SetBitmapMargins 	Set the margins between the bitmap and the text of the button.
    SetBitmapPosition 	Set the position at which the bitmap is displayed.
    SetBitmapPressed 	Sets the bitmap for the selected (depressed) button appearance.

    
    
wx.TextEntry
    Common base class for single line text entry fields.
    #Methods Summary 
    AppendText 	            Appends the text to the end of the text control.
    AutoComplete 	        Call this function to enable auto-completion of the text typed in a single-line text control using the given choices.
    AutoCompleteDirectories Call this function to enable auto-completion of the text using the file system directories.
    AutoCompleteFileNames 	Call this function to enable auto-completion of the text typed in a single-line text control using all valid file system paths.
    CanCopy 	            Returns True if the selection can be copied to the clipboard.
    CanCut 	                Returns True if the selection can be cut to the clipboard.
    CanPaste 	            Returns True if the contents of the clipboard can be pasted into the text control.
    CanRedo 	            Returns True if there is a redo facility available and the last operation can be redone.
    CanUndo 	            Returns True if there is an undo facility available and the last operation can be undone.
    ChangeValue 	        Sets the new text control value.
    Clear 	                Clears the text in the control.
    Copy 	                Copies the selected text to the clipboard.
    Cut 	                Copies the selected text to the clipboard and removes it from the control.
    GetHint 	            Returns the current hint string.
    GetInsertionPoint 	    Returns the insertion point, or cursor, position.
    GetLastPosition 	    Returns the zero based index of the last position in the text control, which is equal to the number of characters in the control.
    GetMargins 	            Returns the margins used by the control.
    GetRange 	            Returns the string containing the text starting in the positions from and up to to in the control.
    GetSelection 	        Gets the current selection span.
    GetStringSelection 	    Gets the text currently selected in the control.
    GetValue 	            Gets the contents of the control.
    IsEditable 	            Returns True if the controls contents may be edited by user (note that it always can be changed by the program).
    IsEmpty 	            Returns True if the control is currently empty.
    Paste 	                Pastes text from the clipboard to the text item.
    Redo 	                If there is a redo facility and the last operation can be redone, redoes the last operation.
    Remove 	                Removes the text starting at the first given position up to (but not including) the character at the last position.
    Replace 	            Replaces the text starting at the first position up to (but not including) the character at the last position with the given text.
    SelectAll 	            Selects all text in the control.
    SelectNone 	            Deselects selected text in the control.
    SetEditable 	        Makes the text item editable or read-only, overriding the wx.TE_READONLY flag.
    SetHint 	            Sets a hint shown in an empty unfocused text control.
    SetInsertionPoint 	    Sets the insertion point at the given position.
    SetInsertionPointEnd 	Sets the insertion point at the end of the text control.
    SetMargins 	            Attempts to set the control margins.
    SetMaxLength 	        This function sets the maximum number of characters the user can enter into the control.
    SetSelection 	        Selects the text starting at the first position up to (but not including) the character at the last position.
    SetValue 	            Sets the new text control value.
    Undo 	                If there is an undo facility and the last operation can be undone, undoes the last operation.
    WriteText 	            Writes the text into the text control at the current insertion position.

    
    
wx.Dialog
    A dialog box is a window with a title bar and sometimes a system menu, 
    which can be moved around the screen.
    #Modal and Modeless
    A modal dialog blocks program flow and user input on other windows until it is dismissed,
    whereas a modeless dialog behaves more like a frame in that program flow continues, 
    and input in other windows is still possible. 
    To show a modal dialog you should use the ShowModal method 
    while to show a dialog modelessly you simply use Show, just as with frames. 
    #Example 
    def AskUser(self):
        try:
            dlg = MyAskDialog(self)
            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print('Hello')
            else:
                # handle dialog being cancelled or ended by some other button
                ...
        finally:
            # explicitly cause the dialog to destroy itself
            dlg.Destroy()

    #OR 
    # The dialog is automatically destroyed on exit from the context manager
    def AskUser(self):
        with MyAskDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                print('Hello')
            else:
                # handle dialog being cancelled or ended by some other button       
    #Styles
        wx.CAPTION: Puts a caption on the dialog box.
        wx.DEFAULT_DIALOG_STYLE: Equivalent to a combination of wx.CAPTION, wx.CLOSE_BOX and wx.SYSTEM_MENU (the last one is not used under Unix).
        wx.RESIZE_BORDER: Display a resizable frame around the window.
        wx.SYSTEM_MENU: Display a system menu.
        wx.CLOSE_BOX: Displays a close box on the frame.
        wx.MAXIMIZE_BOX: Displays a maximize box on the dialog.
        wx.MINIMIZE_BOX: Displays a minimize box on the dialog.
        THICK_FRAME: Display a thick frame around the window.
        wx.STAY_ON_TOP: The dialog stays on top of all other windows.
        NO_3D: This style is obsolete and doesn’t do anything any more, don’t use it in any new code.
        wx.DIALOG_NO_PARENT: By default, a dialog created with a None parent window will be given the application’s top level window as parent. Use this style to prevent this from happening and create an orphan dialog. This is not recommended for modal dialogs.
        wx.DIALOG_EX_CONTEXTHELP: Under Windows, puts a query button on the caption. When pressed, Windows will go into a context-sensitive help mode and wxWidgets will send a wxEVT_HELP event if the user clicked on an application window. Note that this is an extended style and must be set by calling SetExtraStyle before Create is called (two-step construction).
        wx.DIALOG_EX_METAL: On Mac OS X, frames with this style will be shown with a metallic look. This is an extra style.
    #Events : wx.CloseEvent
        EVT_CLOSE: The dialog is being closed by the user or programmatically (see wx.Window.Close ). The user may generate this event clicking the close button (typically the ‘X’ on the top-right of the title bar) if it’s present (see the CLOSE_BOX style) or by clicking a button with the ID_CANCEL or ID_OK ids.
        EVT_INIT_DIALOG: Process a wxEVT_INIT_DIALOG event. See wx.InitDialogEvent.
    #Methods Summary
    AddMainButtonId 	        Adds an identifier to be regarded as a main button for the non-scrolling area of a dialog.
    CanDoLayoutAdaptation 	    Returns True if this dialog can and should perform layout adaptation using DoLayoutAdaptation , usually if the dialog is too large to fit on the display.
    Centre 	                    Centres the dialog box on the display.
    Create 	                    Used for two-step dialog box construction.
    CreateButtonSizer 	        Creates a sizer with standard buttons.
    CreateSeparatedButtonSizer 	Creates a sizer with standard buttons using CreateButtonSizer separated from the rest of the dialog contents by a horizontal wx.StaticLine.
    CreateSeparatedSizer 	    Returns the sizer containing the given one with a separating wx.StaticLine if necessarily.
    CreateStdDialogButtonSizer 	Creates a wx.StdDialogButtonSizer with standard buttons.
    CreateTextSizer 	        Splits text up at newlines and places the lines into wx.StaticText objects in a vertical wx.BoxSizer.
    DoLayoutAdaptation 	        Performs layout adaptation, usually if the dialog is too large to fit on the display.
    EnableLayoutAdaptation 	    A static function enabling or disabling layout adaptation for all dialogs.
    EndModal 	                Ends a modal dialog, passing a value to be returned from the ShowModal invocation.
    GetAffirmativeId 	        Gets the identifier of the button which works like standard wx.OK button in this dialog.
    GetContentWindow 	        Override this to return a window containing the main content of the dialog.
    GetEscapeId 	            Gets the identifier of the button to map presses of ESC button to.
    GetLayoutAdaptationDone 	Returns True if the dialog has been adapted, usually by making it scrollable to work with a small display.
    GetLayoutAdaptationLevel 	Gets a value representing the aggressiveness of search for buttons and sizers to be in the non-scrolling part of a layout-adapted dialog.
    GetLayoutAdaptationMode 	Gets the adaptation mode, overriding the global adaptation flag.
    GetLayoutAdapter 	        A static function getting the current layout adapter object.
    GetMainButtonIds 	        Returns an array of identifiers to be regarded as the main buttons for the non-scrolling area of a dialog.
    GetReturnCode 	            Gets the return code for this window.
    Iconize 	                Iconizes or restores the dialog.
    IsIconized 	                Returns True if the dialog box is iconized.
    IsLayoutAdaptationEnabled 	A static function returning True if layout adaptation is enabled for all dialogs.
    IsMainButtonId 	            Returns True if id is in the array of identifiers to be regarded as the main buttons for the non-scrolling area of a dialog.
    IsModal 	                Returns True if the dialog box is modal, False otherwise.
    SetAffirmativeId 	        Sets the identifier to be used as wx.OK button.
    SetEscapeId 	            Sets the identifier of the button which should work like the standard 'Cancel' button in this dialog.
    SetIcon 	                Sets the icon for this dialog.
    SetIcons 	                Sets the icons for this dialog.
    SetLayoutAdaptationDone 	Marks the dialog as having been adapted, usually by making it scrollable to work with a small display.
    SetLayoutAdaptationLevel 	Sets the aggressiveness of search for buttons and sizers to be in the non-scrolling part of a layout-adapted dialog.
    SetLayoutAdaptationMode 	Sets the adaptation mode, overriding the global adaptation flag.
    SetLayoutAdapter 	        A static function for setting the current layout adapter object, returning the old adapter.
    SetReturnCode 	            Sets the return code for this window.
    Show 	                    Hides or shows the dialog.
    ShowModal 	                Shows an application-modal dialog.
    ShowWindowModal 	        Shows a dialog modal to the parent top level window only.

 

##wxpython - Demo 
#Check demo and API at https://extras.wxpython.org/wxPython4/extras/4.01/ 

##wxpython - button Demo 

import wx
from wx.lib.embeddedimage import PyEmbeddedImage
import sys 

Mondrian = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAHFJ"
    b"REFUWIXt1jsKgDAQRdF7xY25cpcWC60kioI6Fm/ahHBCMh+BRmGMnAgEWnvPpzK8dvrFCCCA"
    b"coD8og4c5Lr6WB3Q3l1TBwLYPuF3YS1gn1HphgEEEABcKERrGy0E3B0HFJg7C1N/f/kTBBBA"
    b"+Vi+AMkgFEvBPD17AAAAAElFTkSuQmCC")


#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1,style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.log = log
        #(parent, id=ID_ANY, label="", pos=DefaultPositionsize=DefaultSize, style=0, validator=DefaultValidator,name=ButtonNameStr)
        b = wx.Button(self, 10, "Default Button", (20, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetDefault()
        b.SetSize(b.GetBestSize())
        b = wx.Button(self, 20, "HELLO AGAIN!", (20, 80))
        #type,handler, source
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTip("This is a Hello button...")
        b = wx.Button(self, 40, "Flat Button?", (20,160), style=wx.NO_BORDER)
        b.SetToolTip("This button has a style flag of wx.NO_BORDER.\n"
                           "On some platforms that will give it a flattened look.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b = wx.Button(self, 50, "wx.Button with icon", (20, 220))
        b.SetToolTip("wx.Button can how have an icon on the left, right,\n"
                           "above or below the label.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetBitmap(Mondrian.Bitmap,
                    wx.LEFT    # Left is the default, the image can be on the other sides too
                    #wx.RIGHT
                    #wx.TOP
                    #wx.BOTTOM
                    )
        b.SetBitmapMargins((2,2)) # default is 4 but that seems too big to me.
        # Setting the bitmap and margins changes the best size, so
        # reset the initial size since we're not using a sizer in this
        # example which would have taken care of this for us.
        b.SetInitialSize()
        #b = wx.Button(self, 60, "Multi-line\nbutton", (20, 280))
        #b = wx.Button(self, 70, pos=(160, 280))
        #b.SetLabel("Another\nmulti-line")
    def OnClick(self, event):
        self.log.write("Click! (%d)\n" % event.GetId())  #ID of the source 


app = wx.App(False)     # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Demo") # A Frame is a top-level window.
TestPanel(frame,sys.stderr)
frame.Show(True)        # Show the frame.
app.MainLoop()
        
        
    
##wxpython - TxtCrtl 

import  sys
import  wx

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    # def OnSetFocus(self, evt):
    #     print("OnSetFocus")
    #     evt.Skip()
    # def OnKillFocus(self, evt):
    #     print("OnKillFocus")
    #     evt.Skip()
    # def OnWindowDestroy(self, evt):
    #     print("OnWindowDestroy")
    #     evt.Skip()
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        #parent, id=ID_ANY, label="", pos=DefaultPosition,size=DefaultSize, style=0, name=StaticTextNameStr)
        l1 = wx.StaticText(self, -1, "wx.TextCtrl")
        #(parent, id=ID_ANY, value="", pos=DefaultPosition,size=DefaultSize, style=0, validator=DefaultValidator,ame=TextCtrlNameStr)
        t1 = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1))
        #callableObj, *args
        wx.CallAfter(t1.SetInsertionPoint, 0)
        self.tc1 = t1
        #type, handler, source
        self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        t1.Bind(wx.EVT_CHAR, self.EvtChar)
        # t1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        # t1.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        # t1.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)
        l2 = wx.StaticText(self, -1, "Password")
        t2 = wx.TextCtrl(self, -1, "", size=(125, -1), style=wx.TE_PASSWORD)
        self.Bind(wx.EVT_TEXT, self.EvtText, t2)
        l3 = wx.StaticText(self, -1, "Multi-line")
        t3 = wx.TextCtrl(self, -1,
                        "Here is a looooooooooooooong line of text set in the control.\n\n"
                        "The quick brown fox jumped over the lazy dog...",
                       size=(200, 100), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        t3.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT, self.EvtText, t3)
        self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, t3)
        #(parent, id=ID_ANY, label="", 
        b = wx.Button(self, -1, "Test Replace")
        self.Bind(wx.EVT_BUTTON, self.OnTestReplace, b)
        b2 = wx.Button(self, -1, "Test GetSelection")
        self.Bind(wx.EVT_BUTTON, self.OnTestGetSelection, b2)
        b3 = wx.Button(self, -1, "Test WriteText")
        self.Bind(wx.EVT_BUTTON, self.OnTestWriteText, b3)
        self.tc = t3
        l4 = wx.StaticText(self, -1, "Rich Text")
        t4 = wx.TextCtrl(self, -1, "If supported by the native control, this is red, and this is a different font.",
                        size=(200, 100), style=wx.TE_MULTILINE|wx.TE_RICH2)
        t4.SetInsertionPoint(0)
        #SetStyle:start, end, style
        #wx.TextAttr:colText, colBack=NullColour, font=NullFont,alignment=TEXT_ALIGNMENT_DEFAULT)
        t4.SetStyle(44, 47, wx.TextAttr("RED", "YELLOW"))
        points = t4.GetFont().GetPointSize()  # get the current size
        #pointSize, family, style, weight, underline=False,faceName="", encoding=FONTENCODING_DEFAULT
        f = wx.Font(points+3, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        t4.SetStyle(63, 77, wx.TextAttr("BLUE", wx.NullColour, f))
        l5 = wx.StaticText(self, -1, "Test Positions")
        t5 = wx.TextCtrl(self, -1, "0123456789\n" * 5, size=(200, 100),
                         style = wx.TE_MULTILINE
                         #| wx.TE_RICH
                         | wx.TE_RICH2
                         )
        t5.Bind(wx.EVT_LEFT_DOWN, self.OnT5LeftDown)
        self.t5 = t5
        space = 6
        #(orient)
        bsizer = wx.BoxSizer(wx.VERTICAL)
        #window, proportion=0, flag=0, border=0, userData=None
        bsizer.Add(b, 0, wx.GROW|wx.ALL, space)
        bsizer.Add(b2, 0, wx.GROW|wx.ALL, space)
        bsizer.Add(b3, 0, wx.GROW|wx.ALL, space)
        #cols, vgap, hgap
        sizer = wx.FlexGridSizer(cols=3, hgap=space, vgap=space)
        #list of tuples, each tuple is arg of .Add()
        #here we are using two overloaded args of .Add()
        #l1,t1,... : (window, flags) , Appends window to Sizer 
        #(0,0) : (size,flags) , Appends a spacer 
        #bsizer : (sizer,flags) : Appends a wx.Sizer instance 
        sizer.AddMany([ l1, t1, (0,0),
                        l2, t2, (0,0),
                        l3, t3, bsizer,
                        l4, t4, (0,0),
                        l5, t5, (0,0),
                        ])
        border = wx.BoxSizer(wx.VERTICAL)
        ##window, proportion=0, flag=0, border=0, userData=None
        border.Add(sizer, 0, wx.ALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)
    def EvtText(self, event):
        self.log.WriteText('EvtText: %s\n' % event.GetString())
    def EvtTextEnter(self, event):
        self.log.WriteText('EvtTextEnter\n')
        event.Skip()
    def EvtChar(self, event):
        self.log.WriteText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def OnTestReplace(self, evt):
        self.tc.Replace(5, 9, "IS A")
        #self.tc.Remove(5, 9)
    def OnTestWriteText(self, evt):
        self.tc.WriteText("TEXT")
    def OnTestGetSelection(self, evt):
        start, end = self.tc.GetSelection()
        text = self.tc.GetValue()
        if wx.Platform == "__WXMSW__":  # This is why GetStringSelection was added
            text = text.replace('\n', '\r\n')
        self.log.write("multi-line GetSelection(): (%d, %d)\n"
                       "\tGetStringSelection(): %s\n"
                       "\tSelectedText: %s\n" %
                       (start, end,
                        self.tc.GetStringSelection(),
                        repr(text[start:end])))
        start, end = self.tc1.GetSelection()
        text = self.tc1.GetValue()
        if wx.Platform == "__WXMSW__":  # This is why GetStringSelection was added
            text = text.replace('\n', '\r\n')
        self.log.write("single-line GetSelection(): (%d, %d)\n"
                       "\tGetStringSelection(): %s\n"
                       "\tSelectedText: %s\n" %
                       (start, end,
                        self.tc1.GetStringSelection(),
                        repr(text[start:end])))
    def OnT5LeftDown(self, evt):
        evt.Skip()
        wx.CallAfter(self.LogT5Position, evt)
    def LogT5Position(self, evt):
        text = self.t5.GetValue()
        ip = self.t5.GetInsertionPoint()
        lp = self.t5.GetLastPosition()
        try:
            self.log.write("LogT5Position:\n"
                           "\tGetInsertionPoint:\t%d\n"
                           "\ttext[insertionpoint]:\t%s\n"
                           "\tGetLastPosition:\t%d\n"
                           "\tlen(text):\t\t%d\n"
                           % (ip, text[ip], lp, len(text)))
        except Exception as exc:#last position eol or eof
            # print('Exception', exc)
            self.log.write("LogT5Position:\n"
                           "\tGetInsertionPoint:\t%d\n"
                           "\tGetLastPosition:\t%d\n"
                           "\tlen(text):\t\t%d\n"
                           % (ip, lp, len(text)))



app = wx.App(False)     # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Demo") # A Frame is a top-level window.
TestPanel(frame,sys.stderr)
frame.Show(True)        # Show the frame.
app.MainLoop()
                           
                    
##wxpython - ScrolledWindow and onPaint 

import wx
import images

# There are two different approaches to drawing, buffered or direct.
# This sample shows both approaches so you can easily compare and
# contrast the two by changing this value.
BUFFERED = 1

'''
Scrolling:
OPT-1: set the scrollbars directly using a call to SetScrollbars (old style)
OPT-2: set the total size of the scrolling area by calling either 
       wx.Window.SetVirtualSize , or wx.Window.FitInside , 
       and setting the scrolling increments by SetScrollRate. 
       Scrolling in some orientation is enabled by setting a non-zero increment for it.
OPT-2: automatic way : Use sizers todetermine the scrolling area. 
       by calling wx.Window.SetSizer . 
       The scrolling area will be set to the size requested by the sizer 
       and the scrollbars will be assigned for each orientation according to the need for them 
       and the scrolling increment set by SetScrollRate. 

An application can draw onto a wx.Scrolled using a device context.
Handle OnPaint handler or overriding the wx.Scrolled.OnDraw function, 
which is passed a pre-scrolled device context (prepared by wx.Scrolled.DoPrepareDC ).

If you don’t wish to calculate your own scrolling, 
you must call DoPrepareDC when not drawing from within OnDraw, 
to set the device origin for the device context according to the current scroll position.

'''

#---------------------------------------------------------------------------

class MyCanvas(wx.ScrolledWindow):  #(<class 'wx._core.ScrolledWindow'>, <class 'wx._core._ScrolledWindowBase'>, <class 'wx._core.Window'>, <class 'wx._core.WindowBase'>, <class 'wx._core.EvtHandler',...)
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        #parent, winid=ID_ANY, pos=DefaultPosition,size=DefaultSize, style=ScrolledWindowStyle, name=PanelNameStr)
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        self.lines = []
        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False
        #color 
        self.SetBackgroundColour("WHITE")
        #wx.Cursor(cursorName, type=BITMAP_TYPE_ANY, hotSpotX=0, hotSpotY=0)
        #wx.Cursor(cursorId)
        self.SetCursor(wx.Cursor(wx.CURSOR_PENCIL))
        #from demo\images.py
        bmp = images.Test2.GetBitmap()
        #wx.Mask(bitmap, colour), wx.BLUE=wx.Colour(0, 0, 255, 255)
        #When associated with a bitmap and drawn in a device context, the unmasked area of the bitmap will be drawn, 
        #and the masked area will not be drawn.
        mask = wx.Mask(bmp, wx.BLUE)
        bmp.SetMask(mask)
        self.bmp = bmp
        #(width, height) or size 
        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        #(xstep, ystep)
        self.SetScrollRate(20,20)

        if BUFFERED:
            # Initialize the buffer bitmap.  No real DC is needed at this point.
            self.buffer = wx.Bitmap(self.maxWidth, self.maxHeight)
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour())) #A brush is a drawing tool for filling in areas.
            dc.Clear()
            self.DoDrawing(dc)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_LEFT_UP,   self.OnLeftButtonEvent)
        self.Bind(wx.EVT_MOTION,    self.OnLeftButtonEvent)
        self.Bind(wx.EVT_PAINT,     self.OnPaint)


    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight

    #Handle Paint event 
    def OnPaint(self, event):
        if BUFFERED:
            # Create a buffered paint DC.  It will create the real
            # wx.PaintDC and then blit the bitmap to it when dc is
            # deleted.  Since we don't need to draw anything else
            # here that's all there is to it.
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        else:
            dc = wx.PaintDC(self)
            self.PrepareDC(dc)
            # Since we're not buffering in this case, we have to
            # (re)paint the all the contents of the window, which can
            # be potentially time consuming and flickery depending on
            # what is being drawn and how much of it there is.
            self.DoDrawing(dc)


    def DoDrawing(self, dc, printing=False):
        dc.SetPen(wx.Pen('RED'))
        dc.DrawRectangle(5, 5, 50, 50)

        dc.SetBrush(wx.LIGHT_GREY_BRUSH)
        dc.SetPen(wx.Pen('BLUE', 4))
        dc.DrawRectangle(15, 15, 50, 50)

        dc.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        dc.SetTextForeground(wx.Colour(0xFF, 0x20, 0xFF))
        te = dc.GetTextExtent("Hello World")
        dc.DrawText("Hello World", 60, 65)

        dc.SetPen(wx.Pen('VIOLET', 4))
        dc.DrawLine(5, 65+te[1], 60+te[0], 65+te[1])

        lst = [(100,110), (150,110), (150,160), (100,160)]
        dc.DrawLines(lst, -60)
        dc.SetPen(wx.GREY_PEN)
        dc.DrawPolygon(lst, 75)
        dc.SetPen(wx.GREEN_PEN)
        dc.DrawSpline(lst+[(100,100)])

        dc.DrawBitmap(self.bmp, 200, 20, True)
        dc.SetTextForeground(wx.Colour(0, 0xFF, 0x80))
        dc.DrawText("a bitmap", 200, 85)

        font = wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        dc.SetTextForeground(wx.BLACK)

        for a in range(0, 360, 45):
            dc.DrawRotatedText("Rotated text...", 300, 300, a)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.BLUE_BRUSH)
        dc.DrawRectangle(50,500, 50,50)
        dc.DrawRectangle(100,500, 50,50)

        dc.SetPen(wx.Pen('RED'))
        dc.DrawEllipticArc(200,500, 50,75, 0, 90)

        if not printing:
            # This has troubles when used on a print preview in wxGTK,
            # probably something to do with the pen styles and the scaling
            # it does...
            y = 20

            for style in [wx.PENSTYLE_DOT, wx.PENSTYLE_LONG_DASH,
                          wx.PENSTYLE_SHORT_DASH, wx.PENSTYLE_DOT_DASH,
                          wx.PENSTYLE_USER_DASH]:
                pen = wx.Pen("DARK ORCHID", 1, style)
                if style == wx.PENSTYLE_USER_DASH:
                    pen.SetCap(wx.CAP_BUTT)
                    pen.SetDashes([1,2])
                    pen.SetColour("RED")
                dc.SetPen(pen)
                dc.DrawLine(300,y, 400,y)
                y = y + 10

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(wx.Colour(0xFF, 0x20, 0xFF), 1, wx.PENSTYLE_SOLID))
        dc.DrawRectangle(450,50,  100,100)
        old_pen = dc.GetPen()
        new_pen = wx.Pen("BLACK", 5)
        dc.SetPen(new_pen)
        dc.DrawRectangle(470,70,  60,60)
        dc.SetPen(old_pen)
        dc.DrawRectangle(490,90, 20,20)

        dc.GradientFillLinear((20, 260, 50, 50),
                              "red", "blue")
        dc.GradientFillConcentric((20, 325, 50, 50),
                                  "red", "blue", (25,25))
        self.DrawSavedLines(dc)

    def DrawSavedLines(self, dc):
        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
        for line in self.lines:
            for coords in line:
                dc.DrawLine(*coords)


    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def OnLeftButtonEvent(self, event):
        if self.IsAutoScrolling():
            self.StopAutoScrolling()

        if event.LeftDown():
            self.SetFocus()
            self.SetXY(event)
            self.curLine = []
            self.CaptureMouse()
            self.drawing = True

        elif event.Dragging() and self.drawing:
            if BUFFERED:
                # If doing buffered drawing we'll just update the
                # buffer here and then refresh that portion of the
                # window.  Then the system will send an event and that
                # portion of the buffer will be redrawn in the
                # EVT_PAINT handler.
                dc = wx.BufferedDC(None, self.buffer)
            else:
                # otherwise we'll draw directly to a wx.ClientDC
                dc = wx.ClientDC(self)
                self.PrepareDC(dc)

            dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
            coords = (self.x, self.y) + self.ConvertEventCoords(event)
            self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.SetXY(event)

            if BUFFERED:
                # figure out what part of the window to refresh, based
                # on what parts of the buffer we just updated
                x1,y1, x2,y2 = dc.GetBoundingBox()
                x1,y1 = self.CalcScrolledPosition(x1, y1)
                x2,y2 = self.CalcScrolledPosition(x2, y2)
                # make a rectangle
                rect = wx.Rect()
                rect.SetTopLeft((x1,y1))
                rect.SetBottomRight((x2,y2))
                rect.Inflate(2,2)
                # refresh it
                self.RefreshRect(rect)

        elif event.LeftUp() and self.drawing:
            self.lines.append(self.curLine)
            self.curLine = []
            self.ReleaseMouse()
            self.drawing = False


## This is an example of what to do for the EVT_MOUSEWHEEL event,
## but since wx.ScrolledWindow does this already it's not
## necessary to do it ourselves. You would need to add an event table
## entry to __init__() to direct wheelmouse events to this handler.

##     wheelScroll = 0
##     def OnWheel(self, evt):
##         delta = evt.GetWheelDelta()
##         rot = evt.GetWheelRotation()
##         linesPer = evt.GetLinesPerAction()
##         print(delta, rot, linesPer)
##         ws = self.wheelScroll
##         ws = ws + rot
##         lines = ws / delta
##         ws = ws - lines * delta
##         self.wheelScroll = ws
##         if lines != 0:
##             lines = lines * linesPer
##             vsx, vsy = self.GetViewStart()
##             scrollTo = vsy - lines
##             self.Scroll(-1, scrollTo)


    
    
##wxpython - inspection tool 
#add an inspection tool to an  application (probably in a Menu handler or before call to MainLoop )
#In the interpreter the name 'obj' will always refer to the item currently selected in the tree, 
 
import wx.lib.inspection
wx.lib.inspection.InspectionTool().Show()

#OR activate via a hot-key(default Ctrl-Alt-I, or Cmd-Alt-I on Mac)
#and it will also preselect the item under the mouse cursor when the tool is shown. 

import wx
import wx.lib.mixins.inspection

class MyFrame(wx.Frame):
    pass
 
class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin): #use Mixin
    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame = MyFrame(None, title="This is a test")
        frame.Show()
        self.SetTopWindow(frame)
        return True

app = MyApp()
app.MainLoop()




##wxpython - Events and Event Handling

#Important functions 
#Any control, frame, panel etc are derived from wx.EvtHandler
wx.EvtHandler.Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY)
    Bind an event to an event handler.
        event – One of the EVT_ event binder objects that specifies the type of event to bind.
        handler – A callable object to be invoked when the event is delivered to self. Pass None to disconnect an event handler.
        source – Sometimes the event originates from a different window than self, but you still want to catch it in self. (For example, a button event delivered to a frame.) By passing the source of the event, the event handling system is able to differentiate between the same event type from different controls.
        id – Used to spcify the event source by ID instead of instance.
        id2 – Used when it is desirable to bind a handler to a range of IDs, such as with EVT_MENU_RANGE.

wx.PostEvent(dest, event)
    In a GUI application, this function posts event to the specified dest object 
    using wx.EvtHandler.AddPendingEvent .
    Otherwise, it dispatches event immediately using wx.EvtHandler.ProcessEvent . 
    Mut be used inside thread 
        dest (wx.EvtHandler) – window where to post 
        event (wx.Event) –

wx.EvtHandler.Unbind(self, event, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, handler=None)
    Disconnects the event handler binding for event from self. Returns True if successful.

    
##Two ways to bind 
#Note multiple handler can be attached to same event 
#by calling Bind with same event, but different handler (only first handler must call .Skip())
#handler take Event instance as it's arg, to get ID of originating window, use Event.getId()
#OPT-1: self is a wx.Frame or another container control:
    self.Bind(wx.EVT_BUTTON, self.OnButton, self.button)
#OPT-2: 
    self.button.Bind(wx.EVT_BUTTON, self.OnButton)
    
##Types of Events
wx.CommandEvent  
    wxPython will search up the containment hierarchy (parent windows) 
    First handler would stop this search by default 
    or use Event.Skip()(a defered call) inside handler to continue  propagation or process other bound events
    or use Event.Veto() to explicitely stop searching 
    Can use both form of binding, but Note if multiple handlers are bound at container and control 
    then container event handler would be called last (if controller event handler calls .Skip())
    or not at all (if no .Skip() call at controller)
other events, derived from wx.Event 
    Only originating Control(no propagation)
    Hence use only below form 
        self.control.Bind(wx.EVT_BUTTON, self.OnButton)

        
##Event - How Events are Processed
#When an event is received from the windowing system, 
#wxPython calls wx.EvtHandler.ProcessEvent on the first event handler object belonging to the window generating the event. 
#The normal order of event table searching by ProcessEvent is as follows, 
0.with the event processing stopping as soon as a handler is found 
 (unless the handler calls wx.Event.Skip() in which case it doesn’t count as having handled the event and the search continues):
1.Before anything else happens, wx.AppConsole.FilterEvent is called. 
  If it returns anything but -1 (default), the event handling stops immediately.
2.If this event handler is disabled via a call to wx.EvtHandler.SetEvtHandlerEnabled 
  the next three steps are skipped and the event handler resumes at step (6).
3.If the object is a wx.Window and has an associated validator, 
   wx.Validator gets a chance to process the event.
4.The list of dynamically bound event handlers, 
  i.e., those for which Bind() was called, is consulted.
  The event table containing all the handlers defined 
  using the same event type in this class and its base classes is examined(not same as parent Window) 
  Notice that this means that any event handler defined in a base class will be executed at this step.
5.The event is passed to the next event handler, if any, 
  in the event handler chain of same Window, i.e., the steps (3) to (4) are done for it. 
  Usually there is no next event handler so the control passes to the next step 
  This chain can be formed using wx.EvtHandler.SetNextHandler
  Additionally, in the case of wx.Window you can build a stack 
  (implemented using wx.EvtHandler double-linked list) using wx.Window.PushEventHandler
6.If the object is a wx.Window and the event is set to propagate 
  (by default only event types derived from wx.CommandEvent are set to propagate), 
  then the processing restarts from the step (2) 
  (and excluding the step (6)) for the parent window. 
  the event eventually reaches the window parent.
8.Finally, i.e., if the event is still not processed, the wx.App object itself 
 (which derives from wx.EvtHandler) gets a last chance to process it.

##Event - How Events Propagate Upwards
1.the events of the classes deriving from wx.CommandEvent are propagated 
  by default to the parent window if they are not processed in this window itself. 
2.other events can be propagated as well because the event handling code 
  uses wx.Event.ShouldPropagate to check whether an event should be propagated
3.when propagating the command events up to the parent window, 
  the event propagation stops when it reaches the parent dialog   
  OR unset wx.WS_EX_BLOCK_EVENTS flag for the dialogs to propagate beyond parent dialog 
4.The events do propagate beyond the wx.Frame 
  or use  wx.Window.SetExtraStyle (wx.WS_EX_BLOCK_EVENTS) explicitly 
  to prevent the events from being propagated beyond the given window
  
   
 
##Vetoing events: to stop processing an event
# -*- coding: utf-8 -*-

import wx

class Example(wx.Frame):           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()
                
    def InitUI(self):
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.SetTitle('Event veto')
        self.Centre()
        self.Show(True)

    def OnCloseWindow(self, e):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)            
        ret = dial.ShowModal()        
        if ret == wx.ID_YES:
            self.Destroy()  #close all windows , don't call .Close()
        else:
            e.Veto()

def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()  

##Event propagation
#For example wx.CloseEvent is a basic event(does not propagate)
#wx.EVT_BUTTON is command event (propagate)
#By default, the event that is caught in a event handler stops propagating. 
#To continue propagation, we must call the Skip() method.


# -*- coding: utf-8 -*-


import wx

class MyPanel(wx.Panel):    
    def __init__(self, *args, **kw):
        super(MyPanel, self).__init__(*args, **kw) 
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
    def OnButtonClicked(self, e):        
        print('event reached panel class', e.GetId())
        e.Skip()


class MyButton(wx.Button):    
    def __init__(self, *args, **kw):
        super(MyButton, self).__init__(*args, **kw) 
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
    def OnButtonClicked(self, e):        
        print('event reached button class', e.GetId())
        e.Skip()
        

class Example(wx.Frame):           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()         
    def InitUI(self):
        mpnl = MyPanel(self)
        MyButton(mpnl, label='Ok', pos=(15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.SetTitle('Propagate event')
        self.Centre()
        self.Show(True)  
    def OnButtonClicked(self, e):        
        print('event reached frame class', e.GetId())
        e.Skip()


def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()  

#output 
event reached button class
event reached panel class
event reached frame class


##Window identifiers
#Each widget has an id parameter. 
#This is a unique number in the event system.
#There are three ways to create window id's.
1.let the system automatically create an id , use wx.Button(parent, -1) or wx.Button(parent, wx.ID_ANY)
  Get that id by control.GetId()
  During event binding, one can pass id instead of control instance eg 
  (self is wx.TopLevelWindow ie wx.Frame etc)
  self.Bind(wx.EVT_BUTTON,  self.OnExit, id=exitButton.GetId())
2. use standard identifiers, check https://docs.wxpython.org/stock_items.html
3. create your own id, wx.NewId()

#Example of standard identifiers
# -*- coding: utf-8 -*-


import wx

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()
                
    def InitUI(self):
        pnl = wx.Panel(self)
        grid = wx.GridSizer(3, 2)
        #list of tuple, each tuple contains args as passed in .Add(window, proportion=0, flag=0, border=0, userData=None))
        grid.AddMany([(wx.Button(pnl, wx.ID_CANCEL), 0, wx.TOP | wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_DELETE), 0, wx.TOP, 9),
            (wx.Button(pnl, wx.ID_SAVE), 0, wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_EXIT)),
            (wx.Button(pnl, wx.ID_STOP), 0, wx.LEFT, 9),
            (wx.Button(pnl, wx.ID_NEW))])
        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)
        pnl.SetSizer(grid)
        self.SetSize((220, 180))
        self.SetTitle("Standard ids")
        self.Centre()
        self.Show(True)
    def OnQuitApp(self, event):        
        self.Close()

def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()  

#Example of using new global ids.

# -*- coding: utf-8 -*-

import wx

ID_MENU_NEW = wx.NewId()
ID_MENU_OPEN = wx.NewId()
ID_MENU_SAVE = wx.NewId()

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)        
        self.InitUI()
                
    def InitUI(self):        
        self.CreateMenuBar()
        self.CreateStatusBar()        
        self.SetSize((250, 180))
        self.SetTitle('Global ids')
        self.Centre()
        self.Show(True)  
        
    def CreateMenuBar(self):        
        mb = wx.MenuBar()        
        fMenu = wx.Menu()
        fMenu.Append(ID_MENU_NEW, 'New')
        fMenu.Append(ID_MENU_OPEN, 'Open')
        fMenu.Append(ID_MENU_SAVE, 'Save')        
        mb.Append(fMenu, '&File')
        self.SetMenuBar(mb)        
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_NEW)
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_OPEN)
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_SAVE)        
        
    def DisplayMessage(self, e):        
        sb = self.GetStatusBar()                
        eid = e.GetId()        
        if eid == ID_MENU_NEW:
            msg = 'New menu item selected'
        elif eid == ID_MENU_OPEN:
            msg = 'Open menu item selected'
        elif eid == ID_MENU_SAVE:
            msg = 'Save menu item selected'        
        sb.SetStatusText(msg)

def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()  


##wx.PaintEvent(wx.EVT_PAINT)(not a command Event, hence handle only at TopLevelWindow)
#A paint event is generated when a window is redrawn. 
#This happens when we resize a window or when we maximize it. 
#A paint event can be generated programatically as well. 
#For example, when we call SetLabel() method to change a wx.StaticText widget. 
#Note that when we minimize a window, no paint event is generated.

#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx

class Example(wx.Frame):           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()                
    def InitUI(self):
        self.count = 0
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetSize((250, 180))
        self.Centre()
        self.Show(True)  
    def OnPaint(self, e):     
        dc = wx.PaintDC(self)
        #DrawMyDocument(dc)  #if required #dc contain many drawing functions
        self.count += 1
        self.SetTitle(str(self.count))
        
def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()  

##wx.FocusEvent(EVT_SET_FOCUS,EVT_KILL_FOCUS)(not a command Event, hence handle only at originating window)
#The window losing focus receives a 'kill focus' event while the window gaining it gets a 'set focus' one.
#set focus event happens both when the user gives focus to the window (whether using the mouse or keyboard) 
#and when it is done from the program itself using wx.Window.SetFocus .
#The focus event handlers should almost invariably call wx.Event.Skip on their event argument to allow the default handling to take plac

import wx

class MyWindow(wx.Panel):    
    def __init__(self, parent):
        super(MyWindow, self).__init__(parent)
        self.color = '#b3b3b3'
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
    def OnPaint(self, e):        
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(self.color))
        x, y = self.GetSize()
        dc.DrawRectangle(0, 0, x, y)
    def OnSize(self, e):        
        self.Refresh()
    def OnSetFocus(self, e):        
        self.color = '#0099f7'
        self.Refresh()
    def OnKillFocus(self, e):        
        self.color = '#b3b3b3'
        self.Refresh()

class Example(wx.Frame):           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()         
    def InitUI(self):
        grid = wx.GridSizer(2, 2, 10, 10)
        #list of tuple, each tuple contains args as passed in .Add(window, proportion=0, flag=0, border=0, userData=None))
        grid.AddMany([(MyWindow(self), 0, wx.EXPAND|wx.TOP|wx.LEFT, 9),
            (MyWindow(self), 0, wx.EXPAND|wx.TOP|wx.RIGHT, 9), 
            (MyWindow(self), 0, wx.EXPAND|wx.BOTTOM|wx.LEFT, 9), 
            (MyWindow(self), 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 9)])
        self.SetSizer(grid)
        self.SetSize((350, 250))
        self.SetTitle('Focus event')
        self.Centre()
        self.Show(True) 
    def OnMove(self, e):        
        print(e.GetEventObject())
        x, y = e.GetPosition()
        self.st1.SetLabel(str(x))
        self.st2.SetLabel(str(y))


def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()  



##wx.KeyEvent - event types(not a command Event, hence handle only at originating window)
EVT_KEY_DOWN
    Process a wxEVT_KEY_DOWN event (any key has been pressed). 
    If this event is handled and not skipped, wxEVT_CHAR will not be generated at all for this key press (but wxEVT_KEY_UP will be).
EVT_KEY_UP
    Process a wxEVT_KEY_UP event (any key has been released).
EVT_CHAR
    Process a wxEVT_CHAR event.

##wx.KeyEvent - extra members 
#Use Get*/Set* methods 
KeyCode 	
    Returns the key code of the key that generated this event.
    ASCII symbols return normal ASCII values, 
    while events from special keys such as 'left cursor arrow' ( WXK_LEFT ) 
    return values outside of the ASCII range. 
    check https://wxpython.org/Phoenix/docs/html/wx.KeyCode.enumeration.html
    for a full list of the virtual key codes.
    Note that this method returns a meaningful value only for special non-alphanumeric keys 
    or if the user entered a Latin-1 character (this includes ASCII and the accented letters found in Western European languages but not letters of other alphabets such as e.g. Cyrillic). 
    Otherwise it simply method returns WXK_NONE 
    and GetUnicodeKey should be used to obtain the corresponding Unicode character.
Position 
    Obtains the position (in client coordinates) at which the key was pressed.
    Notice that under most platforms this position is simply the current mouse pointer position 
    and has no special relationship to the key event itself.
    x and y may be None if the corresponding coordinate is not needed.	
RawKeyCode 	
    Returns the raw key code for this event.
RawKeyFlags 	
    Returns the low level key flags for this event.
UnicodeKey 	
    Returns the Unicode character corresponding to this key event.
    If the key pressed doesn’t have any character value (e.g. a cursor key) 
    this method will return WXK_NONE , then use GetKeyCode to retrieve the value of the key.
X 	
    Returns the X position (in client coordinates) of the event.
Y 	
    Returns the Y position (in client coordinates) of the event.

#Example handler 
def OnChar(self, event):
    keycode = event.GetUnicodeKey()
    if keycode != wx.WXK_NONE:
        # It's a printable character
        wx.LogMessage("You pressed '%c'"%keycode)
    else:
        # It's a special key, deal with all the known ones:
        if keycode in [wx.WXK_LEFT, wx.WXK_RIGHT]:
            # move cursor ...
            MoveCursor()
        elif keycode == wx.WXK_F1:
            # give help ...
            GiveHelp()

  
#Example - A common request is to close application, when the Esc key is pressed.


import wx

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)         
        self.InitUI()
                
    def InitUI(self):
        pnl = wx.Panel(self)
        pnl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        pnl.SetFocus()
        self.SetSize((250, 180))
        self.SetTitle('Key event')
        self.Centre()
        self.Show(True)  

    def OnKeyDown(self, e):        
        key = e.GetKeyCode()        
        if key == wx.WXK_ESCAPE:            
            ret  = wx.MessageBox('Are you sure to quit?', 'Question', 
                wx.YES_NO | wx.NO_DEFAULT, self)                
            if ret == wx.YES:
                self.Close()               
        
def main():    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    






##wx.Event - members  
#use Get*/Set* methods    
EventObject 
    Returns the object (usually a window) associated with the event(event source)
EventType 	
    uniquely identifies the type of the event, wx.EVT_* 
Id 	    
    Orignating window's Id 
Skipped 	
Timestamp 
    Originating timeStamp
        
##wx.Event - Event Subclasses 
wx.ActivateEvent
wx.CloseEvent
wx.DisplayChangedEvent
wx.DropFilesEvent
wx.EraseEvent
wx.FileSystemWatcherEvent
wx.FocusEvent
wx.IconizeEvent
wx.IdleEvent
wx.InitDialogEvent
wx.JoystickEvent
wx.KeyEvent
wx.MaximizeEvent
wx.MenuEvent
wx.MouseCaptureChangedEvent
wx.MouseCaptureLostEvent
wx.MouseEvent
wx.MoveEvent
wx.NavigationKeyEvent
wx.PaintEvent
wx.PaletteChangedEvent
wx.PowerEvent
wx.ProcessEvent
wx.QueryNewPaletteEvent
wx.ScrollWinEvent
wx.SetCursorEvent
wx.ShowEvent
wx.SizeEvent
wx.SysColourChangedEvent
wx.TimerEvent
wx.CommandEvent(mainly Control's event types)
    wx.ChildFocusEvent
    wx.ClipboardTextEvent
    wx.CollapsiblePaneEvent
    wx.ColourPickerEvent
    wx.ContextMenuEvent
    wx.FileCtrlEvent
    wx.FileDirPickerEvent
    wx.FindDialogEvent
    wx.FontPickerEvent
    wx.HelpEvent
    wx.NotifyEvent
    wx.ScrollEvent
    wx.TextUrlEvent
    wx.UpdateUIEvent
    wx.WindowCreateEvent
    wx.WindowDestroyEvent
    wx.WindowModalDialogEvent


##wx.CommandEvent - extra members 
#use Get*/Set* methods   
ClientData 
    Returns client object pointer for a listbox or choice selection event 
    (not valid for a deselection).
ExtraLong 	
    Returns extra information dependent on the event objects type.
    If the event comes from a listbox selection, 
    it is a boolean determining whether the event was a selection (True) 
    or a deselection (False). 
Int 
    Returns the integer identifier corresponding to a listbox, choice or radiobox selection 
    (only if the event was a selection, not a deselection), 
    or a boolean value representing the value of a checkbox.
    For a menu item, this method returns -1 if the item is not checkable 
    or a boolean value (True or False) for checkable items indicating the new state of the item.
Selection 	
    Returns item index for a listbox or choice selection event (not valid for a deselection).
String 	
    Returns item string for a listbox or choice selection event.
    If one or several items have been deselected, 
    returns the index of the first deselected item.
    If some items have been selected and others deselected at the same time, 
    it will return the index of the first selected item.
    
##wx.CommandEvent - Other methods 
IsChecked(self)
    This method can be used with checkbox and menu events: 
    for the checkboxes, the method returns True for a selection event 
    and False for a deselection one.
    For the menu events, this method indicates if the menu item just has become checked or unchecked 
    (and thus only makes sense for checkable menu items).
    Notice that this method cannot be used with wx.CheckListBox currently.

    
##wx.CommandEvent - event types will receive a wx.CommandEvent parameter
#(mainly Control's event types)
EVT_COMMAND
	Process a command, supplying the window identifier, command event identifier, and member function.
EVT_COMMAND_RANGE
	Process a command for a range of window identifiers, supplying the minimum and maximum window identifiers, command event identifier, and member function.
EVT_BUTTON
	Process a wxEVT_BUTTON command, which is generated by a wx.Button control.
EVT_CHECKBOX
	Process a wxEVT_CHECKBOX command, which is generated by a wx.CheckBox control.
EVT_CHOICE
	Process a wxEVT_CHOICE command, which is generated by a wx.Choice control.
EVT_COMBOBOX
	Process a wxEVT_COMBOBOX command, which is generated by a wx.ComboBox control.
EVT_LISTBOX
	Process a wxEVT_LISTBOX command, which is generated by a wx.ListBox control.
EVT_LISTBOX_DCLICK
	Process a wxEVT_LISTBOX_DCLICK command, which is generated by a wx.ListBox control.
EVT_CHECKLISTBOX
	Process a wxEVT_CHECKLISTBOX command, which is generated by a wx.CheckListBox control.
EVT_MENU
	Process a wxEVT_MENU command, which is generated by a menu item.
EVT_MENU_RANGE
	Process a wxEVT_MENU command, which is generated by a range of menu items.
EVT_CONTEXT_MENU
	Process the event generated when the user has requested a popup menu to appear by pressing a special keyboard key (under Windows) or by right clicking the mouse.
EVT_RADIOBOX
	Process a wxEVT_RADIOBOX command, which is generated by a wx.RadioBox control.
EVT_RADIOBUTTON
	Process a wxEVT_RADIOBUTTON command, which is generated by a wx.RadioButton control.
EVT_SCROLLBAR
	Process a wxEVT_SCROLLBAR command, which is generated by a wx.ScrollBar control. This is provided for compatibility only; more specific scrollbar event macros should be used instead (see wx.ScrollEvent).
EVT_SLIDER
	Process a wxEVT_SLIDER command, which is generated by a wx.Slider control.
EVT_TEXT
	Process a wxEVT_TEXT command, which is generated by a wx.TextCtrl control.
EVT_TEXT_ENTER
	Process a wxEVT_TEXT_ENTER command, which is generated by a wx.TextCtrl control. Note that you must use wx.TE_PROCESS_ENTER flag when creating the control if you want it to generate such events.
EVT_TEXT_MAXLEN
	Process a wxEVT_TEXT_MAXLEN command, which is generated by a wx.TextCtrl control when the user tries to enter more characters into it than the limit previously set with SetMaxLength().
EVT_TOGGLEBUTTON
	Process a wxEVT_TOGGLEBUTTON event.
EVT_TOOL
	Process a wxEVT_TOOL event (a synonym for wxEVT_MENU ). Pass the id of the tool.
EVT_TOOL_RANGE
	Process a wxEVT_TOOL event for a range of identifiers. Pass the ids of the tools.
EVT_TOOL_RCLICKED
	Process a wxEVT_TOOL_RCLICKED event. Pass the id of the tool. (Not available on wxOSX.)
EVT_TOOL_RCLICKED_RANGE
	Process a wxEVT_TOOL_RCLICKED event for a range of ids. Pass the ids of the tools. (Not available on wxOSX.)
EVT_TOOL_ENTER
	Process a wxEVT_TOOL_ENTER event. Pass the id of the toolbar itself. The value of wx.CommandEvent.GetSelection is the tool id, or -1 if the mouse cursor has moved off a tool. (Not available on wxOSX.)
EVT_COMMAND_LEFT_CLICK
	Process a wxEVT_COMMAND_LEFT_CLICK command, which is generated by a control (wxMSW only).
EVT_COMMAND_LEFT_DCLICK
	Process a wxEVT_COMMAND_LEFT_DCLICK command, which is generated by a control (wxMSW only).
EVT_COMMAND_RIGHT_CLICK
	Process a wxEVT_COMMAND_RIGHT_CLICK command, which is generated by a control (wxMSW only).
EVT_COMMAND_SET_FOCUS
	Process a wxEVT_COMMAND_SET_FOCUS command, which is generated by a control (wxMSW only).
EVT_COMMAND_KILL_FOCUS
	Process a wxEVT_COMMAND_KILL_FOCUS command, which is generated by a control (wxMSW only).
EVT_COMMAND_ENTER
	Process a wxEVT_COMMAND_ENTER command, which is generated by a control.

    
          
##wx.MouseEvent - event types 
EVT_LEFT_DOWN
	Process a wxEVT_LEFT_DOWN event. 
    The handler of this event should normally call event.Skip() 
    to allow the default processing to take place as otherwise the window under mouse wouldn’t get the focus.
EVT_LEFT_UP
	Process a wxEVT_LEFT_UP event.
EVT_LEFT_DCLICK
	Process a wxEVT_LEFT_DCLICK event.
EVT_MIDDLE_DOWN
	Process a wxEVT_MIDDLE_DOWN event.
EVT_MIDDLE_UP
	Process a wxEVT_MIDDLE_UP event.
EVT_MIDDLE_DCLICK
	Process a wxEVT_MIDDLE_DCLICK event.
EVT_RIGHT_DOWN
	Process a wxEVT_RIGHT_DOWN event.
EVT_RIGHT_UP
	Process a wxEVT_RIGHT_UP event.
EVT_RIGHT_DCLICK
	Process a wxEVT_RIGHT_DCLICK event.
EVT_MOUSE_AUX1_DOWN
	Process a wxEVT_AUX1_DOWN event.
EVT_MOUSE_AUX1_UP
	Process a wxEVT_AUX1_UP event.
EVT_MOUSE_AUX1_DCLICK
	Process a wxEVT_AUX1_DCLICK event.
EVT_MOUSE_AUX2_DOWN
	Process a wxEVT_AUX2_DOWN event.
EVT_MOUSE_AUX2_UP
	Process a wxEVT_AUX2_UP event.
EVT_MOUSE_AUX2_DCLICK
	Process a wxEVT_AUX2_DCLICK event.
EVT_MOTION
	Process a wxEVT_MOTION event.
EVT_ENTER_WINDOW
	Process a wxEVT_ENTER_WINDOW event.
EVT_LEAVE_WINDOW
	Process a wxEVT_LEAVE_WINDOW event.
EVT_MOUSEWHEEL
	Process a wxEVT_MOUSEWHEEL event.
EVT_MOUSE_EVENTS
	Process all mouse events.

##wx.MouseEvent - Extra members 
#use Get*/Set* methods 
LinesPerAction
    Returns the configured number of lines (or whatever) to be scrolled per wheel action.
    Default value under most platforms is three.
LogicalPosition 
    Returns the logical mouse position(wxpoint) in pixels 
    (i.e. translated according to the translation set for the DC, which usually indicates that the window has been scrolled).
WheelDelta 
    Get wheel delta, normally 120.
    This is the threshold for action to be taken, and one such action 
    (for example, scrolling one increment) should occur for each delta.
WheelRotation
    Get wheel rotation, positive or negative indicates direction of rotation.
    The position associated with a mouse event is expressed in the window coordinates of the window which generated the event, you can use wx.Window.ClientToScreen to convert it to screen coordinates and possibly call wx.Window.ScreenToClient next to convert it to window coordinates of another window.



 



##wx.MenuEvent - event types will receive a wx.MenuEvent parameter.
EVT_MENU_OPEN
    A menu is about to be opened. On Windows, this is only sent once for each navigation of the menubar (up until all menus have closed).
EVT_MENU_CLOSE
    A menu has been just closed. Notice that this event is currently being sent before the menu selection ( wxEVT_MENU ) event, if any.
EVT_MENU_HIGHLIGHT
    The menu item with the specified id has been highlighted: used to show help prompts in the status bar by wx.Frame
EVT_MENU_HIGHLIGHT_ALL
    A menu item has been highlighted, i.e. the currently selected menu item has changed.

##wx.MenuEvent - Extra members 
#Use Get*/Set* methods 
Menu 
    Returns the menu which is being opened or closed.
    This method can only be used with the OPEN and CLOSE events.
    The returned value is never None in the ports implementing this function, 
    which currently includes all the major ones.
    Return type:	wx.Menu
MenuId
    Returns the menu identifier associated with the event.
    This method should be only used with the HIGHLIGHT events.


##wx.EventFilter
static wx.EvtHandler.AddFilter(filter)
    Add an event filter whose FilterEvent() method will be called for each 
    and every event processed by wxWidgets.
    The filters are called in LIFO order 
    wx.App is registered as an event filter by default. 
    The pointer must remain valid until it’s removed with RemoveFilter 
    and is not deleted by wx.EvtHandler.
static wx.EvtHandler.RemoveFilter(filter)
    Remove a filter previously installed with AddFilter .    

#wx.App derives from wx.EventFilter and is registered as an event filter during its creation 
#so override FilterEvent method in App-derived class
wx.EventFilter.FilterEvent(self, event)
    Override this method to implement event pre-processing.
    event - (wx.Event instance), use event.GetEventType() to get EVT_*
    Must returns   
        wx.EventFilter.Event_Skip to continue processing the event normally (this should be used in most cases).
        wx.EventFilter.Event_Ignore to not process this event at all (this can be used to suppress some events).
        wx.EventFilter.Event_Processed to not process this event normally but indicate that it was already processed by the event filter and so no default processing should take place neither (this should only be used if the filter really did process the event).
 

#Example - This class allows to determine the last time the user has worked with
# this application:
class LastActivityTimeDetector(wx.EventFilter):
    def __init__(self):
        wx.EventFilter.__init__(self)
        wx.EvtHandler.AddFilter(self)
        self.last = wx.DateTime.Now()
    def __del__(self):
        wx.EvtHandler.RemoveFilter(self)
    def FilterEvent(self, event):
        # Update the last user activity
        t = event.GetEventType()
        if t == wx.EVT_KEY_DOWN.typeId or t == wx.EVT_MOTION.typeId or \
           t == wx.EVT_LEFT_DOWN.typeId or t == wx.EVT_RIGHT_DOWN.typeId or \
           t == wx.EVT_MIDDLE_DOWN.typeId:
            self.last = wx.DateTime.Now()
        # Continue processing the event normally as well.
        return self.Event_Skip
    # This function could be called periodically from some timer to
    # do something (e.g. hide sensitive data or log out from remote
    # server) if the user has been inactive for some time period.
    def IsInactiveFor(self, diff):
        return wx.DateTime.Now() - diff > self.last
        
        
        
        
  

   
   
   
   
##Event - Custom Event - use wx.lib.newevent

import wx
import wx.lib.newevent

SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
SomeNewCommandEvent, EVT_SOME_NEW_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()

#bind the events normally via either binding syntax:
self.Bind(EVT_SOME_NEW_EVENT, self.handler, source, id)


#attach arbitrary data to the event during its creation, 
#then post it to whatever window you choose:
# Create the event
evt = SomeNewEvent(attr1="hello", attr2=654)
# Post the event
wx.PostEvent(target, evt)

#fetch the data via attributes in handler 
def handler(self, evt):
    # Given the above constructed event, the following is true
    evt.attr1 == "hello"
    evt.attr2 == 654

    
    
    
##Event - User Generated Events vs Programmatically Generated Events
#While generically a wx.Event can be generated both by user actions 
#(e.g., resize of a wx.Window) and by calls to functions (e.g., wx.Window.SetSize), 
#wxPython controls normally send wx.CommandEvent -derived events only for the user-generated events. 
#The only exceptions to this rule are:
    wx.BookCtrlBase.AddPage No event-free alternatives
    wx.BookCtrlBase.AdvanceSelection No event-free alternatives
    wx.BookCtrlBase.DeletePage No event-free alternatives
    wx.Notebook.SetSelection: Use wx.Notebook.ChangeSelection instead, as wx.Notebook.SetSelection is deprecated
    wx.TreeCtrl.Delete: No event-free alternatives
    wx.TreeCtrl.DeleteAllItems: No event-free alternatives
    wx.TreeCtrl.EditLabel: No event-free alternatives
    All wx.TextCtrl methods
        wx.TextEntry.ChangeValue can be used instead of wx.TextEntry.SetValue 
        but the other functions, such as wx.TextEntry.Replace 
        or wx.TextCtrl.WriteText don’t have event-free equivalents.

##Event - Event types  generated by wx.Window 
EVT_ACTIVATE
    Process a wxEVT_ACTIVATE event. See wx.ActivateEvent.
EVT_CHILD_FOCUS
	Process a wxEVT_CHILD_FOCUS event. See wx.ChildFocusEvent.
EVT_CONTEXT_MENU
	A right click (or other context menu command depending on platform) has been detected. See wx.ContextMenuEvent.
EVT_HELP
	Process a wxEVT_HELP event. See wx.HelpEvent.
EVT_HELP_RANGE
	Process a wxEVT_HELP event for a range of ids. See wx.HelpEvent.
EVT_DROP_FILES
	Process a wxEVT_DROP_FILES event. See wx.DropFilesEvent.
EVT_ERASE_BACKGROUND
	Process a wxEVT_ERASE_BACKGROUND event. See wx.EraseEvent.
EVT_SET_FOCUS
	Process a wxEVT_SET_FOCUS event. See wx.FocusEvent.
EVT_KILL_FOCUS
	Process a wxEVT_KILL_FOCUS event. See wx.FocusEvent.
EVT_IDLE
	This class is used for idle events, which are generated when the system becomes idle.
    It is sent only Once during one idle time 
    If you need to ensure a continuous stream of idle events, 
    you can either use wx.IdleEvent.RequestMore method in your handler 
    or call wx.WakeUpIdle periodically (for example from a timer event handler), 
EVT_JOY_*
	Processes joystick events. See wx.JoystickEvent.
EVT_KEY_DOWN
	Process a wxEVT_KEY_DOWN event (any key has been pressed). See wx.KeyEvent.
EVT_KEY_UP
	Process a wxEVT_KEY_UP event (any key has been released). See wx.KeyEvent.
EVT_CHAR
	Process a wxEVT_CHAR event. See wx.KeyEvent.
EVT_CHAR_HOOK
	Process a wxEVT_CHAR_HOOK event. See wx.KeyEvent.
EVT_MOUSE_CAPTURE_LOST
	Process a wxEVT_MOUSE_CAPTURE_LOST event. See wx.MouseCaptureLostEvent.
EVT_MOUSE_CAPTURE_CHANGED
	Process a wxEVT_MOUSE_CAPTURE_CHANGED event. See wx.MouseCaptureChangedEvent.
EVT_MOUSE_*
	See wx.MouseEvent.
EVT_PAINT
	Process a wxEVT_PAINT event. See wx.PaintEvent.
EVT_POWER_*
	The system power state changed. See wx.PowerEvent.
EVT_SCROLLWIN_*
	Process scroll events. See wx.ScrollWinEvent.
EVT_SET_CURSOR
	Process a wxEVT_SET_CURSOR event. See wx.SetCursorEvent.
EVT_SIZE
	Process a wxEVT_SIZE event. See wx.SizeEvent.
EVT_SYS_COLOUR_CHANGED
	Process a wxEVT_SYS_COLOUR_CHANGED event. See wx.SysColourChangedEvent.

##Event - Event types  generated by wx.Frame 
EVT_CLOSE
	Process a wxEVT_CLOSE_WINDOW event when the frame is being closed by the user or programmatically (see wx.Window.Close ). The user may generate this event clicking the close button (typically the ‘X’ on the top-right of the title bar) if it’s present (see the CLOSE_BOX style). See wx.CloseEvent.
EVT_ICONIZE
	Process a wxEVT_ICONIZE event. See wx.IconizeEvent.
EVT_MENU_OPEN
	A menu is about to be opened. See wx.MenuEvent.
EVT_MENU_CLOSE
	A menu has been just closed. See wx.MenuEvent.
EVT_MENU_HIGHLIGHT
	The menu item with the specified id has been highlighted
	used to show help prompts in the status bar by wx.Frame. See wx.MenuEvent.
EVT_MENU_HIGHLIGHT_ALL
	A menu item has been highlighted, i.e. the currently selected menu item has changed. See wx.MenuEvent.


    



            
##wxpython - wx.App(derived from wx.AppConsole) 
#A wxPython application does not have a main procedure; 
#the equivalent is the wx.AppConsole.OnInit member in wx.App.

#OnInit will usually create a top window as a bare minimum. 
#it returns a boolean value which indicates whether processing should continue (True) or not (False).



class DerivedApp(wx.App):

    def OnInit(self):
        the_frame = wx.Frame(None, -1)

        # Other initialization code...
        the_frame.Show(True)
        return True

##Application Shutdown
#An application closes by destroying all windows. 
#Because all frames must be destroyed for the application to exit, 
#it is advisable to use parent frames wherever possible when creating new frames, 
#so that deleting the top level frame will automatically delete child frames. 

#OR explicitly delete child frames in the top-level frame’s wx.CloseEvent handler.

#In emergencies the wx.Exit function can be called to kill the application 
#however, normally the application shuts down automatically 
#when the last top-level window closes 
#ie it is enough to call wx.Window.Close`() in response to the "Exit" menu command 
#if program has a single top level window.  
#If this behavior is not desirable wx.PyApp.SetExitOnFrameDelete can be called to change it.

#Note that such logic doesn’t apply for the windows shown before the program enters the main loop
#ie a dialog shown from wx.AppConsole.OnInit would not be closed 

#At the application shutdown, wx.AppConsole.OnExit  is called 
#when the application exits but before wxPython cleans up its internal structures

##wx.AppConsle Virtual Methods 
OnEventLoopEnter(self,loop)
    Called by wx.EventLoopBase.SetActive 
    you can override this function and put here the code which needs an active event loop.
OnEventLoopExit(self,loop)
    Called by wx.EventLoopBase.OnExit for each event loop which is exited.
OnExit(self)
    Override this member function for any processing which needs to be done as the application is about to exit.
OnInit(self)
 	This must be provided by the application, 
    and will usually create the application’s main window, optionally calling SetTopWindow().
    Return True to continue processing, False to exit the application immediately.
OnRun(self)
    This virtual function is where the execution of a program written in wxWidgets starts.

##wx.AppConsle other important  Methods 
SetAppDisplayName 	    Set the application name to be used in the user-visible places such as window titles.
SetAppName 	            Sets the name of the application.
SetCLocale 	            Sets the C locale to the default locale for the current environment.
SetClassName 	        Sets the class name of the application.
SetInstance 	        Allows external code to modify global wx.TheApp , but you should really know what you’re doing if you call it.
SetVendorDisplayName 	Set the vendor name to be used in the user-visible places.
SetVendorName 	        Sets the name of application’s vendor.
SuspendProcessingOfPendingEvents 	Temporary suspends processing of the pending events.
ProcessPendingEvents 	Process all pending events; it is necessary to call this function to process events posted with wx.EvtHandler.QueueEvent or wx.EvtHandler.AddPendingEvent .
ResumeProcessingOfPendingEvents 	Resume processing of the pending events previously stopped because of a call to SuspendProcessingOfPendingEvents 
MainLoop 	            Called by wxWidgets on creation of the application.
DeletePendingEvents 	Deletes the pending events of all EvtHandlers of this application.
ExitMainLoop 	        Call this to explicitly exit the main message (event) loop.
FilterEvent 	        Overridden wx.EventFilter method.




##wxpython - Common Dialogs
#Each Dialog has  .ShowModal()
#that Shows the dialog, returning ID_OK if the user pressed wx.OK, and ID_CANCEL otherwise.
#If ID_OK is returned, respective data can be retrived by some Get*() methods 
wx.ColourDialog(parent, data=None)
    This class represents the colour chooser dialog. 
    data retrival method:  GetColourData():wx.ColourData
wx.FontDialog(parent, data=None)
    This class represents the font chooser dialog.
    data retrival method:   GetFontData():wx.FontData
wx.PrintDialog(parent, data=None)
    This class represents the print and print setup common dialogs.
    data retrival method:GetPrintDC():wx.DC   
                         GetPrintData():wx.PrintData ,used to initialize a wx.PrinterDC or wx.PostScriptDC.
wx.FileDialog(parent, message=FileSelectorPromptStr,
           defaultDir="", defaultFile="",
           wildcard=FileSelectorDefaultWildcardStr, style=FD_DEFAULT_STYLE,
           pos=DefaultPosition, size=DefaultSize, name=FileDialogNameStr)
    This class represents the file chooser dialog.
    data retrival method:GetPath():string
                         GetPaths(self):list of strings, if style is MULTIPLE
wx.DirDialog(parent, message=DirSelectorPromptStr, defaultPath="",
          style=DD_DEFAULT_STYLE, pos=DefaultPosition, size=DefaultSize,
          name=DirDialogNameStr)
    This class represents the directory chooser dialog.
    data retrival method:GetPath():string
wx.TextEntryDialog(parent, message, caption=GetTextFromUserPromptStr,
                value="", style=TextEntryDialogStyle, pos=DefaultPosition)
    This class represents a dialog that requests a one-line text string from the user.
    data retrival method:GetValue():string
wx.PasswordEntryDialog(parent, message,
                    caption=GetPasswordFromUserPromptStr, defaultValue="",
                    style=TextEntryDialogStyle, pos=DefaultPosition)
    This class represents a dialog that requests a one-line password string from the user. 
    data retrival method:GetValue():string
wx.MessageDialog(parent, message, caption=MessageBoxCaptionStr,
              style=OK|CENTRE, pos=DefaultPosition)
    This class represents a dialog that shows a single or multi-line message, 
    with a choice of wx.OK, Yes, No and Cancel buttons.
    ShowModal() returns the identifier of the button which was clicked 
wx.SingleChoiceDialog( parent, message, caption, choices, style=CHOICEDLG_STYLE, pos=DefaultPosition)
    This class represents a dialog that shows a list of strings, and allows the user to select one.
    data retrival method:GetSelection():index or GetStringSelection():string
wx.MultiChoiceDialog(parent, message, caption, n, choices,
                  style=CHOICEDLG_STYLE, pos=DefaultPosition)
    This class represents a dialog that shows a list of strings, 
    and allows the user to select one or more.
    data retrival method:GetSelection():list of index 
    

#Example-wx.ColourDialog, 
#which sets various parameters of a wx.ColourData object, 
#including a grey scale for the custom colours. 
#If the user did not cancel the dialog, the application retrieves the selected colour 
#and uses it to set the background of a window:

data = wx.ColourData()
data.SetChooseFull(True)

for i in xrange(16):
    colour = wx.Colour(i*16, i*16, i*16)
    data.SetCustomColour(i, colour)

dialog = wx.ColourDialog(self, data)
if dialog.ShowModal() == wx.ID_OK:
    retData = dialog.GetColourData()
    col = retData.GetColour()
    brush = wx.Brush(col, wx.SOLID)
    myWindow.SetBackground(brush)
    myWindow.Clear()
    myWindow.Refresh()

#Example - wx.FontDialog. 
#The application uses the returned font and colour for drawing text on a canvas:

data = wx.FontData()
data.SetInitialFont(canvasFont)
data.SetColour(canvasTextColour)

dialog = wx.FontDialog(self, data)
if dialog.ShowModal() == wx.ID_OK:
    retData = dialog.GetFontData()
    canvasFont = retData.GetChosenFont()
    canvasTextColour = retData.GetColour()
    myWindow.Refresh()
    
    
    

##wxpython - Device Contexts
#A wx.DC is a device context onto which graphics and text can be drawn. 
#Represents a number of output devices(screen, printer etc) in a generic way, with the same API being used throughout.

#Some device contexts are created temporarily in order to draw on a window. 
1.wx.ScreenDC. Use this to paint on the screen, as opposed to an individual window.
2.wx.ClientDC. Use this to paint on the client area of window (the part without borders and other decorations), 
  but do not use it from within an wx.PaintEvent.
3.wx.PaintDC. Use this to paint on the client area of a window, 
  but only from within a wx.PaintEvent.
4.wx.WindowDC. Use this to paint on the whole area of a window, including decorations. 
  This may not be available on non-Windows platforms.
5. wx.GCDC  : wx.GCDC is a device context that draws on a wx.GraphicsContext.
6.wx.MemoryDC :A memory device context provides a means to draw graphics onto a bitmap.
7.wx.PrinterDC
  A printer device context is specific to MSW and Mac, and allows access to any printer with a Windows or Macintosh driver.
8.wx.MirrorDC
  wx.MirrorDC is a simple wrapper class which is always associated with a real wx.DC object 
  and either forwards all of its operations to it without changes (no mirroring takes place) 
  or exchanges x and y coordinates which makes it possible to reuse the same code to draw a figure and its mirror
  reflection related to the diagonal line x == y.
9.wx.PostScriptDC
  This defines the wxWidgets Encapsulated PostScript device context, 
  which can write PostScript files on any platform.
10.wx.SVGFileDC
   A wx.SVGFileDC is a device context onto which graphics and text can be drawn, 
   and the output produced as a vector file, in SVG format.


#To use a client
def OnMyCmd(self, event):
    dc = wx.ClientDC(window)
    DrawMyPicture(dc)

##wxpython - Device Context - wx.MemoryDC
#A memory device context provides a means to draw graphics onto a bitmap.
#When drawing in to a mono-bitmap, 
#using WHITE , WHITE_PEN and WHITE_BRUSH will draw the background colour (i.e. 0) 
#whereas all other colours will draw the foreground colour (i.e. 1).

#A bitmap must be selected into the new memory DC before it may be used for anything. 
# Create a memory DC
temp_dc = wx.MemoryDC()
temp_dc.SelectObject(test_bitmap)

# We can now draw into the memory DC...
# Copy from this DC to another DC.
old_dc.Blit(250, 50, BITMAP_WIDTH, BITMAP_HEIGHT, temp_dc, 0, 0)

#Note that the memory DC must be deleted (or the bitmap selected out of it) 
#before a bitmap can be reselected into another memory DC.

#And, before performing any other operations on the bitmap data, 
#the bitmap must be selected out of the memory DC
#This happens automatically when wx.MemoryDC object goes out of scope.
temp_dc.SelectObject(wx.NullBitmap)


##wxpython - Device Context - One Major functions 
wx.DC.Blit(self, xdest, ydest, width, height, source, xsrc, ysrc, logicalFunc=COPY, useMask=False, xsrcMask=DefaultCoord, ysrcMask=DefaultCoord)
    Copy from a source DC to this DC.
    logicalFunc is from https://wxpython.org/Phoenix/docs/html/wx.RasterOperationMode.enumeration.html
    
##wxpython - Device Context - Device and logical units
#In the wx.DC context there is a distinction between logical units and device units. 
#Device units are the units native to the particular device; 
#e.g. for a screen, a device unit is a pixel. 
#For a printer, the device unit is defined by the resolution of the printer (usually given in DPI: dot-per-inch). 

#All wx.DC functions use instead logical units, unless where explicitly stated. 
#Logical units are arbitrary units mapped to device units using the current mapping mode 
#(wx.DC.SetMapMode ). 
#This mechanism allows to reuse the same code which prints on 
#e.g. a window on the screen to print on e.g. a paper.

##wxpython - Device Context - Support for Transparency / Alpha Channel
#In general wx.DC methods don’t support alpha transparency and the alpha component of wx.Colour
#use wx.GraphicsContext for full transparency support
 

##wxpython - Device Context - wx.GraphicsContext
#A wx.GraphicsContext instance is the object that is drawn upon.
#wx.GraphicsContext is a newer, more advanced and more powerful drawing API

def OnPaint(self, event):
    # Create paint DC
    dc = wx.PaintDC(self)
    # Create graphics context from it
    gc = wx.GraphicsContext.Create(dc)
    if gc:
        # make a path that contains a circle and some lines
        gc.SetPen(wx.RED_PEN)
        path = gc.CreatePath()
        path.AddCircle(50.0, 50.0, 50.0)
        path.MoveToPoint(0.0, 50.0)
        path.AddLineToPoint(100.0, 50.0)
        path.MoveToPoint(50.0, 0.0)
        path.AddLineToPoint(50.0, 100.0)
        path.CloseSubpath()
        path.AddRectangle(25.0, 25.0, 50.0, 50.0)
        gc.StrokePath(path)


#Methods pf wx.DC 
Blit 	                Copy from a source DC to this DC.
CalcBoundingBox 	    Adds the specified point to the bounding box which can be retrieved with MinX , MaxX and MinY , MaxY functions.
CanDrawBitmap 	        Does the DC support drawing bitmaps?
CanGetTextExtent 	    Does the DC support calculating the size required to draw text?
CanUseTransformMatrix 	Check if the use of transformation matrix is supported by the current system.
Clear 	                Clears the device context using the current background brush.
CopyAttributes 	        Copy attributes from another DC.
CrossHair 	            Displays a cross hair using the current pen.
DestroyClippingRegion 	Destroys the current clipping region so that none of the DC is clipped.
DeviceToLogicalX 	    Convert device X coordinate to logical coordinate, using the current mapping mode, user scale factor, device origin and axis orientation.
DeviceToLogicalXRel 	Convert device X coordinate to relative logical coordinate, using the current mapping mode and user scale factor but ignoring the axis orientation.
DeviceToLogicalY 	    Converts device Y coordinate to logical coordinate, using the current mapping mode, user scale factor, device origin and axis orientation.
DeviceToLogicalYRel 	Convert device Y coordinate to relative logical coordinate, using the current mapping mode and user scale factor but ignoring the axis orientation.
DrawArc 	            Draws an arc from the given start to the given end point.
DrawBitmap 	            Draw a bitmap on the device context at the specified point.
DrawCheckMark 	        Draws a check mark inside the given rectangle.
DrawCircle 	            Draws a circle with the given centre and radius.
DrawEllipse 	        Draws an ellipse contained in the rectangle specified either with the given top left corner and the given size or directly.
DrawEllipseList 	    Draw a list of ellipses as quickly as possible.
DrawEllipticArc 	    Draws an arc of an ellipse.
DrawIcon 	            Draw an icon on the display (does nothing if the device context is PostScript).
DrawLabel 	            Draw optional bitmap and the text into the given rectangle and aligns it as specified by alignment parameter; it also will emphasize the character with the given index if it is != -1 and return the bounding rectangle if required.
DrawLine 	            Draws a line from the first point to the second.
DrawLineList 	        Draw a list of lines as quickly as possible.
DrawLines 	            This method uses a list of Points, adding the optional offset coordinate.
DrawPoint 	            Draws a point using the color of the current pen.
DrawPointList 	        Draw a list of points as quickly as possible.
DrawPolygon 	        This method draws a filled polygon using a list of Points, adding the optional offset coordinate.
DrawPolygonList 	    Draw a list of polygons, each of which is a list of points.
DrawRectangle 	        Draws a rectangle with the given top left corner, and with the given size.
DrawRectangleList 	    Draw a list of rectangles as quickly as possible.
DrawRotatedText 	    Draws the text rotated by angle degrees (positive angles are counterclockwise; the full angle is 360 degrees).
DrawRoundedRectangle 	Draws a rectangle with the given top left corner, and with the given size.
DrawSpline 	            This is an overloaded member function, provided for convenience. It differs from the above function only in what argument(s) it accepts.
DrawText 	            Draws a text string at the specified point, using the current text font, and the current text foreground and background colours.
DrawTextList 	        Draw a list of strings using a list of coordinants for positioning each string.
EndDoc 	                Ends a document (only relevant when outputting to a printer).
EndPage 	            Ends a document page (only relevant when outputting to a printer).
FloodFill 	            Flood fills the device context starting from the given point, using the current brush colour, and using a style
GetAsBitmap 	        If supported by the platform and the type of DC, fetch the contents of the DC, or a subset of it, as a bitmap.
GetBackground 	        Gets the brush used for painting the background.
GetBackgroundMode 	    Returns the current background mode: SOLID or TRANSPARENT .
GetBoundingBox 	        GetBoundingBox() . (x1,y1, x2,y2)
GetBrush 	            Gets the current brush.
GetCGContext 	 
GetCharHeight 	        Gets the character height of the currently set font.
GetCharWidth 	        Gets the average character width of the currently set font.
GetClippingBox 	        Gets the rectangle surrounding the current clipping region.
GetClippingRect 	    Gets the rectangle surrounding the current clipping region
GetDepth 	            Returns the depth (number of bits/pixel) of this DC.
GetDeviceOrigin 	    Returns the current device origin.
GetFont 	            Gets the current font.
GetFontMetrics 	        Returns the various font characteristics.
GetGdkDrawable 	 
GetHDC 	 
GetHandle 	            Returns a value that can be used as a handle to the native drawing context, if this wx.DC has something that could be thought of in that way.
GetLayoutDirection 	    Gets the current layout direction of the device context.
GetLogicalFunction 	    Gets the current logical function.
GetLogicalOrigin 	    Return the coordinates of the logical point (0, 0).
GetLogicalScale 	    Return the scale set by the last call to SetLogicalScale .
GetMapMode 	            Gets the current mapping mode for the device context.
GetFullMultiLineTextExtent 	Gets the dimensions of the string as it would be drawn.
GetMultiLineTextExtent 	Return the dimensions of the given string’s text extent using the
GetPPI 	                Returns the resolution of the device in pixels per inch.
GetPartialTextExtents 	Fills the widths array with the widths from the beginning of text to the corresponding character of text.
GetPen 	                Gets the current pen.
GetPixel 	            Gets the colour at the specified location on the DC.
GetSize 	            This is an overloaded member function, provided for convenience. It differs from the above function only in what argument(s) it accepts.
GetSizeMM 	            This is an overloaded member function, provided for convenience. It differs from the above function only in what argument(s) it accepts.
GetTextBackground 	    Gets the current text background colour.
GetFullTextExtent 	    Gets the dimensions of the string as it would be drawn.
GetTextExtent 	        Return the dimensions of the given string’s text extent using the
GetTextForeground 	    Gets the current text foreground colour.
GetTransformMatrix 	    Return the transformation matrix used by this device context.
GetUserScale 	        Gets the current user scale factor.
GradientFillConcentric 	Fill the area specified by rect with a radial gradient, starting from initialColour at the centre of the circle and fading to destColour on the circle outside.
GradientFillLinear 	    Fill the area specified by rect with a linear gradient, starting from initialColour and eventually fading to destColour.
IsOk 	                Returns True if the DC is ok to use.
LogicalToDeviceX 	    Converts logical X coordinate to device coordinate, using the current mapping mode, user scale factor, device origin and axis orientation.
LogicalToDeviceXRel 	Converts logical X coordinate to relative device coordinate, using the current mapping mode and user scale factor but ignoring the axis orientation.
LogicalToDeviceY 	    Converts logical Y coordinate to device coordinate, using the current mapping mode, user scale factor, device origin and axis orientation.
LogicalToDeviceYRel 	Converts logical Y coordinate to relative device coordinate, using the current mapping mode and user scale factor but ignoring the axis orientation.
MaxX 	                Gets the maximum horizontal extent used in drawing commands so far.
MaxY 	                Gets the maximum vertical extent used in drawing commands so far.
MinX 	                Gets the minimum horizontal extent used in drawing commands so far.
MinY 	                Gets the minimum vertical extent used in drawing commands so far.
ResetBoundingBox 	    Resets the bounding box: after a call to this function, the bounding box doesn’t contain anything.
ResetTransformMatrix 	Revert the transformation matrix to identity matrix.
SetAxisOrientation 	    Sets the x and y axis orientation (i.e. the direction from lowest to highest values on the axis).
SetBackground 	        Sets the current background brush for the DC.
SetBackgroundMode 	    mode may be one of SOLID and TRANSPARENT .
SetBrush 	            Sets the current brush for the DC.
SetClippingRegion 	    Sets the clipping region for this device context to the intersection of the given region described by the parameters of this method and the previously set clipping region.
SetDeviceClippingRegion Sets the clipping region for this device context.
SetDeviceOrigin 	    Sets the device origin (i.e. the origin in pixels after scaling has been applied).
SetFont 	            Sets the current font for the DC.
SetLayoutDirection 	    Sets the current layout direction for the device context.
SetLogicalFunction 	    Sets the current logical function for the device context.
SetLogicalOrigin 	    Change the offset used for translating wx.DC coordinates.
SetLogicalScale 	    Set the scale to use for translating wx.DC coordinates to the physical pixels.
SetMapMode 	            The mapping mode of the device context defines the unit of measurement used to convert logical units to device units.
SetPalette 	            If this is a window DC or memory DC, assigns the given palette to the window or bitmap associated with the DC.
SetPen 	                Sets the current pen for the DC.
SetTextBackground 	    Sets the current text background colour for the DC.
SetTextForeground 	    Sets the current text foreground colour for the DC.
SetTransformMatrix 	    Set the transformation matrix.
SetUserScale 	        Sets the user scaling factor, useful for applications which require ‘zooming’.
StartDoc 	            Starts a document (only relevant when outputting to a printer).
StartPage 	            Starts a document page (only relevant when outputting to a printer).
StretchBlit 	        Copy from a source DC to this DC possibly changing the scale.
  
  
  
  
  
  
  
  
  
  
##wxpython - Font 
wx.Font()
wx.Font(font)
wx.Font(fontInfo)
wx.Font(pointSize, family, style, weight, underline=False, faceName="", encoding=FONTENCODING_DEFAULT)
wx.Font(pixelSize, family, style, weight, underline=False,faceName="", encoding=FONTENCODING_DEFAULT)
wx.Font(nativeInfoString)
wx.Font(nativeInfo)
    A font is an object which determines the appearance of text.
    Point size 	    This is the standard way of referring to text size.
    Family 	        Supported families are: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN. wx.MODERN is a fixed pitch font; the others are either fixed or variable pitch.
    Style 	        One of wx.FONTSTYLE_NORMAL , wx.FONTSTYLE_SLANT and wx.FONTSTYLE_ITALIC .
                    or wx.NORMAL, WX.BOLD, WX.ITALIC
    Weight 	        wx.FONTWEIGHT_NORMAL,wx.FONTWEIGHT_LIGHT,wx.FONTWEIGHT_BOLD,wx.FONTWEIGHT_MAX
    Underlining 	The value can be True or False.
    Face name 	    An optional string specifying the actual typeface to be used. 
                    If None, a default typeface will chosen based on the family.
    Encoding 	    FONTENCODING_SYSTEM 	Default system encoding.
                    FONTENCODING_DEFAULT 	Default application encoding: this is the encoding set by calls to SetDefaultEncoding and which may be set to, say, KOI8 to create all fonts by default with KOI8 encoding. Initially, the default application encoding is the same as default system encoding.
                    FONTENCODING_ISO8859_1 ...15 	ISO8859 encodings.
                    FONTENCODING_KOI8 	The standard Russian encoding for Internet.
                    FONTENCODING_CP1250 ...1252 	Windows encodings similar to ISO8859 (but not identical).

#To get system Font 
static wx.SystemSettings.GetFont(index)
    Returns a system font.
    Parameters:	index (SystemFont) – Can be one of the https://wxpython.org/Phoenix/docs/html/wx.SystemFont.enumeration.html
    Return type:	wx.Font




##wxpython - wx.Colour
Colour()
Colour(red, green, blue, alpha=ALPHA_OPAQUE)
Colour(colRGB)
Colour(colour)
    A colour is an object representing a combination of Red, Green, and Blue (RGB) 
    intensity values, and is used to determine drawing colours.
    Valid RGB values are in the range 0 to 255.
    #Properties Summary
    #Use Get*/Set* methods to access 
    Pixel 	
    RGB 	
    RGBA 	
    alpha 	
    blue 	
    green 	
    red 	
    
#To get system Color 
static wx.SystemSettings.GetColour(index)
    Returns a system font.
    Parameters:	index  – Can be one of the https://wxpython.org/Phoenix/docs/html/wx.SystemColour.enumeration.html
    Return type:	wx.Colour


##wx.ColourDatabase

wx.TheColourDatabase
    Global instance of wx.ColourDatabase, maintains  predefined set of named colours.
    Use .Find(colourName):wx.Colour or .FindName(colour):string 
    #Names 
    AQUAMARINE 	FIREBRICK 	MEDIUM FOREST GREEN 	RED
    BLACK 	FOREST GREEN 	MEDIUM GOLDENROD 	SALMON
    BLUE 	GOLD 	MEDIUM ORCHID 	SEA GREEN
    BLUE VIOLET 	GOLDENROD 	MEDIUM SEA GREEN 	SIENNA
    BROWN 	GREY 	MEDIUM SLATE BLUE 	SKY BLUE
    CADET BLUE 	GREEN 	MEDIUM SPRING GREEN 	SLATE BLUE
    CORAL 	GREEN YELLOW 	MEDIUM TURQUOISE 	SPRING GREEN
    CORNFLOWER BLUE 	INDIAN RED 	MEDIUM VIOLET RED 	STEEL BLUE
    CYAN 	KHAKI 	MIDNIGHT BLUE 	TAN
    DARK GREY 	LIGHT BLUE 	NAVY 	THISTLE
    DARK GREEN 	LIGHT GREY 	ORANGE 	TURQUOISE
    DARK OLIVE GREEN 	LIGHT STEEL BLUE 	ORANGE RED 	VIOLET
    DARK ORCHID 	LIME GREEN 	ORCHID 	VIOLET RED
    DARK SLATE BLUE 	MAGENTA 	PALE GREEN 	WHEAT
    DARK SLATE GREY 	MAROON 	PINK 	WHITE
    DARK TURQUOISE 	MEDIUM AQUAMARINE 	PLUM 	YELLOW
    DIM GREY 	MEDIUM BLUE 	PURPLE 	YELLOW GREEN




@@@

##wxpython - Wx.Sizer
#platform independent layout 

wx.Object 
    wx.Sizer 
            Use .Add(control_or_sizer, proportion=0, flag=0) to add one control or another sizer to sizer
        wx.BoxSizer(orient=wx.HORIZONTAL or wx.VERTICAL)
                Layout of controls in a row or a column or several hierarchies of either.
            wx.StaticBoxSizer(orient, parent, label='') 
                sizer derived from wx.BoxSizer but adds a static box around the sizer
        wx.GridSizer( rows, cols, vgap, hgap)
                A grid sizer is a sizer which lays out its children in a two-dimensional table with all table fields having the same size, i.e.
                the width of each field is the width of the widest child, the height of each field is the height of the tallest child.
            wx.FlexGridSizer(rows, cols, vgap, hgap)
                A flex grid sizer is a sizer which lays out its children in a two-dimensional table 
                with all table fields in one row having the same height and all fields in one column having the same width, but all rows or all columns are not necessarily the same height or width as in the wx.GridSizer.
                wx.GridBagSizer(vgap=0, hgap=0)
                    A Sizer that can lay out items in a virtual grid like a FlexGridSizer but in this case explicit positioning of the items is allowed using GBPosition, and items can optionally span more than one row and/or column using GBSpan.
            wx.WrapSizer(orient=HORIZONTAL, flags=WRAPSIZER_DEFAULT_FLAGS)
                A wrap sizer lays out its items in a single line, like a box sizer
                Once all available space in the primary direction has been used, a new line is added and items are added there.             

                

#RAD tool using wx.Sizer wxDesigner, DialogBlocks, XRCed and wxWorkshop


#All sizers are containers
#all children of sizers have certain features in common:
A minimal size
A border
An alignment
A stretch factor


##Basic way of adding a window
wx.Sizer.Add (self, window, flags)
wx.Sizer.Add (self, sizer, flags)
wx.Sizer.Add (self, sizer, proportion=0, flag=0, border=0, userData=None)
wx.Sizer.Add (self, width, height, proportion=0, flag=0, border=0, userData=None)
wx.Sizer.Add (self, width, height, flags)
wx.Sizer.Add(self, size, proportion=0, flag=0, border=0, Transfer=None)
wx.Sizer.Add (self, size, flags)
wx.Sizer.Add (self, item)
wx.Sizer.Add(window, proportion=0, flag=0, border=0, userData=None)
    Appends a child or some space(called spacer via width,height or size,wx.Size) to the sizer.
        window 
            a window, a spacer or another sizer to be added to the sizer. 
            Its initial size (either set explicitly by the user or calculated internally) is interpreted as the minimal 
            and in many cases also the initial size.
        proportion (int) 
            this parameter is used in wx.BoxSizer to indicate 
            if a child of a sizer can change its size in the main orientation of the wx.BoxSizer 
            - where 0 stands for not changeable and a value of more than zero is interpreted relative 
            to the value of other children of the same wx.BoxSizer. 
            For example, you might have a horizontal wx.BoxSizer with three children, 
            two of which are supposed to change their size with the sizer. 
            Then the two stretchable windows would get a value of 1 each to make them grow and shrink equally with the sizer’s horizontal dimension.
        flag (int) 
            OR-combination of flags affecting sizer’s behaviour.
        border (int) 
            determines the border width, if the flag parameter is set to include any border flag.
        userData (object) 
            allows an extra object to be attached to the sizer item, for use in derived classes 
            when sizing information is more complex than the proportion and flag will allow for.
            
    Return type:	
        wx.SizerItem


wx.Sizer.AddMany(self, items)
    adding several items to a sizer at one time. 
    pass it a list of tuples, where each tuple consists of the args as given in .Add(...)
    
    
    
#Example - create a vertical sizer (children will be placed on top of each other) 
#and place two buttons in it. 

#any control placed into a sizer this way will appear at its minimum size
#The window size is not changed to fit the sizer. This results in a lot of ugly empty space.
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(wx.Button(self, -1, 'An extremely long button text'), 0, 0, 0)
sizer.Add(wx.Button(self, -1, 'Small button'), 0, 0, 0)
self.SetSizer(sizer)

#To make the window size more appropriate, 
#Use size hints to tell the enclosing window to adjust to the size of the sizer:
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(wx.Button(self, -1, 'An extremely long button text'), 0, 0, 0)
sizer.Add(wx.Button(self, -1, 'Small button'), 0, 0, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

##The proportion parameter
#defines how large the sizer’s children are in relation to each other. 
#In a vertical sizer, this changes the height; 
#in a horizontal sizer, this changes the width. 

#Example - 2nd button is 3 times of first One 
sizer = wx.BoxSizer(wx.VERTICAL)
# Second button is three times as tall as first button
sizer.Add(wx.Button(self, -1, 'An extremely long button text'), 1, 0, 0)
sizer.Add(wx.Button(self, -1, 'Small button'), 3, 0, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
#Another example : First button is 3/2 the height of the second button
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(wx.Button(self, -1, 'An extremely long button text'), 3, 0, 0)
sizer.Add(wx.Button(self, -1, 'Small button'), 2, 0, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

#If one of the proportion parameters is 0, 
#that wx.Window will be the minimum size, and the others will resize proportionally:

sizer = wx.BoxSizer(wx.VERTICAL)
# Third button is twice the size of the second button
sizer.Add(wx.Button(self, -1, 'An extremely long button text'), 0, 0, 0)
sizer.Add(wx.Button(self, -1, 'Small button'), 1, 0, 0)
sizer.Add(wx.Button(self, -1, 'Another button'), 2, 0, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

##The flags and border parameters
#flags : OR-combination of the following flags. 
#border :determines the border width 
#whereas the flags given here determine which side(s) of the item that the border will be added. 

1. These flags are used to specify which side(s) of the sizer item 
   the border width will apply to.
    wx.TOP
    wx.BOTTOM
    wx.LEFT
    wx.RIGHT
    wx.ALL
	
2.The wx.ALIGN* flags allow you to specify the alignment of the item 
  within the space allotted to it by the sizer, adjusted for the border if any.
    wx.ALIGN_CENTER or wx.ALIGN_CENTRE
    wx.ALIGN_LEFT
    wx.ALIGN_RIGHT
    wx.ALIGN_RIGHT
    wx.ALIGN_TOP
    wx.ALIGN_BOTTOM
    wx.ALIGN_CENTER_VERTICAL or wx.ALIGN_CENTRE_VERTICAL
    wx.ALIGN_CENTER_HORIZONTAL or wx.ALIGN_CENTRE_HORIZONTAL
3. Other  flags 
    wx.EXPAND 	
        The item will be expanded to fill the space assigned to the item.
    wx.SHAPED 	
        The item will be expanded as much as possible while also maintaining its aspect ratio
    wx.FIXED_MINSIZE 	
        Normally wx.Sizers will use wx.Window.GetEffectiveMinSize to determine what the minimal size of window items should be, and will use that size to calculate the layout. This allows layouts to adjust when an item changes and its best size becomes different. If you would rather have a window item stay the size it started with then use wx.FIXED_MINSIZE.
    wx.RESERVE_SPACE_EVEN_IF_HIDDEN 	
        Normally wx.Sizers don’t allocate space for hidden windows or other items. This flag overrides this behavior so that sufficient space is allocated for the window even if it isn’t visible. This makes it possible to dynamically show and hide controls without resizing parent dialog, for example.


#the alignment flags
sizer = wx.BoxSizer(wx.VERTICAL)
# Second button is right aligned
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.ALIGN_RIGHT, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

sizer = wx.BoxSizer(wx.VERTICAL)
# Second button is center-aligned
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.ALIGN_CENTER, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
#wx.EXPAND flag. This is synonymous with wx.GROW.
#first button takes its minimum size, and the second one grows to match it
sizer = wx.BoxSizer(wx.VERTICAL)
# Second button expands to the whole parent's width
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.EXPAND, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

#wx.SHAPED.
#width and height of the object stay proportional to each other. 
#It doesn’t make much sense for buttons, but can be excellent for bitmaps, 

sizer = wx.BoxSizer(wx.VERTICAL)
# Second button will scale proportionally
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 1, wx.SHAPED, 0)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
#border flags. Use the border parameter is greater than 0, 
#and describe the sides of the control on which the border should appear
sizer = wx.BoxSizer(wx.VERTICAL)
# Border size effects
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.EXPAND | wx.LEFT, 20)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
sizer = wx.BoxSizer(wx.VERTICAL)
# Border size effects
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
sizer = wx.BoxSizer(wx.VERTICAL)
# Border size effects
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
sizer = wx.BoxSizer(wx.VERTICAL)
# Border size effects
sizer.Add(wx.Button(self, -1, "An extremely long button text"), 0, 0, 0)
sizer.Add(wx.Button(self, -1, "Small Button"), 0, wx.EXPAND | wx.ALL, 20)
sizer.SetSizeHints(self)
self.SetSizer(sizer)

	
##Hiding Controls Using Sizers
#Note like any control, you can hide sizer by wx.Window.Show method. 
#or use wx.Sizer methods listed below 
#This is supported only by wx.BoxSizer and wx.FlexGridSizer.

IsShown (self, window)
    Returns True if the window(wx.Window) is shown.
IsShown (self, sizer)
    Returns True if the sizer(wx.Sizer) is shown.
IsShown (self, index)
    Returns True if the item at index is shown.
Layout(self)
    Call this to force layout of the children anew, 
    e.g. after having added a child to or removed a child (window, other sizer or space) 
    from the sizer while keeping the current dimension.
Show (self, index, show=True)
Show (self, sizer, show=True, recursive=False)
Show (self, window, show=True, recursive=False)
    Shows or hides the window/sizer/index
    To make a sizer item disappear or reappear, use Show followed by Layout .
    Use parameter recursive to show or hide elements found in subsizers.
    Returns True if the child item was found, False otherwise.
ShowItems(self, show)
    Show or hide all items managed by the sizer,show (bool)  
Fit(self, window)
    Tell the sizer to resize the window(wx.Window) 
    so that its client area matches the sizer’s minimal size 
    Returns:	The new window size.wx.Size
FitInside(self, window)
    Tell the sizer to resize the virtual size of the window to match the sizer’s minimal size.
Hide (self, index)
Hide (self, sizer, recursive=False)
Hide (self, window, recursive=False)
    Hides the child window/sizer/index
    To make a sizer item disappear, use Hide followed by Layout .
    Use parameter recursive to hide elements found in subsizers. 
    Returns True if the child item was found, False otherwise.

    
##BoxSizer
#wx.BoxSizer can lay out its children either vertically or horizontally, depending on what flag is being used in its constructor
BoxSizer(orient=HORIZONTAL)

##StaticBoxSizer
#wx.StaticBoxSixer is the same as a wx.BoxSizer, but surrounded by a static box
StaticBoxSizer(orient=HORIZONTAL)

##GridSizer
#wx.GridSizer is a two-dimensional sizer. 
#All children are given the same size, which is the minimal size required by the biggest child,
#Either the number of columns or the number or rows is fixed 
#and the grid sizer will grow in the respectively other orientation if new children are added
GridSizer(cols, vgap, hgap)
GridSizer(cols, gap=Size(0,0))
GridSizer(rows, cols, vgap, hgap)
GridSizer(rows, cols, gap)

##FlexGridSizer
#The width of each column and the height of each row are calculated individually 
#according to the minimal requirements from the respectively biggest child. 
#Additionally, columns and rows can be declared to be stretchable 
#if the sizer is assigned a size different from the one it requested. 
FlexGridSizer(cols, vgap, hgap)
FlexGridSizer(cols, gap=Size(0,0))
FlexGridSizer(rows, cols, vgap, hgap)
FlexGridSizer(rows, cols, gap)

##CreateButtonSizer
#As a convenience, wx.Dialog.CreateButtonSizer(flags) can be used 
#to create a standard button sizer in which standard buttons are displayed. 
#The following flags can be passed to this method:

wx.YES_NO     # Add Yes/No subpanel
wx.YES        # return wx.ID_YES
wx.NO         # return wx.ID_NO
wx.NO_DEFAULT # make the wx.NO button the default,
              # otherwise wx.YES or wx.OK button will be default

wx.OK         # return wx.ID_OK
wx.CANCEL     # return wx.ID_CANCEL
wx.HELP       # return wx.ID_HELP

wx.FORWARD    # return wx.ID_FORWARD
wx.BACKWARD   # return wx.ID_BACKWARD
wx.SETUP      # return wx.ID_SETUP
wx.MORE       # return wx.ID_MORE

#Example of wx.BoxSizer in a dialog 

# We want to get a dialog that is stretchable because it
# has a text ctrl at the top and two buttons at the bottom.

class MyDialog(wx.Dialog):

    def __init__(self, parent, id, title):

        wx.Dialog(parent, id, title, wx.DefaultPosition, wx.DefaultSize,
                  wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer(wx.VERTICAL)

        # create text ctrl with minimal size 100x60
        topsizer.Add(
                wx.TextCtrl(self, -1, "My text.", wx.DefaultPosition, wx.Size(100,60), wx.TE_MULTILINE),
                1,           # make vertically stretchable
                wx.EXPAND |  # make horizontally stretchable
                wx.ALL,      # and make border all around
                10)          # set border width to 10

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(
                wx.Button(self, wx.ID_OK, "OK"),
                0,           # make horizontally unstretchable
                wx.ALL,      # make border all around (implicit top alignment)
                10)          # set border width to 10
        button_sizer.Add(
                wx.Button(self, wx.ID_CANCEL, "Cancel"),
                0,           # make horizontally unstretchable
                wx.ALL,      # make border all around (implicit top alignment)
                10)          # set border width to 10

        topsizer.Add(
                button_sizer,
                0,                # make vertically unstretchable
                wx.ALIGN_CENTER)  # no border and centre horizontally

        self.SetSizerAndFit(topsizer) # use the sizer for layout and size window
                                      # accordingly and prevent it from being resized
                                      # to smaller size

#OR Use new way of specifying flags to wx.Sizer  via wx.SizerFlags. 

# We want to get a dialog that is stretchable because it
# has a text ctrl at the top and two buttons at the bottom.

class MyDialog(wx.Dialog):

    def __init__(self, parent, id, title):

        wx.Dialog(parent, id, title, wx.DefaultPosition, wx.DefaultSize,
                  wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer(wx.VERTICAL)

        # create text ctrl with minimal size 100x60
        topsizer.Add(
                wx.TextCtrl(self, -1, "My text.", wx.DefaultPosition, wx.Size(100,60), wx.TE_MULTILINE),
                wx.SizerFlags(1).Align().Expand().Border(wx.ALL, 10))

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(
                wx.Button(self, wx.ID_OK, "OK"),
                wx.SizerFlags(0).Align().Border(wx.ALL, 10))

        button_sizer.Add(
                wx.Button(self, wx.ID_CANCEL, "Cancel"),
                wx.SizerFlags(0).Align().Border(wx.ALL, 10))

        topsizer.Add(
                button_sizer,
                wx.SizerFlags(0).Center())

        self.SetSizerAndFit(topsizer) # use the sizer for layout and set size and hints



##wxpython - Window Sizing 
'Best Size'
    the best size of a widget depends on what kind of widget it is, 
    and usually also on the contents of the widget. 
    For example a wx.ListBox ‘s best size will be calculated based on how many items it has, up to a certain limit, 
    or a wx.Button ‘s best size will be calculated based on its label size, 
    but normally won’t be smaller than the platform default button size 
    (unless a style flag overrides that). 
    There is a special method in the wxPython window classes called 
    wx.Window.DoGetBestSize that a class needs to override 
    if it wants to calculate its own best size based on its content.
'Minimal Size'
    the minimal size of a widget is a size that is normally explicitly set by the programmer 
    either with the wx.Window.SetMinSize method or with the wx.Window.SetSizeHints method. 
    Most controls will also set the minimal size to the size given in the control’s constructor 
    if a non-default value is passed. 
    Top-level windows such as wx.Frame will not allow the user to resize the frame 
    below the minimal size.
'Maximum Size'
    the maximum size is normally explicitly set by the programmer 
    with the wx.Window.SetMaxSize method or with wx.Window.SetSizeHints. 
    Top-level windows such as wx.Frame will not allow the user to resize the frame 
    above the maximum size.
Size
    the size of a widget can be explicitly set or fetched 
    with the wx.Window.SetSize or wx.Window.GetSize methods. 
    This size value is the size that the widget is currently using on screen 
    and is the way to change the size of something that is not being managed by a sizer.
'Client Size'
    the client size represents the widget’s area inside of any borders belonging to the widget 
    and is the area that can be drawn upon in a wx.EVT_PAINT event. 
    If a widget doesn’t have a border then its client size is the same as its size.
'Initial Size'
    the initial size of a widget is the size given to the constructor of the widget, if any. 
    As mentioned above most controls will also set this size value as the control’s minimal size. 
    If the size passed to the constructor is the default wx.DefaultSize, 
    or if the size is not fully specified (such as wx.Size(150, -1)) 
    then most controls will fill in the missing size components using the best size 
    and will set the initial size of the control to the resulting size.
'Virtual Size'
    the virtual size is the size of the potentially viewable area of the widget. 
    The virtual size of a widget may be larger than its actual size 
    and in this case scrollbars will appear to the let the user ‘explore’ the full contents of the widget. 

##Functions related to sizing
wx.Window.GetEffectiveMinSize() :wx.Size
    returns a blending of the widget’s minimal size and best size, 
    giving precedence to the minimal size. 
    For example, if a widget’s min size is set to (150, -1) and the best size is (80, 22) 
    then the best fitting size is (150, 22). 
    If the min size is (50, 20) then the best fitting size is (50, 20). 
    This method is what is called by the sizers when determining what the requirements of each item in the sizer is, 
    and is used for calculating the overall minimum needs of the sizer.
wx.Window.SetInitialSize(ize=DefaultSize)
    this is a little different than the typical size setters. 
    Rather than just setting an 'initial size' attribute it actually 
    sets the minimal size to the value passed in, blends that value with the best size, 
    and then sets the size of the widget to be the result. 
    This method is what is called by the constructor of most controls 
    to set the minimal size and the initial size of the control.
wx.Window.Fit()
    this method sets the size of a window to fit around its children. 
    If it has no children then nothing is done, 
    if it does have children then the size of the window is set to the window’s best size.
wx.Sizer.Fit(window)
    this sets the size of the window to be large enough to accommodate the minimum size needed by the sizer, 
    (along with a few other constraints...). 
    If the sizer is the one that is assigned to the window then this should be equivalent to wx.Window.Fit.
wx.Sizer.Layout() 
    recalculates the minimum space needed by each item in the sizer, 
    and then lays out the items within the space currently allotted to the sizer.
wx.Window.Layout()
    if the window has a sizer then it sets the space given to the sizer to the current size of the window, 
    which results in a call to wx.Sizer.Layout. 
    If the window has layout constraints instead of a sizer 
    then the constraints algorithm is run. 
    The Layout() method is what is called by the default wx.EVT_SIZE handler for container windows.
wx.Window.GetAutoLayout() 	
    Returns bool
wx.Window.SetAutoLayout(autoLayout)
    autoLayout (bool) – Set this to True if you wish the Layout function to be called automatically when the window is resized.    
    
    
    
##wxpython - Closing Window 
Sequence of Events During Window Deletion
    When the user clicks on the system close button or system close command, 
    in a frame or a dialog, wxPython calls wx.Window.Close. 
    This in turn generates an wx.EVT_CLOSE event(wx.CloseEvent)
    The handler for wx.EVT_CLOSE decides whether or not to destroy the window. 
    If the application is for some reason forcing the application to close 
    ( wx.CloseEvent.CanVeto returns False), the window should always be destroyed by wx.Window.Destroy 
    otherwise there is the option to ignore the request by calling wx.CloseEvent.Veto
Closing Windows
    Use wx.Window.Close() just as the framework does, or call wx.Window.Destroy directly. 
    If using wx.Window.Close(force=True) to tell the event handler 
    thatFramework must o delete the frame and it cannot be vetoed.
    Close executes any clean-up code defined by the wx.EVT_CLOSE handler; 
Default Dialog Close Behaviour
    The default close event handler for wx.Dialog simulates a Cancel command, 
    generating a wx.ID_CANCEL event. 
    Since the handler for this cancel event might itself call Close, 
    there is a check for infinite looping. 
    The default handler for wx.ID_CANCEL hides the dialog (if modeless) 
    or calls EndModal(wx.ID_CANCEL) (if modal). 
    In other words, by default, the dialog is not destroyed.
Default Frame Close Behaviour
    The default close event handler for wx.Frame destroys the frame using Destroy().
User presses Exit From a Menu
    call wx.Window.Close on the frame. 
    This will invoke your own close event handler which may destroy the frame.
Exiting the Application Gracefully
    A wxPython application automatically exits 
    when the last top level window ( wx.Frame or wx.Dialog), is destroyed. 
    Put any application-wide cleanup code in wx.AppConsole.OnExit method 
Automatic Deletion of Child Windows
    Child windows are deleted from within the parent destructor. 
    This includes any children that are themselves frames or dialogs, 
    so you may wish to close these child frame or dialog windows explicitly 
    from within the parent close handler.
Other Kinds of Windows
    use the wx.Window.Destroy method always if required for Controls 

    
    
##wxpython - wx.Timer 
#to execute code at specified intervals.
#Its precision is platform-dependent, but in general will not be better than 1ms nor worse than 1s .

wx.Timer()
wx.Timer(owner, id=-1)

#A timer can only be used from the main thread.
1.CREATION-OPT-1.derive a new class from wx.Timer and override the wx.Timer.Notify member 
  to perform the required action.
2.CREATION-OPT-2.redirect the notifications to any wx.EvtHandler derived object(owner)
  by using the non-default constructor or wx.Timer.SetOwner(owner,id=-1). 
  Then use the EVT_TIMER bindings to connect it to the event handler 
  which will receive wx.TimerEvent notifications.
3.CREATION-OPT-3.Derive class and the EVT_TIMER bindings to connect it to an event handler 
  defined in the derived class. 
  If the default constructor is used, the timer object will be its own owner object, 
  since it is derived from wx.EvtHandler.
4.Note  .Notify(self) should be overridden by the user 
  if the default constructor was used and SetOwner wasn’t called.
5.Then start the timer with wx.Timer.Start(milliseconds=-1, oneShot=TIMER_CONTINUOUS)) 
   If oneShot is False (the default), the Notify function will be called repeatedly until the timer is stopped
   If milliseconds parameter is -1 (value by default), the previous value is used
   OR use StartOnce(self, milliseconds=-1) only for once 
   It can be stopped later with wx.Timer.Stop()
6.wx.TimerEvent object is passed to the event handler of timer events 
    #Additional class members 
    Interval 	
        Returns the interval(int) of the timer which generated this event.
    Timer 	
        Returns the timer object which generated this event.
    
#Example 

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.timer = wx.Timer(self, TIMER_ID)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)    # 1 second interval
    def OnTimer(self, event):
        # do whatever you want to do every second here
        print('Hello')

##wxpython - wx.StopWatch
#The wx.StopWatch class allows to measure time intervals.

#For example, use it to measure the time elapsed by some function:

sw = wx.StopWatch()
CallLongRunningFunction()
wx.LogMessage("The long running function took %dms to execute", sw.Time())
sw.Pause()
# stopwatch is stopped now ...
sw.Resume()
CallLongRunningFunction()
wx.LogMessage("And calling it twice took %dms in all", sw.Time())
 
 
 
##wxpython - Grid 
#https://wxpython.org/Phoenix/docs/html/wx.grid.Grid.html
#Grid and its related classes are used for displaying and editing tabular data.
#Grid supports custom attributes for the table cells, allowing to completely customize its appearance 
#and uses a separate grid table (GridTableBase -derived) class for the data management 
#hence  it can be used to display arbitrary amounts of data.

#list of classes related to Grid:
Grid: The main grid control class itself.
GridTableBase: The base class for grid data provider.
GridStringTable: Simple GridTableBase implementation supporting only string data items and storing them all in memory (hence suitable for not too large grids only).
GridCellAttr: A cell attribute, allowing to customize its appearance as well as the renderer and editor used for displaying and editing it.
GridCellAttrProvider: The object responsible for storing and retrieving the cell attributes.
GridColLabelWindow: The window showing the grid columns labels.
GridRowLabelWindow: The window showing the grid rows labels.
GridCornerLabelWindow: The window used in the upper left grid corner.
GridWindow: The window representing the main part of the grid.
GridCellRenderer: Base class for objects used to display a cell value.
GridCellStringRenderer: Renderer showing the cell as a text string.
GridCellNumberRenderer: Renderer showing the cell as an integer number.
GridCellFloatRenderer: Renderer showing the cell as a floating point number.
GridCellBoolRenderer: Renderer showing the cell as checked or unchecked box.
GridCellEditor: Base class for objects used to edit the cell value.
GridCellStringEditor: Editor for cells containing text strings.
GridCellNumberEditor: Editor for cells containing integer numbers.
GridCellFloatEditor: Editor for cells containing floating point numbers.
GridCellBoolEditor: Editor for boolean-valued cells.
GridCellChoiceEditor: Editor allowing to choose one of the predefined strings (and possibly enter new one).
GridEvent: The event sent by most of Grid actions.
GridSizeEvent: The special event sent when a grid column or row is resized.
GridRangeSelectEvent: The special event sent when a range of cells is selected in the grid.
GridEditorCreatedEvent: The special event sent when a cell editor is created.
GridSelection: The object efficiently representing the grid selection.
GridTypeRegistry: Contains information about the data types supported by the grid.


##Column and Row Sizes
#Initially all Grid rows/cols have the same height, 
#which can be modified for all of them at once using SetDefaultRowSize or  SetDefaultColSize

#Grid also allows its rows to be individually resized to have their own height 
#using SetRowSize /SetColSize
#(a row/col may be hidden entirely by setting its size to 0, or using HideRow /HideCol method). 

#It is also possible to resize a row to fit its contents with AutoSizeRow /AutoSizeCol
#or do it for all rows at once with AutoSizeRows/AutoSizeCols

#Additionally, by default the user can also drag the row separator lines to resize the rows interactively. 
#This can be forbidden by calling DisableDragRowSize/DisableDragColSize
#or just for the individual rows using DisableRowResize/DisableColResize

#it may be a good idea to save their heights/didths and restore it 
#when the grid is recreated the next time by  GetRowSizes/GetColSizes and SetRowSizes/SetColSizes 



##Example - create a grid in a frame or dialog constructor 
#and illustrates some of the formatting functions:

import wx
import wx.grid

class GridFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        # Create a wxGrid object
        #Grid(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=WANTS_CHARS, name=GridNameStr)
        grid = wx.grid.Grid(self, -1)
        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        #(numRows, numCols, selmode=GridSelectCells)
        grid.CreateGrid(100, 10)
        # We can set the sizes of individual rows and columns
        # in pixels
        #(row, height) or (col,width)
        grid.SetRowSize(0, 60)
        grid.SetColSize(0, 120)
        # And set grid cell contents as strings
        #(row, col, s)
        grid.SetCellValue(0, 0, 'wxGrid is good')
        # We can specify that some cells are read.only
        grid.SetCellValue(0, 3, 'This is read.only')
        #(ow, col, isReadOnly=True)
        grid.SetReadOnly(0, 3)
        # Colours can be specified for grid cell contents
        grid.SetCellValue(3, 3, 'green on grey')
        #(row, col, colour)
        grid.SetCellTextColour(3, 3, wx.GREEN)
        #(row, col, colour)
        grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)
        # We can specify the some cells will store numeric
        # values rather than strings. Here we set grid column 5
        # to hold floating point values displayed with width of 6
        # and precision of 2
        #(col, width=-1, precision=-1)
        grid.SetColFormatFloat(5, 6, 2)
        grid.SetCellValue(0, 6, '3.1415')
        self.Show()

if __name__ == '__main__':
    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()
    




 
##wxpython - Few global methods 
wx.CallAfter(callableObj, *args, **kw)
    Call the specified function after the current and pending event handlers have been completed. This is also good for making GUI method calls from non-GUI threads. Any extra positional or keyword args are passed on to the callable when it is called.
    Parameters:	
        callableObj (PyObject) – the callable object
        args – arguments to be passed to the callable object
        kw – keywords to be passed to the callable object
wx.ClientDisplayRect()
    Returns the dimensions of the work area on the display.
    This is the same as wx.GetClientDisplayRect but allows to retrieve the individual components instead of the entire rectangle.
    Any of the output pointers can be None if the corresponding value is not needed by the caller.
    Return type:	tuple
    Returns:	( x, y, width, height )
 wx.DirSelector(message=DirSelectorPromptStr, default_path="", style=0, pos=DefaultPosition, parent=None)
    Pops up a directory selector dialog.
    The arguments have the same meaning as those of DirDialog.__init__ . The message is displayed at the top, and the default_path, if specified, is set as the initial selection.
    The application must check for an empty return value (if the user pressed Cancel). For example:
    selector = wx.DirSelector("Choose a folder")
    if selector.strip():
        # Do something with the folder name
        print selector
 wx.DisplaySize()
    Returns the display size in pixels.
    Either of output pointers can be None if the caller is not interested in the corresponding value.
    Return type:	tuple
    Returns:	( width, height )
    
 wx.EnableTopLevelWindows(enable=True)
    This function enables or disables all top level windows.
    It is used by wx.SafeYield .
    Parameters:	enable (bool) – 
 wx.FileSelector(message, default_path="", default_filename="", default_extension="", wildcard=FileSelectorDefaultWildcardStr, flags=0, parent=None, x=DefaultCoord, y=DefaultCoord)
    Pops up a file selector box.
    In Windows, this is the common file selector dialog. In X, this is a file selector box with the same functionality. The path and filename are distinct elements of a full file pathname. If path is empty, the current directory will be used. If filename is empty, no default filename will be supplied. The wildcard determines what files are displayed in the file selector, and file extension supplies a type extension for the required filename. Flags may be a combination of wx.FD_OPEN, wx.FD_SAVE, wx.FD_OVERWRITE_PROMPT or wx.FD_FILE_MUST_EXIST.
    Both the Unix and Windows versions implement a wildcard filter. Typing a filename containing wildcards (, ?) in the filename text item, and clicking on Ok, will result in only those files matching the pattern being displayed.
    The wildcard may be a specification for multiple types of file with a description for each, such as:
    wildcard = "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif"
    The application must check for an empty return value (the user pressed Cancel). For example:
    filename = wx.FileSelector("Choose a file to open")
    if filename.strip():
        # work with the file
        print filename
    # else: cancelled by user
 wx.FileSelectorEx(message=FileSelectorPromptStr, default_path="", default_filename="", indexDefaultExtension=None, wildcard=FileSelectorDefaultWildcardStr, flags=0, parent=None, x=DefaultCoord, y=DefaultCoord)
    An extended version of FileSelector.
wx.FindMenuItemId(frame, menuString, itemString)
    Find a menu item identifier associated with the given frame’s menu bar.
    Parameters:	
        frame (wx.Frame) –
        menuString (string) –
        itemString (string) –
    Return type:	
    int
wx.FindWindowAtPoint(pt)
    Find the deepest window at the given mouse position in screen coordinates, returning the window if found, or None if not.
    This function takes child windows at the given position into account even if they are disabled. The hidden children are however skipped by it.
    Parameters:	pt (wx.Point) –
    Return type:	wx.Window
wx.FindWindowAtPointer()
    Find the deepest window at the mouse pointer position, returning the window and current pointer position in screen coordinates.
    Return type:	tuple
    Returns:	( wx.Window, pt )
wx.FindWindowById(id, parent=None)
        FindWindowById(id, parent=None) . Window
        Find the first window in the application with the given id. If parent is None, the search will start from all top-level frames and dialog boxes; if non-None, the search will be limited to the given window hierarchy. The search is recursive in both cases.
    Return type:	wx.Window
wx.FindWindowByLabel(label, parent=None)
    Find a window by its label. Depending on the type of window, the label may be a window title or panel item label. If parent is None, the search will start from all top-level frames and dialog boxes; if not None, the search will be limited to the given window hierarchy. The search is recursive in both cases.
    Parameters:	
        label (string) –
        parent (wx.Window) –
    Return type:	
    wx.Window
    Deprecated since version 4.0.1: Replaced by wx.Window.FindWindowByLabel .
wx.FindWindowByName(name, parent=None)
    Find a window by its name (as given in a window constructor or Create function call). If parent is None, the search will start from all top-level frames and dialog boxes; if not None, the search will be limited to the given window hierarchy. The search is recursive in both cases.
    If no such named window is found, wx.FindWindowByLabel is called.
    Parameters:	
        name (string) –
        parent (wx.Window) –
    Return type:	
    wx.Window
    Deprecated since version 4.0.1: Replaced by wx.Window.FindWindowByName .
wx.GetAccelFromString(label)
    Deprecated since version 4.0.1.
wx.GetActiveWindow()
    Gets the currently active window (implemented for MSW and GTK only currently, always returns None in the other ports).
    Return type:	wx.Window
wx.GetApp()
    Returns the current application object.
    Return type:	wx.PyApp
wx.GetBatteryState()
    Returns battery state as one of BATTERY_NORMAL_STATE , BATTERY_LOW_STATE , BATTERY_CRITICAL_STATE , BATTERY_SHUTDOWN_STATE or BATTERY_UNKNOWN_STATE .
        BATTERY_UNKNOWN_STATE is also the default on platforms where this feature is not implemented (currently everywhere but MS Windows).
    Return type:	wx.BatteryState
wx.GetClientDisplayRect()
    Returns the dimensions of the work area on the display.
    On Windows this means the area not covered by the taskbar, etc. Other platforms are currently defaulting to the whole display until a way is found to provide this info for all window managers, etc.
    Return type:	wx.Rect
    See also
    wx.Display
wx.GetColourFromUser(parent, colInit, caption="", data=None)
    Shows the colour selection dialog and returns the colour selected by user or invalid colour (use wx.Colour.IsOk to test whether a colour is valid) if the dialog was cancelled.
    Parameters:	
        parent (wx.Window) – The parent window for the colour selection dialog.
        colInit (wx.Colour) – If given, this will be the colour initially selected in the dialog.
        caption (string) – If given, this will be used for the dialog caption.
        data (wx.ColourData) – Optional object storing additional colour dialog settings, such as custom colours. If none is provided the same settings as the last time are used.
    Return type:	
    wx.Colour
wx.GetDisplayPPI()
    Returns the display resolution in pixels per inch.
    The x component of the returned wx.Size object contains the horizontal resolution and the y one
    Return type:	wx.Size
    New in version 2.9.0.
    See also
    wx.Display
wx.GetDisplaySize()
    Returns the display size in pixels.
    Return type:	wx.Size
    See also
    wx.Display
wx.GetDisplaySizeMM()
    Returns the display size in millimeters.
    Return type:	wx.Size
    See also
    wx.Display
wx.GetFullHostName()
    Returns the FQDN (fully qualified domain host name) or an empty string on error.
    Return type:	string
    See also
    wx.GetHostName
wx.GetHomeDir()
    Return the (current) user’s home directory.
    Return type:	string
    See also
    wx.GetUserHome , wx.StandardPaths
wx.GetHostName()
    Copies the current host machine’s name into the supplied buffer.
    Please note that the returned name is not fully qualified, i.e. it does not include the domain name.
    Under Windows or NT, this function first looks in the environment variable SYSTEM_NAME; if this is not found, the entry HostName in the wxWidgets section of the WIN.INI file is tried.
    Return type:	string
    Returns:	The hostname if successful or an empty string otherwise.
    See also
    wx.GetFullHostName
wx.GetKeyState(key)
    For normal keys, returns True if the specified key is currently down.
    For togglable keys (Caps Lock, Num Lock and Scroll Lock), returns True if the key is toggled such that its LED indicator is lit. There is currently no way to test whether togglable keys are up or down.
    Even though there are virtual key codes defined for mouse buttons, they cannot be used with this function currently.
    In wxGTK, this function can be only used with modifier keys ( WXK_ALT , WXK_CONTROL and WXK_SHIFT ) when not using X11 backend currently.
    Parameters:	key (KeyCode) –
    Return type:	bool
wx.GetLocale()
    Get the current locale object (note that it may be None!)
    Return type:	wx.Locale
wx.GetMousePosition()
    Returns the mouse position in screen coordinates.
    Return type:	wx.Point
wx.GetMouseState()
    Returns the current state of the mouse.
    Returns a wx.MouseState instance that contains the current position of the mouse pointer in screen coordinates, as well as boolean values indicating the up/down status of the mouse buttons and the modifier keys.
    Return type:	wx.MouseState
wx.GetNumberFromUser(message, prompt, caption, value, min=0, max=100, parent=None, pos=DefaultPosition)
    Shows a dialog asking the user for numeric input.
    The dialogs title is set to caption , it contains a (possibly) multiline message above the single line prompt and the zone for entering the number.
    The number entered must be in the range min to max (both of which should be positive) and value is the initial value of it. If the user enters an invalid value, it is forced to fall into the specified range. If the user cancels the dialog, the function returns -1.
    Dialog is centered on its parent unless an explicit position is given in pos .
    Parameters:	
        message (string) –
        prompt (string) –
        caption (string) –
        value (long) –
        min (long) –
        max (long) –
        parent (wx.Window) –
        pos (wx.Point) –
    Return type:	
    long
wx.GetOsDescription()
    Returns the string containing the description of the current platform in a user-readable form.
    For example, this function may return strings like 'Windows NT Version 4.0' or 'Linux 2.2.2 i386'.
    Return type:	string
    See also
    wx.GetOsVersion
wx.GetOsVersion()
    Gets the version and the operating system ID for currently running OS.
    The returned OperatingSystemId value can be used for a basic categorization of the OS family; the major and minor version numbers allows to detect a specific system.
    For Unix-like systems ( OS_UNIX ) the major and minor version integers will contain the kernel major and minor version numbers (as returned by the ‘uname -r’ command); e.g. '2' and '6' if the machine is using kernel 2.6.19.
    For Mac OS X systems ( OS_MAC ) the major and minor version integers are the natural version numbers associated with the OS; e.g. '10' and '6' if the machine is using Mac OS X Snow Leopard.
    For Windows-like systems ( OS_WINDOWS ) the major and minor version integers will contain the following values:
    Windows OS name 	Major version 	Minor version
    Windows 7 	6 	1
    Windows Server 2008 R2 	6 	1
    Windows Server 2008 	6 	0
    Windows Vista 	6 	0
    Windows Server 2003 R2 	5 	2
    Windows Server 2003 	5 	2
    Windows XP 	5 	1
    Windows 2000 	5 	0
    See the`MSDN <http://msdn.microsoft.com/en-us/library/ms724832(VS.85).aspx>`_ for more info about the values above.
    Return type:	tuple
    Returns:	( wx.OperatingSystemId, major, minor )
    See also
    wx.GetOsDescription , PlatformInfo
wx.GetPasswordFromUser(message, caption=GetPasswordFromUserPromptStr, default_value="", parent=None, x=DefaultCoord, y=DefaultCoord, centre=True)
    Similar to wx.GetTextFromUser but the text entered in the dialog is not shown on screen but replaced with stars.
    This is intended to be used for entering passwords as the function name implies.
    Parameters:	
        message (string) –
        caption (string) –
        default_value (string) –
        parent (wx.Window) –
        x (int) –
        y (int) –
        centre (bool) –
    Return type:	
    string
wx.GetSingleChoice(*args, **kw)
    overload Overloaded Implementations:
    GetSingleChoice (message, caption, aChoices, parent=None, x=DefaultCoord, y=DefaultCoord, centre=True, width=CHOICE_WIDTH, height=CHOICE_HEIGHT, initialSelection=0)
    Pops up a dialog box containing a message, OK/Cancel buttons and a single-selection listbox.
    The user may choose an item and press wx.OK to return a string or Cancel to return the empty string. Use wx.GetSingleChoiceIndex if empty string is a valid choice and if you want to be able to detect pressing Cancel reliably.
    You may pass the list of strings to choose from either using choices which is an array of n strings for the listbox or by using a single aChoices parameter of type list of strings .
    If centre is True, the message text (which may include new line characters) is centred; if False, the message is left-justified.
    GetSingleChoice (message, caption, choices, initialSelection, parent=None)
    Parameters:	
        message (string) –
        caption (string) –
        choices (list of strings) –
        initialSelection (int) –
        parent (wx.Window) –
    Return type:	
    string
wx.GetStockLabel(id, flags=STOCK_WITH_MNEMONIC)
    Returns label that should be used for given id element.
    Parameters:	
        id (wx.WindowID) – Given id of the wx.MenuItem, wx.Button, wx.ToolBar tool, etc.
        flags (long) – Combination of the elements of StockLabelQueryFlag.
    Return type:	
    string
wx.GetTextFromUser(message, caption=GetTextFromUserPromptStr, default_value="", parent=None, x=DefaultCoord, y=DefaultCoord, centre=True)
    Pop up a dialog box with title set to caption, message , and a default_value .
    The user may type in text and press wx.OK to return this text, or press Cancel to return the empty string.
    If centre is True, the message text (which may include new line characters) is centred; if False, the message is left-justified.
    This function is a wrapper around wx.TextEntryDialog and while it is usually more convenient to use, using the dialog directly is more flexible, e.g. it allows you to specify the TE_MULTILINE to allow the user enter multiple lines of text while this function is limited to single line entry only.
    Parameters:	
        message (string) –
        caption (string) –
        default_value (string) –
        parent (wx.Window) –
        x (int) –
        y (int) –
        centre (bool) –
    Return type:	
    string
wx.GetTopLevelParent(window)
    Returns the first top level parent of the given window, or in other words, the frame or dialog containing it, or None.
    Parameters:	window (wx.Window) –
    Return type:	wx.Window
wx.GetTopLevelWindows()
    Returns a list-like object of the the application’s top-level windows, (frames,dialogs, etc.)
    Return type:	WindowList
wx.GetUserHome(user="")
    Returns the home directory for the given user.
    If the user is empty (default value), this function behaves like wx.GetHomeDir (i.e. returns the current user home directory).
    If the home directory couldn’t be determined, an empty string is returned.
    Parameters:	user (string) –
    Return type:	string
wx.GetUserId()
    This function returns the 'user id' also known as 'login name' under Unix (i.e.
    something like 'jsmith'). It uniquely identifies the current user (on this system). Under Windows or NT, this function first looks in the environment variables USER and LOGNAME; if neither of these is found, the entry UserId in the wxWidgets section of the WIN.INI file is tried.
    Return type:	string
    Returns:	The login name if successful or an empty string otherwise.
wx.IntersectRect(r1, r2)
        Calculate and return the intersection of r1 and r2. Returns None if there is no intersection.
    Return type:	PyObject
wx.IsBusy()
    Returns True if between two wx.BeginBusyCursor and wx.EndBusyCursor calls.
 wx.IsMainThread()
    Returns True if the current thread is what considers the GUI thread.
    Return type:	bool
wx.LoadFileSelector(what, extension, default_name="", parent=None)
    Ask for filename to load.
    Parameters:	
        what (string) –
        extension (string) –
        default_name (string) –
        parent (wx.Window) –
    Return type:	
    string
wx.LogDebug(message)
    The right functions for debug output.
    They only do something in debug mode (when the preprocessor symbol WXDEBUG is defined) and expand to nothing in release mode (otherwise).
    Parameters:	message (String) –
wx.LogError(message)
    The functions to use for error messages, i.e.
    the messages that must be shown to the user. The default processing is to pop up a message box to inform the user about it.
    Parameters:	message (String) –
wx.LogFatalError(message)
    Like wx.LogError , but also terminates the program with the exit code 3.
    Using abort() standard function also terminates the program with this exit code.
    Parameters:	message (String) –
wx.LogGeneric(level, message)
    Logs a message with the given LogLevel.
    E.g. using LOG_Message as first argument, this function behaves like wx.LogMessage .
    Parameters:	
        level (wx.LogLevel) –
        message (String) –
wx.LogMessage(message)
    For all normal, informational messages.
    They also appear in a message box by default (but it can be changed).
    Parameters:	message (String) –
wx.LogStatus(*args, **kw)
    overload Overloaded Implementations:
    LogStatus (frame, message)
    Messages logged by this function will appear in the statusbar of the frame or of the top level application window by default (i.e.
    when using the second version of the functions).
    If the target frame doesn’t have a statusbar, the message will be lost.
    Parameters:	
        frame (wx.Frame) –
        message (String) –
    LogStatus (message)
    Parameters:	message (String) –
wx.LogSysError(message)
    Mostly used by wxWidgets itself, but might be handy for logging errors after system call (API function) failure.
    It logs the specified message text as well as the last system error code (errno or GetLastError() depending on the platform) and the corresponding error message. The second form of this function takes the error code explicitly as the first argument.
    Parameters:	message (String) –
    See also
    wx.SysErrorCode , wx.SysErrorMsg
wx.LogVerbose(message)
    For verbose output.
    Normally, it is suppressed, but might be activated if the user wishes to know more details about the program progress (another, but possibly confusing name for the same function could be LogInfo ).
    Parameters:	message (String) –
wx.LogWarning(message)
    For warnings - they are also normally shown to the user, but don’t interrupt the program work.
    Parameters:	message (String) –
wx.MacThemeColour(themeBrushID)
    Return type:	wx.Colour
wx.MessageBox(message, caption=MessageBoxCaptionStr, style=OK|CENTRE, parent=None, x=DefaultCoord, y=DefaultCoord)
    Show a general purpose message dialog.
    This is a convenient function which is usually used instead of using wx.MessageDialog directly. Notice however that some of the features, such as extended text and custom labels for the message box buttons, are not provided by this function but only by wx.MessageDialog.
    The return value is one of: YES , NO , CANCEL , OK or HELP (notice that this return value is different from the return value of wx.MessageDialog.ShowModal ).
    For example:
    answer = wx.MessageBox("Quit program?", "Confirm",
                           wx.YES_NO | wx.CANCEL, main_frame)
    if answer == wx.YES:
        main_frame.Close()
    message may contain newline characters, in which case the message will be split into separate lines, to cater for large messages.
    Parameters:	
        message (string) – Message to show in the dialog.
        caption (string) – The dialog title.
        style (int) – Combination of style flags described in wx.MessageDialog documentation.
        parent (wx.Window) – Parent window.
        x (int) – Horizontal dialog position (ignored under MSW). Use wx.DefaultCoord for x and y to let the system position the window.
        y (int) – Vertical dialog position (ignored under MSW).
    Return type:	
    int
wx.MicroSleep(microseconds)
    Sleeps for the specified number of microseconds.
    The microsecond resolution may not, in fact, be available on all platforms (currently only Unix platforms with nanosleep(2) may provide it) in which case this is the same as calling wx.MilliSleep with the argument of microseconds/1000.
    Parameters:	microseconds (long) –
wx.MilliSleep(milliseconds)
    Sleeps for the specified number of milliseconds.
    Notice that usage of this function is encouraged instead of calling usleep(3) directly because the standard usleep() function is not MT safe.
    Parameters:	milliseconds (long) –
wx.NewEventType()
    Generates a new unique event type.
    Usually this function is only used by DEFINE_EVENT and not called directly.
    Return type:	wx.EventType
wx.NewId()
    Generates an integer identifier unique to this run of the program.
    Return type:	int
    Deprecated since version 4.0.1: Ids generated by it can conflict with the Ids defined by the user code, use ID_ANY to assign ids which are guaranteed to not conflict with the user-defined ids for the controls and menu items you create instead of using this function.
wx.Now()
    Returns a string representing the current date and time.
    Return type:	string
wx.PostEvent(dest, event)
    In a GUI application, this function posts event to the specified dest object using wx.EvtHandler.AddPendingEvent .
    Otherwise, it dispatches event immediately using wx.EvtHandler.ProcessEvent . See the respective documentation for details (and caveats). Because of limitation of wx.EvtHandler.AddPendingEvent this function is not thread-safe for event objects having String fields, use wx.QueueEvent instead.
    Parameters:	
        dest (wx.EvtHandler) –
        event (wx.Event) –
wx.pydate2wxdate(date)
    Convert a Python date or datetime to a DateTime object
wx.QueueEvent(dest, event)
    Queue an event for processing on the given object.
    This is a wrapper around wx.EvtHandler.QueueEvent , see its documentation for more details.
    Parameters:	
        dest (wx.EvtHandler) – The object to queue the event on, can’t be NULL .
        event (wx.Event) – The heap-allocated and non- NULL event to queue, the function takes ownership of it.
wx.RegisterId(id)
    Ensures that Ids subsequently generated by wx.NewId do not clash with the given id.
    Parameters:	id (int) –
wx.SafeShowMessage(title, text)
    This function shows a message to the user in a safe way and should be safe to call even before the application has been initialized or if it is currently in some other strange state (for example, about to crash).
    Under Windows this function shows a message box using a native dialog instead of wx.MessageBox (which might be unsafe to call), elsewhere it simply prints the message to the standard output using the title as prefix.
    Parameters:	
        title (string) – The title of the message box shown to the user or the prefix of the message string.
        text (string) – The text to show to the user.
    See also
    wx.LogFatalError
wx.SafeYield(win=None, onlyIfNeeded=False)
    Calls wx.App.SafeYield .
    Parameters:	
        win (wx.Window) –
        onlyIfNeeded (bool) –
    Return type:	
    bool
wx.SaveFileSelector(what, extension, default_name="", parent=None)
    Ask for filename to save.
    Parameters:	
        what (string) –
        extension (string) –
        default_name (string) –
        parent (wx.Window) –
    Return type:	
    string
wx.SetCursor(cursor)
    Globally sets the cursor; only has an effect on Windows, Mac and GTK+.
    You should call this function with NullCursor to restore the system cursor.
    Parameters:	cursor (wx.Cursor) –
    See also
    wx.Cursor, wx.Window.SetCursor
wx.Shell(command="")
    Executes a command in an interactive shell window.
    If no command is specified, then just the shell is spawned.
    Parameters:	command (string) –
    Return type:	bool
    See also
    wx.Execute , External Program Execution Sample
wx.Shutdown(flags=SHUTDOWN_POWEROFF)
    This function shuts down or reboots the computer depending on the value of the flags.
    Parameters:	flags (int) – One of SHUTDOWN_POWEROFF , SHUTDOWN_REBOOT or SHUTDOWN_LOGOFF (currently implemented only for MSW) possibly combined with SHUTDOWN_FORCE which forces shutdown under MSW by forcefully terminating all the applications. As doing this can result in a data loss, this flag shouldn’t be used unless really necessary.
    Return type:	bool
    Returns:	True on success, False if an error occurred.
    Note
    Note that performing the shutdown requires the corresponding access rights (superuser under Unix, SE_SHUTDOWN privilege under Windows NT) and that this function is only implemented under Unix and MSW.
wx.Sleep(secs)
    Sleeps for the specified number of seconds.
    Parameters:	secs (int) –
wx.StripMenuCodes(str, flags=Strip_All)
    Strips any menu codes from str and returns the result.
    By default, the functions strips both the mnemonics character ( '&' ) which is used to indicate a keyboard shortkey, and the accelerators, which are used only in the menu items and are separated from the main text by the \t (TAB) character. By using flags of Strip_Mnemonics or Strip_Accel to strip only the former or the latter part, respectively.
    Notice that in most cases wx.MenuItem.GetLabelFromText or wx.Control.GetLabelText can be used instead.
    Parameters:	
        str (string) –
        flags (int) –
    Return type:	
    string
wx.SysErrorCode()
    Returns the error code from the last system call.
    This function uses errno on Unix platforms and GetLastError under Win32.
    Return type:	int
    See also
    wx.SysErrorMsg , wx.LogSysError
wx.SysErrorMsg(errCode=0)
    Returns the error message corresponding to the given system error code.
    If errCode is 0 (default), the last error code (as returned by wx.SysErrorCode ) is used.
    Parameters:	errCode (long) –
    Return type:	string
    See also
    wx.SysErrorCode , wx.LogSysError
wx.Trap()
    Generate a debugger exception meaning that the control is passed to the debugger if one is attached to the process.
    Otherwise the program just terminates abnormally.
    If DEBUG_LEVEL is 0 (which is not the default) this function does nothing.
wx.Usleep(milliseconds)
    Sleeps for the specified number of milliseconds.
    Parameters:	milliseconds (long) –
    Deprecated since version 4.0.1: This function is deprecated because its name is misleading: notice that the argument is in milliseconds, not microseconds. Please use either wx.MilliSleep or wx.MicroSleep depending on the resolution you need.
wx.version()
    Returns a string containing version and port info
wx.WakeUpIdle()
    This function wakes up the (internal and platform dependent) idle system, i.e.
    it will force the system to send an idle event even if the system currently is idle and thus would not send any idle event until after some other event would get sent. This is also useful for sending events between two threads and is used by the corresponding functions wx.PostEvent and wx.EvtHandler.AddPendingEvent .
wx.Yield()
    Calls wx.AppConsole.Yield .
    Return type:	bool
    Deprecated since version 4.0.1: This function is kept only for backwards compatibility. Please use the wx.AppConsole.Yield method instead in any new code.
wx.YieldIfNeeded()
    Convenience function for wx.GetApp().Yield(True)


##wxpython - Thread

#Worker thread must not update GUI, should only use below threadsafe Methods
wx.PostEvent(dest, event)
    In a GUI application, this function posts event(wx.Event) to the specified dest(wx.EvtHandler) object 
    using wx.EvtHandler.AddPendingEvent .
    OR dispatches event immediately using wx.EvtHandler.ProcessEvent 
wx.CallAfter(callableObj, *args, **kw)
    Call the specified function after the current and pending event handlers have been completed. 
    This is also good for making GUI method calls from non-GUI threads. 
    Any extra positional or keyword args are passed on to the callable when it is called.
wx.CallLater(millis, callableObj, *args, **kwargs)
    A convenience class for wx.Timer, that calls the given callable object once 
    after the given amount of milliseconds, passing any positional or keyword args. 
    The return value of the callable is available after it has been run with the GetResult() 
        GetResult(self)
            Returns the value of the callable.
        HasRun(self)
            Returns whether or not the callable has run.
        Start(self, millis=None, *args, **kwargs)
            (Re)start the timer
            
##creation of New event    
wx.lib.newevent
    1st element is Event class (derived from wx.Event)
    2nd element binder is event type (EVT_*) 
    #Example 
        Attach arbitrary data to the event during its creation
        #create the event
        evt = SomeNewEvent(attr1="hello", attr2=654)
        #post the event
        wx.PostEvent(target, evt)
        #bind 
        self.Bind(binder, self.handler)
        #handler can access those data 
        def handler(self, evt):
            # given the above constructed event, the following is true
            #evt.attr1 == "hello"
            #evt.attr2 == 654
    NewCommandEvent() 	
        Generates a new (command_event, binder) tuple.
    NewEvent() 	
        Generates a new (event, binder) tuple.
    
#Example of wx.PostEvent 
import wx
import time
import threading

import wx.lib.newevent as NE

MooEvent, EVT_MOO = NE.NewEvent()
GooEvent, EVT_GOO = NE.NewCommandEvent()

DELAY = 0.7

def evt_thr(win):
    time.sleep(DELAY)
    wx.PostEvent(win, MooEvent(moo=1))

def cmd_thr(win, id):
    time.sleep(DELAY)
    wx.PostEvent(win, GooEvent(id, goo=id))

ID_CMD1 = wx.NewId()
ID_CMD2 = wx.NewId()

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "MOO")
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.Bind(EVT_MOO, self.on_moo)
        b = wx.Button(self, -1, "Generate MOO")
        sizer.Add(b, 1, wx.EXPAND)
        b.Bind(wx.EVT_BUTTON, self.on_evt_click)
        b = wx.Button(self, ID_CMD1, "Generate GOO with %d" % ID_CMD1)
        sizer.Add(b, 1, wx.EXPAND)
        b.Bind(wx.EVT_BUTTON, self.on_cmd_click)
        b = wx.Button(self, ID_CMD2, "Generate GOO with %d" % ID_CMD2)
        sizer.Add(b, 1, wx.EXPAND)
        b.Bind(wx.EVT_BUTTON, self.on_cmd_click)

        self.Bind(EVT_GOO, self.on_cmd1, id=ID_CMD1)
        self.Bind(EVT_GOO, self.on_cmd2, id=ID_CMD2)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

    def on_evt_click(self, e):
        t = threading.Thread(target=evt_thr, args=(self, ))
        t.setDaemon(True)
        t.start()

    def on_cmd_click(self, e):
        t = threading.Thread(target=cmd_thr, args=(self, e.GetId()))
        t.setDaemon(True)
        t.start()

    def show(self, msg, title):
        dlg = wx.MessageDialog(self, msg, title, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def on_moo(self, e):
        self.show("MOO = %s" % e.moo, "Got Moo")

    def on_cmd1(self, e):
        self.show("goo = %s" % e.goo, "Got Goo (cmd1)")

    def on_cmd2(self, e):
        self.show("goo = %s" % e.goo, "Got Goo (cmd2)")


app = wx.App(0)
f = Frame()
f.Show(True)
app.MainLoop()

#Example of wx.CallAfter
import wx
import functools
import threading
import subprocess
import time

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None, -1, 'Threading Example')
        # add some buttons and a text control
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(3):
            name = 'Button %d' % (i+1)
            button = wx.Button(panel, -1, name)
            func = functools.partial(self.on_button, button=name)
            button.Bind(wx.EVT_BUTTON, func)
            sizer.Add(button, 0, wx.ALL, 5)
        text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text = text
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)
    def on_button(self, event, button):
        # create a new thread when a button is pressed
        thread = threading.Thread(target=self.run, args=(button,))
        thread.setDaemon(True)
        thread.start()
    def on_text(self, text):
        self.text.AppendText(text)
    def run(self, button):
        cmd = ['ls', '-lta']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            wx.CallAfter(self.on_text, line)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame()
    frame.Show()
    app.MainLoop()

    
    
##wxPython, Threading, wx.CallAfter and PubSub
$ pip install Pypubsub
#provides a publish-subscribe broker that allows parts of your application to broadcast messages of a given topic to other parts of the application

Message Topic:
    a. Every message is specific to a “topic”, defined as a string name; 
    b. Topics form a hierarchy. A parent topic is more generic than a child topic.
Message Data: any keyword arguments used by the sender, pub.sendMessage(topic, **data);
    A topic may have no associated message data, or may have any mixture of required and optional data; 
    this is known as its Message Data Specification (MDS);
    The MDS of a child topic cannot be more restrictive than that of a parent topic;
    Once the MDS is set for a topic, it never changes during the runtime of an application.




#Example using API version 1

from wx.lib.pubsub import Publisher as pub

class SomeReceiver(object):
  def __init__(self):
    # here we connect to a signal called 'object.added'
    # we use dotted notation for more specialized topics
    # but you can use tuples too
    pub.subscribe(self.__onObjectAdded, 'object.added')

  def __onObjectAdded(self, message):
    # data passed with your message is put in message.data.
    # Any object can be passed to subscribers this way.
    print('Object', message.data, 'is added)'

# usage;
a = SomeReceiver()
#sendMessage calls may be placed anywhere,
pub.sendMessage('object.added', 'HELLO WORLD')


# topic can be a tuple instead of a 'dotted' string:
pub.subscribe(self.__onObjectAdded, ('object', 'added'))

# use Publisher directly
from wx.lib.pubsub import Publisher
Publisher().sendMessage(('object', 'added'), 'HELLO WORLD')


#The New PubSub: version 3
#requires keyworded arguments for message data, making the code more explicit 

# first line below is necessary only in wxPython 2.8.11.0 since default 
# API in this wxPython is pubsub version 1 (expect later versions 
# of wxPython to use the kwargs API by default)
from wx.lib.pubsub import setupkwargs

# regular pubsub import
from wx.lib.pubsub import pub

class SomeReceiver(object):
  def __init__(self):
    pub.subscribe(self.__onObjectAdded, 'object.added')

  def __onObjectAdded(self, data, extra1, extra2=None):
    # no longer need to access data through message.data.
    print('Object', repr(data), 'is added')
    print(extra1)
    if extra2:
        print(extra2)


a = SomeReceiver()
pub.sendMessage('object.added', data=42, extra1='hello!')
pub.sendMessage('object.added', data=42, extra1='hello!', extra2=[2, 3, 5, 7, 11, 13, 17, 19, 23])

  
##With Threading 

import time
import wx
 
from threading import Thread
from wx.lib.pubsub import pub
 
class TestThread(Thread):
    """Test Worker Thread Class.""" 
    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(6):
            time.sleep(10)
            wx.CallAfter(self.postTime, i)
        time.sleep(5)
        wx.CallAfter(pub.sendMessage, "update", data="Thread finished!")
 
    #----------------------------------------------------------------------
    def postTime(self, amt):
        """
        Send time to GUI
        """
        amtOfTime = (amt + 1) * 10
        pub.sendMessage("update", data=amtOfTime)
 
class MyForm(wx.Frame): 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial") 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started goes here")
        self.btn = btn = wx.Button(panel, label="Start Thread") 
        #bindings 
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        #Layouting 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer) 
        # create a pubsub receiver
        pub.subscribe(self.updateDisplay, "update") 
    #----------------------------------------------------------------------
    def onButton(self, event):
        """
        Runs the thread
        """
        TestThread()
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        btn.Disable() 
    #----------------------------------------------------------------------
    def updateDisplay(self, data):
        """
        Receives data from thread and updates the display
        """
        t = data
        if isinstance(t, int):
            self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
        else:
            self.displayLbl.SetLabel("%s" % t)
            self.btn.Enable()
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()

##LongRunning Task and Thread 
import time
from threading import *
import wx

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

# Thread class that executes processing
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()

    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        for i in range(10):
            time.sleep(1)
            if self._want_abort:
                # Use a result of None to acknowledge the abort (of
                # course you can use whatever you'd like or even
                # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        wx.PostEvent(self._notify_window, ResultEvent(10))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1

# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'Thread Test')

        # Dumb sample frame with two buttons
        wx.Button(self, ID_START, 'Start', pos=(0,0))
        wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
        self.status = wx.StaticText(self, -1, '', pos=(0,100))

        self.Bind(wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.Bind(wx.EVT_BUTTON, self.OnStop, id=ID_STOP)

        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)

        # And indicate we don't have a worker thread yet
        self.worker = None

    def OnStart(self, event):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        if not self.worker:
            self.status.SetLabel('Starting computation')
            self.worker = WorkerThread(self)

    def OnStop(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker:
            self.status.SetLabel('Trying to abort computation')
            self.worker.abort()

    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.status.SetLabel('Computation aborted')
        else:
            # Process results here
            self.status.SetLabel('Computation Result: %s' % event.data)
        # In either event, the worker is done
        self.worker = None

class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
    
    
##LongRunning Task  and wxYield
#add a call to wxYield() somewhere within the computation code such that it executes periodically. 
#At that point, any pending window events will be dispatched (permitting the window to refresh, process button presses, etc...). 


import time
import wx

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()


class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'wxYield Test')

        # Dumb sample frame with two buttons
        wx.Button(self, ID_START, 'Start', pos=(0,0))
        wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
        self.status = wx.StaticText(self, -1, '', pos=(0,100))

        self.Bind (wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.Bind (wx.EVT_BUTTON, self.OnStop, id=ID_STOP)

        # Indicate we aren't working on it yet
        self.working = 0

    #long running task 
    def OnStart(self, event):
        """Start Computation."""
        # Start the processing - this simulates a loop - you need to call
        # wx.Yield at some periodic interval.
        if not self.working:
            self.status.SetLabel('Starting Computation')
            self.working = 1
            self.need_abort = 0

            for i in range(10):
                time.sleep(1)
                wx.Yield()
                if self.need_abort:
                    self.status.SetLabel('Computation aborted')
                    break
            else:
                # Here's where you would process the result
                # Note you should only do this if not aborted.
                self.status.SetLabel('Computation Completed')

            # In either event, we aren't running any more
            self.working = 0

    def OnStop(self, event):
        """Stop Computation."""
        if self.working:
            self.status.SetLabel('Trying to abort computation')
            self.need_abort = 1

class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None,-1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
    
    
##LongRunning Task  and idle handler
#do your work within an idle handler. 
#let wxPython generate an IDLE event whenever it has completed processing normal user events, 
#and then you perform a "chunk" of your processing in each such case. 


import time
import wx

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# GUI Frame class that spins off the worker thread
class MainFrame(wx.Frame):
    """Class MainFrame."""
    def __init__(self, parent, id):
        """Create the MainFrame."""
        wx.Frame.__init__(self, parent, id, 'Idle Test')

        # Dumb sample frame with two buttons
        wx.Button(self, ID_START, 'Start',p os=(0,0))
        wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
        self.status = wx.StaticText(self, -1, '', pos=(0,100))

        self.Bind (wx.EVT_BUTTON, self.OnStart, id=ID_START)
        self.Bind (wx.EVT_BUTTON, self.OnStop, id=ID_STOP)
        self.Bind (wx.EVT_IDLE, self.OnIdle)

        # Indicate we aren't working on it yet
        self.working = 0

    def OnStart(self, event):
        """Start Computation."""
        # Set up for processing and trigger idle event
        if not self.working:
            self.status.SetLabel('Starting Computation')
            self.count = 0
            self.working = 1
            self.need_abort = 0

    def OnIdle(self, event):
        """Idle Handler."""
        if self.working:
            # This is where the processing takes place, one bit at a time
            if self.need_abort:
                self.status.SetLabel('Computation aborted')
            else:
                self.count = self.count + 1
                time.sleep(1)
                if self.count < 10:
                    # Still more work to do so request another event
                    event.RequestMore()
                    return
                else:
                    self.status.SetLabel('Computation completed')

            # Reaching here is an abort or completion - end in either case
            self.working = 0

    def OnStop(self, event):
        """Stop Computation."""
        if self.working:
            self.status.SetLabel('Trying to abort computation')
            self.need_abort = 1

class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()

    
    
##Handling recursive tasks via Thread 

import  threading

# This is a global flag that we will manipulate as needed
# to allow graceful exit from the recursive search.
KeepRunning     =       threading.Event()


class   Worker(threading.Thread):
  def __init__ (self, op, dir1, dir2):
  threading.Thread.__init__(self)
  self.op   = op
  self.Dir1 = dir1
  self.Dir2 = dir2
  KeepRunning.set()

  self.start()

  def run(self):
    self.wb = WorkerBee(self.op, self.Dir1, self.Dir2)
    self.op.AppendText('Done!\n')
    wxBell()

    # Assuming you are following the above example somewhat, assume that this is a
    # similar 'reporting' event class that we are calling. It carries a cargo which
    # is in fact the 'head' WorkerBee.
    wxPostEvent(self.op.GetParent(), NewReport(self.wb))

  def abort(self):
    KeepRunning.clear()

  # print to the output window.
  def Update(self, txt):
    self.op.AppendText(txt)
    self.op.ShowPosition(self.op.GetLastPosition()) # keeps the last line visible
    
 class WorkerBee:
  def __init__ (self, op, dir1, dir2):
    self.DiffList = []  # We will retain a list of changed files
    self.DirList  = []  # We will retain a list of directories.
    self.A        = dir1
    self.B        = dir2
    self.op       = op

    self.Update('scanning %s\n' % self.A)

    self.cmp = filecmp.dircmp(self.A, self.B)
                
    self.Deleted = self.cmp.left_only
    self.New     = self.cmp.right_only
    self.Files   = self.cmp.common_files
    self.Dirs    = self.cmp.common_dirs

    for i in self.Files :
     if not KeepRunning.isSet(): break  

       self.Update('\t%s\\%s' %(self.A,i)) 

       if filecmp.cmp('%s\\%s' % (self.A, i), '%s\\%s' % (self.B, i), shallow=0) == 0 :
         self.Update('\t<---- DIFF ***\n')      # A diff!
         self.DiffList.append(i)
       else:
         self.Update('\n')

    for i in self.Dirs  :
      if not KeepRunning.isSet(): break 

      self.DirList.append ( WorkerBee ( op,
                                        '%s\\%s' % (self.A, i), 
                                        '%s\\%s' % (self.B, i)
                                      )
                          )

  def   Update(self, txt):
    self.op.AppendText(txt)
    self.op.ShowPosition(self.op.GetLastPosition())
    
 
 
 
##wxpython - wx.Bitmap
#This class encapsulates the concept of a platform-dependent bitmap, 
#either monochrome or colour or colour with alpha channel support.
#Note that many wx.Bitmap functions take a type parameter
1.wxMSW supports BMP and ICO files, BMP and ICO resources;
2.wxGTK supports any file supported by gdk-pixbuf;
3.Mac supports PICT resources;
4.X11 supports XPM files, XPM data, XBM data;

#wx.Bitmap can load and save all formats that wx.Image can
#Methods Summary
__init__ 	Default constructor.
ConvertToDisabled 	Returns disabled (dimmed) version of the bitmap.
ConvertToImage 	Creates an image from a platform-dependent bitmap.
CopyFromBuffer 	Copy data from a buffer object to replace the bitmap pixel data.
CopyFromIcon 	Creates the bitmap from an icon.
CopyToBuffer 	Copy pixel data to a buffer object. See CopyFromBuffer for buffer
Create 	        Creates a fresh bitmap.
FromBuffer 	    Creates a wx.Bitmap from in-memory data. The data parameter
FromBufferAndAlpha 	Creates a wx.Bitmap from in-memory data. The data and alpha
FromBufferRGBA 	Creates a wx.Bitmap from in-memory data. The data parameter
FromRGBA 	    Creates a new empty 32-bit wx.Bitmap where every pixel has been
GetDepth 	    Gets the colour depth of the bitmap.
GetHandle 	    MSW-only method to fetch the windows handle for the bitmap.
GetHeight 	    Gets the height of the bitmap in pixels.
GetMask 	    Gets the associated mask (if any) which may have been loaded from a file or set for the bitmap.
GetPalette 	    Gets the associated palette (if any) which may have been loaded from a file or set for the bitmap.
GetSize 	    Returns the size of the bitmap in pixels.
GetSubBitmap 	Returns a sub bitmap of the current one as long as the rect belongs entirely to the bitmap.
GetWidth 	    Gets the width of the bitmap in pixels.
IsOk 	        Returns True if bitmap data is present.
LoadFile 	    Loads a bitmap from a file or resource.
NewFromPNGData 	Loads a bitmap from the memory containing image data in PNG format.
SaveFile 	    Saves a bitmap in the named file.
SetDepth 	    Sets the depth member (does not affect the bitmap data).
SetHandle 	    MSW-only method to set the windows handle for the bitmap.
SetHeight 	    Sets the height member (does not affect the bitmap data).
SetMask 	    Sets the mask for this bitmap.
SetMaskColour 	 
SetPalette 	    Sets the associated palette.
SetSize 	    Set the bitmap size (does not alter the existing native bitmap data or image size).
SetWidth 	    Sets the width member (does not affect the bitmap data).
 
#Properties Summary
#Use Get*/Set* methods to access
Depth 	
Handle 	
Height 	
Mask 	
Palette 
Size 	
Width 	




##wxpython - wx.Image
#This class encapsulates a platform-independent image.

#An image can be created from data, or using wx.Bitmap.ConvertToImage .
#A wx.Image cannot  be drawn directly to a wx.DC. 
#Instead, a platform-specific wx.Bitmap object must be created 
# by using Bitmap.Bitmap(wxImage,int depth) constructor. 
#This bitmap can then be drawn in a device context by wx.DC.DrawBitmap .

Image()
Image(width, height, clear=True)
Image(sz, clear=True)
Image(name, type=BITMAP_TYPE_ANY, index=-1)
Image(name, mimetype, index=-1)
Image(stream, type=BITMAP_TYPE_ANY, index=-1)
Image(stream, mimetype, index=-1)
Image(width, height, data)
Image(width, height, data, alpha)
Image(size, data)
Image(size, data, alpha)
    name (string) 
        Name of the file from which to load the image.
    type (BitmapType) 
        May be one of the following:
        wx.BITMAP_TYPE_BMP: Load a Windows bitmap file.
        wx.BITMAP_TYPE_GIF: Load a GIF bitmap file.
        wx.BITMAP_TYPE_JPEG: Load a JPEG bitmap file.
        wx.BITMAP_TYPE_PNG: Load a PNG bitmap file.
        wx.BITMAP_TYPE_PCX: Load a PCX bitmap file.
        wx.BITMAP_TYPE_PNM: Load a PNM bitmap file.
        wx.BITMAP_TYPE_TIFF: Load a TIFF bitmap file.
        wx.BITMAP_TYPE_TGA: Load a TGA bitmap file.
        wx.BITMAP_TYPE_XPM: Load a XPM bitmap file.
        wx.BITMAP_TYPE_ICO: Load a Windows icon file (ICO).
        wx.BITMAP_TYPE_CUR: Load a Windows cursor file (CUR).
        wx.BITMAP_TYPE_ANI: Load a Windows animated cursor file (ANI).
        wx.BITMAP_TYPE_ANY: Will try to autodetect the format.
    index (int)
        Index of the image to load in the case that the image file contains multiple images. 
        This is only used by GIF, ICO and TIFF handlers. 
        The default value (-1) means 'choose the default image'
        and is interpreted as the first image (index=0) by the GIF and TIFF handler 
        and as the largest and most colourful one by the ICO handler.

##Methods Summary
AddHandler 	        Register an image handler.
AdjustChannels 	    This function muliplies all 4 channels (red, green, blue, alpha) with
Blur 	            Blurs the image in both horizontal and vertical directions by the specified pixel blurRadius.
BlurHorizontal 	    Blurs the image in the horizontal direction only.
BlurVertical 	    Blurs the image in the vertical direction only.
CanRead 	        Returns True if at least one of the available image handlers can read the file with the given name.
CleanUpHandlers 	Deletes all image handlers.
Clear 	            Initialize the image data with zeroes (the default) or with the byte value given as value.
ClearAlpha 	        Removes the alpha channel from the image.
ComputeHistogram 	Computes the histogram of the image.
ConvertAlphaToMask 	If the image has alpha channel, this method converts it to mask.
ConvertToBitmap 	ConvertToBitmap(depth=-1) . Bitmap
ConvertToDisabled 	Returns disabled (dimmed) version of the image.
ConvertToGreyscale 	Returns a greyscale version of the image.
ConvertToMono 	    Returns monochromatic version of the image.
ConvertToMonoBitmap 	ConvertToMonoBitmap(red, green, blue) . Bitmap
Copy 	            Returns an identical copy of this image.
Create 	            Creates a fresh image.
Destroy 	        Destroys the image data.
FindFirstUnusedColour 	Finds the first colour that is never used in the image.
FindHandler 	    Finds the handler with the given name.
FindHandlerMime 	Finds the handler associated with the given MIME type.
GetAlpha 	        Return alpha value at given pixel location.
GetAlphaBuffer 	    Returns a writable Python buffer object that is pointing at the Alpha
GetBlue 	        Returns the blue intensity at the given coordinate.
GetData 	        Returns a copy of the RGB bytes of the image.
GetDataBuffer 	    Returns a writable Python buffer object that is pointing at the RGB
GetGreen 	        Returns the green intensity at the given coordinate.
GetHeight 	        Gets the height of the image in pixels.
GetImageCount 	    If the image file contains more than one image and the image handler is capable of retrieving these individually, this function will return the number of available images.
GetImageExtWildcard 	Iterates all registered wx.ImageHandler objects, and returns a string containing file extension masks suitable for passing to file open/save dialog boxes.
GetMaskBlue 	    Gets the blue value of the mask colour.
GetMaskGreen 	    Gets the green value of the mask colour.
GetMaskRed 	        Gets the red value of the mask colour.
GetOption 	        Gets a user-defined string-valued option.
GetOptionInt 	    Gets a user-defined integer-valued option.
GetOrFindMaskColour 	Get the current mask colour or find a suitable unused colour that could be used as a mask colour.
GetPalette 	        Returns the palette associated with the image.
GetRed 	            Returns the red intensity at the given coordinate.
GetSize 	        Returns the size of the image in pixels.
GetSubImage 	    Returns a sub image of the current one as long as the rect belongs entirely to the image.
GetType 	        Gets the type of image found by LoadFile or specified with SaveFile .
GetWidth 	        Gets the width of the image in pixels.
HSVtoRGB 	        Converts a color in HSV color space to RGB color space.
HasAlpha 	        Returns True if this image has alpha channel, False otherwise.
HasMask 	        Returns True if there is a mask active, False otherwise.
HasOption 	        Returns True if the given option is present.
InitAlpha 	        Initializes the image alpha channel data.
InitStandardHandlers 	Internal use only.
InsertHandler 	    Adds a handler at the start of the static list of format handlers.
IsOk 	            Returns True if image data is present.
IsTransparent 	    Returns True if the given pixel is transparent, i.e. either has the mask colour if this image has a mask or if this image has alpha channel and alpha value of this pixel is strictly less than threshold.
LoadFile 	        Loads an image from an input stream.
Mirror 	            Returns a mirrored copy of the image.
Paste 	            Copy the data of the given image to the specified position in this image.
RGBtoHSV 	        Converts a color in RGB color space to HSV color space.
RemoveHandler 	    Finds the handler with the given name, and removes it.
Replace 	        Replaces the colour specified by r1,g1,b1 by the colour r2,g2,b2.
Rescale 	        Changes the size of the image in-place by scaling it: after a call to this function,the image will have the given width and height.
Resize 	            Changes the size of the image in-place without scaling it by adding either a border with the given colour or cropping as necessary.
Rotate 	            Rotates the image about the given point, by angle radians.
Rotate180 	        Returns a copy of the image rotated by 180 degrees.
Rotate90 	        Returns a copy of the image rotated 90 degrees in the direction indicated by clockwise.
RotateHue 	        Rotates the hue of each pixel in the image by angle, which is a float in the range of -1.0 to +1.0, where -1.0 corresponds to -360 degrees and +1.0 corresponds to +360 degrees.
SaveFile 	        Saves an image in the given stream.
Scale 	            Returns a scaled version of the image.
SetAlpha 	        Sets the alpha value for the given pixel.
SetAlphaBuffer 	    Sets the internal image alpha pointer to point at a Python buffer
SetData 	        Sets the image data without performing checks.
SetDataBuffer 	    Sets the internal image data pointer to point at a Python buffer
SetMask 	        Specifies whether there is a mask or not.
SetMaskColour 	    Sets the mask colour for this image (and tells the image to use the mask).
SetMaskFromImage 	Sets image’s mask so that the pixels that have RGB value of mr,mg,mb in mask will be masked in the image.
SetOption 	        Sets a user-defined option.
SetPalette 	        Associates a palette with the image.
SetRGB 	            Set the color of the pixel at the given x and y coordinate.
SetType 	        Set the type of image returned by GetType .
Size 	            Returns a resized version of this image without scaling it by adding either a border with the given colour or cropping as necessary.

##Properties Summary
Height 	    
MaskBlue 	
MaskGreen 	
MaskRed 	
Type 	    
Width 	    


#Example - Creating a Simple Photo Viewer with wxPython
#Using wx.BitmapFromImage(wx.Image)
#and

import os
import wx
 
class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
 
        self.panel = wx.Panel(self.frame)
 
        self.PhotoMaxSize = 240
 
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
 
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)        
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
 
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()




##Wxpython - wx.Validator, derived from wx.EvtHandler
# A validator is an object that can be plugged into a control (such as a wx.TextCtrl), 
#and mediates between Python data and the control, transferring the data in either direction and validating it. 
#It also is able to intercept events generated by the control, providing filtering behaviour without the need to derive a new control class.

#create a sub-class of wx.Validator 
#This sub-class is then associated with input field by calling:
myInputField.SetValidator(myValidator)
#or while creating instance of Control 
wx.Control(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,
        style=0, validator=DefaultValidator, name=ControlNameStr)
        
#any wx.Window may have a validator; 
#using the WS_EX_VALIDATE_RECURSIVELY style (Window extended styles) 
#you can also implement recursive validation.


#wx.Validator sub-class must implement below methods 
TransferFromWindow(self)
    This optional,overridable function is called 
    when the value in the window must be transferred to the validator.
    Return type:	bool
    Returns:	False if there is a problem.
TransferToWindow(self)
    This optional, overridable function is called 
    when the value associated with the validator must be transferred to the window.
    Return type:	bool
    Returns:	False if there is a problem.
Validate(self, parent)
    This overridable function is called 
    when the value in the associated window must be validated.
    Parameters:	parent (wx.Window) – The parent of the window associated with the validator.
    Return type:	bool
    Returns:	False if the value in the window is not valid; you may pop up an error dialog.
Clone(self)
    All validator classes must implement the Clone function, 
    which returns an identical copy of itself.
    Return type:	wx.Object
    Returns:	This base function returns None.
      
      
##Other methods of wx.Validator 
#To specify a default, 'null' validator, use wx.DefaultValidator .
GetWindow 	            Returns the window associated with the validator.
IsSilent 	            Returns if the error sound is currently disabled.
SetWindow 	            Associates a window with the validator.
SuppressBellOnError 	This functions switches on or turns off the error sound produced by the validators if an invalid key is pressed.



##How Validators Interact with Dialogs
#When a wx.Dialog.Show is called (for a modeless dialog) 
#or wx.Dialog.ShowModal is called (for a modal dialog), 
#The function wx.Window.InitDialog,EVT_INIT_DIALOG is automatically called. 
#This event binding would call all validators 

#For using window or panel for dialog ,call wx.Window.InitDialog explicitly 
#before showing the window.
#When the user clicks on a button, for example the OK button, 
#call wx.Window.Validate, which returns False if something fails
#If returns True, call wx.Window.TransferDataFromWindow and return if this failed. 

#Note wx.Dialog's default ID_OK handler does all the above 



#Example 
    
#!/usr/bin/env python

import  string
import  wx

#----------------------------------------------------------------------

ALPHA_ONLY = 1
DIGIT_ONLY = 2

class MyValidator(wx.Validator):
    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return MyValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        if self.flag == ALPHA_ONLY:
            for x in val:
                if x not in string.ascii_letters:
                    return False

        elif self.flag == DIGIT_ONLY:
            for x in val:
                if x not in string.digits:
                    return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

#----------------------------------------------------------------------

class TestValidatorPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(True)
        VSPACE = 10

        fgs = wx.FlexGridSizer(cols=2)

        fgs.Add((1,1))
        fgs.Add(wx.StaticText(self, -1, "These controls have validators that limit\n"
                             "the type of characters that can be entered."))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "Alpha Only: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)

        fgs.Add(wx.TextCtrl(self, -1, "", validator = MyValidator(ALPHA_ONLY)))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "Digits Only: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)
        fgs.Add(wx.TextCtrl(self, -1, "", validator = MyValidator(DIGIT_ONLY)))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))
        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))
        fgs.Add((0,0))
        b = wx.Button(self, -1, "Test Dialog Validation")
        self.Bind(wx.EVT_BUTTON, self.OnDoDialog, b)
        fgs.Add(b)

        border = wx.BoxSizer()
        border.Add(fgs, 1, wx.GROW|wx.ALL, 25)
        self.SetSizer(border)
        self.Layout()

    def OnDoDialog(self, evt):
        dlg = TestValidateDialog(self)
        dlg.ShowModal()
        dlg.Destroy()


#----------------------------------------------------------------------

class TextObjectValidator(wx.Validator):
    """ This validator is used to ensure that the user has entered something
        into the text object editor dialog's text field.
    """
    def __init__(self):
        """ Standard constructor.
        """
        wx.Validator.__init__(self)


    def Clone(self):
        """ Standard cloner.

            Note that every validator must implement the Clone() method.
        """
        return TextObjectValidator()

    def Validate(self, win):
        """ Validate the contents of the given text control.
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:
            wx.MessageBox("A text object must contain some text!", "Error")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        """ Transfer data from validator to window.
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        """ Transfer data from window to validator.
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

#----------------------------------------------------------------------

class TestValidateDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Validated Dialog")

        self.SetAutoLayout(True)
        VSPACE = 10

        fgs = wx.FlexGridSizer(cols=2)

        fgs.Add((1,1));
        fgs.Add(wx.StaticText(self, -1,
                             "These controls must have text entered into them.  Each\n"
                             "one has a validator that is checked when the Ok\n"
                             "button is clicked."))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "First: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)

        fgs.Add(wx.TextCtrl(self, -1, "", validator = TextObjectValidator()))

        fgs.Add((1,VSPACE)); fgs.Add((1,VSPACE))

        label = wx.StaticText(self, -1, "Second: ")
        fgs.Add(label, 0, wx.ALIGN_RIGHT|wx.CENTER)
        fgs.Add(wx.TextCtrl(self, -1, "", validator = TextObjectValidator()))


        buttons = wx.StdDialogButtonSizer() #wx.BoxSizer(wx.HORIZONTAL)
        b = wx.Button(self, wx.ID_OK, "OK")
        b.SetDefault()
        buttons.AddButton(b)
        buttons.AddButton(wx.Button(self, wx.ID_CANCEL, "Cancel"))
        buttons.Realize()

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(fgs, 1, wx.GROW|wx.ALL, 25)
        border.Add(buttons, 0, wx.GROW|wx.BOTTOM, 5)
        self.SetSizer(border)
        border.Fit(self)
        self.Layout()


app = wx.App(False)     # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Demo") # A Frame is a top-level window.
TestValidatorPanel(frame,sys.stderr)
frame.Show(True)        # Show the frame.
app.MainLoop()
 
       
        
        
##Wxpython - Splitter Windows 

wx.SplitterWindow(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,
               style=SP_3D, name="splitterWindow")
    This class manages up to two subwindows.

#Styles
wx.SP_3D: Draws a 3D effect border and sash.
wx.SP_THIN_SASH: Draws a thin sash.
wx.SP_3DSASH: Draws a 3D effect sash (part of default style).
wx.SP_3DBORDER: Synonym for wx.SP_BORDER.
wx.SP_BORDER: Draws a standard border.
wx.SP_NOBORDER: No border (default).
wx.SP_NO_XP_THEME: Under Windows XP, switches off the attempt to draw the splitter using Windows XP theming, so the borders and sash will take on the pre-XP look.
wx.SP_PERMIT_UNSPLIT: Always allow to unsplit, even with the minimum pane size other than zero.
wx.SP_LIVE_UPDATE: Don’t draw wx.XOR line but resize the child windows immediately.

#Events Emitted by this Class
EVT_SPLITTER_SASH_POS_CHANGING: The sash position is in the process of being changed. May be used to modify the position of the tracking bar to properly reflect the position that would be set if the drag were to be completed at this point. Processes a wxEVT_SPLITTER_SASH_POS_CHANGING event.
EVT_SPLITTER_SASH_POS_CHANGED: The sash position was changed. May be used to modify the sash position before it is set, or to prevent the change from taking place. Processes a wxEVT_SPLITTER_SASH_POS_CHANGED event.
EVT_SPLITTER_UNSPLIT: The splitter has been just unsplit. Processes a wxEVT_SPLITTER_UNSPLIT event.
EVT_SPLITTER_DCLICK: The sash was double clicked. The default behaviour is to unsplit the window when this happens (unless the minimum pane size has been set to a value greater than zero). Processes a wxEVT_SPLITTER_DOUBLECLICKED event.

#Few Important methods of wx.SplitterWindow
SplitHorizontally(self, window1, window2, sashPosition=0)
    Initializes the top and bottom panes of the splitter window.
    The child windows are shown if they are currently hidden.
SplitVertically(self, window1, window2, sashPosition=0)
    Initializes the left and right panes of the splitter window.
    The child windows are shown if they are currently hidden.    
Unsplit(self, toRemove=None)
    Unsplits the window.
    Parameters:	toRemove (wx.Window) – The pane to remove, or None to remove the right or bottom pane.
ReplaceWindow(self, winOld, winNew)
    This function replaces one of the windows managed by the wx.SplitterWindow with another one.    
Initialize(self, window)
    Initializes the splitter window to have one pane.
    This should be called if you wish to initially view only a single pane in the splitter window.

#Example - creating two subwindows and hiding one of them:

class MySplitter(wx.SplitterWindow):
    def __init__(self, parent, ID, log):
        wx.SplitterWindow.__init__(self, parent, ID,wx.Point(0, 0),
                                    wx.Size(400, 400),
                                   style = wx.SP_3D | wx.SP_LIVE_UPDATE
                                   )
        self.log = log
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)

    def OnSashChanged(self, evt):
        self.log.WriteText("sash changed to %s\n" % str(evt.GetSashPosition()))

    def OnSashChanging(self, evt):
        self.log.WriteText("sash changing to %s\n" % str(evt.GetSashPosition()))
        # uncomment this to not allow the change
        #evt.SetSashPosition(-1)
        
#Usage 
app = wx.App(False)     # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Demo") # A Frame is a top-level window.

splitter = MySplitter(nb, -1, sys.stderr)
#sty = wx.BORDER_NONE
#sty = wx.BORDER_SIMPLE
sty = wx.BORDER_SUNKEN

p1 = wx.Window(splitter, style=sty)
p1.SetBackgroundColour("pink")
wx.StaticText(p1, -1, "Panel One", (5,5))

p2 = wx.Window(splitter, style=sty)
p2.SetBackgroundColour("sky blue")
wx.StaticText(p2, -1, "Panel Two", (5,5))

#The default minimum pane size is zero, which means that either pane can be reduced to zero by dragging the sash, 
#thus removing one of the panes
splitter.SetMinimumPaneSize(20)
splitter.SplitVertically(p1, p2, -100)

frame.Show(True)        # Show the frame.
app.MainLoop()


##For displaying only one pane 
splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0),
                             wx.Size(400, 400), wx.SP_3D)

leftWindow = MyWindow(splitter)
leftWindow.SetScrollbars(20, 20, 50, 50)

rightWindow = MyWindow(splitter)
rightWindow.SetScrollbars(20, 20, 50, 50)
rightWindow.Show(False)
#This should be called if you wish to initially view only a single pane in the splitter window.
splitter.Initialize(leftWindow)
# Set this to prevent unsplitting
splitter.SetMinimumPaneSize(20)

##Example - how the splitter window can be manipulated after creation:

def OnSplitVertical(self, event):
    if splitter.IsSplit():
        splitter.Unsplit()
    leftWindow.Show(True)
    rightWindow.Show(True)
    splitter.SplitVertically(leftWindow, rightWindow)


def OnSplitHorizontal(self, event):
    if splitter.IsSplit():
        splitter.Unsplit()
    leftWindow.Show(True)
    rightWindow.Show(True)
    splitter.SplitHorizontally(leftWindow, rightWindow)

def OnUnsplit(self, event):
    if splitter.IsSplit():
        splitter.Unsplit()


