#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys

def count():
    fs = []
    for i in range(1,4):
        def f(i=i):
            return i*i
        fs.append(f)
    return fs

a,b,c = count()
print(a(),b(),c())

d = [1,2,3]
q, w, e = d
print(q,w,e)

def createCounter():
    s = [0]
    print(s)
    def counter():
        s[0] += 1
        return s[0]
    return counter

for i in range(10):
    a = createCounter()
    print("i: "+str(a()))

def asas(i):
    print(i*i)

def log(fc):
    def asss(*args, **kw):
        print(*args, **kw)
        print(fc.__name__)
        return fc(*args, **kw)
    return asss

log(asas)(4, "erafge")
