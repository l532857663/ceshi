package file_into_hbase

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

func check_type_info (file_type string, row []string){
	var rowkey string //数据账号
	var timestamp time.Time
	var timestamp_open string //数据时间戳
	var timestamp_close string //数据时间戳
	var data_info string //数据拼接的xml字符串
	var res bool

	if strings.Compare(file_type, "农信") == 0 {
		//设置时间、主键、拼接xml数据
		Global_data.Time_format = "20060102"//不同
		rowkey = row[3]		//不同
		timestamp, res = get_timestring(row[5])//不同
		if res != true {
			return
		}
		timestamp_open, _ = get_timestamp(timestamp)
		data_info = get_info_data1(row, timestamp_open)//不同

	}else if strings.Compare(file_type, "平顶山银行") == 0 {
		Global_data.Time_format = "20060102"
		rowkey = row[0]

		timestamp, res = get_timestring(row[5])
		if res != true {
			return
		}
		timestamp_open, _ = get_timestamp(timestamp)

		timestamp, res = get_timestring(row[6])
		if res != true {
			return
		}
		timestamp_close, _ = get_timestamp(timestamp)
		data_info = get_info_data2(row, timestamp_open, timestamp_close)

	}else if strings.Compare(file_type, "工行") == 0 {
		Global_data.Time_format = "	2006-01-02"
		rowkey = row[6]

		timestamp, res = get_timestring(row[10])
		if res != true {
			return
		}
		timestamp_open, _ = get_timestamp(timestamp)

		timestamp, res = get_timestring(row[16])
		if res != true {
			return
		}
		timestamp_close, _ = get_timestamp(timestamp)
		data_info = get_info_data3 (row, timestamp_open, timestamp_close)
	}else{
		fmt.Println("文件类型不正确")
		return
	}

	//设置Row_key: 账号/customer_account
	row_key := rowkey
	//插入info数据表
	get_info (row_key, data_info)
}

func check_type_all (file_type string, row []string){
	var timestamp time.Time //数据时间
	var rowkey string //数据账号
	var timestamp_base string //数据时间戳
	var timestamp_sign string //数据时间节点
	var data_detail string //数据拼接的xml字符串
	var res bool

	if strings.Compare(file_type, "农信") == 0 {
		//设置时间、主键、拼接xml数据
		var timestamp_ time.Time
		var timestamp1 string
		if len(row[10]) == 5 {
			timestamp1 = "0" + row[10]
		}else{
			timestamp1 = row[10]
		}
		rowkey = row[3]								//不同
		Global_data.Time_format = "20060102"	//不同
		timestamp, res = get_timestring(row[9])
		if res != true {
			return
		}
		Global_data.Time_format = "150405"
		timestamp_, res = get_timestring(timestamp1)
		if res != true {
			return
		}
		timestamp_ = timestamp_.AddDate (timestamp.Year(), int(timestamp.Month())-1, timestamp.Day()-1)
		timestamp_s, _ := get_timestamp(timestamp)
		timestamp_base, timestamp_sign = get_timestamp(timestamp_)
		data_detail = get_detail_data1(row, timestamp_s, timestamp_base)

	}else if strings.Compare(file_type, "平顶山银行") == 0 {
		Global_data.Time_format = "20060102"
		rowkey = row[6]
		timestamp, res = get_timestring(row[0])
		if res != true {
			return
		}
		timestamp_base, timestamp_sign = get_timestamp(timestamp)
		data_detail = get_detail_data2(row, timestamp_base)

	}else if strings.Compare(file_type, "工行") == 0 {
		var time_t time.Time
		var timestamp_t string //交易时间戳
		var time_w time.Time
		var timestamp_w string //工作日期
		var timestamp_ time.Time
		rowkey = row[6]
		Global_data.Time_format = "	2006-01-02"
		time_w, res = get_timestring(row[4])
		if res != true {
			return
		}
		timestamp, res = get_timestring(row[20])
		if res != true {
			return
		}
		Global_data.Time_format = "	15.04.05"
		timestamp_, res = get_timestring(row[21])
		if res != true {
			return
		}
		fmt.Println("原数据：",timestamp, timestamp_)
		timestamp_ = timestamp_.AddDate (timestamp.Year(), int(timestamp.Month())-1, timestamp.Day()-1)
		timestamp_w, _ = get_timestamp(time_w)
		timestamp_s, _ := get_timestamp(timestamp)
		timestamp_base, timestamp_sign = get_timestamp(timestamp_)

		Global_data.Time_format = "	2006-01-02-15.04.05.000000"
		time_t, res = get_timestring(row[3])
		if res != true {
			return
		}
		timestamp_t, _ = get_timestamp(time_t)
		data_detail = get_detail_data3 (row, timestamp_s, timestamp_t, timestamp_w, timestamp_base)
	}else{
		fmt.Println("文件类型不正确")
		return
	}

	//设置Time_row_key: 账号_时间节点    Detail_row_key: 账号_时间节点_时间戳
	time_row_key := rowkey + "_" + timestamp_sign
	detail_row_key := time_row_key + "_" + timestamp_base
	//插入time索引表
	get_time (time_row_key, timestamp_base)
	//插入detail数据表
	get_detail (detail_row_key, data_detail)
}

func get_timestring (timestamp string)(time_stamp time.Time, res bool){
	var err error
	time_stamp, err = time.ParseInLocation (Global_data.Time_format, timestamp, Global_data.Location)
	if err != nil {
		fmt.Println("时间模板格式不正确:",err)
		res = false
		return
	}
	res = true
	return
}
func get_timestamp(timestamp time.Time)(timestamp_base string, timestamp_sign string){
	//获取时间戳
	timestamp_base = strconv.FormatInt (timestamp.Unix (), 10)
	timestamp_sign = strconv.FormatInt (timestamp.Unix () - timestamp.Unix () % 600, 10)
	fmt.Println("时间节点、时间戳",timestamp_base, timestamp_sign)
	return
}
