/**
 *	文件功能：把数据存入hbase数据库
 */

package hbase_search_database

import (
//	"fmt"
	"strings"
)

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

func (self *Hbase_rest) Set_data_put (data_arr []map[string]interface{}) (ok bool) {

	insert_data := new (Hbase_insert_config)
	for _, val := data_arr {
		config_map := val["configs"].(map[string]string)
		data_map := val["datas"].(map[string]string)
	}
}
