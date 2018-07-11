package file_into_hbase

import (
	"time"
	"github.com/360EntSecGroup-Skylar/excelize"
)

type Global struct {
	Host string
	Bank_data_info string
	Bank_data_time string
	Bank_data_detail string
	Time_format string
	Location *time.Location

	Xlsx_file *excelize.File
}

func (self *Global) init () {
	var err error

	self.Host = "http://192.168.11.133:9900"
	self.Bank_data_info = "bank_data_info"
	self.Bank_data_time = "bank_data_time"
	self.Bank_data_detail = "bank_data_detail"
	self.Time_format = "2006-01-02 15:04:05"

	self.Location, err = time.LoadLocation ("Local")
	if err != nil {
		panic(err)
	}
}
