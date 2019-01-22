#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
from urllib import parse, request
#import json
import time

import xlrd

import logging
logger = logging.getLogger("file_data_analysis")
logger.setLevel(logging.DEBUG)

def logging_in():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	#输出到文件
	fh = logging.FileHandler("log_get_xls1_data.log")
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

def analysis_xls_data(the_data):
	xls_data_dict = {}
	try:
		if type(the_data[1]) == float:
			the_data[1] = str(int(the_data[1]))
		xls_data_dict["index"] = "olddata"
		xls_data_dict["type"] = "881903.com"
		xls_data_dict["id"] = "username_{}_password_{}".format(the_data[0], the_data[1])
		xls_data_dict["username"] = the_data[0]
		xls_data_dict["password"] = the_data[1]
		xls_data_dict["email"] = the_data[0]
	except Exception as e:
		logger.warning("the file analysis error:"+str(e))
	return xls_data_dict

def xls_analysis(the_file):
	try:
		print("the file start:"+the_file)
		logger.info("the file start:"+the_file)
		file_xls = xlrd.open_workbook(the_file)
		for sheet_name in file_xls.sheet_names():
			sh = file_xls.sheet_by_name(sheet_name)
			#获取行数
			nrows = sh.nrows
			#获取列数
			ncols = sh.ncols
			#logger.info("sheet '{}'页, nrows '{}'行, ncols '{}'列\n".format(sheet_name,nrows,ncols))
			#判断有无内容
			if (nrows + ncols) < 2:
				logger.info("the file not have data")
				continue
			#获取各行数据
			for i in range(nrows):
				row_data = sh.row_values(i)
				xls_data_dict = analysis_xls_data(row_data)
				send_data_es(the_file, xls_data_dict)
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
			if ext_str == ".xls":
				xls_analysis(files_path)
				print("the file end:"+files_path)
			else:
				logger.info("other file:"+files_path)
		else:
			logger.info("other files_path:"+files_path)

def main():
	#获取文件
	src_path = "/home/w123/files/olddata2/881903.com"
	get_file_list(src_path)
	#xls_analysis("/home/w123/files/olddata2/881903.com/881903.com-1.xls")

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
