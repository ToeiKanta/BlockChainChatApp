# Usefull Link [ASCII generator] http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

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

# Module for colorfull console 
from colorama import init
init()
from colorama import Fore, Back, Style

### Example of colorama ###
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

# Run BlockChain
blockchain = BlockChain.Blockchain()
genesisBlock = blockchain.head

#Random String for Generate Key and GroupId
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Server Class
class Server:
	# port connection
	port = 0
	# create socket for connection
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# store list of client connection 
	connections = []
	# setting port address on class init
	def __init__(self,port):
		self.port = port
		self.sock.bind(('0.0.0.0',int(port)))
		self.sock.listen(1)
	# method to sending msg to all client
	def sendBoardcast(self):
		while True:
			try:
				data = bytes(input(""),'utf-8')
				# if u type "exit" to console
				# It will terminate program
				if(len(data.split()) == 2):
					BlockChain.editBlock(blockchain,genesisBlock, int(data.split()[1]))
				if(data == "exit"):
					print("Close Server")
					os.kill(os.getpid(), 9)
				# sending msg to all client
				# for connection in self.connections:
				# 	connection.send(data)
			# catch error when press CTRL+C and Terminate program
			except EOFError as error:
				print("Close Server")
				os.kill(os.getpid(), 9)
	# recieve msg handler from Client
	def handler(self,c,a):
		while True:
			try:
				data = c.recv(1024)
			# Catch error when client disconnected then remove that client connection
			except Exception as error:
				print(str(a[0])+':'+str(a[1])+" disconnected")
				self.connections.remove(c)
				c.close()
				break
			#create new block data when msg recieved
			block = BlockChain.Block(data.decode('utf-8'))
			blockchain.mine(block)
			# Send new block data to all Clients
			for connection in self.connections:
				connection.send(bytes(str(block.data),'utf-8'))
			# Disconnect client when they close program
			if not data:
				print(str(a[0])+':'+str(a[1])+" disconnected")
				self.connections.remove(c)
				c.close()
				break
	# start server
	def run(self):
		# create Thread for handle input in terminal
		iThread = threading.Thread(target=self.sendBoardcast)
		iThread.daemon = True
		iThread.start()
		# Clear screen terminal
		os.system('cls')
		os.system('clear')
		# Print Welcome message
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
		# Wait for Client connected
		while True:
			c,a = self.sock.accept()
			cThread = threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon = True
			cThread.start()
			# Add Client connection to Arrays
			self.connections.append(c)
			print(str(a[0])+':'+str(a[1])+" connected")

# Client Class
class Client:
	# Store GROUP secrete key 
	key_aes = ''
	# Store NAME client
	name = ''
	# Store GROUP ID
	groupId = ''
	# Create Socket connection
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# Method sending message to SERVER
	def sendMsg(self):
		# Handler Client sending message
		while True:
			try:
				private_msg = input("")
				# Close Program when type "exit" in console
				if(private_msg == "exit"):
					print("Close connection")
					os.kill(os.getpid(), 9)
				secret_key = self.key_aes
				# Create data to store in BlockChain Data
				data = {
					"groupId" : str(self.groupId),
					"sender" : str(self.name),
					"msg" : str(AES_Cyptography.AESCipher(secret_key).encrypt(private_msg).decode('utf-8'))
				}
				# Change Object to String
				jsonData = json.dumps(data)
				# Send data to SERVER
				self.sock.send(bytes(jsonData,"utf-8"))
			# Catch Error and Terminate yourself
			except EOFError as error:
				print("Close connections")
				os.kill(os.getpid(), 9)
	# Constructure Method when create Class
	def __init__(self,address,port):
		# Socket connect to HOST (SERVER)
		self.sock.connect((address,int(port)))
		# Welcome Message
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
		# Store name client to variable
		self.name = input("ENTER your name : ")
		print("==========================")
		print("    Choose mode")
		print("==========================")
		print("ENTER 1 to CREATE new group:")
		print("ENTER 2 to JOIN group:")
		print("==========================")
		# Wait to select MODE
		while True:
			mode = input("Mode : ")
			# This condition for CREATE new group
			if(mode == "1"):
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				print("You select mode 1 (create new group chat):")
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				# create AES key
				self.key_aes = randomString(20).upper()
				# create group ID
				self.groupId = randomString(10).upper()
				print("==============================================================")
				print(Fore.LIGHTGREEN_EX,"This is your group id (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.groupId))
				print(Fore.LIGHTGREEN_EX,"This is your secrete group key (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.key_aes))
				print(Fore.LIGHTGREEN_EX,"==============================================================")
				# Exit Loop when selected MODE
				break
			# This condition for JOIN group
			elif(mode == "2"):
				print("==================================")
				self.groupId = input("Enter Group ID :")
				self.key_aes = input("Please enter secrete group key : ")
				# Exit Loop when selected MODE
				break
		###############################
		##### ENTERING CHAT ROOM ######
		###############################
		print(Fore.LIGHTYELLOW_EX)
		print("////////// WELCOME TO CHAT ROOM ///////////")
		print(" CHAT ROOM Group_id : "+self.groupId +" Started!!!")
		print(" You are : "+self.name)
		print("///////////////////////////////////////////")
		print(Fore.LIGHTGREEN_EX)
		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()
		# Wait recieve msg from SERVER
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			newBlock = json.loads(data.decode("utf-8"))
			# Get infomation from JSON
			groupId = newBlock["groupId"]
			sender = newBlock["sender"]
			msg = newBlock["msg"]
			# Show Message only current group
			if (groupId == self.groupId):
				print(str(sender) + " : " + str(AES_Cyptography.AESCipher(self.key_aes).decrypt(msg).decode('utf-8')))


######################################################
############ Start Command Handler ###################
######################################################
if(len(sys.argv)>2):
	# Create CLIENT with IP and PORT connected
	client = Client(sys.argv[1],sys.argv[2])
else:
	# Create SERVER with PORT
	server = Server(sys.argv[1])
	server.run()