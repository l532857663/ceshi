#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import sys
import numpy as np
from pyhanlp import *
import keras.preprocessing.text as T
from keras.preprocessing.text import Tokenizer

class DataProcessing:
    file_str_arr = []
    file_tag_arr = []

    def getContents(self, file_data_arr):
        self.file_str_arr = []
        #数据语句分词
        for line in file_data_arr:
            analysis_doc = HanLP.segment(line[0].decode())
            the_doc = []
            for word in analysis_doc:
                word_str = str(word)
                every_arr = word_str.split("/")
                the_doc.append(every_arr[0])
            line_str = ""
            for w in the_doc:
                line_str += w + " "
            self.file_str_arr.append(line_str[:-1])
        return self.file_str_arr

    def getTags(self, file_data_arr):
        line_arr = []
        tag_str = ""
        for line in file_data_arr:
            tag_str += line[1].decode() + " "
        line_arr.append(tag_str[:-1])
        tokenizer = Tokenizer(num_words=None)
        tokenizer.fit_on_texts(line_arr)
        self.file_tag_arr = tokenizer.texts_to_sequences(line_arr)
        return self.file_tag_arr

def getTags(tag_str):
    line_arr = []
    line_arr.append(tag_str[:-1])
    tokenizer = Tokenizer(num_words=None)
    tokenizer.fit_on_texts(line_arr)
    number_line_arr = tokenizer.texts_to_sequences(line_arr)
    return number_line_arr

if __name__ == "__main__":
    filename = sys.argv[1]
    filename_tag = sys.argv[2]
    with open(filename, "r") as f:
        file_data_arr = f.readlines()
    tag_str = ""
    with open(filename_tag, "r") as f:
        file_tag_arr = f.readlines()
    for line in file_data_arr:
        tag_str += line[:-1] + " "
    DP = DataProcessing()
    file_str_arr = DP.getContents(file_data_arr)
    tag_arr = getTags(tag_str)
