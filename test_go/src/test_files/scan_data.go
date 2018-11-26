package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"
)

func Scan_test_func(Hrest *hbase_search_database.Hbase_rest) {
	url_config := new (hbase_search_database.Hbase_url_config)
//	url_config.Namespace = "default"
	url_config.Tablename = "users_test1"
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
		"batch" : "3"
	}`
	fmt.Println("data:", scanner)
	res = Hrest.Set_data_scanner(scanner)
	if !res {
		fmt.Println("put data set error!")
		return
	}

	res_str := "Scanner"
	err := Hrest.Start(res_str)
	if strings.Compare(err, "error") == 0 {
		fmt.Println("get database error")
		return
	}else if strings.Compare(err, "empty") == 0 {
		fmt.Println("get database empty")
		return
	}
	fmt.Println(err)

	//用扫描器返回数据
	Hrest.Url = err
	fmt.Println("scan url:", Hrest.Url)

	Hrest.Set_method_get()
	fmt.Println("scan method:", Hrest.Method)

	Hrest.Body = ""

	res_data := new (hbase_search_database.Hbase_resp_row)
	err = Hrest.Start(res_data)
	if strings.Compare(err, "error") == 0 {
		fmt.Println("get database error")
		return
	}else if strings.Compare(err, "empty") == 0 {
		fmt.Println("get database empty")
		return
	}
	fmt.Println(err)

	fmt.Println("res_data:", res_data)
	res_data.Xml_base642str()
	fmt.Println("res_data str:", res_data)

}
