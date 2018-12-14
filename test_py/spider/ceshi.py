#!/usr/bin/env python3
#!-*- coding:utf-8 -*-

import os,sys
import time

def main(*arg):
	print("START")
	print("arg:", arg)
	for i in range(10):
		print(i)
		time.sleep(2)
	print("END")

if __name__ == "__main__":
	if len(sys.argv) != 5:
		exit("ceshi ceshi")
	a = sys.argv[1]
	b = sys.argv[2]
	c = sys.argv[3]
	d = sys.argv[4]
	main(a, b, c, d)
