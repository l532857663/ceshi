package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"
)

func Scan_test_func(Hrest *hbase_search_database.Hbase_rest) {
	url_config := new (hbase_search_database.Hbase_url_config)
//	url_config.Namespace = "default"
	url_config.Tablename = "users_test"
	url_config.Row = "users_admin"

	var res bool
	Hrest.Url_config = url_config
	res = Hrest.Set_url_scanner ()
	if !res {
		fmt.Println("scan url set error!")
		return
	}
	fmt.Println("scan url:", Hrest.Url)

	Hrest.Set_method_put()
	fmt.Println("scan method:", Hrest.Method)

	//扫描条件
	scanner := `{
		"batch" : "6"
	}`
	fmt.Println("data:", scanner)
	res = Hrest.Set_data_scanner(scanner)
	if !res {
		fmt.Println("scanner data set error!")
		return
	}

	Hrest.Ask_type = "Scanner"
	res_data := new (hbase_search_database.Hbase_resp_row)
	err := Hrest.Start(res_data)
	if strings.Compare(err, "error") == 0 {
		fmt.Println("get database error")
		return
	}else if strings.Compare(err, "empty") == 0 {
		fmt.Println("get database empty")
		return
	}
	fmt.Println(err)
//	Scanner_get_func(Hrest, err)
	res_data, res = Hrest.Get_data_scan(err)
	if !res {
		fmt.Println("get scanner data error!")
		return
	}
	fmt.Println("all res_data:", res_data)
}
