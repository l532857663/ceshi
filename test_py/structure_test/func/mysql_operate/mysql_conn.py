#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import pymysql

'''
	mysql数据库链接
'''

class Mysql_conn:
	
	def __init__(self, config_data):
		config_obj = {
			"host":None,
			"username":None,
			"password":'',
			"database":None,
			"port":0,
			"unix_socket":None,
			"charset":'',
		}
		config_list = ["host", "username", "password", "database", "port", "unix_socket", "charset"]
		config_arr = []
		for key in config_list:
			if key not in config_data:
				logging.info("config %s is not have!" % (key))
				config_arr.append(config_obj[key])
				continue
			config_arr.append(config_data[key])
		print(config_arr)
		try:
			self.Mydb = pymysql.Connect(*config_arr)
		except Exception as e:
			print("Mysql_conn 连接错误!", e)

	def __del__(self):
		logging.info("__del__")
		self.Mydb.close()

	def _do_choose(self, func):
		print("choose func:", func)
		logging.info("Mydb:", self.Mydb)
