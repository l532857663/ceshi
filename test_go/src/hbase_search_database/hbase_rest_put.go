/**
 *	文件功能：把数据存入hbase数据库
 */

package hbase_search_database

import (
	"fmt"
	"strings"
	"encoding/xml"
)

/**
 * 方法功能：设置rest请求的url
 */
func (self *Hbase_rest) Set_url_put () (ok bool) {
	self.Mutex.Lock ()
    *self.Flag = 1
    self.Mutex.Unlock ()

	url := self.Addr + "/"

	url_config := (self.Url_config).(*Hbase_url_config)

	if strings.Compare(url_config.Tablename, "") == 0 {
		ok = false
		return
	}
	url += url_config.Tablename + "/fakerow"

	self.Url = url

	ok = true
	return
}

/**
 * 方法功能：设置rest请求插入数据的xml内容
 */
func (self *Hbase_rest) Set_data_put (data_arr *Hbase_insert_json) (ok bool) {
	insert_data := new (Hbase_insert_config)
	for _, data_map := range data_arr.Datas {
		tmp_row := Map2xml (data_arr.Configs, data_map)
		insert_data.Row = append(insert_data.Row, *tmp_row)
	}
	fmt.Println("all:", insert_data)
	put_body_byte, err := xml.Marshal(insert_data)
	if err != nil {
		fmt.Println("xml Marshal error:", err)
		ok = false
		return
	}
	fmt.Println("all str:", string(put_body_byte))
	self.Body = string(put_body_byte)

	ok = true
	return
}
