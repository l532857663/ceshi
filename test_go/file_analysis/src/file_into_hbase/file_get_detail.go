package file_into_hbase

import (
	"fmt"
	"encoding/base64"
)

func get_one (data_type string, data string) (res string){
	res = "<Cell column=\""
	res += base64.StdEncoding.EncodeToString ([]byte ("info:" + data_type))
	res += "\">"
	res += base64.StdEncoding.EncodeToString ([]byte (data))
	res += "</Cell>"

	return
}
//农信
func get_detail_data1 (row []string, timestamp string, timestamp_base string) (cmd_str string){
	cmd_str = get_one("transaction_location_number",row[0])
	cmd_str += get_one("transaction_location",row[1])
	cmd_str += get_one("customer_name",row[2])
	cmd_str += get_one("customer_account",row[3])
	cmd_str += get_one("summary",row[4])
	cmd_str += get_one("transaction_money",row[5])
	cmd_str += get_one("account_balance",row[6])
	cmd_str += get_one("other_account",row[7])
	cmd_str += get_one("other_name",row[8])
	cmd_str += get_one("transaction_date",timestamp)
	cmd_str += get_one("working_time",timestamp_base)
	cmd_str += get_one("teller_account",row[11])
	return
}
//平顶山银行
func get_detail_data2 (row []string, timestamp string) (cmd_str string){
	cmd_str  = get_one("transaction_date",timestamp)
	cmd_str += get_one("system_account",row[1])
	cmd_str += get_one("transaction_location_number",row[2])
	cmd_str += get_one("transaction_location",row[3])
	cmd_str += get_one("other_account",row[4])
	cmd_str += get_one("other_name",row[5])
	cmd_str += get_one("customer_account",row[6])
	cmd_str += get_one("customer_name",row[7])
	cmd_str += get_one("transaction_money",row[8])
	cmd_str += get_one("lender",row[9])
	cmd_str += get_one("teller_account",row[10])
	cmd_str += get_one("summary",row[11])
	cmd_str += get_one("account_number",row[12])
	return
}
//工行
func get_detail_data3 (row []string, timestamp, timestamp_t, timestamp_w, timestamp_base string) (cmd_str string){
	cmd_str  = get_one("customer_account",row[0])
	cmd_str += get_one("currency",row[1])
	cmd_str += get_one("account_card_number",row[2])
	cmd_str += get_one("transaction_timestamp",timestamp_t)
	cmd_str += get_one("working_date",timestamp_w)
	cmd_str += get_one("lending_sign",row[5])
	cmd_str += get_one("transaction_money",row[6])
	cmd_str += get_one("account_balance",row[7])
	cmd_str += get_one("comment",row[8])
	cmd_str += get_one("other_account",row[9])
	cmd_str += get_one("other_account_number",row[10])
	cmd_str += get_one("transaction_location",row[11])
	cmd_str += get_one("transaction_location_number(original)",row[12])
	cmd_str += get_one("transaction_location",row[13])
	cmd_str += get_one("transaction_location_number(original)",row[14])
	cmd_str += get_one("account_network_number",row[15])
	cmd_str += get_one("teller_account",row[16])
	cmd_str += get_one("authorization_teller_account",row[17])
	cmd_str += get_one("transaction_code",row[18])
	cmd_str += get_one("service_interface",row[19])
	cmd_str += get_one("transaction_date",timestamp)
	cmd_str += get_one("billing_time",timestamp_base)
	cmd_str += get_one("summary",row[22])
	cmd_str += get_one("money_exchange_logo",row[23])
	cmd_str += get_one("terminal_number",row[24])
	cmd_str += get_one("transaction_location_abbreviation",row[25])
	cmd_str += get_one("other_name",row[26])
	cmd_str += get_one("other_account_open_location",row[27])
	return
}


func get_detail (row_key string, data_detail string) {

	cmd_str := `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="`
	cmd_str += base64.StdEncoding.EncodeToString ([]byte (row_key))
	cmd_str += `">`
	//设置调用函数名
	cmd_str += data_detail
	cmd_str += "</Row></CellSet>"

	fmt.Println(cmd_str)

	url := Global_data.Host + "/"
	url += Global_data.Bank_data_detail
	url += "/fakerow"

	fmt.Println(url)
	//插入数据
	insert_data(cmd_str, url)
}
