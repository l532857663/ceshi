#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import print_function
import os,sys
import numpy as np

class ceshi_data1():
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, C, num_rows):
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)

TRAINING_SIZE = 5
DIGITS = 3
REVERSE = True

MAXLEN = DIGITS + 1 + DIGITS

chars = "0123456789+ "
cs = sorted(set(chars))
c_i = dict((c, i) for i, c in enumerate(cs))
i_c = dict((i, c) for i, c in enumerate(cs))

ctable = ceshi_data1(chars)
questions = ['   17+5', '    2+0', '809+862', '  85+47', '147+556']
expected = ['4   ', '13  ', '140 ', '914 ', '41  ']


print('Vectorization...')
x = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)
y = np.zeros((len(questions), DIGITS + 1, len(chars)), dtype=np.bool)
for i, sentence in enumerate(questions):
    #print i,sentence
    x[i] = ctable.encode(sentence, MAXLEN)
    #print x[i]
    #for i, c in enumerate(sentence):
        #print i, c_i[c]
for i, sentence in enumerate(expected):
    #print i,sentence
    y[i] = ctable.encode(sentence, DIGITS + 1)
    #print y[i]
    #for i, c in enumerate(sentence):
        #print i, c_i[c]

indices = np.arange(len(y))
np.random.shuffle(indices)
x = x[indices]
y = y[indices]

split_at = len(x) - len(x) // 5
(x_train, x_val) = x[:split_at], x[split_at:]
(y_train, y_val) = y[:split_at], y[split_at:]

print('Training Data:')
print(x_train.shape)
print(y_train.shape)

print('Validation Data:')
print(x_val.shape)
print(y_val.shape)

ind = np.random.randint(0, 45)
#rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
print (ind,np.array([ind]))
#q = ctable.decode(rowx[0])
#print (rowx[0], rowy[0])
#print('Q', q[::-1] if REVERSE else q, end=' ')
