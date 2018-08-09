#!/usr/bin python
#-*- conding:utf-8 -*-

from _future_ import dicision
import os,sys
import nltk,re,pprint

from nltk.corpus import cmudict,swadesh
from nltk.corpus import wordnet as wn

'''
fr2en = swadesh.entries(['fr','en'])
translate = dict(fr2en)
en2fr = swadesh.entries(['en','fr'])
translate.update(dict(en2fr))
'''
ss = wn.synsets('motorcar')
sss = wn.synset('car.n.01').lemma_names()[1]

print ss,sss
