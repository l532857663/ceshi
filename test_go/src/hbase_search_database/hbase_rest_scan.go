/**
 *	文件功能：把数据存入hbase数据库
 */

package hbase_search_database

import (
	"fmt"
	"strings"
)

func (self *Hbase_rest) Get_data_scan (scanner string) (res_data *Hbase_resp_row, ok bool) {
	self.Mutex.Lock ()
    *self.Flag = 1
    self.Mutex.Unlock ()

	self.Url = scanner
	fmt.Println("scan url:", self.Url)

	self.Set_method_get()
	fmt.Println("scan method:", self.Method)

	self.Ask_type = ""
	self.Body = ""

	res_obj := new (Hbase_resp_row)
	for {
		res_row := new (Hbase_resp_row)
		err := self.Start(res_row)
		if strings.Compare(err, "error") == 0 {
			fmt.Println("get database error")
			ok = false
			return
		}else if strings.Compare(err, "empty") == 0 {
			fmt.Println("get scanner database over")
			break
		}
		fmt.Println(err)

		fmt.Println("res_row:", res_row)
		for _, row := range res_row.Row {
			res_obj.Row = append(res_obj.Row, row)
		}
	}

	res_obj.Xml_base642str()
	res_data = res_obj
	ok = true
	return
}
