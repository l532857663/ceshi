#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import sys
import numpy as np
from get_data import DataSubscripting
from save_model import SaveModel

class DataGeting:
	np_thefile = []

	def __init__(self, input_type, filename=None):
		self.DS = DataSubscripting()
		self.SM = SaveModel()
		#获取数据
		if input_type == "sql_data":
			self.type = "sql_data"
		elif input_type == "file_data":
			self.fileInput(filename)
		else:
			err = "Noting"
	
	def fileInput(self, filename):
		file_cut_arr = []
		with open(filename, "r") as f:
			file_data_arr = f.readlines()

		#数据语句分词
		for line in file_data_arr:
			line_arr = self.DS.sentenceSegmentation(line[:-1])
		self.np_thefile = np.array(self.DS.alldoc)
	
	def makeModel(self, tag_arr):
		self.SM.getData(self.np_thefile, tag_arr)
	
def getTags(filename):
	line_arr = []
	with open(filename, "r") as f:
		file_data_arr = f.readlines()
	for line in file_data_arr:
		line_arr.append(line[:-1])
	return np.array(line_arr)

if __name__ == "__main__":
	filename = sys.argv[1]
	filename_tag = sys.argv[2]
	DG = DataGeting("file_data", filename)
	tag_arr = getTags(filename_tag)
	DG.makeModel(tag_arr)
