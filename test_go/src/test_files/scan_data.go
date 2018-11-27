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
		fmt.Println("put data set error!")
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
	Scanner_get_func(Hrest, err)
}

func Scanner_get_func(Hrest *hbase_search_database.Hbase_rest, url string) {
	//用扫描器返回数据
	Hrest.Url = url
	fmt.Println("scan url:", Hrest.Url)

	Hrest.Set_method_get()
	fmt.Println("scan method:", Hrest.Method)

	Hrest.Ask_type = ""
	Hrest.Body = ""

	res_data := new (hbase_search_database.Hbase_resp_row)
	for {
		res_row := new (hbase_search_database.Hbase_resp_row)
		err := Hrest.Start(res_row)
		if strings.Compare(err, "error") == 0 {
			fmt.Println("get database error")
			break
		}else if strings.Compare(err, "empty") == 0 {
			fmt.Println("get scanner database over")
			break
		}
		fmt.Println(err)

		fmt.Println("res_row:", res_row)
		for _, row := range res_row.Row {
			res_data.Row = append(res_data.Row, row)
		}
	}

	res_data.Xml_base642str()
	fmt.Println("res_data str:", res_data)
}
