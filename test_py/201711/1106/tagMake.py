#!/usr/bin/ python
# -*- coding:utf-8 -*-
import os,sys
import nltk,pprint
from nltk.corpus import brown

text0 = "woman man time day year car moment world family house boy child country job state girl place war way case question"
text1 = "made done put said found had seen given left heard been brought got set was called felt in that told"
text2 = "in on to of and for with from at by that into as up out down through about all is"
text3 = "a his this their its her an that our any all one these my in your no some other and"

txt0 = nltk.word_tokenize(text0)
txt1 = nltk.word_tokenize(text1)

#print nltk.pos_tag(txt1)

brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
tag_fd = nltk.FreqDist(tag for (word,tag) in brown_news_tagged)

word_tag_pairs = nltk.bigrams(brown_news_tagged)
noun_preceders = [a[1] for (a,b) in word_tag_pairs if b[1] == 'NOUN']
strT = nltk.FreqDist(noun_preceders)
print strT.most_common()
