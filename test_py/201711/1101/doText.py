#!/use/bin python
# -*- conding:utf-8 -*-

from __future__ import division

import os,sys
import nltk,re,pprint
reload(sys)
sys.setdefaultencoding('utf-8')

from urllib import urlopen
from bs4 import BeautifulSoup

url = "http://www.gutenberg.org/files/12345/12345.txt"
raw = urlopen(url).read()
#print type(raw),len(raw),raw[:75]

token = nltk.word_tokenize(raw)
#print len(token)

strR = "I love you Beulah Sands,I want to talk with Miss Sands."
tk = nltk.word_tokenize(strR)
print tk,type(tk)
text = nltk.Text(tk)
#text.concordance('Sands')
#print raw.find('Miss Sands'),"\n"
#print raw[23750:23800]

#llog = urlopen("http://languagelog.ldc.upenn.edu/null/?p=35216").read()
llog = urlopen("http://languagelog.ldc.upenn.edu/nll/?p=35216").read()
print type(llog)

raw1 = BeautifulSoup(llog,'lxml')
strTxt = raw1.get_text()
print strTxt[500:600]
print raw1.title.string
print raw1.find(style="padding-left: 30px;")
myF = open("./doc.html",'w')
myF.write(llog)
myF.close()
myF = open("./doc.txt",'w')
myF.write(strTxt)
myF.close()
