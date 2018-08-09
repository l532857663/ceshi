#!/use/bin/ python
# -*- coding:utf-8 -*-

import os,sys
import nltk,random,math

from nltk.corpus import movie_reviews

documents = [(list(movie_reviews.words(fileid)),category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
#test_1:
#print all_words.items()[:20]
word_features = list(all_words)[:2000]
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features
feat = document_features(movie_reviews.words('pos/cv957_8737.txt'))
print feat.items()[:50]

featuresets = [(document_features(d),c) for (d,c) in documents]
#test_2
print len(featuresets)
train_set,test_set = featuresets[100:],featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier,test_set)
classifier.show_most_informative_features(5)
