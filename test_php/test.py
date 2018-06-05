#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys
import re

with open("./result.txt","r") as f:
    arr = f.readlines()
data_arr = []
for str_line in arr:
    rs = re.match(r"^BSS ",str_line)
    if rs:
        data = []
        data_arr.append(data)
        #print "str_line:"+str_line
    data.append(str_line)
print "BEGIN"
print ""
data_all = []
for w in data_arr:
    data_main = {}
    for s in w:
        rs = re.match(r"^BSS ",s)
        if rs:
            data_main["MAC"] = s[4:21]
        if "SSID" in s:
            data_main["SSID"] = s[7:-1]
        if "primary channel" in s:
            data_main["Channel"] = s[22:-1]
    if len(data_main) != 3:
        continue
    data_all.append(data_main)
print len(data_all),data_all
print "END"
