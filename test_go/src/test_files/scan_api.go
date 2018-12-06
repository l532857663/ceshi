package test_files

import (
	"fmt"
	"hbase_search_database"
)

func Scan_api_func(Hrest *hbase_search_database.Hbase_rest) {
	res_data, res := Hrest.Scan_data_api(Scan_data, Test_json, Column_find)
	if !res {
		fmt.Println("scan api insert error")
	}

	fmt.Println("scan database OK")
	fmt.Println("the res:", res_data)
}
