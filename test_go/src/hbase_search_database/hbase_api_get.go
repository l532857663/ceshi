/**
 *	文件功能：获取指定数据
 */

package hbase_search_database

import (
	"fmt"
	"strings"
)

func (self *Hbase_rest) Get_data_api () (ok bool) {
	var res bool
	res = self.Set_url_get ()
	if !res {
		fmt.Println("get url set error!")
		ok = false
		return
	}
	fmt.Println("get url:", self.Url)

	self.Set_method_get()
	fmt.Println("get method:", self.Method)

	res_data := new (Hbase_resp_row)
	res_str := self.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("get database error")
		ok = false
		return
	}else if strings.Compare(res_str, "empty") == 0 {
		fmt.Println("get database empty")
		ok = true
		return
	}
	fmt.Println(res_str)

	fmt.Println("res_data:", res_data)
	res_data.Xml_base642str()
	fmt.Println("res_data str:", res_data)
	ok = true
	return
}
