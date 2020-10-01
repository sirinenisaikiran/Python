##Server Code 
# import socket programming library
import socket
 
# import thread module
import threading
 

 
# thread fuction
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
    port = 12345
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

    
    
##Client Code

# Import socket module
import socket
 
 
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 12345
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))
 
    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:
 
        # message sent to server
        s.send(message.encode('ascii'))
 
        # messaga received from server
        data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))
 
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()
 
if __name__ == '__main__':
    Main()
