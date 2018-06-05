#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

str1 = "\x31\x0a\x35\x38\x34"
str2 = u"ajbiygfawfhbwauiohf"
str3 = "ahsiuhaufhoahwifwaf"

def complay():
    with open("a.dat","rb") as f:
        strData = f.read()
        print(strData)

if __name__ == "__main__":
    print(str1)
    print(str2)
    print(str3)
    complay()
