#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys
import nltk,math,re,pprint

from nltk.corpus import ieer
from nltk.parse import stanford
from nltk.tokenize import PunktSentenceTokenizer
'''
locs = [('Omnicom', 'IN', 'New York'),
    ('DDB Needham', 'IN', 'New York'),
    ('Kaplan Thaler Group', 'IN', 'New York'),
    ('BBDO South', 'IN', 'Atlanta'),
    ('Georgia-Pacific', 'IN', 'Atlanta')]
query = [e1 for (e1, rel, e2) in locs if e2=='Atlanta']
print(query)
'''
def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
    ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

grammar = "NP: {<DT>?<JJ>*<NN.*>}" 
document = "The fourth Wells account moving to another agency is the packaged paper-products division of Georgia-Pacific Corp., which arrived at Wells only last fall. Like Hertz and the History Channel, it is also leaving for an Omnicom-owned agency, the BBDO South unit of BBDO Worldwide. BBDO South in Atlanta, which handles corporate advertising for Georgia-Pacific, will assume additional duties for brands like Angel Soft toilet tissue and Sparkle paper towels, said Ken Haldin, a spokesman for Georgia-Pacific in Atlanta."
ssd = ie_preprocess(document)
print ssd
cp = nltk.RegexpParser(grammar)
print sentence,cp
result = cp.parse(sentence)
re = cp.parse(ssd[0])
print(re)
