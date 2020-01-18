import socket
import threading
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'BlockChain'))
import BlockChain
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AES_Cyptography'))
import AES_Cyptography

# Run BlockChain
blockchain = BlockChain.Blockchain()

class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	def __init__(self):
		self.sock.bind(('0.0.0.0',20002))
		self.sock.listen(1)
	def sendBoardcast(self):
		while True:
			data = bytes(input(""),'utf-8')
			for connection in self.connections:
				connection.send(data)
	def handler(self,c,a):
		while True:
			data = c.recv(1024)
			# Mining Block
			block = BlockChain.Block(data)
			blockchain.mine(block)
			for connection in self.connections:
				connection.send(bytes(str(block),'utf-8'))
				# print(data)
			if not data:
				print(str(a[0])+':'+str(a[1])+" disconnected")
				self.connections.remove(c)
				c.close()
				break
	def run(self):
		iThread = threading.Thread(target=self.sendBoardcast)
		iThread.daemon = True
		iThread.start()
		while True:
			c,a = self.sock.accept()
			cThread = threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0])+':'+str(a[1])+" connected")

class Client:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendMsg(self):
		while True:
			data = bytes(input(""),'utf-8')
			self.sock.send(data)
	def __init__(self,address):
		self.sock.connect((address,20002))
		
		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			print(data)

if(len(sys.argv)>1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()