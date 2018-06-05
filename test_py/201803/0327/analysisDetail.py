#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os,sys
import math,re
import nltk,jieba,json

from jpype import *
from os.path import dirname, abspath

class detailAnalysis:

    def __init__ (self, content=None):
        #停用词词表
        self.lines = [line.strip('\r\n') for line in open('./corpus/stopwords.txt','r')]

        #获取汉语分词
        filepath = "/home/w123/HanLP"
        startJVM(getDefaultJVMPath(), "-Djava.class.path="+filepath+"/hanlp-1.3.4.jar:"+filepath+"/hanlp")
        self.HanLP = JClass('com.hankcs.hanlp.HanLP')

        #获取数据
        self.doc = content 

    def __def__ (self):
        shutdownJVM()

    #获取分词数据
    def alldoc (self,_doc = None):
        all_doc = []
        if _doc is not None:
            analy_doc = self.HanLP.segment(_doc)
        else:
            analy_doc = self.HanLP.segment(self.doc)
        a_doc = str(analy_doc).split(",")
        for v in a_doc[0:len(a_doc)-1]:
            if "/" in v:
                slope=v.index("/")
                letter=v[1:slope]
                flage=v[slope:]
                if len(letter)>0 and '\n\u3000\u3000' in letter:
                    all_doc+="\n"
                elif letter not in self.lines and flage != "/w" and letter != "":
                    all_doc.append(letter)
        return all_doc

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
        strTags = ['\n','\r','\u3000',' ']
        modals = []
        counts = []
        fd = nltk.FreqDist(allword)
        #字典排序
        wordNum = sorted(fd.items(), key=lambda e:e[1], reverse=True)
        print("wordNum", wordNum)

        sumN = 0
        i = 0
        partWord = []
        for tuples in wordNum:
            if tuples[0] not in self.lines and tuples[1] >= 3:
                sumN += tuples[1]
                i += 1
                partWord.append(tuples)
        if i == 0 :
            return ("没有符合条件的词频")
        localNum = math.ceil(sumN/i)
        print("partWord", partWord)
        print("localNum", localNum)
        for tps in partWord:
            if tps[1] >= localNum:
                modals.append(tps[0])
                counts.append(tps[1])
        wordF = [modals,counts]
        print("result: ", wordF)
        return wordF




