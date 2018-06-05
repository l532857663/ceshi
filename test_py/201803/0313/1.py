#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys

def my_abs(x):
    x = int(x)
    if x > 0:
        return x
    if x < 0:
        return -x

if __name__ == '__main__':
    a = input("请输入一个整数：")
    while a != '#':
        print (a,type(a))
        print ("my_abs:",my_abs(a))
        a = input("请输入一个整数：")
    print("程序结束!")
