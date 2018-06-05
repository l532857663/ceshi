#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import numpy as np

import jieba

class dataprocessing:
    '''
    #输入文件和输出文件的处理
    >>>dataprocessing(filestring)
    >>>
    '''
    def __init__(self, inputfile, jsonfile):
        self.strList = [] #文本行列表
        self.docList = [] #文本分词内容
        self.dict_doc = {}#文本下标字典
        self.x_index = [] #文本下表向量列表
        self.tagList = [] #标签内容
        self.dict_tag = {}#标签下标字典
        self.y_index = [] #标签下表向量列表

        self._doit(inputfile, jsonfile)

    def _doit (self, inputfile, jsonfile):
        in_file = inputfile.split("^*^")
        print ("path:", in_file)
        if len(in_file) == 2:
            input_file, input_tag = in_file[0], in_file[1]

        if input_file:
            with open(input_file, "r") as f:
                self.strList = f.readlines()
        if input_tag:
            with open(input_tag, "r") as f:
                tag_list = f.readlines()

        #分词处理
        _alldoc = []
        if self.strList:
            i = 0
            for sent in self.strList:
                analy_doc = list(jieba.cut(sent[:-1]))
                self.docList.append(analy_doc)
                for word in analy_doc:
                    _alldoc.append(word)
            #print("docList ", self.docList)
           
           #列表去重,生成下表向量
            _alldoc = list(set(_alldoc))
            _alldoc.sort()
            for w in _alldoc:
                self.dict_doc[w] = i
                i+=1
        
        if tag_list:
            j = 0
            for tag in tag_list:
                self.tagList.append(tag[:-1])
            _taglist = list(set(self.tagList))
            _taglist.sort()
            for w in _taglist:
                self.dict_tag[w] = j
                j+=1
        #print (self.dict_doc,self.dict_tag)

        #生成json字典
        str_json = str(self.dict_doc)+"\n"+str(self.dict_tag)
        with open(jsonfile, "w") as f:
            f.write(str_json)

        #输入数据进行转换
        self.text_conversion(self.docList, self.tagList)
    
    def text_conversion (self, contents, tags):
        for sent in contents:
            x = []
            for word in sent:
                if word in self.dict_doc.keys():
                    x.append(self.dict_doc[word])
            self.x_index.append(x)
        for tag in tags:
            self.y_index.append(self.dict_tag[tag])
        a = np.array(self.x_index)
        b = np.array(self.y_index)
        np.savez("./corpus/mydata1.npz", x=a, y=b)

if __name__ == "__main__":
    print("start")
