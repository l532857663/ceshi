#!/usr/bin python
# -*- coding:utf-8 -*-

import os,sys
import nltk,re,pylab

colors = 'rgbcmyk' #red,green,blue,cyan,magenta,yellow,black
def bar_chart(categories,words,counts):
    "Plot a bar chart showing counts for each word by category"
    ind = pylab.arange(len(words))
    width = 1.0/(len(categories)+1.0)
    print width
    bar_groups=[]
    for c in range(len(categories)):
        color=colors[c%len(colors)]
        print type(ind+c*width),counts[categories[c]],c,color
        bars = pylab.bar(ind+c*width,counts[categories[c]],width,color=colors[c%len(colors)])
        bar_groups.append(bars)
        print '---------------------------'
        print bar_groups[0][c]
    pylab.xticks(ind+width,words)
    pylab.legend([b[0] for b in bar_groups],categories,loc='upper left')
    pylab.ylabel('Frequency')
    pylab.title('Frequency of Six Modal Verbs by Genre')
    pylab.savefig('modals.png')
   # pylab.show()

genres = ['news','religion','hobbies','government','adventure']
modals = ['can','could','may','might','must','will']

cfdist = nltk.ConditionalFreqDist(
        (genre,word)
        for genre in genres
        for word in nltk.corpus.brown.words(categories=genre)
        if word in modals)
counts = {}
print nltk.corpus.brown.words(categories='news')
for genre in genres:
    counts[genre] = [cfdist[genre][word] for word in modals]

bar_chart(genres,modals,counts)


