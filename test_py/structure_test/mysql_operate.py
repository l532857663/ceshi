#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, sys
import json
import logging
#logging.basicConfig(level=logging.INFO)

import conf.mysql_operate as Cmysql
import func.mysql_operate as Mysql_obj
#import func.mysql_operate.mysql_conn as Fsql_conn

def main():
	print("main")
	#获取配置数据
	config = Cmysql.conn_config
	logging.info(config)

	#链接数据库
#	print(Mysql_obj.mysql_conn)
	mysql_conn = Mysql_obj.mysql_conn.Mysql_conn(config)

if __name__ == "__main__" :
	print("START")
	main()
	print("END")
