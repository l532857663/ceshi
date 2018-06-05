#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import numpy as np

from mk_file2json2 import dataprocessing

if __name__ == "__main__":
    #eg:./ceshi.py "./corpus/errorNews.txt^*^./corpus/datatag.txt|./1.json"
    argvList = sys.argv[1:]
    if argvList:
        filepath = []
        for path in argvList:
            sl = path.split("|")
            filepath += sl
        print(filepath)
        dataAll = dataprocessing(filepath[0], filepath[1])
    with np.load("./corpus/mydata1.npz") as f:
        xs, labels = f['x'], f['y']
    #print (len(xs),len(labels))
    #print (xs, labels)
    with open("./3.json", "r") as f:
        all_data = f.readlines()
    alldata = eval(all_data[0])
    alltag = eval(all_data[1])
    #print(alltag)
    wordNum = sorted(alldata.items(), key=lambda e:e[1], reverse=True)
    print(len(wordNum))
    xss = {}
    for k,v in wordNum:
        xss[v] = k
    
    #cs = [1151, 565, 3083, 3841]
    cs = xs[0]
    if cs:
        for w in cs:
            print(xss[w-3],end=" ")
    print("END")
