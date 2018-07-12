#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import numpy as np
#import keras
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Activation

class SaveModel():
	def __init__ (self, max_words=15000, batch_size=32, epochs=5, test_split=0.2):
		self.max_words = max_words
		self.batch_size = batch_size
		self.epochs = epochs
		self.test_split = test_split

	def getData(self, x, y):
		(x_train, y_train), (x_test, y_test) = self.loadData(x, y)

		num_classes = np.max(y_train) + 1
		print(num_classes, 'classes')

#		print('Vectorizing sequence data...')
#		tokenizer = Tokenizer(num_words=max_words)
#		x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
#		x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
#		print('x_train shape:', x_train.shape)
#		print('x_test shape:', x_test.shape)
		
		y_train = keras.utils.to_categorical(y_train, num_classes)
		y_test = keras.utils.to_categorical(y_test, num_classes)
		print('y_train shape:', y_train.shape)
		print('y_test shape:', y_test.shape)

		argv = {"num_classes":num_classes,
				"x_train":x_train,
				"y_train":y_train,
				"x_test":x_test,
				"y_test":y_test,
				"savepath":'model_wt1.h5'}
		self.saveModel(argv)
	
	def loadData (self, xs, ys, num_words=None, skip_top=0,
									maxlen=None, test_split=0.2, seed=113,
									start_char=1, oov_char=2, index_from=3, **kwargs):
		labels = []
		for y in ys:
			labels.append(int(y))
		labels = np.array(labels)
		np.random.seed(seed)
		indices = np.arange(len(xs))
		np.random.shuffle(indices)
		xs = xs[indices]
		labels = labels[indices]

		idx = int(len(xs) * (1 - test_split))
		x_train, y_train = np.array(xs[:idx]), np.array(labels[:idx])
		x_test, y_test = np.array(xs[idx:]), np.array(labels[idx:])

		return (x_train, y_train), (x_test, y_test)

	def saveModel (self, argv):
		#参数设定
		num_classes = self.argv["num_classes"]
		x_train = self.argv["x_train"]
		y_train = self.argv["y_train"]
		x_test = self.argv["x_test"]
		y_test = self.argv["y_test"]
		savepath = self.argv["savepath"]

		print('Building model...')
		model = Sequential()
		model.add(Dense(512, input_shape=(max_words,)))
		model.add(Activation('relu'))
		model.add(Dropout(0.5))
		model.add(Dense(self.num_classes))
		model.add(Activation('softmax'))
		model.compile(loss='categorical_crossentropy',
					optimizer='adam',
					metrics=['accuracy'])
		self.model = model
		self.model.summary()

		self.model.fit(self.x_train, self.y_train,
						batch_size=batch_size,
						epochs=epochs,
						verbose=1,
						validation_split=0.1)
		score = self.model.evaluate(self.x_test, self.y_test,
									batch_size=batch_size, verbose=1)
		print('Test score:', score[0])
		print('Test accuracy:', score[1])
		self.model.save(self.savepath)
		print("OK")
