#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from analysisDetail import detailAnalysis

class dataprocessing:
    '''
    '''
    def __init__(self, filepath):
        #获取输入文件和输出文件的文件名
        slope = filepath.index("|")
        inputfile, jsonfile = filepath[:slope], filepath[slope+1:]

        self.strList = [] #文本行列表
        self.strStr = ""  #文本内容字符串
        self.docList = [] #文本
        self.dict_doc = {}#文本下标字典

        with open(inputfile, "r") as f:
            self.strStr += f.read()
            self.strList = f.readlines()
        analy_obj = detailAnalysis(strStr)
        #分词处理
        for sent in strList:
            analy_doc = analy_obj.alldoc(sent)
            self.docList.append(analy_doc)
        #print("docList ", self.docList)
        #列表去重,生成下表向量
        all_doc = analy_obj.alldoc()
        i = 0
        all_doc = list(set(all_doc))
        all_doc.sort()
        for w in self.all_doc:
            self.dict_doc[w] = i
            i+=1
        #print (self.dict_doc)
        with open(jsonfile, "w") as f:
            f.write(str(self.dict_doc))
    
    def text_conversion (self):
        for sent in self.docList:
            print (sent)

if __name__ == "__main__":
    argvList = sys.argv[1:]
    inputfile = argvList[0]
    jsonfile = argvList[1]

    strList = []
    docList = []
    strStr = ""
    with open(inputfile, "r") as f:
        strStr += f.read()
        strList = f.readlines()
    analy_obj = detailAnalysis(strStr)
    #分词处理
    for sent in strList:
        analy_doc = analy_obj.alldoc(sent)
        docList.append(analy_doc)
    #print("docList ", docList)
    #列表去重,生成下表向量
    all_doc = analy_obj.alldoc()
    i = 0;dict_doc = {}
    all_doc = list(set(all_doc))
    all_doc.sort()
    for w in all_doc:
        dict_doc[w] = i
        i+=1
    #print (dict_doc)
    with open(jsonfile, "w") as f:
        f.write(str(dict_doc))
