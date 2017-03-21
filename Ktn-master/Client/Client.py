# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
import json
import sys, codecs

class Client:
	"""
	This is the chat client class
	"""

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""

		# Set up the socket connection to the server
		self.host = host
		self.server_port = server_port
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.run()

	def run(self):
		# Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		self.thread = MessageReceiver(self, self.connection)
		self.thread.start()
		
		while True:
			text = input().split(' ', 1)
			if(len(text) > 0 and len(text) < 3):
				if(len(text)==1):
					text.append('')
				if(text[0] == 'login'):
					payload=json.dumps({'request': 'login', 'content': text[1]})
					self.send_payload(payload)
				elif(text[0] == 'logout'):
					self.disconnect()
				elif(text[0] == 'names'):
					payload=json.dumps({'request': 'names'})
					self.send_payload(payload)
				elif(text[0] == 'help'):
					payload=json.dumps({'request': 'help'})
					self.send_payload(payload)
				elif(text[0] == 'msg'):
					payload=json.dumps({'request': 'msg', 'content': text[1]})
					self.send_payload(payload)
				else:
					print('Unknown command, type "help" for help')
			else:
				print('Unknown command, type "help" for help')


	def disconnect(self):
		payload=json.dumps({'request': 'logout'})
		self.send_payload(payload)
		sys.exit()

	def receive_message(self, message):
		recv = message
		if(recv['response'] == 'info'):
			print('[Info]', recv['content'])
		elif(recv['response'] == 'error'):
			print('[Error]', recv['content'])
		elif(recv['response'] == 'msg'):
			print(recv['sender']+':', recv['content'])
		elif(recv['response'] == 'history'):
			for message in recv['content']:
				self.receive_message(message)
		else:
			print('Unknown server message:', recv)
		pass

	def send_payload(self, data):
		self.connection.send(bytes(data, 'UTF-8'))


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.
	No alterations is necessary
	"""
	connect_ip=input("Enter server ip to connect: ")
	print('Type "login <username>" to log in')
	client = Client(connect_ip, 9998)
