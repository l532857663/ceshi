#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import time

HTTP_HOST_NAME = "192.168.11.139"
HTTP_PORT = 8901

'''
http通信类，通过http协议传输.

class HttpHandle(BaseHTTPServer.BaseHTTPRequestHandler):
'''
class HttpHandler(BaseHTTPRequestHandler):
	sendReply = False

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	
	def _json_encode(self, data):
		array = data.split('&')
		json_data = {}
		for item in array:
			item = item.split('=', 1)
			json_data[item[0]] = item[1]
		return json_data

	def _get_handler(self, data):
		json_data = self._json_encode(data)
		print(json_data["username"])
		print(self.sendReply)

		if self.sendReply == True:
			print("ceshi")
			try:
				print("ceshi1")
				result_str = "测试0.0".encode("utf-8")
				time.sleep(50)
				print(result_str)
				self._set_headers
				self.wfile.write(result_str)
			except IOError:
				self.send_error(404,'File Not Found: %s' % self.path)
			print("ceshi2")
	
	def do_GET(self):
		querypath = urlparse(self.path)
		filepath, query = querypath.path, querypath.query
		if filepath == "/":
			self.sendReply = True
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
