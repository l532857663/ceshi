#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import data.send_email as Ds_email
import func.send_email as Fs_email

def create_info():
	# 输入Email地址和口令:
	from_addr = input('From: ')
	password = input('Password: ')
	# 输入收件人地址:
	to_addr = input('To (list:a,b,c): ')
	# 输入SMTP服务器地址:
	smtp_server = input('SMTP server: ')
	content = input('Send content: ')
	return from_addr, password, to_addr, smtp_server, content

if __name__ == "__main__" :
	print("Start")

	#获取数据
#	from_addr, password, to_addr, smtp_server, content = create_info()
	from_addr = Ds_email.config["from_addr"]
	password = Ds_email.config["password"]
	to_addr = Ds_email.config["to_addr"]
	smtp_server = Ds_email.config["smtp_server"]
	content = Ds_email.config["content"]

	SE_obj = Fs_email.Send_email(from_addr, password, to_addr, smtp_server)
	SE_obj.send_email(content)
	
	print("End")
