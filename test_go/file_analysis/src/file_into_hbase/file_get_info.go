package file_into_hbase

import (
	"fmt"
	"encoding/base64"
)

//农信
func get_info_data1 (row []string, timestamp_open string) (cmd_str string) {
	cmd_str = get_one("account_opening_location", row[0])
	cmd_str += get_one("account_opening_address", row[1])
	cmd_str += get_one("customer_name", row[2])
	cmd_str += get_one("customer_account", row[3])
	cmd_str += get_one("account_balance", row[4])
	cmd_str += get_one("account_opening_date", timestamp_open)
	cmd_str += get_one("customer_license_number", row[6])
	cmd_str += get_one("customer_phonenumber", row[7])
	cmd_str += get_one("customer_address", row[8])

	return
}

//平顶山银行
func get_info_data2 (row []string, timestamp_open string, timestamp_close string) (cmd_str string) {
	cmd_str  = get_one("customer_account", row[0])
	cmd_str += get_one("deposit_number", row[1])
	cmd_str += get_one("customer_name", row[2])
	cmd_str += get_one("account_opening_number", row[3])
	cmd_str += get_one("account_opening_location", row[4])
	cmd_str += get_one("account_opening_date", timestamp_open)
	cmd_str += get_one("account_close_date", timestamp_close)
	cmd_str += get_one("account_balance", row[7])
	cmd_str += get_one("document_type", row[8])
	cmd_str += get_one("account_number", row[9])

	return
}
//工行
func get_info_data3 (row []string, timestamp_open string, timestamp_close string) (cmd_str string) {
	cmd_str  = get_one("query_id", row[0])
	cmd_str += get_one("customer_name", row[1])
	cmd_str += get_one("certificate_type", row[2])
	cmd_str += get_one("customer_license_number", row[3])
	cmd_str += get_one("customer_number", row[4])
	cmd_str += get_one("account_type", row[5])
	cmd_str += get_one("customer_account", row[6])
	cmd_str += get_one("currency", row[7])
	cmd_str += get_one("sub_account_number", row[8])
	cmd_str += get_one("account_status", row[9])
	cmd_str += get_one("account_opening_date", timestamp_open)
	cmd_str += get_one("account_opening_number", row[11])
	cmd_str += get_one("account_balance", row[12])
	cmd_str += get_one("account_card_number", row[13])
	cmd_str += get_one("account_card_status", row[14])
	cmd_str += get_one("account_balance_date", row[15])
	cmd_str += get_one("account_close_date", timestamp_close)
	cmd_str += get_one("account_close_number", row[17])

	return
}

func get_info (row_key string, data_detail string) {

	cmd_str := `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="`
	cmd_str += base64.StdEncoding.EncodeToString ([]byte (row_key))
	cmd_str += `">`
	//设置调用函数名
	cmd_str += data_detail
	cmd_str += "</Row></CellSet>"

	fmt.Println(cmd_str)

	url := Global_data.Host + "/"
	url += Global_data.Bank_data_info
	url += "/fakerow"

	fmt.Println(url)
	//插入数据
	insert_data(cmd_str, url)
}
