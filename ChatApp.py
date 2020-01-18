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

from colorama import init
init()
from colorama import Fore, Back, Style
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

# Run BlockChain
blockchain = BlockChain.Blockchain()
# Setting up PORT
PORT = 12346

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Server 
class Server:
	port = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	def __init__(self,port):
		self.port = port
		self.sock.bind(('0.0.0.0',int(port)))
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
		os.system('cls')
		os.system('clear')
		print("//////////// Welcome to ///////////////////")
		print("""
 $$$$$$\  $$\   $$\ $$$$$$$$\               
$$  __$$\ $$ |  $$ |\__$$  __|              
$$ /  \__|$$ |  $$ |   $$ |                 
\$$$$$$\  $$ |  $$ |   $$ |                 
 \____$$\ $$ |  $$ |   $$ |                 
$$\   $$ |$$ |  $$ |   $$ |                 
\$$$$$$  |\$$$$$$  |   $$ |                 
 \______/  \______/    \__|                 
                                            
$$$$$$$\  $$\                     $$\       
$$  __$$\ $$ |                    $$ |      
$$ |  $$ |$$ | $$$$$$\   $$$$$$$\ $$ |  $$\ 
$$$$$$$\ |$$ |$$  __$$\ $$  _____|$$ | $$  |
$$  __$$\ $$ |$$ /  $$ |$$ /      $$$$$$  / 
$$ |  $$ |$$ |$$ |  $$ |$$ |      $$  _$$<  
$$$$$$$  |$$ |\$$$$$$  |\$$$$$$$\ $$ | \$$\ 
\_______/ \__| \______/  \_______|\__|  \__|
                                            
 $$$$$$\  $$\                  $$\          
$$  __$$\ $$ |                 $$ |         
$$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\        
$$ |      $$  __$$\  \____$$\\_$$  _|       
$$ |      $$ |  $$ | $$$$$$$ | $$ |         
$$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\      
\$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |     
 \______/ \__|  \__| \_______|  \____/      
                                            
""")
		print("//////////// This is SERVER ///////////////////")
		print("SERVER running on port "+str(socket.gethostbyname(socket.gethostname()))+":"+str(self.port))
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
	padding_character = "T"
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendMsg(self):
		# When Client send msg
		while True:
			private_msg = input("")
			if(private_msg == "exit"):
				print("Please enter CTRL+C to Exit")
				sys.exit(1)
			secret_key = self.key_aes
			padding_character = self.padding_character
			data = {
				"groupId" : str(self.groupId),
				"sender" : str(self.name),
				"msg" : str(AES_Cyptography.encrypt_message(private_msg, secret_key, padding_character).decode('utf-8'))
			}
			jsonData = json.dumps(data)
			self.sock.send(bytes(jsonData,"utf-8"))
	def __init__(self,address,port):
		self.sock.connect((address,int(port)))
		print(Fore.LIGHTGREEN_EX)
		os.system('cls')
		os.system('clear')
		print("//////////// Welcome to ///////////////////")
		print("""
 $$$$$$\  $$\   $$\ $$$$$$$$\               
$$  __$$\ $$ |  $$ |\__$$  __|              
$$ /  \__|$$ |  $$ |   $$ |                 
\$$$$$$\  $$ |  $$ |   $$ |                 
 \____$$\ $$ |  $$ |   $$ |                 
$$\   $$ |$$ |  $$ |   $$ |                 
\$$$$$$  |\$$$$$$  |   $$ |                 
 \______/  \______/    \__|                 
                                            
$$$$$$$\  $$\                     $$\       
$$  __$$\ $$ |                    $$ |      
$$ |  $$ |$$ | $$$$$$\   $$$$$$$\ $$ |  $$\ 
$$$$$$$\ |$$ |$$  __$$\ $$  _____|$$ | $$  |
$$  __$$\ $$ |$$ /  $$ |$$ /      $$$$$$  / 
$$ |  $$ |$$ |$$ |  $$ |$$ |      $$  _$$<  
$$$$$$$  |$$ |\$$$$$$  |\$$$$$$$\ $$ | \$$\ 
\_______/ \__| \______/  \_______|\__|  \__|
                                            
 $$$$$$\  $$\                  $$\          
$$  __$$\ $$ |                 $$ |         
$$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\        
$$ |      $$  __$$\  \____$$\\_$$  _|       
$$ |      $$ |  $$ | $$$$$$$ | $$ |         
$$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\      
\$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |     
 \______/ \__|  \__| \_______|  \____/      
                                            
""")
		print("//////////////// U R Anonymus //////////////////")
		print("ENTER your name :")
		self.name = input("")
		print("==========================")
		print("    Choose mode")
		print("==========================")
		print("ENTER 1 to CREATE new group:")
		print("ENTER 2 to JOIN group:")
		print("==========================")
		while True:
			mode = input("")
			# create new group
			if(mode == "1"):
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				print("You select mode 1 (create new group chat):")
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				# create AES key
				self.key_aes = AES_Cyptography.generate_secret_key_for_AES_cipher()
				# create group ID
				self.groupId = randomString(10).upper()
				print("==============================================================")
				print(Fore.LIGHTGREEN_EX,"This is your group id (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.groupId))
				print(Fore.LIGHTGREEN_EX,"This is yout secrete group key (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.key_aes.decode("utf-8")))
				print(Fore.LIGHTGREEN_EX,"==============================================================")
				break
			elif(mode == "2"):
				print("==================================")
				print("Enter Group ID :")
				self.groupId = input("")
				print("Please enter secrete group key :")
				self.key_aes = input("")
				break
		print(Fore.LIGHTYELLOW_EX)
		print("////////// WELCOME TO CHAT ROOM ///////////")
		print(" CHAT ROOM Group_id : "+self.groupId +" Started!!!")
		print(" You are : "+self.name)
		print("///////////////////////////////////////////")
		print(Fore.LIGHTGREEN_EX)
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

if(len(sys.argv)>2):
	client = Client(sys.argv[1],sys.argv[2])
else:
	server = Server(sys.argv[1])
	server.run()