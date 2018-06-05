#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from analysisDetail import detailAnalysis

class dataprocessing:
    '''
    #输入文件和输出文件的处理
    >>>dataprocessing(filestring)
    >>>
    '''
    def __init__(self, filepath):
        #获取输入文件和输出文件的文件名
        slope = filepath.index("|")
        inputfile, jsonfile = filepath[:slope], filepath[slope+1:]

        self.strList = [] #文本行列表
        self.strStr = ""  #文本内容字符串
        self.docList = [] #文本分词内容
        self.dict_doc = {}#文本下标字典
        self.x_index = [] #文本下表向量列表
        self.tagList = [] #标签内容
        self.dict_tag = {}#标签下标字典
        self.y_index = [] #标签下表向量列表

        self._doit(inputfile, jsonfile)

    def _doit (self, inputfile, jsonfile):
        in_file = inputfile.split("^*^")
        input_file, input_tag = in_file[0], in_file[1]
        with open(input_file, "r") as f:
            self.strStr += f.read()
        with open(input_file, "r") as f:
            self.strList = f.readlines()
        with open(input_tag, "r") as f:
            tag_list = f.readlines()
        analy_obj = detailAnalysis(self.strStr)
        #列表去重,生成下表向量
        _alldoc = analy_obj.alldoc()
        i = 0; j = 0
        _alldoc = list(set(_alldoc))
        _alldoc.sort()
        for w in _alldoc:
            self.dict_doc[w] = i
            i+=1
        _taglist = list(set(tag_list))
        _taglist.sort()
        for w in _taglist:
            self.dict_tag[w] = j
            j+=1
        print (self.dict_tag)
        #分词处理
        for sent in self.strList:
            analy_doc = analy_obj.alldoc(sent)
            self.docList.append(analy_doc)
        #print("docList ", self.docList)
        with open(jsonfile, "w") as f:
            f.write(str(self.dict_doc))
        for tag in tag_list:
            analy_doc = analy_obj.alldoc(tag)
            self.tagList.append(analy_doc)

        print ("dict_doc: ",len(self.dict_doc))
        i = 0
        sss = []
        for s in self.docList:
            for w in s:
                sss.append(w)
        sss1 = list(set(sss))
        print ("i: ", len(sss1))
        print ("sss1!=doc:")
        for w in sss1:
            if w not in self.dict_doc.keys():
                print (w)
        print ("doc!=sss1:")
        for w in self.dict_doc.keys():
            if w not in sss1:
                print (w)
    
    def text_conversion (self, contents, tags):
        for sent in contents:
            x = []
            for word in sent:
                if word in self.dict_doc.keys():
                    x.append(self.dict_doc[word])
            self.x_index.append(x)
        for tag in tags:
            print (tag,self.dict_tag[tag],end=" ")
            self.y_index.append(self.dict_tag[tag])
        np.savez("./corpus/mydata.npz", x=self.x_index, y=self.y_index)

if __name__ == "__main__":
    argvList = sys.argv[1:]
    inputfile = argvList[0]
    jsonfile = argvList[1]

    strList = []
    docList = []
    strStr = ""
    with open(inputfile, "r") as f:
        strStr += f.read()
    with open(inputfile, "r") as f:
        strList = f.readlines()
    analy_obj = detailAnalysis(strStr)
    #分词处理
    for sent in strList:
        analy_doc = analy_obj.alldoc(sent)
        docList.append(analy_doc)
    
    #列表去重,生成下表向量
    all_doc = analy_obj.alldoc()
    i = 0;dict_doc = {}
    all_doc = list(set(all_doc))
    all_doc.sort()
    for w in all_doc:
        dict_doc[w] = i
        i+=1
    print (dict_doc)
    with open(jsonfile, "w") as f:
        f.write(str(dict_doc))
