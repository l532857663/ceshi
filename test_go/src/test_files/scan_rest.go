package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"
//	"encoding/json"
)

func Scan_rest_func(Hrest *hbase_search_database.Hbase_rest) {
	var res bool
	res = Hrest.Set_url_scan ()
	if !res {
		fmt.Println("scan url set error!")
		return
	}
	fmt.Println("scan url:", Hrest.Url)

	Hrest.Set_method_put()
	fmt.Println("scan method:", Hrest.Method)

	//扫描条件
	filter_str := hbase_search_database.Get_filter_str(Test_json)
	fmt.Println("filter_str:", filter_str)
//	filter_str = `{"type": "FilterList","op": "MUST_PASS_ALL","filters": [{"type":"ValueFilter","op":"EQUAL","comparator":{"type":"BinaryComparator","value":"ZG9pbmc="}}]}`
//	filter_str = `{"type":"FirstKeyOnlyFilter"}`
//	filter_str = `{"type":"FilterList","op":"MUST_PASS_ALL","filters":[{"type":"FirstKeyOnlyFilter"},{"type":"ValueFilter","op":"EQUAL","comparator":{"type":"BinaryComparator","value":"c3RhcnQ="}}]}`
	fmt.Println("filter_str:", filter_str)
	fmt.Println("----------------------------------------------------------------")

	//string to obj
	scanner_data := new (hbase_search_database.Hbase_scanner_json)
	scanner_data.Batch = "6"
//	scanner_data.Columns = Column_find
	scanner_data.Filter = filter_str

	fmt.Println("data obj:", scanner_data)
	res = Hrest.Set_data_scan(scanner_data)
	if !res {
		fmt.Println("scan data set error!")
		return
	}

	Hrest.Ask_type = "Scanner"
	res_data := new (hbase_search_database.Hbase_resp_row)
	res_str := Hrest.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("get database error")
		return
	}else if strings.Compare(res_str, "empty") == 0 {
		fmt.Println("get database empty")
		return
	}
	fmt.Println(res_str)
	res_data, res = Hrest.Get_data_scan(res_str)
	if !res {
		fmt.Println("get scanner data error!")
		return
	}
	fmt.Println("all res_data:", res_data)
}
