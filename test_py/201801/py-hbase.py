#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *

def client_conn(addr, port):
    return client
'''
def scanner(client, table, numRows=100, startRow=None, stopRow=None):
    scan = Hbase.TScan(startRow, stopRow)
    scannerId = client.scannerOpenWithScan(table,scan, {})
    rowList = client.scannerGetList(scannerId, numRows)
    print (scannerId, numRows)
    ret = []

    for r in rowList:
        rd = {}
        row = r.row.decode()
        for key in r.columns.keys():
            value = (r.columns[key].value).decode()
            key = key.decode()
            rd[key] = value
        ret.append(rd)
    print (ret)
    '''
def scanner(client, tableName, columns, startRow):
    scanner = client.scannerOpen(tableName, startRow, columns, {})
    print ('二',1,scanner)
    r = client.scannerGet(scanner)
    result= []
    while r:
        result.append(r[0])
        print (scanner)
        r = client.scannerGet(scanner)
    print ("Scanner finished")
    print (result)

def updateSql(client, tableName, row, column, value, mput):
    result = client.checkAndPut(table, row, column, value, mput, {})
    print ('三', result)

def putSql(client, tableName, row, mutations):
    result = client.mutateRow(tableName, row, mutations, {})
    print ('四', result)

def getSql(client, tableName, row):
    result = client.getRow(tableName, row, {})
    print ("一",result)

if __name__ == "__main__":
    addr = 'localhost'
    port = 9090
    transport = TSocket.TSocket(addr, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    transport.open()
    tableList = client.getTableNames()
    name = Mutation(column=b"userinfo:name", value=b"xiaohong",)
    age = Mutation(column=b'userinfo:age', value=b'22')
    for tbName in tableList:
        #getsql(client, tbName, b'row2')
        #scanner(client, tbName, [b'userinfo'], b'row1')
        #updateSql(client, tbName, b'row2', b'userinfo:name', b'xiaoming', name)
        putSql(client, tbName, b'row3', [name,age])
    transport.close()


