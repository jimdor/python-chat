import socket, threading, logging

# Connection Data
host = '127.0.0.1'
port = 55555

logging.basicConfig(
	level=logging.INFO,
	filename = "mylog.txt",
	format = "time - %(asctime)s - %(message)s",
    datefmt='%H:%M:%S',
	)

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
last_client = str

'''
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON, address='/dev/log')
my_logger.addHandler(handler)
'''

# Sending Messages To All Connected Clients
def broadcast(message):
	for client in clients:
		if (client != last_client):
			client.send(message)
		else: 
			try:
				last_client.send('successfully delivered'.encode('utf-8'))
			except: last_client.send('An error occured!'.encode('utf-8'))

# Handling Messages From Clients
def handle(client):
	global last_client
	while True:
		try:
			# Broadcasting Messages
			message = client.recv(1024)
			last_client = client
			broadcast(message)
			print(message.decode('utf-8'))
			#my_logger.info(message.decode('utf-8'))
			logging.info('address - {} nickname and text - {}'.format(client.getsockname(), message.decode('utf-8')))
		except:
			# Removing And Closing Clients
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast('{} left!'.format(nickname).encode('utf-8'))
			nicknames.remove(nickname)
			break

# Receiving / Listening Function
def receive():
	while True:
		# Accept Connection
		client, address = server.accept()
		print("Connected with {}".format(str(address)))

		# Request And Store Nickname
		client.send('NICK'.encode('utf-8'))
		nickname = client.recv(1024).decode('utf-8')
		nicknames.append(nickname)
		clients.append(client)

		# Print And Broadcast Nickname
		print("Nickname is {}".format(nickname))
		broadcast("{} joined!".format(nickname).encode('utf-8'))
		client.send('Connected to server!'.encode('utf-8'))

		# Start Handling Thread For Client
		thread = threading.Thread(target = handle, args = (client,))
		thread.start()

print('server started')
receive()