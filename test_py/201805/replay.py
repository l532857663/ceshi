#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

def timeReplay(infile,outfile):
    with open(infile,"rb") as f:
        dataArr = f.readlines()
    rRule = rb"\d{4}\-\d{2}-\d{2}\ \d{2}\:\d{2}:\d{2}(\r\n)"
    for sent in dataArr:
        datalist = re.compile(pattern=rRule).findall(sent)
        if datalist:
            datalist = re.sub(rb"\r\n",b"",sent)
            #print(datalist)
            with open(outfile,"ab") as f:
                f.write(datalist)
        else:
            with open(outfile,"ab") as f:
                f.write(sent)
    print("END")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Error:输入 ./replay.py Security.dat b.dat")
    infile = sys.argv[1]
    outfile = sys.argv[2]
    strShell = "rm "+outfile
    os.system(strShell)
    print("BEGIN: "+infile+" >>>> "+outfile)
    timeReplay(infile,outfile)
