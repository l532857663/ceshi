#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
from urllib import parse, request
#import json
import re
import time
import logging
logger = logging.getLogger("file_data_analysis")
logger.setLevel(logging.DEBUG)

def logging_in():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	#输出到文件
	fh = logging.FileHandler("log_get_txt2_data.log")
	fh.setLevel(logging.INFO)
	#设置日志格式
	fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
	ch.setFormatter(fomatter)
	fh.setFormatter(fomatter)
	logger.addHandler(ch)
	logger.addHandler(fh)

def send_data_es(the_file, data):
	try:
		header_dict = {
			'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
			'Content-Type' : 'application/x-www-form-urlencoded',
			'Accept-Language' : 'zh-CN,zh;q=0.8',
			'Connection' : 'Keep-Alive'
		}
		formdata = parse.urlencode(data).encode('utf-8')

		url = "http://192.168.201.110:4444/receive"
		req = request.Request(url, formdata, headers=header_dict)
		res = request.urlopen(req).read().decode('utf-8')
		#jsonData = json.loads(res)
		logger.info("ask es data:"+res)
	except Exception as e:
		logger.warning("ask es is error:"+str(e))

def analysis_txt_data(the_data):
	txt_data_dict = {}
	try:
		tmp_data = {}
		if len(the_data) == 2:
			tmp_data["username"] = the_data[0].decode("utf-8", "ignore")
			tmp_data["password"] = the_data[1].decode("utf-8", "ignore")
			tmp_data["email"] = the_data[0].decode("utf-8")
		else:
			return
		txt_data_dict["index"] = "olddata"
		txt_data_dict["type"] = "tw"
		txt_data_dict["id"] = "username_{}_password_{}".format(tmp_data["username"], tmp_data["password"])
		txt_data_dict["username"] = tmp_data["username"]
		txt_data_dict["password"] = tmp_data["password"]
		txt_data_dict["email"] = tmp_data["email"]
	except Exception as e:
		print("error data:", the_data)
		logger.warning("the file analysis error:"+str(e))
	return txt_data_dict

def txt_analysis(the_file):
	try:
		print("the file start:"+the_file)
		logger.info("the file start:"+the_file)
		with open(the_file, "rb") as f:
			content_list = f.readlines()
		for line in content_list:
			patter_bytes = bytes(r'\ +', encoding = "utf-8")
			line = line.strip(b"\r\n")
			res = re.split(patter_bytes, line)
			txt_data_dict = analysis_txt_data(res)
			if not txt_data_dict:
				continue
			send_data_es(the_file, txt_data_dict)
	except Exception as e:
		logger.warning("the file is error:"+str(e))

def get_file_list(src_path):
	#读取目的文件夹列表
	target_list = os.listdir(src_path)
	for target_path in target_list:
		files_path = os.path.join(src_path, target_path)
		if os.path.isdir(files_path):
			#下层目录
			get_file_list(files_path)
		elif os.path.isfile(files_path):
			ext_str = os.path.splitext(files_path)[1].lower()
			if ext_str == ".txt":
				txt_analysis(files_path)
				print("the file end:"+files_path)
				logger.info("the file end:"+files_path)
			else:
				logger.info("other file:"+files_path)
		else:
			logger.info("other files_path:"+files_path)

def main():
	#获取文件
	src_path = "/home/w123/files/olddata2/台湾105W"
	get_file_list(src_path)
	#txt_analysis("/home/w123/files/olddata2/nccu.edu.tw/maaaalll.txt")

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
