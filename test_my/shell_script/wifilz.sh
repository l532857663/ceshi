#!/bin/bash

serverpath="/home/w123/git_my/wifilz/server_core/src/lib"
pathname="router_firmware_web_server"
#aimsname="passwd_crack_web_server"
filename="router_firmware_web_server.go"

###文件夹遍历，打印全部文件
file_path(){
    echo "file_path--->"
    #echo "|${2}层："$1
    files=`ls $1`
    #echo "all:"$files
###文件夹循环
    for file in $files;do
        ###是文件夹
        if [ -d $1"/"$file ]
        then
            echo "|$2文件夹："$file
            file_path $1"/"$file $2"----" $3">>>>"
        else
            #echo "|$3文件: "$file
           ###选中文件操作
            if [ ${file:0-3:3} == ".go" ]
            then
                echo $file
            fi
        fi
    done
}

do_it(){
    echo "do_it--->"
    files=`ls $1`
    for file in $files;do
        if [ -d $1"/"$file ]
        then
            echo "|$2文件夹："$file
            if [ $file != "index" ]
            then
                `rm -rf $1"/"$file`
            fi
        else
            echo "|$3文件: "$file
            if [ $file != $filename ]
            then
                `mv $1"/"$file $1"/"$filename`
                make_file $1 ${file:0:0-3}
            fi
        fi
    done
}

make_file(){
    echo "ex $1"/"$filename < ./a.vim"
    `"echo :%s/$2/$pathname"`
    `ex $1"/"$filename < ./a.vim`
}

###选中目标文件夹
check_path(){
    echo "check_path--->"
    files=`ls $1`
    for file in $files;do
        if [ -d $1"/"$file ]
        then
            if [ $file == $pathname ]
            then
                echo "|$2文件夹："$file
                #file_path $1"/"$file $2"--" $3">>"
                #do_it $1"/"$file $2"--" $3">>"
                #$4 $1"/"$file $2"--" $3">>"
            else
                echo "|$3文件："$file
            fi
        fi
    done
}               
#check_path $serverpath "--" ">>" "do_it"


#*********************** 一些操作 *******************************#
#echo "ex $1"/"$file < ../a.vim" 对文件进行vi编辑命令

