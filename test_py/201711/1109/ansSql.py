#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys
import nltk,math,re,pprint

from nltk import load_parser

def haha(query):
    cp = load_parser('grammars/book_grammars/sql1.fcfg')
    trees = list(cp.parse(query.split()))
    #test_1
    answer = trees[0].label()['SEM']
    answer = [s for s in answer if s]
    q = ' '.join(answer)
    print(q)

#query = 'What cities are located in China'
query = 'What cities are in China and have populations above 1,000,000'
haha(query)

print nltk.pos_tag(nltk.word_tokenize(query))
