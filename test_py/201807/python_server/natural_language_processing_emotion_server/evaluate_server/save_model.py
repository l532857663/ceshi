#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

class SaveModel():
	def __init__ (self):
		self.max_words = 15000
		self.batch_size = 32
		self.epochs = 5

		num_classes = np.max(y_train) + 1
		print(num_classes, 'classes')

		print('Vectorizing sequence data...')
		tokenizer = Tokenizer(num_words=max_words)
		x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
		x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
		print('x_train shape:', x_train.shape)
		print('x_test shape:', x_test.shape)
		
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
		self.saveModel()

	def saveModel (self):
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
