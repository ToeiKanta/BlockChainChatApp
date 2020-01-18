import socket
import threading
import sys, os
import random
import string
import json
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
		self.sock.bind(('0.0.0.0',20003))
		self.sock.listen(1)
	def sendBoardcast(self):
		while True:
			data = bytes(input(""),'utf-8')
			for connection in self.connections:
				connection.send(data)

	# recieve msg handler from Client
	def handler(self,c,a):
		while True:
			data = c.recv(1024)
			#create new block
			block = BlockChain.Block(data.decode('utf-8'))
			blockchain.mine(block)
			for connection in self.connections:
				connection.send(bytes(str(block.data),'utf-8'))
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
	padding_character = "X"
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendMsg(self):
		while True:
			private_msg = input("")
			secret_key = self.key_aes
			padding_character = self.padding_character
			data = {
				"groupId" : str(self.groupId),
				"sender" : str(self.name),
				"msg" : str(AES_Cyptography.encrypt_message(private_msg, secret_key, padding_character).decode('utf-8'))
			}
			jsonData = json.dumps(data)
			# data = bytes('{ "groupId": "' + str(self.groupId)+ '","sender": "'+ str(self.name) +'","msg": "' + str(AES_Cyptography.encrypt_message(private_msg, secret_key, padding_character))  + '"}','utf-8')
			self.sock.send(bytes(jsonData,"utf-8"))
	def __init__(self,address):
		self.sock.connect((address,20003))
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
		# recieve msg from server
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			newBlock = json.loads(data.decode("utf-8"))
			groupId = newBlock["groupId"]
			sender = newBlock["sender"]
			msg = newBlock["msg"]
			if (groupId == self.groupId):
				print(str(sender) + " : " + str(AES_Cyptography.decrypt_message(msg, self.key_aes, self.padding_character).decode('utf-8')))

if(len(sys.argv)>1):
	client = Client(sys.argv[1])
else:
	server = Server()
	server.run()