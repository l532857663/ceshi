#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import sys
from pyhanlp import *
import keras
import random
import numpy as np
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer

class DataSubscripting:

	def __init__(self):
		self.alldoc = [] #文本分词内容
		self.thedoc = [] #文本分词后，不带标点内容
		self.np_thedoc
	
#分词处理
	def sentenceSegmentation(self, data_string):
		analysis_doc = []
		if data_string == "":
			err = "无数据传入"
			return err

		analysis_doc = HanLP.segment(data_string)
		print("1",analysis_doc)

		for word in analysis_doc:
			word_str = str(word)
			every_arr = word_str.split("/")
			if every_arr[1] == "w":
				self.alldoc.append(every_arr[0])
			else:
				self.alldoc.append(every_arr[0])
				self.thedoc.append(every_arr[0])
		self.np_thedoc = np.array(self.thedoc)
		print(self.np_thedoc)

	def dataType(self):
		tokenizer = Tokenizer(num_words=15000)
		x_train = tokenizer.sequences_to_matrix(self.np_thedoc, mode='binary')
		print('x_train shape:', x_train.shape)
		my_model = load_model(filepath[1])
		config = my_model.get_config()
		my_model.from_config(config)
		my_model.summary()
		preds = my_model.predict_classes(self.np_thedoc, verbose=0)

if __name__ == "__main__":
    strData = sys.argv[1]
    DS = DataSubscripting()
    ss = DS.sentenceSegmentation(strData)
    print(ss)
