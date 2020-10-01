import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
	"""
	Only override handle
	"""

	def handle(self):    #it handles only one surge of data, put in while loop for handling many such surges
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data.decode('ascii'))
		# just send back the same data, but upper-cased
		self.request.send(self.data.upper())
		

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
