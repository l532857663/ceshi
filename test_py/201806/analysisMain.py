#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

from analysisFile.analysisExcel import excelAnalysis
#from analysisFile.analysisDocx import docxAnalysis,docAnalysis
#from analysisFile.analysisTxt import txtAnalysis,htmlAnalysis

if __name__ == "__main__":
    fileList = sys.argv
    if len(fileList) == 1:
        sys.exit("格式错误：eg-> ./analysisMain files/test.xls")
    for i in range(1,len(fileList)):
        fileName = sys.argv[i]
        suffixFile = fileName.split(".")[-1]
        case = {
                "xls":"excelAnalysis",\
                "docx":"docxAnalysis",\
                "doc":"docAnalysis",\
                "text":"txtAnalysis",\
                "txt":"txtAnalysis",\
                "html":"htmlAnalysis",
                }
        try:
            doc = eval(case[suffixFile])(fileName)
            print(doc)
        except:
            types, value, back = sys.exc_info() # 捕获异常
            print("Unexpected error:", types)
            print(value)
            #sys.excepthook(types, value, back)  # 打印异常
