#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import random

def make_password():
	symbol = "abcdefghi%jklm^*nopqrs-tuvwxyz+!@ABCDEFGHIJKLMNOP&QRSTUVWX#YZ01234$56789"
	strSym = ""
	for i in range(16):
		j = random.randint(0,len(symbol)-1)
		ss = symbol[j]
		strSym += ss
	print(strSym)

if __name__ == "__main__":
	make_password()
