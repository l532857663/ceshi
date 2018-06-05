#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from analysisDetail import detailAnalysis

if __name__ == "__main__":
    argvList = sys.argv[1:]
    if argvList:
        for path in argvList:
            with open(path,"r") as f:
                strDoc = f.read()
    doc_obj = detailAnalysis(strDoc)
    try:
        wordF = doc_obj.wordfrequency()
    except:
        types, value, back = sys.exc_info() # 捕获异常
        print("Unexpected error:savefile.py->", types)
        sys.exit(value)
    print("END")
