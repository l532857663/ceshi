#!/usr/bin/ python
# -*- conding: utf-8 -*-

import os,sys
import nltk,re,pprint
#reload(sys)
#sys.setdefaultencoding('utf-8')
'''
from nltk.corpus import gutenberg
raw = gutenberg.raw('melville-moby_dick.txt')
#print type(raw),len(raw)
raw1 = nltk.word_tokenize(raw)
fsss = nltk.FreqDist(w.lower() for w in raw1 if w.isalpha())
print fsss,fsss.items()[:10]
fdist = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())
print fdist.items()
print fdist.keys()[:5]
'''
rr = 'python hello world,hello Python python'
tet = nltk.word_tokenize(rr)
fstr = nltk.FreqDist(w for w in tet)
fstr.keys()
print fstr.items()
#fstr.plot()

wsj = sorted(set(nltk.corpus.treebank.words()))
fd = nltk.FreqDist(vs for word in wsj
        for vs in re.findall(r'[aeiou]{2,}',word))
print fd.items()[:20]
