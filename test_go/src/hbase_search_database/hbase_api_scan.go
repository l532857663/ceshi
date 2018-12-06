/**
 *	文件功能：用检索条件查scanner扫描器
 */

package hbase_search_database

import (
	"fmt"

	"strings"
	"encoding/json"
)

func (self *Hbase_rest) Scan_data_api(scanner string, filter_json map[string]string, columns []string) (res_data *Hbase_resp_row, ok bool) {
	var res bool
	res = self.Set_url_scan ()
	if !res {
		fmt.Println("scan url set error!")
		ok = false
		return
	}
	fmt.Println("scan url:", self.Url)

	self.Set_method_put()
	fmt.Println("scan method:", self.Method)

	//扫描条件
	filter_str := Get_filter_str(filter_json)
	fmt.Println("filter_str:", filter_str)

	//string to obj
	scanner_data := new (Hbase_scanner_json)
	err := json.Unmarshal([]byte(scanner), &scanner_data)
	if err != nil {
		fmt.Println("json Marshal error:", err)
		ok = false
		return
	}
	scanner_data.Columns = columns
	scanner_data.Filter = filter_str

	fmt.Println("data obj:", scanner_data)
	res = self.Set_data_scan(scanner_data)
	if !res {
		fmt.Println("scanner data set error!")
		ok = false
		return
	}

	self.Ask_type = "Scanner"
	res_str := self.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("get database error")
		ok = false
		return
	}else if strings.Compare(res_str, "empty") == 0 {
		fmt.Println("get database empty")
		ok = false
		return
	}
	fmt.Println(res_str)
	res_data, res = self.Get_data_scan(res_str)
	if !res {
		fmt.Println("get scanner data error!")
		ok = false
		return
	}
//	fmt.Println("all res_data:", res_data)
	ok = true
	return
}
