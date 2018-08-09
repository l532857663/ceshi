#! /bin/bash

for filename in `ls sqldata`;do
	echo $filename
	echo "iconv -f gbk -t utf-8 sqldata/$filename -o utfdata/$filename"
	#`iconv -f gbk -t utf-8 'sqldata/'$filename -o 'utfdata/'$filename`
done
