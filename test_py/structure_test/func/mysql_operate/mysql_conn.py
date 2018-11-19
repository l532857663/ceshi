#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import pymysql

'''
	mysql数据库链接
'''

class Mysql_conn:
	choose_obj = {
		"show" : "self._show_sql",
		"do" : "self._do_sql"
	}
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
		logging.info(config_arr)
		try:
			self.Conn = pymysql.Connect(*config_arr)
		except Exception as e:
			print("Mysql_conn 连接错误!", e)

	def __del__(self):
		logging.info("__del__")
		self.Conn.close()
	
	def _create_sql(self, method, data_dict):
		print("method:", method)
		print("data_dict:", data_dict)
		the_sql = "show databases"
		row, res = exec(self.choose_obj[method] + '(the_sql)')
		if not res:
			print("sql do it error")
	
	def _show_sql(self, the_sql):
		# 获取游标
		res = True
		cursor = self.Conn.cursor()
		try:
			cursor.execute(the_sql)
		except Exception as e:
			print("show_sql mysql error: ", e)
			res = False
		row = cursor.fetchall()
		return row, res

	def _do_sql(self, the_sql):
		# 获取游标
		res = True
		cursor = self.Conn.cursor()
		try:
			for sql, data in the_sql:
				print("sql:", sql)
				print("data", data)
				cursor.execute(sql, data)
		except Exception as e:
			print("do_sql mysql error: ", e)
			# 事务回滚
			self.Conn.rollback()
			res = False
		else:
			self.Conn.commit()
		cursor.close()
		return _, res
