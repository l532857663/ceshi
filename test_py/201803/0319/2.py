#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys
import numpy as np

seed = 113
a = [[1243,154,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,11,23254],[4534,18],[5434,43,4863,486]]

start_char = None
index_from = 3
a = np.array(a)
print np.max(a)
np.random.seed(seed)
print "seed: ",seed
indices = np.arange(len(a))
print indices
np.random.shuffle(indices)

print indices,a
print type(a),type(indices)
a = a[indices]
print a

if start_char is not None:
    a = [[start_char] + [w + index_from for w in x] for x in a]
elif index_from:
    a = [[w + index_from for w in x] for x in a]

print a

for i in range(10):
    ind = np.random.randint(0, 838)
    idn = np.array([ind])
    print(ind, idn)
