#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import os,sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse,unquote
import time

from evaluate_server.fit_model import ModelModify


HTTP_HOST_NAME = "192.168.11.133"
HTTP_PORT = 8932

'''
http通信类，通过http协议传输.

'''
class HttpHandler(BaseHTTPRequestHandler):
    sendReply = False
    MM = ModelModify()
    path = ""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_massage(self,res):
        try:
            result_string = res.encode("utf-8")
            print("The end")
            self._set_headers()
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

    def _post_handler(self, data):
        print("sadasd:",data)
        json_data = self._json_encode(data)
        if json_data['username'] == "admin":
            self.sendReply = True
        
            ok = MM.modelInterface(json_data['dbname'], json_data['do_type'], model_id=json_data['model_id'], model_remark=json_data['model_remark'])
            if not ok:
                print("modelInterface error")
                res = json_data["data_str"]
                self._send_massage(res)

        if self.sendReply == True:
            self._send_massage(result)

    def do_POST(self):
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        print(querypath)
        self.path = filepath
        if filepath == "/Fit":
            print("The start:'"+query+"'")
            self._post_handler(query)
        else:
            self.send_error(404,'File Not Found: %s' % self.path)

    def send_error(self, type_code, res):
        result_string = res.encode("utf-8")
        self._set_headers()
        self.wfile.write(result_string)

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
