/**
 * 文件功能：构造hbase数据的类型转换方法
 
 *	请求方式GET:
	 	self.Set_method_get()
	PUT:
		self.Set_method_put()
	POST:
		self.Set_method_post()
	DELETE:
		self.Set_method_delete()

 *	map数据转化成可以用xml参数:
 	Map2xml (tmp_part, tmp_map map[string]string) (tmp_row *Row_config)

 *	Json结构转字符串，xml中提交使用：
 	Json2string (json_obj interface{}) (json_str string)

 *	map结构获取可用的字符串
 	Get_filter_str (tmp_json map[string]string) (tmp_filter_str string)

 *	查询结果的base64转义为string
 	Xml_base642str ()

 */

package hbase_search_database

import (
	"fmt"

	"encoding/json"
	"encoding/base64"
	"strings"
	"strconv"
)

func Map2xml (tmp_part []map[string]string, tmp_map map[string]string) (tmp_row *Row_set){
	tmp_row = new (Row_set)
	//设置key
//	fmt.Println("the_key:",tmp_part)
	var tmp_key_arr []string
	for _, key_pary := range tmp_part {
		for name, value := range key_pary {
			if strings.Compare(name, "direct") == 0 {
				tmp_key_arr = append(tmp_key_arr, value)
			}else if strings.Compare(name, "indirect") == 0 {
				tmp_key_arr = append(tmp_key_arr, tmp_map[value])
			}
		}
	}
	tmp_key := strings.Join(tmp_key_arr, "_")
//	fmt.Println("the_key_arr:",tmp_key_arr)
//	fmt.Println("the_key_str:",tmp_key)
	tmp_row.Key = base64.StdEncoding.EncodeToString ([]byte (tmp_key))
	//设置cell
	for name, value := range tmp_map {
		tmp_cell := new (Cell_set)
		tmp_cell.Column = base64.StdEncoding.EncodeToString ([]byte (name))
		tmp_cell.Value = base64.StdEncoding.EncodeToString ([]byte (value))

		tmp_row.Cell = append (tmp_row.Cell, *tmp_cell)
	}

	return
}

func Json2string (json_obj interface{}) (json_str string) {
	json_byte, err := json.Marshal(json_obj)
	if err != nil {
		fmt.Println("json Marshal error", err)
		return
	}
	json_str = string(json_byte)
	return
}

func Get_filter_str (tmp_json map[string]string) (tmp_filter_str string) {
	fmt.Println("---------------------------------------------")
	fmt.Println("filter_str:", tmp_json)
	filter_tmp := map[string]string {
		"Type" : "",
		"Value" : "",
		"Op" : "",
		"LatestVersion" : "",
		"Comparator_Type" : "",
		"Comparator_Value" : "",
	}
	Comparator_class := map[string]string {
		"BinaryComparator" : "base64",
		"SubstringComparator" : "string",
		"RegexStringComparator" : "string",
	}

	for name, _ := range filter_tmp {
		ss, ok := tmp_json[name]
		if !ok {
			continue
		}
		filter_tmp[name] = ss
	}

	tmp_filter_json := new(Filter_json)
	tmp_filter_json.Type = filter_tmp["Type"]
	tmp_filter_json.Value = base64.StdEncoding.EncodeToString([]byte (filter_tmp["Value"]))
	/*
	if strings.Compare(filter_tmp["LatestVersion"], "true") == 0 {
		tmp_filter_json.LatestVersion = true
	}else{
		tmp_filter_json.LatestVersion = false
	}
	*/
	tmp_filter_json.LatestVersion = filter_tmp["LatestVersion"]
	tmp_filter_json.Op = filter_tmp["Op"]

	tmp_comparator_json := new(Comparator_json)
	tmp_comparator_json.Type = filter_tmp["Comparator_Type"]
	if strings.Compare(Comparator_class[filter_tmp["Comparator_Type"]], "base64") == 0 {
		tmp_comparator_json.Value = base64.StdEncoding.EncodeToString([]byte (filter_tmp["Comparator_Value"]))
	}else if strings.Compare(Comparator_class[filter_tmp["Comparator_Type"]], "string") == 0 {
		tmp_comparator_json.Value = filter_tmp["Comparator_Value"]
	}else{
		fmt.Println("not find the Comparator_Type")
	}

	tmp_filter_json.Comparator = tmp_comparator_json

	tmp_filter_str = Json2string(tmp_filter_json)

	return
}

func (self *Hbase_resp_row) Xml_base642str () {
	for key, row_obj := range self.Row {
		//row_key base64转string
		rowkey_str := ""
		rowkey_byte, err := base64.StdEncoding.DecodeString(row_obj.Key)
		if err != nil {
			fmt.Println("row_key base64 decode failure")
			rowkey_str = row_obj.Key
		}
		rowkey_str = string(rowkey_byte)
//		fmt.Println("Key:",rowkey_str)
		row_obj.Key = rowkey_str

		for k, cell_obj := range row_obj.Cell {
			//row column base64转string
			column_str := ""
			column_byte, err := base64.StdEncoding.DecodeString(cell_obj.Column)
			if err != nil {
				fmt.Println("row column base64 decode failure")
				column_str = cell_obj.Column
			}
			column_str = string(column_byte)
			cell_obj.Column = column_str
			//row value base64转string
			value_str := ""
			value_byte, err := base64.StdEncoding.DecodeString(cell_obj.Value)
			if err != nil {
				fmt.Println("row value base64 decode failure")
				value_str = cell_obj.Value
			}
			value_str = string(value_byte)
			cell_obj.Value = value_str
			//row timestamp_int64
			tmp_timestamp, err := strconv.ParseInt (cell_obj.Timestamp, 10, 64)
			if err != nil {
				fmt.Println("row timestamp to int64 failure")
				tmp_timestamp = int64(0)
			}
			cell_obj.Timestamp_int64 = tmp_timestamp

			row_obj.Cell[k] = cell_obj
		}
		self.Row[key] = row_obj
	}
}

func (self *Hbase_rest) Set_method_get () {
	self.Method = "GET"
}
func (self *Hbase_rest) Set_method_put () {
	self.Method = "PUT"
}
func (self *Hbase_rest) Set_method_post () {
	self.Method = "POST"
}
func (self *Hbase_rest) Set_method_delete () {
	self.Method = "DELETE"
}
