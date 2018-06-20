#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re
import docxpy
import subprocess

'''
    解析docx文件的内容函数docxAnalysis()；
'''
def docxAnalysis(fname):
    doc = docxpy.process(fname)
    return (doc)

'''
    解析doc文件的内容函数docAnalysis()；
.doc 只解析文字数据，把bytes数据转换成str数据输出
'''
def docAnalysis(fname):
    content = subprocess.check_output(["./www/data_anay/py/bin/antiword", fname])
    content = content.decode()
    return (content)
