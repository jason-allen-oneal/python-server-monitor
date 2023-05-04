#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
import email.utils

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
        message = MIMEText(msg.strip(), 'plain', 'utf-8')
        message['From'] = self.email
        message['To'] = self.email
        message['Subject'] = 'Server Monitor output'
        message['Message-ID'] = email.utils.make_msgid()
        with self.server as smtp:
            smtp.send_message(message)
