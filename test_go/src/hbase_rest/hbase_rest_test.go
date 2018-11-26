package hbase_rest

import (
	"testing"
	"fmt"
	"sync"

//	"strings"
)

func Test_Fuck (t *testing.T) {
	var mutex sync.Mutex
	var flag int
	Hrest := New_hbase_rest ("http://192.168.201.112:9900", &mutex, &flag)

//	Put_func (Hrest)
	Get_func (Hrest)
//	Scan_func (Hrest)
}

func Put_func (Hrest *Hbase_rest) {
	//Put_row
	fmt.Println ("Put_ROW-----------------------------------------------------------")
	test_aaa := map[string]string {
		"key" : "users_",
		"value" : "userinfo:users_username",
	}
	test_sss := map[string]string {
		"userinfo:users_username" : "qazasdasd",
		"userinfo:users_password" : "123666",
		"userinfo:users_name" : "Administartor",
	}
	tmp_row := Map2xml (test_aaa, test_sss)
	fmt.Println(tmp_row)
	fmt.Println (Hrest.Put_row ("users_test", tmp_row))
}

func Get_func (Hrest *Hbase_rest) {
	//Get_row
	fmt.Println ("Get_ROW-----------------------------------------------------------")
	fmt.Println (Hrest.Get_row ("users_test", "users_qazqweqwe"))
}

func Scan_func (Hrest *Hbase_rest) {
	//Scan_row
	fmt.Println ("Scan_ROW-----------------------------------------------------------")
	test_json := map[string]string {
		"Type" : "ValueFilter",
		"Op" : "EQUAL",
		"Comparator_Type" : "BinaryComparator",
		"Comparator_Value" : "admin",
	}

	test_json["Comparator_Type"] = "SubstringComparator"
	test_json["Comparator_Value"] = "666"
	test_json["Comparator_Type"] = "RegexStringComparator"
	test_json["Comparator_Value"] = "123"
	test_json = map[string]string {
		"Type" : "PrefixFilter",
		"Value" : "users_qwe",
	}

	var filter_str string
	tmp_filter_json := Get_filter(test_json)
	fmt.Println("tmp_json:",tmp_filter_json)

	filter_str = Json2string(tmp_filter_json)
	fmt.Println("filter_str:",filter_str)

	var columns_arr []string
//	columns_arr = append(columns_arr, "userinfo:user_username")

	scan_url, ok := Hrest.Scan_row ("users_test", "2", "", "", columns_arr, filter_str)
	if !ok {
		return
	}
	fmt.Println (scan_url)
	res, _ := Hrest.Get_scan (scan_url)
	for _,value := range res {
		fmt.Println("value:", value)
	}
}
