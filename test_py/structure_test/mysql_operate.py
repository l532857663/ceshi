#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, sys
import json
import logging
logging.basicConfig(level=logging.INFO)

import conf.mysql_operate as Cmysql
import func.mysql_operate as Mysql_obj
#import func.mysql_operate.mysql_conn as Fsql_conn

def create_data():
	data_dict = {
		"table":"tables",
	}
	return data_dict

def main():
	print("main")
	#获取配置数据
	config = Cmysql.conn_config
	logging.info(config)

	#链接数据库
	mysql_conn = Mysql_obj.mysql_conn.Mysql_conn(config)

	#操作数据库
	data_dict = create_data()
	logging.info(data_dict)
	mysql_conn._create_sql("show", data_dict)

def ceshi():
	the_sql = [("show %s",("tables"))]
	for (sql, data) in the_sql:
		print("sql:", sql)
		print("data", data)

if __name__ == "__main__" :
	print("START")
	main()
#	ceshi()
	print("END")
