#!/bin/bash

file_path(){
#    echo "|${2}层："$1
    files=`ls $1`
#    echo "all:"$files
    for file in $files;do
        if [ -d $1"/"$file ]
        then
            #`chmod 777 $path"/"$file`
            echo "|$2文件夹："$file
            file_path $1"/"$file $2"----" $3">>>>"
        else
            echo "|$3文件: "$file
        fi
    done
}               
file_path `pwd` "--" ">>"
