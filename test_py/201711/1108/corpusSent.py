#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys,time,math
import nltk,re,pprint

cp = nltk.RegexpParser('CHUNK: {<V.*> <TO> <V.*>}')
brown = nltk.corpus.brown
'''
for sent in brown.tagged_sents():
    tree = cp.parse(sent)
    for subtree in tree.subtrees():
        if subtree.label() == 'CHUNK': 
            print sent
            print type(tree),tree
            print subtree.label()
            print(subtree)
'''
ssd = [(u'Once', u'CS'), (u'the', u'AT'), (u'grains', u'NNS'), (u'are', u'BER'), (u'ground', u'VBN'), (u',', u','), (u'vitamin', u'NN'), (u'E', u'NN'), (u'begins', u'VBZ'), (u'to', u'TO'), (u'deteriorate', u'VB'), (u'immediately', u'RB'), (u'and', u'CC'), (u'half', u'ABN'), (u'of', u'IN'), (u'it', u'PPO'), (u'is', u'BEZ'), (u'lost', u'VBN'), (u'by', u'IN'), (u'oxidation', u'NN'), (u'and', u'CC'), (u'exposure', u'NN'), (u'to', u'IN'), (u'the', u'AT'), (u'air', u'NN'), (u'within', u'IN'), (u'one', u'CD'), (u'week', u'NN'), (u'.', u'.')]
tree = cp.parse(ssd)
for subtree in tree.subtrees():
    print subtree.label(),1
