#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
if __name__ == '__main__':
    f = lambda n:n % 2 == 1
    L = list(filter(f, range(1,20)))
    print (L)
