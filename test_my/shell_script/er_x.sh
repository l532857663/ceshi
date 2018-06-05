#!/bin/bash

file_path(){
#    echo "|${2}层："$1
    files=`ls $1`
#    echo "all:"$files
    for file in $files;do
        if [ -d $1"/"$file ]
        then
            #echo "|$2文件夹："$file
            file_path $1"/"$file $2"----" $3">>>>"
        else
            #echo "|$3文件: "$file
            if [ ${file:0-4:4} == "json" ]
            then
                echo "|$3文件: "$file
            fi
        fi
    done
}               
file_path "/var/www/work/er_x/www" "--" ">>"
