#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer

class SaveModel():
    def __init__ (self, savepath="model_wt1.h5", max_words=5000, batch_size=32, epochs=20, test_split=0.2):
        self.Max_words = max_words
        self.Batch_size = batch_size
        self.Epochs = epochs
        self.Test_split = test_split
        self.Savepath = savepath

    def getArgv(self, x, y):
        self.getData(x, y)
        return self.x_data, self.y_data, self.Argv_arr

    def getData(self, x, y):
        (x_train_source, y_train_source), (x_test_source, y_test_source) = self.loadData(x, y)

        num_classes = np.max(y_train_source) + 1

        #向量化数据
        x_train = list(x_train_source)
        tokenizer = Tokenizer (num_words = self.Max_words)
        tokenizer.fit_on_texts(x_train)
        x_train = tokenizer.texts_to_matrix(x_train)

        x_test = list(x_test_source)
        self.x_data = x_test
        self.y_data = list(y_test_source)
        tokenizer.fit_on_texts(x_test)
        x_test = tokenizer.texts_to_matrix(x_test)
        print('x_train shape:', x_train.shape)
        print('x_test shape:', x_test.shape)

        y_train = keras.utils.to_categorical(y_train_source, num_classes)
        y_test = keras.utils.to_categorical(y_test_source, num_classes)
        print('y_train shape:', y_train.shape)
        print('y_test shape:', y_test.shape)

        self.Argv_arr = {"num_classes":num_classes,
                "x_train":x_train,
                "y_train":y_train,
                "x_test":x_test,
                "y_test":y_test}

    def loadData (self, xs, ys, **kwargs):
        #测试数据比例
        test_split = self.Test_split
        xs = np.array(xs)
        labels = np.array(ys)
        #数据量对比
        if not len(xs) == len(labels):
            print("数据错误:",len(xs), len(labels))

        #乱序数据内容
        indices = np.arange(len(xs))
        print("数据量：",len(xs),len(labels),len(indices))
        np.random.shuffle(indices)
        xs = xs[indices]
        if len(indices) < len(labels):
            print("数据错误：",labels, len(labels))
        labels = labels[indices]

        idx = int(len(xs) * (1 - test_split))
        x_train, y_train = xs[:idx], labels[:idx]
        x_test, y_test = xs[idx:], labels[idx:]

        return (x_train, y_train), (x_test, y_test)

    def saveModel (self):
        #参数设定
        argv_arr = self.Argv_arr
        num_classes = argv_arr["num_classes"]
        x_train = argv_arr["x_train"]
        y_train = argv_arr["y_train"]
        x_test = argv_arr["x_test"]
        y_test = argv_arr["y_test"]

        print('Building model...')
        model = Sequential()
        model.add(Dense(512, input_shape=(self.Max_words,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
        my_model = model
        my_model.summary()

        my_model.fit(x_train, y_train,
                batch_size=self.Batch_size,
                epochs=self.Epochs,
                verbose=1,
                validation_split=0.1)
        #保存权重
        my_model.save(self.Savepath)
        #测试模型/可删除
        score = my_model.evaluate(x_test, y_test,
                batch_size=self.Batch_size, verbose=1)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
        for i in range(10):
            ind = np.random.randint(0, len(x_test))
            rowx, rowy = x_test[np.array([ind])], y_test[np.array([ind])]
            print(self.x_data[ind],self.y_data[ind])
            preds = my_model.predict_classes(rowx, verbose=0)
            print (preds)
        print("OK")
