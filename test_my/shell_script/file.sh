#!/bin/bash
echo "Hello world!"

for file in `ls -lh`;do
    if [ -d "`pwd`/"$file ]
    then
        echo "'"$file"' 是文件夹"
    else
        `chmod u+x $file`
    fi
done

echo "END"
