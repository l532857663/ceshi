#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,sys
import re

if __name__ == "__main__":
    with open("./corpus/tttNews.txt", "r") as f:
        g_newsList = f.readlines()
    
    kword = r'天网|迪士尼|海洛因|白粉|红烧肉'
    for sent in g_newsList:
        result = re.search(r'.*?('+kword+').*?', sent, re.I|re.S)
        #result = re.match(r'.*?('+kword+').*?', sent, re.I|re.S)
        if result:
            #print(result.group(1),sent)
            rs = result.group(1)+'\n'
            with open("./corpus/ceshiNews.txt", "a") as f:
                f.write(sent)
            with open("./corpus/ceshitag.txt", "a") as f:
                f.write(rs)
    print ("OK")


