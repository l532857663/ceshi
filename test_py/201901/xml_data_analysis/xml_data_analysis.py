#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
from urllib import parse, request
#import json
import time
import random

#from sql_operating import DatabaseOperating

import xlrd

import logging
logger = logging.getLogger("file_data_analysis")
logger.setLevel(logging.DEBUG)

#DO = DatabaseOperating()

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

def model_sql_ceshi():
    sqlStr = "select corpus_data_detail,corpus_data_evaluate from `%s`"
    data = DO.sqlSelect(sqlStr, "ceshi_corpus_data")
    with open("model_wt1.h5", "rb") as f:
        model_weights = f.read()
    #把数据插入数据库
    time_now = int(time.time())
    # model_weights_string = "0x" + model_weights.hex ()
    model_weights_string = "UNHEX('" + model_weights.hex () + "')"
    sqlStr = "insert into `Lyrical_model_base` (`model_base_weights`,`model_base_timestamp`,`model_base_remark`) values (" + model_weights_string + ",%s,%s)"
    res = DO.sqlAdd(sqlStr, time_now, "ce shi yi xia")
    if res == "OK":
        print("OJBK")
    else:
        print(res, sqlStr)

def create_table(sqltablename):
    sqlStr = "create table if not exists `" + sqltablename + "_corpus_data` (\
            `corpus_data_id` INT UNSIGNED AUTO_INCREMENT,\
            `corpus_data_title` TEXT,\
            `corpus_data_detail` BLOB NOT NULL,\
            `corpus_data_evaluate` BLOB NOT NULL,\
            PRIMARY KEY (`corpus_data_id`)\
            )ENGINE=InnoDB DEFAULT CHARSET=utf8"
    print(sqlStr)
    #res = DO.tableAdd(sqlStr)
    res = "OK"
    if not res == "OK":
        print("数据库添加失败")

def file_sql_ceshi(sqltablename, file_data_content):
    #数据导入数据库
    title = file_data_content[0].encode()
    detail = file_data_content[1].encode()
    evaluate = file_data_content[2].encode()
    sqlStr = title + b"|-*-|" + detail + b"|-*-|" + evaluate + b"\n"
    return sqlStr

def xls_analysis(the_file, data_list, type_str):
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
			print("sheet '{}'页, nrows '{}'行, ncols '{}'列\n".format(sheet_name,nrows,ncols))
			#判断有无内容
			if (nrows + ncols) < 2:
				logger.info("the file not have data")
				continue
			#获取各行数据
			for i in range(1, nrows):
				row_data = sh.row_values(i)
				row_data.append(type_str)
				data_list.append(row_data)
	except Exception as e:
		logger.warning("the file is error:"+str(e))

def get_file_list(src_path):
	#读取目的文件夹列表
	data_list = []
	target_list = os.listdir(src_path)
	for target_path in target_list:
		files_path = os.path.join(src_path, target_path)
		if os.path.isdir(files_path):
			#下层目录
			get_file_list(files_path)
		elif os.path.isfile(files_path):
			ext_str = os.path.splitext(files_path)[1].lower()
			if ext_str == ".xls":
				xls_analysis(files_path, data_list, "非垃圾")
			elif ext_str == ".xlsx":
				xls_analysis(files_path, data_list, "垃圾")
			else:
				logger.info("other file:"+files_path)
			print("the file end:"+files_path)
		else:
			logger.info("other files_path:"+files_path)
	print(len(data_list))
	print(data_list[0])
	random.shuffle(data_list)
	sqltablename = "initial_test"
	#create_table(sqltablename)
	with open("./insert_sql.txt", "wb") as f:
		for data in data_list:
			query_str = file_sql_ceshi(sqltablename, data)
			f.write(query_str)

def main():
	#获取文件
	src_path = "/home/w123/files/woxun"
	get_file_list(src_path)
	#xls_analysis("/home/w123/files/woxun/2.xlsx")

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
