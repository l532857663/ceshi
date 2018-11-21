package hbase_rest

import (
	"fmt"
//	"encoding/xml"
)

func (self *Hbase_rest) Put_row (table_name string, row_data *Row_config) (ok bool) {
	self.Mutex.Lock ()
	*self.Flag = 1
	self.Mutex.Unlock ()

	url := self.Addr + "/" + table_name + "/fakerow"

	put_body := `<CellSet><Row key="`
	put_body += row_data.Key
	put_body += `">`
	for _, v := range row_data.Cell {
		put_body += `<Cell column="`
		put_body += v.Column
		put_body += `">`
		put_body += v.Value
		put_body += `</Cell>`
	}
	put_body += `</Row></CellSet>`

	fmt.Println(url)
	fmt.Println(put_body)

	_, _, ok = self.Get_base ("PUT", url, put_body)

	if (!ok) {
		fmt.Println ("scan error")
		ok = false
		return
	}

	ok = true
	return
}
