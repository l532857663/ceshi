package hbase_rest

import (
	"fmt"
	"encoding/base64"
	"encoding/xml"
)

func (self *Hbase_rest) Scan_row (table_name string, batch string, begin_row string, end_row string, columns []string, filter_str string) (res_url string, ok bool) {
	self.Mutex.Lock ()
	*self.Flag = 1
	self.Mutex.Unlock ()

	url := self.Addr + "/" + table_name + "/scanner"

	scan_obj := new(Scanner_config)
	scan_obj.Batch = batch
	scan_obj.StartRow = base64.StdEncoding.EncodeToString ([]byte (begin_row))
	scan_obj.EndRow = base64.StdEncoding.EncodeToString ([]byte (end_row))
	for k,v := range columns {
		columns[k] = base64.StdEncoding.EncodeToString ([]byte (v))
	}
	scan_obj.Column = columns
	scan_obj.Filter = filter_str

	scan_byte, err := xml.Marshal(scan_obj)
	if err != nil {
		fmt.Println("xml 转义错误：", err)
	}
	put_body := string(scan_byte)

	fmt.Println(url)
	fmt.Println(put_body)

	_, resp, ok := self.Get_base ("PUT", url, put_body)
	fmt.Println ("scan my data:", resp, ok)

	if (!ok) {
		fmt.Println ("scan error")
		ok = false
		return
	}

	res_url = resp.Header[`Location`][0]
	fmt.Println ("res_url, ", res_url)
	if (!ok) {
		ok = false
		return
	}

	ok = true
	return
}
