#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys,time
import nltk,math

from nltk.corpus import brown

sents = nltk.corpus.treebank_raw.sents()
tokens = []
boundaries = set()
offset = 0
for sent in sents:
    tokens.extend(sent)
    offset += len(sent)
    boundaries.add(offset-1)
print len(tokens),offset,len(boundaries)
i=1
for w in boundaries:
    print w
    i+=1
    if i==20:
        break




