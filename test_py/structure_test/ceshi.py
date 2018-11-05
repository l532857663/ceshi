#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json

import data.ceshi as Dceshi
import func.ceshi as Fceshi

def main():
	print("ceshi")
	tmp_data = Dceshi.ceshi
	json_str = json.dumps(tmp_data)
	print("source data:", tmp_data)
	print("string data:", json_str)
	for name in tmp_data:
		print("source data->name:", name)
		print("source data->value:", tmp_data[name])
	
	Fceshi.ceshi()

if __name__ == "__main__" :
	print("START")
	main()
	print("END")
