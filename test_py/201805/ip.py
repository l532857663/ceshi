#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

def searchIP(infile,outfile):
    with open(infile,"rb") as f:
        dataArr = f.readlines()
    rRule = rb"(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)"
    dataAll = []
    for sent in dataArr:
        datalist = re.compile(pattern=rRule).findall(sent)
        if datalist:
            #print(sent)
            #with open(outfile,"a") as f:
            #    f.write(sent)
            for ipT in datalist:
                dataip = ""
                for ipSymbol in ipT:
                    dataip += ipSymbol.decode()+"."
                dataAll.append(dataip[:-1])
            #with open(outfile,"a") as f:
            #    strData = str(datasent)+"\n"
            #    f.write(strData)
    dataList = list(set(dataAll))
    for ip in dataList:
        shellStr = "echo 'IPADDRESS:"+ip+"' >> "+outfile
        shellStr1 = "cat "+infile+" | grep -a "+ip+" >> "+outfile
        os.system(shellStr)
        os.system(shellStr1)
    print("END")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Error:输入 ./ip.py a.dat b.dat")
    infile = sys.argv[1]
    outfile = sys.argv[2]
    print("BEGIN: "+infile+" >>>> "+outfile)
    searchIP(infile,outfile)
