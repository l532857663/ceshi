#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

from analysisFile.analysisExcel import excelAnalysis
#from analysisFile.analysisDocx import docxAnalysis,docAnalysis
#from analysisFile.analysisTxt import txtAnalysis,htmlAnalysis

def fileAnalysis(fileName):
    suffixFile = fileName.split(".")[-1]
    suffixList = ["xls","docx","doc","text","txt","html"]
    print(suffixList)
    if suffixFile not in suffixList:
        suffixFile = ""
    case = {
            "xls":"excelAnalysis",\
            "docx":"docxAnalysis",\
            "doc":"docAnalysis",\
            "text":"txtAnalysis",\
            "txt":"txtAnalysis",\
            "html":"htmlAnalysis",\
            "":"txtAnalysis"
            }
    try:
        print(case[suffixFile],fileName)
        detailStr = eval(case[suffixFile])(fileName)
#        return detailStr
        print(detailStr)
    except:
        types, value, back = sys.exc_info() # 捕获异常
        print("Unexpected error:analysisFiles.py->", types)
        print(value)
        #sys.excepthook(types, value, back)  # 打印异常
