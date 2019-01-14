#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import base64
from urllib import parse, request
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

def str_byte():
	str_a = b"afcsaaswffv12"
	print("str_a type:", type(str_a))
	print("str_a:", str_a)
	print("str_a str:", str(str_a, encoding="utf-8"))
	for data_alone in str_a:
		print("data_alone str:", chr(data_alone))
	str_aa = {"asd":"请求党和国家为分配到"}
	sss = parse.urlencode(str_aa).encode('utf-8')
	print(sss)
	sss1 = parse.urlencode(str_aa)
	print(sss1)
	print(str_a.decode("utf-8"))

def join_split():
	content_list = []
	content_str = "\n\n".join(split_list)
	content_str1 = "\n\n".join(content_list)
	print("'"+content_str+"'")
	print("'"+content_str1+"'")

def main():
	print("main start")
	#文件操作
#	file_operation()
	#logging_test()
	#mk_path()
	#str_byte()
	join_split()
	print("main end")


if __name__ == "__main__":
	print("START")
	main()
	print("END")
