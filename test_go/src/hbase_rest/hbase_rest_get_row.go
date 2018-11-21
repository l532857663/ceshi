package hbase_rest

import (
	"fmt"
	"encoding/base64"
	"bytes"
	"strconv"
)

func (self *Hbase_rest) Get_row (table_name string, row_name string) (res_cell []Cell_config, ok bool) {
	self.Mutex.Lock ()
	*self.Flag = 1
	self.Mutex.Unlock ()

	url := self.Addr + "/" + table_name + "/" + row_name
	tmp_data, _, ok := self.Get_base ("GET", url, "")
	fmt.Println ("my data:", tmp_data, ok)

	if (!ok) {
		ok = false
		return
	}

	tmp_row_name, err := base64.StdEncoding.DecodeString (tmp_data.Row[0].Key)
	if err != nil {
		ok = false
		return
	}

	if bytes.Compare ([]byte (row_name), tmp_row_name) != 0 {
		ok = false
		return
	}

	for _, v := range tmp_data.Row[0].Cell {
		tmp_family_name, err := base64.StdEncoding.DecodeString (v.Column)
		if err != nil {
			ok = false
			return
		}

		tmp_res_data, err := base64.StdEncoding.DecodeString (v.Value)
		if err != nil {
			ok = false
			return
		}

		tmp_timestamp, err := strconv.ParseInt (tmp_data.Row[0].Cell[0].Timestamp, 10, 64)
		if err != nil {
			ok = false
			return
		}

		tmp_res_cell := new (Cell_config)
		tmp_res_cell.Column = string (tmp_family_name)
		tmp_res_cell.Value = string (tmp_res_data)
		tmp_res_cell.Timestamp_int64 = tmp_timestamp

		res_cell = append (res_cell, *tmp_res_cell)
	}

	ok = true

	return
}
