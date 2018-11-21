/**
 *	文件功能：查询hbase数据库
 */

package hbase_search_database

import (
//	"fmt"
	"strings"
)

func (self *Hbase_rest) Set_url_get () (ok bool) {
	self.Mutex.Lock ()
    *self.Flag = 1
    self.Mutex.Unlock ()

	url := self.Addr + "/"

	url_config := (self.Url_config).(*Hbase_url_config)

	if strings.Compare(url_config.Namespace, "") != 0 {
		url += url_config.Namespace + ":"
	}

	if strings.Compare(url_config.Tablename, "") == 0 {
		ok = false
		return
	}
	url += url_config.Tablename + "/"
	if strings.Compare(url_config.Row, "") == 0 {
		ok = false
		return
	}
	url += url_config.Row + "/"

	if strings.Compare(url_config.Family, "") != 0 {
		url += url_config.Family
		if strings.Compare(url_config.Column, "") != 0 {
			url += ":" + url_config.Column
		}
	}

	self.Url = url

	ok = true
	return
}
