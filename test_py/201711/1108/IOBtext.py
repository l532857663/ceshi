#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys,time,math
import nltk,re,pprint
reload(sys)
sys.setdefaultencoding('utf-8')
from nltk.corpus import conll2000
from Unig import UnigramChunker,BigramChunker

text = '''
he PRP B-NP
accepted VBD B-VP
the DT B-NP
position NN I-NP
of IN B-PP
vice NN B-NP
chairman NN I-NP
of IN B-PP
Carlyle NNP B-NP
Group NNP I-NP
, , O
a DT B-NP
merchant NN I-NP
banking NN I-NP
concern NN I-NP
. . O
#ssd = nltk.chunk.conllstr2tree(text, chunk_types=['VP'])
#print ssd

#print conll2000.chunked_sents("train.txt")[99]
grammar = r"NP: {<[CDJNP].*>+}"
cp = nltk.RegexpParser(grammar)
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
print(cp.evaluate(test_sents))
'''

test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
unigram_chunker = UnigramChunker(train_sents)
#print(unigram_chunker.evaluate(test_sents))
bigram_chunker = BigramChunker(train_sents)
print(bigram_chunker.evaluate(test_sents))

#sssd = set(pos for sent in train_sents for (word,pos) in sent.leaves())
postags = sorted(set(pos for sent in train_sents for (word,pos) in sent.leaves()))
print(unigram_chunker.tagger.tag(postags))


