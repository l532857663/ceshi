#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

def ceshi():
	pattern = r'\{(.*)(abc)(.*)\}'
	sss = "adwba{baba{{fsdaf{}}abcffdfd{}ffdf{}[]}asba}"
	matchobj = re.search(pattern, sss)
	print(matchobj.group(0))
	print(matchobj.group(1))

if __name__ == "__main__":
	ceshi()
