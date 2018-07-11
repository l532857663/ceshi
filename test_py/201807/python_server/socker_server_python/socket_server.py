#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python的socket协议通信，通过socket请求访问

startServer 开启server，监听端口，多线程进行
"""
import os,sys
import socket
import time

HOST_NAME = "192.168.11.139"
PORT_NUMBER = 8901


class SocketHttpServer:
	def __init__(self):
		print("Socket server test: {}:{}".format(HOST_NAME,PORT_NUMBER))
		localtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		print("Start time: {}".format(localtime))
		self.startServer()
		print("End time: {}".format(localtime))

	def startServer(self):
		sk = socket.socket(
			socket.AF_INET,
			socket.SOCK_STREAM
		)

		sk.bind((HOST_NAME,PORT_NUMBER))
		sk.listen(5)

		while True:
			try:
				client_sk, client_address = sk.accept()
				self.connectServer(client_sk, client_address)
			except Exception as err:
				print(err)
				client_sk.close()
	
	def connectServer(self, client_sk, address):
		print("address is: %s" % str(address))
		requestList = client_sk.recv(1024).decode().split("\r\n")
		# 解析HTTP请求报文
		ret = parseReq(requestList)
		response = getResponse(ret)

		# 返回HTTP响应报文
		client_sk.sendall(response.encode('utf-8'))
		client_sk.close()

if __name__ == "__main__":
	this_strat = SocketHttpServer()
