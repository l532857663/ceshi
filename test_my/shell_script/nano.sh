#!/bin/bash

file_path(){
#    echo "|${2}层："$1
    files=`ls $1`
#    echo "all:"$files
    for file in $files;do
        if [ -d $1"/"$file ]
        then
            echo "|$2文件夹："$file
            file_path $1"/"$file $2"----" $3">>>>"
        else
            echo "|$3文件: "$file
            if [ ${file:0-4:4} == ".php" ]
            then
                echo "ex $1"/"$file < ../a.vim"
                `ex $1"/"$file < ../a.vim`
            fi
        fi
    done
}               
file_path "/var/www/work/nanoStation0" "--" ">>"
