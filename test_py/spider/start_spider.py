#!/usr/bin/env python3
#!-*- coding:utf-8 -*-

import os,sys
import time

userid_list = ["KatzeGato1","A404411","bless_miles","ak47dealer","WilderMohn","baotong1932","papa_pahoo","hrw_chinese","ChenYun","Kenn_Zou","CaoChangqing","datomen","Yehuosi","xzs233"]
module_list = ["followers","following","information","likes","media","tweets","tweets_replies"]

def main():
	print("START\n")
	for userid in userid_list:
		for module in module_list:
			cmd_str = "python ./spider_twitter.py '" + userid + "' '" + module + "' 'qazxsw31154@gmail.com' '1qaz@WSX' 'http://192.168.201.110:4444/receive'"
			print ("the module:", cmd_str)
			os.system(cmd_str)
	print("END\n")

if __name__ == "__main__":
	main()
