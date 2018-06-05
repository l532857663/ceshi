#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import codecs, sys 
import jieba
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

strD = "让我们荡起双浆"
a = list(jieba.cut(strD))

print ("Content-type: text/html")
print ()
print ('<html>')
print ('<head>')
print ("<meta charset=\"utf-8\">")
print ('<title>Hello Word - my first CGI program</title>')
print ('</head>')
#a="环境变量"
print ('<body>')
print ("<b>环境变量</b>")
#print ("<b>"+a+"</b>")
print ("<ul>")
print ('<h1>Hello Word! I am kalo</h1>')
#for key in os.environ.keys():
#    print ("<li><span style='color:green'>%30s </span> : %s </li>" % (key,os.environ[key]))
for key in a:
    print (key+'\n')
print ("</ul>")
print ('</body>')
print ('</html>')
