#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
from py_hbase.py_hbaseOperate import Hbaseoperate

if __name__ == "__main__":
    addr = 'localhost'
    port = 9090
    tableName = 'ceshi'.encode()
    row = 'row3'.encode()

    thehbase = Hbaseoperate(addr,port)
    #client = thehbase.client
    #tableList = client.getTableNames()
    #print (tableList)
    #result = thehbase.scanner(tableName,b'',b'row1')
    result = thehbase.getSql(tableName, row)
    #thehbase.addSql(tableName, b'row4', b'xiaobai', b'27')
    print (result)
    
