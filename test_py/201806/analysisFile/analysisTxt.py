#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re
#import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

'''
    解析Text文件的内容函数txtAnalysis()；
'''

def txtAnalysis(fname):
    myF = open(fname,"r")
    contentStr = ""
    for line in myF:
        contentStr += line
    myF.close()
    return (contentStr)

def htmlAnalysis(fname):
    myF = open(fname,"r")
    contentStr = ""
    for line in myF:
        contentStr += line
#        print (line)
    myF.close()
    return (contentStr)
