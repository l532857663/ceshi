package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"

	"encoding/json"
)

func Put_rest_func(Hrest *hbase_search_database.Hbase_rest) {
	var res bool
	res = Hrest.Set_url_put ()
	if !res {
		fmt.Println("put url set error!")
		return
	}
	fmt.Println("put url:", Hrest.Url)

	Hrest.Set_method_put()
	fmt.Println("put method:", Hrest.Method)

	//插入数据
	put_data_json := make(map[string]map[string]string)
	tmp_data := map[string]string {
		"userinfo:users_username" : "admin",
		"userinfo:users_password" : "123456",
		"userinfo:users_name" : "Administartor",
	}
	tmp_data1 := map[string]string {
	   "userinfo:users_username" : "qazasdasd",
	   "userinfo:users_password" : "123666",
	   "userinfo:users_name" : "张三",
	}
	put_data_json["admin"] = tmp_data
	put_data_json["qazasdasd"] = tmp_data1

	res = Hrest.Set_data_put(put_data_json)
	if !res {
		fmt.Println("put data set error!")
		return
	}

	res_data := new (hbase_search_database.Hbase_resp_row)
	res_str := Hrest.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("put database error")
		return
	}
	fmt.Println(res_str)

	fmt.Println("put database OK")
}
