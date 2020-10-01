import socket
import threading
import socketserver

import socket, threading, time, signal, sys



class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	""" Only override handle"""
	def handle(self): 
		data = str(self.request.recv(1024), 'ascii')
		cur_thread = threading.current_thread()
		print("{} wrote:".format(self.client_address[0]))
		print(data)
		response = bytes("{}: {}".format(cur_thread.name, data.upper()), 'ascii')
		self.request.sendall(response)

		
#The ForkingMixIn class - spawn a new process for each request.
#MixIn class must be at first
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

	

if __name__ == "__main__":	
	
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "localhost", 9998

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address	
	
	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()
	print("Server loop running in thread:", server_thread.name)
	input("PRESS ENTER TO Exit") # py2.x raw_input

    
