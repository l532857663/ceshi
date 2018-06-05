#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *

class Hbaseoperate:
    def __init__(self, addr, port):
        transport = TSocket.TSocket(addr, port)
        self.transport = TTransport.TBufferedTransport(transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = Hbase.Client(self.protocol)
        self.transport.open()
        self.tableList = self.client.getTableNames()

    def __def__(self):
        self.transport.close()

    def __isexistTb(self, tableName):
        if tableName not in self.tableList:
            sys.exit("Error:操作数据表不存在")
        return

    #scanner函数:遍历输出数据库;用作输出目录
    def scanner(self, tableName, columns, startRow, attributes={}):
        self.__isexistTb(tableName)
        scanner = self.client.scannerOpen(tableName, startRow, columns, attributes)
        r = self.client.scannerGet(scanner)
        result= []
        while r:
            r = {
                'row':r[0].row,
                'userinfo:name':r[0].columns[b'userinfo:name'].value,
                'userinfo:age':r[0].columns[b'userinfo:age'].value,}
            result.append(r)
            r = self.client.scannerGet(scanner)
        return result
    
    #getSql函数:定位行查询;查询某行的所有数据
    def getSql(self, tableName, row, attributes={}):
        self.__isexistTb(tableName)
        rsList = []
        result = self.client.getRow(tableName, row, attributes)
        for rs in result:
            r = {
                'row':rs.row,
                'userinfo:name':rs.columns[b'userinfo:name'].value,
                'userinfo:age':rs.columns[b'userinfo:age'].value,}
            rsList.append(r)
        return rsList

    #updateSql函数:定位查询修改;查询某个行、列、属性的值，正确则修改此行的值
    def updateSql(self, tableName, row, column, value, mput, attributes={}):
        self.__isexistTb(tableName)
        result = self.client.checkAndPut(tableName, row, column, value, mput, {})
        if result is True:
            print ("数据修改成功！")

    #addSql函数:添加数据;
    def addSql(self, tableName, row, name, age, attributes={}):
        self.__isexistTb(tableName)
        name = Mutation(column=b'userinfo:name', value=name)
        age = Mutation(column=b'userinfo:age', value=age)
        result = self.client.mutateRow(tableName, row, [name,age], attributes)
        if result is None:
            print ("数据添加成功！")



