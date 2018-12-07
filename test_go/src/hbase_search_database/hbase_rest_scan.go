/**
 *	文件功能：用检索条件查scanner扫描器
 */

package hbase_search_database

import (
	"fmt"
	"strings"
	"encoding/xml"
	"encoding/base64"
)

func (self *Hbase_rest) Set_url_scan () (ok bool) {
	self.Mutex.Lock ()
    *self.Flag = 1
    self.Mutex.Unlock ()

	url := self.Addr + "/"

	url_config := (self.Url_config).(*Hbase_url_config)

	if strings.Compare(url_config.Tablename, "") == 0 {
		ok = false
		return
	}
	url += url_config.Tablename + "/scanner"

	if strings.Compare(url_config.Limit, "") != 0 {
		url += "/*?limit=" + url_config.Limit
	}

	self.Url = url

	ok = true
	return
}

func (self *Hbase_rest) Set_data_scan (scanner_data *Hbase_scanner_json) (ok bool) {
	//obj to xml
	scan_obj := new(Scanner_config)
	scan_obj.Batch = scanner_data.Batch
	scan_obj.StartRow = base64.StdEncoding.EncodeToString ([]byte (scanner_data.Begin_row))
	scan_obj.EndRow = base64.StdEncoding.EncodeToString ([]byte (scanner_data.End_row))
	for _, val := range scanner_data.Columns {
		column_base64 := base64.StdEncoding.EncodeToString ([]byte (val))
		scan_obj.Column = append(scan_obj.Column, column_base64)
	}
	scan_obj.Filter = scanner_data.Filter

	fmt.Println("all:", scan_obj)
	scanner_body_byte, err := xml.Marshal(scan_obj)
	if err != nil {
		fmt.Println("xml Marshal error:", err)
		ok = false
		return
	}
	fmt.Println("all str:", string(scanner_body_byte))
	self.Body = string(scanner_body_byte)

	ok = true
	return
}
