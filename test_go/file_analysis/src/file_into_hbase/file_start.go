package file_into_hbase

import (
//	"fmt"
)

var Global_data Global

func Start(file_name string, file_type string){
	Global_data.init()

	//文件解析部分
	file_analysis(file_name, file_type)
}
