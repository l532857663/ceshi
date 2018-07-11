#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import time
from evaluate_server.get_data import DataSubscripting

HTTP_HOST_NAME = "192.168.11.139"
HTTP_PORT = 8901

'''
http通信类，通过http协议传输.

class HttpHandle(BaseHTTPServer.BaseHTTPRequestHandler):
'''
class HttpHandler(BaseHTTPRequestHandler):
	sendReply = False
	DS = DataSubscripting()
	path = ""

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	
	def _send_massage(self,res):
		try:
			result_string = res.encode("utf-8")
			self._set_headers
			self.wfile.write(result_string)
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	
	def _json_encode(self, data):
		array = data.split('&')
		json_data = {}
		for item in array:
			item = item.split('=', 1)
			json_data[item[0]] = item[1]
		return json_data

	def _get_handler(self, data):
		json_data = self._json_encode(data)
		print(json_data)
		if json_data['username'] == "admin":
			self.sendReply = True
			print(json_data["data_str"])
			res = self.DS.sentenceSegmentation(json_data["data_str"])
		else:
			res = json_data["data_str"]
			self._send_massage()

		if self.sendReply == True:
			self._send_massage(res)
	
	def do_GET(self):
		querypath = urlparse(self.path)
		filepath, query = querypath.path, querypath.query
		self.path = filepath
		if filepath == "/":
			self._get_handler(query)

if __name__ == "__main__":
	print("http server test: {}:{}".format(HTTP_HOST_NAME, HTTP_PORT))
	httpd = HTTPServer((HTTP_HOST_NAME, HTTP_PORT), HttpHandler)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print("Begin time: {}".format(localtime))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print("End time: {}".format(localtime))
