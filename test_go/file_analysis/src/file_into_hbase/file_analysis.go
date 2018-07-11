package file_into_hbase

import (
	"fmt"
	"strings"

	"github.com/360EntSecGroup-Skylar/excelize"
)

func file_analysis(file_name string, file_type string) {
	var err error
	file_name_arr := strings.Split(file_name, ".")

	//xlsx文件解析数据
	if file_name_arr[len(file_name_arr)-1] == "xlsx" {
		Global_data.Xlsx_file, err = excelize.OpenFile (file_name)
		if err != nil {
			fmt.Println("xlsx文件解析错误")
			panic(err)
		}

		for _, sheelName := range Global_data.Xlsx_file.GetSheetMap() {
			rows := Global_data.Xlsx_file.GetRows(sheelName)
			type_str := ""
			for row_num, row := range rows {
				if strings.Compare(file_type,"平顶山银行") == 0 {
					if strings.Compare(row[0], "账号") == 0 {
						type_str = "info"
						fmt.Println(row)
						continue
					}else if strings.Compare(row[0], "交易日期") == 0 {
						type_str = "detail"
						fmt.Println(row)
						continue
					}
				}
				if strings.Compare(file_type,"农信") == 0 {
					if strings.Compare(row[0], "开户机构名称") == 0 {
						type_str = "info"
						fmt.Println(row)
						continue
					}else if strings.Compare(row[0], "交易机构号") == 0 {
						type_str = "detail"
						continue
					}
				}
				if strings.Compare(file_type,"工行") == 0 {
					if strings.Compare(row[0], "查询ID") == 0 {
						type_str = "info"
						fmt.Println(row,len(row))
						continue
					}else if strings.Compare(row[0], "账号") == 0 {
						type_str = "detail"
						fmt.Println(row,len(row))
						continue
					}
				}

				if strings.Compare(type_str, "info") == 0 {
					check_type_info(file_type, row)
				}else if strings.Compare(type_str, "detail") == 0 {
					check_type_all(file_type, row)
				}
				if row_num == 20 {
					break
				}
			}
		}
	}else{
		panic("文件类型错误")
	}
}
