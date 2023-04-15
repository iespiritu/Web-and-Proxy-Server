# -*- coding: utf-8 -*-
# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

proxySocket = socket(AF_INET, SOCK_STREAM)
proxyHost = "127.0.0.1"
proxyPort = 8888										
FORMAT = "utf-8" 							# default
BUFFER_SIZE = 4096

proxySocket.bind((proxyHost, proxyPort)) 	# Input must be a tuple
proxySocket.listen(1) 						# Listening for connections


# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	# Set up a new connection from the client
	clientSocket, addr = proxySocket.accept()             

	# Receives the request message from the client
	message = clientSocket.recv(BUFFER_SIZE)

	# Output message received from the client
	print("Message in bytes received from client:")
	print(message)
 
	# Extract the path of the requested object from the message
	# The path is the second part of HTTP header, identified by [1]
	filename_for = message.split()[1]

	SLASH = "/"
	parseDest = filename_for.decode().split(SLASH) 			# Decodes GET message to string then breaks into array
	parseRemove = SLASH + parseDest[1]						# Locates web address to parse from GET message string and includes forward slash
	messageStr = message.decode().replace(parseRemove, "")	# Removes web address string from GET message string
	temporaryBuffer = messageStr.encode()					# Recreates GET message as bytes

	print("Message in bytes parsed from client and sent to web server:")
	print (temporaryBuffer)
	#f.close()

	# Create web socket and connect to webserver
	webSocket = socket(AF_INET, SOCK_STREAM)
	webHost = "127.0.0.1"  						# replace with web server hostname
	webPort = 6789  							# replace with web server port
	webSocket.connect((webHost, webPort))
	webSocket.send(temporaryBuffer) 			# Send the message from client to web server, ONLY FORWARD EXACT MESSAGE -webserveraddr
	
	# Receive the response message from the web server
	response = webSocket.recv(BUFFER_SIZE)
	print("Header in bytes received from web server:")
	print(response)
	clientSocket.send(response) 					# Send header response from server to client

	# Read requested image or html file if any from server and send back to client
	dataBuffer = bytes("", encoding = FORMAT)
	while True:
		responseBuffer = webSocket.recv(BUFFER_SIZE)
		if not responseBuffer:
			break
		dataBuffer += responseBuffer
	clientSocket.send(dataBuffer)
	clientSocket.close()

proxySocket.close()