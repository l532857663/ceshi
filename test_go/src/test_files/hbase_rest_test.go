package test_files

import (
	"testing"
//	"fmt"
	"sync"

//	"strings"
	"hbase_search_database"
)

var Put_data string
var Test_json map[string]string

func Test_get_data (t *testing.T) {
	var mutex sync.Mutex
	var flag int
	Hrest := hbase_search_database.New_hbase_rest ("http://192.168.201.112:9900", &mutex, &flag)
	url_config := new (hbase_search_database.Hbase_url_config)
//	url_config.Namespace = "default"
	url_config.Tablename = "users_test"
	url_config.Row = "users_admin"
//	url_config.Family = "userinfo"
//	url_config.Column = "users_name"
	Hrest.Url_config = url_config

	Get_data()

//	Get_rest_func(Hrest)
//	Put_rest_func(Hrest)
	Scan_rest_func(Hrest)

//	Put_api_func(Hrest)
}

func Get_data() {
	//插入数据
	Put_data = `{
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
	//Scan_row
	Test_json = map[string]string {
		"Type" : "ValueFilter",
		"Op" : "EQUAL",
		"Comparator_Type" : "BinaryComparator",
		"Comparator_Value" : "admin",
	}

	Test_json["Comparator_Type"] = "SubstringComparator"
	Test_json["Comparator_Value"] = "666"
	Test_json["Comparator_Type"] = "RegexStringComparator"
	Test_json["Comparator_Value"] = "123"
	Test_json = map[string]string {
		"Type" : "PrefixFilter",
		"Value" : "users_qaz",
	}

}
