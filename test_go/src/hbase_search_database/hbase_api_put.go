/**
 *	文件功能：把数据存入hbase数据库
 */

package hbase_search_database

import (
	"fmt"
	"strings"
	"encoding/json"
)

func (self *Hbase_rest) Put_data_api (data_str string) (ok bool) {
	var res bool
	res = self.Set_url_put ()
	if !res {
		fmt.Println("put url set error!")
		ok = false
		return
	}
	fmt.Println("put url:", self.Url)

	self.Set_method_put()
	fmt.Println("put method:", self.Method)

	//string to obj
	put_data_json := new (Hbase_insert_json)
	err := json.Unmarshal([]byte(data_str), &put_data_json)
	if err != nil {
		fmt.Println("json Marshal error:", err)
		ok = false
		return
	}
	fmt.Println("put data json:", put_data_json)
	res = self.Set_data_put(put_data_json)
	if !res {
		fmt.Println("put data set error!")
		ok = false
		return
	}

	res_data := new (Hbase_resp_row)
	res_str := self.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("put database error")
		ok = false
		return
	}
	fmt.Println(res_str)

	ok = true
	return
}
