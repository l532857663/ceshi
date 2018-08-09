#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import sys
from pyhanlp import *
import keras
import random
import numpy as np
import json
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from .sql_operating import DatabaseOperating

class DataGeting:

    def __init__(self, db_model_name):
        #获取模型数据库表名
        self.Db_model_name = db_model_name
        self._judgmentModel()
        self.result_json = {}

    #分词处理
    def sentenceSegmentation(self, data_string):
        #文本分词内容
        analysis_doc = []
        analysis_str = ""
        the_str = ""
        keyword_str = ""
        sentence_str = ""

        if data_string == "":
            err = "no string"
            return err

        #HanLP分词
        analysis_doc = HanLP.segment(data_string)
        for word in analysis_doc:
            word_str = str(word)
            analysis_str += word_str + "|-*-|"
            every_arr = word_str.split("/")
            the_str += every_arr[0] + " "
        #语义情感评估
        judge_result = self._dataType(the_str[:-1])
        #HanLP关键词提取
        keyword_list = HanLP.extractKeyword(data_string, 5)
        for word in keyword_list:
            word_str = str(word)
            keyword_str += word_str + "|-*-|"
        #HanLP自动摘要
        sentence_list = HanLP.extractSummary(data_string, 3);
        for word in sentence_list:
            word_str = str(word)
            sentence_str += word_str + "|-*-|"

        self.result_json["analysis_doc"] = analysis_str
        self.result_json["keyword_list"] = keyword_str
        self.result_json["sentence_list"] = sentence_str
        self.result_json["judge_result"] = judge_result

        return self.result_json

    def _dataType(self, the_doc):
        print("传入数据:",the_doc)
        test_arr = []
        test_arr.append(the_doc)
        #传入数据模型化
        tokenizer = Tokenizer (num_words = 5000)
        tokenizer.fit_on_texts(test_arr)
        x_test = tokenizer.texts_to_matrix(test_arr)

        my_model = load_model(self.Model_name)

        #my_model.summary()
        preds = my_model.predict_classes(x_test, verbose=0)
        preds_key = str(preds[0])
        result = self.Model_tag[preds_key]
        return result

    def _judgmentModel(self):
        DO = DatabaseOperating()
        sqlStr = "select model_base_id from `" + self.Db_model_name + "` order by model_base_id desc limit 1"
        data = DO.sqlSelect(sqlStr)
        self._model_data_id = data[0][0]
        self._getModel(DO)
        print("model ready OK")

    def _getModel(self, DO):
        sqlStr = "select model_base_weights,model_data_tag from Lyrical_model_base where model_base_id=%s"
        data = DO.sqlSelect(sqlStr, self._model_data_id)
        if not data:
            print("查无此模型存在")
            return False
        model_weight_byte = data[0][0]
        self.Model_tag = json.loads(data[0][1])
        model_name = "model_wt_new.h5"
        print(model_name)
        with open(model_name, "wb") as f:
            f.write(model_weight_byte)
        self.Model_name = model_name

if __name__ == "__main__":
    strData = sys.argv[1]
    DG = DataGeting()
    res = DG.sentenceSegmentation(strData)
