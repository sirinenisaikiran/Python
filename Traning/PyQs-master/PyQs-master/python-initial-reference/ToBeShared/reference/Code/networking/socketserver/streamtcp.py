import socketserver

#makes use of streams (file-like objects ) with file interfaces
		
class MyTCPHandler(socketserver.StreamRequestHandler):
	"""
	Only override handle
	"""
	def handle(self):  #it handles only one surge of data, put in while loop for handling many such surges
		# self.rfile is a file-like object created by the handler;
		# we can now use e.g. readline() instead of raw recv() calls
		self.data = self.rfile.readline().strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# Likewise, self.wfile is a file-like object used to write back
		# to the client
		self.wfile.write(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
