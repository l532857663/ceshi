#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse,unquote
import time
from evaluate_server.get_data import DataGeting

HTTP_HOST_NAME = "192.168.11.139"
HTTP_PORT = 8931
DB_MODEL_NAME = "Lyrical_model_base"

'''
http通信类，通过http协议传输.

'''
class HttpHandler(BaseHTTPRequestHandler):
    sendReply = False
    DG = DataGeting(DB_MODEL_NAME)
    path = ""
    result_val = {}

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_massage(self):
        try:
            res = json.dumps(self.result_val)
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
            if len(item) < 2:
                self.send_error(200,'数据格式不正确')
                return
            json_data[item[0]] = item[1]
        return json_data

    def _post_handler(self):
        post_data = self.rfile.read(int(self.headers['content-length']))
        json_data = {}
        post_data = self._json_encode(post_data.decode("utf-8"))
        for key in post_data.keys():
            json_data[key] = unquote(post_data[key], encoding='utf-8', errors='replace')
        if json_data['username'] == "admin":
            self.sendReply = True

            data_str = json_data["data_str"]
            data_str = unquote(data_str, encoding='utf-8', errors='replace')
            print(data_str)
            res_json = self.DG.sentenceSegmentation(data_str)
            print(res_json)
            if res_json == "no string":
                self.result_val["res_code"] = "无数据传入"
            else:
                self.result_val["res_code"] = res_json
            print("The result:",json.dumps(self.result_val))
        else:
            self.result_val["res_code"] = json_data["data_str"]
            self._send_massage()

        if self.sendReply == True:
            self._send_massage()

    def do_POST(self):
        querypath = urlparse(self.path)
        filepath = querypath.path
        self.path = filepath
        if filepath == "/Evaluate":
            print("The start:")
            self._post_handler()
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
