#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText

class Mailer:
	def __init__(self, opts):
		self.reporting = opts.report
		self.email = opts.email
		self.password = opts.password
		if self.reporting == 'gmail':
			self.server = smtplib.SMTP(host="smtp.gmail.com", port=587)
			self.server.starttls()
			self.server.login(self.email, self.password)
		if self.reporting == 'email':
			self.server = smtplib.SMTP('localhost')
	
	def send(self, msg):
		message = """\
		Subject: Server Monitor output
		
		"""
		message = message + msg
		self.server.sendmail(self.email, self.email, message)
		self.server.quit()
