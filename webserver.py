# -*- coding: utf-8 -*-
# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverHost = "127.0.0.1"									
FORMAT = "utf-8"
BUFFER_SIZE = 4096
#serverHost = gethostbyname(gethostname())
serverSocket.bind((serverHost, serverPort)) 	# Input must be a tuple
serverSocket.listen(1) 								# Listening for connections

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()             
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(BUFFER_SIZE)
	
    	# Outputs message received from the client
		print("Message in bytes received from client or proxy: ", message)
	
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1]

		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
		f = open(filename[1:], 'rb')

		# Store the entire content of the requested file in a temporary buffer
		temporaryBuffer = f.read()
		f.close()

		# Send the HTTP response header line to the connection socket
		http_version = 'HTTP/1.1'
		status_code = 200
		reason_phrase = 'OK'
		content_length = len(temporaryBuffer)
		header_lines = [
			f'{http_version} {status_code} {reason_phrase}',
			'Content-Type: text/html',
			f'Content-Length: {content_length}',
			'\r\n'
		]
		header = '\r\n'.join(header_lines).encode(FORMAT)
		connectionSocket.sendall(header)

		print("Header in bytes sent to client or proxy: ", header)

		# Send the content of the requested file to the connection socket
		for i in range(0, len(temporaryBuffer)):  
			connectionSocket.send(temporaryBuffer[i:i+1])
		connectionSocket.send("\r\n".encode())
		
		# Close the client connection socket
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		http_version = 'HTTP/1.1'
		status_code = 404
		reason_phrase = 'Not Found'
		content_length = len(temporaryBuffer)
		header_lines = [
			f'{http_version} {status_code} {reason_phrase}',
			'Content-Type: text/html',
			f'Content-Length: {content_length}',
			'\r\n'
		]
		header = '\r\n'.join(header_lines).encode(FORMAT)
		connectionSocket.sendall(header)

		# Close the client connection socket
		connectionSocket.close()

serverSocket.close()