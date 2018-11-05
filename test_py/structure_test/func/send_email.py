#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

class Send_email:
	def __init__(self, from_addr, password, to_addr, smtp_server):
		self.from_addr = from_addr
		self.password = password
		self.to_addr = to_addr
		self.to_addr_arr = to_addr.split(",")
		self.smtp_server = smtp_server

	def _format_addr(self, s):
		name, addr = parseaddr(s)
		print("name:", name)
		print("addr:", addr)
		return formataddr((Header(name, 'utf-8').encode(), addr))

	def send_email(self, _content, _type="plain", _charset="utf-8"):
		msg = MIMEText(_content, _type, _charset)
		msg['From'] = self._format_addr('Python爱好者 <%s>' % self.from_addr)
		msg['To'] = self._format_addr('管理员 <%s>' % self.to_addr)
		msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

		# SMTP协议默认端口是25
		server = smtplib.SMTP(self.smtp_server, 25)
		server.set_debuglevel(1)
		server.login(self.from_addr, self.password)
#		server.sendmail(self.from_addr, self.to_addr_arr, msg.as_string())
		server.quit()
