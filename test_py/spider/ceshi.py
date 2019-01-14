#!/usr/bin/env python3
#!-*- coding:utf-8 -*-

import os,sys
import time

def main(*arg):
	print("START\n")
	sys.stdout.flush()
	print("arg:", arg, "\n")
	sys.stdout.flush()
	for i in arg:
		print(i)
		sys.stdout.flush()
		time.sleep(10)
	with open("./asdasd", "a") as f:
		f.write(i)
	print("END")

if __name__ == "__main__":
	if len(sys.argv) != 5:
		exit("ceshi ceshi")
	a = sys.argv[1]
	b = sys.argv[2]
	c = sys.argv[3]
	d = sys.argv[4]
	main(a,b,c,d)
