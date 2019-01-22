#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
from urllib import parse, request
#import json
import re
from bs4 import BeautifulSoup
import time
import logging
logger = logging.getLogger("file_data_analysis")
logger.setLevel(logging.DEBUG)

def logging_in():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	#输出到文件
	fh = logging.FileHandler("log_get_html1_data.log")
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

def analysis_html_data(the_data):
	html_data_dict = {}
	try:
		tmp_data = {}
		tmp_data["name"] = the_data[0]
		tmp_data["username"] = the_data[1]
		tmp_data["password"] = the_data[2]
		tmp_data["email"] = the_data[3]

		html_data_dict["index"] = "olddata"
		html_data_dict["type"] = "nccu.edu.tw"
		html_data_dict["id"] = "username_{}_password_{}".format(tmp_data["username"], tmp_data["password"])
		html_data_dict["name"] = tmp_data["name"]
		html_data_dict["username"] = tmp_data["username"]
		html_data_dict["password"] = tmp_data["password"]
		html_data_dict["email"] = tmp_data["email"]
	except Exception as e:
		print("error data:", the_data)
		logger.warning("the file analysis error:"+str(e))
	return html_data_dict

def html_analysis(the_file):
	try:
		print("the file start:"+the_file)
		logger.info("the file start:"+the_file)
		with open(the_file, "rb") as f:
			html = f.read()
		soup = BeautifulSoup(html, features ="lxml")
		print(soup.table)
		res_list = [
			["系統管理員", "adjournal", "adjournal2013", "chienyu@nccu.edu.tw"],
			["編委老師們", "nccumcr", "2013", ""],
			["房翠瑩", "fangzi", "0711", "fangzi0711@gmail.com"],
			["黃安琪", "angel", "25698", "angel25698@hotmail.com"],
			["吳佳珍", "joannawu", "323", "joannawu323@gmail.com"],
			["黃葳威", "vhuang", "29387220", "vhuang@nccu.edu.tw"],
			["陳鴻嘉", "hoop0113", "hsin0113", "hoop0113@gmail.com"],
			["臧國仁", "kjt1026", "1026", "kjt1026@nccu.edu.tw"],
			["系統管理員", "rts", "rts2013", "rtvjournal@gmail.com"],
			["系統管理員", "mcr", "MCR2013", "masscomm@nccu.edu.tw"],
		]
		print(res_list)
		for res in res_list:
			html_data_dict = analysis_html_data(res)
			send_data_es(the_file, html_data_dict)
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
			if ext_str == ".html":
				html_analysis(files_path)
				print("the file end:"+files_path)
				logger.info("the file end:"+files_path)
			else:
				logger.info("other file:"+files_path)
		else:
			logger.info("other files_path:"+files_path)

def main():
	#获取文件
	src_path = "/home/w123/files/olddata2/nccu.edu.tw"
	#get_file_list(src_path)
	html_analysis("/home/w123/files/olddata2/nccu.edu.tw/table1.html")

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
