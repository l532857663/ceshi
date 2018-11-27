/**
 *	文件功能：把数据存入hbase数据库
 */

package hbase_search_database

import (
	"fmt"
	"strings"
	"encoding/xml"
	"encoding/json"
)

func (self *Hbase_rest) Put_data_api (data_str string) (ok bool) {
	//string to obj
	put_data := new (Hbase_insert_json)
	err := json.Unmarshal([]byte(data_str), &put_data)
	if err != nil {
		fmt.Println("json Marshal error:", err)
		ok = false
		return
	}


}
