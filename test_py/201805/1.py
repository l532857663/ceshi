#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

def timeReplay(infile,outfile):
    '''
    去除时间戳后边的\r\n,合并时间戳与数据
    '''
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

def searchIP(infile,outfile):
    '''
    匹配IP地址,过滤出有IP地址的数据,生成某IP地址的全部数据
    '''
    with open(infile,"rb") as f:
        dataArr = f.readlines()
    rRule = rb"(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)"
    dataAll = []
    i=0;j=0
    for sent in dataArr:
        datalist = re.compile(pattern=rRule).findall(sent)
        if datalist:
            for ipT in datalist:
                dataip = ""
                for ipSymbol in ipT:
                    dataip += ipSymbol.decode()+"."
                dataAll.append(dataip[:-1])
                j+=1
            i+=1
            #print(sent)
            #with open(outfile,"ab") as f:
            #    f.write(sent)
            #with open(outfile,"ab") as f:
            #    strData = str(datasent)+"\n"
            #    f.write(strData)
    dataList = list(set(dataAll))
    for ip in dataList:
        shellStr = "echo 'IPADDRESS:"+ip+"' >> "+outfile
        shellStr1 = "cat "+infile+" | grep -a "+ip+" >> "+outfile
        os.system(shellStr)
        os.system(shellStr1)
    print("ENDALL")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Error:输入 ./1.py Security.dat tmp result.dat")
    infile = sys.argv[1]
    changefile = sys.argv[2]
    outfile = sys.argv[3]
    if os.path.exists(changefile):
        strShell = "rm "+changefile
        os.system(strShell)
    if os.path.exists(outfile):
        strShell = "rm "+outfile
        os.system(strShell)
    print("BEGIN: "+infile+" >>>> "+changefile)
    timeReplay(infile,changefile)
    searchIP(changefile,outfile)
