#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os,sys
import math,re
import nltk,jieba,json

from jpype import *
from os.path import dirname, abspath

class detailAnalysis:

    def __init__ (self, content):
        #停用词词表
        self.lines = [line.strip('\r\n') for line in open('./www/static/stopwords.txt','r')]

        #获取汉语分词
        filepath = "/home/w123/HanLP"
        startJVM(getDefaultJVMPath(), "-Djava.class.path="+filepath+"/hanlp-1.3.4.jar:"+filepath+"/hanlp")
        self.HanLP = JClass('com.hankcs.hanlp.HanLP')

        #获取数据
        self.doc = content 

    def __def__ (self):
        shutdownJVM()

    #关键词
    def keyword (self):
        kWords = self.HanLP.extractKeyword(self.doc, 5)
        keyWord = ""
        for kw in kWords:
            keyWord += "<span>"+kw+"</span>"
        return keyWord

    #摘要
    def summary (self):
        sMarys = self.HanLP.extractSummary(self.doc,2)
        sumMary = ""
        for sm in sMarys:
            sumMary += "<span>"+sm+"</span><br />"
        return sumMary

    #获取词频
    def wordfrequency (self):
        doc = jieba.cut(self.doc)
        modals = []
        counts = []
        fd = nltk.FreqDist(doc)
        #字典排序
        wordNum = sorted(fd.items(), key=lambda e:e[1], reverse=True)

        sumN = 0
        i = 0
        partWord = []
        for tuples in wordNum:
            if tuples[0] not in self.lines and tuples[0] != '\u3000' and tuples[1] >= 3:
                sumN += tuples[1]
                i += 1
                partWord.append(tuples)
        if i == 0 :
            return ("没有符合条件的词频")
        localNum = math.ceil(sumN/i)
        for tps in partWord:
            if tps[1] >= localNum:
                modals.append(tps[0])
                counts.append(tps[1])
        wordF = [modals,counts]
        return wordF




