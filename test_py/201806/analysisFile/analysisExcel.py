#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re
import xlrd

'''
    解析Excel文件的内容函数excelAnalysis()；
bk.sheet_names()            文件sheet页名字列表
bk.nsheets                  文件sheet页总数
bk.sheet_by_name('页名')    根据页名获取内容
bk.sheet_by_index(x)        根据定位获取内容
cell_value(x,y)             定位函数，所给位置的值；
row_values(x)                行定位，所给行的全部列的值(列表)；
'''
def excelAnalysis(fname):
    bk = xlrd.open_workbook(fname)
    try:
        sheet1 = bk.sheet_names()[0]
    except:
         sys.exit("no sheet in {} named Sheet1".format(fname))
    allSheet = "{"
    for i in range(bk.nsheets):
        shName = bk.sheet_names()[i]
        sh = bk.sheet_by_name(shName)
        #获取行数
        nrows = sh.nrows
        #获取列数
        ncols = sh.ncols
        content = "sheet '{}'页, nrows '{}'行, ncols '{}'列\n".format(shName,nrows,ncols)
        rs = nrows + ncols
        if rs >= 2:
            #获取第一行第一列数据
            #cell_value = sh.cell_value(0,0)
            #print (cell_value)
            row_list = {}
            #获取各行数据
            row_key = sh.row_values(0)
            for i in range(1,nrows):
                row_data = sh.row_values(i)
                content += "{}\n".format(row_data)
                for i in range(0,ncols):
                    row_list[row_key[i]] = row_data[i]
                    if i > 3:
                        break
                str_list = str(row_list)
                allSheet += str_list + ","
            allSheet += allSheet[0:len(allSheet)-1] + "}"
            print (allSheet)
