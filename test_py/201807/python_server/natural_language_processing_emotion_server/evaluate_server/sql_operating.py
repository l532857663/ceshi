#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os,sys
import pymysql
import re

class DatabaseOperating:
    #连接数据库
    Mydb = pymysql.connect("127.0.0.1","root","123456","Lyrical_base")
    def __init__(self):
        self.cursor = self.Mydb.cursor()

    def __del__(self):
        self.Mydb.close()

    #数据库操作 增删改查
    def sqlSelect(self, sqlStr, *tablename):
        try:
            sqlStr = sqlStr%tablename

            self.cursor.execute(sqlStr)
            res = self.cursor.fetchall()
        except:
            #自己定义错误
            print ("Select data Error: unable to fecth data")
            return "FAILURE"
        return res

    def sqlAdd(self, sqlStr, *argv_t):
        try:
            list_arr = []
            for arg in argv_t:
                list_arr.append(self.Mydb.escape(arg))
            sqlStr = sqlStr%tuple(list_arr)
            self.cursor.execute(sqlStr)
            self.Mydb.commit()
            res = "OK"
        except:
            self.Mydb.rollback()
            #自己定义错误
            print ("Add data Error",tuple(list_arr))
            res = "FAILURE"
        return res

    def tableAdd(self,sqlStr):
        try:
            self.cursor.execute(sqlStr)
            self.Mydb.commit()
            res = "OK"
        except:
            self.Mydb.rollback()
            #自己定义错误
            print ("Add table Error")
            return "FAILURE"
        return res
