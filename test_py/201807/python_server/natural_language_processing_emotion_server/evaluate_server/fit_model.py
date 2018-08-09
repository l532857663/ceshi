#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
import os,sys
import keras
import time
import json
import numpy as np
from keras.models import load_model
from .data_processing import DataProcessing,getTags
from .save_model import SaveModel
from .sql_operating import DatabaseOperating

class ModelModify:
    DO = DatabaseOperating()
    SM = SaveModel()
    Batch_size = SM.Batch_size
    Epochs = SM.Epochs
    Tag_dict = {}

    #模型接口
    def modelInterface(self, db_name, flag, **kwargv):
        sqlStr = "select corpus_data_detail,corpus_data_evaluate from %s" % (db_name)
        data = self.DO.sqlSelect(sqlStr)
        self.Remark = kwargv["model_remark"]
        #模型生成内容 语料库名+模型ID
        self.Model_content = db_name

        #获取生成模型可用的正文内容及可用的对应标签
        DP = DataProcessing()
        file_str_arr = DP.getContents(data)
        tag_arr = DP.getTags(data)
        file_tag_arr = tag_arr[0]
        #获取评价对照表
        sqlStr = "select DISTINCT corpus_data_evaluate from %s" % (db_name)
        data = self.DO.sqlSelect(sqlStr)
        tag_str = ""
        tag_source_arr = []
        for tag in data:
            tag_source_arr.append(tag[0].decode())
            tag_str += tag[0].decode() + " "
        tag_arr = getTags(tag_str)
        for i in range(len(tag_source_arr)):
            self.Tag_dict[tag_arr[0][i]] = tag_source_arr[i]
        print(self.Tag_dict)

        if flag == "重构":
            self.Model_content += " 直接生成"
            #使用数据重构模型
            res = self._modelRefactoring(file_str_arr, file_tag_arr)
            if not res:
                return False
        elif flag == "调整":
            self.Model_content += "+"+kwargv["model_id"]+" 训练生成"
            sqlStr = "select model_base_weights from Lyrical_model_base where model_base_id=%s"
            data = self.DO.sqlSelect(sqlStr,kwargv["model_id"])
            if not data:
                print("查无此模型存在")
                return False
            model_weight_byte = data[0][0]
            model_name = str(time.time()) +"_model_wt.h5"
            print(model_name)
            with open(model_name, "wb") as f:
                f.write(model_weight_byte)

            #使用数据调整已有模型
            res = self._modelAdjustment(file_str_arr, file_tag_arr, model_name)
            if not res:
                return False
        else:
            print("***************:modelInterface flag error")
            return False
        print("modelInterface End")
        return True
    
    #模型重构
    def _modelRefactoring(self, file_str_arr, file_tag_arr):
        #生成模型
        self.SM.Savepath = str(time.time()) +"_model_wt.h5"
        self.SM.getData(file_str_arr, file_tag_arr)
        self.SM.saveModel()
        #获取模型权重数据
        model_weights = ""
        with open(self.SM.Savepath, "rb") as f:
            model_weights = f.read()
        if model_weights == "":
            print("***************:model_weights get error")
            return False
        #保存模型权重
        res = self._modelSaveSql(model_weights)
        if not res:
            print("***************:model save sql error")
            return False
        os.remove(self.SM.Savepath)
        print("Refactoring End")
        return True

    #模型调整校对
    def _modelAdjustment(self, file_str_arr, file_tag_arr, model_name):
        #参数设定
        x_data, y_data, argv_arr = self.SM.getArgv(file_str_arr, file_tag_arr)
        num_classes = argv_arr["num_classes"]
        x_train = argv_arr["x_train"]
        y_train = argv_arr["y_train"]
        x_test = argv_arr["x_test"]
        y_test = argv_arr["y_test"]
        print("ceshi:",model_name)
        my_model = load_model(model_name)
        my_model.fit(x_train, y_train,
                batch_size=self.Batch_size,
                epochs=self.Epochs,
                verbose=1,
                validation_split=0.1)
        my_model.save(model_name)
        print("ceshi1:",model_name)
        #获取模型权重数据
        model_weights = ""
        with open(model_name, "rb") as f:
            model_weights = f.read()
        if model_weights == "":
            print("***************:model_weights get error")
            return False
        #保存模型权重
        res = self._modelSaveSql(model_weights)
        if not res:
            print("***************:model save sql error")
            return False
        print("ceshi2:",model_name)
        os.remove(model_name)
        #测试模型/可删除
        score = my_model.evaluate(x_test, y_test,
                batch_size=self.Batch_size, verbose=1)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
        for i in range(10):
            ind = np.random.randint(0, len(x_test))
            rowx, rowy = x_test[np.array([ind])], y_test[np.array([ind])]
            print(x_data[ind], y_data[ind])
            preds = my_model.predict_classes(rowx, verbose=0)
            print (preds)
        print("Adjustment End")
        return True

    def _modelSaveSql(self, model_weights):
        #把数据插入数据库
        model_weights_string = "UNHEX('" + model_weights.hex () + "')"
        time_now = int(time.time())
        sqlStr = "insert into `Lyrical_model_base` \
                (`model_base_weights`,`model_data_tag`,`model_base_timestamp`,`model_base_content`,`model_base_remark`) \
                values (" + model_weights_string + ",%s,%s,%s,%s)"
        print("tag_dict:",json.dumps(self.Tag_dict))
        res = self.DO.sqlAdd(sqlStr, json.dumps(self.Tag_dict), time_now, self.Model_content, self.Remark)
        if res == "OK":
            return True
        else:
            print(res)
            return False


if __name__ == "__main__":
    print("Start:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    MM = ModelModify()
    res = MM.modelInterface("luoyang1_corpus_data", "重构", model_remark="luoyangshuju")
    #res = MM.modelInterface("ceshi_corpus_data", "调整", model_id="1", model_remark="ce shi yi xia 1")
    if not res:
        print("End***************:modelInterface error")
    print("End:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
