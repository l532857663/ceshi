#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys
import nltk,math


def entropy(labels):
    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(l) for l in freqdist]
    print "items:{},probs:{}".format(freqdist.items(),probs)
    return -sum(p * math.log(p,2) for p in probs)

print (entropy(['male', 'male', 'male', 'male']))
print(entropy(['male', 'female', 'male', 'male']))
print(entropy(['female', 'male', 'female', 'male']))
print(entropy(['female', 'female', 'male', 'female']))
print(entropy(['female', 'female', 'female', 'female']))


s = nltk.FreqDist(['male', 'female', 'male', 'male', 'female', 'female', 'female', 'female'])
for l in s:
    print l,s.freq(l)
