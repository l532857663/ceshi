#!/bin/bash

file_path(){
	echo $1
	files=`ls $1`
	for filename in $files;do
		echo $filename
		sed -i 's/'$2'/'$1'/g' $1'/'$filename
		`sync`
	done
}

change_filename(){
	files=`ls $1`
	for filename in $files;do
		file_new=${filename/$2/$1}
		mv $1/$filename $1/$file_new
	done
}

`cp $2 $1 -rfd`
change_filename $1 $2
file_path $1 $2
