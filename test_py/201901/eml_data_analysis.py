#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
import datetime
from urllib import parse, request
import json
import re
import time
import base64
import hashlib
import eml_parser
import logging
logger = logging.getLogger("eml_file_analysis")
logger.setLevel(logging.DEBUG)

def logging_in():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	#输出到文件
	fh = logging.FileHandler("log_get_eml_data.log")
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

		time.sleep(1)
		
		url = "http://192.168.201.110:4444/receive"
		req = request.Request(url, formdata, headers=header_dict)
		res = request.urlopen(req).read().decode('utf-8')
		#jsonData = json.loads(res)
		os.system("rm ./attachment_file/* attachment_file.tar.xz attachment_file.tar -rf")
		logger.info("ask es data:"+res)
	except Exception as e:
		logger.warning("ask es is error:"+str(e))

def analysis_eml_data(the_data):
	eml_data_dict = {}
	try:
		#the_data_attachment = the_data["attachment"]
		#the_data_body = the_data["body"]
		eml_data_dict["index"] = "email_parse"

		the_data_header = the_data["header"]
		timestamp = the_data_header["date"].timestamp()
		timestamp_str = str(int(timestamp))
		eml_data_dict["timestamp"] = timestamp_str
		eml_data_dict["email"] = the_data_header["from"]
		type_str = the_data_header["from"].split("@")[1]
		eml_data_dict["type"] = type_str
		eml_data_dict["id"] = the_data_header["from"]+"_"+timestamp_str
		eml_data_dict["title"] = the_data_header["subject"]
		eml_data_dict["host_ip"] = the_data_header["received_ip"][0]

		the_data_header_header = the_data_header["header"]
		eml_data_dict["nickname"] = the_data_header_header["from"][0]
		eml_data_dict["user-agent"] = the_data_header_header["received"][0]
		eml_data_dict["dest_emails"] = the_data_header_header["to"][0].split(", ")
		with open("./attachment_file.tar.xz", "rb") as f:
			content_file = f.read()
		eml_data_dict["content_file"] = str(base64.b64encode(content_file), encoding='utf-8')
	except Exception as e:
		logger.warning("the file analysis error:"+str(e))
	return eml_data_dict

def get_attachment(the_file, the_data):
	try:
		filename_hash_dict = {}
		for obj in the_data["attachment"]:
			filename_hash_dict[obj["hash"]["sha512"]] = obj["filename"]

		with open(the_file, "rb") as f:
			content_data = f.read()
		patter = r'Content-Disposition: attachment.*?\r\n\r\n(.*?)\r\n------=_Part'
		patter_bytes = bytes(patter, encoding = "utf8")
		res = re.findall(patter_bytes, content_data, re.S|re.I)
		if len(res) > 0:
			for data_base64 in res:
				data_byte = base64.b64decode(data_base64)
				hash_sha512 = hashlib.sha512()
				hash_sha512.update(data_byte)
				hash_str = hash_sha512.hexdigest()
				filename_str = filename_hash_dict[hash_str]
				filename_path = os.path.join("./attachment_file", filename_str)
				with open(filename_path, "wb") as f:
					f.write(data_byte)
		else:
			logger.warning("the eml not have attachment:"+the_file)
			return
		os.system("tar -cvf attachment_file.tar ./attachment_file; xz -z attachment_file.tar")
	except Exception as e:
		logger.warning("the eml get attachment error:"+str(e))

def eml_analysis(the_file):
	os.system("rm ./attachment_file/* attachment_file.tar attachment_file.tar.xz -rfd")
	with open(the_file, "rb") as f:
		raw_email = f.read()
	try:
		logger.info("the eml file start:"+the_file)
		parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)
		get_attachment(the_file, parsed_eml)
		eml_data_dict = analysis_eml_data(parsed_eml)
		send_data_es(the_file, eml_data_dict)
	except Exception as e:
		logger.warning("the eml file is error:"+str(e))

def get_file_list(src_path):
	#读取目的文件夹列表
	eml_file_list = []
	target_list = os.listdir(src_path)
	for target_path in target_list:
		files_path = os.path.join(src_path, target_path)
		if os.path.isdir(files_path):
			#下层目录
			get_file_list(files_path)
		elif os.path.isfile(files_path):
			ext_str = os.path.splitext(files_path)[1].lower()
			if ext_str == ".eml":
				eml_analysis(files_path)
			else:
				logger.info("other file:"+files_path)
		else:
			logger.info("other files_path:"+files_path)

def main():
	#获取文件
	src_path = "/home/w123/ry/email/邮件"
	get_file_list(src_path)
	#file_name = "/home/w123/ry/email/邮件/系统退信(85).eml"
	#eml_analysis(file_name)

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
