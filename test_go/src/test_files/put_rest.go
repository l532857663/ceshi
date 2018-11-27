package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"

	"encoding/json"
)

var put_data string

func init() {
	//插入数据
	put_data = `{
		"configs" : [
			{"direct":"users"},
			{"indirect":"userinfo:users_username"}
		],
		"datas" : [
			{
				"userinfo:users_username" : "admin",
				"userinfo:users_password" : "123456",
				"userinfo:users_name" : "Administartor"
			},
			{
				"userinfo:users_username" : "qazasdasd",
				"userinfo:users_password" : "123666",
				"userinfo:users_name" : "张三"
			},
			{
				"userinfo:users_username" : "qweasdasd",
				"userinfo:users_password" : "123888",
				"userinfo:users_name" : "李四"
			},
			{
				"userinfo:users_username" : "qazqweqwe",
				"userinfo:users_password" : "666888",
				"userinfo:users_name" : "赵五"
			}
		]
	}`
}

func Put_test_func(Hrest *hbase_search_database.Hbase_rest) {
	url_config := new (hbase_search_database.Hbase_url_config)
	url_config.Tablename = "users_test"

	var res bool
	Hrest.Url_config = url_config
	res = Hrest.Set_url_put ()
	if !res {
		fmt.Println("put url set error!")
		return
	}
	fmt.Println("put url:", Hrest.Url)

	Hrest.Set_method_put()
	fmt.Println("put method:", Hrest.Method)

	put_data_json := new (Hbase_insert_json)
	err := json.Unmarshal([]byte(put_data), &put_data_json)
	if err != nil {
		fmt.Println("json Marshal error:", err)
		ok = false
		return
	}
	res = Hrest.Set_data_put(put_data_json)
	if !res {
		fmt.Println("put data set error!")
		return
	}

	res_data := new (hbase_search_database.Hbase_resp_row)
	err := Hrest.Start(res_data)
	if strings.Compare(err, "error") == 0 {
		fmt.Println("put database error")
		return
	}
	fmt.Println(err)

	fmt.Println("put database OK")
}
