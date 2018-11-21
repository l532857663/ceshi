package hbase_rest

import (
	// "fmt"
	"encoding/base64"
	// "bytes"
	"strconv"
)

func (self *Hbase_rest) Get_scan (url string) (res_row []Row_config, ok bool) {
	self.Mutex.Lock ()
	*self.Flag = 1
	self.Mutex.Unlock ()

	for {
		tmp_data, resp, tmp_data_ok := self.Get_base ("GET", url, "")
		if (!tmp_data_ok) {
			ok = false
			return
		}

		if resp.StatusCode == 204 {
			ok = true
			return
		}

		for _, row_v := range tmp_data.Row {
			tmp_row_name, err := base64.StdEncoding.DecodeString (row_v.Key)
			if err != nil {
				ok = false
				return
			}
			tmp_res_row := new (Row_config)
			tmp_res_row.Key = string (tmp_row_name)

			for _, cell_v := range row_v.Cell {
				tmp_family_name, err := base64.StdEncoding.DecodeString (cell_v.Column)
				if err != nil {
					ok = false
					return
				}

				tmp_res_data, err := base64.StdEncoding.DecodeString (cell_v.Value)
				if err != nil {
					ok = false
					return
				}

				tmp_timestamp, err := strconv.ParseInt (cell_v.Timestamp, 10, 64)
				if err != nil {
					ok = false
					return
				}

				tmp_res_cell := new (Cell_config)
				tmp_res_cell.Column = string (tmp_family_name)
				tmp_res_cell.Value = string (tmp_res_data)
				tmp_res_cell.Timestamp_int64 = tmp_timestamp

				tmp_res_row.Cell = append (tmp_res_row.Cell, *tmp_res_cell)
			}

			res_row = append (res_row, *tmp_res_row)
		}
	}
}
