import socket
import threading
import sys, os
import random
import string
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'BlockChain'))
import BlockChain
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AES_Cyptography'))
import AES_Cyptography

# Run BlockChain
blockchain = BlockChain.Blockchain()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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
	key_aes = ''
	name = ''
	groupId = ''
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendMsg(self):
		while True:
			private_msg = input("")
			secret_key = self.key_aes
			padding_character = "X"
			data = bytes("{ groupID: " + str(self.groupId)+ ";name: "+ str(self.name) +";msg: " + str(AES_Cyptography.encrypt_message(private_msg, secret_key, padding_character))  + "}",'utf-8')
			self.sock.send(data)
	def __init__(self,address):
		self.sock.connect((address,20002))
		print("Welcome to BlockChat")
		print("Enter your name :")
		self.name = input("")
		print("What do you want?")
		print("enter 1 to create new group:")
		print("enter 2 to join group:")
		mode = input("")
		# create new group
		if(mode == "1"):
			# create AES key
			self.key_aes = AES_Cyptography.generate_secret_key_for_AES_cipher()
			# create group ID
			self.groupId = randomString(10)
			print("GroupID generated : " + str(self.groupId))
			print("Secrete Group Key generated : " + str(self.key_aes.decode("utf-8")))
		elif(mode == "2"):
			print("Enter Group ID :")
			self.groupId = input("")
			print("Please enter secrete group key :")
			self.key_aes = input("")

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