#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys

def ceshi(x, y=1):
    x = x+2
    y = y*3
    return x, y

def char2num(s):
    dist = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}
    return dist[s]

if __name__ == '__main__':
    listD = [1,2,1,3,2,6]
    listD1 = ["AwjsSDiu", "caDwef", "XkFef", "dFFWvc"]
#    strNum = input("请输入数字字符串：")
#    rs = list(map(char2num, strNum))
    rs = list(map(str.lower, listD1))
    print ("转换为：",rs)
    print("程序结束!")
