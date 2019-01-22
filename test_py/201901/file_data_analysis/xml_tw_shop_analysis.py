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

order_payway = {
	"1" : "銀行ATM轉帳",
	"2" : "銀行匯款",
	"3" : "郵局ATM轉帳",
	"4" : "郵局匯款",
	"5" : "現金掛號",
	"6" : "郵局現金袋服務",
	"7" : "網路銀行轉帳",
	"8" : "7-11取貨便",
	"13" : "貨到付款(宅配)",
	"10" : "無摺存款",
	"12" : "宅配貨到付款150",
}

type_dict = {
	"手機號" : "telphone",
	"姓" : "lastname",
	"名" : "firstname",
	"性別" : "sex",
	"帳號" : "username",
	"郵箱" : "email",
	"地址" : "address",
	"生日" : "birthday",
	"訂單號" : "order_number",
	"付款方式" : "payment_method",
	"取貨方式" : "pick_up_method",
	"de_order_payinf2" : "payment_information",
	"訂單總額" : "order_total",
	"訂單日期" : "order_data",
	"收貨人姓名" : "consignee_name",
	"收貨人郵編" : "consignee_zip",
	"收貨人地址" : "consignee_address",
	"訂單狀態" : "order_status",
	"訂單數量" : "order_quantity",
	"產品名稱" : "product_name", 
	"產品價格" : "product_price", 
}

def logging_in():
	#输出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.WARNING)
	#输出到文件
	fh = logging.FileHandler("log_get_xls3_data.log")
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

def analysis_xls_data(row_key, the_data):
	xls_data_dict = {}
	try:
		for key in type_dict.keys():
			type_str = type_dict[key]
			index = row_key.index(key)
			if key == "訂單日期" or key == "生日":
				if type(the_data[index]) == float:
					tmp_data = str(int((the_data[index]-70*365-19)*86400-8*3600))
				elif type(the_data[index]) == str:
					if the_data[index] == "0000-00-00" or the_data[index] == "":
						continue
					timeArray = time.strptime(the_data[index], "%Y-%m-%d %H:%M:%S")
					tmp_data = str(int(time.mktime(timeArray)))
				else:
					return
			elif key == "付款方式":
				if not str(int(the_data[index])) in order_payway.keys():
					continue
				tmp_data = order_payway[str(int(the_data[index]))]
			elif type(the_data[index]) == float:
				tmp_data = str(int(the_data[index]))
			else:
				tmp_data = the_data[index]
			if tmp_data == "":
				continue
			xls_data_dict[type_str] = tmp_data
		xls_data_dict["index"] = "order_information"
		xls_data_dict["type"] = "_doc"
		xls_data_dict["id"] = "unknow_{}_{}_{}".format(xls_data_dict["username"], xls_data_dict["order_number"], xls_data_dict["order_data"])
		xls_data_dict["fake_type"] = "taiwan"
	except Exception as e:
		xls_data_dict = {}
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
			print("sheet '{}'页, nrows '{}'行, ncols '{}'列\n".format(sheet_name,nrows,ncols))
			#判断有无内容
			if (nrows + ncols) < 2:
				logger.info("the file not have data")
				continue
			row_key = sh.row_values(0)
			#获取各行数据
			for i in range(2, nrows):
				row_data = sh.row_values(i)
				xls_data_dict = analysis_xls_data(row_key, row_data)
				#print(xls_data_dict)
				if not xls_data_dict:
					logger.info("the row is error: "+str(i+1))
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
	src_path = "/home/w123/files/olddata2/tw-shop"
	get_file_list(src_path)
	#xls_analysis("/home/w123/files/olddata2/tw-shop/myorder_angel_333.xls")

if __name__ == "__main__":
	print("START")
	logging_in()
	main()
	print("END")
