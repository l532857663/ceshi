#!/bin/bash
echo "Hello world!"


str=`cat test`
echo "str的长度："${#str}
echo "ls -lh: "${str}
echo `expr index "$str" a`
echo "str:112: "${str:57:4}
str1="runoob is a great site"
echo "str: "${str1}
echo `expr index "${str1}" e`
echo "str_index: "${str1:14:2}

for x in "$*";do
    echo $x
done

for x in "$@";do
    echo $x
done
