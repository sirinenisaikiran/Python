import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
	"""
	Only override handle
	"""
	
	def handle(self):  #to handle multiple surge, put under some while loop
		data = self.request[0].strip()   #request = (data , client socket)
		socket = self.request[1]
		print("{} wrote:".format(self.client_address[0]))
		print(data)
		socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
