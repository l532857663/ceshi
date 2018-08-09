#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
"""
from sql_operating import DatabaseOperating
import os,sys
import time

DO = DatabaseOperating()

def model_sql_ceshi():
    sqlStr = "select corpus_data_detail,corpus_data_evaluate from `%s`"
    data = DO.sqlSelect(sqlStr, "ceshi_corpus_data")
    with open("model_wt1.h5", "rb") as f:
        model_weights = f.read()
    #把数据插入数据库
    time_now = int(time.time())
    # model_weights_string = "0x" + model_weights.hex ()
    model_weights_string = "UNHEX('" + model_weights.hex () + "')"
    sqlStr = "insert into `Lyrical_model_base` (`model_base_weights`,`model_base_timestamp`,`model_base_remark`) values (" + model_weights_string + ",%s,%s)"
    res = DO.sqlAdd(sqlStr, time_now, "ce shi yi xia")
    if res == "OK":
        print("OJBK")
    else:
        print(res, sqlStr)

def file_sql_ceshi(filename):
    file_data_content = []
    file_data_tag = []
    sqltablename = filename.split("/")[-1].split(".")[0]

    #获取测试数据正文内容和对应标签
    with open(filename, "rb") as f:
        file_data = f.readlines()
    print(sqltablename,len(file_data))
    sqlStr = "create table if not exists `" + sqltablename + "_corpus_data` (\
            `corpus_data_id` INT UNSIGNED AUTO_INCREMENT,\
            `corpus_data_title` TEXT,\
            `corpus_data_detail` BLOB NOT NULL,\
            `corpus_data_evaluate` BLOB NOT NULL,\
            PRIMARY KEY (`corpus_data_id`)\
            )ENGINE=InnoDB DEFAULT CHARSET=utf8"
    print(sqlStr)
    res = DO.tableAdd(sqlStr)
    if not res == "OK":
        print("数据库添加失败")
        return False
    i=1
    for line in file_data:
        line_arr = line[:-1].split(b"\t")
        if not len(line_arr) == 2:
            print(i,line_arr)
        else:
            file_data_content.append(line_arr[0])
            file_data_tag.append(line_arr[1])
        i += 1

    #数据导入数据库
    data_len = len(file_data_content)
    print("file_len:",data_len)
    if not len(file_data_tag) == data_len:
        print("数据跟标签不对应")
        return False
    for i in range(data_len):
        if i == 0:
            continue
        sqlStr = "insert into `"+sqltablename+"_corpus_data` (`corpus_data_title`,`corpus_data_detail`,`corpus_data_evaluate`) values ('ceshi"+str(i)+"',%s,%s)"
        res = DO.sqlAdd(sqlStr,file_data_content[i],file_data_tag[i])
        if res == "OK":
            continue
        else:
            print(res, "第", i, "条数据")
            return False
    return True

if __name__ == "__main__":
    print("Start:",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #model_sql_ceshi()
    filepath = sys.argv[1]
    if not os.path.isdir(filepath):
        sys.exit("路径错误")
    for filename in os.listdir(filepath):
        if not file_sql_ceshi(filepath+filename):
            sys.exit("数据读取错误")    

    print("End:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
