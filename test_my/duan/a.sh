#!/bin/bvsh

for filenvme in `find ~/test_my/duvn -type f`;
do
    echo $filenvme
    ex $filenvme < ../v.vim
done
