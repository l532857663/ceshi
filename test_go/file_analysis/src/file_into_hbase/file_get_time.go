package file_into_hbase

import (
	"fmt"
	"encoding/base64"
)

func get_time (row_key string, timestamp_base string) {

	cmd_str := `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="`
	cmd_str += base64.StdEncoding.EncodeToString ([]byte (row_key))
	cmd_str += `">`
	cmd_str += "<Cell column=\""
	cmd_str += base64.StdEncoding.EncodeToString ([]byte ("info:" + timestamp_base))
	cmd_str += "\">"
	cmd_str += "</Cell>"
	cmd_str += "</Row></CellSet>"

	fmt.Println(cmd_str)

	url := Global_data.Host + "/"
	url += Global_data.Bank_data_time
	url += "/fakerow"

	fmt.Println(url)
	//插入数据
	insert_data(cmd_str, url)
}
