#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import base64
import logging
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)

split_list = ["LS0tLQ==", "CQ==", "ICAgIA=="]
relation_dict = {
	"LS0tLQ==" : "hengxian",
	"CQ==" : "zhibiao",
	"ICAgIA==" : "kongge",
}

def logging_test():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	#输出到文件
	fh = logging.FileHandler("log2.log")
	fh.setLevel(logging.DEBUG)
	#设置日志格式
	fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
	ch.setFormatter(fomatter)
	fh.setFormatter(fomatter)
	logger.addHandler(ch)
	logger.addHandler(fh)

def mk_path():
	for name in relation_dict:
		print(name)
	logger.debug("debug message sadawwa")
	logger.info("info message adcsfef")
	logger.warning("warning message sadadwfa")

def file_operation():
	with open("ceshi.txt", "wb") as f:
		f.write(b"14654aw----awdasc----q54aw----awd--------aaa")
	with open("ceshi.txt", "rb") as f:
		content = f.readline()
	print("content:", content)
	res_dict = {}
	for split_str in split_list:
		split_byte = base64.b64decode(split_str.encode('utf-8'))
		#content_list = content.split(split_byte)
		res_dict[split_str] = len(content.split(split_byte))
	print(res_dict)

def main():
	print("main start")
	#文件操作
#	file_operation()
	logger.debug("debug message")
	logger.info("info message")
	logger.warning("warning message")
	logging_test()
	mk_path()
	print("main end")


if __name__ == "__main__":
	print("START")
	main()
	print("END")
