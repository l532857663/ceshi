package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"
)

func Get_test_func(Hrest *hbase_search_database.Hbase_rest) {
	url_config := new (hbase_search_database.Hbase_url_config)
//	url_config.Namespace = "default"
	url_config.Tablename = "users_test"
	url_config.Row = "users_admin"
//	url_config.Family = "userinfo"
//	url_config.Column = "users_name"

	var res bool
	Hrest.Url_config = url_config
	res = Hrest.Set_url_get ()
	if !res {
		fmt.Println("get url set error!")
		return
	}
	fmt.Println("get url:", Hrest.Url)

	Hrest.Set_method_get()
	fmt.Println("get method:", Hrest.Method)

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

	fmt.Println("res_data:", res_data)
	res_data.Xml_base642str()
	fmt.Println("res_data str:", res_data)
}

