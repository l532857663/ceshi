#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
ceshi模块 方法包
'''

import os,sys

def ceshi():
	print("Hello World")
	_the_file_path = os.getcwd()
	_the_file_name = os.path.basename(os.path.realpath(__file__))
	_func_name = sys._getframe().f_code.co_name
	print("file path:", _the_file_path, _the_file_name)
	print("func name:", _func_name)

if __name__ == "__main__" :
	ceshi()
