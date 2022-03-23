import sys
from threading import Thread
import itertools
import socket
import ssl
from mailer import Mailer
import datetime
import json

class StatusCheck(Thread):
	def __init__(self, site, opts):
		Thread.__init__(self)
		self.site = site
		self.opts = opts
		self.mail = Mailer(opts)
	
	def run(self):
		data = self.performCheck()
		
		if self.opts.report == 'screen':
			print(data)
		elif self.opts.report == 'local':
			with open('monitor.log', 'a') as f: 
				f.write(json.dumps(data))
			f.close()
		else:
			print(str(json.dumps(data)))
			self.mail.send(str(json.dumps(data)))
	
	def performCheck(self):
		data = {
			'http': False,
			'https': False
		}
		
		if self.siteRunning():
			data['http'] = True
		
		if self.sslRunning():
			data['https'] = True
		
		return data
	
	def siteRunning(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.site, 80))
			return True
		except:
			return False

	def sslRunning(self):
		try:
			context = ssl.create_default_context()
			with socket.create_connection((self.site, 443)) as sock:
				with context.wrap_socket(sock, server_hostname=self.site) as ssock:
					return True
		except:
			return False